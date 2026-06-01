import re


file_path = "/var/log/auth.log"
search_string = "Failed password for"
failed_attempts = {}

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
                ip = ip_address.group()
                print("Failed IP Address:", ip)
                # 실패한 IP 주소를 딕셔너리에 저장, 횟수 카운트
                if ip not in failed_attempts:
                    failed_attempts[ip] = 1
                else:
                    failed_attempts[ip] += 1
                print("Failed Attempts List:", failed_attempts)
            



