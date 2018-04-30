from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item
from lists.views import home_page


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

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the_only_list_in_the_world/')

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        new_item_text = '신규 작업 아이템'
        request.POST['item_text'] = new_item_text

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the_only_list_in_the_world/')

    def test_home_page_only_saves_items_when_POST(self):
        request = HttpRequest()
        home_page(request)

        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        Item.objects.create(text='첫번째 아이템')
        Item.objects.create(text='두번째 아이템')

        self.assertIsNotNone(Item.objects.get(text='첫번째 아이템'))
        self.assertIsNotNone(Item.objects.get(text='두번째 아이템'))


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the_only_list_in_the_world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the_only_list_in_the_world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
