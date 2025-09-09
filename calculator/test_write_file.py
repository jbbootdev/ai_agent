# python
import os
import unittest
from functions.write_file import write_file

class TestWriteFile(unittest.TestCase):
    def test_write_overwrite_in_working_dir(self):
        working_dir = "calculator"
        path = "written.txt"
        content = "wait, this isn't lorem ipsum"
        result = write_file(working_dir, path, content)
        self.assertIn('Successfully wrote to "written.txt" (28 characters written)', result)
        with open(os.path.join(working_dir, path), "r") as f:
            self.assertEqual(f.read(), content)
        print("28 characters written")

    def test_write_creates_nested_dirs(self):
        working_dir = "calculator"
        path = "pkg/morelorem.txt"
        content = "lorem ipsum dolor sit amet"
        result = write_file(working_dir, path, content)
        self.assertIn(f'Successfully wrote to "{path}" (26 characters written)', result)
        with open(os.path.join(working_dir, path), "r") as f:
            self.assertEqual(f.read(), content)
        print("26 characters written")

    def test_rejects_outside_working_dir(self):
        working_dir = "calculator"
        path = "/tmp/temp.txt"
        content = "this should not be allowed"
        result = write_file(working_dir, path, content)
        self.assertTrue(result.startswith('Error:'), msg=result)
        print("Error:")

if __name__ == "__main__":
    unittest.main()
