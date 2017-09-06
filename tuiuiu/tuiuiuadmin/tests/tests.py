# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core import mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase, override_settings
from django.utils.translation import ugettext_lazy as _
from taggit.models import Tag

from tuiuiu.tests.utils import TuiuiuTestUtils
from tuiuiu.tuiuiuadmin.menu import MenuItem
from tuiuiu.tuiuiuadmin.site_summary import PagesSummaryItem
from tuiuiu.tuiuiuadmin.utils import send_mail, user_has_any_page_permission
from tuiuiu.tuiuiucore.models import Page, Site


class TestHome(TestCase, TuiuiuTestUtils):
    def setUp(self):
        # Login
        self.login()

    def test_simple(self):
        response = self.client.get(reverse('tuiuiuadmin_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the Test Site Tuiuiu CMS")

    def test_admin_menu(self):
        response = self.client.get(reverse('tuiuiuadmin_home'))
        self.assertEqual(response.status_code, 200)
        # check that media attached to menu items is correctly pulled in
        self.assertContains(
            response,
            '<script type="text/javascript" src="/static/testapp/js/kittens.js"></script>'
        )
        # check that custom menu items (including classname / attrs parameters) are pulled in
        self.assertContains(
            response,
            '<a href="http://www.tomroyal.com/teaandkittens/" class="icon icon-kitten" data-fluffy="yes">Kittens!</a>'
        )

        # Check that the explorer menu item is here, with the right start page.
        self.assertContains(
            response,
            'data-explorer-start-page="1"'
        )

        # check that is_shown is respected on menu items
        response = self.client.get(reverse('tuiuiuadmin_home') + '?hide-kittens=true')
        self.assertNotContains(
            response,
            '<a href="http://www.tomroyal.com/teaandkittens/" class="icon icon-kitten" data-fluffy="yes">Kittens!</a>'
        )

    def test_never_cache_header(self):
        # This tests that tuiuiuadmins global cache settings have been applied correctly
        response = self.client.get(reverse('tuiuiuadmin_home'))

        self.assertIn('private', response['Cache-Control'])
        self.assertIn('no-cache', response['Cache-Control'])
        self.assertIn('no-store', response['Cache-Control'])
        self.assertIn('max-age=0', response['Cache-Control'])

    def test_nonascii_email(self):
        # Test that non-ASCII email addresses don't break the admin; previously these would
        # cause a failure when generating Gravatar URLs
        get_user_model().objects.create_superuser(username='snowman', email='☃@thenorthpole.com', password='password')
        # Login
        self.assertTrue(self.client.login(username='snowman', password='password'))
        response = self.client.get(reverse('tuiuiuadmin_home'))
        self.assertEqual(response.status_code, 200)


class TestPagesSummary(TestCase, TuiuiuTestUtils):
    def setUp(self):
        self.login()

    def get_request(self):
        """
        Get a Django WSGI request that has been passed through middleware etc.
        """
        return self.client.get('/admin/').wsgi_request

    def test_page_summary_single_site(self):
        request = self.get_request()
        root_page = request.site.root_page
        link = '<a href="{}">'.format(reverse('tuiuiuadmin_explore', args=[root_page.pk]))
        page_summary = PagesSummaryItem(request)
        self.assertIn(link, page_summary.render())

    def test_page_summary_multiple_sites(self):
        Site.objects.create(
            hostname='example.com',
            root_page=Page.objects.get(pk=1))
        request = self.get_request()
        link = '<a href="{}">'.format(reverse('tuiuiuadmin_explore_root'))
        page_summary = PagesSummaryItem(request)
        self.assertIn(link, page_summary.render())

    def test_page_summary_zero_sites(self):
        Site.objects.all().delete()
        request = self.get_request()
        link = '<a href="{}">'.format(reverse('tuiuiuadmin_explore_root'))
        page_summary = PagesSummaryItem(request)
        self.assertIn(link, page_summary.render())


class TestEditorHooks(TestCase, TuiuiuTestUtils):
    def setUp(self):
        self.homepage = Page.objects.get(id=2)
        self.login()

    def test_editor_css_hooks_on_add(self):
        response = self.client.get(reverse('tuiuiuadmin_pages:add', args=('tests', 'simplepage', self.homepage.id)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<link rel="stylesheet" href="/path/to/my/custom.css">')

    def test_editor_js_hooks_on_add(self):
        response = self.client.get(reverse('tuiuiuadmin_pages:add', args=('tests', 'simplepage', self.homepage.id)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<script src="/path/to/my/custom.js"></script>')

    def test_editor_css_hooks_on_edit(self):
        response = self.client.get(reverse('tuiuiuadmin_pages:edit', args=(self.homepage.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<link rel="stylesheet" href="/path/to/my/custom.css">')

    def test_editor_js_hooks_on_edit(self):
        response = self.client.get(reverse('tuiuiuadmin_pages:edit', args=(self.homepage.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<script src="/path/to/my/custom.js"></script>')


class TestSendMail(TestCase):
    def test_send_email(self):
        send_mail("Test subject", "Test content", ["nobody@email.com"], "test@email.com")

        # Check that the email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test subject")
        self.assertEqual(mail.outbox[0].body, "Test content")
        self.assertEqual(mail.outbox[0].to, ["nobody@email.com"])
        self.assertEqual(mail.outbox[0].from_email, "test@email.com")

    @override_settings(TUIUIUADMIN_NOTIFICATION_FROM_EMAIL='anothertest@email.com')
    def test_send_fallback_to_tuiuiuadmin_notification_from_email_setting(self):
        send_mail("Test subject", "Test content", ["nobody@email.com"])

        # Check that the email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test subject")
        self.assertEqual(mail.outbox[0].body, "Test content")
        self.assertEqual(mail.outbox[0].to, ["nobody@email.com"])
        self.assertEqual(mail.outbox[0].from_email, "anothertest@email.com")

    @override_settings(DEFAULT_FROM_EMAIL='yetanothertest@email.com')
    def test_send_fallback_to_default_from_email_setting(self):
        send_mail("Test subject", "Test content", ["nobody@email.com"])

        # Check that the email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test subject")
        self.assertEqual(mail.outbox[0].body, "Test content")
        self.assertEqual(mail.outbox[0].to, ["nobody@email.com"])
        self.assertEqual(mail.outbox[0].from_email, "yetanothertest@email.com")

    def test_send_default_from_email(self):
        send_mail("Test subject", "Test content", ["nobody@email.com"])

        # Check that the email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test subject")
        self.assertEqual(mail.outbox[0].body, "Test content")
        self.assertEqual(mail.outbox[0].to, ["nobody@email.com"])
        self.assertEqual(mail.outbox[0].from_email, "webmaster@localhost")


class TestTagsAutocomplete(TestCase, TuiuiuTestUtils):
    def setUp(self):
        self.login()
        Tag.objects.create(name="Test", slug="test")

    def test_tags_autocomplete(self):
        response = self.client.get(reverse('tuiuiuadmin_tag_autocomplete'), {
            'term': 'test'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(data, ['Test'])

    def test_tags_autocomplete_partial_match(self):
        response = self.client.get(reverse('tuiuiuadmin_tag_autocomplete'), {
            'term': 'te'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(data, ['Test'])

    def test_tags_autocomplete_different_term(self):
        response = self.client.get(reverse('tuiuiuadmin_tag_autocomplete'), {
            'term': 'hello'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(data, [])

    def test_tags_autocomplete_no_term(self):
        response = self.client.get(reverse('tuiuiuadmin_tag_autocomplete'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, [])


class TestMenuItem(TestCase, TuiuiuTestUtils):
    def setUp(self):
        self.login()
        response = self.client.get(reverse('tuiuiuadmin_home'))
        self.request = response.wsgi_request

    def test_menuitem_reverse_lazy_url_pass(self):
        menuitem = MenuItem(_('Test'), reverse_lazy('tuiuiuadmin_home'))
        self.assertEqual(menuitem.is_active(self.request), True)


class TestUserPassesTestPermissionDecorator(TestCase):
    """
    Test for custom user_passes_test permission decorators.
    testapp_bob_only_zone is a view configured to only grant access to users with a first_name of Bob
    """
    def test_user_passes_test(self):
        # create and log in as a user called Bob
        get_user_model().objects.create_superuser(first_name='Bob', last_name='Mortimer', username='test', email='test@email.com', password='password')
        self.assertTrue(self.client.login(username='test', password='password'))

        response = self.client.get(reverse('testapp_bob_only_zone'))
        self.assertEqual(response.status_code, 200)

    def test_user_fails_test(self):
        # create and log in as a user not called Bob
        get_user_model().objects.create_superuser(first_name='Vic', last_name='Reeves', username='test', email='test@email.com', password='password')
        self.assertTrue(self.client.login(username='test', password='password'))

        response = self.client.get(reverse('testapp_bob_only_zone'))
        self.assertRedirects(response, reverse('tuiuiuadmin_home'))

    def test_user_fails_test_ajax(self):
        # create and log in as a user not called Bob
        get_user_model().objects.create_superuser(first_name='Vic', last_name='Reeves', username='test', email='test@email.com', password='password')
        self.assertTrue(self.client.login(username='test', password='password'))

        response = self.client.get(reverse('testapp_bob_only_zone'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)


class TestUserHasAnyPagePermission(TestCase):
    def test_superuser(self):
        user = get_user_model().objects.create_superuser(
            username='superuser', email='admin@example.com', password='p')
        self.assertTrue(user_has_any_page_permission(user))

    def test_inactive_superuser(self):
        user = get_user_model().objects.create_superuser(
            username='superuser', email='admin@example.com', password='p')
        user.is_active = False
        self.assertFalse(user_has_any_page_permission(user))

    def test_editor(self):
        user = get_user_model().objects.create_user(
            username='editor', email='ed@example.com', password='p')
        editors = Group.objects.get(name='Editors')
        user.groups.add(editors)
        self.assertTrue(user_has_any_page_permission(user))

    def test_moderator(self):
        user = get_user_model().objects.create_user(
            username='moderator', email='mod@example.com', password='p')
        editors = Group.objects.get(name='Moderators')
        user.groups.add(editors)
        self.assertTrue(user_has_any_page_permission(user))

    def test_no_permissions(self):
        user = get_user_model().objects.create_user(
            username='pleb', email='pleb@example.com', password='p')
        user.user_permissions.add(
            Permission.objects.get(content_type__app_label='tuiuiuadmin', codename='access_admin')
        )
        self.assertFalse(user_has_any_page_permission(user))
