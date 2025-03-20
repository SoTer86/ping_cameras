import pandas as pd

from datetime import date
from pathlib import Path
from subprocess import PIPE, Popen


NUM : int = 1
WAIT : int = 1000
host : str = "google.com"
STATUS_ON : str = "OK"
STATUS_OFF : str = "FAIL"

total : int = 0
total_ok : int = 0
total_fail : int = 0

result_file_name = f"fail{date.today()}.log"


def excel_to_ips(filename : str) -> dict:
    """чтение ip-адресов из excel-файла"""
    ips, address = [], []
    df = pd.read_excel(filename, sheet_name='Данные', engine='openpyxl')
    lines_ips = df['ip'].to_list()
    lines_address = df['address'].to_list()
    
    for i, ip in enumerate(lines_ips):
        ip_strip = str(ip).strip()
        if ip_strip not in ips and '.' in ip_strip:
            ips.append(str(ip).strip())
            address.append(lines_address[i])
            
    return dict(zip(ips, address))


def init_write_file(filename : str):
    with open(filename,'w') as f:
        pass


def write_file_line(filename : str, data) -> None:
    """Запись данных в файл"""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{data}\n")
          

def ping_one(ip_address : str) -> str:
    """проверка доступности ip-адреса и подсчет кол-ва адресов"""
    ping = Popen(f"ping -n 1 -w 1000 {ip_address}", stdout=PIPE, stderr=PIPE)
    exit_code = ping.wait()
    global total
    global total_ok
    global total_fail
    total += 1
    if exit_code != 0:
        total_fail += 1
    else:
        total_ok += 1
    return STATUS_OFF if exit_code != 0 else STATUS_ON


def ping_all(ip_address : dict) -> list:
    """проверка доступности ip-адресов."""
    for i, ip in enumerate(ip_address.keys()):
        global total_fail
        ping_status = ping_one(ip)
        print(f"[{i + 1}] {ip} - {ping_status} - {ip_address[ip]}")    
        if ping_status == STATUS_OFF:
            write_file_line(
                result_file_name, 
                f"[{total_fail}] {ip} - {ping_status} {ip_address[ip]}"
            )  


def ping_run() -> None:
    """Основной модуль"""
    filename = 'cameras.xlsx'
    file = Path(filename)
    if not file.exists():
        print('Файл с таблицей не существует.')
        input()
        exit(1)
    init_write_file(result_file_name)
    ip_addresses = excel_to_ips(filename)
    ping_all(ip_addresses)
    print(f"\nTOTAL: {total}\nOK: {total_ok}\nFAIL: {total_fail}")
    input()


if __name__ == "__main__":
    ping_run()