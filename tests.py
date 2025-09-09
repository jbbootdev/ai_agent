import unittest


# python
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


class TestGetFileInfo(unittest.TestCase):
    def test_lists_pkg_dir(self):
        out = get_files_info("calculator", "pkg")
        self.assertIn("calculator.py", out)
    
    def test_rejects_outside_working_dir(self):
        result = get_files_info("calculator", "/bin")
        self.assertTrue(result.startswith("Error:"), msg=result)


class TestGetFileContent(unittest.TestCase):
    def test_reads_calculator_main(self):
        content = get_file_content("calculator", "main.py")
        self.assertIn("def main():", content)

    def test_reads_pkg_calculator(self):
        content = get_file_content("calculator", "pkg/calculator.py")
        self.assertIn("def _apply_operator(", content)

    def test_rejects_outside_working_dir(self):
        msg = get_file_content("calculator", "/bin/cat")
        self.assertTrue(msg.startswith("Error:"), msg)

    def test_missing_file(self):
        msg = get_file_content("calculator", "pkg/does_not_exist.py")
        self.assertTrue(msg.startswith("Error:"), msg)

    def test_truncates_long_file(self):
        content = get_file_content("calculator", "lorem.txt")
        self.assertTrue(len(content) > 10000)
        self.assertIn('truncated at 10000 characters', content)

        
if __name__ == "__main__":
    unittest.main(exit=False)

    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))  # should start with "Error:"
