import threading
import time
from datetime import datetime
from flask import Flask
import requests
import re
import yagmail
from waitress import serve
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
    #print(response.text)
    text = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:web=\"WebServices\"><soapenv:Body><web:RunWASSQL><web:SQLBlock>exec  spa_calcRate @send_agent_id='11000100',@payout_agent_id=NULL,@total_collected='1000000',@payment_type='Bank Account',@payout_country='Viet Nam',@payoutAmount=NULL,@currencyType='VND'</web:SQLBlock><web:CustomerID></web:CustomerID><web:Functionname>spa_calcRate</web:Functionname><web:Flag>h</web:Flag><web:Logxmlsno></web:Logxmlsno><web:Response></web:Response><web:Request></web:Request></web:RunWASSQL></soapenv:Body></soapenv:Envelope>--tr_end--serviceCharge--td_clm--3500--td_end--exchangeRate--td_clm--18.38910098--td_end--sendAmount--td_clm--1000000--td_end--receiveAmount--td_clm--18389100--td_end--receiveCType--td_clm--VND--td_end----tr_end--"

    match = re.search(r'receiveAmount--td_clm--(\d+)--td_end--', text)
    if match:
        receive_amount = match.group(1)
        return receive_amount
    else:
        return "Received Amount not found"

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

def background_task():
    while True:
        print("Running background task...")
        # Replace this with your actual task

        current_datetime = datetime.now()
        money_price = get_data_price()
        #print(f"{current_datetime}:   {money_price}")
        if int(money_price) > 18400000:
            email = yagmail.SMTP(user="donganhguk@gmail.com", password="wqcl gjqw bdfc umzf")


            email.send(to="guidetuanhp@gmail.com",
                       subject=f"Hello, Guide, {current_datetime}",
                       contents=f"Price is up. \n\n {get_data_price()}")
            print(f"Price is up : {money_price} \n  and {current_datetime}")
        else:
            print(f"Price is down : {money_price} \n Price is updating!!!! \n {current_datetime}")

        time.sleep(1800)


# Start the background task in a separate thread
background_thread = threading.Thread(target=background_task)
background_thread.daemon = True  # Daemonize the thread so it terminates with the main thread
background_thread.start()




if __name__ == "__main__":
    # from waitress import serve
    serve(app, host='0.0.0.0', port=8080)