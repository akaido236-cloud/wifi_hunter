# WiFi Hunter - Complete Usage Guide

## 📋 Table of Contents

1. [Installation](#installation)
2. [Professional Network Tools](#professional-network-tools)
3. [WiFi Scanner](#wifi-scanner)
4. [MAC Address Changer](#mac-address-changer)
5. [Configuration](#configuration)
6. [Logging](#logging)
7. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Administrator privileges (Windows)
- Internet connection (for pip)

### Install Dependencies
```bash
pip install -r requirements.txt
```

If you encounter issues:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## Professional Network Tools

The main pentesting tool with ARP spoofing and DNS interception.

### Basic Usage
```bash
python professional_network_tools.py -t TARGET_IP -g GATEWAY_IP
```

### Arguments

| Argument | Short | Type | Required | Default | Description |
|----------|-------|------|----------|---------|-------------|
| --target | -t | IP | Yes | - | Target IP address |
| --gateway | -g | IP | Yes | - | Gateway IP address |
| --mode | -m | str | No | full | Mode: full, spoof, sniff |
| --verbose | -v | flag | No | False | Enable verbose output |
| --config | -c | file | No | - | JSON config file |

### Modes Explained

#### Mode: Full (Default)
ARP spoofing + DNS sniffer simultaneously.
```bash
python professional_network_tools.py -t 192.168.1.50 -g 192.168.1.1
```

#### Mode: Spoof
ARP spoofing only (no DNS sniffing).
```bash
python professional_network_tools.py -t 192.168.1.50 -g 192.168.1.1 -m spoof
```

#### Mode: Sniff
DNS sniffing only (no ARP spoofing).
```bash
python professional_network_tools.py -t 192.168.1.50 -g 192.168.1.1 -m sniff
```

### Advanced Examples

**With verbose output:**
```bash
python professional_network_tools.py -t 192.168.1.50 -g 192.168.1.1 -v
```

**With custom config:**
```bash
python professional_network_tools.py -t 192.168.1.50 -g 192.168.1.1 -c custom.json
```

**Monitor specific target silently:**
```bash
python professional_network_tools.py -t 192.168.1.100 -g 192.168.1.1 -m sniff
```

### What It Does

1. **ARP Spoofing**: Intercepts traffic between target and gateway
2. **DNS Interception**: Captures all DNS queries
3. **Credential Capture**: Extracts passwords from HTTP traffic
4. **Mobile Detection**: Identifies iPhone, Android devices
5. **Domain Blocking**: Blocks specified domains
6. **DNS Poisoning**: Redirects domains to fake IPs
7. **Logging**: Saves all data to JSON/TXT files

---

## WiFi Scanner

Network discovery and device identification tool.

### Basic Usage
```bash
python wifi_hunter.py -t NETWORK_RANGE
```

### Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| --target | -t | Network range (e.g., 192.168.1.0/24) |
| --timeout | - | Timeout per scan (default: 3) |
| --retries | - | Retry attempts (default: 2) |
| --search-ip | - | Search by IP address |
| --search-mac | - | Search by MAC address |
| --filter-vendor | - | Filter by device type |
| --verbose | -v | Verbose output |
| --interface | -i | Network interface |

### Usage Examples

**Basic network scan:**
```bash
python wifi_hunter.py -t 192.168.1.0/24
```

**Verbose scan:**
```bash
python wifi_hunter.py -t 192.168.1.0/24 -v
```

**Search for specific IP:**
```bash
python wifi_hunter.py -t 192.168.1.0/24 -search-ip 192.168.1.50
```

**Search by MAC address:**
```bash
python wifi_hunter.py -t 192.168.1.0/24 -search-mac "ac:9b:0a"
```

**Filter by device type:**
```bash
python wifi_hunter.py -t 192.168.1.0/24 -filter-vendor Apple
```

**Custom timeout and retries:**
```bash
python wifi_hunter.py -t 192.168.1.0/24 -timeout 5 -retries 3
```

### Output Example

```
[+] 192.168.1.1          ac:f1:df:12:34:56        Router
[+] 192.168.1.50         ac:9b:0a:ab:cd:ef        iPhone
[+] 192.168.1.51         52:54:00:12:34:56        Android
[+] 192.168.1.100        c8:5b:76:12:34:56        Windows PC
```

### Supported Device Types

- iPhone / iPad (Apple)
- Android Devices
- Raspberry Pi
- Samsung Devices
- LG Devices
- Windows PCs
- Linux Machines
- VirtualBox VMs

---

## MAC Address Changer

Change network MAC address on Windows.

### Usage

**Run as Administrator:**
```powershell
powershell -ExecutionPolicy Bypass -File mac_simple.ps1
```

### Menu Options

```
[MENU]
  1. List adapters       - Show available network adapters
  2. Change MAC          - Change MAC address
  3. Restore MAC         - Restore original MAC
  4. Exit                - Exit program
```

### How to Change MAC

1. Run script as Admin
2. Select option 2
3. Enter adapter name (e.g., "Ethernet", "Wi-Fi")
4. Enter new MAC address
5. Wait for restart
6. Done!

### MAC Address Formats

Both formats work:
- `AA:BB:CC:DD:EE:FF` (with colons)
- `AABBCCDDEEFF` (without colons)

### Example

```powershell
[MENU]
  1. List adapters
  2. Change MAC
  3. Restore MAC
  4. Exit

[>] Choice: 2
[>] Adapter name: Ethernet
[>] New MAC (AA:BB:CC:DD:EE:FF): AA:11:22:33:44:55
[+] Success! New MAC: AA:11:22:33:44:55
```

---

## Configuration

### config.json Structure

```json
{
  "domain_blocking": true,
  "blocked_domains": [
    "ads.google.com",
    "tracking.com",
    "analytics.google.com"
  ],
  "ssl_interception": true,
  "session_capture": true,
  "mobile_detection": true,
  "dns_poisoning": false,
  "credential_capture": true,
  "fake_ips": {
    "ads.google.com": "192.168.1.1",
    "facebook.com": "192.168.1.1"
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| domain_blocking | bool | true | Enable domain blocking |
| blocked_domains | array | [] | List of domains to block |
| ssl_interception | bool | true | Enable SSL interception |
| session_capture | bool | true | Capture network sessions |
| mobile_detection | bool | true | Detect mobile devices |
| dns_poisoning | bool | false | Enable DNS poisoning |
| credential_capture | bool | true | Capture credentials |
| fake_ips | object | {} | DNS poison mappings |

### Custom Configuration

Create `config.json`:
```bash
cp config.json custom.json
# Edit custom.json
python professional_network_tools.py -t 192.168.1.50 -g 192.168.1.1 -c custom.json
```

---

## Logging

### Log Directory Structure

```
logs/
├── dns_20240101_120000.txt
├── credentials_20240101_120000.txt
├── sessions_20240101_120000.json
└── stats_20240101_120000.json
```

### Log File Types

**DNS Log (dns_*.txt):**
```
[12:00:15] 192.168.1.50 -> google.com OK
[12:00:16] 192.168.1.50 -> ads.google.com BLOCKED
[12:00:17] 192.168.1.50 -> youtube.com OK
```

**Credentials Log (credentials_*.txt):**
```
[2024-01-01T12:00:15] 192.168.1.50 - ['password123']
[2024-01-01T12:00:20] 192.168.1.51 - ['secret456']
```

**Statistics (stats_*.json):**
```json
{
  "packets": 1542,
  "data": 45230,
  "ips": ["192.168.1.50", "192.168.1.100"],
  "http": 256,
  "https": 512,
  "dns": 128
}
```

---

## Troubleshooting

### Common Issues

#### "Permission Denied"
```
Solution: Run as Administrator
- Windows: Run Command Prompt as Admin
- Linux: Use sudo
```

#### "No module named scapy"
```
Solution: Install dependencies
pip install -r requirements.txt
```

#### "Connection failed"
```
Solution: Verify connectivity
- Check target IP is reachable
- Verify gateway IP is correct
- Ensure you're on the same network
```

#### "No DNS queries captured"
```
Solution: Target may have DNS protection
- Check if target uses VPN
- Check for DNS over HTTPS
- Use -m sniff mode
```

#### "MAC change not working"
```
Solution: Run as Administrator
- Right-click Command Prompt
- Select "Run as administrator"
- Try again
```

---

## Performance Tips

1. Use `-m sniff` for DNS only (lower load)
2. Exclude large networks if possible
3. Use `-timeout 1` for faster scans
4. Close unnecessary programs

---

## Security Reminders

- ⚠️ Only use on authorized networks
- ⚠️ Inform network administrator
- ⚠️ Don't use for illegal purposes
- ⚠️ Follow local laws

---

## Support

For issues and questions:
- Check existing issues on GitHub
- Create new issue with details
- Include error messages
- Describe steps to reproduce

---

**Happy hunting!** 🚀
