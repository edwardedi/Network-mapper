import ipaddress
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5) # will raise a socket.timeout exception if it takes longer than 0.5 seconds to complete
            result = s.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "unknown"
                return f"{ip}:{port} ({service.upper()})"
    except Exception as e:
        pass
    return None

def scan_ip(ip, ports):
    online_ports = []
    for port in ports:
        result = scan_port(ip, port)
        if result:
            online_ports.append(result)
    return online_ports

def main():
    start_time = time.time()

    if len(sys.argv) < 2:
        print("Usage: network_mapper.py <CIDR> [port1, port2, ...]")
        sys.exit(1)

    cidr = sys.argv[1]
    ports = [80, 443, 22, 21, 445, 139, 8080] #HTTP, HTTPS, SSH, FTP, SMB, NetBIOS, HTTP-Proxy
    if len(sys.argv) > 2:
        try:
            ports = list(map(int, sys.argv[2:]))
        except ValueError:
            print("Ports need to be integer numbers.")
            sys.exit(1)

    try:
        network = ipaddress.ip_network(cidr, strict=False) 
    except ValueError:
        print("CIDR invalid.")
        sys.exit(1)

    print(f"Scanning network: {cidr}")
    print(f"On ports: {ports}")

    with ThreadPoolExecutor(max_workers = 800) as executor:
        thread_results = {executor.submit(scan_ip, str(ip), ports): ip for ip in network.hosts()}
        for th_result in thread_results:
            online_ports = th_result.result()
            if online_ports:
                for port in online_ports:
                    print(port)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed time: {round(elapsed_time,2)} seconds.")

if __name__ == "__main__":
    main()
