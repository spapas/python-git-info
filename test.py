import unittest
import os
import gitinfo


class TestMethods(unittest.TestCase):
    def test_has_git(self):
        ret = gitinfo.get_git_info()
        self.assertTrue("commit" in ret)
        self.assertTrue("message" in ret)

    def test_doesnot_have_git(self):
        # The parent directory should *not* have a git file
        ret = gitinfo.get_git_info(os.path.dirname(os.getcwd()))
        self.assertEquals(ret, None)


if __name__ == "__main__":
    unittest.main()
