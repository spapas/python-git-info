import unittest
import os
from gitinfo import get_git_info


class TestMethods(unittest.TestCase):
    def test_has_git(self):
        ret = get_git_info()
        self.assertTrue("commit" in ret)
        self.assertTrue("message" in ret)
        self.assertTrue("refs" in ret)

    def test_message_not_empty(self):
        ret = get_git_info()
        self.assertTrue(len(ret["message"]) > 0)

    def test_has_gitdir(self):
        ret = get_git_info()
        self.assertTrue("gitdir" in ret)
        self.assertTrue(os.path.dirname(ret["gitdir"]) == os.getcwd())

    def test_doesnot_have_git(self):
        # The parent directory should *not* have a git file
        with self.assertLogs("gitinfo.gitinfo", level="WARNING") as cm:
            ret = get_git_info(os.path.dirname(os.getcwd()))
            self.assertEqual(ret, None)
            self.assertIn("No git dir found", cm.output[0])

    def test_should_work_with_relative_paths(self):
        # The parent directory should *not* have a git file
        # Should work with ..
        with self.assertLogs("gitinfo.gitinfo", level="WARNING") as cm:
            ret = get_git_info("..")
            self.assertEqual(ret, None)
            self.assertIn("No git dir found", cm.output[0])

    def test_should_not_crash_with_emtpy_git_dir(self):
        # Create a dir named named empty_git and run git init there to test this
        if os.path.isdir("empty_git"):
            ret = get_git_info("empty_git")
            self.assertEqual(ret, None)

    def test_packed(self):
        ret = get_git_info("../../c/git")
        self.assertTrue("commit" in ret)
        self.assertTrue("message" in ret)
        self.assertTrue("refs" in ret)


if __name__ == "__main__":
    unittest.main()
