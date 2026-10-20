import socket
import threading
import random  
import re   # True Input 
import datetime

# ===================== RULES =====================
responses = {
    # Greetings
    "hello": ["Hello!", "Hi 👋", "Hey!", "Hello there 😊"],
    "hi": ["Hi!", "Hey!", "Hello!"],
    "good morning": ["Good morning ☀️", "Morning! Have a nice day"],
    "good evening": ["Good evening 🌙", "Hope your evening is great"],
    "good night": ["Good night 😴", "Sweet dreams"],

    # Personal
    "how are you": ["I'm fine 😊", "Doing great!", "All good, thanks"],
    "your name": ["I'm a chatbot 🤖", "You can call me AI Bot"],
    "who are you": ["I'm a rule-based chatbot", "I'm here to help you"],
    "what can you do": [
        "I can chat with you",
        "I can answer questions",
        "I can help with programming and study"
    ],

    # Feelings
    "i am sad": ["I'm sorry to hear that 😔", "Everything will be okay ❤️"],
    "i am happy": ["That's great 😄", "I'm happy for you!"],
    "i am tired": ["Take some rest 😴", "You deserve a break"],
    "i am bored": ["Let's talk 😄", "Try learning something new"],

    # Study
    "study": ["Studying helps your future", "Study a little every day"],
    "exam": ["Good luck in your exam 🍀", "Stay calm and confident"],
    "project": ["Projects build real skills", "Work step by step"],

    # Programming
    "programming": ["Programming solves problems", "Programming needs logic"],
    "python": ["Python is easy and powerful", "Python is great for AI"],
    "c++": ["C++ is fast and powerful", "C++ is used in systems"],
    "java": ["Java is platform independent"],

    # Networking
    "socket": ["Sockets connect client and server"],
    "tcp": ["TCP is reliable and connection-oriented"],
    "udp": ["UDP is fast but unreliable"],
    "ip": ["IP identifies devices on a network"],

    # General
    "help": [
        "You can ask about programming, study, networking, time, date",
        "Try asking me something 😊"
    ],
    "joke": [
        "Why do programmers hate nature? Too many bugs 😂",
        "Why was the computer cold? It forgot to close Windows 😂"
    ],
    "weather": [
        "I can't check live weather, but I hope it's nice ☀️",
        "Weather depends on your location 🌍"
    ],

    # Thanks & Bye
    "thank": ["You're welcome 😊", "No problem!", "Anytime 👍"],
    "thanks": ["Glad to help!", "You're welcome 😄"],
    "bye": ["Goodbye 👋", "See you later!", "Take care ❤️"],
    "exit": ["Bye 👋", "Hope to see you again"]
} 
# Emotions ----> win + .

# ===================== FUNCTIONS =====================
def chatbot_response(message):
    message = message.lower() # عشان لو دخل حرف كابيتال

    # Time
    if "time" in message:
        return "Current time: " + datetime.datetime.now().strftime("%H:%M:%S")

    # Date
    if "date" in message or "day" in message:
        return "Today's date: " + datetime.datetime.now().strftime("%Y-%m-%d")

    for key in responses:
        if key in message:
            return random.choice(responses[key])

    return random.choice([     # لو قال حاجة غير اللي موجودة في rules
        "Sorry, I didn't understand that 🤔",
        "Can you explain more?",
        "I'm still learning, try something else 😊"
    ])

def is_valid_ip(ip):  # عشان يشوف ip  ويدخله صح
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(part) <= 255 for part in ip.split("."))

def is_valid_port(port):  #port 1024 : 65535
    return 1024 <= port <= 65535

def handle_client(client_socket, client_address):   # يعمل connect   بتشتغل مع كل Client لوحده
    print(f"[NEW CONNECTION] {client_address} connected.")

    username = client_socket.recv(1024).decode()    #بتتنفذ داخل Thread   استقبال اسم المستخدم
    print(f"[USERNAME] {username} joined")

    while True:
        try:
            message = client_socket.recv(1024).decode()  #استقبال الرسائل   إرسال رد البوت  إنهاء الاتصال
            if not message: #لو فاضية 
                break

            print(f"[{username}] {message}")
            reply = chatbot_response(message)  #إرسال الرد
            client_socket.send(reply.encode())

            if message.lower() == "bye":
                break
        except:
            break

    print(f"[DISCONNECTED] {username}")
    client_socket.close()

# ===================== SERVER SETUP =====================
while True:
    HOST = input("Enter IP to bind (e.g. 127.0.0.1 or 0.0.0.0): ")  
    if is_valid_ip(HOST) or HOST == "0.0.0.0":   #dafult
        break
    print("❌ Invalid IP")

while True:
    try:
        PORT = int(input("Enter Port (1024-65535): "))
        if is_valid_port(PORT):
            break
        print("❌ Invalid Port range")
    except:
        print("❌ Port must be a number")

server = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)  #create server  استخدام IPv4   بروتوكول TCP
server.bind((HOST, PORT)) #ربط السيرفر بالـ IP و Port
server.listen()

print(f"[SERVER RUNNING] Listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server.accept()  #Thread جديد
    threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    ).start()
 #يستخدم السيرفر Socket Programming مع Multi-Threading
#حيث يتم إنشاء Thread مستقل لكل Client
#مما يسمح بالتعامل مع عدة مستخدمين في نفس الوقت