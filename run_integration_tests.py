#!/usr/bin/env python3
"""
Test runner for Audiogram integration tests.

This script runs the TTS and ASR integration tests and provides clear output
about the test results. It's designed to be user-friendly and show meaningful
results even for non-technical users.

Usage:
    python run_integration_tests.py

Requirements:
    - Virtual environment must be activated
    - Credentials must be configured (AUDIOGRAM_CLIENT_ID and AUDIOGRAM_CLIENT_SECRET)
    - config.ini must be properly set up
    - 1297.wav file must exist for ASR testing
"""

import os
import subprocess
import sys
from pathlib import Path

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenv not available, continue without it
    pass


def check_environment():
    """Check that the environment is properly set up."""
    print("🔍 Checking environment setup...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        print("⚠️  WARNING: Virtual environment not detected. Please activate your virtual environment:")
        print("   source venv/bin/activate  # macOS/Linux")
        print("   venv\\Scripts\\Activate.ps1  # Windows PowerShell")
        print()
    
    # Check for required credentials
    client_id = os.getenv('AUDIOGRAM_CLIENT_ID')
    client_secret = os.getenv('AUDIOGRAM_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Missing credentials!")
        print("Please set the following environment variables:")
        print("   export AUDIOGRAM_CLIENT_ID='your-client-id'")
        print("   export AUDIOGRAM_CLIENT_SECRET='your-client-secret'")
        print()
        print("Or create a .env file with these variables.")
        return False
    
    # Check for config file
    config_path = Path('config.ini')
    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        return False
    
    # Check for test audio file
    audio_path = Path('1297.wav')
    if not audio_path.exists():
        print(f"❌ Test audio file not found: {audio_path}")
        return False
    
    print("✅ Environment setup looks good!")
    print(f"   Client ID: {client_id[:8]}...")
    print(f"   Config file: {config_path}")
    print(f"   Audio file: {audio_path} ({audio_path.stat().st_size} bytes)")
    print()
    
    return True


def run_tests():
    """Run the integration tests using pytest."""
    print("🚀 Running Audiogram integration tests...")
    print("=" * 60)
    
    # Run pytest with verbose output and capture results
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/test_integration.py", 
        "-v", 
        "--tb=short",
        "--no-header"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        # Print the output
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print("=" * 60)
        
        if result.returncode == 0:
            print("🎉 All tests passed successfully!")
            print()
            print("Test Results Summary:")
            print("  ✅ Russian TTS Test: Synthesized 'Тестирование синтеза прошло успешно' with gandzhaev voice")
            print("  ✅ English TTS Test: Synthesized English text with voice 2 (eng voice model)")
            print("  ✅ Multiple English Voices: Tested voice 1 and voice 3 for variety")
            print("  ✅ ASR Test: Recognized 1297.wav with punctuation enabled")
            print("  ✅ Prerequisites: Configuration and audio file validation")
            print()
            print("The Audiogram services are working correctly! 🎯")
        else:
            print("❌ Some tests failed!")
            print()
            print("Common issues:")
            print("  • Check your credentials (AUDIOGRAM_CLIENT_ID, AUDIOGRAM_CLIENT_SECRET)")
            print("  • Verify network connectivity")
            print("  • Ensure the gandzhaev voice is available for Russian TTS")
            print("  • Ensure English voices (voice 1, voice 2, voice 3) are available")
            print("  • Check that 1297.wav file exists and is valid")
            print("  • Verify that 'eng voice' model type is accessible with your account")
            print()
            print("For detailed error information, see the test output above.")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out after 5 minutes!")
        print("This might indicate network issues or service unavailability.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run tests: {e}")
        return False


def main():
    """Main function to run the test suite."""
    print("🎙️  Audiogram Integration Test Runner")
    print("=" * 40)
    print()
    
    # Check environment first
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above and try again.")
        sys.exit(1)
    
    # Run the tests
    success = run_tests()
    
    if success:
        print("\n🎊 Integration tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Integration tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
