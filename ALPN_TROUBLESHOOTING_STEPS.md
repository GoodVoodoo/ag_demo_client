# 🔧 ALPN Issue Troubleshooting Steps - Try Before Contacting Support

## 🎯 **Quick Summary**
- ✅ HTTP/2 ALPN works: `curl` successfully negotiates `h2`
- ❌ gRPC ALPN fails: "missing selected ALPN property"
- **Issue**: Likely gRPC-specific configuration or client-side problem

## 🚀 **Immediate Actions to Try**

### **Step 1: Test with grpcurl (if available)**
```bash
# Install grpcurl if not available
brew install grpcurl

# Test gRPC connection
grpcurl -v -d '{}' asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443 list

# Test with insecure connection (diagnostic only)
grpcurl -v -plaintext -d '{}' asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443 list
```

### **Step 2: Try Alternative gRPC Configuration**
Let's modify the gRPC client to force specific ALPN behavior:

1. **Create a test script**:
```bash
cat > test_grpc_alpn.py << 'EOF'
import grpc
import ssl
from audiogram_client.common_utils.config import Settings
from pathlib import Path

# Load configuration
config_path = Path('config_audiokit_dev_sf.ini')
settings = Settings([str(config_path)])

# Create channel with explicit options
options = [
    ('grpc.keepalive_time_ms', 30000),
    ('grpc.keepalive_timeout_ms', 5000),
    ('grpc.keepalive_permit_without_calls', True),
    ('grpc.http2.max_pings_without_data', 0),
    ('grpc.http2.min_time_between_pings_ms', 10000),
    ('grpc.http2.min_ping_interval_without_data_ms', 300000)
]

# Test with system default certs
creds = grpc.ssl_channel_credentials()
channel = grpc.secure_channel(settings.api_address, creds, options=options)

try:
    # Simple connectivity test
    grpc.channel_ready_future(channel).result(timeout=10)
    print("✅ gRPC channel connection successful!")
except Exception as e:
    print(f"❌ gRPC connection failed: {e}")
finally:
    channel.close()
EOF

python test_grpc_alpn.py
```

### **Step 3: Try Different TLS/SSL Configurations**

**Option A: Force TLS 1.2**
```python
# Add to your test script
import ssl
ctx = ssl.create_default_context()
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
ctx.maximum_version = ssl.TLSVersion.TLSv1_2
creds = grpc.ssl_channel_credentials(root_certificates=None, private_key=None, certificate_chain=None)
```

**Option B: Test without client certificates**
Update `config_audiokit_dev_sf.ini`:
```ini
ca_cert_path = ""
cert_private_key_path = ""
cert_chain_path = ""
use_ssl = true
```

### **Step 4: Network Diagnostics**
```bash
# Check if there are multiple IPs
nslookup asr-tts-ha.dev.sf.audiokit.mts-corp.ru

# Test direct IP connection
openssl s_client -connect 10.136.168.213:443 -alpn h2,http/1.1 -servername asr-tts-ha.dev.sf.audiokit.mts-corp.ru

# Check for proxy/firewall issues
telnet asr-tts-ha.dev.sf.audiokit.mts-corp.ru 443
```

## 📞 **Contact Information Search**

### **Where to Find AudioKit Dev SF Support**:

1. **Check Internal Resources**:
   ```bash
   # Look for contact info in project files
   grep -r -i "support\|contact\|email\|team" . --include="*.md" --include="*.txt" --include="*.ini"
   
   # Check for documentation
   find . -name "*audiokit*" -o -name "*contact*" -o -name "*support*"
   ```

2. **Common Contact Patterns**:
   - `support@audiokit.mts-corp.ru`
   - `api-support@audiokit.mts-corp.ru` 
   - `dev-sf-support@audiokit.mts-corp.ru`
   - `technical-support@audiokit.mts-corp.ru`

3. **Check Your `.env` file source**:
   - Who provided the `audiogram-dev` credentials?
   - That person likely has the technical contact

### **Internal Team Contacts**:
1. **Project Manager/Team Lead** who arranged AudioKit Dev SF access
2. **DevOps/Infrastructure team** member who set up the integration
3. **Previous developers** who worked on this integration

## 📋 **Information to Gather Before Contact**

### **From Your Team**:
- [ ] Who provided the AudioKit Dev SF credentials?
- [ ] Is there existing AudioKit Dev SF documentation?
- [ ] Previous integration attempts or working examples?
- [ ] Technical contact information provided with credentials?

### **From Your Environment**:
```bash
# Gather system information
echo "macOS Version: $(sw_vers -productVersion)"
echo "Python Version: $(python --version)"
echo "gRPC Version: $(python -c 'import grpc; print(grpc.__version__)')"
echo "OpenSSL Version: $(openssl version)"

# Save current configuration
cp config_audiokit_dev_sf.ini config_backup_$(date +%Y%m%d).ini
```

## 🎯 **Most Likely Solutions**

### **Scenario 1: Different gRPC Endpoint**
The AudioKit team might say:
- "Use port 8443 for gRPC"
- "Add `/grpc` path prefix"
- "Use different subdomain for gRPC"

### **Scenario 2: Client Configuration**
They might require:
- Specific gRPC channel options
- Different authentication headers
- Modified TLS configuration

### **Scenario 3: Environment Issue**
Possible responses:
- "Development environment has known issues"
- "Use production endpoint instead"
- "Wait for upcoming server update"

## ⚡ **If You Get Immediate Resolution**

### **Test Script for Quick Validation**:
```bash
# After getting solution from AudioKit team, test with:
source venv/bin/activate
python -m pytest tests/test_integration.py::TestAudioKitDevSFIntegration::test_dev_sf_tts_gandzhaev_voice -v -s

# If successful, run full suite:
python -m pytest tests/test_integration.py::TestAudioKitDevSFIntegration -v
```

## 📝 **Documentation to Request**

When contacting support, also ask for:
1. **gRPC Integration Guide** specific to AudioKit Dev SF
2. **Example client code** (Python/gRPC)
3. **Troubleshooting documentation** for common issues
4. **Server status page** or health check endpoint
5. **Alternative endpoints** for development/testing

## 🎉 **Success Criteria**

You'll know it's fixed when:
- [ ] No more "missing selected ALPN property" errors
- [ ] gRPC TTS synthesis calls succeed
- [ ] Test suite shows 4/4 tests PASSED
- [ ] Audio files are generated successfully

**Expected timeline**: Most gRPC configuration issues are resolved within 1-3 business days once the right technical contact is reached.
