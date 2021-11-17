import unicode_maps as um

"""
Handles Unicode cleaning and Unicode normalizing of text. To simplify further processing, text normalizeing and
grapheme-to-phoneme conversion, we clean the text of most unicode characters not contained in the Icelandic
alphabet, and also delete or substitue a number of punctuation characters and special symbols.
"""

# the Icelandic alphabet
CHAR_SET = ['a', 'á', 'b', 'd', 'ð', 'e', 'é', 'f', 'g', 'h', 'i', 'í', 'j', 'k', 'l', 'm', 'n', 'o', 'ó', 'p', 'r',
            's', 't', 'u', 'ú', 'v', 'y', 'ý', 'þ', 'æ', 'ö', 'x']
PUNCTUATION_SET = ['.',',',':','!','?']

def normalize_encoding(text):
    """ Normalize the unicode encoding of the input text. This includes deleting or substituting certain characters
    and symbols, as defined in unicode_maps"""
    normalized_text = text
    for c in text:
        repl = get_replacement(c)
        if repl is not None:
            normalized_text = normalized_text.replace(c, repl)
        if should_delete(c):
            normalized_text = normalized_text.replace(c, '')

    return normalized_text


def get_replacement(char):
    if char in um.unified_dictionary:
        return um.unified_dictionary[char]


def should_delete(char):
    return char in um.delete_chars_map


def get_ice_alpha_replacement(char):
    if char in um.post_dict_lookup:
        return um.post_dict_lookup[char]
    return ''


def normalize_alphabet(sentences):
    """
         This method is the last in the normalization process. That is, we already have
         normalized the text with regards to abbreviations, digits, etc., but as last procedure
         we need to ensure that no non-valid characters are delivered to the g2p system.

         Before replaceing possible non-valid characters, we make a lexicon-lookup, since
         words with non-Icelandic characters might be stored there, even if automatic g2p
         would fail.

         TODO: this needs more careful handling and a "contract" with the g2p module: which
         characters should be allowed?

    """
    if isinstance(sentences, list):
        sentence_list = sentences
    else:
        sentence_list = [sentences]
    normalized_sentences = []
    norm_sent = ''
    for sent in sentence_list:
        tokens = sent.split()
        for token in tokens:
            for ind, char in enumerate(token):
                # is it an Icelandic character?
                if char.lower() not in CHAR_SET:
                    replacement = get_ice_alpha_replacement(char)
                    # we found a replacement for the non-Icelandic character
                    if len(replacement) > 0:
                        token = token.replace(char, replacement)
                    # sounds odd if parenthesis are ignored and don't cause the tts voice
                    # to pause a little, try a comma
                    # TODO: we might need a more general approach to this, i.e. which
                    # symbols and punctuation chars should cause the voice to pause?
                    elif (char == '(' or char == ')' or char == '"'):
                        token = token.replace(char, ",")
                    # we want to keep punctuation marks still present in the normalized
                    # string, but delete the unknown character otherwise
                    elif char not in PUNCTUATION_SET:
                        token = token.replace(char, "") # TODO: to replace with can probably be passed in as a variable

            # we restore the original string with valid words / characters only
            norm_sent += token + ' '
            # don't add an extra space if we deleted the word

        normalized_sentences.append(norm_sent.lower().strip())

    return normalized_sentences


def normalize_alphabet_from_tuples(normalized_tuples):
    """
    For normalization requests that require the return value to be a list of tuples perserving the original tokens,
    this method hands the normalized tokens over to the normalize_alphabet method and returns the tuple list
    with the alphabet-normalized tokens.

    :param normalized_tuples: pairs of original tokens with their normalization
    :return: same list of tuples as the input, where the normalized tokens have been run through alpahbet-normalizing
    """
    new_tuple_list = []
    for tuple in normalized_tuples:
        final_norm = normalize_alphabet(tuple[1])
        new_tuple_list.append((tuple[0], final_norm[0]))

    return new_tuple_list


def main():
    text = 'norma\u00adlize this and \u0394'
    normalized = normalize_encoding(text)
    print(text)
    print(normalized)


if __name__ == '__main__':
    main()
