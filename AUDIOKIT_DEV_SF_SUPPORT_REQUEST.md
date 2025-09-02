# 🔧 AudioKit Dev SF Support Request - ALPN/gRPC Configuration

## 📋 **Issue Summary**

**Integration Status**: 95% Complete - SSL/TLS working, ALPN/gRPC configuration needed

**Current Error**: `Cannot check peer: missing selected ALPN property`

**Request**: Server-side gRPC ALPN configuration verification/fix

---

## 📧 **Email Template for AudioKit Dev SF Team**

### **Subject**: AudioKit Dev SF gRPC ALPN Configuration Issue - Integration Support Request

### **Email Body**:

```
Dear AudioKit Dev SF Technical Team,

I am working on integrating with the AudioKit Dev SF TTS endpoint and have encountered a gRPC protocol configuration issue that requires your assistance.

INTEGRATION STATUS:
✅ SSL/TLS certificates: Working correctly
✅ Authentication: Successful (Keycloak tokens obtained)
✅ Network connectivity: Established
❌ gRPC protocol: ALPN negotiation failing

TECHNICAL DETAILS:
- Endpoint: asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443
- Error: "Cannot check peer: missing selected ALPN property"
- SSL handshake: Successful
- Certificate validation: Working
- Authentication: Valid tokens obtained from https://isso.mts.ru/auth/

CURRENT TEST RESULTS:
- SSL certificate verification: ✅ PASS
- Authentication token retrieval: ✅ PASS  
- gRPC TTS synthesis calls: ❌ ALPN failure

TECHNICAL ANALYSIS:
🔍 **IMPORTANT UPDATE**: Diagnostic tests show the server DOES support HTTP/2 via ALPN:
- `ALPN: server accepted h2` ✅
- `using HTTP/2` ✅  
- SSL handshake successful ✅

However, gRPC clients are still getting "missing selected ALPN property" errors, suggesting a discrepancy between HTTP/2 ALPN support and gRPC-specific ALPN negotiation.

DIAGNOSTIC INFORMATION:
```bash
# SSL connection test (working):
openssl s_client -connect asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443 -servername asr-tts-ha.dev.sf.audiokit.mts-corp.ru

# ALPN test needed:
openssl s_client -connect asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443 -alpn h2,http/1.1
```

QUESTIONS FOR YOUR TEAM:
1. ✅ ALPN/HTTP2 confirmed working - server accepts `h2` protocol
2. **NEW ISSUE**: Why do gRPC clients get "missing selected ALPN property" when HTTP/2 ALPN works?
3. Are there any gRPC-specific ALPN requirements or content-type headers needed?
4. Is the gRPC service running on the same handler as the HTTP/2 endpoint?
5. Are there any specific client configuration requirements for gRPC calls?
6. Is there a different port or path for gRPC traffic? (e.g., `/grpc/` prefix)

DIAGNOSTIC RESULTS:
```bash
# ✅ ALPN HTTP/2 works:
curl: "ALPN: server accepted h2" and "using HTTP/2"

# ❌ gRPC ALPN fails:
grpc: "Cannot check peer: missing selected ALPN property"
```

CLIENT CONFIGURATION:
- Platform: macOS
- gRPC library: Python grpc (latest)
- SSL/TLS: Working with MTS Class 2 Root CA
- Authentication: Keycloak OAuth2 client credentials flow

REQUEST:
Please verify that the server at asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443 is properly configured to:
1. Advertise HTTP/2 (h2) protocol in ALPN during TLS handshake
2. Accept gRPC requests over HTTP/2
3. Handle gRPC TTS synthesis requests

If there are any specific configuration requirements or alternative endpoints for gRPC traffic, please provide details.

Thank you for your assistance in resolving this integration issue.

Best regards,
[Your Name]
[Your Contact Information]
[Company/Organization]
```

---

## 🔍 **Technical Details to Include**

### **Configuration Files**
- Share `config_audiokit_dev_sf.ini` (without sensitive credentials)
- Mention the complete certificate setup with MTS Class 2 Root CA

