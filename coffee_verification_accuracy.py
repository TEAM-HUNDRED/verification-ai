import pandas as pd
from accuracy_test import verification_image_captioning

# Replace 'your_csv_file_path.csv' with the path to your CSV file
csv_file_path = '/Users/day/Desktop/SAVABLE/Project/management/ai-verification/csv/challenge_1.csv'

# Load the CSV file into a DataFrame
data = pd.read_csv(csv_file_path)

# Extract all the values from the 'Image' column
image_column_values = data['Image'].tolist()
state_column_values = data['State'].tolist()

accuracy = [[0, 0], [0, 0]]
for i in range(50, 100): # 일단 30개만 진행
    print(i)
    try:
        ai_bool = verification_image_captioning(image_column_values[i])
        print('H: ', state_column_values[i], '/ AI: ', ai_bool)
        if state_column_values[i] == 'SUCCESS':  # 인간 성공
            if ai_bool:  # AI 성공
                accuracy[0][0] += 1
            else:  # AI 실패
                accuracy[1][0] += 1
        elif state_column_values[i] == 'FAIL':
            if ai_bool:  # AI 성공
                accuracy[0][1] += 1
            else:  # AI 실패
                accuracy[1][1] += 1
    except Exception as e:
        print(f"Error occurred: {e}")
        pass  # 에러 발생 시 다음 반복으로 넘어감

    for x in range(2):
        for y in range(2):
            print(accuracy[x][y], end=' ')
        print()

# # Print the list of image values
# print(image_column_values)
# print(state_column_values)
