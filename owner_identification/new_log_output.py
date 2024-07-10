import re
import time
import openpyxl
from datetime import datetime

# グローバル変数
message_lst = []
log_time = ""
data = [
        ['日付', 'IPアドレス', 'MACアドレス', 'ホスト名']
    ]

# エクセルファイルへ保存する情報をDDNSのログ文から生成する
def generate_message(line):
    global log_time, message_lst

    # DHCPのログファイルのパス
    dhcp_log_file = "/home/sora/new_logs/6_20/core-s2/dhcp.log"
    # 対象外のホスト名リスト
    not_name_lst = [
        "c0a2", "ubuntu-server", "mpy-esp32", "test-sora", "prometheus", "kawatake", "elk-system", "elastic"
    ]
    
    # if "100.162" in line:
    #     print(f"原文: {line}")

    # DNSへの追加が成功していたらそのログの日時を小数点第2位まで取得する
    if "DHCP_DDNS_ADD_SUCCEEDED" in line:
        log_time = re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{2}', line).group()
        message_lst.append(log_time)

    # 取得した日時と同じで，FQDNがあれば
    elif "FQDN:" in line and log_time in message_lst:
        fqdn = re.search(r'FQDN: \[(.*?)\.\]', line).group(1)
        message = re.search(r'^[^.]+', fqdn).group()

        # 対象外のホスト名でないか
        out_flag = False
        for not_name in not_name_lst:
            if not_name in message:
                out_flag = True
                break
        if out_flag:
            message_lst = []
            out_flag = False
        else:
            message_lst.append(message)

    # 取得した日時と同じで，IP Addressがあれば
    elif "Address:" in line and log_time in message_lst:
        message = re.search(r'IP Address: \[(.*?)\]', line).group(1)
        message_lst.append(message)

    # 日時，IPアドレス，FQDNが追加されていれば
    if len(message_lst) >= 3:
        # dataに追加
        time_stamp = message_lst[0]
        host_name = re.search(r'^[^.]+', message_lst[1]).group()
        ip_address = message_lst[2]
        mac_address = generate_mac_address(dhcp_log_file, ip_address)

        # データ(日付，IPアドレス，MACアドレス，ホスト名)を追加
        data.append([time_stamp, ip_address, mac_address, host_name])
        message_lst = []

        if time_stamp == "2024-06-20T15:27:54.32":
            print(f"状況  time: {time_stamp}, ip: {ip_address}, mac: {mac_address}, hostname: {host_name}, ")

# macアドレスを取得するために
def generate_mac_address(file_path, ddns_ip):
    with open(file_path, "r") as f:
        for line in f:
            if "DHCP4_LEASE_ALLOC" not in line:
                continue

            dhcp_log_time = re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{5}', line).group()
            dhcp_dt_time = datetime.strptime(dhcp_log_time, "%Y-%m-%dT%H:%M:%S.%f")
            log_dt_time = datetime.strptime(log_time, "%Y-%m-%dT%H:%M:%S.%f")
            ip_address = re.search(r'lease ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line).group(1)

            if (log_dt_time - dhcp_dt_time).total_seconds() <= 0.4 and (ip_address == ddns_ip):
                mac_address = re.search(r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', line).group()
                #print(f"macaddress:{mac_address}, ddns_ip: {ddns_ip}, dhcp_log_time: {dhcp_log_time}, log_time: {log_time}")
                return mac_address

# Excelへデータを保存する関数
def save_xlsx(data_lst):
    # 保存したいExcelファイルのパス
    excel_path = "/home/sora/basic_ex/outputs/jun_20-core-s2.xlsx"
    # 新しいワークブックを作成
    wb = openpyxl.Workbook()
    # アクティブなワークシートを取得
    ws = wb.active

    for row in data:
        print(f"row:{row}")
        ws.append(row)

    # Excel ファイルを保存
    wb.save(excel_path)

if __name__ == "__main__":
    log_path = "/home/sora/new_logs/6_20/core-s2/ddns.log"

    # ログファイルを1行ずつ読み込む
    with open(log_path) as fobj:
        for line in fobj:
            line_log_time = re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{2}', line).group()

            if line_log_time >= log_time:
                generate_message(line)

    # Excelファイルへ出力
    save_xlsx(data)
