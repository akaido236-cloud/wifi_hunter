# 🔴 WIFI HUNTER v3.0 ELITE

```
╔══════════════════════════════════════════════════════════╗
║          [ WIFI HUNTER v3.0 ELITE ]                      ║
║      Advanced Network Penetration Suite                  ║
║    ARP │ DNS │ SSL │ CREDENTIAL │ INTERCEPTION           ║
║              ~ by kaido dev ~                            ║
╚══════════════════════════════════════════════════════════╝
```

Professional-grade network penetration toolkit for advanced network analysis, ARP spoofing, DNS sniffing, and credential capture. Built for security professionals and network administrators.

---

## ⚡ Quick Features

- ⚡ ARP Spoofing Engine
- 🔍 Advanced DNS Sniffer  
- 💾 Credential Extractor
- 📱 Mobile Device Detection
- 🚫 Domain Blocking & DNS Poisoning
- 📊 Comprehensive Logging & Statistics
- 🎨 Elite Hacker UI Design

---

## 🛠️ Tools Overview

### 1️⃣ Professional Network Tools
Advanced ARP spoofing and DNS interception.

```bash
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1
```

**Modes:**
- `full` - ARP + DNS (default)
- `spoof` - ARP only
- `sniff` - DNS only

### 2️⃣ WiFi Hunter Scanner
Network discovery and device detection.

```bash
python wifi_hunter.py -t 192.168.1.0/24
```

### 3️⃣ MAC Address Changer
Network identity spoofing.

```powershell
powershell -ExecutionPolicy Bypass -File mac_simple.ps1
```

---

## 📦 Installation

```bash
git clone https://github.com/akaido236-cloud/wifi_hunter.git
cd wifi_hunter
pip install -r requirements.txt
```

---

## 🔧 Usage Examples

### Scanner
```bash
python wifi_hunter.py -t 192.168.1.0/24 -v
python wifi_hunter.py -t 192.168.1.0/24 -search-ip 192.168.1.5
python wifi_hunter.py -t 192.168.1.0/24 -filter-vendor Apple
```

### Network Tools
```bash
python professional_network_tools.py -t 192.168.1.50 -g 192.168.1.1 -m full -v
python professional_network_tools.py -t 192.168.1.50 -g 192.168.1.1 -c config.json
```

### MAC Changer
```powershell
powershell -ExecutionPolicy Bypass -File mac_simple.ps1
```

---

## ⚙️ Configuration

Edit `config.json`:

```json
{
  "domain_blocking": true,
  "blocked_domains": ["ads.google.com"],
  "dns_poisoning": false,
  "credential_capture": true,
  "mobile_detection": true
}
```

---

## 📊 Logging

All data saved to `logs/`:
- `dns_*.txt` - DNS queries
- `credentials_*.txt` - Captured data
- `sessions_*.json` - Network sessions
- `stats_*.json` - Statistics

---

## 🔒 Legal & Ethics

⚠️ **For authorized security testing only**

- Only use on networks you own/have permission to test
- Unauthorized access is illegal
- Use responsibly and ethically

---

## 📋 Requirements

- Python 3.7+
- scapy >= 2.4.5
- colorama >= 0.4.3
- Windows 10/11 //linux (for full features)

---

## 🚀 Quick Start

```bash
# 1. Scan network
python wifi_hunter.py -t 192.168.1.0/24

# 2. Identify target
# (check output for IP)

# 3. Start analysis
python professional_network_tools.py -t [IP] -g 192.168.1.1

# 4. Review logs
# (check logs/ directory)
```

---

## 📄 License

MIT License - See LICENSE file

---

## 👤 Author

**kaido dev**

---

## ⭐ Show Your Support

Star this repository if you find it useful! ⭐

---

**Version:** 3.0 Elite  
**Status:** Stable ✅  
**Last Updated:** 2024
