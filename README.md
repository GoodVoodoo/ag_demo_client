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
# Get all available models with statistics
python -m clients.main models info --config config.ini --show-stats

# Get only ASR models
python -m clients.main models recognize --config config.ini

# Get only TTS models  
python -m clients.main models synthesize --config config.ini
```

#### Advanced Model Queries
```bash
# Get models in JSON format
python -m clients.main models info --config config.ini --output-format json

# Filter by sample rate
python -m clients.main models info --config config.ini --filter-sample-rate 22050

# Filter TTS models by quality level
python -m clients.main models info --config config.ini --service tts --filter-quality High

# Group models by service type
python -m clients.main models info --config config.ini --group-by service

# Save detailed model information to file
python -m clients.main models info --config config.ini --output-format json --save-to models.json
```

#### Filtering and Grouping Options
```bash
# Filter by language
python -m clients.main models info --config config.ini --filter-language ru

# Group TTS models by voice name
python -m clients.main models synthesize --config config.ini --group-by-voice

# Sort by sample rate
python -m clients.main models info --config config.ini --sort-by sample_rate

# Verbose output with detailed information
python -m clients.main models info --config config.ini --verbose
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
python -m clients.main recognize file --audio-file audio.wav --config config.ini

# With enhanced features from MP3
python -m clients.main recognize file --audio-file your_audio.mp3 --config config.ini --enable-antispoofing --enable-punctuator --enable-genderage

# Using best model with converted audio
python -m clients.main recognize file --audio-file output/output.wav --config config.ini --model e2e-v3
```

#### Complete MP3 to ASR Workflow
```bash
# 1. Start with checking location (Windows PowerShell)
pwd

# 2. Convert MP3 to optimal format (if needed)
python audio_converter.py speech_recording.mp3 --output-dir converted

# 3. Run ASR with best available model
python -m clients.main recognize file --audio-file converted/output.wav --config config.ini --model e2e-v3 --enable-antispoofing --enable-punctuator

# 4. Check available ASR models
python -m clients.main models recognize --config config.ini
```

#### Streaming Recognition
```bash
# Real-time transcription
python -m clients.main recognize stream --audio-file audio.wav --config config.ini
```

#### Dumping request JSON (for debugging)
Print the JSON representation of the ASR request (RecognitionConfig) and audio byte-size. Metadata headers are not printed.

```bash
# File mode (macOS/Linux)
./venv/bin/python -m clients.main recognize file --audio-file ./SPK-13769/gen/GLEB_NEWS_000955.wav --config ./config.ini --dump-json-request

# Stream mode (macOS/Linux)
./venv/bin/python -m clients.main recognize stream --audio-file ./SPK-13769/gen/GLEB_NEWS_000955.wav --config ./config.ini --dump-json-request

# PowerShell examples
python -m clients.main recognize file --audio-file .\SPK-13769\gen\GLEB_NEWS_000955.wav --config .\config.ini --dump-json-request
python -m clients.main recognize stream --audio-file .\SPK-13769\gen\GLEB_NEWS_000955.wav --config .\config.ini --dump-json-request
```

### Text-to-Speech (TTS)

#### File-based Synthesis
```bash
# Basic synthesis
python -m clients.main synthesize file \
    --text "Привет, как дела?" \
    --config config.ini \
    --save-to output.wav

# Advanced synthesis with voice selection
python -m clients.main synthesize file \
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
python -m clients.main synthesize file \
    --text "<speak>Почему <emphasis strength='strong'>они</emphasis> не согласны?</speak>" \
    --config config.ini \
    --save-to emphasized.wav

# Number and date formatting
python -m clients.main synthesize file \
    --text "<speak>Сегодня <say-as interpret-as='date' format='genitive'>21.12</say-as></speak>" \
    --config config.ini \
    --save-to date_announcement.wav
```

#### Streaming Synthesis
```bash
# Real-time synthesis
python -m clients.main synthesize stream \
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

### JSON Output Example
```json
{
  "timestamp": "2025-01-06T12:40:36.123456",
  "service": "all",
  "total_count": 22,
  "request_ids": {
    "asr": "MR-25db467a-5491-40b2-a58e-d40c7d4950cc",
    "tts": "MS-4fe922ad-f22d-437c-8747-b9bbb8cd6e00"
  },
  "models": [
    {
      "name": "e2e-v3",
      "type": "ASR",
      "language_code": "ru",
      "sample_rate_hertz": 16000,
      "dictionaries": ["kion", "v0"],
      "quality_level": null
    }
  ]
}
```

### CSV Export
```bash
# Export model information to CSV
python -m clients.main models info --config config.ini --output-format csv --save-to models.csv
```

## Testing and Development

### Interactive Testing
```bash
# Run the interactive test script
python test_models_service.py
```

### Generate Usage Documentation
```bash
# Create comprehensive usage guide
python test_models_service.py
# Select option 2 to generate GetModelsInfo_Usage_Guide.md
```

### Command-line Testing Examples
```bash
# Test basic ASR functionality
python -m clients.main models recognize --config config.ini --verbose

# Test TTS with grouping
python -m clients.main models synthesize --config config.ini --group-by-voice

# Test comprehensive service with statistics
python -m clients.main models info --config config.ini --show-stats --verbose
```

## Integration Examples

### Python Script Integration
```python
from clients.models_service import ModelsService
from clients.common_utils.config import load_settings

# Load configuration
settings = load_settings("config.ini")

# Create service instance
service = ModelsService(settings)

# Get all models
all_models, request_ids = service.get_all_models()
print(f"Found {len(all_models)} total models")

# Filter models by criteria
asr_models = [m for m in all_models if m.type == "ASR"]
high_quality_tts = [m for m in all_models if m.type == "TTS" and m.quality_level == "High"]

print(f"ASR models: {len(asr_models)}")
print(f"High-quality TTS models: {len(high_quality_tts)}")
```

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

- **API Documentation**: See `AG_manual_ru.md` for complete API reference
- **Usage Examples**: Run `python test_models_service.py` for interactive examples
- **Generated Docs**: Use option 2 in test script to create detailed usage guide

## Contributing

When contributing to this project:
1. Follow the existing code structure
2. Add comprehensive error handling
3. Include usage examples in docstrings
4. Update tests for new functionality
5. Maintain compatibility with existing APIs

## License

This project is provided as demonstration code for MTS Audiogram services. See the license file for usage terms.