import re
from text_cleaner import clean

def test_default_clean():
    assert clean.clean("π námundast í 3.14") == "pí námundast í 3.14"
    assert clean.clean("we strip all 😎 emojis 😎") == "ve strip all emojis"
    assert clean.clean("📌 red pin") == "red pin"
    assert clean.clean("ß Ø") == "ss Ö"
    assert clean.clean("<p> HTML tög </p>") == "HTML tög"
    assert clean.clean("raki (e. humidity)") == "raki ,e. humidity,"

def test_preserve_characters():
    assert clean.clean("π námundast í 3.14", char_to_preserve=['π']) == "π námundast í 3.14"
    assert clean.clean("ß Ø", char_to_preserve=['ß']) == "ß Ö"
    assert clean.clean("🤡😎🔥📌", char_to_preserve=['🤡','😎']) == "🤡😎"
    assert clean.clean("∫∬∭∮∯∰∱∲∳", char_to_preserve=['∫','∬','∭','∮','∯','∰','∱','∲','∳']) == "∫∬∭∮∯∰∱∲∳"
    
    #  characters stored in unicode_maps
    assert clean.clean("gríski stafurinn \u03a4", char_to_preserve=['\u03a4']) == "gríski stafurinn \u03a4"
    assert clean.clean("hebreski stafurinn \u05db", char_to_preserve=['\u05db']) == "hebreski stafurinn \u05db"
    assert clean.clean("pólski stafurinn ł", char_to_preserve=['ł']) == "pólski stafurinn ł"

    # tokens to be preserved
    assert clean.clean("z zz zzz zzzz", char_to_preserve=['zz']) == "s zz sss ssss"
    assert clean.clean("z zz zzz zzzz", char_to_preserve=['zz', 'zzzz']) == "s zz sss zzzz"
    assert clean.clean("Zorro notar ekki hanzka", char_to_preserve=['Z']) == "Zorro notar ekki hanska"
    assert clean.clean("Barizt hefur Zorro margoft án hanzka", char_to_preserve=['Zorro']) == "Barist hefur Zorro margoft án hanska"
    
 