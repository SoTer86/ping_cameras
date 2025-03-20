import pandas as pd

df = pd.read_excel('cameras.xlsx', sheet_name='Данные')
lines_ip = df['ip'].to_list()
lines_address = df['address'].to_list()
lines_names_cams = df['name'].to_list()
ips = dict(zip(lines_ip, lines_address))


print(ips)