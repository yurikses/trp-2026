from django.test import TestCase, override_settings


class ErrorPageTests(TestCase):
    @override_settings(DEBUG=False)
    def test_unknown_url_uses_custom_not_found_page(self):
        response = self.client.get('/page-that-does-not-exist/')

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Страница не найдена', status_code=404)
        self.assertContains(response, 'Вернуться на главную', status_code=404)
