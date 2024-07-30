import pandas as pd
from datetime import datetime, timedelta

# メンバーリストから取得してきた名簿
member_dic = {
    "Monday": [[""], [""]],
    "Tuesday": [[""], [""], [""]],
    "Wednesday": [[""], [""]],
    "Thursday": [[""], [""]],
    "Friday": [[""]]
}

# 割り当てられたアドレスを保持する辞書
address_dic = {
    "Monday": [[], []],
    "Tuesday": [[], [], []],
    "Wednesday": [[], []],
    "Thursday": [[], []],
    "Friday": [[]]
}

# 削除するMACアドレスを識別するための辞書
ip_dic = {}

# 曜日の入ったリスト
days_lst = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

data_lst = []

# ログデータのエクセルを読み込む関数
def excel_readr(file_path):
    # エクセルファイルを読み込む
    df = pd.read_excel(file_path)

    # データフレームの各行を1行ずつ処理する
    for row in df.itertuples(index=False, name=None):
        data_lst.append(row)

# アドレス等の計算を行う関数
def cul(lst):
    for data in lst:
        # 必要な情報の変数化

        date_time = datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%S.%f")
        log_time = date_time.strftime("%H:%M:%S")
        weekday = date_time.strftime("%A")
        dns_mapping = data[1]
        ip_address = data[2]
        mac_address = data[3]
        host_name = data[4]

        if int(date_time.strftime("%d")) < 11 or host_name == "unikube":
            continue

        #DNSレコードを追加していれば
        if dns_mapping == "add":
            #1限開前のログであれば
            if log_time < "08:50:00.00":
                for i in range(len(address_dic[weekday])):
                    if mac_address not in address_dic[weekday][i]:
                        address_dic[weekday][i].append(mac_address)
            elif "08:50:00.00" <= log_time < "10:45:00.00":
                for i in range(1, len(address_dic[weekday])):
                    if mac_address not in address_dic[weekday][i]:
                        address_dic[weekday][i].append(mac_address)
            elif "10:45:00.00" <= log_time < "13:15:00.00" and len(address_dic[weekday]) == 3:
                if mac_address not in address_dic[weekday][2]:
                    address_dic[weekday][2].append(mac_address)
            ip_dic[ip_address] = mac_address
        elif dns_mapping == "remove":
            try:
                if log_time < "08:50:00.00":
                    for i in range(len(address_dic[weekday])):
                        address_dic[weekday][i].remove(ip_dic[ip_address])
                elif "08:50:00.00" <= log_time < "10:45:00.00":
                    for i in range(1, len(address_dic[weekday])):
                        address_dic[weekday][i].remove(ip_dic[ip_address])
                elif "10:45:00.00" <= log_time < "13:15:00.00" and len(address_dic[weekday]) == 3:
                    address_dic[weekday][2].remove(ip_dic[ip_address])
            except ValueError:
                print(f"MAC address {ip_dic[ip_address]} not found in list.")

    print(address_dic)

# 月曜日1限と火曜日1限のように比較する
def loop_compare():
    global days_lst
    for i in range(len(address_dic)):
        address_dic[days_lst[i]]

if __name__ == "__main__":
    excel_path = "/home/sora/basic_ex/outputs_ver2/jun_week.xlsx"

    excel_readr(excel_path)

    cul(data_lst)

    print("#############")

    count = 0
    duple_address = []
    for address in address_dic["Tuesday"][0]:
        if address in address_dic["Friday"][0]:
            if address not in duple_address:
                duple_address.append(address)
                count += 1

    print("火曜1限と木曜1限")
    print(f"count: {count}")
    print(duple_address)
