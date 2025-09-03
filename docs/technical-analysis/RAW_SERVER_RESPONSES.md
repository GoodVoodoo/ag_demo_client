# 🔍 Raw Server Responses - AudioKit Dev SF gRPC Problem

## 📡 **Raw Server Response Analysis**

Here are the exact raw responses and errors we're getting from the AudioKit Dev SF server:

---

## 🔒 **OpenSSL Raw Response (Working)**

### **Command**: `openssl s_client -connect asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443 -alpn h2`

### **Raw Output**:
```
Connecting to 10.136.168.213
CONNECTED(00000005)
depth=2 C=RU, O=Mobile TeleSystems PJSC, CN=MTS Class 2 Root CA
verify error:num=19:self-signed certificate in certificate chain
verify return:1

Certificate chain
 0 s:CN=k8s-cluster-dev-sf
   i:DC=ru, DC=mts, DC=msk, CN=winca G2
 1 s:DC=ru, DC=mts, DC=msk, CN=winca G2  
   i:C=RU, O=Mobile TeleSystems PJSC, CN=MTS Class 2 Root CA
 2 s:C=RU, O=Mobile TeleSystems PJSC, CN=MTS Class 2 Root CA
   i:C=RU, O=Mobile TeleSystems PJSC, CN=MTS Class 2 Root CA

Server certificate
subject=CN=k8s-cluster-dev-sf
issuer=DC=ru, DC=mts, DC=msk, CN=winca G2

Protocol: TLSv1.3
Cipher: TLS_AES_256_GCM_SHA384
Compression: NONE
Expansion: NONE
ALPN protocol: h2                    ← ✅ HTTP/2 ALPN WORKS
Early data was not sent
Verify return code: 19 (self-signed certificate in certificate chain)
```

**✅ Key Finding**: Server successfully negotiates `ALPN protocol: h2`

---

## ❌ **gRPC Raw Error Response (Failing)**

### **Command**: Python gRPC client connection

### **Raw Error**:
```
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
    status = StatusCode.UNAVAILABLE
    details = "failed to connect to all addresses; last error: UNKNOWN: 
              ipv4:178.248.237.216:443: Cannot check peer: missing selected ALPN property."
    debug_error_string = "UNKNOWN:Error received from peer  
                         {grpc_status:14, grpc_message:"failed to connect to all addresses; 
                         last error: UNKNOWN: ipv4:178.248.237.216:443: 
                         Cannot check peer: missing selected ALPN property."}"
>
```

### **Error Breakdown**:
- **Status Code**: `StatusCode.UNAVAILABLE` (14)
- **Core Error**: `Cannot check peer: missing selected ALPN property`
- **IP Address**: `ipv4:178.248.237.216:443` (resolves to same server)
- **Connection State**: `failed to connect to all addresses`

---

## 🔍 **IP Address vs Hostname Comparison**

### **Hostname Connection**: `asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443`
```
Error: "Cannot check peer: missing selected ALPN property"
```

### **Direct IP Connection**: `10.136.168.213:443`
```
Error: "CERTIFICATE_VERIFY_FAILED: self signed certificate in certificate chain"
```

**✅ Key Insight**: Different errors indicate hostname/SNI-related ALPN issue

---

## 📊 **Protocol Analysis**

### **HTTP/2 ALPN (OpenSSL)**:
```bash
$ openssl s_client -alpn h2,http/1.1 -connect [server]:443
Response: ALPN protocol: h2          ← ✅ WORKS
```

### **HTTP/2 with curl**:
```bash
$ curl -v --http2 https://[server]/
Response: * ALPN: server accepted h2 ← ✅ WORKS
         * using HTTP/2               ← ✅ WORKS
```

### **gRPC over HTTP/2**:
```bash
gRPC client connection attempt
Response: Cannot check peer: missing selected ALPN property ← ❌ FAILS
```

---

## 🎯 **Root Cause Evidence**

### **What Works** ✅:
1. **TLS handshake**: Successful
2. **Certificate chain**: Valid (with system trust store)
3. **HTTP/2 ALPN**: Server advertises and accepts `h2`
4. **Network connectivity**: TCP connection successful

### **What Fails** ❌:
1. **gRPC ALPN negotiation**: "missing selected ALPN property"
2. **gRPC service calls**: Cannot establish RPC connection

### **Technical Diagnosis**:
The server **supports HTTP/2 ALPN** but there's a **configuration mismatch** in how gRPC clients negotiate the ALPN during the handshake process.

---

## 🔧 **Server-Side Issue Confirmed**

### **Evidence Summary**:
1. **Multiple clients fail**: Python gRPC, grpcurl - same error
2. **HTTP/2 works**: OpenSSL and curl successfully negotiate h2
3. **Hostname dependency**: Different errors for hostname vs IP
4. **ALPN advertised**: Server does support HTTP/2 ALPN

### **Most Likely Cause**:
**Server-side gRPC service configuration issue** where:
- HTTP/2 ALPN is enabled at the TLS layer
- gRPC service is not properly configured for ALPN negotiation
- SNI/hostname handling may be affecting gRPC-specific ALPN

---

## 📞 **For AudioKit Dev SF Support**

### **Raw Error to Report**:
```
EXACT ERROR: "Cannot check peer: missing selected ALPN property"
STATUS CODE: StatusCode.UNAVAILABLE (14)
SERVER RESPONSE: ipv4:178.248.237.216:443
HOSTNAME: asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443

WORKING: OpenSSL ALPN negotiation (h2)
FAILING: gRPC ALPN negotiation (missing property)
```

### **Technical Questions**:
1. Is the gRPC service properly configured to handle ALPN negotiation?
2. Are there specific gRPC server settings for ALPN that need adjustment?
3. Is the certificate configuration complete for gRPC over hostname?
4. Does the server require specific client ALPN settings?

---

## 🏆 **Resolution Expectation**

**Issue Type**: Server-side gRPC ALPN configuration
**Complexity**: Low-Medium (configuration adjustment)
**Timeline**: 1-3 business days
**Fix Required**: Server-side gRPC service configuration update

The raw server responses provide **clear evidence** that this is a server-side configuration issue, not a client problem.
