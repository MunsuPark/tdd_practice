import os

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = self.get_chromedriver_borrower()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def get_chromedriver_borrower(self):
        return webdriver.Chrome(
            os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)),
                '../chromedriver')
        )

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_adn_retrieve_it_later(self):
        # 신규 사용자인 에디스가 웹사이트 확인
        self.browser.get(self.live_server_url)

        # 웹페이지 타이틀에 'To-do' 있는지 확인
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 작업 추가하기
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

        # "공작깃털 사기"라고 텍스트 상자에 입력
        inputbox.send_keys('공작깃털 사기')

        # 엔터키를 치면 페이지가 갱신되고 작업 목록에 "1: 공작깃털 사기" 아이템이 추가된다
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지 갱신, 두개의 아이템이 목록에 보임
        self.check_for_row_in_list_table('1: 공작깃털 사기')
        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')

        # 새로운 사용자인 프란시스가 사이트에 접속한다.

        # 새로운 브라우저 세션을 이용해서 에디스의 정보가
        # 쿠키를 통해 유입되는 것을 방지한다

        self.browser.quit()
        self.browser = self.get_chromedriver_borrower()

        # 프란시스가 홈페이지에 접속한다
        # 에디스의 리스트는 보이지 않는다.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        # 프란시스가 새로운 작업 아이템을 입력하기 시작한다
        # 그는 에디스보다 재미가 없다
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 URL을 취득한다.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 입력한 흔적이 없다는 것을 다시 확인한다
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)

        # 사이트가 입력한 목록을 보여주는 URL과 그에 대한 설명을 제공한다.

        # 해당 URL에 접속하면 그녀가 만든 작업 목록이 그대로 있는 것을 확인
