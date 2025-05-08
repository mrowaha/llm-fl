analyze_coverage_prompt = """
<your role>
You will shorten the text of a file provided to you based on certain rules.
This will be a partial python file.
As a text shortner, you will not attempt to fix the code but are restricted to following:
1. You will remove empty functions from the code. Empty functions are functions that have no body or only have comments or docstring
2. if you see empty class methods, remove them in the same way as you removed functions. If you remove all the
class methods, remove that class too

<example>
input: 
def pytest_addoption(parser):
    group = parser.getgroup("thefuck")
    group.addoption('--enable-functional', action="store_true", default=False,
                    help="Enable functional tests")
@pytest.fixture
def no_memoize(monkeypatch):

def foo(monkeypatch):
  \""" foo has no body but only this comment \"""
output:
def pytest_addoption(parser):
    group = parser.getgroup("thefuck")
    group.addoption('--enable-functional', action="store_true", default=False,
                    help="Enable functional tests")

explanation:
no_memoize function had no function body so it was removed
foo function had nothing but docstring so it was also removed
</example>
Wrap your answer inside <file_content> </file_content> tags
</your role>
"""
