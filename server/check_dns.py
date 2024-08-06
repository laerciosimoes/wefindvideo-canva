import socket

def check_dns_resolution(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        print(f"DNS resolution successful: {hostname} -> {ip}")
    except Exception as e:
        print(f"DNS resolution failed: {e}")

check_dns_resolution('wefindvideo.blob.core.windows.net')