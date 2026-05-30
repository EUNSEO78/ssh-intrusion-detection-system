# print("SSH Defense System Start")

import re


file_path = "/var/log/auth.log"
search_string = "Failed password for"

with open(file_path, "r") as file:
    for line in file:
        if search_string in line:
            print(line.strip())
            failed_log = line.strip()
            # IP 주소 추출
            ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
            ip_address = re.search(ip_regex, failed_log)
            print(ip_address)
            if ip_address:
                print("Failed IP Address:", ip_address.group())



