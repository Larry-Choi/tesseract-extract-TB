import csv
from PIL import Image
import pytesseract
import os
from datetime import datetime
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_texts_to_csv(input_directory, output_csv_path):
    """디렉토리 내 모든 이미지를 처리하여 필요한 데이터를 추출하고 같은 행(row)에 저장"""
    data_row = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  # 현재 시간 추가

    # 디렉토리 내 모든 이미지 처리
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(input_directory, filename)
            
            # 이미지에서 텍스트 추출
            text = pytesseract.image_to_string(Image.open(image_path), lang="kor+eng", config='--psm 6')
            
            # 특정 데이터 추출
            if "내장 배터리용 전원 충전" in text:
                match = re.search(r"([\d.]+W)", text)
                data_row['내장 배터리용 전원 충전'] = match.group(1) if match else "N/A"
            elif "오늘 발전량" in text:
                match = re.search(r"([\d.]+ W-h)", text)
                data_row['오늘 발전량'] = match.group(1) if match else "N/A"
            elif "오늘 평균 배터리 전력" in text:
                match = re.search(r"([\d.]+%)", text)
                data_row['오늘 평균 배터리 전력'] = match.group(1) if match else "N/A"
            
            print(f"Processed: {filename}")
            #os.remove(image_path)  # 이미지 파일 삭제

    # 기본 값 추가 (결측 데이터 처리)
    for field in ['내장 배터리용 전원 충전', '오늘 발전량', '오늘 평균 배터리 전력']:
        if field not in data_row:
            data_row[field] = "N/A"

    # CSV 저장
    fieldnames = ['timestamp', '내장 배터리용 전원 충전', '오늘 발전량', '오늘 평균 배터리 전력']
    file_exists = os.path.isfile(output_csv_path)

    with open(output_csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # 헤더 작성
        writer.writerow(data_row)  # 데이터 저장

    print(f"Data saved to {output_csv_path}")

# 입력 이미지 파일 경로와 출력 CSV 파일 경로 설정
input_directory = "./testing-source/"  # 이미지 파일이 있는 디렉토리
output_csv_path = "./output/output.csv"  # CSV 파일 경로

# 함수 실행
extract_texts_to_csv(input_directory, output_csv_path)
