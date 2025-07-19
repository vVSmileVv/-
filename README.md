# DCInside Gallog 방명록 자동 삭제기

디시인사이드 갤로그 방명록을 키워드 조건에 따라 자동으로 삭제하는 파이썬 스크립트입니다. Selenium 기반으로 크롬 브라우저를 자동 제어합니다.

---

## 사용법

### 1. 크롬드라이버 설치
- [크롬드라이버 다운로드](https://chromedriver.chromium.org/downloads)
- 본인 크롬 브라우저 버전에 맞는 드라이버를 설치하고, PATH에 추가하거나 스크립트와 같은 폴더에 두세요.

### 2. 파이썬 패키지 설치
```bash
pip install selenium
```

### 3. 환경설정
- `gallog cleaner.py` 상단에서 아래 항목을 설정하세요.

```python
DC_ID = os.environ.get('GALLOG_ID', '식별 코드 입력')
DC_PW = os.environ.get('GALLOG_PW', '비밀번호 입력')

# 삭제할 키워드 (빈 문자열이면 전체 삭제, 값이 있으면 해당 키워드 포함 글만 삭제)
KEYWORD = ''  # 예: '테스트' 또는 ''

# 삭제 간격(초)
DELETE_INTERVAL = 1
---

## 주요 옵션
- **KEYWORD**: 빈 문자열이면 전체 삭제, 값이 있으면 해당 키워드 포함 글만 삭제
- **DELETE_INTERVAL**: 삭제 시도 간격(초)
- **headless 모드**: 기본값은 headless(창 안뜸), 창을 띄우고 싶으면 `chrome_options.add_argument('--headless')` 부분을 주석 처리

---

## 주의사항
- 크롬의 비밀번호 유출 팝업 등 브라우저 자체 팝업이 뜨면 자동화가 멈출 수 있습니다. (수동으로 닫아주세요)
- 너무 빠른 삭제는 서버에서 비정상 요청으로 간주될 수 있으니, 삭제 간격을 너무 짧게 설정하지 마세요(1초 이상 권장).
- 크롬드라이버와 크롬 브라우저 버전이 맞지 않으면 실행이 안 될 수 있습니다.
- 2차 인증이 활성화 되어있으면 작동하지 않습니다.
