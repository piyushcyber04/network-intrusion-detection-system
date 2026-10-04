# Network Intrusion Detection System (NIDS)

A Python-based Network Intrusion Detection System that monitors network traffic, identifies common network protocols and services, and detects unusually high packet activity from source IP addresses using a configurable threshold-based detection mechanism.

The project uses **Scapy** for packet capture and analysis and a **Flask** web server to display and manage security alerts.

## Project Overview

This project was developed as a cybersecurity-focused network monitoring system.

The NIDS continuously captures IP packets and analyzes:

* Source IP address
* Network protocol
* Destination port
* Type of network activity
* Packet frequency within a defined time window

When a source IP generates more than **30 packets within 10 seconds**, the system generates a security alert and sends it to the Flask server.

## Key Features

* Real-time packet sniffing using Scapy
* IPv4 packet monitoring
* TCP, UDP, and ICMP protocol identification
* Destination port identification
* Basic network activity classification
* Source IP-based packet counting
* Threshold-based suspicious activity detection
* Configurable packet threshold and time window
* Automatic alert generation
* Flask REST endpoints for alert management
* Web-based alert display
* Duplicate alert prevention in the Flask alert list

## Technologies Used

| Technology | Purpose                                               |
| ---------- | ----------------------------------------------------- |
| Python     | Core implementation                                   |
| Scapy      | Network packet capture and analysis                   |
| Flask      | Web server and alert API                              |
| Requests   | Communication between packet sniffer and Flask server |
| HTML       | Web dashboard                                         |
| CSS        | Dashboard styling                                     |

## System Architecture

```text
                 Network Traffic
                       │
                       ▼
                ┌──────────────┐
                │    Scapy     │
                │ Packet Sniffer│
                └──────┬───────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Packet Analysis   │
              │                  │
              │ TCP / UDP / ICMP │
              │ Source IP        │
              │ Destination Port │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Activity Counter │
              │                  │
              │ 30 packets /     │
              │ 10 seconds       │
              └────────┬─────────┘
                       │
                Threshold Exceeded?
                    /        \
                  No          Yes
                  │            │
                  │            ▼
                  │      Generate Alert
                  │            │
                  │            ▼
                  │      HTTP POST Request
                  │            │
                  │            ▼
                  │      Flask Server
                  │            │
                  │            ▼
                  │       Alert Dashboard
                  │
                  └───────────────
```

## Detection Logic

The system maintains two counters for each source IP:

```text
packet_counter
first_seen
```

The current configuration is:

```python
THRESHOLD = 30
TIME_WINDOW = 10
```

This means that when a source IP generates more than **30 packets within a 10-second window**, the system generates an alert.

After an alert is generated, the packet counter for that source IP is reset.

### Example

If the system observes:

```text
Source IP: 192.168.1.10
Packets: 31
Time: 10 seconds
```

the system generates an alert containing:

```text
IP
Protocol
Port
Activity
Packet rate
```

## Network Activity Identification

The system identifies several common types of network activity.

### TCP

The destination port is inspected:

|  Port | Activity                 |
| ----: | ------------------------ |
|    80 | Web Browsing             |
|   443 | HTTPS                    |
|    22 | SSH Remote Login         |
|    21 | FTP Transfer             |
| Other | TCP Service on that port |

### UDP

|  Port | Activity                 |
| ----: | ------------------------ |
|    53 | DNS Lookup               |
| Other | UDP Service on that port |

### ICMP

ICMP traffic is classified as:

```text
Ping / Network Check
```

## Alert Generation

When the packet threshold is exceeded, an alert is created in the following format:

```text
🚨 IP: <source-ip> |
Protocol: <protocol> |
Port: <port> |
Activity: <activity> |
Rate: <packets>/<time-window>s
```

For example:

```text
🚨 IP: 192.168.1.10 | Protocol: TCP | Port: 443 |
Activity: Web Browsing / HTTPS 🌐 | Rate: 31/10s
```

The generated alert is printed to the terminal and sent to the Flask server using an HTTP POST request.

## Flask Alert Server

The Flask application provides three main routes.

### Home

```text
GET /
```

Displays the web dashboard using:

```text
templates/index.html
```

### Get Alerts

```text
GET /alerts
```

Returns the stored alerts as JSON.

### Add Alert

```text
POST /add_alert
```

Receives alerts from the packet sniffer and stores them in the Flask application's alert list.

The endpoint prevents the same alert string from being added more than once.

## Project Structure

```text
network-intrusion-detection-system/
│
├── app.py
├── sniffer.py
├── requirements.txt
│
├── static/
│   └── style.css
│
└── templates/
    └── index.html
```

### `app.py`

Contains the Flask web server and alert management API.

### `sniffer.py`

Contains the packet capture, protocol identification, packet counting, threshold detection, and alert generation logic.

### `templates/index.html`

Contains the web dashboard interface.

### `static/style.css`

Contains the styling for the dashboard.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/piyushcyber04/network-intrusion-detection-system.git
```

### 2. Navigate to the project

```bash
cd network-intrusion-detection-system
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Requirements

The project requires:

```text
Python 3.x
Flask
Scapy
Requests
```

On Windows, packet capture may also require **Npcap** and appropriate permissions.

## Running the Project

### Step 1 — Start the Flask server

Open a terminal in the project directory and run:

```bash
python app.py
```

The Flask server will run at:

```text
http://127.0.0.1:5000
```

### Step 2 — Start the packet sniffer

Open another terminal and run:

```bash
python sniffer.py
```

The sniffer will begin monitoring network packets.

When suspicious packet activity exceeds the configured threshold, the alert is sent to the Flask application.

## Configuration

The detection threshold can be modified in `sniffer.py`:

```python
THRESHOLD = 30
TIME_WINDOW = 10
```

For example, changing:

```python
THRESHOLD = 50
TIME_WINDOW = 15
```

would change the detection condition to more than 50 packets within a 15-second window.

## Current Limitations

This project uses a threshold-based detection approach and is intended as an educational cybersecurity project.

Current limitations include:

* Detection is based primarily on packet frequency.
* It does not currently use machine learning.
* It does not use a database for persistent alert storage.
* Alerts are stored in memory while the Flask application is running.
* It does not currently perform automated IP blocking.
* It does not integrate with an external SIEM or threat-intelligence platform.
* The current detection logic does not perform advanced payload inspection.

## Future Improvements

Possible future enhancements include:

* Machine-learning-based anomaly detection
* Signature-based intrusion detection
* Persistent alert storage using a database
* SIEM integration with Wazuh or Splunk
* Threat-intelligence and IP reputation integration
* Email or Telegram notifications
* Automated response and IP blocking
* Advanced packet and payload analysis
* Authentication for the monitoring dashboard
* Historical traffic and alert analytics

## Cybersecurity Concepts Demonstrated

This project provides practical experience with:

* Network packet analysis
* Network protocols
* TCP/UDP/ICMP traffic
* Port analysis
* Network monitoring
* Threshold-based anomaly detection
* Security alert generation
* REST API communication
* Python cybersecurity programming
* Flask-based security dashboards

## Disclaimer

This project is intended for educational and authorized defensive-security purposes.

Only monitor network traffic on systems and networks for which you have appropriate permission.

## Author

**Piyush Tiwari**

B.Tech Computer Science Engineering

Cybersecurity Enthusiast | Software Engineer

GitHub: [@piyushcyber04](https://github.com/piyushcyber04)
