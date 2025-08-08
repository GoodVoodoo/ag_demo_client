# MTS Audiogram Demo Clients

This project provides comprehensive client implementations for MTS Audiogram services, with advanced support for Text-to-Speech (TTS) and Automatic Speech Recognition (ASR) functionality, including enhanced model information retrieval capabilities.

## Features

### Core Services
- **Text-to-Speech (TTS) Synthesis**
  - File-based synthesis with SSML support
  - Streaming synthesis for real-time applications
  - Multiple voice options and quality levels
  - Advanced voice styling and effects

- **Automatic Speech Recognition (ASR)**
  - File-based recognition with multiple model support
  - Streaming recognition for real-time applications
  - Anti-spoofing detection
  - Automatic punctuation and normalization

### Enhanced Model Information Services
- **Comprehensive Model Discovery**
  - Unified ASR and TTS model information retrieval
  - Advanced filtering and search capabilities
  - Multiple output formats (Table, JSON, CSV)
  - Statistical analysis and reporting

- **Model Management Features**
  - Language-based filtering
  - Sample rate compatibility checking
  - Quality level classification
  - Dictionary and capability mapping

### Additional Capabilities
- **Audio Format Conversion**
  - Support for MP4, MP3, WAV, M4A, AAC, OGG, FLAC
  - Optimized output for speech recognition
  - Video audio extraction with detailed metadata

- **Common Utilities**
  - Robust authentication and configuration management
  - gRPC client implementations with error handling
  - Advanced audio processing utilities

## Project Structure

```
.
├── clients/
│   ├── asr/                    # Automatic Speech Recognition
│   │   ├── get_models_info.py  # Enhanced ASR model information
│   │   ├── file_recognize.py   # File-based recognition
│   │   └── recognize.py        # Streaming recognition
│   ├── tts/                    # Text-to-Speech
│   │   ├── get_models_info.py  # Enhanced TTS model information
│   │   ├── synthesize.py       # File-based synthesis
│   │   └── stream_synthesize.py # Streaming synthesis
│   ├── models_service.py       # Comprehensive model service
│   ├── genproto/              # Generated protocol buffers
│   ├── audio_archive/         # Audio archive functionality
│   ├── common_utils/          # Shared utilities
│   │   ├── auth.py           # Authentication utilities
│   │   ├── audio.py          # Audio processing utilities
│   │   ├── config.py         # Configuration management
│   │   └── grpc.py           # gRPC client utilities
│   └── main.py               # Main CLI implementation
├── test_models_service.py     # Test and demo script
├── audio_converter.py         # Audio format converter utility
├── pyproject.toml            # Project configuration
├── config.ini               # Service configuration
└── output/                  # Default output directory
```

## Prerequisites

- **Python 3.11 or higher** (recommended for optimal performance)
- **FFmpeg** (required for audio conversion and processing)
- **Network access** to MTS Audiogram services
- **Valid authentication credentials** for the service

### Installing FFmpeg

#### Windows
```bash
# Using winget (Windows Package Manager)
winget install Gyan.FFmpeg

# Or download from: https://ffmpeg.org/download.html#build-windows
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ffmpeg

# Fedora/RHEL
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

#### macOS
```bash
# Using Homebrew
brew install ffmpeg

# Using MacPorts
sudo port install ffmpeg
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/mts-ai/audiogram-demo-clients.git
cd audiogram-demo-clients
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Unix/macOS
source venv/bin/activate
```

3. **Install the project:**
```bash
pip install -e .
```

## Configuration

1. **Create configuration file:**
```bash
python -m clients.main create-config
```

2. **Edit `config.ini` with your credentials:**
```ini
# gRPC API configuration
api_address = "grpc.audiogram-demo.mts.ai:443"
use_ssl = true
timeout = 60

# Authentication credentials
client_id = "your-client-id"
client_secret = "your-client-secret"
iam_account = "demo"
iam_workspace = "default"

# Keycloak configuration
sso_url = "https://sso.dev.mts.ai"
realm = "audiogram-demo"
verify_sso = true
```

## Usage Guide

### Using the bundled virtual environment
If you created a virtual environment in `venv/`, you can run commands via the venv Python directly:
```bash
./venv/bin/python -m clients.main models recognize --config ./config.ini
```

### Model Information Services

#### Quick Model Discovery
```bash
# Get only ASR models
audiogram models recognize --config config.ini

