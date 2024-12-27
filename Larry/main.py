import os
import time
import pyautogui
import json
import subprocess
import pkg_resources
import sys

# 실행할 파이썬 파일 경로 설정
script1 = 'capturing.py' #screenshot
script2 = 'preprocessing.py' #preprocessing
#script3 = 'extract.py'  #ocr
script4 = 'simple-extract.py'  #ocr

def ensure_pkg_resources():
    """pkg_resources가 없을 경우 setuptools 설치"""
    try:
        import pkg_resources  # pkg_resources가 이미 설치되어 있는지 확인
        print("pkg_resources is available.")
    except ImportError:
        # pkg_resources가 없으면 setuptools 설치
        print("pkg_resources is not available. Installing setuptools...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
            print("setuptools has been installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install setuptools. Error: {e}")
            sys.exit(1)  # 설치 실패 시 프로그램 종료

def install_package(package_name):
    """패키지가 설치되어 있는지 확인하고, 설치되어 있지 않으면 pip로 설치"""
    try:
        # 패키지 설치 여부 확인
        pkg_resources.get_distribution(package_name)
        print(f"{package_name} is already installed.")
    except pkg_resources.DistributionNotFound:
        # 패키지가 설치되어 있지 않으면 설치 진행
        try:
            print(f"Installing {package_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"{package_name} has been installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_name}. Error: {e}")

def install_packages(packages):
    """여러 패키지를 설치"""
    for package in packages:
        install_package(package)

def get_mouse_position(prompt):
    """마우스 클릭으로 좌표를 설정"""
    print(prompt)
    print("Move the mouse to the desired position and press Enter...")
    input("Press Enter when ready.")  # 사용자가 Enter를 누를 때까지 대기
    position = pyautogui.position()  # 현재 마우스 위치 좌표 가져오기
    print(f"Selected position: {position}")
    return position

def setup_positions():
    """좌표 설정 또는 기존 좌표 불러오기"""
    if os.path.exists('positions.json'):
        # 기존 좌표를 사용할지 재설정할지 묻기
        use_existing = input("Positions.json exists. Do you want to use the existing positions? (y/n): ").strip().lower()
        if use_existing == 'y':
            # 기존 좌표 불러오기
            print("Loaded existing positions from positions.json.")
            return
        elif use_existing == 'n':
            print("Resetting positions...")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            return setup_positions()

    # 새로운 좌표 설정
    print("Setting click positions...")
    first_position = get_mouse_position("Set the first refresh position.")
    second_position = get_mouse_position("Set the second refresh position.")
    third_position = get_mouse_position("Set the top-left corner of the capture region.")
    fourth_position = get_mouse_position("Set the bottom-right corner of the capture region.")

    positions = {
        "first_position": {"x": first_position.x, "y": first_position.y},
        "second_position": {"x": second_position.x, "y": second_position.y},
        "third_position": {"x": third_position.x, "y": third_position.y},
        "fourth_position": {"x": fourth_position.x, "y": fourth_position.y}
    }

    # 좌표 저장
    with open('positions.json', 'w') as f:
        json.dump(positions, f)
    print("Positions saved to positions.json.")
    return positions

def main():

    # pkg_resources가 없으면 setuptools 설치
    ensure_pkg_resources()

    # 필요한 패키지 설치
    packages_to_install = ["pytesseract", "Pillow", "pyautogui"]
    install_packages(packages_to_install)

    # 좌표 설정 또는 불러오기
    setup_positions()

    # 주기적 반복
    start_time = time.time()
    while True:
        tmp_time = time.time()
        os.system(f'python {script1}')
        time.sleep(1)  # 5초 대기
        os.system(f'python {script2}')
        time.sleep(1)
        os.system(f'python {script4}')
        time.sleep(5)  # 5초 대기
        
        # 1분 대기
        rest = 60 - (time.time() - tmp_time)
        time.sleep(rest)
    

if __name__ == '__main__':
    main()  # duration 값 전달