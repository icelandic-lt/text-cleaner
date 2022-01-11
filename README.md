# Text Cleaner 

## Introduction

Text cleaning module for processing raw text input.

This module is a component of a TTS-Frontend engine, more specifically, it is the first step in processing raw text input before being normalized in the next step.

Despite this module being designed as a component of the TTS-Frontend engine, it's designed with versatility in mind to accommodate various text cleaning tasks, therefore multiple configurations have been built into the text cleaner to allow for task specific cleaning.

If being used as a part of the TTS-Frontend pipeline then no configurations should be made, the default values are based on input/output specifications between components in the TTS-Frontend pipeline.

## Installation
```bash
# clone this repository.
$ git clone https://github.com/grammatek/text-cleaner

# enter the repository
$ cd text-cleaner

# install dependancies
$ pip install -e .
```
## Usage

### Command line tool
```bash
# Run the app by passing in "text to be cleaned". 
$ python3 text_cleaner/main.py "Hann Bubbi söng 🎤 afmælißønginn fyrir π."

['hann bubbi söng . afmælissönginn fyrir pí.']
```

### As import in Python
```python
from text-cleaner import clean

# All available arguments are listed below with their default values (most are empty by design).
clean(
    "text to be cleaned",                  
    char_replacement={},                 # dictionary of characters to convert     
    emoji_replacement='.',               # str to replace emojis with        
    punct_replacement='',                # str to replace punctuations with
    alphabet=[],                         # list of char that don't need converting     
    punct_set=[],                        # list of punctuation marks set to preserve
    preserve_string=[],                  # list of strings forbidden to strip or convert
    preserve_emoji=False,                # if True, we preserve emojis
    clean_emoji=False,                   # if True, we convert emojis to their text description 
    delete_labelled_translations=False,  # if True, we delete all labelled translations
)

# basic example, no arguments set.
>>> print(clean("π á afmæli í dåg 🎉"))
"pí á afmæli í dag ."

# we can convert emojis to any string and also configure which characters are to be preserved.
>>> print(clean("π á afmæli í dåg 🎉", emoji_replacement="emójí", preserve_string=['π'])
"π á afmæli í dag emójí"

# instead of removing characters, we can convert them to a string of our choice. 
>>> print(clean("π á afmæli í dåg 🎉", char_replacement={'æ':'ae'}, ))
"pí á afmaeli í dag ."
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
