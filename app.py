from flask import Flask, request
from decouple import config
import pprint
import requests
app = Flask(__name__)
API_TOKEN = config('API_TOKEN') # 상수는 대문자
CHAT_ID = config('CHAT_ID')

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/greeting/<name>')
def greeting(name):
    return f'Hello, {name}'


@app.route(f'/{API_TOKEN}', methods=['POST'])
def telegram():
    from_telegram = request.get_json()
    # pprint.pprint(from_telegram)
    if from_telegram.get('message') is not None:  #dictionary 접근방법 1)대괄호(안에 내용없으면 error) 2).get(안에 내용없으면 없는대로 나옴)
        # 우리가 원하는 로직을 쌓아가면 된다.
        #나한테 챗 보낸사람의 id를 순간순간 꺼내서 보냄
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text') # 사용자가 보낸 텍스트

        if text == '점심메뉴':
            text = '짜장면이나 먹어!'


        # 내가 받은 문자를 그대로 보낸다.
        # Send Message API URL Logic
        base_url = 'https://api.telegram.org'
        api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url)



    return '', 200


if __name__ == '__main__':
    app.run(debug=True)








