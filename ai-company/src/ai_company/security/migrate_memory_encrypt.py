"""One-time migration script to encrypt existing plaintext memory entries.

This script encrypts all existing plaintext memory entries in the SQLite
database. It is idempotent — entries that are already encrypted (have the
``ENC:`` prefix) are skipped.

Usage::

    from ai_company.security.migrate_memory_encrypt import encrypt_legacy_entries
    count = encrypt_legacy_entries()

Or via CLI::

    ai-company security encrypt-memory
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from ai_company.data.database import Database

if TYPE_CHECKING:
    from ai_company.security.encryption_key_manager import EncryptionKeyManager

logger = logging.getLogger(__name__)


def encrypt_legacy_entries(
    database: Database | None = None,
    key_manager: EncryptionKeyManager | None = None,
) -> int:
    """Encrypt all existing plaintext memory entries.

    Args:
        database: An initialised Database instance. If ``None``, uses the
            module-level singleton from ``ai_company.data.database``.
        key_manager: An EncryptionKeyManager instance. If ``None``, creates
            one with default settings.

    Returns:
        The number of entries that were encrypted (skipped entries are not counted).
    """
    from ai_company.data.database import get_database, init_database
    from ai_company.security.encryption_key_manager import EncryptionKeyManager
    from ai_company.security.memory_encryption import is_encrypted

    if database is None:
        database = get_database() or init_database()

    if key_manager is None:
        key_manager = EncryptionKeyManager()

    # Fetch all memory entries
    rows = database.fetchall("SELECT id, content FROM memory_entries")

    encrypted_count = 0
    for row in rows:
        content = row["content"]
        if is_encrypted(content):
            continue  # Already encrypted, skip

        # Encrypt the plaintext content
        from ai_company.security.memory_encryption import encrypt

        encrypted_content = encrypt(content, key_manager)
        database.execute(
            "UPDATE memory_entries SET content = ?, content_search = ? WHERE id = ?",
            (encrypted_content, content, row["id"]),
        )
        encrypted_count += 1

    if encrypted_count > 0:
        database.commit()
        logger.info("Encrypted %d legacy memory entries", encrypted_count)
    else:
        logger.info("No plaintext memory entries found to encrypt")

    return encrypted_count


def migrate_file_based_entries(
    base_dir: str = "memory",
    key_manager: EncryptionKeyManager | None = None,
) -> int:
    """Encrypt existing plaintext entries in the legacy file-based memory store.

    Modifies JSON files in-place, encrypting the ``content`` field of each entry.

    Args:
        base_dir: Directory containing ``*.json`` memory files.
        key_manager: An EncryptionKeyManager instance.

    Returns:
        The number of entries encrypted.
    """
    from pathlib import Path

    from ai_company.security.encryption_key_manager import EncryptionKeyManager
    from ai_company.security.memory_encryption import encrypt, is_encrypted

    if key_manager is None:
        key_manager = EncryptionKeyManager()

    base = Path(base_dir)
    if not base.exists():
        logger.warning("Memory directory not found: %s", base)
        return 0

    encrypted_count = 0
    for json_file in base.glob("*.json"):
        if json_file.name == "memory_keys.json":
            continue  # Skip key metadata file

        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        if not isinstance(data, list):
            continue

        modified = False
        for entry in data:
            content = entry.get("content", "")
            if not content or is_encrypted(content):
                continue
            entry["content"] = encrypt(content, key_manager)
            modified = True
            encrypted_count += 1

        if modified:
            json_file.write_text(
                json.dumps(data, indent=2, default=str), encoding="utf-8"
            )

    if encrypted_count > 0:
        logger.info("Encrypted %d file-based memory entries", encrypted_count)
    else:
        logger.info("No plaintext file-based memory entries found to encrypt")

    return encrypted_count
