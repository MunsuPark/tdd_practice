from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from .views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expect_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expect_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        new_item_text = '신규 작업 아이템'
        request.POST['item_text'] = new_item_text

        response = home_page(request)

        self.assertIn(new_item_text, response.content.decode())
        expect_html = render_to_string(
            'home.html',
            {'new_item_text': new_item_text}
        )
        self.assertEqual(response.content.decode(), expect_html)
