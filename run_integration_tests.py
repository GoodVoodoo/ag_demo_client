#!/usr/bin/env python3
"""
Audiogram Integration Test Runner

This script runs integration tests for TTS and ASR functionality.
It provides clear output and can be run directly without pytest.

Usage:
    python run_integration_tests.py
    
Requirements:
    - Set environment variables: AUDIOGRAM_CLIENT_ID, AUDIOGRAM_CLIENT_SECRET
    - Ensure config.ini is properly configured
    - Test audio file 1297.wav should be present
"""

import os
import sys
import tempfile
import traceback
from pathlib import Path
from subprocess import PIPE, run
from typing import Dict, List, Tuple

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")


def print_test_result(test_name: str, passed: bool, details: str = "") -> None:
    """Print formatted test result."""
    status = f"{Colors.GREEN}✅ PASSED{Colors.END}" if passed else f"{Colors.RED}❌ FAILED{Colors.END}"
    print(f"{Colors.BOLD}{test_name}:{Colors.END} {status}")
    if details:
        for line in details.strip().split('\n'):
            print(f"   {line}")
    print()


def run_command(cmd: List[str]) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = run(cmd, stdout=PIPE, stderr=PIPE, text=True, timeout=120)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def check_prerequisites() -> bool:
    """Check if all prerequisites are met."""
    print_header("CHECKING PREREQUISITES")
    
    all_good = True
    
    # Check environment variables
    required_vars = ["AUDIOGRAM_CLIENT_ID", "AUDIOGRAM_CLIENT_SECRET"]
    for var in required_vars:
        if os.getenv(var):
            print(f"{Colors.GREEN}✅{Colors.END} Environment variable {var} is set")
        else:
            print(f"{Colors.RED}❌{Colors.END} Environment variable {var} is missing")
            all_good = False
    
    # Check config file
    if os.path.exists("config.ini"):
        print(f"{Colors.GREEN}✅{Colors.END} Configuration file config.ini found")
    else:
        print(f"{Colors.RED}❌{Colors.END} Configuration file config.ini not found")
        all_good = False
    
    # Check test audio file
    if os.path.exists("1297.wav"):
        file_size = os.path.getsize("1297.wav")
        print(f"{Colors.GREEN}✅{Colors.END} Test audio file 1297.wav found ({file_size} bytes)")
    else:
        print(f"{Colors.RED}❌{Colors.END} Test audio file 1297.wav not found")
        all_good = False
    
    # Check Python modules
    try:
        import audiogram_cli.main
        print(f"{Colors.GREEN}✅{Colors.END} Audiogram CLI module available")
    except ImportError as e:
        print(f"{Colors.RED}❌{Colors.END} Audiogram CLI module not available: {e}")
        all_good = False
    
    if not all_good:
        print(f"\n{Colors.RED}Prerequisites not met. Please fix the issues above before running tests.{Colors.END}")
        return False
    
    print(f"\n{Colors.GREEN}All prerequisites met!{Colors.END}")
    return True


def test_models_info() -> bool:
    """Test model information retrieval."""
    print(f"{Colors.BOLD}Testing Model Information Retrieval...{Colors.END}")
    
    cmd = [sys.executable, "-m", "audiogram_cli.main", "--config", "config.ini", "models"]
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code != 0:
        print_test_result("Model Info Test", False, f"Command failed with exit code {exit_code}\nStderr: {stderr}")
        return False
    
    if "model" not in stdout.lower():
        print_test_result("Model Info Test", False, "No model information found in output")
        return False
    
    print_test_result("Model Info Test", True, "Successfully retrieved model information")
    return True


def test_tts_synthesis() -> bool:
    """Test TTS synthesis with Russian text and gandzhaev voice."""
    print(f"{Colors.BOLD}Testing TTS Synthesis...{Colors.END}")
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        output_file = tmp_file.name
    
    try:
        cmd = [
            sys.executable, "-m", "audiogram_cli.main",
            "--config", "config.ini",
            "tts", "file",
            "--voice-name", "gandzhaev", 
            "--text", "Тестирование синтеза прошло успешно",
            "--output-file", output_file,
            "--sample-rate", "16000"
        ]
        
        exit_code, stdout, stderr = run_command(cmd)
        
        if exit_code != 0:
            print_test_result("TTS Synthesis Test", False, 
                            f"Command failed with exit code {exit_code}\nStderr: {stderr}")
            return False
        
        if not os.path.exists(output_file):
            print_test_result("TTS Synthesis Test", False, "Output audio file was not created")
            return False
        
        file_size = os.path.getsize(output_file)
        if file_size < 1000:
            print_test_result("TTS Synthesis Test", False, 
                            f"Output file too small ({file_size} bytes), likely corrupted")
            return False
        
        details = f"Generated audio file: {file_size} bytes\n"
        details += f"Voice: gandzhaev\n"
        details += f"Text: Тестирование синтеза прошло успешно"
        
        print_test_result("TTS Synthesis Test", True, details)
        return True
        
    finally:
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_asr_recognition() -> bool:
    """Test ASR recognition with punctuation."""
    print(f"{Colors.BOLD}Testing ASR Recognition...{Colors.END}")
    
    cmd = [
        sys.executable, "-m", "audiogram_cli.main",
        "--config", "config.ini",
        "asr", "file",
        "--audio-file", "1297.wav",
        "--model", "e2e-v3",
        "--enable-punctuator"
    ]
    
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code != 0:
        print_test_result("ASR Recognition Test", False,
                        f"Command failed with exit code {exit_code}\nStderr: {stderr}")
        return False
    
    if "Punctuator enabled: True" not in stdout:
        print_test_result("ASR Recognition Test", False, "Punctuator was not enabled")
        return False
    
    if "Hypothesis" not in stdout or "is_final: True" not in stdout:
        print_test_result("ASR Recognition Test", False, "No final recognition hypothesis found")
        return False
    
    # Extract recognized text
    recognized_text = ""
    lines = stdout.split('\n')
    for line in lines:
        if 'Hypothesis' in line and 'is_final: True' in line and '"' in line:
            start_quote = line.find('"')
            end_quote = line.rfind('"')
            if start_quote != -1 and end_quote != -1 and start_quote < end_quote:
                recognized_text = line[start_quote+1:end_quote]
                break
    
    details = f"Audio file: 1297.wav\n"
    details += f"Model: e2e-v3\n"
    details += f"Punctuation: enabled\n"
    details += f"Recognized text: '{recognized_text}'"
    
    print_test_result("ASR Recognition Test", True, details)
    return True


def main() -> int:
    """Main test runner function."""
    print_header("AUDIOGRAM INTEGRATION TESTS")
    
    if not check_prerequisites():
        return 1
    
    print_header("RUNNING TESTS")
    
    tests = [
        ("Model Information", test_models_info),
        ("TTS Synthesis", test_tts_synthesis), 
        ("ASR Recognition", test_asr_recognition),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print_test_result(f"{test_name} Test", False, f"Exception occurred: {str(e)}")
            if "--verbose" in sys.argv or "-v" in sys.argv:
                traceback.print_exc()
            results[test_name] = False
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASSED{Colors.END}" if result else f"{Colors.RED}FAILED{Colors.END}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{Colors.BOLD}Overall Result: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 All tests passed successfully!{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Some tests failed. Please check the output above.{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
