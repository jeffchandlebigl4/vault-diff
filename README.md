# vault-diff

> CLI tool to compare secrets across HashiCorp Vault namespaces and output structured diffs

---

## Installation

```bash
pip install vault-diff
```

Or install from source:

```bash
git clone https://github.com/yourorg/vault-diff.git && cd vault-diff && pip install .
```

---

## Usage

Compare secrets between two Vault namespaces:

```bash
vault-diff --source secret/prod --target secret/staging
```

Output a JSON-formatted diff:

```bash
vault-diff --source secret/prod --target secret/staging --format json
```

Compare a specific path recursively:

```bash
vault-diff --source secret/prod/app --target secret/staging/app --recursive
```

### Options

| Flag | Description |
|------|-------------|
| `--source` | Source Vault path |
| `--target` | Target Vault path |
| `--format` | Output format: `text` (default), `json`, `yaml` |
| `--recursive` | Recursively compare all sub-paths |
| `--redact` | Mask secret values in output |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `VAULT_ADDR` | Vault server address |
| `VAULT_TOKEN` | Vault authentication token |

---

## Requirements

- Python 3.8+
- HashiCorp Vault 1.x
- `hvac` Python client

---

## License

This project is licensed under the [MIT License](LICENSE).