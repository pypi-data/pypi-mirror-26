import os, tempfile, shutil, mock, six
from django.contrib import messages
from django.test import TestCase, override_settings

from awl.waelsteng import AdminToolsMixin, messages_from_response

from awl.tests.admin import LinkAdmin
from awl.tests.models import Link
from awl.waelsteng import WRunner

# ============================================================================

class AdminToolsMixinTest(TestCase, AdminToolsMixin):
    def setUp(self):
        self.initiate()

    def test_mixin(self):
        link1 = Link.objects.create(url='/admin/', text='Admin')
        link2 = Link.objects.create(url='', text='Blank')
        link_admin = LinkAdmin(Link, self.site)

        self.authed_get('/admin/')
        self.authed_post('/admin/', {})

        expected = ('url', 'text', 'visit_me')
        self.assertEqual(expected, self.field_names(link_admin))
        self.assertEqual('Admin', self.field_value(link_admin, link1, 'text'))

        self.visit_admin_link(link_admin, link1, 'visit_me')
        with self.assertRaises(AttributeError):
            self.visit_admin_link(link_admin, link2, 'visit_me')


    def test_coverage(self):
        # miscellaneous pieces to get our coverage to 100%

        # test before get, to check that auth call worked
        self.authed_post('/admin/', {})

    def assert_messages(self, contents):
        self.assertEqual(2, len(contents))
        self.assertEqual('One', contents[0][0])
        self.assertEqual(messages.SUCCESS, contents[0][1])
        self.assertEqual('Two', contents[1][0])
        self.assertEqual(messages.ERROR, contents[1][1])

    def test_messages_from_response(self):
        response = self.authed_get('/awl_test_views/test_view_for_messages/')

        m = messages_from_response(response)
        self.assert_messages(m)

        # -- test handling with cookies

        # wipe out the context, so that the cookie that was set is what gets
        # processed
        response.context = None

        m = messages_from_response(response)
        self.assert_messages(m)

        # -- test handling bad response objects
        response.cookies.pop('messages')
        m = messages_from_response(response)
        self.assertEqual(0, len(m))

        # object without context
        m = messages_from_response({})
        self.assertEqual(0, len(m))

        # object with context but empty
        class Dummy(object):
            pass

        d = Dummy()
        d.context = {}
        m = messages_from_response(d)
        self.assertEqual(0, len(m))

        # object with context without messages key
        d.context = {'foo':'bar'}
        m = messages_from_response(d)
        self.assertEqual(0, len(m))

# ============================================================================

# dummy objects and settings for testing the runner
class GotHere(Exception):
    pass

def fake_loader():
    raise GotHere()

wrunner_settings = {
    'TEST_DATA':'awl.tests.test_waelsteng.fake_loader',
}

class WRunnerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()
        cls.media_dir = os.path.abspath(os.path.join(cls.tempdir, 'media'))

    def assert_test_strings(self, expected, tests):
        names = [str(test) for test in tests]
        self.assertEqual(set(expected), set(names))

    @override_settings(WRUNNER=wrunner_settings)
    def test_runner(self):
        global wrunner_settings
        wrunner_settings['MEDIA_ROOT'] = self.media_dir

        # this is going to get ugly... we're using the runner right now, so to
        # test the nooks and crannies we have create another one; django, as
        # of 1.11 doesn't like you to do this, so we'll mock out super() to
        # stop the parent from getting invoked

        name = '%s.super' % six.moves.builtins.__name__
        with mock.patch(name):
            fake_runner = WRunner()

            # check media root handling
            fake_runner.setup_test_environment()
            self.assertTrue(os.path.isdir(self.media_dir))

            # do it again to make sure directory already existing doesn't blow
            # anything up 
            fake_runner.setup_test_environment()

            # check test loader
            with self.assertRaises(GotHere):
                fake_runner.setup_databases()

            # -- check media root cleanup
            fake_runner.teardown_databases(old_config=[])
            self.assertFalse(os.path.exists(self.media_dir))

        # the ugliness continues! to test the building test suites we need a
        # real, not faked out, runner, so now we'll create one that isn't
        # mocked out

        real_runner = WRunner()

        # -- test various labels work
        expected = [
            'test_same_order (awl.tests.test_ranked.GroupedTests)',
            'test_same_order (awl.tests.test_ranked.AloneTests)',
            'test_too_large (awl.tests.test_ranked.GroupedTests)',
        ]
        suite = real_runner.build_suite([
            'awl.tests.test_ranked.GroupedTests.test_too_large',
            '=_same_order'])
        self.assert_test_strings(expected, suite)

        # shortcuts only
        expected = [
            'test_same_order (awl.tests.test_ranked.GroupedTests)',
            'test_same_order (awl.tests.test_ranked.AloneTests)',
        ]
        suite = real_runner.build_suite(['=_same_order'])
        self.assert_test_strings(expected, suite)

        # test no labels at all
        suite = real_runner.build_suite([])
        self.assertTrue(list(suite))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)
