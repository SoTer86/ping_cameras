# import os
import pandas as pd
# from subprocess import PIPE, Popen
# from datetime import date


def read_file(filename : str) -> list:
    """чтение ip-адресов из excel-файла"""
    dvn = 0
    mmpl = -26 # минус камеры г. Югорск
    kt = 0
    vshs = 0
    vdcc = 0
    vdos = 0

    df = pd.read_excel(filename, sheet_name='Данные')
    lines = df['cameraType'].to_list()
    for line in lines:
        line_strip = str(line).strip()
        if line_strip == 'ДВН': dvn += 1
        if line_strip == 'ММПЛ': mmpl += 1
        if line_strip == 'КТ': kt += 1
        if line_strip == 'ВШС': vshs += 1
        if line_strip == 'ВДСС': vdcc += 1
        if line_strip == 'ВДОС': vdos += 1
    
    print(df.head())

    print(f"\nДВН (дворовое) = {dvn}")
    print(f"ММПЛ (места.мас.скоп.людей) = {mmpl}")
    print(f"КТ (котельные) = {kt}")
    print(f"ВШС (школы) = {vshs}")
    print(f"ВДСС (сады) = {vdcc}")
    print(f"ВДОС (доп.обр.) = {vdos}")
    print(f"\nВсего: {dvn+mmpl+kt+vshs+vdcc+vdos}")
            
    


def ping_run():
    """Основной модуль"""
    read_file('cameras.xlsx')


if __name__ == "__main__":
    ping_run()