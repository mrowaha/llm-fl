import pytest
from myproject.foo import bar
from myproject.bar import foo

@pytest.mark.parametrize('input', [
    ('foo')
])
def test_get_foo(input):
    output = foo()
    assert(output == input)