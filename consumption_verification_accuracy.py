import pandas as pd
from accuracy_test import verification_ocr

# Replace 'your_csv_file_path.csv' with the path to your CSV file
csv_file_path = '/Users/day/Desktop/SAVABLE/Project/management/ai-verification/csv/challenge_4.csv'

# Load the CSV file into a DataFrame
data = pd.read_csv(csv_file_path)

# Extract all the values from the 'Image' column
image_column_values = data['Image'].tolist()
state_column_values = data['State'].tolist()

accuracy = [[0, 0], [0, 0]]
for i in range(100): # 일단 30개만 진행
    print(i)
    try:
        ai_bool = verification_ocr(image_column_values[i])
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
        pass

    for i in range(2):
        for j in range(2):
            print(accuracy[i][j], end=' ')
        print()

for i in range(2):
    for j in range(2):
        print(accuracy[i][j], end=' ')
    print()

# # Print the list of image values
# print(image_column_values)
# print(state_column_values)
