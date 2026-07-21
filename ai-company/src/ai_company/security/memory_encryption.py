"""Content encryption engine for memory entries.

Provides AES-256-GCM authenticated encryption with unique nonces per entry.
Encrypted content uses the format ``ENC:<base64(nonce || ciphertext)>`` and
is backward-compatible with plaintext (passthrough on encrypt, passthrough
for non-encrypted content on decrypt).
"""

from __future__ import annotations

import base64
import logging
import secrets
from typing import TYPE_CHECKING

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

if TYPE_CHECKING:
    from ai_company.security.encryption_key_manager import EncryptionKeyManager

logger = logging.getLogger(__name__)

_ENC_PREFIX = "ENC:"
_NONCE_SIZE = 12  # 96-bit nonce for AES-GCM


def is_encrypted(content: str) -> bool:
    """Check whether content has been encrypted (has ``ENC:`` prefix)."""
    return content.startswith(_ENC_PREFIX)


def encrypt(plaintext: str, key_manager: EncryptionKeyManager) -> str:
    """Encrypt plaintext using AES-256-GCM.

    If plaintext is already encrypted (has ``ENC:`` prefix), it is returned
    unchanged to avoid double-encryption.

    Returns:
        ``ENC:<base64(nonce || ciphertext)>`` string.
    """
    if is_encrypted(plaintext):
        return plaintext

    if not plaintext:
        return plaintext

    key = key_manager.get_current_key()
    nonce = secrets.token_bytes(_NONCE_SIZE)
    aesgcm = AESGCM(key)
    # Associated data is empty; the nonce provides uniqueness
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    blob = nonce + ciphertext
    encoded = base64.b64encode(blob).decode("ascii")
    return f"{_ENC_PREFIX}{encoded}"


def decrypt(payload: str, key_manager: EncryptionKeyManager) -> str:
    """Decrypt an encrypted payload, or return plaintext unchanged.

    Tries the current key first, then falls back to the previous key
    (supporting the rotation window).

    Args:
        payload: ``ENC:<base64>`` string, or plain text.
        key_manager: The key manager providing decryption keys.

    Returns:
        The decrypted plaintext.

    Raises:
        ValueError: If decryption fails with both current and previous keys.
    """
    if not is_encrypted(payload):
        return payload

    encoded = payload[len(_ENC_PREFIX):]
    try:
        blob = base64.b64decode(encoded)
    except Exception as exc:
        raise ValueError(f"Invalid encrypted payload: {exc}") from exc

    nonce = blob[:_NONCE_SIZE]
    ciphertext = blob[_NONCE_SIZE:]

    # Try current key first
    last_error: Exception | None = None
    for label, key in [
        ("current", key_manager.get_current_key()),
        ("previous", key_manager.get_previous_key()),
    ]:
        if key is None:
            continue
        try:
            aesgcm = AESGCM(key)
            plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext_bytes.decode("utf-8")
        except Exception as exc:
            last_error = exc
            logger.debug("Decrypt failed with %s key: %s", label, exc)

    raise ValueError(
        f"Failed to decrypt memory content with any available key: {last_error}"
    )
