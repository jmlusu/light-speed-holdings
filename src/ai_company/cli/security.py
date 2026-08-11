"""CLI commands for security operations."""

from __future__ import annotations

import typer

app = typer.Typer(help="Security operations — encryption, key rotation, scanning")


@app.command("encrypt-memory")
def encrypt_memory(
    database_path: str = typer.Option(
        "data/ai_company.db",
        help="Path to the SQLite database file",
    ),
    rotate_key: bool = typer.Option(
        False,
        "--rotate-key",
        "-r",
        help="Rotate the encryption key before encrypting",
    ),
) -> None:
    """Encrypt all existing plaintext memory entries.

    This is an idempotent migration — already-encrypted entries are skipped.
    Use ``--rotate-key`` to generate a new encryption key first.
    """
    from ai_company.data.database import Database
    from ai_company.security.encryption_key_manager import EncryptionKeyManager
    from ai_company.security.migrate_memory_encrypt import encrypt_legacy_entries

    typer.echo("Initializing encryption key manager...")
    key_manager = EncryptionKeyManager()

    if rotate_key:
        new_id = key_manager.rotate()
        typer.echo(f"Rotated to new key: {new_id}")

    typer.echo(f"Connecting to database: {database_path}")
    db = Database(database_path)
    db.init_schema()

    typer.echo("Encrypting plaintext memory entries...")
    count = encrypt_legacy_entries(database=db, key_manager=key_manager)

    typer.echo(f"Done. Encrypted {count} entries.")
    if count == 0:
        typer.echo("No plaintext entries found — all memory is already encrypted.")


@app.command("rotate-key")
def rotate_key(
    key_dir: str = typer.Option(
        "security",
        help="Directory for key metadata files",
    ),
) -> None:
    """Rotate the memory encryption key.

    The old current key becomes the previous key (retained for decryption).
    New entries will use the new key; existing entries can still be decrypted
    with the previous key.
    """
    from ai_company.security.encryption_key_manager import EncryptionKeyManager

    key_manager = EncryptionKeyManager(key_dir=key_dir)
    old_id = key_manager.current_key_id
    new_id = key_manager.rotate()

    typer.echo(f"Key rotated: {old_id} → {new_id}")
    typer.echo("The previous key is retained for decrypting existing entries.")


@app.command("key-status")
def key_status(
    key_dir: str = typer.Option(
        "security",
        help="Directory for key metadata files",
    ),
) -> None:
    """Show current encryption key status."""
    from ai_company.security.encryption_key_manager import EncryptionKeyManager

    key_manager = EncryptionKeyManager(key_dir=key_dir)
    typer.echo(f"Current key ID:  {key_manager.current_key_id}")
    typer.echo(f"Previous key ID: {key_manager.previous_key_id or '(none)'}")
