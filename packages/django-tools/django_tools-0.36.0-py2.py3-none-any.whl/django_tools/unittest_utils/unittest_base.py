# coding: utf-8

"""
    unittest base
    ~~~~~~~~~~~~~

    :copyleft: 2009-2017 by the django-tools team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import unicode_literals, absolute_import, division, print_function


import os
import sys
import textwrap
import warnings

from django.contrib import auth
from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core import management

from django_tools.unittest_utils.user import create_user
from .BrowserDebug import debug_response


class BaseUnittestCase(TestCase):
    """
    Extensions to plain Unittest TestCase
    """
    def _dedent(self, txt):
        # Remove any common leading whitespace from every line
        txt = textwrap.dedent(txt)

        # strip whitespace at the end of every line
        txt = "\n".join([line.rstrip() for line in txt.splitlines()])
        txt = txt.strip()
        return txt

    def assertEqual_dedent(self, first, second, msg=None):
        first = self._dedent(first)
        second = self._dedent(second)
        try:
            self.assertEqual(first, second, msg)
        except AssertionError as err:
            # Py2 has a bad error message
            msg = (
                "%s\n"
                "------------- [first] -------------\n"
                "%s\n"
                "------------- [second] ------------\n"
                "%s\n"
                "-----------------------------------\n"
            ) % (err, first, second)
            raise AssertionError(msg)

    def assertIn_dedent(self, member, container, msg=None):
        member = self._dedent(member)
        container = self._dedent(container)
        try:
            self.assertIn(member, container, msg)
        except AssertionError as err:
            # Py2 has a bad error message
            msg = (
                "%s\n"
                "------------- [member] -------------\n"
                "%s\n"
                "----------- [container] ------------\n"
                "%s\n"
                "------------------------------------\n"
            ) % (err, member, container)
            raise AssertionError(msg)

    def assert_is_dir(self, path):
        if not os.path.isdir(path):
            self.fail('Directory "%s" doesn\'t exists!' % path)

    def assert_not_is_dir(self, path):
        if os.path.isdir(path):
            self.fail('Directory "%s" exists, but should not exists!' % path)

    def assert_is_file(self, path):
        if not os.path.isfile(path):
            self.fail('File "%s" doesn\'t exists!' % path)

    def assert_not_is_File(self, path):
        if os.path.isfile(path):
            self.fail('File "%s" exists, but should not exists!' % path)


class BaseTestCase(BaseUnittestCase):
    # Should we open a browser traceback?
    browser_traceback = True

    TEST_USERS = {
        "superuser": {
            "username": "superuser",
            "email": "superuser@example.org",
            "password": "superuser_password",
            "is_staff": True,
            "is_superuser": True,
        },
        "staff": {
            "username": "staff_test_user",
            "email": "staff_test_user@example.org",
            "password": "staff_test_user_password",
            "is_staff": True,
            "is_superuser": False,
        },
        "normal": {
            "username": "normal_test_user",
            "email": "normal_test_user@example.org",
            "password": "normal_test_user_password",
            "is_staff": False,
            "is_superuser": False,
        },
    }

    def _pre_setup(self):
        super(BaseTestCase, self)._pre_setup()

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        cls.UserModel = auth.get_user_model()

    def create_user(self, verbosity, **userdata):
        """
        Create a user and return the instance.
        """
        warnings.warn(
            "Old API! This will be removed in the future!"
            " Use: django_tools.unittest_utils.user.create_user()",
            FutureWarning,
            stacklevel=2
        )
        return create_user(**userdata)

    def create_testusers(self, verbosity=2):
        """
        Create all available testusers and UserProfiles
        """
        for userdata in list(self.TEST_USERS.values()):
            create_user(**userdata)

    def login(self, usertype):
        """
        Login the user defined in self.TEST_USERS
        return User model instance
        """
        test_user = self._get_userdata(usertype)

        count = self.UserModel.objects.filter(username=test_user["username"]).count()
        self.assertNotEqual(count, 0, "You have to call self.create_testusers() first!")
        self.assertEqual(count, 1)

        ok = self.client.login(username=test_user["username"],
                               password=test_user["password"])
        self.assertTrue(ok, 'Can\'t login test user "%s"!' % usertype)
        return self._get_user(usertype)

    def add_user_permissions(self, user, permissions):
        """
        add permissions to the given user instance.
        permissions e.g.: ("AppLabel.add_Modelname", "auth.change_user")
        """
        assert isinstance(permissions, (list, tuple))
        for permission in permissions:
            # permission, e.g: blog.add_blogentry
            app_label, permission_codename = permission.split(".", 1)
            model_name = permission_codename.split("_", 1)[1]

            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model_name)
            except ContentType.DoesNotExist:
                etype, evalue, etb = sys.exc_info()
                evalue = etype('Can\'t get ContentType for app "%s" and model "%s": %s' % (
                    app_label, model_name, evalue
                ))
                raise etype(evalue).with_traceback(etb)

            perm = Permission.objects.get(content_type=content_type, codename=permission_codename)
            user.user_permissions.add(perm)
            user.save()

        self.assertTrue(user.has_perms(permissions))

    def refresh_user(self, user):
        """
        Return a fresh User model instance from DB.
        Note: Using "user.refresh_from_db()" will not help in every case!
        e.g.: Add new permission on user group and check the added one.
        """
        return self.UserModel.objects.get(pk=user.pk)

    def _get_userdata(self, usertype):
        """ return userdata from self.TEST_USERS for the given usertype """
        try:
            return self.TEST_USERS[usertype]
        except KeyError as err:
            etype, evalue, etb = sys.exc_info()
            evalue = etype(
                'Wrong usetype %s! Existing usertypes are: %s' % (err, ", ".join(list(self.TEST_USERS.keys())))
            )
            raise etype(evalue).with_traceback(etb)

    def _get_user(self, usertype):
        """ return User model instance for the given usertype"""
        test_user = self._get_userdata(usertype)
        return self.UserModel.objects.get(username=test_user["username"])

    def _create_testusers(self):
        """ Create all available testusers. """
        def create_user(username, password, email, is_staff, is_superuser):
            """
            Create a user and return the instance.
            """
            defaults = {'password':password, 'email':email}
            User = auth.get_user_model()
            user, created = self.UserModel.objects.get_or_create(
                username=username, defaults=defaults
            )
            if not created:
                user.email = email
            user.set_password(password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
        for usertype, userdata in self.TEST_USERS.items():
            create_user(**userdata)

    def raise_browser_traceback(self, response, msg):
        debug_response(
            response, self.browser_traceback, msg, display_tb=False
        )
        msg += ' (url: "%s")' % response.request.get("PATH_INFO", "???")
        raise self.failureException(msg)

    def assertStatusCode(self, response, excepted_code=200):
        """
        assert response status code, if wrong, do a browser traceback.
        """
        if response.status_code == excepted_code:
            return # Status code is ok.
        msg = 'assertStatusCode error: "%s" != "%s"' % (response.status_code, excepted_code)
        self.raise_browser_traceback(response, msg)

    # def _assert_and_parse_html(self, html, user_msg, msg):
    #     """
    #     convert a html snippet into a DOM tree.
    #     raise error if snippet is no valid html.
    #     """
    #     try:
    #         return parse_html(html)
    #     except HTMLParseError as e:
    #         self.fail('html code is not valid: %s - code: "%s"' % (e, html))
    #
    # def _assert_and_parse_html_response(self, response):
    #     """
    #     convert html response content into a DOM tree.
    #     raise browser traceback, if content is no valid html.
    #     """
    #     try:
    #         return parse_html(response.content)
    #     except HTMLParseError as e:
    #         self.raise_browser_traceback(response, "Response's content is no valid html: %s' % e)

    def assertDOM(self, response, must_contain=(), must_not_contain=(), use_browser_traceback=True):
        """
        Asserts that html response contains 'must_contain' nodes, but no
        nodes from must_not_contain.
        """
        for txt in must_contain:
            try:
                self.assertContains(response, txt, html=True)
            except AssertionError as err:
                if use_browser_traceback:
                    self.raise_browser_traceback(response, err)
                raise

        for txt in must_not_contain:
            try:
                self.assertNotContains(response, txt, html=True)
            except AssertionError as err:
                if use_browser_traceback:
                    self.raise_browser_traceback(response, err)
                raise

    def assertResponse(self, response,
            must_contain=None, must_not_contain=None,
            status_code=200,
            template_name=None,
            html=False,
            browser_traceback=True):
        """
        Check the content of the response
        must_contain - a list with string how must be exists in the response.
        must_not_contain - a list of string how should not exists.
        """
        if must_contain is not None:
            for must_contain_snippet in must_contain:
                try:
                    self.assertContains(response, must_contain_snippet,
                        status_code=status_code, html=html
                    )
                except AssertionError as err:
                    if browser_traceback:
                        msg = 'Text not in response: "%s": %s' % (
                            must_contain_snippet, err
                        )
                        debug_response(
                            response, self.browser_traceback, msg, display_tb=True
                        )
                    raise

        if must_not_contain is not None:
            for must_not_contain_snippet in must_not_contain:
                try:
                    self.assertNotContains(response, must_not_contain_snippet,
                        status_code=status_code, html=html
                    )
                except AssertionError as err:
                    if browser_traceback:
                        msg = 'Text should not be in response: "%s": %s' % (
                            must_not_contain_snippet, err
                        )
                        debug_response(
                            response, self.browser_traceback, msg, display_tb=True
                        )
                    raise

        try:
            self.assertEqual(response.status_code, status_code)
        except AssertionError as err:
            if browser_traceback:
                msg = 'Wrong status code: %s' % err
                debug_response(
                    response, self.browser_traceback, msg, display_tb=True
                )
            raise

        if template_name is not None:
            try:
                self.assertTemplateUsed(response, template_name=template_name)
            except AssertionError as err:
                if browser_traceback:
                    msg = 'Template not used: %s' % err
                    debug_response(
                        response, self.browser_traceback, msg, display_tb=True
                    )
                raise

def direct_run(raw_filename):
    """
    Run a test direct from a unittest file.
    A unittest file should add something like this:

    if __name__ == "__main__":
        # Run this unittest directly
        direct_run(__file__)
    """
    appname = os.path.splitext(os.path.basename(raw_filename))[0]
    print('direct run "%s"' % appname)
    management.call_command('test', appname)

