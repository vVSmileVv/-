import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.service import Service

# ====== 환경설정 ======
# 아이디/비밀번호는 환경변수 또는 직접 입력
DC_ID = os.environ.get('GALLOG_ID', '식별 코드 압력')
DC_PW = os.environ.get('GALLOG_PW', '비밀번호 입력')

# 삭제할 키워드 (빈 문자열이면 전체 삭제, 값이 있으면 해당 키워드 포함 글만 삭제)
KEYWORD = ''  # 예: '테스트' 또는 ''

# 삭제 간격(초)
DELETE_INTERVAL = 1

# =====================

# 크롬드라이버 로그 최소화
service = Service()

# 크롬드라이버 옵션 설정 (headless 모드 등)
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--lang=ko-KR')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--headless')  # 창을 띄우지 않으려면 주석 해제
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument('--mute-audio')

# 크롬드라이버 실행
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

total_attempt = 0

# 크롬의 비밀번호 유출 팝업 등 브라우저 자체 팝업이 뜨면 수동으로 닫아야 합니다.

try:
    # 1. 디시인사이드 메인 페이지 접속
    print('[INFO] 메인 페이지 접속 중...')
    browser.get('https://www.dcinside.com/')

    # 2. 아이디/비밀번호 입력 및 로그인 (메인에서 바로)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'user_id'))
    )
    browser.find_element(By.ID, 'user_id').send_keys(DC_ID)
    browser.find_element(By.ID, 'pw').send_keys(DC_PW)
    browser.find_element(By.ID, 'login_ok').click()
    print('[INFO] 로그인 시도 완료')
    time.sleep(3)

    # 3. 갤로그 방명록 페이지로 바로 이동
    print('[INFO] 방명록 페이지 접속 중...')
    browser.get(f'https://gallog.dcinside.com/{DC_ID}/guestbook')
    time.sleep(2)

    # 4. 방명록 삭제 반복 (키워드 조건 적용, 페이지네이션)
    while True:
        guestbook_items = browser.find_elements(By.CSS_SELECTOR, '#gb_comments > li')
        if not guestbook_items:
            print('[INFO] 더 이상 삭제할 방명록이 없습니다.')
            break

        found = False
        for item in guestbook_items:
            content = item.text
            preview = content[:30].replace('\n', ' ')
            if KEYWORD and KEYWORD not in content:
                print(f'[SKIP] 키워드 미포함: "{preview}" ...')
                continue
            try:
                delete_btns = item.find_elements(By.CSS_SELECTOR, '.btn_delete')
                if not delete_btns:
                    continue
                total_attempt += 1
                print(f'[TRY] {total_attempt}번째 삭제 시도: "{preview}" ...')
                delete_btns[0].click()
                try:
                    alert = browser.switch_to.alert
                    alert.accept()
                except NoAlertPresentException:
                    pass
                time.sleep(DELETE_INTERVAL)
                found = True
                break  # 삭제 후 목록을 새로 불러오기 위해 break
            except Exception:
                time.sleep(DELETE_INTERVAL)
                continue
        if found:
            continue  # 삭제가 일어나면 같은 페이지에서 다시 검사
        # 삭제할 대상이 없으면 다음 페이지로 이동
        try:
            current_page_elem = browser.find_element(By.CSS_SELECTOR, '.bottom_paging_box em')
            current_page = int(current_page_elem.text.strip())
            next_page_link = browser.find_element(By.XPATH, f'//div[contains(@class, "bottom_paging_box")]//a[text()="{current_page+1}"]')
            next_page_href = next_page_link.get_attribute('href')
            if not next_page_href:
                print('[INFO] 더 이상 다음 페이지가 없습니다.')
                break
            browser.get(next_page_href)
            time.sleep(2)
        except Exception:
            print('[INFO] 더 이상 다음 페이지가 없습니다.')
            break
    print('\n[RESULT] 방명록 청소 완료!')
finally:
    browser.quit()
