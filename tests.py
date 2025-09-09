from os import writev
import unittest


# python
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file

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

class TestRunPythonFile(unittest.TestCase):
    def test_rejects_outside_working_dir(self):
        msg = run_python_file("calculator", "../main.py")
        self.assertTrue(msg.startswith("Error: Cannot execute"), msg)

    def test_missing_python_file(self):
        msg = run_python_file("calculator", "nope.py")
        self.assertEqual('Error: File "nope.py" not found.', msg)

    def test_rejects_non_python_file(self):
        msg = run_python_file("calculator", "lorem.txt")
        self.assertEqual('Error: "lorem.txt" is not a Python file.', msg)

    def test_runs_python_and_formats_output(self):
        out = run_python_file("calculator", "main.py")
        self.assertIn("STDOUT:", out)
        if "Traceback" in out or "Error" in out:
            self.assertIs("STDERR:", out)



 # python
if __name__ == "__main__":
    import unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # include local tests
    suite.addTests(loader.loadTestsFromModule(__import__(__name__)))
    # include calculator tests
    suite.addTests(loader.discover(start_dir="calculator", pattern="test*.py"))
    runner = unittest.TextTestRunner()
    runner.run(suite)       

  # Ensure these get printed for the CLI check
    from functions.run_python_file import run_python_file
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))
