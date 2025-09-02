# AudioKit Dev SF Voice Cloning Setup Guide

This guide explains how to configure and use the AudioKit Dev SF instance for voice cloning functionality.

## 🔧 Configuration Files

### 1. Main Configuration: `config_audiokit_dev_sf.ini`

The configuration file has been created with the following settings:

- **Endpoint**: `asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443`
- **SSL Certificate**: `WinCAG2ANDclass2root.pem`
- **SSO URL**: `https://isso.mts.ru/auth/`
- **Realm**: `mts`
- **IAM**: Not required (per administrator)

### 2. SSL Certificate Setup

**IMPORTANT**: You need to place the `WinCAG2ANDclass2root.pem` certificate file in the project root directory.

```bash
# Make sure the certificate file exists in the project root
ls -la WinCAG2ANDclass2root.pem
```

## 🔐 Credentials Setup

### Option 1: Environment Variables (Recommended)

Create or update your `.env` file with the AudioKit Dev SF credentials:

```bash
# AudioKit Dev SF Instance Credentials
AUDIOGRAM_CLIENT_ID=your-audiokit-dev-sf-client-id
AUDIOGRAM_CLIENT_SECRET=your-audiokit-dev-sf-client-secret

# AudioKit Dev SF Configuration
# Note: IAM settings not required for this instance
AUDIOGRAM_SSO_URL=https://isso.mts.ru/auth/
AUDIOGRAM_REALM=mts
AUDIOGRAM_API_ADDRESS=asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443
```

### Option 2: Direct Configuration File Edit

Edit `config_audiokit_dev_sf.ini` directly (less secure):

```ini
client_id = "your-audiokit-dev-sf-client-id"
client_secret = "your-audiokit-dev-sf-client-secret"
```

## 🚀 Usage Instructions

### Step 1: Prepare Environment

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Load environment variables (if using .env)
source .env

# 3. Verify certificate exists
ls -la WinCAG2ANDclass2root.pem
```

### Step 2: Test Connection

```bash
# Test connection to AudioKit Dev SF instance
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini models
```

### Step 3: Clone Voice

```bash
# Clone a voice using the AudioKit Dev SF instance
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini vc clone --audio-file voice_clonning_justai/voice_1_wav.wav
```

### Step 4: Check Task Status

```bash
# Check the status of your voice cloning task
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini vc get-task-info --task-id YOUR_TASK_ID
```

### Step 5: Use Cloned Voice

Once the voice is ready, you can use it for TTS:

```bash
# Synthesize speech using your cloned voice
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini tts file --text "Hello, this is my cloned voice!" --voice-name YOUR_VOICE_ID --output-file cloned_voice_output.wav
```

## 🔄 Switching Between Instances

### Demo Instance (ASR/TTS only)
```bash
# Use default config for demo instance
python -m audiogram_cli.main models
python -m audiogram_cli.main tts file --text "Hello" --voice-name borisova --output-file demo_output.wav
```

### AudioKit Dev SF Instance (Voice Cloning)
```bash
# Use AudioKit config for voice cloning
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini vc clone --audio-file your_audio.wav
```

## 📋 Command Reference

### Voice Cloning Commands

| Command | Description | Example |
|---------|-------------|---------|
| `vc clone` | Clone a voice from audio file | `--audio-file voice.wav` |
| `vc get-task-info` | Check cloning task status | `--task-id abc123` |
| `vc delete` | Delete a cloned voice | `--voice-id voice_xyz` |

### Configuration Options

| CLI Option | Config File Key | Description |
|------------|-----------------|-------------|
| `--config` | N/A | Path to config file |
| `--api-address` | `api_address` | gRPC endpoint |
| `--ca-cert` | `ca_cert_path` | SSL certificate path |
| `--client-id` | `client_id` | Authentication client ID |
| `--realm` | `realm` | Keycloak realm |

## 🛠️ Troubleshooting

### SSL Certificate Issues
```bash
# Verify certificate file exists and is readable
file WinCAG2ANDclass2root.pem
openssl x509 -in WinCAG2ANDclass2root.pem -text -noout
```

### Permission Issues
- Ensure your client credentials have voice cloning permissions
- Verify the IAM account and workspace are correct
- Check with your administrator for proper access rights

### Connection Issues
```bash
# Test basic connectivity
ping asr-tts-ha.dev.sf.audiokit.mts-corp.ru

# Test SSL handshake
openssl s_client -connect asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443 -CAfile WinCAG2ANDclass2root.pem
```

## 📝 Example Workflow

```bash
# 1. Setup
source venv/bin/activate
source .env

# 2. Clone voice
TASK_ID=$(python -m audiogram_cli.main --config config_audiokit_dev_sf.ini vc clone --audio-file voice_clonning_justai/voice_1_wav.wav | grep "task created with ID:" | cut -d' ' -f6)

# 3. Wait and check status
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini vc get-task-info --task-id $TASK_ID

# 4. Once ready, use the voice (replace VOICE_ID with actual ID from step 3)
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini tts file --text "This is my cloned voice speaking!" --voice-name VOICE_ID --output-file my_cloned_voice.wav
```

## ⚠️ Security Notes

- **Never commit** the `.env` file or certificates to version control
- Store the `WinCAG2ANDclass2root.pem` certificate securely
- Use environment variables for credentials in production
- Rotate credentials regularly
- Keep the certificate file updated as needed
