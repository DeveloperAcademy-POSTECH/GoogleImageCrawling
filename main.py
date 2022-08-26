## 개인깃허브에 추가하기!!

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os, time, random
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.request


## driver 생성
def chromeWebdriver():
    options = Options()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument('window-size=1920x1080')
    options.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def collect_image(search_word):
    url = "https://www.google.co.kr"
    file_path = "/Users/david/Desktop/imagecrawling"
    os.makedirs(file_path + "/" + search_word)
    file_save_dir = file_path + "/" + search_word

    driver = chromeWebdriver()
    driver.get(url)
    time.sleep(random.uniform(2, 3))
    elem_q = driver.find_element(By.NAME, 'q')
    elem_q.send_keys(search_word)
    elem_q.submit()

    driver.find_element(By.LINK_TEXT, '이미지').click() # 텍스트 메뉴 '이미지' 링크 클릭
    time.sleep(random.uniform(1,2))

    file_no = 1
    count = 1
    img_src = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    imgs = driver.find_elements(By.CSS_SELECTOR, '#islrg > div.islrc > div a.wXeWr.islib.nfEiy')
    print(len(imgs))

    for img in imgs:
        img_src1 = img.click()
        img_src2 = driver.find_element(By.CSS_SELECTOR, '#Sva75c > div > div > div.pxAole > div.tvh9oe.BIB1wf > c-wiz > div > div.OUZ5W > div.zjoqD > div.qdnLaf.isv-id > div > a')
        time.sleep(random.uniform(1, 2))
        img_src3 = img_src2.find_element(By.TAG_NAME, 'img').get_attribute('src')
        if img_src3[:4] != 'http':
            continue
        print(count, img_src3, '\n')
        img_src.append(img_src3)
        count += 1

    for i in range(len(img_src)):
        extention = img_src[i].split('.')[-1]
        ext = ''
        print(extention)
        if extention in ('jpg', 'JPG', 'jpeg','JPEG', 'png', 'PNG', 'gif', 'GIF'):
            ext = '.' + extention
        else:
            ext = '.jpg'
        try:
            # path = "/Users/david/Desktop/imagecrawling/" + search_word
            urllib.request.urlretrieve(img_src[i], str(file_no).zfill(3) + ext)
            print(img_src[i])
        except Exception:
            continue
        file_no += 1
        # 파일디렉토리에 저장하기
        imagePath = file_path + "/" + search_word
        print(f'{file_no}번째 이미지 저장')
    driver.close()


if __name__ == '__main__':
    collect_image("트와이스")
