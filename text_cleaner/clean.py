"""
    TextCleaner is a text processing module that cleans input text from characters and symbols - or replaces them -
    that would disturb further processing of the text.

    Copyright (C) 2022 Grammatek ehf.

    This software is published under the Apache 2.0 License, sie LICENSE.
    Please note that submodules might be published under the MIT License (https://opensource.org/licenses/MIT)

    This module offers a custom adaption of valid characters and replacement maps as well as text extracting
    from html, replacing tags with punctuation where applicable.

    The module is developed with text processing for TTS in mind, but params can be adjusted for other use cases
    as well.

"""
import argparse, sys
import logging
import re
from text_cleaner import constants as consts
from text_cleaner import emoji_dictionary

# Common punctuation symbols, often to be ignored at start/end of tokens
COMMON_PUNCT = ',.?!:;()'
URL_PATTERN = '^(www)|(http).*'
EN_LABEL = '(e. '
# SSML 1.1 standard
SSML_LANG_START = '<lang xml:lang="en-GB"> '
SSML_LANG_END = ' </lang>'


class TextCleaner:

    def __init__(self, replacement_dict={}, post_dict={}, char_replacement={}, punct_replacement='', alphabet=[],
                 punct_set=[], preserve_strings=[], emoji_replacement='.', preserve_emojis=False, describe_emojis=False,
                 delete_labelled_translations=False):

        """
        Initializes the textCleaner, arguments offer custom handling of characters, symbols and strings.
        All arguments have default values, so if no customized cleaning is wanted, textCleaner can be initialized
        without arguments.

        Note: the params regarding the handling of emojis are mutually exclusive and are ordered:
            * if char_replacement or preserve_strings contain emojis, those will have priority over general emoji-handling
            * if 'preserve_emojis' is set to True, 'describe_emojis' and 'emoji_replacement' are discarded
            * otherwise, if 'describe_emojis' is set to True, 'emoji_replacement' is discarded


        :param replacement_dict: a dictionary of characters and diverse unicode symbols with their replacements.
        :param post_dict: a dictionary of foreign characters to check at the end of the cleaning process.
        :param char_replacement: dictionary of characters to convert, will be added to replacement_dict
        :param punct_replacement: one string to replace all punctuation symbols #TODO: does this interfere with replacement dict?
        :param alphabet:  list of char that shouldn't be converted, even if they are included in a replacement map,
                            default is defined in constants.py
        :param punct_set: list of punctuation marks set to preserve, default is defined in constants.py
        :param preserve_string: list of strings forbidden to strip or convert, regardless if they contain non-valid chars
        :param preserve_emojis: if True, we preserve emojis, default is False
        :param describe_emojis: if True, replace emojis with their description, default is False. Note that 'preserve_emoji'
                                overrides this parameter!
        :param emoji_replacement: str to replace emojis with, default is '.'. Note that 'preserve_emoji' and
                                'describe_emojis' override this parameter!
        :param delete_labelled_translations: if True, we delete text/tokens labelled as foreign, default is False

        """
        # since we might alter replacement_dictionary, make a copy of the parameter dictionary
        self.replacement_dictionary = replacement_dict.copy()
        self.post_dict_lookup = post_dict
        if char_replacement:
            self.update_replacement_dictionary(char_replacement)
        if punct_set:
            self.preserved_punctuation = punct_set
        else:
            self.preserved_punctuation = consts.punctuation_marks
        if punct_replacement:
            punct_dict = self.create_dict(self.preserved_punctuation, punct_replacement)
            self.update_replacement_dictionary(punct_dict)
        if alphabet:
            self.alphabet = alphabet
        else:
            self.alphabet = consts.character_alphabet
        self.preserve_strings = preserve_strings
        self.delete_translations = delete_labelled_translations
        if preserve_emojis:
            self.preserve_emojis = True
            self.describe_emojis = False
            self.emoji_replacement = ''
        elif describe_emojis:
            self.preserve_emojis = False
            self.describe_emojis = True
            self.emoji_replacement = ''
        else:
            self.preserve_emojis = False
            self.describe_emojis = False
            self.emoji_replacement = emoji_replacement

    @staticmethod
    def create_dict(keys_list: list, value: str) -> dict:
        """
        Create a dictionary containing the elements from 'keys_list' as keys and the same value 'value'
        for each key in the dictionary.
        :param keys_list: list of keys for the new dictionary
        :param value: a value to put at each key in the new dictionary
        :return: a dictionary with keys from 'keys_list' and each value is 'value'
        """
        result_dict = {}
        for elem in keys_list:
            result_dict[elem] = value
        return result_dict

    @staticmethod
    def remove_consecutive_punctuation(text: str) -> str:
        # the following regex demarks a string that starts with a punctuation mark,
        # followed by 1 or more occurrences of 0 or more whitespaces, followed by 1
        # or more punctuation marks
        return re.sub(r'([' + COMMON_PUNCT + '])(\s*[' + COMMON_PUNCT + ']+)+', r'\1', text)

    @staticmethod
    def text_to_tokens(text: str) -> list:
        """
        Splits the input text at whitespaces into tokens. Exception
        is made within parenthesis to simplify the cleaning process.
        """
        # the following regex demarks a string within parentheses (opening and closing parenthesis)
        return re.split(r'\s(?![^(]*\))', text)

    @staticmethod
    def labelled_translation_to_ssml(token) -> str:
        token = token.replace(EN_LABEL, SSML_LANG_START)
        token = token.replace(')', SSML_LANG_END)

        return token + ' '

    def clean(self, text: str, html=False) -> str:
        """
        Clean the input text according to the parameter settings in __init__.
        Return a cleaned version of 'text'.

        :param text: string to clean
        :param html: if True, first parse the input text as html
        :return: a cleaned version of 'text' according to init settings
        """
        clean_text = self.process_emojis(text)
        clean_text = self.text_to_tokens(clean_text)

        cleaned_text = ''
        for token in clean_text:
            # TODO: only covers english text atm and assumes it's prefixed by "(e." as is by convention
            if token.startswith(EN_LABEL):
                cleaned_text += self.clean_labelled_translation(token)
            elif token in self.preserve_strings or token.strip('r'+COMMON_PUNCT) in self.preserve_strings:
                # TODO: is this defined somewhere? Why '"()'?
                token = re.sub(r'["()]', ' , ', token)
                cleaned_text += token + ' '
            elif re.match(URL_PATTERN, token):
                # If not handled separately, the different punctuation symbols in a URL would be deleted/replaced
                # and the token splitted. We don't want that, keep URLs as one token
                # TODO: what about email?
                cleaned_text += token + ' '
            else:
                cleaned_text += self.validate_characters(token)

        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text = re.sub(r'\n+', ' ', cleaned_text)
        cleaned_text = self.remove_consecutive_punctuation(cleaned_text)

        return cleaned_text.strip()

    def process_emojis(self, text: str) -> str:
        """
        Process emojis according to init parameters of the class. We might not do anything at all, or replace
        them with their description or with one replacement string (default is '.')
        :param text: a string that might contain emojis
        :return: 'text' where emojis have been processed according to the init parameters of the class
        """
        if self.preserve_emojis:
            return text
        if self.describe_emojis:
            return self.replace_emojis(text)
        if self.emoji_replacement:
            return self.replace_emojis(text, self.emoji_replacement)
        return text

    def replace_emojis(self, text: str, replacement='') -> str:
        """
        Replace emojis in text. Emojis are defined in emoji_dictionary.py, if no replacement is given,
        we replace each emoji by its value in the emoji_dictionary. Otherwise, replace each emoji
        by replacement

        Note: we don't offer the possibility to delete emojis without a trace, i.e. without at least replacing
        them by a '.' . We might add that possibility later if it turns out to be useful.

        :param text: a string that might contain emojis
        :param replacement: if not empty, replace each emoji in text with this string
        :return: a text without emojis, replaced either by emoji descriptions or by param replacement
        """
        for emoji in emoji_dictionary.EMOJI_PATTERN:
            if emoji in text and emoji not in self.preserve_strings:
                if replacement:
                    text = text.replace(emoji, replacement)
                else:
                    text = text.replace(emoji, emoji_dictionary.EMOJI_PATTERN[emoji])
        return text

    def validate_characters(self, token: str) -> str:
        """
        Checks each character of the input word (token) to see
        if it matches any predefined character, as defined
        in constants or the second input 'string_to_preserve'.
        """
        for char in token:
            repl = self.replacement_dictionary[char] if char in self.replacement_dictionary else ''
            if repl:
                token = token.replace(char, repl)
            elif char.isdigit():
                continue
            elif char in emoji_dictionary.EMOJI_PATTERN:
                # We have already taken care of emojis
                continue
            elif char.lower() not in self.alphabet and char not in self.preserved_punctuation:
                token = self.replace_or_drop(char, token)

        return token + ' '

    def replace_or_drop(self, char: str, token: str) -> str:
        replacement = self.get_ice_alpha_replacement(char)
        if replacement:
            token = token.replace(char, replacement)
        elif char in ['(', ')', '"']:
            # again: where do these symbols come from?
            token = token.replace(char, " , ")
        elif char not in self.preserved_punctuation and char not in self.replacement_dictionary.values():
            token = token.replace(char, '')

        return token

    def get_ice_alpha_replacement(self, char) -> str:
        """
        Replace 'char' with a letter or letters from self.alphabet. Return an empty string if the current
        self.alphabet turns out not to contain the replacement value from the post_dict_lookup

        :param char: a char to check for validity
        :return: 'char' if valid, replacement, if valid replacement is found, empty string otherwise
        """
        if char in self.post_dict_lookup:
            # validate the character returned by post_dict_lookup
            for lookup_char in self.post_dict_lookup[char].lower():
                if lookup_char not in self.alphabet:
                    return ''
            return self.post_dict_lookup[char]
        return ''

    def clean_labelled_translation(self, token) -> str:
        if self.delete_translations:
            return ' '
        else:
            return self.labelled_translation_to_ssml(token)

    def update_replacement_dictionary(self, custom_replacements: dict) -> None:
        """
        Adds the custom_replacements to the collection of character
        replacement dictionaries, as defined in self.replacement_dictionary
        """
        if type(custom_replacements) is dict:
            self.replacement_dictionary.update(custom_replacements)
        else:
            logging.warning("Param 'custom_replacement' should be a dictionary, but is a " +
                            str(type(custom_replacements)) + ". Did not update replacement_dictionary")



def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--infile', '-i', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="Text file to be cleaned")
    group.add_argument('text', nargs='?', type=str, help='Input string to be cleaned')
    args = parser.parse_args()
    
    return args


def main():
    args = parse_arguments()
    cleaner = TextCleaner()
    if args.text:
        text = args.text
        print(cleaner.clean(text))
    elif args.infile == sys.stdin and sys.stdin.isatty():
        print("Please provide an input file or a string to be cleaned")
        raise ValueError("No input given")
    else:
        file_content = args.infile.read().splitlines()
        cleaned_arr = []
        for line in file_content:
            cleaned_arr.append(cleaner.clean(line))
        for elem in cleaned_arr:
            print(elem)


if __name__ == '__main__':
    main()
