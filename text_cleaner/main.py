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
    text,
    char_to_preserve=[],
    char_to_replace={},
    alphabet=[],
    punct_set=[],
    clean_emoji=True,
    clean_punct=False,
    replace_emoji_with="",
    replace_punct_with="",
):

    """
    Process (clean) the raw input text for NLP (Natural Language Processing) by removing 
    unhelpful and unusable data, as well as reducing noise.
    
    Text cleaning is task specific so multiple configurations are available.
    Args:
                      text: raw text for cleaning                       
          char_to_preserve: list of char types forbidden to strip or convert
           char_to_replace: dictionary of characters to convert     
                  alphabet: list of char that don't need converting     
                 punct_set: list of punctuation marks set to preserve
               clean_emoji: if True, convert emojis to the value of "replace_emoji_with"
               clean_punct: if True, convert punctuations to the value of "replace_punct_with
        replace_emoji_with: str to replace emojis with        
        replace_punct_with: str to replace punctuations with

    Returns:
        str: cleaned text based on function args
    """
    
    if char_to_preserve:
        PRESERVE_SET = char_to_preserve
    if char_to_replace:
        um.unified_dictionary.update(char_to_replace)
    if punct_set:
        un.PUNCT_SET = punct_set
    if alphabet:
        un.CHAR_SET = alphabet
    if replace_punct_with:
        update_replacement_dictionary(punct_set, replace_punct_with)
    if clean_emoji:
        text = re.sub(EMOJI_PATTERN, replace_emoji_with, text)
    if clean_punct:
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
                #punct_set=[',','.'],
                #clean_emoji=True,
                #clean_punct=False,
                #replace_emoji_with="<emoji>",
                #replace_punct_with="  <punctuation>  ",
                ))

if __name__ == '__main__':
    main()