#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scapy.all as scapy
import argparse, sys, re
from colorama import Fore, Style, init
from ipaddress import ip_network

init(autoreset=True)

class NetworkScanner:
    def __init__(self):
        self.devices = {}
        self.device_types = {
            "ac:9b:0a": "iPhone", "52:54:00": "Android", "b0:95:75": "Raspberry Pi",
            "68:a8:6d": "Samsung", "9c:20:7b": "LG", "00:1a:95": "Apple",
            "00:50:f2": "Windows", "08:00:27": "VirtualBox"
        }
        
    def print_header(self):
        print(f"""{Fore.RED}
╔══════════════════════════════════════════════════════╗
║         {Fore.CYAN}[ WIFI HUNTER SCANNER v3.0 ]{Fore.RED}               ║
║         {Fore.YELLOW}Advanced Network Discovery{Fore.RED}                 ║
║            {Fore.GREEN}~ by kaido dev ~{Fore.RED}                    ║
╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    def get_device_type(self, mac):
        mac_upper = mac.upper()
        for prefix, dtype in self.device_types.items():
            if mac.upper().startswith(prefix.upper()):
                return dtype
        if "00:00:00" in mac:
            return "Router"
        return "Unknown"
    
    def scan_network(self, net, timeout=3, retries=2, verbose=False):
        print(f"{Fore.CYAN}[*] Scanning {net}...{Style.RESET_ALL}\n")
        
        try:
            network = ip_network(net, strict=False)
        except:
            print(f"{Fore.RED}[-] Invalid network{Style.RESET_ALL}")
            return self.devices
        
        for ip in network.hosts():
            ip_str = str(ip)
            
            for attempt in range(retries):
                arp_req = scapy.ARP(pdst=ip_str)
                broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
                
                try:
                    answered = scapy.srp(broadcast/arp_req, timeout=timeout, verbose=False)[0]
                    
                    if answered:
                        mac = answered[0][1].hwsrc
                        dtype = self.get_device_type(mac)
                        
                        self.devices[ip_str] = {
                            'mac': mac,
                            'type': dtype
                        }
                        
                        if verbose or len(self.devices) % 5 == 0:
                            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {ip_str:15} {mac:20} {Fore.MAGENTA}{dtype}{Style.RESET_ALL}")
                        break
                except:
                    if attempt == retries - 1 and verbose:
                        print(f"{Fore.YELLOW}[-]{Style.RESET_ALL} {ip_str:15} No response")
        
        return self.devices
    
    def search_by_ip(self, ip):
        if ip in self.devices:
            dev = self.devices[ip]
            print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL}")
            print(f"  IP: {Fore.YELLOW}{ip}{Style.RESET_ALL}")
            print(f"  MAC: {Fore.MAGENTA}{dev['mac']}{Style.RESET_ALL}")
            print(f"  Type: {Fore.CYAN}{dev['type']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[NOT FOUND]{Style.RESET_ALL}")
    
    def search_by_mac(self, mac):
        for ip, dev in self.devices.items():
            if mac.lower() in dev['mac'].lower():
                print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL}")
                print(f"  IP: {Fore.YELLOW}{ip}{Style.RESET_ALL}")
                print(f"  MAC: {Fore.MAGENTA}{dev['mac']}{Style.RESET_ALL}")
                print(f"  Type: {Fore.CYAN}{dev['type']}{Style.RESET_ALL}")
                return
        print(f"{Fore.RED}[NOT FOUND]{Style.RESET_ALL}")
    
    def filter_by_type(self, dtype):
        results = {ip: dev for ip, dev in self.devices.items() if dtype.lower() in dev['type'].lower()}
        if not results:
            print(f"{Fore.YELLOW}No devices found{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}[{len(results)} devices found]{Style.RESET_ALL}\n")
        for ip, dev in results.items():
            print(f"{Fore.YELLOW}{ip:15}{Style.RESET_ALL} {dev['mac']:20} {Fore.CYAN}{dev['type']}{Style.RESET_ALL}")
    
    def show_results(self):
        if not self.devices:
            print(f"{Fore.RED}No devices found{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[SCAN RESULTS] Total: {len(self.devices)} devices{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        for ip, dev in sorted(self.devices.items()):
            print(f"{Fore.YELLOW}{ip:15}{Style.RESET_ALL} {dev['mac']:20} {Fore.CYAN}{dev['type']}{Style.RESET_ALL}")
        
        type_count = {}
        for dev in self.devices.values():
            dtype = dev['type']
            type_count[dtype] = type_count.get(dtype, 0) + 1
        
        print(f"\n{Fore.CYAN}[STATISTICS]{Style.RESET_ALL}")
        for dtype, count in sorted(type_count.items()):
            print(f"  {Fore.MAGENTA}{dtype:20}{Style.RESET_ALL} {count}")
        print()

def main():
    parser = argparse.ArgumentParser(description="WiFi Hunter Scanner v3.0")
    parser.add_argument("-t", "--target", help="Network range (192.168.1.0/24)")
    parser.add_argument("-timeout", type=int, default=3, help="Timeout (default: 3)")
    parser.add_argument("-retries", type=int, default=2, help="Retries (default: 2)")
    parser.add_argument("-search-ip", help="Search by IP")
    parser.add_argument("-search-mac", help="Search by MAC")
    parser.add_argument("-filter-vendor", help="Filter by type (Apple, Android, etc)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")
    parser.add_argument("-i", "--interface", help="Interface")
    
    args = parser.parse_args()
    
    scanner = NetworkScanner()
    scanner.print_header()
    
    if args.target:
        scanner.scan_network(args.target, args.timeout, args.retries, args.verbose)
        
        if args.search_ip:
            scanner.search_by_ip(args.search_ip)
        elif args.search_mac:
            scanner.search_by_mac(args.search_mac)
        elif args.filter_vendor:
            scanner.filter_by_type(args.filter_vendor)
        else:
            scanner.show_results()
    else:
        print(f"{Fore.YELLOW}[!] Usage: python wifi_hunter.py -t 192.168.1.0/24{Style.RESET_ALL}")
        print(f"    More examples:")
        print(f"    python wifi_hunter.py -t 192.168.1.0/24 -search-ip 192.168.1.5")
        print(f"    python wifi_hunter.py -t 192.168.1.0/24 -filter-vendor Apple")

if __name__ == "__main__":
    main()
