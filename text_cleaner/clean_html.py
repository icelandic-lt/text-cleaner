
import re
from bs4 import BeautifulSoup as bs
from text_cleaner import constants


def remove_whitespace_before_punctuation(text):
    # the following regex demarks a string with 1 or more 
    # whitespaces followed by a punctuation mark
    return re.sub(r'\s+([,.?!])', r'\1', text)


def remove_duplicate_punctuation_marks(soup):
    # the following regex demarks a string with 1 punctuation 
    # mark followed by 1 or more punctuation marks
    return re.sub(r'([,.?!])[,.?!]+', r'\1', soup)


# TODO: Incomplete.
# Currently this method only works for tables with the same amount of rows & columns
# Also the headers are currently appended to all rows (even those before), this will become
# problematic if a table with that description is in the html document.
def organize_text_in_table(soup):
    """
    Organizes text in tables by prepending a header for each cell in it's 
    column and finally removes the rows containing only headers.
    
    This is so headers are read each time by TTS engines before the cell's content.
    """
    tables = soup.find_all('table')

    for table in tables:
        table_row = table.find_all('tr')
        # used by each cell to reference it's header content
        table_headers = table.find_all('th')

        for _, row, in enumerate(table_row):
            table_cell = row.find_all('td') # list of cells for current row
            for idx2, cell in enumerate(table_cell):
                cell = cell.insert_before(table_headers[idx2].get_text())

        # remove headers after they've been prepended to each cell in their shared table
        for th in table_headers:
            th.decompose()
    return soup


def append_punctuation_to_tag_content(text, html_tag_to_punctuation_mark):    
    for tag in html_tag_to_punctuation_mark:
        for text_within_tag in text.find_all(tag):
            text_within_tag.append(html_tag_to_punctuation_mark[tag])

    return text


def clean_html(
    html_document,
    html_tag_to_punctuation_mark={},
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

    # WIP - Read description for method
    # soup = organize_text_in_table(soup)

    text = append_punctuation_to_tag_content(soup, html_tag_to_punctuation_mark)
    text = soup.get_text()

    text = remove_whitespace_before_punctuation(text)
    text = remove_duplicate_punctuation_marks(text)

    # convenient while developing this html cleaner
    # f = open("audiobook.txt", "a")
    # f.write(str(text))
    # f.close()

    return text


def main():
    dictionary = {}
    for element in constants.HTML_ELEMENTS: # convenient while developing this html cleaner
        dictionary[element] = '. '

    print(
        clean_html(
        html_document='audio2.html',
        html_tag_to_punctuation_mark=dictionary,
        div_class_name={"class": "content-text"},
    ))


if __name__ == '__main__':
    main()