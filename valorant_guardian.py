import psutil
import time
import tkinter as tk
from tkinter import messagebox
import threading
import os
import sys
import shutil
import winreg

# ==============================
# ユーザーに警告ポップアップを表示
# ==============================
def show_popup():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning(
        "VALORANTブロック発動",
        "VALORANTまたはRiotのプロセスを検出。\n強制終了しました。\nまた3時間溶けるところでした。"
    )
    root.destroy()

# ==============================
# スタートアップ登録処理
# ==============================
def add_to_startup():
    file_path = os.path.realpath(sys.argv[0])
    app_name = "ValorantGuardian"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Run",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(key)

# ==============================
# プロセス監視と強制終了
# ==============================
def monitor_and_kill():
    while True:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name']
                if name and ('riot' in name.lower() or 'valorant' in name.lower()):
                    # 強制終了
                    proc.kill()
                    # 警告表示（別スレッド）
                    threading.Thread(target=show_popup).start()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        time.sleep(5)

# ==============================
# 実行開始
# ==============================
if __name__ == "__main__":
    add_to_startup()  # 自動起動に登録（初回のみでもOK）
    monitor_and_kill()
