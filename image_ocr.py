import requests
import uuid
import time
import json
from io import BytesIO

api_url = 'https://5sem7j9eeb.apigw.ntruss.com/custom/v1/26283/46536879e3a74171667ed272899406e7d708967df8836c6d789d05d7f45d50aa/general'
secret_key = 'dFdVSGZyeXBVZU94TU5pZkxTYkpwdlFlQVVYSVpUT20='

def clova_ocr(image_url):
    # 이미지 데이터 다운로드
    response = requests.get(image_url)
    image_data = BytesIO(response.content)

    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
      ('file', ('image.jpg', image_data))  # 이미지 데이터와 파일 이름 지정
    ]
    headers = {
      'X-OCR-SECRET': secret_key
    }

    # OCR API에 요청 보내기
    ocr_response = requests.post(api_url, headers=headers, data=payload, files=files)

    # 응답 데이터를 JSON으로 변환
    json_data = ocr_response.json()

    # inferText 값을 저장할 리스트 초기화
    infer_texts = []

    # images 내의 모든 field들을 순회하면서 inferText를 추출
    for image in json_data['images']:
        for field in image['fields']:
            infer_texts.append(field['inferText'])

    # infer_texts를 개행 문자로 구분하여 하나의 문자열로 만듦
    output_text = '\n'.join(infer_texts)

    # 결과 출력
    return output_text