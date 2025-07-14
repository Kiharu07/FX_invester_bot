import time #時間を扱うため
import yaml #config.yamlを読み込むため
import logging
from logging.handlers import RotatingFileHandler # ログをファイルに保存するため（どういうこと？）

import random #ダミーデータ用設定


logger = logging.getLogger("fxBotLogger") #"fxBotという名前のログ記録のノートを作成"
logger.setLevel(logging.INFO) #記録する基準となる重要度をINFO（通常）に設定
handler = RotatingFileHandler("trade_log.txt",maxBytes=1024*1024,backupCount=2,encoding="utf-8") #trade_log.textファイルに記録し、1MBまで保存でき、２つまで古いファイルを残す。
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s') #日付と時間、重要度、メッセージ内容をフォーマットとする。（例：2023-10-01 12:00:00,000 : INFO : 今は147円
handler.setFormatter(formatter) #設定したフォーマットをペン先にセット
logger.addHandler(handler) #ペン先をノートにセット

with open("config.yaml", "r",encoding="utf-8") as unchi: #config.yamlを読み込んで（r=readの略）、unchiという名前で使えるようにする
    config = yaml.safe_load(unchi) #yamlの内容をconfigという名前でpythonで使える形に変換

buy_border = config["strategy"]["buy_border"] #config.yamlのstrategyのbuy_borderをbuy_borderという名前で使えるようにする
sell_border = config["strategy"]["sell_border"] #config.yamlのstrategyのsell_borderをsell_borderという名前で使えるようにする
volume = config["strategy"]["volume"] #config.yamlのstrategyのvolumeをvolumeという名前で使えるようにする
interval = config["interval"] #config.yamlのintervalをintervalという名前で使えるようにする

trademode = "IDLE"#初期トレードモードをIDLE（何もしない）に設定

def get_buy_point(price):
    return random.uniform(0,100) #ランダムな買いポイントを生成

def get_sell_point(price):
    return random.uniform(0,100) #ランダムな売りポイントを生成    

def should_trade(buy_point,sell_point,buy_border,sell_border,trademode):
    if trademode == "IDLE":
        if buy_point > buy_border:
            return {"type":"buy","reason":f"BuyPoint={buy_point:.2f} > BuyBorder={buy_border}"} #買う時のtypeと理由を返す (f"文字列"は{}内を数字として扱う書き方)
    elif trademode == "TRADING":
        if sell_point > sell_border:
            return {"type":"sell","reason":f"SellPoint={sell_point:.2f} > SellBorder={sell_border}"} #売る時のtypeと理由を返す
    return None #トレードしない場合はNoneを返す

def current_price():
    return random.uniform(140.0,160.0) #ダミー価格取得の関数を設定

def main():
    global trademode #trademodeを関数外でもどこでも使えるようにする

    logger.info("FX Bot 起動") #FX Botの起動をtrade_log.txtに記録.(logのレベルはinfoなので、重要度は通常)
    while True: #無限ループ
        try:#エラーが起きても止まらずに続けたい
            
            price = current_price() #現在の価格を取得
            buy_point = get_buy_point(price) #買いポイントを取得
            sell_point = get_sell_point(price) #売りポイントを取得
            logger.info(f"[価格]: {price:.2f}|[BuyPoint]: {buy_point:.2f}|[SellPoint]: {sell_point:.2f}|[Mode]{trademode}") #現在の価格と買いポイント、売りポイントをtrade_log.txtに記録
            
            decision = None #decisionを初期化
            decision = should_trade(buy_point,sell_point,buy_border,sell_border,trademode) #トレードの判断をする
            if decision: #decisionがNoneでない場合（トレードする場合）
                logger.info(f"→取引判断:{decision['type']} 実行 | 理由: {decision['reason']}") #decisonの内容をtrade_log.txtに記録
                if decision["type"] == "buy": #買う場合
                    trademode = "TRADING" #トレードモードをTRADINGに変更
                elif decision["type"] == "sell": #売る場合
                    trademode = "IDLE" #トレードモードをIDLEに変更
            else:
                logger.info("→取引無し")
            time.sleep(interval) #設定した時間だけ待つ

        except Exception as e: #何かエラーが起きたら
            logger.info(f"エラー発生: {e}") #エラー内容をtrade_log.txtに記録
            time.sleep(10)#10秒待ってから再試行

if __name__ == "__main__": #ほかのファイルからインポートされた場合に勝手に実行しないようにする
    main() # main関数を実行
