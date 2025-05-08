analyze_coverage_prompt = """
This will be a partial python file.
As a text shortner, you will not attempt to fix the code but are restricted to following:
1. You will remove empty functions from the code. Empty functions are functions that have no body or have pass or only have comments or docstring
2. if you see empty class methods, remove them in the same way as you removed functions. If you remove all the
class methods, remove that class too

<example>
- input: 
def pytest_addoption(parser):
    group = parser.getgroup("thefuck")

@pytest.fixture
def no_memoize(monkeypatch):

def foo():
  \""" foo has no body but only this comment \"""

def bar():
    pass

- output:
def pytest_addoption(parser):
    group = parser.getgroup("thefuck")
    group.addoption('--enable-functional', action="store_true", default=False,
                    help="Enable functional tests")

explanation:
no_memoize function had no function body so it was removed
foo function had nothing but docstring so it was also removed
bar function removed because it had only 'pass' in its body
</example>
Wrap your answer inside <file_content> </file_content> tags
"""

keep_definitions_prompt = """
You will receive an incomplete python file and a list of definitions.
As a text shortner, you will not attempt to fix the code but are restricted to following:
<restrictions>
- keep all import statements in the file that import any of the listed definitions
- if the definitions are not imported (and are defined inside the script), keep those definitions
- otherwise remove all other definitions
</restrictions>

Wrap your answer inside <file_content> </file_content> tags
"""
