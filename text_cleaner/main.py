import argparse
import re

EMOJI_PATTERN = "\U0001f469|\u2764" # Temporary for testing TODO: Find a list with extensive coverage of emojis    

def update_replacement_dictionary(char_to_replace, replacement):
    """
    Updates the replacement dictionary
    """
    dict = {}
    for cr in char_to_replace: 
        dict[cr] = replacement

    # TODO: Add dict to dictionary in unicode_maps

def clean(
    text,                               # text to be cleaned
    char_to_preserve=[],                # list of characters to preserve i.e. forbidden to convert or strip
    char_to_replace={},                 # dictionary of chars to replace e.g. {'a': 'x'} converts all 'a' found to 'x'
    alphabet=[],                        # list of the desired alphabet (Icelandic as default)
    punctuation_set=[],                 # list of punctuations (we strip the rest)
    clean_emoji=True,                   # clean emojis i.e. replace them
    punctuation=False,                  # clean all punctuation
    replace_emoji_with="",              # replace all emojis with custom char
    replace_punctuation_with="",        # replace all punctuation with a custom string / char
    ):

    # TODO: needs paraphrasing
    """
    Text cleaner with customizeable features

    """
    
    if char_to_preserve:
        # TODO: Solve how we'll make sure chars are preserved
        PRESERVE_SET = char_to_preserve
    if char_to_replace:
        # TODO: Add to dictionary in unicode_maps
        print("char_to_replace")
    if punctuation_set:
        print("punctuation_set")
        # TODO: Replace punctuation list in unicode_normalizer
    if alphabet:
        print("alphabet")
        # TODO: Replace alphabet list in unicode_normalizer
    if replace_punctuation_with:
        update_replacement_dictionary(punctuation_set, replace_punctuation_with)
    if clean_emoji:
        # TODO: Unclear whether we'll solve this by using a dictionary or a dedicated function
        text = re.sub(EMOJI_PATTERN, replace_emoji_with, text)
    if punctuation:
        print('punctuation')

    # TODO: Clean text using unicode_normalizer & unicode_maps
        
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