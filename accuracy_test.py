from flask import Flask, jsonify, request
from openai import OpenAI
from http import HTTPStatus
from image_ocr import clova_ocr

client = OpenAI(
  # api_key = "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" # 다영
    api_key = "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" # 채원
)

def verification_image_captioning(image_url):
    # 요청으로부터 이미지 URL 받기
    print("IMAGE CAPTIONING api  호출")
    prompt = "사진을 분석하고 다음 항목을 만족하는지 O, X를 통해 판단해 줘." \
             "\n답변은 O, X만 공백으로 구분해서 반환해 줘." \
             "\n1.컵이나 텀블러처럼 음료를 담을 수 있는 물체가 존재하는가?" \
             "\n2.음료를 담을 수 있는 물체의 내부에 음료와 같은 액체가 있거나, 음료를 타먹을 수 있는 가루나 시럽 같은 것이 담겨 있는가?" \
             "\n3.음료를 만들어 먹을 수 있는 스틱, 티백, 차 주머니 등이 있는가?" \
             "\n4.음료를 만들어 먹을 수 있는 스틱, 티백, 차 주머니 등이 개봉되거나 사용되어 있는 상태인가?" \
             "\n5.커피 머신을 이용해 커피를 내려먹고 있는가?"

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
                            "detail": "low"  # 이미지 해상도 설정
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
    return pass_or_fail_coffee(message)

def verification_ocr(image_url):
    # 요청으로부터 이미지 URL 받기
    print("OCR api  호출")

    ocr_result = clova_ocr(image_url) # 이미지 기반 OCR 진행
    prompt = ocr_result + '\n' + '위는 가계부 이미지를 OCR을 진행한 결과야.\n' \
                                 '위 텍스트를 내용을 분석하고 다음 항목을 만족하는지 O, X를 통해 판단해 줘.\n' \
                                 '답변은 O, X만 공백으로 구분해서 반환해 줘.\n' \
                                 '1. 가계부 날짜가 존재하는가?\n' \
                                 '2. 상품을 구매한 지출 내역이 존재하는가?\n' \
                                 '3. 지출에 대한 소감/설명/한 줄 평 등이 존재하는가?\n' \
                                 '4. 지출이 없는 날인가?\n' \
                                 '5. 지출이 없는 경우 무지출에 대한 노하우가 작성되어 있는가?\n'
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
        max_tokens=500,
    )
    # 응답 반환
    message = response.choices[0].message.content.split(' ')
    return pass_or_fail_consumption(message)

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
