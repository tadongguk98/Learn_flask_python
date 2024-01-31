import requests
import re
import yagmail
from datetime import datetime

def get_data_price():
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7",
        "Content-Length": "0",
        "Dnt": "1",
        "Origin": "https://mapi.gmoneytrans.net",
        "Referer": "https://mapi.gmoneytrans.net/exratenew1/Default.asp?country=viet%20nam",
        "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    payload = {
        "receive_amount": "",  # Fill in the actual value
        "payout_country": "Viet Nam",
        "total_collected": "1000000",
        "payment_type": "Bank Account",
        "currencyType": "VND"
    }
    response = requests.post("https://mapi.gmoneytrans.net/exratenew1/ajx_calcRate.asp?receive_amount=&payout_country=Viet%20Nam&total_collected=1000000&payment_type=Bank%20Account&currencyType=VND",
                             headers= headers,
                             data = payload,
                             verify=False
                             )
    text = response.text
    match = re.search(r'receiveAmount--td_clm--(\d+)--td_end--', text)
    if match:
        receive_amount = match.group(1)
        return receive_amount
    else:
        return "Received Amount not found"
money_price = get_data_price()

current_datetime = datetime.now()
#print(f"{current_datetime}:   {money_price}")
if int(money_price) < 18400000:
    email = yagmail.SMTP(user="donganhguk@gmail.com", password="wqcl gjqw bdfc umzf")


    email.send(to="guidetuanhp@gmail.com",
               subject=f"Hello, Guide, {current_datetime}",
               contents=f"Price is up. \n\n {money_price}")
    print(f"Price is up : {money_price} \n  and {current_datetime}")
else:
    print(f"Price is down : {money_price} \n Price is updating!!!! \n {current_datetime}")