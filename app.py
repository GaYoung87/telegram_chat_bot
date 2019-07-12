from flask import Flask, request
from decouple import config
import pprint
import requests
app = Flask(__name__)

# 변수
API_TOKEN = config('API_TOKEN') # 상수는 대문자
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')


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

        # 첫 네글자가 '/한영 '일 때 -> 띄어쓰기 있어야 돌아감
        if text[0:4] == '/한영 ':
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
            }  # 요청을 받으면 그것을 header라는 곳에 넣어줘!
            data = {
                'source': 'ko',
                'target': 'en',
                'text': text[4:] # '/번역 ' 이후의 문자열만 대상으로 번역
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data) # requests : 요청보내기, request : ________________
            text = papago_res.json().get('message').get('result').get('translatedText')  #.json했던 딕셔너리값으로 

        if text[0:4] == '/영한 ':
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
            }  # 요청을 받으면 그것을 header라는 곳에 넣어줘!
            data = {
                'source': 'en',
                'target': 'ko',
                'text': text[4:] # '/번역 ' 이후의 문자열만 대상으로 번역
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data) # requests : 요청보내기, request : ________________
            text = papago_res.json().get('message').get('result').get('translatedText')


        # 내가 받은 문자를 그대로 보낸다.
        # Send Message API URL Logic
        base_url = 'https://api.telegram.org'
        api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url)



    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
