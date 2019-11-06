import os, sys, re, socket, subprocess


def validate_address_format(address):
    # IPv6 not supported
    ip_regex = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    hostname_regex = r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    return re.search(ip_regex, address) or re.search(hostname_regex, address)


def check_reachable(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, 80))
        return True
    except socket.error:
        return False


def error_check(hostname):
    if not validate_address_format(hostname):
        print("Error: invalid hostname {} ".format(hostname))
        exit(1)
    if not check_reachable(hostname):
        print("Error: {} is unreachable".format(hostname))
        exit(1)


def port_connect(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = sock.connect_ex((ip, port))
    sock.close()
    return not response


def port_scan(hostname, start_port, end_port):
    if start_port is None:
        start_port = 1
    if end_port is None:
        end_port = 65535
    ip = socket.gethostbyname(hostname)
    print("Scanning {} Port {}-{}".format(ip, start_port, end_port))
    for port in range(start_port, end_port + 1):
        if port_connect(ip, port):
            print("{}:{}/TCP is open".format(ip, port))
        else:
            print("{}:{}/TCP is closed".format(ip, port))


def main():
    hostname = sys.argv[1]
    error_check(hostname)
    port_scan(hostname, 21, 25)


main()