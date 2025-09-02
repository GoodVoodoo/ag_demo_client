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
# Set your credentials in .env file or export them
export AUDIOGRAM_CLIENT_ID="your-client-id"
export AUDIOGRAM_CLIENT_SECRET="your-client-secret"

# Test TTS (Text-to-Speech)
python -m audiogram_client.tts.synthesize --config config.ini --text "Hello world!" --output-file test.wav

# Test ASR (Speech Recognition) with punctuation
python -m audiogram_client.asr.file_recognize --config config.ini --audio-file your_audio.wav --model e2e-v3 --enable-punctuator

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

## 🧪 Testing

### Integration Tests

The project includes comprehensive integration tests for TTS and ASR functionality that verify real API interactions.

#### Test Scenarios

1. **TTS (Text-to-Speech) Test**
   - Synthesizes Russian phrase: "Тестирование синтеза прошло успешно"
   - Uses `gandzhaev` voice
   - Validates audio file generation and quality

2. **ASR (Automatic Speech Recognition) Test**
   - Recognizes audio file `1297.wav` with punctuation enabled
   - Uses `e2e-v3` model
   - Validates transcription accuracy and punctuation

3. **Model Service Test**
   - Verifies model information retrieval
   - Ensures API connectivity

#### Running Tests

**Option 1: Quick Test Script (Recommended)**
```bash
# Set your credentials
export AUDIOGRAM_CLIENT_ID="your-client-id"
export AUDIOGRAM_CLIENT_SECRET="your-client-secret"

# Run the integration test script
python run_integration_tests.py
```

**Option 2: Using pytest**
```bash
# Install dev dependencies
pip install -e .[dev]

# Run integration tests only
pytest tests/test_integration.py -v -m integration

# Run all tests
pytest -v
```

#### Prerequisites

Before running tests, ensure you have:

- ✅ **Valid credentials** set as environment variables
- ✅ **Configuration file** (`config.ini`) properly configured
- ✅ **Test audio file** (`1297.wav`) present in project root
- ✅ **Network connectivity** to Audiogram API endpoints

#### Test Output

The test script provides detailed, colored output showing:
- ✅ Prerequisites check results
- 🔄 Real-time test execution progress  
- 📊 Individual test results with details
- 📈 Summary with pass/fail statistics
- 🎉 Clear success/failure indicators

#### Troubleshooting Tests

**Common Issues:**
- **Authentication errors**: Check your `AUDIOGRAM_CLIENT_ID` and `AUDIOGRAM_CLIENT_SECRET`
- **Network timeouts**: Verify API endpoints in `config.ini`
- **Missing audio file**: Ensure `1297.wav` exists in project root
- **Permission errors**: Check file system permissions for temporary files

**Debug Mode:**
```bash
python run_integration_tests.py --verbose
```

## Contributing

Contributions are welcome! Please see the `improvements.md` file for a list of planned improvements.
