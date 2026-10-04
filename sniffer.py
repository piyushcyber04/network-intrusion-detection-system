from scapy.all import sniff, IP, TCP, UDP, ICMP
from collections import defaultdict
import time
import requests

packet_counter = defaultdict(int)
first_seen = defaultdict(lambda: time.time())

THRESHOLD = 30
TIME_WINDOW = 10
SERVER_URL = "http://127.0.0.1:5000/add_alert"

def identify_activity(packet):
    # Detect protocol and port
    if packet.haslayer(TCP):
        port = packet[TCP].dport
        if port in [80, 443]:
            return "TCP", port, "Web Browsing / HTTPS 🌐"
        elif port == 22:
            return "TCP", port, "SSH Remote Login 🔐"
        elif port == 21:
            return "TCP", port, "FTP Transfer 📁"
        else:
            return "TCP", port, f"TCP Service on Port {port}"

    elif packet.haslayer(UDP):
        port = packet[UDP].dport
        if port == 53:
            return "UDP", port, "DNS Lookup 📡"
        else:
            return "UDP", port, f"UDP Service on Port {port}"

    elif packet.haslayer(ICMP):
        return "ICMP", "-", "Ping / Network Check 📶"

    return "Unknown", "-", "Unknown Traffic"

def send_alert(message):
    try:
        requests.post(SERVER_URL, json={"alert": message})
    except:
        pass

def process_packet(packet):
    if packet.haslayer(IP):
        src = packet[IP].src
        proto, port, activity = identify_activity(packet)
        current_time = time.time()

        packet_counter[src] += 1

        if current_time - first_seen[src] > TIME_WINDOW:
            packet_counter[src] = 1
            first_seen[src] = current_time

        if packet_counter[src] > THRESHOLD:
            alert = (
                f"🚨 IP: {src} | "
                f"Protocol: {proto} | "
                f"Port: {port} | "
                f"Activity: {activity} | "
                f"Rate: {packet_counter[src]}/{TIME_WINDOW}s"
            )
            print(alert)
            send_alert(alert)

            packet_counter[src] = 0
            first_seen[src] = current_time

sniff(prn=process_packet, store=False)
