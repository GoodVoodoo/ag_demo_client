# Audiogram Demo Clients

This repository contains a set of demonstration clients for the Audiogram gRPC API. These clients provide a command-line interface for interacting with the ASR (Speech-to-Text), TTS (Text-to-Speech), and Voice Cloning services.

## Documentation

- **[Quickstart Guide](docs/quickstart.md):** Learn how to install, configure, and use the clients.
- **[CLI Reference](docs/cli.md):** A detailed reference for the command-line interface.
- **[Architecture Overview](docs/architecture.md):** An overview of the project structure and its core components.

## 🔒 Security & Credentials

### Quick Setup

Set your credentials as environment variables (recommended):

```bash
export AUDIOGRAM_CLIENT_ID="your-client-id"
export AUDIOGRAM_CLIENT_SECRET="your-client-secret"
```

### Environment Variables

The application supports the following environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `AUDIOGRAM_CLIENT_ID` | Keycloak client ID | ✅ Yes |
| `AUDIOGRAM_CLIENT_SECRET` | Keycloak client secret | ✅ Yes |
| `AUDIOGRAM_IAM_ACCOUNT` | IAM account name | Optional (default: "demo") |
| `AUDIOGRAM_IAM_WORKSPACE` | IAM workspace name | Optional (default: "default") |
| `AUDIOGRAM_SSO_URL` | Keycloak SSO URL | Optional (default: configured) |
| `AUDIOGRAM_REALM` | Keycloak realm | Optional (default: configured) |
| `AUDIOGRAM_API_ADDRESS` | gRPC API address | Optional (default: configured) |

### Configuration Priority

Settings are loaded in this order (highest priority first):

1. **Environment variables** (`AUDIOGRAM_*`)
2. **`.env` file** (not tracked by git)
3. **`config.ini` file**
4. **Command line arguments**

### Security Best Practices

- ✅ **Use environment variables** for credentials (never commit secrets)
- ✅ **Create a `.env` file** for local development (auto-ignored by git)
- ✅ **Keep `config.ini`** free of sensitive data
- ✅ **Rotate credentials** regularly
- ❌ **Never commit** `.env` files or secrets to version control

### Testing Your Setup

Verify your credentials are working:

```bash
# Set your credentials
export AUDIOGRAM_CLIENT_ID="your-client-id"
export AUDIOGRAM_CLIENT_SECRET="your-client-secret"

# Test the connection
python -c "
from audiogram_client.models_service import ModelService
from audiogram_client.common_utils.config import Settings
settings = Settings(['config.ini'])
settings.validators.validate()
service = ModelService(settings)
models = service.get_models()
print(f'✅ Success! Found {len(models)} models')
"
```

### Detailed Setup Instructions

For complete setup instructions, troubleshooting, and security best practices, see:
- **[SECURITY_SETUP.md](SECURITY_SETUP.md)** - Complete security configuration guide
- **[SECURITY_IMPLEMENTATION_SUMMARY.md](SECURITY_IMPLEMENTATION_SUMMARY.md)** - Implementation details

## Contributing

Contributions are welcome! Please see the `improvements.md` file for a list of planned improvements.
