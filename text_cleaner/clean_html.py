import re
from bs4 import BeautifulSoup as bs
from text_cleaner import constants

def remove_whitespace_before_punctuation(text):
    # TODO: regex description
    return re.sub(r'\s+([,.?!])', r'\1', text)

def remove_duplicate_punctuation_marks(soup):
    # TODO: regex description
    return re.sub(r'([,.?!])[,.?!]+', r'\1', soup)

def replace_html_tags(text, html_tag_replacement_dict):    
    for tag in html_tag_replacement_dict:
        for text_within_tag in text.find_all(tag):
            text_within_tag.append(html_tag_replacement_dict[tag])

    return text

def clean_html(
    html_document,
    html_tag_replacement={},
    div_class_name={}, 
):
    """
    Preprocess html document input for text cleaning by parsing text content 
    specified by input, by removing and replacing html tags based on dictionary input.
    
    Args:
        html_document           : html document to be cleaned
        html_tag_replacement    : dictionary of html tags to be convert 
        div_class_name          : the target div that contains all the content to be cleaned

    Returns:
        str: html tag stripped text from the input html document
    """

    html_doc = open(html_document)
    soup = bs(html_doc.read())
    soup = soup.find("div", div_class_name)

    soup = replace_html_tags(soup, html_tag_replacement)
    text = soup.get_text()

    text = remove_whitespace_before_punctuation(text)

    text = remove_duplicate_punctuation_marks(text)

    # convenient whilst developing this html cleaner
    f = open("audiobook.txt", "a")
    f.write(str(text))
    f.close()

    return text

def main():
    dictionary = {}
    for element in constants.HTML_ELEMENTS:
        dictionary[element] = '.'

    print(
        clean_html(
        html_document='audio.html', 
        #html_tag_replacement={'p':'.', 'li':'.'},
        html_tag_replacement=dictionary,
        div_class_name={"class": "content-text"},
    ))
    
if __name__ == '__main__':
    main()