# Confidante Usage Guide

This guide provides detailed information about using Confidante for configuration management in your applications.

## Table of Contents

1. [Basic Configuration Management](#basic-configuration-management)
2. [Working with Different Formats](#working-with-different-formats)
3. [Secrets Management](#secrets-management)
4. [Environment Variables](#environment-variables)
5. [Command Line Interface](#command-line-interface)
6. [Advanced Usage](#advanced-usage)

## Basic Configuration Management

### Loading Configuration Files

```python
from confidante import Confidante

# Load JSON configuration
config = Confidante.load("config.json")

# Load YAML configuration
config = Confidante.load("config.yaml")

# Load TOML configuration
config = Confidante.load("config.toml")
```

### Accessing Configuration Values

Confidante provides two ways to access configuration values:

```python
# Dot notation
database_url = config.config.database.url
port = config.config.server.port

# Dictionary notation
database_url = config.config["database"]["url"]
port = config.config["server"]["port"]
```

## Working with Different Formats

### JSON Configuration Example

```json
{
  "database": {
    "url": "postgresql://localhost:5432/mydb",
    "pool_size": 5
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

### YAML Configuration Example

```yaml
database:
  url: postgresql://localhost:5432/mydb
  pool_size: 5
server:
  host: 0.0.0.0
  port: 8000
```

### TOML Configuration Example

```toml
[database]
url = "postgresql://localhost:5432/mydb"
pool_size = 5

[server]
host = "0.0.0.0"
port = 8000
```

## Secrets Management

### Symmetric Encryption

```python
# Initialize with symmetric encryption
config.unlock(key="your-encryption-key")

# Encrypt a value
config.encrypt_value(["database", "password"], "secret123")

# Save the configuration
config.save()

# Later, decrypt the configuration
config.unlock(key="your-encryption-key")
decrypted_password = config.config.database.password
```

### Asymmetric Encryption

```python
# Initialize with asymmetric encryption
config.unlock(private_key_path="path/to/private_key.pem")

# Encrypt a value (uses public key internally)
config.encrypt_value(["api", "secret"], "api_secret_123")

# Save the configuration
config.save()
```

## Environment Variables

Override configuration values using environment variables:

```bash
# Format: CONFIDANTE__section__key=value
export CONFIDANTE__database__url="postgresql://prod-db:5432/proddb"
export CONFIDANTE__server__port="9000"
```

```python
# Load configuration with environment variable support
config = Confidante.load("config.json", merge_env_vars=True)
```

## Command Line Interface

### Basic Commands

```bash
# View configuration
confidante load config.json

# View decrypted configuration
confidante load config.json --decrypted --key your-key

# Encrypt a value
confidante encrypt-key config.json database.password "secret123" --key your-key

# Tidy configuration file
confidante tidy config.json

# Validate configuration
confidante validate config.json
```

### Working with Keys

```bash
# Using symmetric encryption
confidante encrypt-key config.json api.key "secret" --key your-symmetric-key

# Using asymmetric encryption
confidante encrypt-key config.json api.key "secret" --private-key-path /path/to/private.pem
```

## Advanced Usage

### Custom Configuration Loaders

Confidante supports custom configuration loaders by implementing the `ConfigLoader` protocol:

```python
from confidante.loaders.base import ConfigLoader

class CustomLoader(ConfigLoader):
    def load(self, path: str) -> dict[str, Any]:
        # Implementation here
        pass
    
    def dump(self, data: dict[str, Any], path: str) -> None:
        # Implementation here
        pass
```

### Error Handling

```python
from confidante.exceptions import ConfidanteError

try:
    config = Confidante.load("config.json")
    config.unlock(key="encryption-key")
except ConfidanteError as e:
    print(f"Configuration error: {e}")
```

### Tidying Configuration Files

```python
# Load and tidy configuration
config = Confidante.load("config.json")
config.tidy()
config.save()
```

This will:

- Sort all dictionary keys
- Standardize formatting
- Maintain encryption status of values

## Best Practices

1. **Key Management**
    - Store encryption keys securely
    - Use environment variables for key injection
    - Consider using a secure key management service

2. **Configuration Structure**
    - Keep configurations flat when possible
    - Use consistent naming conventions
    - Document all configuration options

3. **Security**
    - Encrypt all sensitive values
    - Use asymmetric encryption for production environments
    - Regularly rotate encryption keys

4. **Version Control**
    - Don't commit encrypted secrets to version control
    - Use template files for configuration examples
    - Document required configuration values

## Troubleshooting

Common issues and their solutions:

1. **Invalid Key Error**
    - Ensure the encryption key matches the one used for encryption
    - Verify key format (especially for symmetric keys)

2. **File Format Errors**
    - Verify file extension matches content
    - Ensure valid JSON/YAML/TOML syntax

3. **Environment Variable Issues**
    - Check variable name formatting
    - Verify environment variable values
