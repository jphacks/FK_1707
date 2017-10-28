import requests
import json
import re
import psycopg2.extensions


def reply_location_text(cur, reply_token, REPLY_ENDPOINT, HEADER, userid, address, latitude, longitude):
    # 緯度と経度を小数点２桁に丸める
    latitude = round(latitude, 2)
    longitude = round(longitude, 2)
    reply = ''

    # DB操作
    cur.execute("SELECT * FROM location WHERE userid=%s;", [userid])
    if cur.fetchone() == None:
        cur.execute("INSERT INTO location (userid, address, latitude, longitude) VALUES(%s, %s, %s, %s);", [
                    userid, address, latitude, longitude])
        reply += '現在地を設定しました。\n'
    else:
        # DB操作(現在地を再設定)
        cur.execute("UPDATE location SET address=%s, latitude=%s, longitude=%s WHERE userid=%s;", [
                    address, latitude, longitude, userid])

        reply += '現在地を設定し直しました。\n'

    reply += address + '\n'
    reply += '緯度は' + str(latitude) + '、\n'
    reply += '経度は' + str(longitude) + 'です。'

    payload = {
        "replyToken": reply_token,
        "messages": [
              {
                  "type": "text",
                  "text": reply
              }
        ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER,
                  data=json.dumps(payload))  # LINEにデータを送信

    return reply
