# Audiogram Demo Clients

This repository contains a set of demonstration clients for the Audiogram gRPC API. These clients provide a command-line interface for interacting with the ASR (Speech-to-Text), TTS (Text-to-Speech), and Voice Cloning services.

## ✅ Tested & Working Features

- **🎯 Speech Recognition (ASR)** - Convert speech to text with punctuation support
- **🗣️ Text-to-Speech (TTS)** - Generate natural-sounding speech from text
- **🎙️ Voice Cloning** - Clone voices and use them for TTS (AudioKit Dev SF instance)
- **📝 Punctuator** - Automatic punctuation and capitalization in transcriptions

## Documentation

- **[Quickstart Guide](docs/quickstart.md):** Learn how to install, configure, and use the clients.
- **[CLI Reference](docs/cli.md):** A detailed reference for the command-line interface.
- **[Architecture Overview](docs/architecture.md):** An overview of the project structure and its core components.

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11+ (recommended: Python 3.13)
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ag_demo_client
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows (PowerShell):
   venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   # Install from pyproject.toml (recommended)
   pip install -e .
   
   # Or install development dependencies
   pip install -e ".[dev]"
   ```

4. **Verify installation:**
   ```bash
   python -m audiogram_cli.main --help
   ```

### Important Notes

- ✅ **Always activate the virtual environment** before using the CLI tools
- ✅ **Use `pyproject.toml`** for dependency management (not requirements.txt)
- ✅ **Keep virtual environment activated** for all audiogram commands
- ❌ **Don't install dependencies globally** - use the virtual environment

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
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\Activate.ps1  # Windows PowerShell

# Set your credentials in .env file or export them
export AUDIOGRAM_CLIENT_ID="your-client-id"
export AUDIOGRAM_CLIENT_SECRET="your-client-secret"

# Test ASR (Speech Recognition) with punctuation using CLI
python -m audiogram_cli.main asr file --config config.ini --audio-file your_audio.wav --model e2e-v3 --enable-punctuator

# Test TTS (Text-to-Speech) using CLI
python -m audiogram_cli.main tts file --config config.ini --text 'Тест синтеза речи.' --voice-name <voice-name> --save-to test.wav

# Test model listing
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

## 🎤 Voice Cloning (AudioKit Dev SF Instance)

Voice cloning functionality is available on a separate AudioKit Dev SF instance with enhanced security requirements.

### Quick Start for Voice Cloning

1. **Get Required Files:**
   - SSL Certificate: `WinCAG2ANDclass2root.pem`
   - AudioKit Dev SF credentials (Client ID & Secret)

2. **Setup Configuration:**
   ```bash
   # Use the pre-configured AudioKit Dev SF config
   python -m audiogram_cli.main --config config_audiokit_dev_sf.ini vc clone --audio-file your_voice.wav
   ```

3. **Environment Variables for Voice Cloning:**
   ```bash
   export AUDIOGRAM_CLIENT_ID="your-audiokit-dev-sf-client-id"
   export AUDIOGRAM_CLIENT_SECRET="your-audiokit-dev-sf-client-secret"
   export AUDIOGRAM_SSO_URL="https://isso.mts.ru/auth/"
   export AUDIOGRAM_REALM="mts"
   export AUDIOGRAM_API_ADDRESS="asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443"
   # Note: IAM settings not required for AudioKit Dev SF instance
   ```

### Configuration Files

| Instance | Config File | Endpoint | Features |
|----------|-------------|----------|----------|
| **Demo** | `config.ini` | `grpc.audiogram-demo.mts.ai:443` | ASR, TTS (preset voices) |
| **AudioKit Dev SF** | `config_audiokit_dev_sf.ini` | `asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443` | Voice Cloning, TTS |

### Voice Cloning Workflow

```bash
# 1. Clone a voice
TASK_ID=$(python -m audiogram_cli.main --config config_audiokit_dev_sf.ini vc clone --audio-file voice.wav)

# 2. Check cloning status
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini vc get-task-info --task-id $TASK_ID

# 3. Use cloned voice (once ready)
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini tts file --voice-name YOUR_VOICE_ID --text "Hello!"
```

### Detailed Voice Cloning Setup

For comprehensive setup instructions, certificate configuration, and troubleshooting:
- **[AUDIOKIT_DEV_SF_SETUP.md](AUDIOKIT_DEV_SF_SETUP.md)** - Complete AudioKit Dev SF configuration guide

## 🧪 Integration Tests

The project includes comprehensive integration tests to verify that TTS and ASR services work correctly with real API calls.

### Test Scenarios

The integration tests cover the following scenarios:

1. **TTS Test**: Synthesizes the phrase "Тестирование синтеза прошло успешно" using the `gandzhaev` voice
2. **ASR Test**: Recognizes the `1297.wav` audio file with punctuation enabled
3. **Prerequisites**: Validates configuration, credentials, and required files

### Running Integration Tests

#### Quick Start

Use the provided test runner script for the easiest testing experience:

```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\Activate.ps1  # Windows PowerShell

# Set your credentials
export AUDIOGRAM_CLIENT_ID="your-client-id"
export AUDIOGRAM_CLIENT_SECRET="your-client-secret"

# Run integration tests
python run_integration_tests.py
```

#### Manual Testing with pytest

You can also run tests manually using pytest:

```bash
# Run all integration tests
python -m pytest tests/test_integration.py -v

# Run specific test
python -m pytest tests/test_integration.py::TestIntegration::test_tts_gandzhaev_voice -v
python -m pytest tests/test_integration.py::TestIntegration::test_asr_with_punctuation -v

# Run with detailed output
python -m pytest tests/test_integration.py -v -s
```

### Test Requirements

For integration tests to work, you need:

- ✅ **Active virtual environment**
- ✅ **Valid credentials** (AUDIOGRAM_CLIENT_ID, AUDIOGRAM_CLIENT_SECRET)
- ✅ **Proper configuration** (`config.ini` file)
- ✅ **Test audio file** (`1297.wav` must exist)
- ✅ **Network connectivity** to Audiogram services

### Test Output

Successful test run shows:
```
🎉 All tests passed successfully!

Test Results Summary:
  ✅ TTS Test: Synthesized 'Тестирование синтеза прошло успешно' with gandzhaev voice
  ✅ ASR Test: Recognized 1297.wav with punctuation enabled  
  ✅ Prerequisites: Configuration and audio file validation

The Audiogram services are working correctly! 🎯
```

### Troubleshooting Tests

If tests fail, common issues include:

- **Missing credentials**: Set `AUDIOGRAM_CLIENT_ID` and `AUDIOGRAM_CLIENT_SECRET`
- **Network issues**: Check connectivity to `grpc.audiogram-demo.mts.ai:443`
- **Missing files**: Ensure `1297.wav` and `config.ini` exist
- **Voice unavailable**: Verify `gandzhaev` voice is accessible with your account
- **Virtual environment**: Make sure you've activated the virtual environment

For detailed error information, run tests with verbose output (`-v -s` flags).

## Contributing

Contributions are welcome! Please see the `improvements.md` file for a list of planned improvements.
