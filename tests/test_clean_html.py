# This Python file uses the following encoding: utf-8
from text_cleaner import *


def test_regex():
    assert remove_whitespace_before_punctuation("hello world. . .") == "hello world..."
    assert remove_whitespace_before_punctuation("I'm not superstitious , but I am a little stitious ! ") == "I'm not superstitious, but I am a little stitious! "
    assert remove_whitespace_before_punctuation(" ! : ? . ,") == "!:?.,"
    assert remove_consecutive_punct_marks("hello world...") == "hello world."
    assert remove_consecutive_punct_marks("A day without sunshine is like, you know,. night.!?") == "A day without sunshine is like, you know, night."
    assert remove_consecutive_punct_marks("not quite consecutive. .") == "not quite consecutive. ."
    
def test_text_cleanup():
    assert tidy_up_text_format("Hello.  \n\n World.") == ("Hello. \n World.")
    assert tidy_up_text_format(".,\n   \n\n?   \n\n   .! :.") == "."
    assert tidy_up_text_format("Trying,  is the first! :step: toward failure.") == "Trying, is the first!step: toward failure."
