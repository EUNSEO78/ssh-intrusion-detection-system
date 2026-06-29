![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-E95420?logo=ubuntu)
![UFW](https://img.shields.io/badge/Firewall-UFW-red)
![Discord](https://img.shields.io/badge/Discord-Webhook-5865F2?logo=discord)


# 🛡️ SSH Intrusion Detection & Auto-Blocking System

**SSH 로그인 실패 로그**를 **실시간으로 모니터링**하여 **Brute Force 공격을 탐지**하고, 

일정 횟수 이상 공격이 발생하면 **UFW**를 통해 **공격 IP**를 **자동 차단**하며,

**Discord Webhook**을 통해 **실시간 알림**을 제공하는 **보안 자동화 프로젝트** 입니다.

---

## ✨ Features

- 🔍 `/var/log/auth.log` 실시간 모니터링
- 🚨 SSH Brute Force 공격 탐지
- ⛔ UFW 기반 공격 IP 자동 차단
- 🔁 일정 시간 후 자동 차단 해제
- 🔔 Discord Webhook 실시간 알림
- 🗜️ systemd 서비스 등록 및 자동 실행

---

## 🏗️ Architecture

![Architecture](architecture-image.png)

---

## 🧰 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3 |
| OS | Ubuntu Server 24.04 |
| Attack Environment | Kali Linux |
| Firewall | UFW |
| SSH | OpenSSH |
| Notification | Discord Webhook |
| Service | systemd |
| Virtualization | VirtualBox |

---

## 📂 Directory Structure

```text
ssh-intrusion-detection-system/
│
├── app.py
├── blocked_ips.txt
├── requirements.txt
├── ssh-defense.service
├── README.md
└── venv/
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/EUNSEO78/ssh-intrusion-detection-system.git

cd ssh-intrusion-detection-system
```

### Create Virtual Environment

```bash
python3 -m venv venv
```

### Activate

```bash
source venv/bin/activate
```

### Install Packages

```bash
pip install -r requirements.txt
```

### Environment Variables

`.env`

```text
WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_URL
```

---

## ▶️ Run

### Execute

```bash
source venv/bin/activate
sudo venv/bin/python3 app.py
```

> **Note**
> UFW 제어를 위해 root 권한이 필요합니다.

또는

```bash
sudo systemctl daemon-reload
sudo systemctl enable ssh-defense
sudo systemctl start ssh-defense
sudo systemctl status ssh-defense
```

로그 확인

```bash
sudo journalctl -u ssh-defense -f
```

---

## 🧪 Security Testing

| Test | Result |
|------|--------|
| Brute Force Detection | ✅ |
| Auto Blocking | ✅ |
| Discord Notification | ✅ |
| Auto Unblocking | ✅ |
| Time Window Verification | ✅ |
| Service Restart | ✅ |
| Server Reboot | ✅ |

---

## 📸 Demo

### Brute Force Detection

![Brute Force Detection](brute-force-detection.png)

### UFW Auto Blocking

![UFW Auto Blocking](ufw-block.png)

### Discord Notification

![Discord Notification](discord-notification.png)

### Auto Unblocking

![Auto Unblocking](auto-unblock.png)

---

## 📚 Documentation

프로젝트의 전체 구현 과정 및 테스트는 아래 문서를 참고해주세요.


- 📖 Notion : [Notion Documentation](https://app.notion.com/p/SSH-Intrusion-Detection-Auto-Blocking-System-38824cb4abc680e593cfdecb07945927)

