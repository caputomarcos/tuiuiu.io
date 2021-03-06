from __future__ import absolute_import, unicode_literals

import logging

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_delete

from tuiuiu.tuiuiucore.models import Page, Site

logger = logging.getLogger('tuiuiu.core')


# Clear the tuiuiu_site_root_paths from the cache whenever Site records are updated.
def post_save_site_signal_handler(instance, update_fields=None, **kwargs):
    cache.delete('tuiuiu_site_root_paths')


def post_delete_site_signal_handler(instance, **kwargs):
    cache.delete('tuiuiu_site_root_paths')


def pre_delete_page_unpublish(sender, instance, **kwargs):
    # Make sure pages are unpublished before deleting
    if instance.live:
        # Don't bother to save, this page is just about to be deleted!
        instance.unpublish(commit=False)


def post_delete_page_log_deletion(sender, instance, **kwargs):
    logger.info("Page deleted: \"%s\" id=%d", instance.title, instance.id)


def register_signal_handlers():
    post_save.connect(post_save_site_signal_handler, sender=Site)
    post_delete.connect(post_delete_site_signal_handler, sender=Site)

    pre_delete.connect(pre_delete_page_unpublish, sender=Page)
    post_delete.connect(post_delete_page_log_deletion, sender=Page)
