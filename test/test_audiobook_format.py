#from ..text_cleaner.main import main as m
from text_cleaner.main import clean

def test():
    assert clean("hi") == "hi"
    