# This Python file uses the following encoding: utf-8
from text_cleaner import *
import text_cleaner.unicode_maps as umaps


def test_default_clean():
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup)
    assert cleaner.clean("π námundast í 3.14") == "pí námundast í 3.14"
    assert cleaner.clean("we convert all 😎 emojis 😎 to .") == "ve konvert all . emojis . to ."
    assert cleaner.clean("📌 red pin") == ". red pin"
    assert cleaner.clean("ß Ø") == "ss Ö"
    # we should preserve tags at this stage, i.e. after the html parsing
    assert cleaner.clean("<p> HTML tög </p>") == "<p> HTML tög </p>"
    assert cleaner.clean("raki (e. humidity)") == 'raki <lang xml:lang="en-GB"> humidity </lang>'
    assert cleaner.clean("123") == "123"
    assert cleaner.clean("(hello).") == ", hello ,"
    assert cleaner.clean("Leikurinn fór 5-2 fyrir ÍA") == "Leikurinn fór 5-2 fyrir ÍA"
    assert cleaner.clean("Græn­lands­haf snemma í morg­un.") == "Grænlandshaf snemma í morgun."


def test_preserve_characters():
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup,
                          preserve_emojis=True, preserve_strings=['π', '🤡','😎', '∫','∬','∭','∮','∯','∰','∱',
                                                                  '∲','∳', 'Z', '\u03a4', '\u05db', 'ł', 'zz', 'zzzz', 'Zorro', 'Zwoozh'])
    assert cleaner.clean("german 🐍: ßßß") == "german 🐍: ssssss"
    assert cleaner.clean("π námundast í 3.14") == "π námundast í 3.14"
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup,
                          preserve_strings=['π', 'ß', '🤡', '😎', '∫', '∬', '∭', '∮', '∯', '∰', '∱',
                                            '∲', '∳', 'Z', '\u03a4', '\u05db', 'ł', 'zz', 'zzzz', 'Zorro', 'Zwoozh'])
    assert cleaner.clean("ß Ø") == "ß Ö"
    assert cleaner.clean("🤡😎🔥📌") == "🤡😎."
    assert cleaner.clean("∫∬∭∮∯∰∱∲∳") == "∫∬∭∮∯∰∱∲∳"
    assert cleaner.clean("Zorro notar ekki hanzka") == "Zorro notar ekki hanska"
    # characters stored in unicode_maps
    assert cleaner.clean("gríski stafurinn \u03a4") == "gríski stafurinn \u03a4"
    assert cleaner.clean("hebreski stafurinn \u05db") == "hebreski stafurinn \u05db"
    assert cleaner.clean("pólski stafurinn ł") == "pólski stafurinn ł"
    # tokens to be preserved
    assert cleaner.clean("z zz zzz zzzz") == "s zz sss zzzz"
    assert cleaner.clean("Barizt hefur Zorro, margoft án hanzka") == "Barist hefur Zorro, margoft án hanska"
    assert cleaner.clean("(Zwoozh) er ekki ízlenzkt orð.") == ", Zwoozh , er ekki íslenskt orð."
    
def test_clean_punctuation():
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup, punct_set=[',','.'])
    # replace punct set
    assert cleaner.clean(",.:!?") == ","
    assert cleaner.clean("?. ., ,.") == "."

def test_clean_emoji():
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup, describe_emojis=True)
    assert cleaner.clean("🔥") == "fire"
    assert cleaner.clean("a 🧹 is used to play quidditch") == "a broom is used to play kuidditkh"

def test_labelled_translations():
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup, delete_labelled_translations=True)
    assert cleaner.clean("algengt er að skrifa Halló Heimur (e. Hello World)") == "algengt er að skrifa Halló Heimur"

def test_helper_functions():
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup)
    # tests both 'get_replacement' and 'should_delete' as well
    assert cleaner.validate_characters("\u010c").strip() == "Tj"
    assert cleaner.validate_characters("\u05dc").strip() == ""
    assert cleaner.validate_characters("\u03ba").strip() == "kappa"
    assert cleaner.validate_characters("×").strip() == ""
    # method tested is subject to change.
    assert cleaner.clean_labelled_translation("(e. Hello)") == '<lang xml:lang="en-GB"> Hello </lang> '
    assert cleaner.clean_labelled_translation("(e. Hello World)") == '<lang xml:lang="en-GB"> Hello World </lang> '
    assert cleaner.clean_labelled_translation("(e. kwartz)") == '<lang xml:lang="en-GB"> kwartz </lang> '
    # tests 'get_ice_alpha_replacement' as well
    assert cleaner.validate_characters("(\")").strip() == ",  ,  ,"
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup, preserve_strings=[')', '"'])
    assert cleaner.validate_characters("())(\"").strip() == ", )) , \""
    assert cleaner.validate_characters("cwartz").strip() == "kvarts"
    assert cleaner.validate_characters("123").strip() == "123"

def test_replace_character():
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup, punct_replacement=' world')
    ## replacement configurations mutate the state of the cleaner 
    # replace punctuation
    assert cleaner.clean("hello.") == "hello world"
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup, punct_replacement='1')
    assert cleaner.clean("..,,.,.,.,") == "1111111111"
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup, punct_replacement='\u03ae')
    assert cleaner.clean(".") == "\u03ae"
    # character replace
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup,
                          char_replacement={'a': 'k', 'ð': 'eéfghi'})
    assert cleaner.clean("aábd") == "kábd"
    assert cleaner.clean("abdð") == "kbdeéfghi"
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup)
    assert cleaner.clean("abdð") == "abdð"
    # replace alphabet
    cleaner = TextCleaner(replacement_dict=umaps.replacement_dictionary, post_dict=umaps.post_dict_lookup,
                          char_replacement={'a': 'k', 'ð': 'eéfghi'}, alphabet=['a', 'b', 'c', 'd'])
    assert cleaner.clean("aábdð") == "kbdeéfghi"
    assert cleaner.clean("abcdefghijklmnopqrstuvwxyz") == "kbcdegikos"

