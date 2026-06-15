from datetime import datetime
import subprocess
import re



file_path = "/var/log/auth.log"
search_string = "Failed password for"
failed_attempts = {}
threshold = 5

WHITELIST = [
    "127.0.0.1",      # localhost
    "192.168.218.1"   # 관리자 PC IP 주소 (예시)
]

# IP 차단 로직 구현 (UFW 자동 차단)
def block_ip(ip):
    try:
        subprocess.run(["sudo", "ufw", "deny", "from", ip], check=True, capture_output=True)
        print(f"Blocked IP: {ip}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error blocking IP {ip}: {e}")
        return False

# 차단된 IP를 파일(blocked_ips.txt)에 저장
def save_blocked_ip(ip, count):
    with open("blocked_ips.txt", "a", encoding="utf-8") as file:
        log_message = f"⚪{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} / {ip} / {count}\n"
        file.write(log_message)
        print(log_message.strip())


# IP 주소 추출을 위한 정규표현식 패턴
ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"



with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        if search_string in line:
            print(line.strip())
            failed_log = line.strip()
            # IP 주소 추출
            ip_address = re.search(ip_regex, failed_log)
            if ip_address:
                ip = ip_address.group()
                print("Failed IP Address:", ip)
                # 실패한 IP 주소를 딕셔너리에 저장, 횟수 카운트
                if ip not in failed_attempts:
                    failed_attempts[ip] = 1
                else:
                    failed_attempts[ip] += 1
                print("Failed Attempts List:", failed_attempts)
    
# 임계치 초과 시 IP 차단
for ip, count in failed_attempts.items():
    if ip in WHITELIST:
        print(f"⚪WHITELISTED IP: {ip}⚪")
        continue

    if count >= threshold:
        print(f"🔴Warning: {ip} has {count} failed Login Attacks!🔴")
        if block_ip(ip):
                save_blocked_ip(ip, count)


