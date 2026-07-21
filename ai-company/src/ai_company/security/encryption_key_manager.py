"""Encryption key lifecycle manager for memory encryption.

Derives AES-256 keys from a master secret using HKDF-SHA256 and supports
key rotation with a dual-key window (current + previous). Key metadata
(not raw keys) is persisted to ``security/memory_keys.json``.

Raw keys are encrypted with a secondary derivation before disk write.

Master secret is read from the ``MEMORY_ENCRYPTION_KEY`` environment variable,
falling back to ``JWT_SECRET_KEY``.
"""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import secrets
import time
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

logger = logging.getLogger(__name__)

_DEFAULT_KEY_DIR = Path("security")
_KEY_FILE = "memory_keys.json"
_KEY_SIZE = 32  # 256 bits
_NONCE_SIZE = 12  # GCM nonce
_HKDF_INFO = b"ai-company-memory-encryption-key-v1"
_HKDF_SECONDARY_INFO = b"ai-company-key-at-rest-protection-v1"


def _hkdf_derive(master_secret: bytes, info: bytes, length: int = _KEY_SIZE) -> bytes:
    """Derive a key using HKDF-SHA256."""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=info,
    )
    return hkdf.derive(master_secret)


def _get_master_secret() -> bytes:
    """Read the master secret from environment variables."""
    secret = os.environ.get("MEMORY_ENCRYPTION_KEY") or os.environ.get("JWT_SECRET_KEY")
    if not secret:
        raise RuntimeError(
            "No master secret found. Set MEMORY_ENCRYPTION_KEY or JWT_SECRET_KEY."
        )
    return secret.encode("utf-8")


class EncryptionKeyManager:
    """Manages AES-256 encryption keys for memory content.

    Supports key rotation with a dual-key window so that data encrypted
    with a previous key can still be decrypted during the rotation period.

    Args:
        key_dir: Directory for persisting key metadata. Defaults to ``security/``.
    """

    def __init__(self, key_dir: str | Path = _DEFAULT_KEY_DIR) -> None:
        self._key_dir = Path(key_dir)
        self._key_dir.mkdir(parents=True, exist_ok=True)
        self._key_file = self._key_dir / _KEY_FILE
        self._current_key: bytes | None = None
        self._previous_key: bytes | None = None
        self._current_key_id: str = ""
        self._previous_key_id: str = ""
        self._loaded = False
        self._load_or_create()

    # ── Public API ────────────────────────────────────────────────────

    @property
    def current_key_id(self) -> str:
        return self._current_key_id

    @property
    def previous_key_id(self) -> str:
        return self._previous_key_id

    def get_current_key(self) -> bytes:
        """Return the current AES-256 encryption key."""
        return self._current_key  # type: ignore[return-value]

    def get_previous_key(self) -> bytes | None:
        """Return the previous encryption key, or ``None``."""
        return self._previous_key

    def rotate(self) -> str:
        """Rotate to a new key. Returns the new key ID.

        The old current key becomes the previous key.
        """
        old_current = self._current_key
        old_current_id = self._current_key_id

        self._current_key = self._derive_new_key()
        self._current_key_id = self._generate_key_id()

        self._previous_key = old_current
        self._previous_key_id = old_current_id

        self._save_metadata()
        logger.info(
            "Encryption key rotated: %s → %s",
            old_current_id or "(genesis)",
            self._current_key_id,
        )
        return self._current_key_id

    # ── Private helpers ───────────────────────────────────────────────

    def _derive_new_key(self) -> bytes:
        """Derive a fresh AES-256 key from the master secret."""
        master = _get_master_secret()
        # Mix in a random salt for uniqueness across rotations
        salt = secrets.token_bytes(16)
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=_KEY_SIZE,
            salt=salt,
            info=_HKDF_INFO,
        )
        return hkdf.derive(master + salt)

    def _generate_key_id(self) -> str:
        """Generate a short deterministic key identifier."""
        assert self._current_key is not None
        return hashlib.sha256(self._current_key).hexdigest()[:12]

    def _encrypt_key_for_storage(self, raw_key: bytes) -> str:
        """Encrypt a raw key with a secondary derivation for at-rest protection."""
        master = _get_master_secret()
        secondary_key = _hkdf_derive(master, _HKDF_SECONDARY_INFO)
        nonce = secrets.token_bytes(_NONCE_SIZE)
        aesgcm = AESGCM(secondary_key)
        ciphertext = aesgcm.encrypt(nonce, raw_key, None)
        blob = nonce + ciphertext
        return base64.b64encode(blob).decode("ascii")

    def _decrypt_key_from_storage(self, encrypted_b64: str) -> bytes:
        """Decrypt a stored key using the secondary derivation."""
        master = _get_master_secret()
        secondary_key = _hkdf_derive(master, _HKDF_SECONDARY_INFO)
        blob = base64.b64decode(encrypted_b64)
        nonce = blob[:_NONCE_SIZE]
        ciphertext = blob[_NONCE_SIZE:]
        aesgcm = AESGCM(secondary_key)
        return aesgcm.decrypt(nonce, ciphertext, None)

    def _save_metadata(self) -> None:
        """Persist key metadata (encrypted keys, not raw) to disk."""
        assert self._current_key is not None
        meta: dict[str, Any] = {
            "current_key_id": self._current_key_id,
            "previous_key_id": self._previous_key_id,
            "current_key_encrypted": self._encrypt_key_for_storage(self._current_key),
            "previous_key_encrypted": (
                self._encrypt_key_for_storage(self._previous_key)
                if self._previous_key
                else None
            ),
            "created_at": time.time(),
        }
        self._key_file.write_text(
            json.dumps(meta, indent=2), encoding="utf-8"
        )
        logger.debug("Key metadata saved to %s", self._key_file)

    def _load_or_create(self) -> None:
        """Load existing key metadata or create genesis keys."""
        if self._loaded:
            return

        if self._key_file.exists():
            try:
                meta = json.loads(self._key_file.read_text(encoding="utf-8"))
                self._current_key_id = meta.get("current_key_id", "")
                self._previous_key_id = meta.get("previous_key_id", "")
                self._current_key = self._decrypt_key_from_storage(
                    meta["current_key_encrypted"]
                )
                prev_enc = meta.get("previous_key_encrypted")
                self._previous_key = (
                    self._decrypt_key_from_storage(prev_enc) if prev_enc else None
                )
                self._loaded = True
                logger.debug("Loaded existing encryption keys from %s", self._key_file)
                return
            except Exception:
                logger.warning("Failed to load key metadata, creating new genesis keys")

        # Genesis: create first key
        self._current_key = self._derive_new_key()
        self._current_key_id = self._generate_key_id()
        self._previous_key = None
        self._previous_key_id = ""
        self._save_metadata()
        self._loaded = True
        logger.info("Created genesis encryption key: %s", self._current_key_id)
