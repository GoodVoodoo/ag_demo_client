# Security Setup Guide

This guide explains how to securely configure your Audiogram client credentials.

## ⚠️ Important Security Note

**Never commit sensitive credentials to version control!** Always use environment variables for sensitive data like client secrets.

## Setup Instructions

### 1. Set Environment Variables

You can set your credentials using environment variables. The configuration system will automatically use these if available:

```bash
# Required credentials
export AUDIOGRAM_CLIENT_ID="audiogram-wer"
export AUDIOGRAM_CLIENT_SECRET="your-actual-secret-here"

# Optional overrides
export AUDIOGRAM_IAM_ACCOUNT="demo"
export AUDIOGRAM_IAM_WORKSPACE="default"
export AUDIOGRAM_SSO_URL="https://sso.dev.mts.ai"
export AUDIOGRAM_REALM="audiogram-demo"
export AUDIOGRAM_API_ADDRESS="grpc.audiogram-demo.mts.ai:443"
```

### 2. Alternative: Create a .env file (not committed to git)

Create a `.env` file in the project root:

```bash
# .env file - DO NOT COMMIT TO GIT!
AUDIOGRAM_CLIENT_ID=audiogram-wer
AUDIOGRAM_CLIENT_SECRET=your-actual-secret-here
AUDIOGRAM_IAM_ACCOUNT=demo
AUDIOGRAM_IAM_WORKSPACE=default
```

### 3. Windows PowerShell Setup

For Windows users, set environment variables in PowerShell:

```powershell
$env:AUDIOGRAM_CLIENT_ID="audiogram-wer"
$env:AUDIOGRAM_CLIENT_SECRET="your-actual-secret-here"
$env:AUDIOGRAM_IAM_ACCOUNT="demo"
$env:AUDIOGRAM_IAM_WORKSPACE="default"
```

### 4. Persistent Environment Variables

#### On macOS/Linux (add to ~/.bashrc or ~/.zshrc):
```bash
export AUDIOGRAM_CLIENT_ID="audiogram-wer"
export AUDIOGRAM_CLIENT_SECRET="your-actual-secret-here"
```

#### On Windows (use System Properties > Environment Variables):
- Variable: `AUDIOGRAM_CLIENT_ID`
- Value: `audiogram-wer`
- Variable: `AUDIOGRAM_CLIENT_SECRET` 
- Value: `your-actual-secret-here`

## Configuration Priority

The system will use credentials in this order (highest priority first):

1. Environment variables (AUDIOGRAM_*)
2. .env file values
3. config.ini file values
4. Command line arguments

## SSL Certificate Issues

If you encounter SSL certificate validation errors with Keycloak:

1. **Development**: Set `verify_sso = false` in config.ini
2. **Production**: Obtain proper certificates or configure certificate paths:
   ```ini
   ca_cert_path = "/path/to/ca-certificates.crt"
   ```

## Security Best Practices

1. ✅ Use environment variables for secrets
2. ✅ Add .env to .gitignore
3. ✅ Rotate credentials regularly
4. ✅ Use different credentials for different environments
5. ✅ Enable SSL verification in production
6. ❌ Never commit secrets to version control
7. ❌ Never share credentials in chat/email

## Testing Your Setup

Run this command to verify your credentials work:

```bash
# Activate virtual environment first
source venv/bin/activate

# Test the setup
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
