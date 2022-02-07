# Text Cleaner 

## Introduction

Text cleaning module for processing raw text input.

This module is a component of a TTS-Frontend engine, more specifically, it is the first step in processing raw text input before being normalized in the next step in the TTS-Frontend pipeline.

Despite this module being designed as a component of the TTS-Frontend engine, it's designed with versatility in mind to accommodate various text cleaning tasks, therefore multiple configurations have been built into the text cleaner to allow for task specific cleaning.

Coupled with this text cleaning module is a preprocessing feature for text embedded in html documents (primarily designed for audiobooks). This preprocessing step includes parsing, extraction and re-organizing of text for TTS engines.

## Installation
```bash
# clone this repository.
$ git clone https://github.com/grammatek/text-cleaner

# enter the repository
$ cd text-cleaner

# install dependencies
$ pip install -e .
```
## Usage

### Via the command line tool
```bash
# Run the app by passing in a "string" to be cleaned. 
$ python3 text_cleaner/clean.py "Hann Bubbi söng 🎤 afmælißønginn fyrir π."
['Hann Bubbi söng . afmælissönginn fyrir pí.']
```

### As an import in Python
```python
from text_cleaner import clean

clean(
    "text to be cleaned",                  
    char_replacement={},                 # dictionary of characters to convert     
    emoji_replacement='.',               # str to replace emojis with        
    punct_replacement='',                # str to replace punctuations with
    alphabet=[],                         # list of char that don't need converting     
    punct_set=[],                        # list of punctuation marks set to preserve
    preserve_string=[],                  # list of strings forbidden to strip or convert
    preserve_emojis=False,               # if True, preserve emojis
    clean_emojis=False,                  # if True, convert emojis to their text description 
    delete_labelled_translations=False,  # if True, delete all labelled translations
)

# If being used as a part of the TTS-Frontend pipeline, 
# then no configurations should be made. All default 
# values are configured for input/output specifications 
# between components in the TTS-Frontend pipeline.

# basic example, no arguments.
>>> print(clean("π á afmæli í dåg 🎉"))
"pí á afmæli í dog ."

# convert emojis to any string and also configure 
# which characters are to be preserved.
>>> print(clean("π á afmæli í dåg 🎉", 
                emoji_replacement="emójí", 
                preserve_string=['π']))
"π á afmæli í dog emójí"

# instead of removing characters, we 
# can convert them to any string. 
>>> print(clean("π á afmæli í dåg 🎉", 
                char_replacement={'æ':'ae'}, 
                clean_emojis=True))
"pí á afmaeli í dog party popper"

```
## Usage for html preprocessing feature

### Via the command line tool
```bash
# html doc 'my_audobook.html' stored in root:
# <div class="content-text">
#    <h1>hello</h1>
#    <h2>world</h2>
# </div>

# run the html preprocessing feature by by passing in the name of the html document.
$ python3 text_cleaner/clean_html.py "my_audiobook.html"
hello.
world.

# use the -w flag if you want the output to be written to a file.
$ python3 text_cleaner/clean_html.py "my_audiobook.html" -w "output_file.txt"
hello.
world.

```

### As an import in Python

```python
from text_cleaner import clean_html

clean_html(
    "html_document.html",   # name of the html document to "clean"
    # default value has a comprehensive dictionary of html tags, 
    # see html_closing_tag_replacement in constants.py for details. 
    replace_html_closing_tag_with={},   # dictionary with html tags and what their 
                                        # closing tags are to be replaced with e.g. 
                                        # {'p':'!'} adds an exclamation mark at the 
                                        # end of every text embedded in a <p> tag.
    content_parent_div={"class": "content-text"},   # the parent div that contains 
                                                    # all the text to be extracted
    write_to_file='',   # if not left empty, writes to file for given input
)

# html doc 'my_audobook.html' stored in root:
# <div class="content-text">
#    <h1>hello</h1>
#    <h2>world</h2>
# </div>

# basic example, no arguments.
>>> print(clean_html("my_audiobook.html"))
hello. 
world.

# we can choose what closing tags are replaced by as well as write the output to file
>>> print(clean_html("my_audiobook.html", 
                     replace_html_closing_tag_with={'h2':'!'},
                     write_to_file='my_audiobook_cleaned.txt'))
hello.
world!
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
