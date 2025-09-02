#!/usr/bin/env python3
"""
Test different TLS configurations for gRPC ALPN issues
"""
import grpc
import ssl
from audiogram_client.common_utils.config import Settings
from audiogram_client.common_utils.grpc import SSLCreds, open_grpc_channel, ssl_creds_from_settings
from pathlib import Path

def test_tls_configurations():
    """Test various TLS configurations"""
    
    config_path = Path('config_audiokit_dev_sf.ini')
    settings = Settings([str(config_path)])
    
    print(f"🔧 Testing TLS configurations for: {settings.api_address}")
    print()
    
    # Test 1: No custom certificates (system trust store)
    print("📝 Test 1: System trust store only")
    try:
        # Temporarily clear certificate path
        original_ca_path = settings.ca_cert_path
        settings.ca_cert_path = ""
        
        with open_grpc_channel(settings.api_address, ssl_creds_from_settings(settings)) as channel:
            # Try to create a stub
            from audiogram_client.genproto import tts_pb2_grpc
            stub = tts_pb2_grpc.TTSStub(channel)
            print("✅ Channel created with system trust store")
            return True
            
    except Exception as e:
        print(f"❌ System trust store failed: {type(e).__name__}: {e}")
    finally:
        settings.ca_cert_path = original_ca_path
    
    # Test 2: With our complete certificate bundle
    print("\n📝 Test 2: Complete certificate bundle")
    try:
        # Use the complete bundle we created
        settings.ca_cert_path = "ca_certificates_only.pem"
        
        with open_grpc_channel(settings.api_address, ssl_creds_from_settings(settings)) as channel:
            from audiogram_client.genproto import tts_pb2_grpc
            stub = tts_pb2_grpc.TTSStub(channel)
            print("✅ Channel created with certificate bundle")
            return True
            
    except Exception as e:
        print(f"❌ Certificate bundle failed: {type(e).__name__}: {e}")
    
    # Test 3: Disable SSL verification (testing only!)
    print("\n📝 Test 3: Insecure connection (testing only)")
    try:
        # Test insecure connection
        settings.use_ssl = False
        
        with open_grpc_channel(settings.api_address, ssl_creds_from_settings(settings)) as channel:
            from audiogram_client.genproto import tts_pb2_grpc
            stub = tts_pb2_grpc.TTSStub(channel)
            print("✅ Insecure channel created")
            return True
            
    except Exception as e:
        print(f"❌ Insecure connection failed: {type(e).__name__}: {e}")
    finally:
        settings.use_ssl = True
    
    # Test 4: Custom SSL context with specific settings
    print("\n📝 Test 4: Custom SSL context")
    try:
        # Create custom SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Create credentials with custom context
        creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(settings.api_address, creds)
        
        from audiogram_client.genproto import tts_pb2_grpc
        stub = tts_pb2_grpc.TTSStub(channel)
        
        print("✅ Custom SSL context channel created")
        channel.close()
        return True
        
    except Exception as e:
        print(f"❌ Custom SSL context failed: {type(e).__name__}: {e}")
    finally:
        try:
            channel.close()
        except:
            pass
    
    return False

if __name__ == "__main__":
    print("🚀 Starting TLS configuration tests...")
    print("=" * 50)
    
    success = test_tls_configurations()
    
    print("=" * 50)
    if success:
        print("🎉 Found a working TLS configuration!")
    else:
        print("💡 All TLS configurations failed")
        print("🔍 This suggests the issue is at the protocol level, not TLS")
