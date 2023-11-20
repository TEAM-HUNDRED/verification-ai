from flask import Flask, jsonify, request
from openai import OpenAI
from http import HTTPStatus

# Flask 애플리케이션 초기화
app = Flask(__name__)

client = OpenAI(
  api_key = "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"
)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'message': 'Bad Request'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not Found'}), 404

# 이미지 캡셔닝 API 엔드포인트 정의
@app.route('/image-captioning', methods=['POST'])
def image_captioning():
    # 요청으로부터 이미지 URL 받기
    print("api  호출")
    params = request.get_json()
    image_url = params['image']
    text = "사진을 분석하고 다음 항목을 만족하는지 O, X를 통해 판단해줘.\n" \
           "답변은 O, X만 공백으로 구분해서 반환해줘.\n" \
           "1. 컵이나 텀블러처럼 음료를 담을 수 있는 물체가 존재하는가?\n" \
           "2. 음료를 담을 수 있는 물체의 내부에 음료와 같은 액체가 있거나, 음료를 타먹을 수 있는 가루나 시럽 같은 것이 담겨 있는가?\n" \
           "3. 음료를 만들어 먹을 수 있는 스틱, 티백, 차 주머니 등이 있는가?\n" \
           "4. 음료를 만들어 먹을 수 있는 스틱, 티백, 차 주머니 등이 개봉되거나 사용되어 있는 상태인가?\n" \
           "5. 커피머신을 이용해 커피를 내려먹고 있는가?"

    print(text)
    # OpenAI에 요청 보내기
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
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
    print(pass_or_fail(message))
    return jsonify({"status": HTTPStatus.OK, "data": pass_or_fail(message)})

def pass_or_fail(result):
    # 조건 확인: index 0, 1, 2, 3가 O이거나 index 0, 1, 4가 O인 경우
    if (result[0] == "O" and result[1] == "O" and result[2] == "O" and result[3] == "O") or \
       (result[0] == "O" and result[1] == "O" and result[4] == "O"):
        return True
    else:
        return False

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
