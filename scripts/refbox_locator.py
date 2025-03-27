#!/usr/bin/env python3

import argparse
from scapy.all import sniff, get_if_list
from time import sleep
import threading

seen_ips = set()
lock = threading.Lock()

def start_sniffer(iface, port):
    print(f"Starting sniffer on {iface} (port {port})")
    try:
        sniff(
            iface=iface,
            filter=f"udp and dst port {port}",
            prn=lambda pkt: handle_packet(pkt),
            store=0,
        )
    except Exception as e:
        print(f"Sniffer failed on {iface}: {e}")

def handle_packet(pkt):
    ip = pkt[0][1].src  # assuming Ether/IP/UDP
    with lock:
        if ip not in seen_ips:
            print(f"Refbox located at: {ip}")
            seen_ips.add(ip)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP sniffer to detect refbox IPs.")
    parser.add_argument("port", type=int, nargs="?", default=4444, help="UDP port to sniff on (default: 4444)")
    args = parser.parse_args()

    interfaces = get_if_list()
    print(f"Sniffing on interfaces: {interfaces}")

    threads = []
    for iface in interfaces:
        t = threading.Thread(target=start_sniffer, args=(iface, args.port), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            sleep(0.2)
    except KeyboardInterrupt:
        print("Stopping sniffers.")
