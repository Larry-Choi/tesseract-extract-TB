from PIL import Image, ImageFilter, ImageEnhance
import os
import time

def preprocess_image(input_directory):
    """이미지 전처리 함수"""
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(input_directory, filename)
            try:
                # 이미지 열기
                img = Image.open(image_path)

                # 이미지 확대
                img = img.resize((img.width * 4, img.height * 4))

                # 그레이스케일 변환
                img = img.convert("L")

                # 노이즈 제거 (미디언 필터)
                img = img.filter(ImageFilter.MedianFilter(size=3))

                # 대비 증가
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(3.0)

                # 이진화 처리
                threshold = 192  # 임계값
                img = img.point(lambda p: p > threshold and 255)

            
                # 전처리된 이미지 저장
                preprocessed_path = image_path.replace(".png", "_preprocessed.png")
                img.save(preprocessed_path)

                print(f"Preprocessed image saved to {preprocessed_path}")

                os.remove(image_path)  # 원본 이미지 삭제
                time.sleep(1)  # 1초 대기
            except Exception as e:
                print(f"Error during image preprocessing: {e}")
                return None
            
def subprocess_image(input_directory):
    """이미지 전처리 함수"""
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(input_directory, filename)
            try:
                # 이미지 열기
                img = Image.open(image_path)

                # 이미지 확대
                img = img.resize((img.width * 3, img.height * 3))

                # 노이즈 제거 (미디언 필터)
                img = img.filter(ImageFilter.MedianFilter(size=3))

                # 대비 증가
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(3.0)

                # 이진화 처리
                threshold = 192  # 임계값
                img = img.point(lambda p: p > threshold and 255)

            
                # 전처리된 이미지 저장
                preprocessed_path = image_path.replace(".png", "_preprocessed.png")
                img.save(preprocessed_path)

                print(f"Preprocessed image saved to {preprocessed_path}")

                os.remove(image_path)  # 원본 이미지 삭제
                time.sleep(1)  # 1초 대기
            except Exception as e:
                print(f"Error during image preprocessing: {e}")
                return None

if __name__ == "__main__":
    # 사용자 입력
    input_directory = "./testing-source/"  # 이미지 파일이 있는 디렉토리
    preprocess_image(input_directory)  # 이미지 전처리 실행
    subprocess_image(input_directory)  # 이미지 전처리 실행
