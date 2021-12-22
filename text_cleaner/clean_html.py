
import argparse
import re
from bs4 import BeautifulSoup as beautiful_soup
from text_cleaner import constants


def remove_whitespace_before_punctuation(text):
    # the following regex demarks a string with 1 or more 
    # whitespaces followed by a punctuation mark
    return re.sub(r'\s+([,.?!])', r'\1', text)


def remove_duplicate_punctuation_marks(soup):
    # the following regex demarks a string with 1 punctuation 
    # mark followed by 1 or more punctuation marks
    return re.sub(r'([,.:;?!])[,.:;?!]+', r'\1', soup)


# TODO: Incomplete.
# Currently this method only works for tables with the same amount of rows & columns
# Also the headers are currently appended to all rows (even those before), this will become
# problematic if a table with that description is in the html document.
def clean_html_tables(soup):
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


def extract_html_from_file(html_doc, extract_from_div):
    html_doc_content = open(html_doc)
    soup = beautiful_soup(html_doc_content.read(), features='html.parser')
    soup = soup.find("div", extract_from_div)

    return soup


def clean_html(
    html_doc,
    html_tag_to_punctuation_mark={},
    content_parent_div={},
    write_to_file='',
):
    """
    Preprocess html document input for text cleaning by parsing text content 
    specified by input, by removing and replacing html tags based on dictionary input.
    
    Args:
        html_doc                : html document to extract from
        html_tag_replacement    : dictionary of html tags to be convert 
        write_to_file           : name of output file
        content_parent_div      : the parent div of all the content to be cleaned

    Returns:
        str: the input html document stripped of html tags
    """


    # WIP - Read description for method
    # soup = clean_html_tables(soup)

    html_soup = extract_html_from_file(html_doc, extract_from_div=content_parent_div)

    html_soup = append_punctuation_to_tag_content(html_soup, html_tag_to_punctuation_mark)
    text = html_soup.get_text()



    text = remove_whitespace_before_punctuation(text)
    text = remove_duplicate_punctuation_marks(text)

    if write_to_file:
        f = open(write_to_file, "a")    
        f.write(str(text))
        f.close()

    return text


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'), help="html file to be extracted")
    args = parser.parse_args()
    
    return args


def main():
    dictionary = {}
    for element in constants.HTML_ELEMENTS: # convenient while developing this html cleaner
        dictionary[element] = '. '

    print(
        clean_html(
            html_doc='html_snip.html',
            html_tag_to_punctuation_mark=dictionary,
            content_parent_div={"class": "content-text"},
            write_to_file='cleaned_html_text.txt'
        ))


if __name__ == '__main__':
    main()