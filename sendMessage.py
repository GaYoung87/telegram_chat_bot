import requests  # 우리한테 sendMessage를 보내라는 요청을 하기 위해
import pprint
from decouple import config #decouple에서부터 config라는 것만 호출


base_url = 'https://api.telegram.org'
token = config('API_TOKEN')  #.env라는 파일에 API_TOKEN이랑 CHAT_ID입력
chat_id = config('CHAT_ID')
text = '디커풀 테스트!'

api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'

response = requests.get(api_url)  # 요청을 어떻게 처리했는지에 대한 응답은 해줌.(ex.404, 200)
pprint.pprint(response.json())

# 코드 저장하려니까 id, token값을 숨기고 저장하고픔 -> .env 라는 파일 만듦
# 우리가 hi라고 메세지하면 그에 대한 답을 하는거도 가능.

















