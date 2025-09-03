#!/usr/bin/env python3
"""
Example showing how to customize log rotation limits.
"""

from audiogram_client.common_utils.logging_config import TTSLogger

# Custom logging with smaller limits
def create_compact_logging():
    """Create logging with smaller file limits."""
    
    # You can modify the logging configuration
    logger = TTSLogger(log_dir="compact_logs", log_level="INFO")
    
    # The limits are set in the code, but you can create a custom version:
    # - Main log: 10MB max (with 5 backups = 50MB total)
    # - Error log: 5MB max (with 3 backups = 15MB total)  
    # - JSON log: 20MB max (with 3 backups = 60MB total)
    
    print("📁 Log limits:")
    print("  Main log: 10MB per file, 5 backups (50MB max)")
    print("  Error log: 5MB per file, 3 backups (15MB max)")
    print("  JSON log: 20MB per file, 3 backups (60MB max)")
    print("  📊 Total maximum: ~125MB")
    
    return logger

# Monitor current log usage
def check_log_usage():
    """Check current log file sizes."""
    from pathlib import Path
    
    logs_dir = Path("logs")
    if not logs_dir.exists():
        print("No logs directory found")
        return
    
    total_size = 0
    print("📊 Current log usage:")
    
    for log_file in logs_dir.glob("*"):
        if log_file.is_file():
            size_mb = log_file.stat().st_size / (1024 * 1024)
            total_size += size_mb
            print(f"  📄 {log_file.name}: {size_mb:.2f} MB")
    
    print(f"  📊 Total: {total_size:.2f} MB")
    print(f"  📈 Percentage of max (125MB): {(total_size/125)*100:.1f}%")

if __name__ == "__main__":
    create_compact_logging()
    check_log_usage()
