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
        subprocess.run(["sudo", "ufw", "deny", "from", ip], check=True)
        print(f"Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Error blocking IP {ip}: {e}")
       


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
    
    # 임계치 초과 시 IP 차단
    for ip, count in failed_attempts.items():
        if ip in WHITELIST:
            print(f"⚪WHITELISTED IP: {ip}⚪")
            continue

        if count >= threshold:
            print(f"🔴Warning: {ip} has {count} failed Login Attacks!🔴")
            block_ip(ip)


