# Text Cleaner 

## Introduction

Text cleaning module for processing raw text input for NLP (Natural Language Processing)
  
## Usage

### From the terminal

```bash
# Clone this repository
$ git clone https://github.com/grammatek/text-cleaner

# Enter the directory
$ cd ./text-cleaner

# Install dependancies 
$ pip install -r requirements.txt

# Run the app by passing in "text-to-be-cleaned" 
$ python3 text_cleaner/main.py "hreinsa þennan texta takk."

['hreinsa þennan texta takk.']
```

### As import in Python
```python
from text-cleaner import clean

cleaned_text = clean(
    "text to be cleaned",
    char_to_preserve=[],            # list of characters to preserve i.e. forbidden to convert or strip
    char_to_replace={},             # dictionary of chars to replace e.g. {'a': 'x'} converts all 'a' found to 'x'
    alphabet=[],                    # list of the desired alphabet (Icelandic as default)
    punctuation_set=[],             # list of punctuations (we strip the rest)
    clean_emoji=True,               # clean emojis i.e. replace them
    clean_punctuation=False,        # clean punctuation i.e. replace them with      remove, do nothing, replace
    replace_emoji_with="",          # replace all emojis with custom char
    replace_punctuation_with="",    # replace all punctuation with a custom string / char
)
```
*The default parameters are listed above*

## Getting help

Feel free to open an issue inside the [issue tracker](https://github.com/grammatek/text-cleaner/issues). You can also [contact us](mailto:info@grammatek.com) via email.

## Contributing

You can contribute to this project by forking it, creating a private branch and opening a new [pull request](https://github.com/grammatek/text-cleaner/pulls).

## License

Copyright © 2021 Grammatek ehf.

This software is developed under the auspices of the Icelandic Government 5-Year Language Technology Program, described in
[Icelandic](https://www.stjornarradid.is/lisalib/getfile.aspx?itemid=56f6368e-54f0-11e7-941a-005056bc530c) and
[English](https://clarin.is/media/uploads/mlt-en.pdf)

This software is licensed under the [Apache License](LICENSE)

## Acknowledgments
* https://github.com/jfilter/clean-text
