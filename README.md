# Confidante

Confidante is a secure configuration management library for Python applications that provides encrypted secrets storage, multiple format support, and flexible configuration access patterns.

## Features

- **Multiple Configuration Formats**: Native support for JSON, YAML, and TOML configuration files
- **Encrypted Secrets**: Support for both symmetric (Fernet) and asymmetric (RSA) encryption of sensitive values
- **Environment Variable Overrides**: Override configuration values using environment variables
- **Flexible Access Patterns**: Access configuration values using both dot notation and dictionary syntax
- **Command Line Interface**: Comprehensive CLI for managing configurations and secrets
- **Type Safety**: Full type hints support with Python's typing system
- **Automated Tidying**: Built-in configuration file cleanup and standardization

## Installation

```bash
pip install confidante
```

## Quick Start

```python
from confidante import Confidante

# Load a configuration file
config = Confidante.load("config.json")

# Access values using dot notation
app_name = config.config.app.name

# Access values using dictionary syntax
debug_mode = config.config["app"]["settings"]["debug"]

# Encrypt a secret
config.unlock(key="your-encryption-key")
config.encrypt_value(["credentials", "api_key"], "secret-value")
config.save()
```

## Security Features

### Symmetric Encryption
Uses the Fernet implementation from the cryptography library, providing secure symmetric encryption for secrets.

### Asymmetric Encryption
Supports RSA encryption for scenarios requiring public/private key pairs.

## CLI Usage

```bash
# Load and view configuration
confidante load config.json

# Load and decrypt configuration
confidante load config.json --decrypted --key your-key

# Encrypt a value
confidante encrypt-key config.json path.to.secret "secret-value" --key your-key

# Tidy configuration file
confidante tidy config.json
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and code of conduct before submitting pull requests.

## License

This project is under the [GNU LGPLv3 (GNU Lesser General Public License v3.0)](LICENSE) license.

## Project Status

Active development - API is stable but may evolve.

## Credits

Built with these dependencies:
- cryptography
- PyYAML
- tomli/tomli_w
- click

## Maintainers

[Araray Velho]([https://github.com/araray)

