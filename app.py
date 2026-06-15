from datetime import datetime
import subprocess
import re
import time



file_path = "/var/log/auth.log"
search_string = "Failed password for"
failed_attempts = {}
threshold = 5
blocked_ips = set()

WHITELIST = [
    "127.0.0.1",      # localhost
    "192.168.218.1"   # 관리자 PC IP 주소 (예시)
]

# IP 주소 추출을 위한 정규표현식 패턴
ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"



# IP 차단 로직 구현 (UFW 자동 차단)
def block_ip(ip):
    try:
        subprocess.run(["sudo", "ufw", "deny", "from", ip], check=True, capture_output=True)
        print(f"Blocked IP: {ip}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error blocking IP {ip}: {e}")
        return False

# 차단된 IP를 파일(blocked_ips.txt)에 저장하는 로직 구현
def save_blocked_ip(ip, count):
    with open("blocked_ips.txt", "a", encoding="utf-8") as file:
        log_message = f"⚪{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} / {ip} / {count}\n"
        file.write(log_message)
        print(log_message.strip())

# 로그 파일을 실시간으로 모니터링하는 제너레이터 함수 구현
def follow_log(filename):
    with open(filename, "r", encoding="utf-8") as file:
        # 파일의 끝으로 이동
        file.seek(0, 2)

        while True:
            line = file.readline()
            if not line:
                time.sleep(1)
                continue
            # 새 로그 라인이 추가될 때마다 해당 라인을 반환
            yield line.strip()


# 로그 파일을 실시간으로 모니터링하면서 "Failed password for" 문자열이 포함된 라인을 찾고, 해당 라인에서 IP 주소를 추출하여 실패한 로그인 시도를 카운트하는 로직 구현
for line in follow_log(file_path):
    if search_string in line:
            print(line.strip())
            failed_log = line.strip()
            # IP 주소 추출
            ip_address = re.search(ip_regex, failed_log)
            if ip_address:
                ip = ip_address.group()
                if ip in blocked_ips:
                    print(f"⚪IP {ip} is already blocked⚪")
                    continue
                print("Failed IP Address:", ip)
                # 실패한 IP 주소를 딕셔너리에 저장, 횟수 카운트
                if ip not in failed_attempts:
                    failed_attempts[ip] = 1
                else:
                    failed_attempts[ip] += 1
                # WHITELIST 에 없고, 실패한 로그인 시도가 threshold 이상인 IP 주소를 차단
                if ip not in WHITELIST and failed_attempts[ip] >= threshold:
                    print(f"🔴Warning: {ip} has {failed_attempts[ip]} failed Login Attacks!🔴")
                    if block_ip(ip):
                        blocked_ips.add(ip)
                        save_blocked_ip(ip, failed_attempts[ip])



    

                


