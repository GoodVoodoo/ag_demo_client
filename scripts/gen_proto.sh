#!/bin/bash
set -e

# This script regenerates the gRPC client code from the .proto files.

# Ensure the output directory exists
mkdir -p audiogram_client/genproto

# Generate Python code from .proto files
python -m grpc_tools.protoc \
    --proto_path=proto \
    --python_out=audiogram_client/genproto \
    --grpc_python_out=audiogram_client/genproto \
    proto/stt.proto proto/tts.proto

# Add __init__.py to the generated directories to make them packages
touch audiogram_client/genproto/__init__.py

echo "✅ Protobuf files regenerated successfully."
