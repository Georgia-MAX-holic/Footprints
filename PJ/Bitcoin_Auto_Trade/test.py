from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time

def capture_upbit_chart():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        # 업비트 차트 URL로 이동
        driver.get("https://upbit.com/full_chart?code=CRIX.UPBIT.KRW-BTC")
        time.sleep(5)  # 차트 로딩 대기

        # 차트 요소를 찾고 스크린샷 캡처
        chart_element = driver.find_element_by_css_selector("div.chart-container")
        location = chart_element.location
        size = chart_element.size

        driver.save_screenshot("full_page.png")
        full_image = Image.open("full_page.png")

        # 차트 부분만 잘라내기
        chart_image = full_image.crop((
            location['x'],
            location['y'],
            location['x'] + size['width'],
            location['y'] + size['height']
        ))
        chart_image.save("upbit_chart.png")

    finally:
        driver.quit()

capture_upbit_chart()