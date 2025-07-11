# 🔧 Step 1: Setup SSH Server & ngrok
!apt -qq update
!apt -qq install openssh-server curl > /dev/null
!wget -q -O ngrok.zip https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
!unzip -qq -o ngrok.zip && mv ngrok /usr/local/bin && chmod +x /usr/local/bin/ngrok

# 🔐 Step 2: Konfigurasi User SSH
import getpass, os, time, json, urllib.request

PASSWORD = "123456"  # Ganti jika ingin password lain
os.system(f"echo root:{PASSWORD} | chpasswd")
os.system("mkdir -p /var/run/sshd")
os.system("echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config")
os.system("echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config")
os.system("echo 'Port 22' >> /etc/ssh/sshd_config")
os.system("service ssh restart")

# 🔗 Step 3: Jalankan ngrok TCP Tunnel
NGROK_TOKEN = "2zhgCmr6rMkwxMUfpJGW9JbBmCE_54iTeCP7BPYY8tNreDHshf"  # Token kamu
os.system(f"ngrok authtoken {NGROK_TOKEN}")
get_ipython().system_raw("ngrok tcp 22 &")

# ⏱️ Step 4: Retry ambil URL sampai berhasil
def get_ssh_url(timeout=20):
    for i in range(timeout):
        try:
            time.sleep(2)
            data = json.load(urllib.request.urlopen("http://localhost:4040/api/tunnels"))
            for t in data["tunnels"]:
                if t["proto"] == "tcp":
                    return t["public_url"].replace("tcp://", "")
        except:
            pass
    return None

url = get_ssh_url()

# ✅ Step 5: Output Final
if url:
    host, port = url.split(":")
    print("🎯 SSH Server Aktif via ngrok!")
    print(f"🔗 Command : ssh root@{host} -p {port}")
    print(f"🔐 Password: {PASSWORD}")
else:
    print("❌ Gagal mendapatkan alamat ngrok meski sudah mencoba maksimal.")
    print("📋 Cek ulang token ngrok, runtime, atau jaringan Colab.")
