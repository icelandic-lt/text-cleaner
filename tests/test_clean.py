# This Python file uses the following encoding: utf-8
from text_cleaner import *

def test_default_clean():
    assert clean("π námundast í 3.14") == "pí námundast í 3.14"
    assert clean("we convert all 😎 emojis 😎 to .") == "ve konvert all . emojis . to ."
    assert clean("📌 red pin") == ". red pin"
    assert clean("ß Ø") == "ss Ö"
    assert clean("<p> HTML tög </p>") == "p HTML tög p"
    assert clean("raki (e. humidity)") == 'raki <lang xml:lang="en-GB"> humidity </lang>'
    assert clean("123") == "123"
    assert clean("(hello).") == ", hello ,"

def test_preserve_characters():
    assert clean("german 🐍: ßßß", preserve_emojis=True) == "german 🐍: ssssss"
    assert clean("π námundast í 3.14", preserve_string=['π']) == "π námundast í 3.14"
    assert clean("ß Ø", preserve_string=['ß']) == "ß Ö"
    assert clean("🤡😎🔥📌", preserve_string=['🤡','😎'], emoji_replacement='') == "🤡😎"
    assert clean("∫∬∭∮∯∰∱∲∳", preserve_string=['∫','∬','∭','∮','∯','∰','∱','∲','∳']) == "∫∬∭∮∯∰∱∲∳"
    assert clean("Zorro notar ekki hanzka", preserve_string=['Z']) == "Zorro notar ekki hanska"
    # characters stored in unicode_maps
    assert clean("gríski stafurinn \u03a4", preserve_string=['\u03a4']) == "gríski stafurinn \u03a4"
    assert clean("hebreski stafurinn \u05db", preserve_string=['\u05db']) == "hebreski stafurinn \u05db"
    assert clean("pólski stafurinn ł", preserve_string=['ł']) == "pólski stafurinn ł"
    # tokens to be preserved
    assert clean("z zz zzz zzzz", preserve_string=['zz']) == "s zz sss ssss"
    assert clean("z zz zzz zzzz", preserve_string=['zz', 'zzzz']) == "s zz sss zzzz"
    assert clean("Barizt hefur Zorro, margoft án hanzka", preserve_string=['Zorro']) == "Barist hefur Zorro, margoft án hanska"
    assert clean("(Zwoozh) er ekki ízlenzkt orð.", preserve_string=['Zwoozh']) == ", Zwoozh , er ekki íslenskt orð."
    
def test_clean_punctuation():
    # replace punct set
    assert clean(",.:!?", punct_set=[',','.']) == ","
    assert clean("?. ., ,.", punct_set=[',','.']) == "."

def test_clean_emoji():
    assert clean("🔥", clean_emojis=True) == "fire"
    assert clean("a 🧹 is used to play quidditch", clean_emojis=True) == "a broom is used to play kuidditkh"

def test_labelled_translations():
    assert clean("algengt er að skrifa Halló Heimur (e. Hello World)", delete_labelled_translations=True) == "algengt er að skrifa Halló Heimur"

def test_helper_functions():
    # tests both 'get_replacement' and 'should_delete' as well
    assert validate_characters("\u010c", [], False, False).strip() == "Tj" 
    assert validate_characters("\u05dc", [], False, False).strip() == ""
    assert validate_characters("\u03ba", [], False, False).strip() == "kappa" 
    assert validate_characters("×", [], False, False).strip() == ""
    # method tested is subject to change.
    assert labelled_translation_to_ssml("(e. Hello)") == '<lang xml:lang="en-GB"> Hello </lang> '
    assert labelled_translation_to_ssml("(e. Hello World)") == '<lang xml:lang="en-GB"> Hello World </lang> '
    assert labelled_translation_to_ssml("(e. kwartz)") == '<lang xml:lang="en-GB"> kwartz </lang> '
    # tests 'get_ice_alpha_replacement' as well
    assert validate_characters("(\")", [], False, False).strip() == ",  ,  ,"
    assert validate_characters("())(\"", [")", "\""], False, False).strip() == ", )) , \""
    assert validate_characters("cwartz", [], False, False).strip() == "kvarts"
    assert validate_characters("123", [], False, False).strip() == "123"

def test_replace_character():
    ## replacement configurations mutate the state of the cleaner 
    # replace punctuation
    assert clean("hello.", punct_replacement=' world') == "hello world"
    assert clean("..,,.,.,.,", punct_replacement='1') == "1111111111"
    assert clean(".", punct_replacement='\u03ae') == "\u03ae"
    # character replace
    assert clean("aábdð", char_replacement={'a': 'k'}) == "kábdð"
    assert clean("abdð", char_replacement={'ð': 'eéfghi'}) == "kbdeéfghi"
    # replace alphabet
    assert clean("aábdð", alphabet=['a','b','c','d']) == "k bdeéfghi"
    assert clean("abcdefghijklmnopqrstuvwxyz") == "bcd"

