# Audiogram Demo Clients

This repository contains a set of demonstration clients for the Audiogram gRPC API. These clients provide a command-line interface for interacting with the ASR (Speech-to-Text), TTS (Text-to-Speech), and Voice Cloning services.

## ✅ Tested & Working Features

- **🎯 Speech Recognition (ASR)** - Convert speech to text with punctuation support
- **🗣️ Text-to-Speech (TTS)** - Generate natural-sounding speech from text in Russian and English
- **🎙️ Voice Cloning** - Clone voices and use them for TTS (AudioKit Dev SF instance)
- **📝 Punctuator** - Automatic punctuation and capitalization in transcriptions
- **📊 Universal Logging System** - Professional-grade logging for ALL operations with automatic rotation

## Documentation

- **[Quickstart Guide](docs/quickstart.md):** Learn how to install, configure, and use the clients.
- **[CLI Reference](docs/cli.md):** A detailed reference for the command-line interface.
- **[Architecture Overview](docs/architecture.md):** An overview of the project structure and its core components.
- **[Universal Logging System](UNIVERSAL_LOGGING_SYSTEM_README.md):** Complete documentation for professional logging across all operations.

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

## 🗣️ Text-to-Speech (TTS) Examples

The Audiogram TTS service supports both Russian and English speech synthesis with high-quality, natural-sounding voices.

### Russian TTS

Russian TTS uses high-quality neural voices optimized for natural speech synthesis:

```bash
# Basic Russian synthesis
python -m audiogram_cli.main tts file \
  --text 'Привет! Это демонстрация русского синтеза речи.' \
  --voice-name borisova \
  --save-to russian_example.wav

# High-quality Russian synthesis with specific parameters
python -m audiogram_cli.main tts file \
  --text 'Тестирование синтеза прошло успешно с голосом Гандзяев.' \
  --voice-name gandzhaev \
  --sample-rate 22050 \
  --model-type high_quality \
  --save-to russian_gandzhaev.wav

# Available Russian voices
# borisova, gandzhaev, eldarov, gavrilov, kishchik, klukvin, koryakina, vostretsov
```

### English TTS

English TTS uses specialized English neural voices with optimized pronunciation:

```bash
# Basic English synthesis
python -m audiogram_cli.main tts file \
  --text 'Hello! This is a demonstration of English text-to-speech synthesis.' \
  --voice-name 'voice 2' \
  --model-type 'eng voice' \
  --sample-rate 22050 \
  --save-to english_example.wav

# Multiple English voice options
python -m audiogram_cli.main tts file \
  --text 'Testing different English voices for natural speech generation.' \
  --voice-name 'voice 3' \
  --model-type 'eng voice' \
  --sample-rate 22050 \
  --save-to english_voice3.wav

# Available English voices
# 'voice 1', 'voice 2', 'voice 3', 'voice 4'
```

### TTS Parameters

| Parameter | Russian Values | English Values | Description |
|-----------|----------------|----------------|-------------|
| `--voice-name` | `borisova`, `gandzhaev`, etc. | `'voice 1'`, `'voice 2'`, etc. | Voice selection |
| `--model-type` | `high_quality` | `'eng voice'` | Model type for synthesis |
| `--sample-rate` | `8000`, `22050` | `22050` | Audio quality (Hz) |
| `--voice-style` | `neutral`, `happy`, `angry`, `sad`, `surprised` | `neutral` | Emotional style |
| `--language-code` | `ru` (default) | `ru` (for English voices) | Language code |

### Advanced TTS Features

```bash
# Stream synthesis (real-time generation)
python -m audiogram_cli.main tts stream \
  --text 'Потоковый синтез для быстрой генерации речи.' \
  --voice-name borisova \
  --save-to stream_output.wav

# SSML support for advanced markup
python -m audiogram_cli.main tts file \
  --text '<speak>Привет! <break time="1s"/> Это <emphasis>особенный</emphasis> текст.</speak>' \
  --voice-name borisova \
  --read-ssml \
  --save-to ssml_example.wav

# Voice style variations
python -m audiogram_cli.main tts file \
  --text 'Этот текст произносится с эмоциональной окраской.' \
  --voice-name gandzhaev \
  --voice-style happy \
  --save-to emotional_speech.wav
```

### Checking Available Models

```bash
# List all available TTS models and voices
python -m audiogram_cli.main models

# Get detailed TTS model information
python -c "
from audiogram_client.models_service import ModelService
from audiogram_client.common_utils.config import Settings
settings = Settings(['config.ini'])
settings.validators.validate()
service = ModelService(settings)
models = service.get_models()
tts_models = [m for m in models if m.service == 'TTS']
for model in tts_models:
    print(f'{model.name} ({model.language}) - {model.type} - {model.sample_rate_hertz}Hz')
"
```

### TTS Best Practices

- ✅ **Use appropriate sample rates**: 22050 Hz for high quality, 8000 Hz for telephony
- ✅ **Choose the right model type**: `high_quality` for Russian, `'eng voice'` for English
- ✅ **Match voice to language**: Russian voices for Russian text, English voices for English text
- ✅ **Use SSML markup** for advanced pronunciation control and pauses
- ✅ **Test different voice styles** to find the best emotional tone for your content
- ❌ **Don't mix languages** in a single synthesis request for best results

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
asr file --config config.ini --audio-file your_audio.wav --model e2e-v3 --enable-punctuator

