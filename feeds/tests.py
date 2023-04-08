from django.test import TestCase
from django.utils import timezone
from .models import Article
from django.urls.base import reverse


class FeedsTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Some random article",
            description="A clearly random article",
            pub_date=timezone.now(),
            link="https://myawesomeshow.com",
            # image="https://image.myawesomeshow.com",
            journal_name="Random Journal",
            guid="de194720-7b4c-49e2-a05f-432436d3fetr",
        )

    def test_article_content(self):
        self.assertEqual(self.article.description, "Some random article")
        self.assertEqual(self.article.link, "https://myawesomeshow.com")
        self.assertEqual(self.article.guid, "de194720-7b4c-49e2-a05f-432436d3fetr")

    def test_article_str_representation(self):
        self.assertEqual(str(self.article), "Random Journal: Some random article")

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "homepage.html")

    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "Some random article")
