# Standard Library
import logging

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Third Party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from feeds.models import Article
from dateutil.tz import gettz
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


logger = logging.getLogger(__name__)


def get_article_image(url):
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(request_site)
    soup = BeautifulSoup(response)
    images = []
    for img in soup.findAll("img"):
        images.append(img.get("src"))

    # from selenium import webdriver

    # # import time
    # from selenium.webdriver.chrome.options import Options

    # options = Options()
    # options.headless = True
    # driver = webdriver.Chrome(
    #     options=options, executable_path="/opt/homebrew/bin/chromedriver"
    # )
    # driver.get(url)
    # images = driver.find_elements("tag name", "img")
    # images = [image.get_attribute("src") for image in images]

    images = [
        image
        for image in images
        if (image.startswith("http")) and ((".png" in image) or (".jpg" in image))
    ]
    if len(images) == 0:
        return ""
    return images[0]


def save_new_articles(feed):
    """Saves new articles to the database.

    Checks the article GUID against the articles currently stored in the
    database. If not found, then a new `Article` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    journal_title = feed.channel.title

    for item in feed.entries:
        if not Article.objects.filter(guid=item.link).exists():
            tzinfos = {"UTC": gettz("Europe/Zurich")}
            episode = Article(
                title=item.title,
                description=item.summary,
                pub_date=parser.parse(item.updated, tzinfos=tzinfos, dayfirst=False),
                link=item.link,
                image=get_article_image(item.link),
                journal_name=journal_title,
                guid=item.link,
            )
            episode.save()


def fetch_nature():
    """Fetches new episodes from RSS for Nature."""
    _feed = feedparser.parse("https://www.nature.com/nature.rss")
    save_new_articles(_feed)


def fetch_science():
    """Fetches new episodes from RSS for Nature Materials."""
    _feed = feedparser.parse("https://www.science.org/rss/news_current.xml")
    save_new_articles(_feed)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_nature,
            trigger="interval",
            minutes=2,
            id="Nature",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Nature.")

        scheduler.add_job(
            fetch_science,
            trigger="interval",
            minutes=2,
            id="Science",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Science.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")


def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
