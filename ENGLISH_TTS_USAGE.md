# English TTS Usage Guide for Audiogram

## Configuration

Based on the official specifications, here's how to use English TTS:

### English Voice Configuration:
- **language_code**: `"en"`
- **encoding**: `LINEAR_PCM`
- **sample_rate_hertz**: `8000`
- **voice_name**: `"voice 2"` (also available: `"voice 1"`, `"voice 3"`, `"voice 4"`)
- **text**: Use the `text` field (NOT `ssml`)
- **synthesize_options**:
  - **model_type**: `"eng voice"`
  - **voice_style**: `VOICE_STYLE_NEUTRAL`
  - **postprocessing_mode**: `POST_PROCESSING_DISABLE`
  - **custom_options**: `{"length_scale": 1.33}` (English only)

### Russian Voice Configuration (for comparison):
- **language_code**: `"ru"`
- **encoding**: `LINEAR_PCM`
- **sample_rate_hertz**: `8000`
- **voice_name**: `"borisova"` (or other Russian voices)
- **text**: Use the `ssml` field
- **synthesize_options**:
  - **model_type**: `"high_quality"`
  - **voice_style**: `VOICE_STYLE_NEUTRAL`
  - **postprocessing_mode**: `POST_PROCESSING_DISABLE`

## Code Example

```python
# English TTS
python -m audiogram_client.tts.synthesize \
    --text "Hello, this is English text to speech" \
    --voice-name "voice 2" \
    --model-type "eng voice" \
    --language-code "en" \
    --sample-rate 8000 \
    --save-to english_output.wav

# Russian TTS (using SSML)
python -m audiogram_client.tts.synthesize \
    --text "<speak>Привет, это русский текст для синтеза</speak>" \
    --read-ssml \
    --voice-name "borisova" \
    --model-type "high_quality" \
    --language-code "ru" \
    --sample-rate 8000 \
    --save-to russian_output.wav
```

## Note on Custom Options

The current CLI doesn't support custom options like `length_scale`. To use this feature, you'll need to use the Python API directly or modify the code to support custom options.

