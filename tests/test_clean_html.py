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

def test_html_parse():
    html_cleaner = HtmlCleaner()
    result = html_cleaner.clean_html(get_html_string())
    assert result
    assert result.find('</') == -1
    assert result.find('(e.') > 1


def get_html_string():
    return '<p id="hix00274"><span id="qitl_0591" class="sentence">Í kjölfarið sýndi hann fram á að það stuðli að ' \
               'heilbrigði ef einstaklingar geti fundið samhengi í tengslum við lífsatburði eða öðlast skilning á aðstæðum sínum. ' \
               '</span><span id="qitl_0592" class="sentence">Hann taldi uppsprettu heilbrigðis ' \
               '(e. </span><em><span id="qitl_0593" class="sentence">salutogenesis)</span></em><span id="qitl_0594" class="sentence"> ' \
               'vera að finna í mismunandi hæfni einstaklinga til að stjórna viðbrögðum sínum við álagi. </span>' \
               '<span id="qitl_0595" class="sentence">Antonovsky sýndi fram á að ef einstaklingar sem upplifðu álag sæju ' \
               'tilgang með reynslu sinni, þá þróaðist með þeim tilfinning fyrir samhengi í lífinu ' \
               '(e. </span><em><span id="qitl_0596" class="sentence">sense of coherence).</span></em>' \
               '<span id="qitl_0597" class="sentence"> Sigrún Gunnarsdóttir hefur íslenskað skilgreiningu hugtaksins ' \
               'um tilfinningu fyrir samhengi í lífinu á eftirfarandi hátt: </span></p>'
