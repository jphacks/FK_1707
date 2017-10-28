import requests
import json
import re
import psycopg2.extensions
import bot.secret as secret


def reply_text(cur, reply_token, REPLY_ENDPOINT, HEADER, text, userid):
    reply = ''

    """
    url= secret.WCDAPI
    response = requests.get(url)
    tenki = json.loads(response.text)
    """

    if re.match('登録 ', text):
        memo = text[3:]
        cur.execute("INSERT INTO touroku(userid, data) VALUES(%s, %s);", [
                    userid, memo])
        reply += "「" + memo + '」を登録しました。'

    elif re.match('削除 ', text):
        memo = text[3:]
        if memo == '全部' or memo == 'ぜんぶ' or memo == 'すべて' or memo == '全て':
            cur.execute("DELETE FROM touroku WHERE userid=%s", [userid])
            reply += "すべてのメモを削除しました。"

        elif memo == '最後' or memo == 'さいご':
            cur.execute("SELECT * FROM touroku WHERE userid=%s", [userid])
            sakujo_taplelist = cur.fetchall()
            last_memo = len(sakujo_taplelist) - 1
            idz = sakujo_taplelist[last_memo][0]
            reply += "「" + sakujo_taplelist[last_memo][2] + "」を削除しました。"
            cur.execute("DELETE FROM touroku WHERE id=%s", [idz])

        else:
            memo = int(memo) - 1
            cur.execute("SELECT * FROM touroku WHERE userid=%s", [userid])
            sakujo_taplelist = cur.fetchall()
            idz = sakujo_taplelist[memo][0]
            reply += "「" + sakujo_taplelist[memo][2] + "」を削除しました。"
            cur.execute("DELETE FROM touroku WHERE id=%s", [idz])

    elif text == '一覧':
        cur.execute("SELECT * FROM touroku WHERE userid = %s", [userid])
        itiran_taplelist = cur.fetchall()
        if len(itiran_taplelist) is not 0:
            print(itiran_taplelist)
            for i, j in enumerate(itiran_taplelist):
                reply += str(i+1) + " " + j[2] + '\n'
            reply = reply[:-1]
        else:
            reply += "何も登録されていません！"

    elif re.match('おうむがえし ', text):
        reply += text[7:]

    elif re.match('userid', text):
        reply += userid

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
