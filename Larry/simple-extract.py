import csv
from PIL import Image
import pytesseract
import os
from datetime import datetime
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_and_save_to_csv(input_directory, output_csv_path):
    """디렉토리 내 모든 이미지를 처리하여 필요한 데이터를 추출하고 CSV에 저장"""
    data_row = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  # 현재 시간 추가

    # 디렉토리 내 모든 이미지 텍스트 처리
    all_text = ""
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(input_directory, filename)
            
            # 이미지에서 텍스트 추출
            text = pytesseract.image_to_string(Image.open(image_path), lang="kor+eng", config='--psm 6')
            all_text += text + "\n"  # 모든 텍스트를 하나로 합침

            print(all_text)
            
            print(f"Processed: {filename}")
            os.remove(image_path)  # 이미지 파일 삭제

    # 전체 텍스트에서 필요한 데이터 추출
    match_battery = re.search(r"내장 배터리용 전원 충전.*?([\d.]+W)", all_text, re.DOTALL)
    match_generation = re.search(r"오늘 발전량.*?([\d.]+ W-h)", all_text, re.DOTALL)
    match_avg_battery = re.search(r"오늘 평균 배터리 전력.*?([\d.]+%)", all_text, re.DOTALL)

    # 데이터 정리
    battery_power = match_battery.group(1) if match_battery else "N/A"
    data_row['내장 배터리용 전원 충전'] = battery_power
    data_row['오늘 발전량'] = match_generation.group(1) if match_generation else "N/A"
    data_row['오늘 평균 배터리 전력'] = match_avg_battery.group(1) if match_avg_battery else "N/A"

    # Voltage 계산
    if battery_power != "N/A":
        numeric_battery = float(battery_power.replace("W", ""))
        print(numeric_battery)
        data_row['생산전압'] = numeric_battery / 5
    else:
        data_row['생산전압'] = "N/A"

    # CSV 저장
    fieldnames = ['timestamp', '내장 배터리용 전원 충전', '오늘 발전량', '오늘 평균 배터리 전력', '생산전압']
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
parse_and_save_to_csv(input_directory, output_csv_path)
