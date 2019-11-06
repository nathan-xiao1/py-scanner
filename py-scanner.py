import os, re, subprocess


def validate_address_format(address):
    # IPv6 not supported
    ip_regex = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    hostname_regex = r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    return re.search(ip_regex, address) or re.search(hostname_regex, address)


def ping(hostname):
    param = "-n" if os.name == "nt" else "-c"
    if subprocess.call(["ping", param, "1", hostname], stdout=open(os.devnull, 'w')) == 0:
        return True
    else:
        return False


def main():
    print(ping("google.com"))


main()