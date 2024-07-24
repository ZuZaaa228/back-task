from django.db import connection
from django.test import TestCase, Client
from django.test.utils import CaptureQueriesContext


class MenuTests(TestCase):

    def test_menu_renders_with_one_query(self):
        """
        Проверка на количество запросов к базе данных
        :return:
        """
        client = Client()
        with CaptureQueriesContext(connection) as queries:
            client.get("/home/about/team/member-1/")
            client.get("/home/about/team/member-2/")
            client.get("/home/about/team/member-1/")
            client.get("/home/about/team/")
            client.get("/home/about/history/")
            client.get("/home/services/")
            client.get("/")  # Тут даст 2 запроса, т.к рендерит 2 меню: main_menu, secondary_menu

        print(f"SQL queries: {len(queries)}")
        self.assertEqual(len(queries), 8)
