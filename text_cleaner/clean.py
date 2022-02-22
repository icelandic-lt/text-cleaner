import argparse, sys
import re
from text_cleaner import unicode_maps as umaps
from text_cleaner import constants as consts
from text_cleaner import emoji_dictionary 

def update_replacement_dictionary(char_to_replace, replacement) -> None:
    """
    Adds the input char_to_replace to the collection of character 
    replacement dictionaries, as defined in unicode_maps.
    """
    dict = {}
    for cr in char_to_replace: 
        dict[cr] = replacement

    umaps.replacement_dictionary.update(dict)


def replace_or_drop(char, token) -> str:
    replacement = get_ice_alpha_replacement(char)
    if replacement:
        token = token.replace(char, replacement)
    elif (char == '(' or char == ')' or char == '"'):
        token =  token.replace(char, " , ")
    elif char not in consts.punctuation_marks and char not in umaps.replacement_dictionary.values():
        token = token.replace(char, ' ')
    
    return token


def get_ice_alpha_replacement(char) -> str:
    if char in umaps.post_dict_lookup:
        # validate the character returned by post_dict_lookup
        for lookup_char in umaps.post_dict_lookup[char].lower(): 
            if lookup_char not in consts.character_alphabet:
                return ''

        return umaps.post_dict_lookup[char]
    return ''


def replace_emojis(text, emoji_replacement, string_to_preserve) -> str:
    for emoji in emoji_dictionary.EMOJI_PATTERN:
        if emoji in text and emoji not in string_to_preserve:
            text = text.replace(emoji, emoji_replacement)

    return text


def get_replacement(char) -> str:
    if char in umaps.replacement_dictionary:
        return umaps.replacement_dictionary[char]
        

def labelled_translation_to_ssml(token) -> str:
    # SSML 1.1 standard
    token = token.replace("(e. ", '<lang xml:lang="en-GB"> ') 
    token = token.replace(")", " </lang>")

    return token + ' '


def clean_labelled_translation(token, delete_labelled_translations) -> str:
    if not delete_labelled_translations:
        return labelled_translation_to_ssml(token)
    
    return ' '


def remove_consecutive_punctuation(cleaned_text):
    # the following regex demarks a string that starts with a punctuation mark,
    # followed by 1 or more occurrences of 0 or more whitespaces, followed by 1 
    # or more punctuation marks 
    return re.sub(r'([,.:;?!])(\s*[,.:;?!]+)+', r'\1', cleaned_text)
    

def text_to_tokens(text) -> list:
    """
    Splits the input text at whitespaces into tokens. Exception 
    is made within parenthesis to simplify the cleaning process.
    """
    # the following regex demarks a string within parentheses (opening and closing parenthesis) 
    return re.split(r'\s(?![^(]*\))', text)


def validate_characters(token, string_to_preserve, preserve_emojis, clean_emoji) -> str:
    """
    Checks each character of the input word (token) to see 
    if it matches any predefined character, as defined
    in constants or the second input 'string_to_preserve'.
    """
    for _, char in enumerate(token):
        repl = get_replacement(char)
        if repl:
            token = token.replace(char, repl)
        elif char in string_to_preserve or char.isdigit():
            continue
        elif char in emoji_dictionary.EMOJI_PATTERN and (clean_emoji or preserve_emojis):
            if clean_emoji:
                emoji_description = emoji_dictionary.EMOJI_PATTERN[char]
                token = token.replace(char, emoji_description)
            elif preserve_emojis:
                continue
        elif char.lower() not in consts.character_alphabet and char not in consts.punctuation_marks:
            token = replace_or_drop(char, token)

    return token + ' '


def clean(
    text,
    char_replacement={}, 
    emoji_replacement='.', 
    punct_replacement='', 
    alphabet=[], 
    punct_set=[], 
    preserve_string=[],
    preserve_emojis=False,
    clean_emojis=False,
    delete_labelled_translations=False,
) -> str:
    """
    Process (clean) the raw input text for NLP (Natural Language Processing) 
    by removing unhelpful and unusable data, as well as reducing noise.
    
    Text cleaning is task specific so multiple configurations are made available.

    Args:
        text                          : raw text for cleaning                       
        char_replacement              : dictionary of characters to convert     
        emoji_replacement             : str to replace emojis with        
        punct_replacement             : str to replace punctuations with
        alphabet                      : list of char that don't need converting     
        punct_set                     : list of punctuation marks set to preserve
        preserve_string               : list of strings forbidden to strip or convert
        preserve_emoji                : if True, we preserve emojis
        delete_labelled_translations  : if True, we delete foreign labelled text
        clean_emoji                   : if True, replace emojis with their description

    """
    
    if emoji_replacement and not clean_emojis and not preserve_emojis:
        text = replace_emojis(text, emoji_replacement, preserve_string)
    if char_replacement:
        umaps.replacement_dictionary.update(char_replacement)
    if punct_set:
        consts.punctuation_marks = punct_set
    if alphabet:
        consts.character_alphabet = alphabet
    if punct_replacement:
        update_replacement_dictionary(consts.punctuation_marks, punct_replacement)
    
    text = text_to_tokens(text)

    cleaned_text = ''
    for token in text:
        # TODO: only covers english text atm and assumes it's prefixed by "(e." as is by convention
        if token.startswith('(e. '):
            cleaned_text += clean_labelled_translation(token, delete_labelled_translations)
        elif token.strip(r",.\?!:()") in preserve_string:
            for punct_mark in ['"','(',')']:
                if punct_mark in token:
                    token = token.replace(punct_mark, ' , ')
            cleaned_text += token + ' '
        elif token.startswith('www') or token.startswith('http'):
            cleaned_text += token + ' '
        else:
            cleaned_text += validate_characters(token, preserve_string, preserve_emojis, clean_emojis)

    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = remove_consecutive_punctuation(cleaned_text)

    return cleaned_text.strip()


def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--infile', '-i', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="Text file to be cleaned")
    group.add_argument('text', nargs='?', type=str, help='Input string to be cleaned')
    args = parser.parse_args()
    
    return args


def main():
    args = parse_arguments()
    if args.text:
        text = args.text
        print(clean(text))
    elif args.infile == sys.stdin and sys.stdin.isatty():
        print("Please provide an input file or a string to be cleaned")
        raise ValueError("No input given")
    else:
        file_content = args.infile.read().splitlines()
        cleaned_arr = []
        for line in file_content:
            cleaned_arr.append(clean(line))
        for elem in cleaned_arr:
            print(elem)


if __name__ == '__main__':
    main()
