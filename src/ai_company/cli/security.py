"""CLI commands for security operations."""

from __future__ import annotations

import secrets
from pathlib import Path

import typer

app = typer.Typer(help="Security operations — encryption, key rotation, scanning")

_ROTATE_SECRETS_ARG = typer.Argument(
    None,
    help="Names of secrets to rotate (e.g., OPENCODE_API_KEY GEMINI_API_KEY). If omitted, rotates all placeholder keys.",
)


def _update_env_file(env_path: Path, key: str, new_value: str) -> bool:
    """Update or add a key in .env file, preserving comments and formatting."""
    lines = []
    found = False

    if env_path.exists():
        content = env_path.read_text(encoding="utf-8")
        for line in content.splitlines(keepends=True):
            stripped = line.lstrip()
            if stripped.startswith(f"{key}="):
                lines.append(f"{key}={new_value}\n")
                found = True
            else:
                lines.append(line)

    if not found:
        lines.append(f"\n{key}={new_value}\n")

    env_path.write_text("".join(lines), encoding="utf-8")
    return found


@app.command("rotate-secrets")
def rotate_secrets(
    names: list[str] = _ROTATE_SECRETS_ARG,
    env_file: str = typer.Option(
        ".env",
        "--env-file",
        "-f",
        help="Path to .env file to update",
    ),
    show: bool = typer.Option(
        False,
        "--show",
        help="Show old and new values (default: only show new)",
    ),
) -> None:
    """Rotate API keys and dashboard secrets in .env file.

    Generates new cryptographically secure keys with secrets.token_urlsafe(32)
    and updates the .env file. If no names provided, rotates all keys that
    currently have placeholder values.

    Example:
        ai-company security rotate-secrets OPENCODE_API_KEY GEMINI_API_KEY
        ai-company security rotate-secrets --env-file .env.staging
        ai-company security rotate-secrets --show
    """
    env_path = Path(env_file)

    # Default placeholder keys to check
    placeholder_keys = {
        "OPENCODE_API_KEY": "your_opencode_api_key_here",
        "GEMINI_API_KEY": "your_gemini_api_key_here",
        "DEEPSEEK_API_KEY": "your_deepseek_api_key_here",
        "KIMI_API_KEY": "your_kimi_api_key_here",
        "OPENAI_API_KEY": "your_openai_api_key_here",
        "ANTHROPIC_API_KEY": "your_anthropic_api_key_here",
        "DASHBOARD_API_KEY": "your_dashboard_api_key_here",
        "DASHBOARD_RUN_KEY": "your_run_key_here",
        "DASHBOARD_APPROVE_KEY": "your_approve_key_here",
        "DASHBOARD_ADMIN_KEY": "your_admin_key_here",
    }

    # Determine which keys to rotate
    if names:
        keys_to_rotate = {k: placeholder_keys[k] for k in names if k in placeholder_keys}
        unknown = [k for k in names if k not in placeholder_keys]
        if unknown:
            typer.echo(
                f"Warning: Unknown keys (not in known placeholder list): {', '.join(unknown)}"
            )
    else:
        # Check which keys currently have placeholder values
        keys_to_rotate = {}
        if env_path.exists():
            content = env_path.read_text(encoding="utf-8")
            for key, placeholder in placeholder_keys.items():
                if f"{key}={placeholder}" in content:
                    keys_to_rotate[key] = placeholder
        else:
            typer.echo(f".env file not found at {env_path}")
            raise typer.Exit(1)

    if not keys_to_rotate:
        typer.echo("No keys to rotate (no placeholders found or none match specified names).")
        return

    typer.echo(f"Rotating {len(keys_to_rotate)} secret(s) in {env_path}...")

    for key, old_value in keys_to_rotate.items():
        new_key = secrets.token_urlsafe(32)
        _update_env_file(env_path, key, new_key)

        if show:
            typer.echo(f"  {key}: {old_value} -> {new_key}")
        else:
            typer.echo(f"  {key}: *** -> {new_key}")

    typer.echo(f"\nDone. Updated {env_path}")
    typer.echo("\nNext steps:")
    typer.echo("  1. Update the same keys in your secret store / deployed environments")
    typer.echo(
        '  2. Verify dashboard health endpoint: curl -H "X-API-Key: $DASHBOARD_ADMIN_KEY" http://localhost:8421/health'
    )
    typer.echo(
        '  3. Run verification: uv run python -c "from dotenv import load_dotenv; load_dotenv(); from ai_company.security.rbac import verify_keys; verify_keys()"'
    )


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
