"""API key rotation manager for LLM provider keys.

Manages rotation of LLM provider API keys with:
- Scheduled rotation (configurable interval)
- Graceful transition (overlap period with old key)
- Audit logging for rotation events
- Fail-closed: rejects requests if no valid key available
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_KEY_DIR = Path("security")
_API_KEYS_FILE = "llm_api_keys.json"
_DEFAULT_ROTATION_INTERVAL = 86400.0  # 24 hours
_DEFAULT_OVERLAP_PERIOD = 3600.0  # 1 hour


@dataclass
class APIKeyMetadata:
    """Metadata for a single API key."""

    provider: str
    key_id: str
    key_encrypted: str
    created_at: float
    rotated_at: float | None = None
    is_active: bool = True
    is_previous: bool = False


@dataclass
class ProviderKeyState:
    """Current state of API keys for a provider."""

    provider: str
    current_key_id: str | None = None
    previous_key_id: str | None = None
    current_key: str | None = None  # decrypted for runtime use
    previous_key: str | None = None  # decrypted for transition period
    last_rotation: float | None = None
    rotation_interval: float = _DEFAULT_ROTATION_INTERVAL
    overlap_period: float = _DEFAULT_OVERLAP_PERIOD

    def is_rotation_due(self) -> bool:
        """Check if key rotation is due."""
        if self.last_rotation is None:
            return True
        return (time.time() - self.last_rotation) >= self.rotation_interval

    def is_in_overlap(self) -> bool:
        """Check if we're in the overlap period after rotation."""
        if self.last_rotation is None or self.previous_key is None:
            return False
        return (time.time() - self.last_rotation) < self.overlap_period


