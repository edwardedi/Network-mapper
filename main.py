import sys
from concurrent.futures import ThreadPoolExecutor

def main():
    if len(sys.argv) < 2:
        print("Usage: network_mapper.py <CIDR> [port1, port2, ...]")
        sys.exit(1)

    cidr = sys.argv[1]
    ports = [80, 443, 22, 21, 445, 139, 8080] 
    if len(sys.argv) > 2:
        try:
            ports = list(map(int, sys.argv[2:]))
        except ValueError:
            print("Ports need to be integer numbers.")
            sys.exit(1)

if __name__ == "__main__":
    main()
