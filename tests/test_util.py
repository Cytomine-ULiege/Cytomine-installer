

import os
from tempfile import TemporaryDirectory
from unittest import TestCase

from bootstrapper.util import list_relative_files, write_dotenv


class TestUtil(TestCase):
  def testWriteDotenv(self):
    envs = {
      "VAR1": "value1",
      "VAR2": "value2"
    }
    with TemporaryDirectory() as tmpdir:
      write_dotenv(tmpdir, envs)
      with open(os.path.join(tmpdir, ".env"), "r", encoding="utf8") as file:
        parsed_envs = {line.split("=", 1)[0]: line.strip().split("=", 1)[1] for line in file.readlines()}
    
    self.assertDictEqual(envs, parsed_envs)

  def testListRelativeFilesInvalidPath(self):
    with TemporaryDirectory() as tmpdir:
      self.assertEqual(len(list_relative_files(os.path.join(tmpdir, "aa"))), 0)
  
  def testListRelativeFilesEmptyPath(self):
    with TemporaryDirectory() as tmpdir:
      self.assertEqual(len(list_relative_files(tmpdir)), 0)

  def testListRelativeFilesOneFile(self):
    with TemporaryDirectory() as tmpdir:
      with open(os.path.join(tmpdir, "file1.txt"), "w"):
        pass
      relative = list_relative_files(tmpdir)
      self.assertEqual(len(relative), 1)
      self.assertEqual(relative[0], "file1.txt")

  def testListRelativeFilesSeveralFiles(self):
    with TemporaryDirectory() as tmpdir:
      files = ["file1.txt", "file2.txt"]
      for file in files:  
        with open(os.path.join(tmpdir, file), "w"):
          pass
      relative = list_relative_files(tmpdir)
      self.assertEqual(len(relative), 2)
      self.assertListEqual(sorted(files), sorted(relative))

  def testListRelativeFilesSeveralFilesAndFolders(self):
    with TemporaryDirectory() as tmpdir:
      dirs = ["dir1", "dir2"]
      for dirname in dirs:
        os.makedirs(os.path.join(tmpdir, dirname))
      files = ["dir1/file1.txt", "file2.txt"]
      for file in files:  
        with open(os.path.join(tmpdir, file), "w"):
          pass
      relative = list_relative_files(tmpdir)
      self.assertEqual(len(relative), 2)
      self.assertListEqual(sorted(files), sorted(relative))

    