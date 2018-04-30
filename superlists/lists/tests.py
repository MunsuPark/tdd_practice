from django.core.urlresolvers import resolve, reverse
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

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': '신규 작업 아이템'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': '신규 작업 아이템'}
        )
        self.assertRedirects(response, reverse('view_list'))