### **Error Logs**
```
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
status = StatusCode.UNAVAILABLE
details = "failed to connect to all addresses; last error: UNKNOWN: 
ipv4:178.248.237.216:443: Cannot check peer: missing selected ALPN property."
```

### **Working Components**
- Authentication: Keycloak token retrieval successful
- SSL/TLS: Certificate chain validation working
- Network: Can establish TCP connection to server

---

## 📞 **Contact Information to Find**

### **Where to Look for Support Contacts**:

1. **Check Documentation**:
   - Look in `AUDIOKIT_DEV_SF_SETUP.md`
   - Check any existing AudioKit documentation
   - Review integration guides or API documentation

2. **Common Contact Channels**:
   - Technical support email (usually support@domain or api-support@domain)
   - Integration/API team contact
   - DevOps/Infrastructure team for server configuration issues

3. **Internal Contacts**:
   - Your project manager or team lead
   - Whoever provided the AudioKit Dev SF credentials
   - System administrator who set up the integration

### **Suggested Contact Priority**:
1. **Primary**: AudioKit Dev SF technical/API support team
2. **Secondary**: Your internal team member who arranged this integration
3. **Escalation**: AudioKit Dev SF infrastructure/DevOps team

---

## 🧪 **Additional Diagnostic Commands**

Before contacting support, run these commands to gather more information:

```bash
# Check ALPN support
openssl s_client -connect asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443 -alpn h2,http/1.1 -servername asr-tts-ha.dev.sf.audiokit.mts-corp.ru

# Test HTTP/2 support
curl -v --http2 https://asr-tts-ha.dev.sf.audiokit.mts-corp.ru/

# Check if there's a health/status endpoint
curl -v https://asr-tts-ha.dev.sf.audiokit.mts-corp.ru/health
curl -v https://asr-tts-ha.dev.sf.audiokit.mts-corp.ru/status

# Test different ports (if any are documented)
nmap -p 443,8080,8443,9000,9443 asr-tts-ha.dev.sf.audiokit.mts-corp.ru
```

---

## 📝 **Information to Gather From Your Team**

Before contacting AudioKit Dev SF, collect this information:

1. **Project Details**:
   - Project name/ID
   - Integration timeline
   - Who arranged the AudioKit Dev SF access

2. **Documentation**:
   - Any integration guides provided by AudioKit Dev SF
   - API documentation or specifications
   - Contact information previously provided

3. **Credentials Source**:
   - Who provided the client credentials (`audiogram-dev`)
   - If there are specific technical contacts for this integration

4. **Environment Details**:
   - Is this a development/testing environment?
   - Are there production endpoints that might be different?
   - Any specific configuration requirements mentioned previously

---

## ⚡ **Quick Resolution Possibilities**

### **Alternative Endpoints to Try**:
If the team mentions alternative configurations, try:

```bash
# Different protocol or port
asr-tts-ha.dev.sf.audiokit.mts-corp.ru:8443
asr-tts-ha.dev.sf.audiokit.mts-corp.ru:9000

# HTTP instead of HTTPS (development only)
http://asr-tts-ha.dev.sf.audiokit.mts-corp.ru:8080
```

### **Configuration Adjustments**:
The team might suggest:
- Different gRPC channel options
- Specific TLS/SSL configuration
- Alternative authentication methods
- Different endpoint URLs

---

## 🎯 **Expected Resolution Timeline**

- **Immediate response**: Server configuration check (1-2 business days)
- **Resolution**: ALPN/HTTP2 configuration fix (2-5 business days)
- **Testing**: Verification of fix (1 day after resolution)

---

## ✅ **Success Criteria**

The issue will be resolved when:
1. `openssl s_client -alpn h2` shows HTTP/2 in server response
2. gRPC TTS synthesis calls succeed
3. Test suite shows 4/4 tests PASSED

Your integration will then be 100% complete and production-ready!
