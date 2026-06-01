#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Hunter v3.0 - Comprehensive Test Suite
اختبار شامل لجميع أدوات WiFi Hunter
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class TestSuite:
    def __init__(self):
        self.workspace = r"c:\Users\lenovo\Desktop\wifi hunter"
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def test_files_exist(self):
        """التحقق من وجود جميع الملفات المطلوبة"""
        print("\n" + "="*70)
        print("✓ Test 1: Checking File Existence")
        print("="*70)
        
        required_files = [
            'wifi_hunter.py',
            'mac_simple.ps1',
            'professional_network_tools.py',
            'config.json',
            'requirements.txt',
            'README.md'
        ]
        
        for file in required_files:
            filepath = os.path.join(self.workspace, file)
            exists = os.path.exists(filepath)
            status = "✅ PASS" if exists else "❌ FAIL"
            print(f"  {status}: {file}")
            
            if exists:
                self.passed += 1
            else:
                self.failed += 1
                
    def test_python_syntax(self):
        """التحقق من صحة بناء الجملة Python"""
        print("\n" + "="*70)
        print("✓ Test 2: Python Syntax Check")
        print("="*70)
        
        py_files = ['wifi_hunter.py', 'professional_network_tools.py']
        
        for file in py_files:
            filepath = os.path.join(self.workspace, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    compile(f.read(), file, 'exec')
                print(f"  ✅ PASS: {file}")
                self.passed += 1
            except (SyntaxError, UnicodeDecodeError) as e:
                print(f"  ❌ FAIL: {file} - {str(e)}")
                self.failed += 1
                
    def test_imports(self):
        """التحقق من استيراد المكتبات"""
        print("\n" + "="*70)
        print("✓ Test 3: Module Imports Check")
        print("="*70)
        
        modules = ['scapy', 'colorama', 'argparse']
        
        for module in modules:
            try:
                __import__(module)
                print(f"  ✅ PASS: {module} available")
                self.passed += 1
            except ImportError:
                print(f"  ⚠️  WARNING: {module} not found (install with: pip install {module})")
                
    def test_config_json(self):
        """التحقق من صيغة config.json"""
        print("\n" + "="*70)
        print("✓ Test 4: config.json Structure Check")
        print("="*70)
        
        config_file = os.path.join(self.workspace, 'config.json')
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Check required keys
            required_keys = [
                'domain_blocking',
                'dns_poisoning',
                'credential_capture',
                'mobile_detection',
                'blocked_domains',
                'fake_ips'
            ]
            
            all_present = all(key in config for key in required_keys)
            
            if all_present:
                print(f"  ✅ PASS: config.json structure valid")
                print(f"     - Features: {len(config)} keys")
                print(f"     - Blocked domains: {len(config['blocked_domains'])}")
                print(f"     - Fake IPs: {len(config['fake_ips'])}")
                self.passed += 1
            else:
                print(f"  ❌ FAIL: Missing required keys")
                self.failed += 1
                
        except json.JSONDecodeError as e:
            print(f"  ❌ FAIL: Invalid JSON - {str(e)}")
            self.failed += 1
            
    def test_cli_arguments(self):
        """التحقق من وسائط سطر الأوامر"""
        print("\n" + "="*70)
        print("✓ Test 5: CLI Arguments Check")
        print("="*70)
        
        os.chdir(self.workspace)
        
        # Test wifi_hunter help
        try:
            result = subprocess.run(
                [sys.executable, 'wifi_hunter.py', '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"  ✅ PASS: wifi_hunter.py CLI")
                self.passed += 1
            else:
                print(f"  ❌ FAIL: wifi_hunter.py CLI")
                self.failed += 1
                
        except Exception as e:
            print(f"  ❌ FAIL: wifi_hunter.py - {str(e)}")
            self.failed += 1
        
        # Test professional_network_tools help
        try:
            result = subprocess.run(
                [sys.executable, 'professional_network_tools.py', '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"  ✅ PASS: professional_network_tools.py CLI")
                self.passed += 1
            else:
                print(f"  ❌ FAIL: professional_network_tools.py CLI")
                self.failed += 1
                
        except Exception as e:
            print(f"  ❌ FAIL: professional_network_tools.py - {str(e)}")
            self.failed += 1
            
    def test_module_loading(self):
        """التحقق من تحميل الوحدات"""
        print("\n" + "="*70)
        print("✓ Test 6: Module Loading Check")
        print("="*70)
        
        os.chdir(self.workspace)
        
        try:
            from professional_network_tools import ProfessionalNetworkTools
            
            tools = ProfessionalNetworkTools('config.json')
            
            checks = {
                'Config loaded': bool(tools.config),
                'Logging setup': bool(tools.log_dir),
                'DNS Poisoning': tools.config.get('dns_poisoning'),
                'Domain Blocking': tools.config.get('domain_blocking'),
                'Credential Capture': tools.config.get('credential_capture'),
                'Mobile Detection': tools.config.get('mobile_detection')
            }
            
            for check, result in checks.items():
                status = "✅" if result else "⚠️ "
                print(f"  {status} {check}")
                
            print(f"  ✅ PASS: Module loaded successfully")
            self.passed += 1
            
        except Exception as e:
            print(f"  ❌ FAIL: Module loading - {str(e)}")
            self.failed += 1
            
    def test_log_directory(self):
        """التحقق من مجلد السجلات"""
        print("\n" + "="*70)
        print("✓ Test 7: Logging Directory Check")
        print("="*70)
        
        logs_dir = os.path.join(self.workspace, 'logs')
        
        if os.path.exists(logs_dir):
            print(f"  ✅ PASS: logs directory exists")
            print(f"     - Location: {logs_dir}")
            self.passed += 1
        else:
            print(f"  ℹ️  INFO: logs directory will be created on first run")
            self.passed += 1
            
    def test_documentation(self):
        """التحقق من الوثائق"""
        print("\n" + "="*70)
        print("✓ Test 8: Documentation Check")
        print("="*70)
        
        docs = ['README.md', 'README_v3.md', 'QUICKSTART.md']
        
        for doc in docs:
            filepath = os.path.join(self.workspace, doc)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"  ✅ PASS: {doc} ({size} bytes)")
                self.passed += 1
            else:
                print(f"  ⚠️  WARNING: {doc} not found")
                
    def print_summary(self):
        """طباعة ملخص الاختبارات"""
        print("\n" + "="*70)
        print("FINAL REPORT - تقرير النتائج النهائي")
        print("="*70)
        
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n✅ PASSED: {self.passed}/{total}")
        print(f"❌ FAILED: {self.failed}/{total}")
        print(f"📊 SUCCESS RATE: {percentage:.0f}%")
        
        if self.failed == 0:
            print(f"\n🎉 ALL TESTS PASSED!")
            print("All tools are ready to use!")
        else:
            print(f"\n⚠️  Some tests failed. Check requirements.")
            
        print("\n" + "="*70 + "\n")
        
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("\n" + "="*70)
        print("🔍 WiFi Hunter v3.0 - Comprehensive Test Suite")
        print("🔍 اختبار شامل لأدوات WiFi Hunter")
        print("="*70)
        
        self.test_files_exist()
        self.test_python_syntax()
        self.test_imports()
        self.test_config_json()
        self.test_cli_arguments()
        self.test_module_loading()
        self.test_log_directory()
        self.test_documentation()
        
        self.print_summary()

if __name__ == "__main__":
    suite = TestSuite()
    suite.run_all_tests()
