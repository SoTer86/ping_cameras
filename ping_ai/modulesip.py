import pandas as pd

def excel_to_ips(filename : str) -> dict:
    """read ip-addresses in excel-file"""
    ips, address = [], []
    df = pd.read_excel(filename, sheet_name='Данные', engine='openpyxl')
    lines_ips = df['ip'].to_list()
    lines_name = df['name'].to_list()
    lines_address = df['address'].to_list()
    
    for i, ip in enumerate(lines_ips):
        ip_strip = str(ip).strip()
        if ip_strip not in ips and '.' in ip_strip:
            ips.append(ip_strip)
            address.append(f"{lines_address[i]} ({lines_name[i]})")
    
    di = zip(ips, address)
            
    return dict(sorted(di))