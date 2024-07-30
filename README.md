# device_owner_identification

## 手順
1. new_log_putput.pyでDDNS•DHCPサーバログからADDされたIPアドレス、MACアドレスとその時刻を取得し、xlsx形式で保存する
2. ログが複数ある場合、sort.pyでログを昇順にして再度xlsx形式で保存する
3. 上で作成したxlsxファイルと各自の学生名簿を用意し、identify.pyを実行する

上記の手順により、各曜日の授業ごとに共通しているMACアドレスを取得できる

identify.pyを実行した結果は以下である．

![image](https://github.com/user-attachments/assets/e4df5c61-d4c2-4bf3-9b9e-5def4e6427b8)

