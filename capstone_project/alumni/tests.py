from django.test import TestCase #  subclass of unittest.TestCase

from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from alumni import models
# Create your tests here.

# NB - Note that the Django test framework creates a separate, blank set of database tables for testing (i.e. "runs each test inside a transaction to provide isolation" in the 1.8 docs)
# i.e. making new DB objects just for testing purposes can be done freely since they won't foul up the database!

# Reference: https://docs.djangoproject.com/en/1.8/topics/testing/overview/

class ForumTestCase(TestCase):
    def set_up(self):
        testcase_user = User.create(name = "SCMHUCK")
        # forum, thread, post
        testcase_forum = models.Forum.create(title = "FORUMTESTCASE-FORUM")
        testcase_thread_one = models.Thread.create(title = "FORUMTESTCASE-THREAD-ONE", forum = testcase_forum.pk, creating_user = testcase_user)
        testcase_thread_two = models.Thread.create(title = "FORUMTESTCASE-THREAD-TWO", forum = testcase_forum.pk, creating_user = testcase_user)
        testcase_post_one = models.Post.create(title = "FORUMTESTCASE-POST", thread = testcase_thread_one.pk, creating_user = testcase_user, text ="post-one")
        testcase_post_two = models.Post.create(title = "FORUMTESTCASE-POST", thread = testcase_thread_two.pk, creating_user = testcase_user, text ="post-two")
        testcase_post_three = models.Post.create(title = "FORUMTESTCASE-POST", thread = testcase_thread_two.pk, creating_user = testcase_user, text ="post-three")
    '''When you run your tests, the default behavior of the test utility is to find all the test cases 
    (that is, subclasses of unittest.TestCase) in any file **whose name begins with test**, automatically build a test suite out of those test cases, and run that suite.'''
    def test_get_num_post_functions(self):
        self.assertEqual(testcase_forum.get_num_posts(),3)
        self.assertEqual(testcase_thread_one.get_num_posts(),1)
        self.assertEqual(testcase_thread_one.get_num_posts(),2)


