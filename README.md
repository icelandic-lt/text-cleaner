# Text Cleaner 

## Introduction

Text cleaning module for processing raw text input.

This module is a component of the TTS-Frontend Pipeline, more specifically, it is the first step in processing raw text input before being normalized in the next step.

If being used as a part of the TTS-Frontend Pipeline then no configurations should be made, the default values are based on input/output specifications between components in the TTS-Frontend.

Despite this module being designed as a component of the TTS-Frontend Pipeline its designed with versatility in mind since text cleaning is task specific so multiple configurations are available.

## Usage

### From the terminal

```bash
# Clone this repository.
$ git clone https://github.com/grammatek/text-cleaner

# Enter the directory.
$ cd ./text-cleaner

# Run the app by passing in "any string". 
$ python3 text_cleaner/main.py "Hann Bubbi söng 🎤 afmælißønginn fyrir π."

['hann bubbi söng . afmælissönginn fyrir pí.']
```

### As import in Python
```python
from text-cleaner import clean

# All available arguments are listed below with their default values (most are empty by design). 
cleaned_text = clean(
    "text to be cleaned",
    char_to_preserve=[],            # list of characters forbidden to convert or strip.
    char_to_replace={},             # dictionary of characters to convert.
    alphabet=[],                    # list of the alphabet letters used (Icelandic as default).
    punct_set=[],                   # list of punctuations (we strip the rest).
    clean_emoji=True,               # clean emojis i.e. replace them.
    replace_emoji_with=".",         # replace all emojis with custom char.           
)

# basic example, no usage of arguments.
>>> print(clean("π á afmæli í dag, Bubbi söng 🎤 afmælißønginn í tilefni dagsins."))
"pí á afmæli í dag, Bubbi söng . afmælissönginn í tilefni dagsins."

# we can convert emojis to any string, also configure which characters are "off limits".
>>> print(clean("π á afmæli í dag, Bubbi söng 🎤 afmælißønginn í tilefni dagsins.", 
            replace_emoji_with=":emójí:", char_to_preserve=['π', 'ø'])
"π á afmæli í dag, Bubbi söng :emójí: afmælissønginn í tilefni dagsins."

# we can define what punctuation marks we want to keep, also if we want emojis to be preserved.
>>> print(clean("sem dæmi: ekki hlaupa á ganginum! hrópa 😱 mamma, amma og pabbi öll í kór.", 
            clean_emoji=False, punct_set=['.',',']))
"sem dæmi ekki hlaupa á ganginum hrópa 😱 mamma, amma og pabbi öll í kór."

# instead of getting rid of some characters, we can also convert them to a string of our choice. 
>>> print(clean("sem dæmi: ekki hlaupa á ganginum! hrópa mamma, amma og pabbi öll í kór.", 
            char_to_replace={'æ':'ae', ':': ',', '!': '.'}))
"sem daemi, ekki hlaupa á ganginum. hrópa mamma, amma og pabbi öll í kór."
```


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