class APIKeyManager:
    """Manages API key rotation for LLM providers.

    Features:
    - Per-provider key management with rotation scheduling
    - Dual-key window (current + previous) for graceful transition
    - Encrypted storage of keys at rest
    - Audit logging of all rotation events
    - Fail-closed: returns None if no valid key available

    Args:
        key_dir: Directory for persisting key metadata. Defaults to ``security/``.
        master_secret_env: Environment variable for master encryption secret.
            Defaults to ``LLM_API_KEY_MASTER`` falling back to ``JWT_SECRET_KEY``.
    """

    def __init__(
        self,
        key_dir: str | Path = _DEFAULT_KEY_DIR,
        master_secret_env: str = "LLM_API_KEY_MASTER",
    ) -> None:
        self._key_dir = Path(key_dir)
        self._key_dir.mkdir(parents=True, exist_ok=True)
        self._keys_file = self._key_dir / _API_KEYS_FILE
        self._master_secret_env = master_secret_env
        self._providers: dict[str, ProviderKeyState] = {}
        self._loaded = False
        self._load_or_create()

    def get_key(self, provider: str) -> str | None:
        """Get the current active API key for a provider.

        Returns the key if available, None if no key is configured (fail-closed).
        During overlap period, returns the current key (new key takes precedence).
        """
        self._ensure_loaded()
        state = self._providers.get(provider)
        if state is None or state.current_key is None:
            logger.warning("No active API key for provider %s (fail-closed)", provider)
            return None
        return state.current_key

    def get_previous_key(self, provider: str) -> str | None:
        """Get the previous API key for a provider (during overlap period)."""
        self._ensure_loaded()
        state = self._providers.get(provider)
        if state is None or state.previous_key is None:
            return None
        if not state.is_in_overlap():
            return None
        return state.previous_key

    def set_key(self, provider: str, api_key: str) -> str:
        """Set/rotate the API key for a provider.

        Returns the new key ID.
        """
        self._ensure_loaded()
        state = self._providers.get(provider)
        if state is None:
            state = ProviderKeyState(provider=provider)
            self._providers[provider] = state

        # If there's an existing current key, move it to previous
        if state.current_key is not None:
            state.previous_key = state.current_key
            state.previous_key_id = state.current_key_id

        state.current_key = api_key
        state.current_key_id = self._generate_key_id(api_key)
        state.last_rotation = time.time()
        self._save()
        logger.info("API key set for provider %s: %s", provider, state.current_key_id)
        return state.current_key_id

    def rotate_key(self, provider: str, new_key: str | None = None) -> str | None:
        """Rotate the API key for a provider.

        If new_key is provided, uses it. Otherwise, generates a new key
        (for providers that support programmatic key generation).

        Returns the new key ID, or None if rotation not possible.
        """
        self._ensure_loaded()
        state = self._providers.get(provider)
        if state is None:
            logger.warning("No existing key for provider %s, cannot rotate", provider)
            return None

        if new_key is None:
            logger.warning("No new key provided for rotation of %s", provider)
            return None

        old_key_id = state.current_key_id
        state.previous_key = state.current_key
        state.previous_key_id = state.current_key_id
        state.current_key = new_key
        state.current_key_id = self._generate_key_id(new_key)
        state.last_rotation = time.time()
        self._save()

        self._audit_log(
            provider=provider,
            event="key_rotated",
            old_key_id=old_key_id,
            new_key_id=state.current_key_id,
        )
        logger.info(
            "API key rotated for provider %s: %s → %s", provider, old_key_id, state.current_key_id
        )
        return state.current_key_id

    def is_rotation_due(self, provider: str) -> bool:
        """Check if key rotation is due for a provider."""
        self._ensure_loaded()
        state = self._providers.get(provider)
        if state is None:
            return True
        return state.is_rotation_due()

    def get_status(self, provider: str) -> dict[str, Any] | None:
        """Get key status for a provider."""
        self._ensure_loaded()
        state = self._providers.get(provider)
        if state is None:
            return None
        return {
            "provider": provider,
            "current_key_id": state.current_key_id,
            "previous_key_id": state.previous_key_id,
            "last_rotation": state.last_rotation,
            "rotation_due": state.is_rotation_due(),
            "in_overlap": state.is_in_overlap(),
            "rotation_interval": state.rotation_interval,
            "overlap_period": state.overlap_period,
        }

    def list_providers(self) -> list[str]:
        """List all configured providers."""
        self._ensure_loaded()
        return list(self._providers.keys())

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self._load_or_create()

    def _generate_key_id(self, key: str) -> str:
        """Generate a short deterministic key identifier."""
        import hashlib

        return hashlib.sha256(key.encode()).hexdigest()[:12]

    def _get_master_secret(self) -> bytes:
        """Read the master secret from environment variables."""
        secret = os.environ.get(self._master_secret_env) or os.environ.get("JWT_SECRET_KEY")
        if not secret:
            raise RuntimeError(
                f"No master secret found. Set {self._master_secret_env} or JWT_SECRET_KEY."
            )
        return secret.encode("utf-8")

    def _encrypt_key(self, raw_key: str) -> str:
        """Encrypt an API key for storage."""
        import base64
        import secrets

        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF

        master = self._get_master_secret()
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"ai-company-llm-api-key-v1",
        )
        derived_key = hkdf.derive(master)
        nonce = secrets.token_bytes(12)
        aesgcm = AESGCM(derived_key)
        ciphertext = aesgcm.encrypt(nonce, raw_key.encode(), None)
        blob = nonce + ciphertext
        return base64.b64encode(blob).decode("ascii")

    def _decrypt_key(self, encrypted_b64: str) -> str:
        """Decrypt an API key from storage."""
        import base64

        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF

        master = self._get_master_secret()
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"ai-company-llm-api-key-v1",
        )
        derived_key = hkdf.derive(master)
        blob = base64.b64decode(encrypted_b64)
        nonce = blob[:12]
        ciphertext = blob[12:]
        aesgcm = AESGCM(derived_key)
        return aesgcm.decrypt(nonce, ciphertext, None).decode()

    def _save(self) -> None:
        """Persist key metadata (encrypted keys) to disk."""
        meta: dict[str, Any] = {}
        for provider, state in self._providers.items():
            if state.current_key is not None:
                meta[provider] = {
                    "current_key_id": state.current_key_id,
                    "current_key_encrypted": self._encrypt_key(state.current_key),
                    "previous_key_id": state.previous_key_id,
                    "previous_key_encrypted": (
                        self._encrypt_key(state.previous_key) if state.previous_key else None
                    ),
                    "last_rotation": state.last_rotation,
                    "rotation_interval": state.rotation_interval,
                    "overlap_period": state.overlap_period,
                }
        self._keys_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        logger.debug("API key metadata saved to %s", self._keys_file)

    def _load_or_create(self) -> None:
        """Load existing key metadata or create empty state."""
        if self._loaded:
            return

        if self._keys_file.exists():
            try:
                meta = json.loads(self._keys_file.read_text(encoding="utf-8"))
                for provider, data in meta.items():
                    state = ProviderKeyState(
                        provider=provider,
                        current_key_id=data.get("current_key_id"),
                        previous_key_id=data.get("previous_key_id"),
                        last_rotation=data.get("last_rotation"),
                        rotation_interval=data.get("rotation_interval", _DEFAULT_ROTATION_INTERVAL),
                        overlap_period=data.get("overlap_period", _DEFAULT_OVERLAP_PERIOD),
                    )
                    if data.get("current_key_encrypted"):
                        state.current_key = self._decrypt_key(data["current_key_encrypted"])
                    if data.get("previous_key_encrypted"):
                        state.previous_key = self._decrypt_key(data["previous_key_encrypted"])
                    self._providers[provider] = state
                self._loaded = True
                logger.debug("Loaded existing API keys from %s", self._keys_file)
                return
            except (json.JSONDecodeError, KeyError, ValueError) as exc:
                logger.warning("Failed to load API key metadata, starting fresh: %s", exc)

        self._loaded = True
        logger.info("Created new API key manager (no existing keys)")

    def _audit_log(self, provider: str, event: str, **kwargs: Any) -> None:
        """Write an audit log entry for key rotation events."""
        from ai_company.audit.events import AuditEvent, AuditEventType
        from ai_company.audit.integration import get_writer

        try:
            writer = get_writer()
            if writer is None:
                return
            writer.write(
                AuditEvent(
                    event_type=AuditEventType.API_KEY_ROTATED,
                    agent_id=f"system:{provider}",
                    tool="api_key_rotation",
                    args=dict(kwargs),
                    metadata={"rotation_event": event, "resource": f"api_key:{provider}"},
                )
            )
        except Exception:  # noqa: BLE001 - audit logging is best-effort
            logger.debug("Audit logging failed for API key event", exc_info=True)


_api_key_manager: APIKeyManager | None = None


def get_api_key_manager(
    key_dir: str | Path = _DEFAULT_KEY_DIR,
    master_secret_env: str = "LLM_API_KEY_MASTER",
) -> APIKeyManager:
    """Get the singleton API key manager instance."""
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = APIKeyManager(key_dir=key_dir, master_secret_env=master_secret_env)
    return _api_key_manager
