# This Python file uses the following encoding: utf-8
from text_cleaner import clean

def test_default_clean():
    assert clean.clean("π námundast í 3.14") == "pí námundast í 3.14"
    assert clean.clean("we convert all 😎 emojis 😎 to .") == "ve konvert all . emojis . to ."
    assert clean.clean("📌 red pin") == ". red pin"
    assert clean.clean("ß Ø") == "ss Ö"
    assert clean.clean("<p> HTML tög </p>") == "p HTML tög p"
    assert clean.clean("raki (e. humidity)") == 'raki <lang xml:lang="en-GB"> humidity </lang>'
    assert clean.clean("123") == "123"
    assert clean.clean("(hello).") == ", hello ,"

def test_preserve_characters():
    assert clean.clean("german 🐍: ßßß", preserve_emojis=True) == "german 🐍: ssssss"
    assert clean.clean("π námundast í 3.14", preserve_string=['π']) == "π námundast í 3.14"
    assert clean.clean("ß Ø", preserve_string=['ß']) == "ß Ö"
    assert clean.clean("🤡😎🔥📌", preserve_string=['🤡','😎'], emoji_replacement='') == "🤡😎"
    assert clean.clean("∫∬∭∮∯∰∱∲∳", preserve_string=['∫','∬','∭','∮','∯','∰','∱','∲','∳']) == "∫∬∭∮∯∰∱∲∳"
    assert clean.clean("Zorro notar ekki hanzka", preserve_string=['Z']) == "Zorro notar ekki hanska"
    # characters stored in unicode_maps
    assert clean.clean("gríski stafurinn \u03a4", preserve_string=['\u03a4']) == "gríski stafurinn \u03a4"
    assert clean.clean("hebreski stafurinn \u05db", preserve_string=['\u05db']) == "hebreski stafurinn \u05db"
    assert clean.clean("pólski stafurinn ł", preserve_string=['ł']) == "pólski stafurinn ł"
    # tokens to be preserved
    assert clean.clean("z zz zzz zzzz", preserve_string=['zz']) == "s zz sss ssss"
    assert clean.clean("z zz zzz zzzz", preserve_string=['zz', 'zzzz']) == "s zz sss zzzz"
    assert clean.clean("Barizt hefur Zorro, margoft án hanzka", preserve_string=['Zorro']) == "Barist hefur Zorro, margoft án hanska"
    assert clean.clean("(Zwoozh) er ekki ízlenzkt orð.", preserve_string=['Zwoozh']) == ", Zwoozh , er ekki íslenskt orð."
    
def test_clean_punctuation():
    # replace punct set
    assert clean.clean(",.:!?", punct_set=[',','.']) == ","
    assert clean.clean("?. ., ,.", punct_set=[',','.']) == "."

def test_clean_emoji():
    assert clean.clean("🔥", clean_emojis=True) == "fire"
    assert clean.clean("a 🧹 is used to play quidditch", clean_emojis=True) == "a broom is used to play kuidditkh"

def test_labelled_translations():
    assert clean.clean("algengt er að skrifa Halló Heimur (e. Hello World)", delete_labelled_translations=True) == "algengt er að skrifa Halló Heimur"

def test_helper_functions():
    # tests both 'get_replacement' and 'should_delete' as well
    assert clean.validate_characters("\u010c", [], False, False).strip() == "Tj" 
    assert clean.validate_characters("\u05dc", [], False, False).strip() == ""
    assert clean.validate_characters("\u03ba", [], False, False).strip() == "kappa" 
    assert clean.validate_characters("×", [], False, False).strip() == ""
    # method tested is subject to change.
    assert clean.labelled_translation_to_ssml("(e. Hello)") == '<lang xml:lang="en-GB"> Hello </lang> '
    assert clean.labelled_translation_to_ssml("(e. Hello World)") == '<lang xml:lang="en-GB"> Hello World </lang> '
    assert clean.labelled_translation_to_ssml("(e. kwartz)") == '<lang xml:lang="en-GB"> kwartz </lang> '
    # tests 'get_ice_alpha_replacement' as well
    assert clean.validate_characters("(\")", [], False, False).strip() == ",  ,  ,"
    assert clean.validate_characters("())(\"", [")", "\""], False, False).strip() == ", )) , \""
    assert clean.validate_characters("cwartz", [], False, False).strip() == "kvarts"
    assert clean.validate_characters("123", [], False, False).strip() == "123"

def test_replace_character():
    ## replacement configurations mutate the state of the cleaner 
    # replace punctuation
    assert clean.clean("hello.", punct_replacement=' world') == "hello world"
    assert clean.clean("..,,.,.,.,", punct_replacement='1') == "1111111111"
    assert clean.clean(".", punct_replacement='\u03ae') == "\u03ae"
    # character replace
    assert clean.clean("aábdð", char_replacement={'a': 'k'}) == "kábdð"
    assert clean.clean("abdð", char_replacement={'ð': 'eéfghi'}) == "kbdeéfghi"
    # replace alphabet
    assert clean.clean("aábdð", alphabet=['a','b','c','d']) == "k bdeéfghi"
    assert clean.clean("abcdefghijklmnopqrstuvwxyz") == "bcd"

