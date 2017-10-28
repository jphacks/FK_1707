import json
import requests
import re
import psycopg2.extensions

from django.shortcuts import render
from django.http import HttpResponse
import bot.secret as secret
from bot import touroku , location , getweather


REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'

ACCESS_TOKEN = secret.ACCESS_TOKEN
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

# コネクションの作成
con = psycopg2.connect(secret.connection_postgreSQL)
# カーソルの作成
print("カーソル作成！")
cur = con.cursor()
print(cur)


def index(request):
    return HttpResponse("This is bot api.")


def callback(request):

    reply = ""
    request_json = json.loads(request.body.decode(
        'utf-8'))  # requestの情報をdict形式で取得

    for e in request_json['events']:
        userid = e['source']['userId']  # userIDの取得
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            # LINEにセリフを送信する関数
            if re.match('天気', text):
                reply += getweather.reply_weather(cur, reply_token, REPLY_ENDPOINT, HEADER, userid)

            reply += touroku.reply_text(cur, reply_token,
                                        REPLY_ENDPOINT, HEADER, text, userid)

        elif message_type == 'location':  # メッセージタイプが位置情報だった場合
            if 'address' in e['message']:
                address = e['message']['address']  # アドレスを取得
            else:
                address = '住所がありませんでした。'
            latitude = e['message']['latitude']  # 緯度を取得
            longitude = e['message']['longitude']  # 経度を取得
            reply += location.reply_location_text(
                cur, reply_token, REPLY_ENDPOINT, HEADER, userid, address, latitude, longitude)
    if reply == "":
        print("replyは空です！")
    # DBをコミット
    else:

        print(reply)
        print("コミット")
        con.commit()
    print("終了")
    return HttpResponse(reply)  # テスト用
