# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from binance.client import Client
import math
import os
from datetime import datetime
import schedule
import time

class main:
    
    def __init__(self):
        api_key = 'APIK_KEY'
        api_secret = 'API_SECRET'
        self.client = Client(api_key, api_secret)
        
        self.buy_pow_usd = 11 #per coin/usd
        self.coin_list = ['BTCUSDT','ETHUSDT','BNBUSDT','ADAUSDT','LINKUSDT','RENUSDT']
        
    def startLog(self):
        try:
            logFolder = os.getcwd() + '\\log\\'
            if not os.path.exists(os.path.dirname(logFolder)):
                os.makedirs(os.path.dirname(logFolder)) 
            firstLog = os.listdir(logFolder)
            if not firstLog:
                logPath = logFolder + 'log_' + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.txt'  
                self.wf = open(logPath,"w+") 
            else:
                logPath = logFolder + firstLog[0]
                self.wf = open(logPath,"a")    
        except Exception as e:
            self.writeInLog('Exception in function startLog' + + str(e))
    
    def writeInLog(self,text):
        try:
            self.wf.writelines(text + '\n')
        except Exception as e:
            self.writeInLog('Exception in function writeInLog: ' + str(e))
            
    def closeLog(self):
        try:
            self.wf.close()         
        except Exception as e:
            self.writeInLog('Exception in function closeLog: ' + str(e)) 
            
    def run(self):
        self.startLog()
        self.writeInLog(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        try:
            for i in self.coin_list:
                coin_price = self.client.get_symbol_ticker(symbol=i)
                
                #get order details and precision for coin
                info = self.client.get_symbol_info(i)
                step_size = float(info['filters'][2]['stepSize'])    
                precision = int(round(-math.log(step_size, 10), 0))
            
                #amount to buy vs minimum amount allowed on binance for purchase
                amt_to_buy = round(self.buy_pow_usd/float(coin_price['price']),precision)   
                min_order = round(float(info['filters'][2]['minQty']),precision)
                
                self.writeInLog(i)
                
                #reassign amount to buy if it is below minimum allowed for an order
                if amt_to_buy <= min_order:
                    amt_to_buy = min_order
                    
                #make the purchase
                order = self.client.order_market_buy(symbol=i, quantity=amt_to_buy)
                self.writeInLog(str(order))
        except Exception as e:
            self.writeInLog('Exception in function run: ' + str(e))             
        self.closeLog()
        print(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        
    def job(self):
        #self.run()
        print("I'm running...")
        schedule.every().day.at("06:00").do(self.run)
        while True:
            schedule.run_pending()
            time.sleep(1)   
        
if __name__ == "__main__":
    new_main = main()
    new_main.job()
