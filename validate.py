#!/usr/bin/env python3

import os
import sys
import json
import subprocess

class ProjectValidator:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        
    def check(self, name, condition):
        if condition:
            print(f"✅ {name}")
            self.passed += 1
        else:
            print(f"❌ {name}")
            self.failed += 1
    
    def validate(self):
        print("🔍 WiFi Hunter - Project Validation\n")
        
        self.check("professional_network_tools.py exists", os.path.exists("professional_network_tools.py"))
        self.check("wifi_hunter.py exists", os.path.exists("wifi_hunter.py"))
        self.check("mac_simple.ps1 exists", os.path.exists("mac_simple.ps1"))
        self.check("config.json exists", os.path.exists("config.json"))
        self.check("requirements.txt exists", os.path.exists("requirements.txt"))
        self.check("README.md exists", os.path.exists("README.md"))
        self.check("LICENSE exists", os.path.exists("LICENSE"))
        self.check(".gitignore exists", os.path.exists(".gitignore"))
        
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
            self.check("config.json valid JSON", True)
            self.check("domain_blocking in config", "domain_blocking" in config)
            self.check("credential_capture in config", "credential_capture" in config)
        except:
            self.check("config.json valid JSON", False)
        
        try:
            result = subprocess.run([sys.executable, "professional_network_tools.py", "--help"],
                                  capture_output=True, text=True, timeout=5)
            self.check("professional_network_tools.py CLI", result.returncode == 0)
        except:
            self.check("professional_network_tools.py CLI", False)
        
        try:
            result = subprocess.run([sys.executable, "wifi_hunter.py", "--help"],
                                  capture_output=True, text=True, timeout=5)
            self.check("wifi_hunter.py CLI", result.returncode == 0)
        except:
            self.check("wifi_hunter.py CLI", False)
        
        print(f"\n📊 Results: {self.passed} passed, {self.failed} failed")
        return self.failed == 0

if __name__ == "__main__":
    validator = ProjectValidator()
    success = validator.validate()
    sys.exit(0 if success else 1)
