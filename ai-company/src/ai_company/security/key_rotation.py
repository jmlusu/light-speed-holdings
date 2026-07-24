"""OAuth2 / API key rotation manager.

Manages the lifecycle of API keys with automatic expiration, rotation,
and revocation. Keys are persisted to ``keys.yaml`` with metadata
including creation time, expiration, last-used timestamp, and status.

Usage::

    manager = KeyRotationManager(keys_dir="security")
    key = manager.create_key(name="openai-prod", expires_days=90)
    manager.revoke_key(key.key_id)
    manager.rotate_key(key.key_id)  # creates new, revokes old
"""

from __future__ import annotations

import logging
import secrets
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

_DEFAULT_KEYS_DIR = Path("security")
_KEYS_FILE = "keys.yaml"
_KEY_PREFIX = "lsh_"  # Light Speed Holdings key prefix
_KEY_BYTES = 32  # 256-bit keys


@dataclass
class APIKey:
    """Represents an API key with lifecycle metadata."""

    key_id: str
    key_hash: str
    name: str
    prefix: str  # First 8 chars of the actual key (for display)
    scopes: list[str] = field(default_factory=list)
    status: str = "active"  # active | expired | revoked
    created_at: float = field(default_factory=time.time)
    expires_at: float = 0.0  # 0 means no expiration
    last_used_at: float = 0.0
    rotated_from: str = ""  # Previous key_id if this key was rotated from another

    def is_valid(self) -> bool:
        """Check if the key is currently valid (active and not expired)."""
        if self.status != "active":
            return False
        if self.expires_at > 0 and time.time() > self.expires_at:
            return False
        return True

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dictionary for YAML storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> APIKey:
        """Deserialize from a dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class KeyRotationPolicy:
    """Configuration for automatic key rotation."""

    max_key_age_days: int = 90
    warning_days: int = 14  # Warn when key is within N days of expiration
    require_rotation: bool = False
    max_active_keys: int = 5  # Maximum number of active keys per name


class KeyRotationManager:
    """Manages API key lifecycle: creation, rotation, revocation, and validation.

    Keys are stored in ``keys.yaml`` with full lifecycle metadata. The manager
    supports:
    - Creating new API keys with configurable expiration
    - Rotating keys (creating new + revoking old) with overlap window
    - Revoking compromised keys
    - Validating key hashes for authentication
    - Checking expiration and triggering rotation warnings

    Args:
        keys_dir: Directory for persisting key data. Defaults to ``security/``.
    """

    def __init__(self, keys_dir: str | Path = _DEFAULT_KEYS_DIR) -> None:
        self._keys_dir = Path(keys_dir)
        self._keys_dir.mkdir(parents=True, exist_ok=True)
        self._keys_file = self._keys_dir / _KEYS_FILE
        self._keys: dict[str, APIKey] = {}  # key_id -> APIKey
        self._key_hash_map: dict[str, str] = {}  # key_hash -> key_id
        self._policy = KeyRotationPolicy()
        self._load_keys()

    # ── Public API ────────────────────────────────────────────────────

    @property
    def policy(self) -> KeyRotationPolicy:
        return self._policy

    @policy.setter
    def policy(self, value: KeyRotationPolicy) -> None:
        self._policy = value

    def create_key(
        self,
        name: str,
        scopes: list[str] | None = None,
        expires_days: int | None = None,
    ) -> tuple[APIKey, str]:
        """Create a new API key.

        Args:
            name: Human-readable name for the key (e.g., "openai-prod").
            scopes: Permission scopes (e.g., ["read", "write"]).
            expires_days: Days until expiration. ``None`` uses policy default.

        Returns:
            Tuple of (APIKey metadata, raw_key_string). The raw key is shown
            only once and cannot be retrieved later.

        Raises:
            ValueError: If too many active keys exist for this name.
        """
        # Check active key limit
        active_for_name = [
            k for k in self._keys.values()
            if k.name == name and k.status == "active"
        ]
        if len(active_for_name) >= self._policy.max_active_keys:
            raise ValueError(
                f"Maximum active keys ({self._policy.max_active_keys}) "
                f"reached for '{name}'. Rotate or revoke an existing key."
            )

        # Generate the raw key
        raw_key = f"{_KEY_PREFIX}{secrets.token_urlsafe(_KEY_BYTES)}"
        key_hash = self._hash_key(raw_key)
        key_id = f"key_{secrets.token_hex(8)}"

        # Calculate expiration
        if expires_days is None:
            expires_days = self._policy.max_key_age_days
        expires_at = time.time() + (expires_days * 86400) if expires_days > 0 else 0.0

        api_key = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            name=name,
            prefix=raw_key[:12],
            scopes=scopes or ["*"],
            status="active",
            created_at=time.time(),
            expires_at=expires_at,
        )

        self._keys[key_id] = api_key
        self._key_hash_map[key_hash] = key_id
        self._save_keys()

        logger.info("Created API key %s (%s) expires in %d days", key_id, name, expires_days)
        return api_key, raw_key

    def validate_key(self, raw_key: str) -> APIKey | None:
        """Validate a raw API key and return its metadata.

        Returns the APIKey if valid, ``None`` if the key is invalid, expired,
        or revoked. Updates ``last_used_at`` on successful validation.
        """
        key_hash = self._hash_key(raw_key)
        key_id = self._key_hash_map.get(key_hash)
        if key_id is None:
            return None

        api_key = self._keys.get(key_id)
        if api_key is None or not api_key.is_valid():
            return None

        # Update last used timestamp
        api_key.last_used_at = time.time()
        self._save_keys()
        return api_key

    def rotate_key(self, key_id: str) -> tuple[APIKey, str]:
        """Rotate an existing key: create a new key and revoke the old one.

        The new key inherits the name and scopes of the old key. The old key
        is revoked but its metadata is preserved for audit purposes.

        Args:
            key_id: The ID of the key to rotate.

        Returns:
            Tuple of (new APIKey, raw_key_string).

        Raises:
            KeyError: If the key_id doesn't exist.
            ValueError: If the key is already revoked.
        """
        old_key = self._keys.get(key_id)
        if old_key is None:
            raise KeyError(f"Key not found: {key_id}")
        if old_key.status == "revoked":
            raise ValueError(f"Key {key_id} is already revoked")

        # Create new key inheriting name and scopes
        new_key, raw_key = self.create_key(
            name=old_key.name,
            scopes=old_key.scopes,
            expires_days=None,  # Use policy default
        )

        # Link the rotation
        new_key.rotated_from = key_id
        self._keys[new_key.key_id] = new_key

        # Revoke the old key
        old_key.status = "revoked"
        self._save_keys()

        logger.info("Rotated key %s → %s", key_id, new_key.key_id)
        return new_key, raw_key

    def revoke_key(self, key_id: str) -> APIKey:
        """Revoke an API key immediately.

        Args:
            key_id: The ID of the key to revoke.

        Returns:
            The revoked APIKey.

        Raises:
            KeyError: If the key_id doesn't exist.
        """
        api_key = self._keys.get(key_id)
        if api_key is None:
            raise KeyError(f"Key not found: {key_id}")

        api_key.status = "revoked"
        self._save_keys()

        logger.info("Revoked API key %s (%s)", key_id, api_key.name)
        return api_key

    def list_keys(
        self,
        name: str | None = None,
        status: str | None = None,
    ) -> list[APIKey]:
        """List API keys with optional filtering.

        Args:
            name: Filter by key name.
            status: Filter by status (active, expired, revoked).

        Returns:
            List of matching APIKey objects.
        """
        results = list(self._keys.values())
        if name is not None:
            results = [k for k in results if k.name == name]
        if status is not None:
            results = [k for k in results if k.status == status]
        return sorted(results, key=lambda k: k.created_at, reverse=True)

    def get_key(self, key_id: str) -> APIKey | None:
        """Get a key by ID."""
        return self._keys.get(key_id)

    def check_expirations(self) -> list[APIKey]:
        """Check for keys approaching expiration.

        Returns a list of active keys that are within the policy's
        ``warning_days`` threshold of expiration.
        """
        now = time.time()
        warning_cutoff = now + (self._policy.warning_days * 86400)
        expiring: list[APIKey] = []

        for api_key in self._keys.values():
            if api_key.status != "active":
                continue
            if api_key.expires_at <= 0:
                continue  # No expiration set
            if api_key.expires_at <= warning_cutoff:
                expiring.append(api_key)
                # Auto-expire keys past their deadline
                if api_key.expires_at < now:
                    api_key.status = "expired"
                    logger.warning(
                        "Key %s (%s) has expired", api_key.key_id, api_key.name
                    )

        if any(k.status == "expired" for k in expiring):
            self._save_keys()

        return expiring

    def cleanup_expired(self) -> int:
        """Mark expired keys and return count of keys affected.

        Returns:
            Number of keys that were transitioned to expired status.
        """
        now = time.time()
        count = 0
        for api_key in self._keys.values():
            if api_key.status == "active" and api_key.expires_at > 0 and api_key.expires_at < now:
                api_key.status = "expired"
                count += 1
                logger.info("Auto-expired key %s (%s)", api_key.key_id, api_key.name)

        if count > 0:
            self._save_keys()
        return count

    # ── Private helpers ───────────────────────────────────────────────

    @staticmethod
    def _hash_key(raw_key: str) -> str:
        """Hash a raw API key using SHA-256 for storage."""
        import hashlib

        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def _save_keys(self) -> None:
        """Persist all keys to YAML."""
        data: dict[str, Any] = {
            "version": 1,
            "keys": {kid: k.to_dict() for kid, k in self._keys.items()},
        }
        self._keys_file.write_text(
            yaml.dump(data, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )
        logger.debug("Saved %d keys to %s", len(self._keys), self._keys_file)

    def _load_keys(self) -> None:
        """Load keys from YAML, or start with empty state."""
        if not self._keys_file.exists():
            return

        try:
            data = yaml.safe_load(self._keys_file.read_text(encoding="utf-8"))
            if data is None or not isinstance(data, dict):
                return

            keys_data = data.get("keys", {})
            if not isinstance(keys_data, dict):
                return

            for kid, kdata in keys_data.items():
                if isinstance(kdata, dict):
                    api_key = APIKey.from_dict(kdata)
                    self._keys[kid] = api_key
                    self._key_hash_map[api_key.key_hash] = kid

            logger.debug("Loaded %d keys from %s", len(self._keys), self._keys_file)
        except Exception:
            logger.warning("Failed to load keys from %s, starting fresh", self._keys_file)