# Get only TTS models
audiogram models synthesize --config config.ini
```

```

#### Grouping Options
```bash
# Group TTS models by voice name
audiogram models synthesize --config config.ini --group-by-voice
```

### Automatic Speech Recognition (ASR)

#### Working with MP3 Files

##### Option 1: Direct ASR with MP3 (Recommended)
The ASR service supports MP3 files directly:
```bash
python -m clients.main recognize file --audio-file your_audio.mp3 --config config.ini
```

##### Option 2: Convert MP3 to WAV First (If needed)
If you encounter issues or want optimal format for ASR:

**Step 1: Convert MP3 to WAV**
```bash
python audio_converter.py your_audio.mp3 --output-dir output
```

This converts your MP3 to ASR-optimized WAV format:
- Mono channel
- 16kHz sample rate  
- 16-bit PCM encoding

**Step 2: Run ASR on converted file**
```bash
python -m clients.main recognize file --audio-file output/output.wav --config config.ini
```

#### Audio Format Support
The `audio_converter.py` utility supports these input formats:
- **Audio**: MP3, WAV, M4A, AAC, OGG, FLAC
- **Video**: MP4 (extracts audio automatically)

```bash
# List supported formats
python audio_converter.py --list-formats

# Convert with detailed output
python audio_converter.py my_speech.mp3 --output-dir converted
```

#### File-based Recognition
```bash
# Basic transcription
audiogram recognize file --audio-file audio.wav --config config.ini

# With enhanced features from MP3
audiogram recognize file --audio-file your_audio.mp3 --config config.ini --enable-antispoofing --enable-punctuator --enable-genderage

# Using best model with converted audio
audiogram recognize file --audio-file output/output.wav --config config.ini --model e2e-v3
```

#### Complete MP3 to ASR Workflow
```bash
# 1. Start with checking location (Windows PowerShell)
pwd

# 2. Convert MP3 to optimal format (if needed)
python audio_converter.py speech_recording.mp3 --output-dir converted

# 3. Run ASR with best available model
audiogram recognize file --audio-file converted/output.wav --config config.ini --model e2e-v3 --enable-antispoofing --enable-punctuator

# 4. Check available ASR models
audiogram models recognize --config config.ini
```

#### Streaming Recognition
```bash
# Real-time transcription
audiogram recognize stream --audio-file audio.wav --config config.ini
```

#### Dumping request JSON (for debugging)
Print the JSON representation of the ASR request (RecognitionConfig) and audio byte-size. Metadata headers are not printed.

```bash
# File mode (macOS/Linux)
audiogram recognize file --audio-file ./SPK-13769/gen/GLEB_NEWS_000955.wav --config ./config.ini --dump-json-request

# Stream mode (macOS/Linux)
audiogram recognize stream --audio-file ./SPK-13769/gen/GLEB_NEWS_000955.wav --config ./config.ini --dump-json-request

# PowerShell examples
audiogram recognize file --audio-file .\SPK-13769\gen\GLEB_NEWS_000955.wav --config .\config.ini --dump-json-request
audiogram recognize stream --audio-file .\SPK-13769\gen\GLEB_NEWS_000955.wav --config .\config.ini --dump-json-request
```

### Text-to-Speech (TTS)

#### File-based Synthesis
```bash
# Basic synthesis
audiogram synthesize file \
    --text "Привет, как дела?" \
    --config config.ini \
    --save-to output.wav

# Advanced synthesis with voice selection
audiogram synthesize file \
    --text "Ваш заказ готов к получению" \
    --config config.ini \
    --voice-name borisova \
    --sample-rate 22050 \
    --model-type high_quality \
    --voice-style neutral \
    --save-to order_ready.wav
```

#### SSML-Enhanced Synthesis
```bash
# Using SSML for advanced control
audiogram synthesize file \
    --text "<speak>Почему <emphasis strength='strong'>они</emphasis> не согласны?</speak>" \
    --config config.ini \
    --save-to emphasized.wav

# Number and date formatting
audiogram synthesize file \
    --text "<speak>Сегодня <say-as interpret-as='date' format='genitive'>21.12</say-as></speak>" \
    --config config.ini \
    --save-to date_announcement.wav
```

