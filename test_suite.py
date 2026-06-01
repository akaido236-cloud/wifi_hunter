#!/usr/bin/env python3
"""
WiFi Hunter - Complete Test Suite
اختبار شامل لجميع الأدوات
"""

import subprocess
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def print_header(title):
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[TEST] {title}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def test_wifi_scanner():
    """اختبار ماسح WiFi"""
    print_header("WiFi Scanner Test")
    
    print(f"{Fore.YELLOW}[*] Testing: wifi_hunter.py --help{Style.RESET_ALL}")
    
    try:
        result = subprocess.run(
            [sys.executable, "wifi_hunter.py", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}[✓] WiFi Scanner: OK{Style.RESET_ALL}")
            if "Network range" in result.stdout:
                print(f"{Fore.GREEN}[✓] Arguments parsed correctly{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[✗] WiFi Scanner: FAILED{Style.RESET_ALL}")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"{Fore.RED}[✗] Error: {str(e)}{Style.RESET_ALL}")
        return False

def test_advanced_tools():
    """اختبار Advanced Network Tools"""
    print_header("Advanced Network Tools Test")
    
    print(f"{Fore.YELLOW}[*] Testing: advanced_network_tools.py --help{Style.RESET_ALL}")
    
    try:
        result = subprocess.run(
            [sys.executable, "advanced_network_tools.py", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}[✓] Advanced Tools: OK{Style.RESET_ALL}")
            if "ARP Spoofing" in result.stdout or "TARGET" in result.stdout:
                print(f"{Fore.GREEN}[✓] Arguments parsed correctly{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[✗] Advanced Tools: FAILED{Style.RESET_ALL}")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"{Fore.RED}[✗] Error: {str(e)}{Style.RESET_ALL}")
        return False

def test_requirements():
    """اختبار المكتبات المطلوبة"""
    print_header("Requirements Test")
    
    required_modules = ["scapy", "colorama"]
    all_ok = True
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"{Fore.GREEN}[✓] {module}: Installed{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.RED}[✗] {module}: NOT installed{Style.RESET_ALL}")
            all_ok = False
    
    return all_ok

def test_files_exist():
    """اختبار وجود الملفات"""
    print_header("Files Existence Test")
    
    import os
    
    files = [
        "wifi_hunter.py",
        "advanced_network_tools.py",
        "mac_simple.ps1",
        "requirements.txt",
        "README.md"
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"{Fore.GREEN}[✓] {file}: {size} bytes{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] {file}: NOT FOUND{Style.RESET_ALL}")
            all_ok = False
    
    return all_ok

def test_syntax():
    """اختبار بناء الجملة"""
    print_header("Syntax Check")
    
    python_files = [
        "wifi_hunter.py",
        "advanced_network_tools.py"
    ]
    
    all_ok = True
    for file in python_files:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"{Fore.GREEN}[✓] {file}: Syntax OK{Style.RESET_ALL}")
        except SyntaxError as e:
            print(f"{Fore.RED}[✗] {file}: Syntax Error{Style.RESET_ALL}")
            print(f"    {e}")
            all_ok = False
        except Exception as e:
            print(f"{Fore.RED}[✗] {file}: Error - {str(e)}{Style.RESET_ALL}")
            all_ok = False
    
    return all_ok

def main():
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════╗
║     WiFi Hunter - Complete Test Suite              ║
║         اختبار شامل لجميع الأدوات               ║
╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    results = {
        "Files Existence": test_files_exist(),
        "Python Syntax": test_syntax(),
        "Requirements": test_requirements(),
        "WiFi Scanner": test_wifi_scanner(),
        "Advanced Tools": test_advanced_tools()
    }
    
    # النتائج النهائية
    print_header("Test Results Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if result else f"{Fore.RED}FAIL{Style.RESET_ALL}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"Total: {Fore.YELLOW}{passed}/{total}{Style.RESET_ALL} tests passed")
    
    if passed == total:
        print(f"\n{Fore.GREEN}[✓] All tests passed! Everything is ready!{Style.RESET_ALL}")
        return 0
    else:
        print(f"\n{Fore.RED}[✗] Some tests failed. Please check the errors above.{Style.RESET_ALL}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
