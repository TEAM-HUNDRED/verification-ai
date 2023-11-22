from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from http import HTTPStatus
from image_ocr import clova_ocr

# Flask 애플리케이션 초기화
app = Flask(__name__)
CORS(app)

client = OpenAI(
  api_key = "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"
)

@app.route('/')
def home():
   return 'EC2 Flask Test'

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'message': 'Bad Request'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not Found'}), 404

# 이미지 캡셔닝 API 엔드포인트 정의
@app.route('/image-captioning', methods=['POST'])
def verification_image_captioning():
    # 요청으로부터 이미지 URL 받기
    print("IMAGE CAPTIONING api  호출")
    params = request.get_json()
    image_url = params['image']
    prompt = params['prompt']

    print(prompt)
    # OpenAI에 요청 보내기
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                            "detail": "high"  # 이미지 해상도 설정
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    # 응답 반환
    message = response.choices[0].message.content.split(' ')
    print(message)
    print(pass_or_fail_coffee(message))
    return jsonify({"status": HTTPStatus.OK, "data": pass_or_fail_coffee(message)})

# OCR 결과 분 API 엔드포인트 정의
@app.route('/ocr', methods=['POST'])
def verification_ocr():
    # 요청으로부터 이미지 URL 받기
    print("OCR api  호출")
    params = request.get_json()
    image_url = params['image']

    ocr_result = clova_ocr(image_url) # 이미지 기반 OCR 진행
    prompt = ocr_result + '\n' + params['prompt']
    print(prompt)

    # OpenAI에 요청 보내기
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        max_tokens=300,
    )
    # 응답 반환
    message = response.choices[0].message.content.split(' ')
    print(message)
    print(pass_or_fail_consumption(message))
    return jsonify({"status": HTTPStatus.OK, "data": pass_or_fail_consumption(message)})

def pass_or_fail_coffee(result): # 음료값 절약 챌린지
    # 조건 확인: index 0, 1, 2, 3가 O이거나 index 0, 1, 4가 O인 경우
    if (result[0] == "O" and result[1] == "O" and result[2] == "O" and result[3] == "O") or \
       (result[0] == "O" and result[1] == "O" and result[4] == "O"):
        return True
    else:
        return False

def pass_or_fail_consumption(result): # 음료값 절약 챌린지
    if (result[0] == "O" and result[1] == "O") or \
       (result[0] == "O" and result[3] == "O"):
        return True
    else:
        return False

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