#### Streaming Synthesis
```bash
# Real-time synthesis
audiogram synthesize stream \
    --text "Длинный текст для потокового синтеза" \
    --config config.ini \
    --voice-name gandzhaev
```

## Available Models and Voices

### ASR Models
| Model Name | Language | Sample Rate | Dictionaries | Description |
|------------|----------|-------------|--------------|-------------|
| e2e-v3     | ru       | 16000 Hz    | kion, v0     | Latest conformer model with best accuracy |
| e2e-v1     | ru       | 16000 Hz    | kion, v0     | Stable conformer model |

### TTS Voices
| Voice Name  | Gender | Sample Rates    | Quality      | Languages |
|-------------|--------|-----------------|--------------|-----------| 
| borisova    | Female | 8000, 22050 Hz | high_quality | Russian   |
| kishchik    | Female | 8000, 22050 Hz | high_quality | Russian   |
| koryakina   | Female | 8000, 22050 Hz | high_quality | Russian   |
| gandzhaev   | Male   | 8000, 22050 Hz | high_quality | Russian   |
| gavrilov    | Male   | 8000, 22050 Hz | high_quality | Russian   |
| eldarov     | Male   | 8000, 22050 Hz | high_quality | Russian   |
| klukvin     | Male   | 8000, 22050 Hz | high_quality | Russian   |
| vostretsov  | Male   | 8000, 22050 Hz | high_quality | Russian   |
| voice 1-4   | Mixed  | 22050 Hz       | eng voice    | English   |

## Output Formats

## Testing and Development

### Command-line Testing Examples
```bash
# Test basic ASR functionality
audiogram models recognize --config config.ini --verbose

# Test TTS with grouping
audiogram models synthesize --config config.ini --group-by-voice
```

## Integration Examples
Use the `audiogram` CLI in your automation scripts or invoke the `clients` Python modules directly for advanced use.

## Error Handling and Troubleshooting

### Common Issues

1. **Authentication Failures**
   ```bash
   # Verify credentials
   python -m clients.main models info --config config.ini --verbose
   ```

2. **Connection Issues**
   ```bash
   # Test with increased timeout
   python -m clients.main models recognize --config config.ini --timeout 120
   ```

3. **Empty Results**
   ```bash
   # Check filters
   python -m clients.main models info --config config.ini --service all
   ```

### Debug Commands
```bash
# Verbose output for debugging
python -m clients.main models info --config config.ini --verbose

# Test individual services
python -m clients.main models recognize --config config.ini --verbose
python -m clients.main models synthesize --config config.ini --verbose
```

## Best Practices

1. **Model Selection**
   - Use `e2e-v3` for best ASR accuracy
   - Choose appropriate sample rates for your use case
   - Consider quality vs. performance trade-offs for TTS

2. **Audio File Preparation**
   - Try MP3 files directly with ASR first
   - Use `audio_converter.py` if conversion is needed
   - For best ASR results, ensure audio is:
     * Clear speech with minimal background noise
     * Mono channel, 16kHz sample rate preferred
     * Good quality recording (avoid heavily compressed audio)

3. **Performance Optimization**
   - Use filtering to reduce response sizes
   - Cache model information when possible
   - Use streaming for real-time applications
   - Convert large video files to audio-only format first

4. **File Management**
   - Save model information to JSON for programmatic use
   - Use CSV exports for analysis in spreadsheet applications
   - Implement proper error handling in production code
   - Keep converted files organized in output directories

## Advanced Features

### SSML Support
The TTS system supports comprehensive SSML (Speech Synthesis Markup Language) features:
- Voice selection and styling
- Emphasis and prosody control
- Date and number formatting
- Pause insertion and timing control

### Model Compatibility
- Automatic sample rate detection and conversion
- Language compatibility checking
- Quality level recommendations
- Dictionary availability verification

## Support and Documentation

- Refer to this README and inline `--help` for each CLI command: `audiogram --help`

## Contributing

When contributing to this project:
1. Follow the existing code structure
2. Add comprehensive error handling
3. Include usage examples in docstrings
4. Update tests for new functionality
5. Maintain compatibility with existing APIs

## License

This project is provided as demonstration code for MTS Audiogram services. See the license file for usage terms.