import socket  #توصل بالسرفر
import threading
import tkinter as tk  #مكتبة واجهة
from tkinter import messagebox # تطلع حاجة زي تنبيه ان محصلش اتصال
import re

# ================= Validation =================
def is_valid_ip(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(part) <= 255 for part in ip.split("."))

def is_valid_port(port):
    return 1024 <= port <= 65535

# ================= Client GUI =================
class ChatClientGUI:     # نبدا ننظم الكود
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot Client")  #عنوان الوااجهة 
        self.root.geometry("500x500")   # حجم الواجهة

        self.client = None 

        self.build_login_ui()  # نبدا نسخل و ندخل ال client

    # ---------- Login Screen ----------
    def build_login_ui(self): # اول واجهة   التسجيل
        self.clear_screen()

        tk.Label(self.root, text="Chatbot Login", font=("Arial", 16)).pack(pady=10) # الاماكن اللي هكتب فيه

        tk.Label(self.root, text="Server IP").pack()  # لادخال ip
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack()

        tk.Label(self.root, text="Port").pack()  # port 
        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()

        tk.Label(self.root, text="Username").pack() # الاسم
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Button(self.root, text="Connect", command=self.connect).pack(pady=10) # زارا الاتصال

    # ---------- Chat Screen ----------
    def build_chat_ui(self):
        self.clear_screen()

        self.chat_area = tk.Text(self.root, state="disabled")
        self.chat_area.pack(padx=10, pady=10, expand=True, fill="both")

        self.msg_entry = tk.Entry(self.root)  #للمربع اللي هكتب فيه الرسالة
        self.msg_entry.pack(padx=10, pady=5, fill="x")
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        tk.Button(self.root, text="Send", command=self.send_message).pack(pady=5) # زارا بعت الرسالة

    def clear_screen(self):  # يمسح القديم
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------- Connection ----------
    def connect(self):  #توصل بالسرفر
        ip = self.ip_entry.get()    #يقرا الداتا اللي مدخلها
        port = self.port_entry.get()
        username = self.username_entry.get()

        if not is_valid_ip(ip):
            messagebox.showerror("Error", "Invalid IP address")
            return

        try:
            port = int(port)
            if not is_valid_port(port):
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid Port")
            return

        if username.strip() == "":
            messagebox.showerror("Error", "Username required")
            return

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((ip, port))
            self.client.send(username.encode())
        except:
            messagebox.showerror("Error", "Connection failed")
            return

        self.username = username
        self.build_chat_ui()

        threading.Thread(target=self.receive_messages, daemon=True).start() #   بدء الثريد

    # ---------- Messaging ----------
    def send_message(self):
        message = self.msg_entry.get()
        if message == "":
            return

        self.client.send(message.encode())
        self.display_message(f"You: {message}")
        self.msg_entry.delete(0, tk.END)

        if message.lower() == "bye":
            self.client.close()
            self.root.quit()

    def receive_messages(self):
        while True:
            try:
                reply = self.client.recv(1024).decode()
                if not reply:
                    break
                self.display_message(f"Bot: {reply}")
            except:
                break

    def display_message(self, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)

# ================= Run App =================
root = tk.Tk()
app = ChatClientGUI(root)
root.mainloop()
