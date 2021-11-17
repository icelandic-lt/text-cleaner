import argparse
import re
import unicode_maps as um
import unicode_normalizer as un

EMOJI_PATTERN = "\U0001f469|\u2764" # Temporary for testing TODO: Find a list with extensive coverage of emojis    

def update_replacement_dictionary(char_to_replace, replacement):
    """
    This method takes a list of strings and a string respectively. It then creates a dictionary using values 
    from 'char_to_replace' as key and 'replacement' as value. Finally it adds it to the "replacement" dictionary
    """
    dict = {}
    for cr in char_to_replace: 
        dict[cr] = replacement

    um.unified_dictionary.update(dict)

def clean(
    text,                               # text to be cleaned
    char_to_preserve=[],                # list of characters to preserve i.e. forbidden to convert or strip
    char_to_replace={},                 # dictionary of chars to replace e.g. {'a': 'x'} converts all 'a' found to 'x'
    alphabet=[],                        # list of the desired alphabet (Icelandic as default)
    punctuation_set=[],                 # list of punctuations (we strip the rest)
    clean_emoji=True,                   # clean emojis i.e. replace them
    punctuation=False,                  # clean punctuation i.e. replace them
    replace_emoji_with="",              # replace all emojis with custom char
    replace_punctuation_with="",        # replace all punctuation with a custom string / char
    ):

    """
    Process (clean) the raw input text for NLP (Natural Language Processing) by removing 
    unhelpful and unusable data, as well as reducing noise.
    
    Text cleaning is task specific so multiple configurations are available.
    TODO: 
    """
    
    if char_to_preserve:
        PRESERVE_SET = char_to_preserve
    if char_to_replace:
        um.unified_dictionary.update(char_to_replace)
    if punctuation_set:
        un.PUNCTUATION_SET = punctuation_set
    if alphabet:
        un.CHAR_SET = alphabet
    if replace_punctuation_with:
        update_replacement_dictionary(punctuation_set, replace_punctuation_with)
    if clean_emoji:
        text = re.sub(EMOJI_PATTERN, replace_emoji_with, text)
    if punctuation:
        print('punctuation')

    text = un.normalize_encoding(text)
    text = un.normalize_alphabet(text)
        
    return text

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
                #punctuation_set=[',','.'],
                #clean_emoji=True,
                #punctuation=False,
                #replace_emoji_with="<emoji>",
                #replace_punctuation_with="  <punctuation>  ",
                ))

if __name__ == '__main__':
    main()