#!/bin/bash

echo "🔧 Menyiapkan SSH Server & ngrok..."

# 1. Install jika belum
sudo apt update -y && sudo apt install -y openssh-server curl unzip > /dev/null

# 2. Atur password root
echo "root:123456" | sudo chpasswd
echo "PasswordAuthentication yes" | sudo tee -a /etc/ssh/sshd_config > /dev/null
sudo mkdir -p /var/run/sshd
sudo systemctl restart ssh

# 3. Jalankan ngrok (jika belum ada)
if ! command -v ngrok &> /dev/null; then
  curl -s -o ngrok.zip https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
  unzip -o ngrok.zip
  sudo mv ngrok /usr/local/bin
  chmod +x /usr/local/bin/ngrok
fi

# 4. Autentikasi dan jalankan tunnel
ngrok config add-authtoken 2zhgCmr6rMkwxMUfpJGW9JbBmCE_54iTeCP7BPY8tNreDHshf
pkill ngrok
nohup ngrok tcp 22 > ngrok.log &

# 5. Tunggu dan ambil URL
echo "⏳ Menunggu tunnel aktif..."
sleep 10
SSH_URL=$(grep -o 'tcp://[0-9A-Za-z.:]*' ngrok.log | head -n 1)

if [[ -n "$SSH_URL" ]]; then
  HOST=$(echo $SSH_URL | cut -d'/' -f3 | cut -d':' -f1)
  PORT=$(echo $SSH_URL | cut -d':' -f3)
  echo -e "\n✅ SSH Siap Dipakai!"
  echo "📡 ssh root@$HOST -p $PORT"
  echo "🔐 Password: 123456"
else
  echo "❌ Gagal mendapatkan URL ngrok. Coba jalankan ulang."
fi
