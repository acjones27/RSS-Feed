from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector

from .models import Article
from django.db.models import Q


class HomePageView(ListView):
    template_name = "homepage.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter().order_by("-pub_date")
        return context


class JournalView(ListView):
    template_name = "journal.html"
    model = Article

    def get_queryset(self):
        self.journal = self.kwargs["journal"]
        return Article.objects.filter().order_by("-pub_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter(
            journal_name__contains=self.journal
        ).order_by("-pub_date")
        context["journal"] = self.journal
        return context


class SearchView(ListView):
    template_name = "search.html"
    model = Article

    def get_queryset(self):
        self.keyword = self.kwargs["keyword"]
        return Article.objects.filter().order_by("-pub_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtered_articles"] = Article.objects.filter(
            Q(title__contains=self.keyword) | Q(description__contains=self.keyword)
        ).order_by("-pub_date")
        context["keyword"] = self.keyword
        return context
