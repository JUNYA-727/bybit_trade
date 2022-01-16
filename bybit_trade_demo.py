import bybit
import time
import datetime

#API情報の取得(自身で作成したAPIとAPI_secret_keyを入力する)
client=bybit.bybit(test=True,api_key='******',api_secret='******')
cnt=0

#どれくらいの頻度で売買を行うか(秒)
interval=900

#エントリーしていないときは0､買いで保有しているときは1､売りで保有しているときは2
have=0

price_data=[]
entry_price=0
'''
今回は簡単なデモトレードを行うので､機械学習を使わないかなりシンプルなものにする｡
-アルゴリズム概要-
前の価格が現在の価格に対し±20USDの際に買いか売りの売買を行う｡
利益が購入した価格に対して±40USDの際に取引を終了する
'''
while True:
    now_time=(datetime.datetime.utcnow()+datetime.timedelta(hours=9))
    time_data=time.strftime('%Y-%m-%d-%H-%M-%S')
    price=float(client.Market.Market_symbolInfo(symbol="BTCUSD").result()[0]['result'][0]['last_price'])
    price_data.append(price)
    if cnt==0:
        print('自動売買を開始します')
        print('売買を行う間隔は'+str(int(interval)/60)+'分です｡')
    if cnt>0:
        if (100<cnt) and (have==0):
            print('自動売買を終了します')
            break

        old_price=price_data[-2]
        now_price=price_data[-1]
        if have==0:
            if now_price-old_price<-20:
                client.Order.Order_new(side="Sell",symbol="BTCUSD",order_type="Market",qty=10000,time_in_force="GoodTillCancel").result()
                entry_prce=now_price
                have=2
            if now_price-old_price>20:
                client.Order.Order_new(side="Buy",symbol="BTCUSD",order_type="Market",qty=10000,time_in_force="GoodTillCancel").result()
                entry_price=now_price
                have=1
        if have==1:
            if now_price-entry_prce>40:
                client.Order.Order_new(side="Sell",symbol="BTCUSD",order_type="Market",qty=10000,time_in_force="GoodTillCancel").result()
                have=0
                print('損益は'+str(now_price-entry_prce)+'ドルです')
            if now_price-entry_prce<-40:
                client.Order.Order_new(side="Sell",symbol="BTCUSD",order_type="Market",qty=10000,time_in_force="GoodTillCancel").result()
                have=0
                print('損益は'+str(entry_prce-now_price)+'ドルです')
        if have==2:
            if entry_prce-now_price>40:
                client.Order.Order_new(side="Buy",symbol="BTCUSD",order_type="Market",qty=10000,time_in_force="GoodTillCancel").result()
                have=0
                print('損益は'+str(entry_prce-now_price)+'ドルです')
            if entry_prce-now_price<-40:
                client.Order.Order_new(side="Buy",symbol="BTCUSD",order_type="Market",qty=10000,time_in_force="GoodTillCancel").result()
                have=0
                print('損益は'+str(entry_prce-now_price)+'ドルです') 
    cnt+=1
    time.sleep(interval)
    
'''
かなりシンプルなので利益率の期待はかなり低いですが､あくまでAPIを用いたトレードの仕組みだけを理解するため参考になれば幸いです

自動売買をする上で重要なアクション
終値を取得する
client.Market.Market_symbolInfo(symbol="BTCUSD").result()[0]['result'][0]['last_price']
エントリーをする(成り行き買い)
client.Order.Order_new(side="Buy",symbol="BTCUSD",order_type="Market",qty=10000,time_in_force="GoodTillCancel")
エントリーをする(成り行き売り)
client.Order.Order_new(side="Sell",symbol="BTCUSD",order_type="Market",qty=10000,time_in_force="GoodTillCancel")
損益を確定するには､エントリーした際の逆の事をするだけ
'''

            