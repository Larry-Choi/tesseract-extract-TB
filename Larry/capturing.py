import pyautogui
import os
from datetime import datetime
import time
import json

# 저장할 디렉토리 설정
output_directory = './testing-source'
os.makedirs(output_directory, exist_ok=True)


def refresh(first_position, second_position):
    """갱신"""
    # 첫 번째 클릭
    pyautogui.click(first_position['x'], first_position['y'])
    time.sleep(2)

    # 두 번째 클릭
    pyautogui.click(second_position['x'], second_position['y'])
    print("Refresh completed.")

def calculate_region(third_position, fourth_position):
    """좌상단과 우하단 좌표로 직사각형 영역 계산"""
    x = third_position['x']
    y = third_position['y']
    width = fourth_position['x'] - third_position['x']
    height = fourth_position['y'] - third_position['y']
    return (x, y, width, height)

def screenshot(region_do=None):
# 현재 시간으로 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(output_directory, f'screenshot_{timestamp}.png')

    # 특정 영역 캡처
    screenshot = pyautogui.screenshot(region=region_do)


    # 파일로 저장
    screenshot.save(file_path)
    print(f'Screenshot saved to {file_path}')

if __name__ == '__main__':
    # 좌표 읽기
    with open('positions.json', 'r') as f:
        positions = json.load(f)

    # 저장되어있는 json 파일에서 좌표 가져오기
    first_position = positions['first_position']
    second_position = positions['second_position']
    third_position = positions['third_position']
    fourth_position = positions['fourth_position']

    # 직사각형 영역 계산
    region = calculate_region(third_position, fourth_position)

    refresh(first_position, second_position)
    time.sleep(3)
    screenshot(region)
