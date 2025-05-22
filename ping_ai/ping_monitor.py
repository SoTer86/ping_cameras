from flask import Flask, render_template
import subprocess
import threading
import time
from datetime import datetime

from modulesip import excel_to_ips

app = Flask(__name__)

# Конфигурация
PING_INTERVAL = 300  # Интервал пинга в секундах

ip_data = excel_to_ips("cameras.xlsx")
IP_LIST = list(ip_data.keys())

# Глобальный словарь для хранения статусов
status_data = {
    "last_update": "Не обновлялось",
    "hosts": {},
    "descriptions": ip_data,
    "online_count": 0,
    "offline_count": 0,
    "total_count": len(IP_LIST)
}

def ping_host(ip):
    """Пингует хост и возвращает True, если доступен"""
    try:
        output = subprocess.check_output(["ping", "-n", "1", "-w", "1000", ip], 
                                      stderr=subprocess.STDOUT,
                                      universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False

def update_statuses():
    """Обновляет статусы всех хостов"""
    while True:
        online = 0
        offline = 0
        
        for ip in IP_LIST:
            status = ping_host(ip)
            status_data["hosts"][ip] = status
            if status:
                online += 1
            else:
                offline += 1
        
        status_data["online_count"] = online
        status_data["offline_count"] = offline
        status_data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(PING_INTERVAL)

@app.route('/')
def status_page():
    """Главная страница с отображением статусов"""
    return render_template('status2.html', 
                         hosts=status_data["hosts"], 
                         descriptions=status_data["descriptions"],
                         last_update=status_data["last_update"],
                         online_count=status_data["online_count"],
                         offline_count=status_data["offline_count"],
                         total_count=status_data["total_count"])

if __name__ == '__main__':
    # Запускаем фоновый поток для обновления статусов
    updater_thread = threading.Thread(target=update_statuses)
    updater_thread.daemon = True
    updater_thread.start()
    
    # Запускаем веб-сервер
    app.run(host='0.0.0.0', port=5000)