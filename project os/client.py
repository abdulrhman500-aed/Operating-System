import socket
import re

def is_valid_ip(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(part) <= 255 for part in ip.split("."))

def is_valid_port(port):
    return 1024 <= port <= 65535

while True:
    HOST = input("Enter Server IP: ")
    if is_valid_ip(HOST):
        break
    print("❌ Invalid IP")

while True:
    try:
        PORT = int(input("Enter Server Port (1024-65535): "))
        if is_valid_port(PORT):
            break
        print("❌ Invalid Port range")
    except:
        print("❌ Port must be numeric")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect((HOST, PORT))

username = input("Enter your username: ")
client.send(username.encode())

print("Connected to server. Type 'bye' to exit.")

while True:
    message = input(f"{username}: ")
    client.send(message.encode())

    reply = client.recv(1024).decode()  # يجيب الرد
    print("Bot:", reply)  

    if message.lower() == "bye":
        break

client.close()
 
'''
      الفكرة و التشغيل 
      
       ip 127. . . or 0.0.0.0
       any port
       
          client  السرفر  هو اللي هكتبه في ال ip 
          لكن البورت يتغير عادي
          
      بعرف ع السيرفر ip  port 
       بعدين بروح لل client 
       وادخل ال ip  port 
       بعدين ببعت الرسالة ثم يجي الرد
'''