from openai import OpenAI

client = OpenAI(
  api_key = "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"
)

image_url = "https://savable-app-server.s3.ap-northeast-2.amazonaws.com/verification/member_835/participation_1740_a8bfd13625dd40c2b8b61310740080e6.jpg";

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "이 이미지에는 무엇이 있나요?"},
        {
          "type": "image_url",
          "image_url": {
            "url": image_url,
            "detail": "high" # 이미지 해상도 설정
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(type(response.choices[0].message.content))