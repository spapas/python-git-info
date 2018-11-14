import unittest
import os
from gitinfo import get_git_info


class TestMethods(unittest.TestCase):
    def test_has_git(self):
        ret = get_git_info()
        self.assertTrue("commit" in ret)
        self.assertTrue("message" in ret)

    def test_doesnot_have_git(self):
        # The parent directory should *not* have a git file
        ret = get_git_info(os.path.dirname(os.getcwd()))
        self.assertEqual(ret, None)


if __name__ == "__main__":
    unittest.main()
