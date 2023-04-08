from django.urls import path

from .views import HomePageView, SearchView, JournalView

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("<journal>", JournalView.as_view(), name="journal"),
    path("search/<keyword>/", SearchView.as_view(), name="search"),
]
