import pandas as pd
from datetime import datetime, timedelta

#メンバーリストから取得してきた名簿
#とりあえず手動で辞書作成
member_dic = {
    "Monday":[["石川 裕人", "遠藤 空", "橋本 健", "山本 真也", "近藤 悠斗", "瀬川 絢翔"], ["高橋 風太", "西村 克己", "加藤 健吾", "川端 ももの", "三上 翔太", "越後谷 澪", "鈴木 友也"]],
    "Tuesday":[["加藤 健吾", "川端 ももの", "三上 翔太", "鈴木 友也", "筒井 優貴"], ["平尾 真斗", "山野 倖平", "田中 美帆", "石川 裕人", "宮本 港斗", "近藤 悠斗"], ["高橋 風太", "平尾 真斗", "大沢 恭平"]],
    "Wednesday":[["平尾 真斗", "西村 克己", "山野 倖平", "加藤 健吾", "田中 美帆", "川端 ももの", "近藤 悠斗"], ["大沢 恭平", "橋本 健", "瀬川 絢翔", "山本 真也", "筒井 優貴", "遠藤 空"]],
    "Thursday":[["高橋 風太", "石川 裕人", "三上 翔太", "橋本 健", "鈴木 友也", "遠藤 空"], ["山野 倖平", "西村 克己", "田中 美帆", "越後谷 澪", "宮本 港斗"]],
    "Friday":["大沢 恭平", "山本 真也", "越後谷 澪", "筒井 優貴", "宮本 港斗", "瀬川 絢翔"]
}

#割り当てられたアドレスを保持する辞書
address_dic = {
    "Monday":[],
    "Tuesday":[], 
    "Wednesday":[], 
    "Thursday":[],
    "Friday":[]
}

#曜日の入ったリスト
days_lst = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

data_lst = []

#ログデータのエクセルを読み込む関数
def excel_readr(file_path):
    #エクセルファイルを読み込む
    df = pd.read_excel(file_path)

    #データフレームの各行を1行ずつ処理する
    for row in df.itertuples(index=False, name=None):
        data_lst.append(row)

#アドレス等の計算を行う関数
def cul(lst):
    #8:50以降のデータのみの場合，リストが追加されてしまうことへのたいしょ
    append_first_flag = True

    for data in lst:
        #必要な情報の変数化

        #グリニッジ標準時刻から日本時刻へ変換
        '''
        date_greenwich= datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%S.%f")
        jst_offset = timedelta(hours=9)
        date_time = date_greenwich + jst_offset
        '''
        date_time = datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%S.%f")
        log_time = date_time.strftime("%H:%M:%S")
        weekday = date_time.strftime("%A")
        ip_address = data[1]
        mac_address = data[2]
        host_name = data[3]
        
        
        #一限からいて2限に授業ある場合は最初に割り当てられたアドレスにflagをつけておいて，removeがあったら削除するようにするはどう？

        if log_time < "08:50:00.00":
        #log_time < "10:45:00.00":

            if len(address_dic[weekday]) == 0:
                #print(f"macaddressの型: {type(mac_address)}")
                address_dic[weekday].append([mac_address])
                append_first_flag = False
            else:
                #print(f"log_time: {log_time}, date_time: {date_time}")
                address_dic[weekday][0].append(mac_address)

        #elif log_time > "08:50:00.00" and log_time < "10:45:00.00"
        else:
            #print(f"member_dic: {weekday}")
            if len(address_dic[weekday]) < len(member_dic[weekday]):
                address_dic[weekday].append([mac_address])
            else:
                address_dic[weekday][1].append(mac_address)
    print(address_dic)


#月曜日1限と火曜日1限のように比較する
def loop_compare():
    global days_lst
    for i in range(len(address_dic)):
        address_dic[days_lst[i]]

if __name__ == "__main__":
    excel_path = "/home/sora/basic_ex/outputs/jun_week2.xlsx"

    excel_readr(excel_path)

    cul(data_lst)

    #print("-------------")
    #print(f"水曜: {address_dic['Wednesday']}")
    #print("-------------")
    #print(f"木曜: {address_dic['Thursday']}")
    print("#############")

    count = 0
    duple_address = []
    for address in address_dic["Tuesday"][1]:
        if address in address_dic["Friday"][0]:
            #print(f"一致したaddress: {address}")
            if address not in duple_address:
                duple_address.append(address)
                count +=1
    
    #print(f"火曜1限と木曜2限")
    #print(f"count: {count}")
    #print(duple_address)
    #print(f"len_address_dic: {len(address_dic)})")

    #if address_dic["月"] == []:
    #    print("a")
    #else:
    #    print(address_dic["月"])
    #    print("b")
    