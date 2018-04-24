import os

from selenium import webdriver

browser = webdriver.Chrome(
    os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        'chromedriver'))

# 웹사이트 확인

browser.get('http://localhost:8000')

# 웹페이지 타이틀에 'To-do' 있는지 확인
assert 'To-do' in browser.title

# 작업 추가하기

# "공작깃털 사기"라고 텍스트 상자에 입력

# 엔터키를 치면 페이지가 갱신되고 작업 목록에 "1: 공작깃털 사기" 아이템이 추가된다

# 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재

# 다시 "공작 깃털을 이용해서 그물 만들기" 라고 입력한다

# 페이지는 갱신되고, 두 개 아이템 목록이 보인다.

# 사이트가 입력한 목록을 보여주는 URL과 그에 대한 설명을 제공한다.

# 해당 URL에 접속하면 그녀가 만든 작업 목록이 그대로 있는 것을 확인
