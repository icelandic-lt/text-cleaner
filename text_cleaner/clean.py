import argparse
import re
from text_cleaner import unicode_maps as umaps
from text_cleaner import constants as consts
from text_cleaner import emoji_dictionary as emoji_dicts

EMOJI_PATTERN = "\U0001f469|\u2764" # Temporary for testing TODO: Find a list with extensive coverage of emojis    

def update_replacement_dictionary(char_to_replace, replacement):
    """
    Adds the input char_to_replace to the collection of (character replacement) 
    dictionaries, as defined in unicode_maps.
    """
    dict = {}
    for cr in char_to_replace: 
        dict[cr] = replacement

    umaps.replacement_dictionary.update(dict)

def get_ice_alpha_replacement(char):
    if char in umaps.post_dict_lookup:
        for lookup_char in umaps.post_dict_lookup[char].lower():
            if lookup_char not in consts.character_alphabet:
                return ''
        
        return umaps.post_dict_lookup[char]
    return ''

def get_replacement(char):
    if char in umaps.replacement_dictionary:
        return umaps.replacement_dictionary[char]

def should_delete(char):
    return char in umaps.delete_chars_map

def clean_foreign_text_occurrence(token):
    token = token.replace("(e.", "<en>") # TODO: placeholder
    token = token.replace(")", " </en>")
    return token + ' '


def validate_characters(token, char_to_preserve):
    """
    Checks each character of the input word (token) to see if it matches any predefined character, as defined
    in constants or the second input 'char_to_preserve'.
    """
    for _, char in enumerate(token):
        repl = get_replacement(char)
        if repl:
            token = token.replace(char, repl)
        elif should_delete(char):
            token = token.replace(char, '')
        elif char in char_to_preserve:
            continue
        elif char.isdigit(): 
            continue
        elif char.lower() not in consts.character_alphabet and consts.punctuation_marks: 
            replacement = get_ice_alpha_replacement(char)
            if replacement:
                token = token.replace(char, replacement)
            elif (char == '(' or char == ')' or char == '"'):
                token = token.replace(char, ",")
            elif char not in consts.punctuation_marks and umaps.replacement_dictionary.values():
                token = token.replace(char, ' ')

    return token + ' '

def text_to_tokens(text):
    """
    Splits the input text at whitespaces into tokens. Exception is made within parenthesis to 
    simplify the cleaning process.
    """
    # the following regex demarks a string within parentheses (opening and closing parenthesis) 
    return re.split(r"\s(?![^(]*\))", text)

def clean(
    text,
    char_to_preserve=[],
    char_to_replace={},
    alphabet=[],
    punct_set=[],
    clean_emoji=True,
    clean_audiobook=False,
    replace_emoji_with='',
    replace_punct_with='',
):

    """
    Process (clean) the raw input text for NLP (Natural Language Processing) by removing 
    unhelpful and unusable data, as well as reducing noise.
    
    Text cleaning is task specific so multiple configurations are available.
    Args:
        text                : raw text for cleaning                       
        char_to_preserve    : list of char types forbidden to strip or convert
        char_to_replace     : dictionary of characters to convert     
        alphabet            : list of char that don't need converting     
        punct_set           : list of punctuation marks set to preserve
        clean_emoji         : if True, convert emojis to the value of "replace_emoji_with"
        replace_emoji_with  : str to replace emojis with        
        replace_punct_with  : str to replace punctuations with

    Returns:
        str: cleaned text based on function args
    """

    text = text_to_tokens(text)
    
    if char_to_replace:
        umaps.replacement_dictionary.update(char_to_replace)
    if punct_set:
        consts.punctuation_marks = punct_set
    if alphabet:
        consts.character_alphabet = alphabet
    if replace_punct_with:
        update_replacement_dictionary(consts.punctuation_marks, replace_punct_with)
    if clean_emoji:
        emoji_dicts.emoji_dict # TODO: compile into a pattern object

    cleaned_text = ''
    for token in text:
        # strip punctuation marks around the token before comparing against the char to 
        # preserve on the off chance that it's prefixed or followed by a punctuation mark. 
        if token.strip(r",.\?!:()") in char_to_preserve:
            cleaned_text += token + ' '
        # TODO: This get's reworked in an upcoming feature which introduces html_clean()
        elif token in consts.HTML_TAGS or token in consts.HTML_CLOSING_TAGS and not clean_audiobook:
            continue 
        # TODO: This get's reworked in an upcoming feature which introduces html_clean()
        elif token in consts.HTML_CLOSING_TAGS and clean_audiobook:
            cleaned_text += '. ' 
        # TODO: only covers english text atm and assumes it's prefixed be "(e." as is by convention
        elif token.startswith('(e.') and clean_audiobook: 
            token = clean_foreign_text_occurrence(token)
            cleaned_text += token
        else:
            cleaned_text += validate_characters(token, char_to_preserve)

    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text.strip()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="a text to be cleaned")
    args = parser.parse_args()
    
    return args.text

def main():
    text = parse_arguments()
    print(clean(text, 
                #char_to_preserve=['c'],
                #char_to_replace={'t': 's'},
                #alphabet=['a','b'],
                #punct_set=[',','.'],
                #clean_emoji=True,
                #replace_emoji_with="<emoji>",
                #replace_punct_with="  <punctuation>  ",
                ))

if __name__ == '__main__':
    main()