# Test TTS (Text-to-Speech) using CLI

# Russian TTS (high quality voices)
python -m audiogram_cli.main tts file --config config.ini --text 'Тест синтеза речи.' --voice-name borisova --save-to test_russian.wav

# English TTS (specialized English voices)  
python -m audiogram_cli.main tts file --config config.ini --text 'Hello, this is an English text-to-speech test.'
 --save-to test_english.wav

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

1. **Russian TTS Test**: Synthesizes the phrase "Тестирование синтеза прошло успешно" using the `gandzhaev` voice
2. **English TTS Test**: Synthesizes English text using `voice 2` with the `eng voice` model (22050 Hz)
3. **Multiple English Voices Test**: Tests `voice 1` and `voice 3` to ensure variety and accessibility
4. **ASR Test**: Recognizes the `1297.wav` audio file with punctuation enabled
5. **Prerequisites**: Validates configuration, credentials, and required files

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

# Run specific tests
python -m pytest tests/test_integration.py::TestIntegration::test_tts_gandzhaev_voice -v
python -m pytest tests/test_integration.py::TestIntegration::test_tts_english_voice -v
python -m pytest tests/test_integration.py::TestIntegration::test_tts_multiple_english_voices -v
python -m pytest tests/test_integration.py::TestIntegration::test_asr_with_punctuation -v

# Run all TTS tests only
python -m pytest tests/test_integration.py -k "tts" -v

# Run with detailed output
python -m pytest tests/test_integration.py -v -s
```

### TTS Testing Coverage

The integration tests provide comprehensive coverage for both Russian and English TTS functionality:

#### Russian TTS Testing
- **Voice**: `gandzhaev` (high-quality neural voice)
- **Sample Rate**: 22050 Hz for optimal quality
- **Model Type**: `high_quality` (auto-detected)
- **Test Phrase**: "Тестирование синтеза прошло успешно"
- **Validation**: Ensures audio file generation with minimum 1000 bytes

#### English TTS Testing
- **Primary Voice**: `voice 2` with `eng voice` model
- **Additional Voices**: `voice 1` and `voice 3` for variety testing
- **Sample Rate**: 22050 Hz for high-quality English synthesis
- **Model Type**: `eng voice` (specialized English model)
- **Test Phrases**: Natural English sentences for each voice
- **Validation**: Individual voice testing with size and quality verification

#### TTS Test Commands
```bash
# Test Russian TTS only
python -m pytest tests/test_integration.py::TestIntegration::test_tts_gandzhaev_voice -v -s

# Test primary English TTS
python -m pytest tests/test_integration.py::TestIntegration::test_tts_english_voice -v -s

# Test multiple English voices
python -m pytest tests/test_integration.py::TestIntegration::test_tts_multiple_english_voices -v -s

# Test all TTS functionality
python -m pytest tests/test_integration.py -k "tts" -v -s
```

### Test Requirements

For integration tests to work, you need:

- ✅ **Active virtual environment**
- ✅ **Valid credentials** (AUDIOGRAM_CLIENT_ID, AUDIOGRAM_CLIENT_SECRET)
- ✅ **Proper configuration** (`config.ini` file)
- ✅ **Test audio file** (`1297.wav` must exist)
- ✅ **Network connectivity** to Audiogram services
- ✅ **Voice permissions** for both Russian and English voices

### Test Output

Successful test run shows:
```
🎉 All tests passed successfully!

Test Results Summary:
  ✅ Russian TTS Test: Synthesized 'Тестирование синтеза прошло успешно' with gandzhaev voice
  ✅ English TTS Test: Synthesized English text with voice 2 (eng voice model)
  ✅ Multiple English Voices: Tested voice 1 and voice 3 for variety
  ✅ ASR Test: Recognized 1297.wav with punctuation enabled  
  ✅ Prerequisites: Configuration and audio file validation

The Audiogram services are working correctly! 🎯
```

### Troubleshooting Tests

If tests fail, common issues include:

#### General Issues
- **Missing credentials**: Set `AUDIOGRAM_CLIENT_ID` and `AUDIOGRAM_CLIENT_SECRET`
- **Network issues**: Check connectivity to `grpc.audiogram-demo.mts.ai:443`
- **Missing files**: Ensure `1297.wav` and `config.ini` exist
- **Virtual environment**: Make sure you've activated the virtual environment

#### Russian TTS Issues
- **Voice unavailable**: Verify `gandzhaev` voice is accessible with your account
- **Model type**: Ensure `high_quality` model type is available for Russian voices

#### English TTS Issues
- **English voices unavailable**: Verify English voices (`voice 1`, `voice 2`, `voice 3`) are accessible
- **Model type mismatch**: Ensure `eng voice` model type works with your English voice permissions
- **Sample rate issues**: English voices require 22050 Hz sample rate
- **Protobuf compatibility**: If English TTS fails but Russian works, check protobuf file versions

#### Specific Test Debugging
```bash
# Test only Russian TTS to isolate issues
python -m pytest tests/test_integration.py::TestIntegration::test_tts_gandzhaev_voice -v -s

# Test only English TTS primary voice
python -m pytest tests/test_integration.py::TestIntegration::test_tts_english_voice -v -s

# Check available models
python -m audiogram_cli.main models
```

For detailed error information, run tests with verbose output (`-v -s` flags).

## Contributing

Contributions are welcome! Please see the `improvements.md` file for a list of planned improvements.
