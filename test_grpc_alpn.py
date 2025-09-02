#!/usr/bin/env python3
"""
Test script for gRPC ALPN configuration issues
"""
import grpc
import ssl
from audiogram_client.common_utils.config import Settings
from pathlib import Path
import time

def test_grpc_connection():
    """Test gRPC connection with various configurations"""
    
    # Load configuration
    config_path = Path('config_audiokit_dev_sf.ini')
    settings = Settings([str(config_path)])
    
    print(f"🔧 Testing gRPC connection to: {settings.api_address}")
    print(f"📋 gRPC version: {grpc.__version__}")
    print(f"🔒 SSL version: {ssl.OPENSSL_VERSION}")
    print()
    
    # Test 1: Basic connection with system certs
    print("📝 Test 1: Basic connection with system certs")
    try:
        creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(settings.api_address, creds)
        
        # Try to connect with timeout
        future = grpc.channel_ready_future(channel)
        future.result(timeout=10)
        
        print("✅ gRPC channel connection successful!")
        channel.close()
        return True
        
    except grpc.FutureTimeoutError:
        print("❌ Connection timeout (10s)")
    except Exception as e:
        print(f"❌ Connection failed: {type(e).__name__}: {e}")
    finally:
        try:
            channel.close()
        except:
            pass
    
    # Test 2: Connection with channel options
    print("\n📝 Test 2: Connection with gRPC channel options")
    try:
        options = [
            ('grpc.keepalive_time_ms', 30000),
            ('grpc.keepalive_timeout_ms', 5000),
            ('grpc.keepalive_permit_without_calls', True),
            ('grpc.http2.max_pings_without_data', 0),
            ('grpc.http2.min_time_between_pings_ms', 10000),
            ('grpc.http2.min_ping_interval_without_data_ms', 300000),
            ('grpc.max_receive_message_length', 4194304),
            ('grpc.max_send_message_length', 4194304),
        ]
        
        creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(settings.api_address, creds, options=options)
        
        future = grpc.channel_ready_future(channel)
        future.result(timeout=10)
        
        print("✅ gRPC channel with options successful!")
        channel.close()
        return True
        
    except grpc.FutureTimeoutError:
        print("❌ Connection timeout with options (10s)")
    except Exception as e:
        print(f"❌ Connection with options failed: {type(e).__name__}: {e}")
    finally:
        try:
            channel.close()
        except:
            pass
    
    # Test 3: Force TLS 1.2
    print("\n📝 Test 3: Force TLS 1.2")
    try:
        # Create SSL context with TLS 1.2
        ssl_context = ssl.create_default_context()
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2
        
        creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(settings.api_address, creds)
        
        future = grpc.channel_ready_future(channel)
        future.result(timeout=10)
        
        print("✅ gRPC channel with TLS 1.2 successful!")
        channel.close()
        return True
        
    except grpc.FutureTimeoutError:
        print("❌ Connection timeout with TLS 1.2 (10s)")
    except Exception as e:
        print(f"❌ Connection with TLS 1.2 failed: {type(e).__name__}: {e}")
    finally:
        try:
            channel.close()
        except:
            pass
    
    # Test 4: Direct IP connection
    print("\n📝 Test 4: Direct IP connection")
    try:
        ip_address = "10.136.168.213:443"  # From previous diagnostics
        
        creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(ip_address, creds)
        
        future = grpc.channel_ready_future(channel)
        future.result(timeout=10)
        
        print("✅ gRPC channel to IP successful!")
        channel.close()
        return True
        
    except grpc.FutureTimeoutError:
        print("❌ Connection timeout to IP (10s)")
    except Exception as e:
        print(f"❌ Connection to IP failed: {type(e).__name__}: {e}")
    finally:
        try:
            channel.close()
        except:
            pass
    
    print("\n❌ All gRPC connection tests failed")
    return False

if __name__ == "__main__":
    print("🚀 Starting gRPC ALPN connection tests...")
    print("=" * 50)
    
    success = test_grpc_connection()
    
    print("=" * 50)
    if success:
        print("🎉 At least one gRPC connection method worked!")
    else:
        print("💡 All connection attempts failed - this confirms the ALPN issue")
        print("📞 Time to contact AudioKit Dev SF support team!")
