# 📡 Original Request Analysis - JSON & Raw Data

## 🎯 **Complete Request Structure for AudioKit Dev SF**

Here are the original requests being sent to the server that result in the ALPN error:

---

## 📝 **JSON Request Payload (TTS Synthesize)**

### **Original Request Data**:
```json
{
  "text": "Тестирование AudioKit Dev SF прошло успешно",
  "language_code": "ru",
  "encoding": "LINEAR_PCM",
  "sample_rate_hertz": 22050,
  "voice_name": "gandzhaev",
  "synthesize_options": {}
}
```

### **Request Metadata**:
- **Text Length**: 43 characters (Russian)
- **Language**: `ru` (Russian)
- **Voice**: `gandzhaev`
- **Sample Rate**: `22050 Hz`
- **Encoding**: `LINEAR_PCM` (1)
- **Binary Size**: 93 bytes (protobuf)

### **Raw Protobuf Binary** (hex):
```
0a44d0a2d0b5d181d182d0b8d180d0bed0b2d0b0d0bdd0b8d0b520417564696f4b69742044657620534620d0bfd180d0bed188d0bbd0be20d183d181d0bfd0b5d188d0bdd0be1a027275200128a2ac01320967616e647a686165763a00
```

---

## 🔐 **Authentication Request Structure**

### **Keycloak Token Request**:
```http
POST https://isso.mts.ru/auth/realms/mts/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
client_id=audiogram-dev
client_secret=[REDACTED]
```

### **gRPC Authentication Metadata**:
```
authorization: Bearer [JWT_TOKEN]
user-agent: grpc-python/1.74.0
grpc-accept-encoding: gzip, deflate
```

---

## 📡 **Complete gRPC Call Structure**

### **HTTP/2 Request Headers**:
```http
POST /audiogram.tts.TTS/Synthesize HTTP/2
Host: asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443
Content-Type: application/grpc
Authorization: Bearer [JWT_TOKEN]
TE: trailers
User-Agent: grpc-python/1.74.0
Accept-Encoding: gzip, deflate
GRPC-Accept-Encoding: gzip
```

### **Service Definition**:
- **Service**: `audiogram.tts.TTS`
- **Method**: `Synthesize`
- **Request Type**: `SynthesizeSpeechRequest`
- **Response Type**: `SynthesizeSpeechResponse`

---

## 🔒 **OpenSSL Raw Handshake Data**

### **TLS Client Hello** (what OpenSSL sends):
```
>>> TLS 1.0, RecordHeader [length 0005]
    16 03 01 06 27
>>> TLS 1.3, Handshake [length 0627], ClientHello
    01 00 06 23 03 03 d6 8c 2f 08 fd 31 dd c1 cf 62
```

### **ALPN Extension in Client Hello**:
```
00 10 00 05 00 03 02 68 32
```
- **Extension Type**: `00 10` (ALPN)
- **Extension Length**: `00 05`
- **ALPN Data**: `00 03 02 68 32` = "h2" (HTTP/2)

### **Server Name Indication (SNI)**:
```
00 00 00 2b 00 29 00 00 26 61 73 72 2d 74 74 73 2d 68 61 2e 64 65 76 2e 73 66 2e 61 75 64 69 6f 6b 69 74 2e 6d 74 73 2d 63 6f 72 70 2e 72 75
```
Decoded: `asr-tts-ha.dev.sf.audiokit.mts-corp.ru`

---

## 🔍 **Request vs Response Analysis**

### **What Gets Sent Successfully** ✅:
1. **TLS Handshake**: Complete with ALPN `h2` extension
2. **SNI**: Correct hostname `asr-tts-ha.dev.sf.audiokit.mts-corp.ru`
3. **Certificate Validation**: Passes with system trust store
4. **HTTP/2 Negotiation**: Server accepts with `ALPN protocol: h2`

### **What Fails During gRPC** ❌:
```
grpc._channel._InactiveRpcError: 
  status = StatusCode.UNAVAILABLE
  details = "Cannot check peer: missing selected ALPN property"
```

### **Key Insight**:
- **OpenSSL handshake**: Successful ALPN negotiation
- **gRPC client handshake**: Fails at ALPN validation stage

---

## 🎯 **The Disconnect**

### **OpenSSL Perspective** (Working):
```
Client sends: ALPN extension with "h2"
Server responds: ALPN protocol: h2
Result: ✅ SUCCESS
```

### **gRPC Client Perspective** (Failing):
```
Client attempts: gRPC over HTTP/2 with ALPN
Server validation: "missing selected ALPN property"
Result: ❌ FAILURE
```

---

## 📊 **Technical Evidence for Support**

### **Request That Should Work**:
```json
{
  "service": "audiogram.tts.TTS",
  "method": "Synthesize",
  "request": {
    "text": "Тестирование AudioKit Dev SF прошло успешно",
    "language_code": "ru",
    "voice_name": "gandzhaev",
    "sample_rate_hertz": 22050,
    "encoding": "LINEAR_PCM"
  },
  "auth": "Bearer [JWT_TOKEN]",
  "protocol": "gRPC over HTTP/2"
}
```

### **Server Issue Evidence**:
1. **Valid request structure**: Properly formatted JSON/protobuf
2. **Successful authentication**: JWT token obtained
3. **Working ALPN**: OpenSSL proves server supports HTTP/2
4. **gRPC ALPN failure**: "missing selected ALPN property"

**Conclusion**: Server-side gRPC service not properly configured for ALPN negotiation despite HTTP/2 support being available.
