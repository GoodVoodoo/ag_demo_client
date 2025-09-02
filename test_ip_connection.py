#!/usr/bin/env python3
"""
Test gRPC connection using direct IP address instead of hostname
"""
import grpc
import tempfile
import os
from pathlib import Path

def test_ip_vs_hostname():
    """Test gRPC connection to IP vs hostname"""
    
    hostname = "asr-tts-ha.dev.sf.audiokit.mts-corp.ru:443"
    ip_address = "10.136.168.213:443"
    
    print(f"🔧 Comparing gRPC connections:")
    print(f"   Hostname: {hostname}")
    print(f"   IP: {ip_address}")
    print()
    
    # Test 1: Hostname connection
    print("📝 Test 1: Hostname connection")
    try:
        creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(hostname, creds)
        
        future = grpc.channel_ready_future(channel)
        future.result(timeout=10)
        
        print("✅ Hostname connection successful!")
        channel.close()
        hostname_works = True
        
    except Exception as e:
        print(f"❌ Hostname connection failed: {type(e).__name__}: {e}")
        hostname_works = False
        try:
            channel.close()
        except:
            pass
    
    # Test 2: IP connection with SNI
    print("\n📝 Test 2: IP connection with proper SNI")
    try:
        # Use IP but keep proper SNI for certificate validation
        options = [
            ('grpc.ssl_target_name_override', 'asr-tts-ha.dev.sf.audiokit.mts-corp.ru'),
        ]
        
        creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(ip_address, creds, options=options)
        
        future = grpc.channel_ready_future(channel)
        future.result(timeout=10)
        
        print("✅ IP connection with SNI successful!")
        channel.close()
        ip_works = True
        
    except Exception as e:
        print(f"❌ IP connection with SNI failed: {type(e).__name__}: {e}")
        ip_works = False
        try:
            channel.close()
        except:
            pass
    
    # Test 3: IP connection without certificate validation (diagnostic only)
    print("\n📝 Test 3: IP connection without cert validation (diagnostic)")
    try:
        options = [
            ('grpc.ssl_target_name_override', 'asr-tts-ha.dev.sf.audiokit.mts-corp.ru'),
        ]
        
        # Use insecure credentials for testing
        channel = grpc.insecure_channel(ip_address)
        
        future = grpc.channel_ready_future(channel)
        future.result(timeout=10)
        
        print("✅ IP insecure connection successful!")
        channel.close()
        insecure_works = True
        
    except Exception as e:
        print(f"❌ IP insecure connection failed: {type(e).__name__}: {e}")
        insecure_works = False
        try:
            channel.close()
        except:
            pass
    
    return hostname_works, ip_works, insecure_works

def test_tts_with_ip():
    """Test actual TTS call using IP address"""
    from audiogram_client.common_utils.config import Settings
    from audiogram_client.common_utils.auth import get_auth_metadata
    from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
    from audiogram_client.genproto import tts_pb2, tts_pb2_grpc
    from audiogram_client.tts.utils.request import make_tts_request
    from audiogram_client.common_utils.types import TTSVoiceStyle
    
    print("\n🎯 Testing TTS with IP address")
    
    # Load configuration but override the address
    config_path = Path('config_audiokit_dev_sf.ini')
    settings = Settings([str(config_path)])
    
    # Override with IP address
    original_address = settings.api_address
    settings.api_address = "10.136.168.213:443"
    
    try:
        # Get auth metadata
        auth_metadata = get_auth_metadata(
            settings.sso_url,
            settings.realm,
            settings.client_id,
            settings.client_secret,
            settings.iam_account,
            settings.iam_workspace,
            settings.verify_sso,
        )
        print("✅ Authentication successful")

        # Create TTS request
        test_text = "IP address connection test successful"
        request = make_tts_request(
            text=test_text,
            is_ssml=False,
            voice_name="gandzhaev",
            rate=22050,
            model_type=None,
            model_rate=None,
            voice_style=TTSVoiceStyle.neutral,
        )
        print("✅ TTS request created")

        # Make gRPC call with IP address
        with open_grpc_channel(
            settings.api_address,
            ssl_creds_from_settings(settings),
        ) as channel:
            stub = tts_pb2_grpc.TTSStub(channel)
            print("✅ gRPC stub created")

            # Try the actual TTS call
            response = stub.Synthesize(
                request,
                metadata=auth_metadata,
                timeout=settings.timeout,
            )
            
            print(f"🎉 TTS SUCCESS! Generated {len(response.audio)} bytes of audio!")
            
            # Save to file for verification
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(response.audio)
                output_file = temp_file.name
            
            print(f"📁 Audio saved to: {output_file}")
            return True

    except Exception as e:
        print(f"❌ TTS with IP failed: {type(e).__name__}: {e}")
        return False
    
    finally:
        # Restore original address
        settings.api_address = original_address

if __name__ == "__main__":
    print("🚀 Testing IP address connection approach...")
    print("=" * 60)
    
    # Test connections
    hostname_ok, ip_ok, insecure_ok = test_ip_vs_hostname()
    
    print("\n" + "=" * 60)
    print("📊 Connection Results:")
    print(f"   Hostname: {'✅' if hostname_ok else '❌'}")
    print(f"   IP with SNI: {'✅' if ip_ok else '❌'}")
    print(f"   IP insecure: {'✅' if insecure_ok else '❌'}")
    
    # If any connection worked, try TTS
    if hostname_ok or ip_ok:
        print("\n" + "=" * 60)
        tts_success = test_tts_with_ip()
        
        if tts_success:
            print("\n🎉 IP ADDRESS SOLUTION FOUND!")
            print("💡 Update your config to use IP address directly")
        else:
            print("\n🤔 Connection works but TTS still fails")
    
    print("\n" + "=" * 60)
