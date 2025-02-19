import configparser
import grpc
from typing import Optional

def create_channel(config_path: str, credentials: Optional[grpc.ChannelCredentials] = None) -> grpc.Channel:
    """Create gRPC channel from config"""
    config = configparser.ConfigParser()
    config.read(config_path)

    if 'connection' not in config:
        raise ValueError("Config file must contain 'connection' section")

    conn_config = config['connection']
    host = conn_config.get('host', 'localhost')
    port = conn_config.getint('port', 50051)
    endpoint = f"{host}:{port}"

    if credentials:
        return grpc.secure_channel(endpoint, credentials)
    else:
        return grpc.insecure_channel(endpoint) 