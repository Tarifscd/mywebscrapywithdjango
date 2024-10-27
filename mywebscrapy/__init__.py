from .celery import app as celery_app

__all__ = ('celery_app',)

# from srcap.tasks import scrapping
# r = scrapping()