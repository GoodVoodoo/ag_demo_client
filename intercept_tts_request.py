import grpc
import json
from pathlib import Path
from concurrent import futures
from google.protobuf.json_format import MessageToJson

from audiogram_client.common_utils.config import Settings
# Corrected: We will implement the auth logic directly based on auth.py
from audiogram_client.common_utils.auth import get_token
from audiogram_client.tts.utils.request import make_tts_request
from audiogram_client.genproto.tts_pb2_grpc import TTSStub

def intercept_tts_communication():
    """
    Constructs and displays the original TTS request, then attempts to connect
    and displays the original server answer (which is a connection error).
    """
    print("--- 🔬 Intercepting TTS Request & Response ---")

    # 1. Load Configuration
    config_path = Path('config_audiokit_dev_sf.ini')
    if not config_path.exists():
        print(f"❌ ERROR: Configuration file not found at '{config_path}'")
        return
    settings = Settings([str(config_path)])

    # 2. Authenticate and get token
    print("\nSTEP 1: Authenticating to get token...")
    try:
        # Replicating the logic from get_authorization_metadata
        token = get_token(settings)
        auth_metadata = [('authorization', f'Bearer {token}')]
        print("✅ Authentication successful. Token metadata prepared.")
    except Exception as e:
        print(f"❌ Authentication Failed: {e}")
        return

    # 3. Construct the Original TTS Request
    print("\nSTEP 2: Constructing the original TTS request...")
    request_text = "Проверка связи с сервером AudioKit."
    tts_request = make_tts_request(
        text=request_text,
        voice_name='gandzhaev',
        rate=22050
    )
    request_json = json.loads(MessageToJson(tts_request, preserving_proto_field_name=True))
    
    print("✅ Request constructed.")

    # --- THIS IS THE ORIGINAL REQUEST ---
    print("\n" + "="*25 + " ORIGINAL REQUEST " + "="*25)
    print("This is the complete request that the client attempts to send.")
    
    print("\n▶️ HTTP/2 Headers:")
    print("-----------------")
    print(f"  :method: POST")
    print(f"  :scheme: https")
    print(f"  :path: /audiogram.tts.TTS/Synthesize")
    print(f"  :authority: {settings.api_address}")
    print(f"  authorization: Bearer [TOKEN_REDACTED_FOR_OUTPUT]")
    print(f"  content-type: application/grpc")
    print(f"  user-agent: grpc-python/1.74.0")

    print("\n▶️ gRPC Payload (JSON Format):")
    print("-----------------------------")
    print(json.dumps(request_json, indent=2, ensure_ascii=False))

    print("\n▶️ gRPC Payload (Raw Binary Bytes Sent):")
    print("---------------------------------------")
    serialized_data = tts_request.SerializeToString()
    print(f"  Size: {len(serialized_data)} bytes")
    print(f"  Data (hex): {serialized_data.hex()}")
    print("="*70)

    # 4. Attempt to Send Request and Capture Response
    print("\nSTEP 3: Sending request and capturing server answer...")
    
    # --- THIS IS THE ORIGINAL SERVER ANSWER ---
    print("\n" + "="*23 + " ORIGINAL SERVER ANSWER " + "="*23)
    try:
        creds = grpc.ssl_channel_credentials()
        with grpc.secure_channel(settings.api_address, creds) as channel:
            stub = TTSStub(channel)
            # This call will fail, and the exception is the "answer"
            response_iterator = stub.Synthesize(
                tts_request,
                metadata=auth_metadata,
                timeout=5
            )
            # We don't expect to get here
            print("✅ SUCCESS: Received a response stream from the server.")
            for response in response_iterator:
                if response.audio_chunk:
                    print(f"  - Received audio chunk of {len(response.audio_chunk)} bytes.")

    except grpc.RpcError as e:
        print("The server rejected the connection at the gRPC level.")
        print("\n▶️ gRPC Status:")
        print("---------------")
        print(f"  Code: {e.code()}")
        
        print("\n▶️ gRPC Error Details (This is the raw answer):")
        print("------------------------------------------------")
        print(f"  Details: {e.details()}")
        
        print("\n▶️ Debug String:")
        print("---------------")
        print(f"  Debug Info: {e.debug_error_string()}")

    except Exception as e:
        print("A non-gRPC error occurred during the connection attempt.")
        print("\n▶️ Error Type:")
        print("---------------")
        print(f"  {type(e).__name__}")
        print("\n▶️ Error Message:")
        print("----------------")
        print(f"  {e}")
        
    print("="*70)

if __name__ == '__main__':
    intercept_tts_communication()
