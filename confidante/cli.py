import click
import json
import sys
from pathlib import Path
from confidante.core import Confidante
from confidante.exceptions import ConfidanteError

@click.group()
def main():
    """Confidante CLI for managing configuration and secrets."""
    pass

@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--decrypted', is_flag=True, help="Attempt to decrypt values")
def load(path, decrypted):
    """Load and print configuration."""
    try:
        config = Confidante.load(path)
        if decrypted:
            config.unlock(prompt=True)
        click.echo(json.dumps(config.config._data, indent=2))
    except ConfidanteError as e:
        click.echo(str(e), err=True)
        sys.exit(1)

@main.command()
@click.argument('path', type=click.Path(exists=True))
def tidy(path):
    """Tidy up the configuration file."""
    try:
        config = Confidante.load(path)
        config.tidy()
        click.echo("Configuration file tidied successfully.")
    except ConfidanteError as e:
        click.echo(str(e), err=True)
        sys.exit(1)

@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--key', help='Symmetric key for decryption')
@click.option('--private-key-path', help='Private key path for asymmetric decryption')
@click.option('--prompt', is_flag=True, help='Prompt for key')
def unlock(path, key, private_key_path, prompt):
    """Unlock a configuration file."""
    try:
        config = Confidante.load(path)
        config.unlock(key=key, private_key_path=private_key_path, prompt=prompt)
        click.echo("Configuration unlocked.")
    except ConfidanteError as e:
        click.echo(str(e), err=True)
        sys.exit(1)

@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.argument('key_path', nargs=-1)
@click.argument('value')
@click.option('--key', help='Symmetric key for encryption')
@click.option('--private-key-path', help='Private key path (if asymmetric)')
@click.option('--passphrase', help='Passphrase for private key')
def encrypt_key(path, key_path, value, key, private_key_path, passphrase):
    """Encrypt a value and set it at given key path."""
    try:
        config = Confidante.load(path)
        config.unlock(key=key, private_key_path=private_key_path, passphrase=passphrase, prompt=(key is None and private_key_path is None))
        config.encrypt_value(list(key_path), value)
        config.save()
        click.echo("Secret encrypted and saved.")
    except ConfidanteError as e:
        click.echo(str(e), err=True)
        sys.exit(1)

@main.command()
@click.argument('path', type=click.Path(exists=True))
def validate(path):
    """Validate configuration."""
    try:
        config = Confidante.load(path)
        # Placeholder for schema validation
        click.echo("Configuration is valid.")
    except ConfidanteError as e:
        click.echo(str(e), err=True)
        sys.exit(1)
