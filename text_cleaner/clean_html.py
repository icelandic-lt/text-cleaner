import argparse
import re
from bs4 import BeautifulSoup as beautiful_soup, element
from text_cleaner import constants as consts


def remove_whitespace_before_punctuation(text) -> str:
    # the following regex demarks a string with 1 or more 
    # whitespaces followed by a punctuation mark
    return re.sub(r'\s+([,.:;?!])', r'\1', text)


def remove_consecutive_punct_marks(text) -> str:
    # note that currently this gets rid of all consecutive 
    # punctuation marks while that might not be desired for all tasks.
    
    # the following regex demarks a string with 1 punctuation 
    # mark followed by 1 or more punctuation marks
    return re.sub(r'([,.:;?!])[,.:;?!]+', r'\1', text)


def tidy_up_text_format(text):
    """
    Removes duplicate punctuation marks, whitespaces or newlines.
    """
    text = text.replace(" \n","\n")
    text = re.sub(r'\n\n+', '\n', text).strip()
    text = re.sub('  +', ' ', text)

    text = remove_whitespace_before_punctuation(text)
    text = remove_consecutive_punct_marks(text)

    return text


def clean_html_tables(soup) -> element.Tag:
    """
    Organizes text in tables to a more readable form for TTS engines.
    This function does so by prepending a table header to each data 
    cell in the same column and removes all original text in headers.
    """
    tables = soup.find_all('table')

    for table in tables:
        table_row = table.find_all('tr')
        # used by each cell to reference it's header content
        table_headers = table.find_all('th')

        for _, row, in enumerate(table_row):
            # list of cells for current row
            table_cell = row.find_all('td') 
            for idx2, cell in enumerate(table_cell):
                if idx2 < len(table_headers):
                    cell = cell.insert_before(table_headers[idx2].get_text() + ': ')

        # remove headers after they've been prepended to each cell in their column
        for th in table_headers:
            th.decompose()
        
    return soup


def append_punctuation_to_tag_content(text) -> element.Tag:  
    """
    Appends a string to closing html tags as described 
    by 'html_closing_tag_replacement' in constants.py
    """
    for tag in consts.html_closing_tag_replacement:
        for text_within_tag in text.find_all(tag):
            text_within_tag.append(consts.html_closing_tag_replacement[tag] + ' ')
    
    return text


def extract_html_from_file(html_doc, extract_from_div) -> element.Tag:
    html_doc_content = open(html_doc)
    soup = beautiful_soup(html_doc_content.read(), features='html.parser')
    soup = soup.find("div", extract_from_div)

    return soup


def clean_html(
    html_doc,
    replace_html_closing_tag_with={},
    content_parent_div={"class": "content-text"},
    write_to_file='',
) -> str:
    """
    Preprocess html document input for text cleaning by parsing text content 
    specified by input, by removing and replacing html tags based on dictionary input.
    The parent div of the content to be parsed and cleaned has to be specified so the
    html cleaner can distinct between what's relevant.
    
    Args:
        html_doc                        : html document to extract from
        replace_html_closing_tag_with   : dictionary of html tags to be convert 
        write_to_file                   : name of output file
        content_parent_div              : the parent div of all the content to be parsed
    """

    if replace_html_closing_tag_with:
        consts.html_closing_tag_replacement.update(replace_html_closing_tag_with)

    html_soup = extract_html_from_file(html_doc, content_parent_div)
    html_soup = clean_html_tables(html_soup)
    html_soup = append_punctuation_to_tag_content(html_soup)
    
    text = html_soup.get_text()
    text = tidy_up_text_format(text)

    if write_to_file:
        f = open(write_to_file, "a")
        f.write(str(text))
        f.close()

    return text


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("html_doc", help="html document")
    parser.add_argument("-w", "--write", default="", help="name of the file for the text output")

    args = parser.parse_args()

    return args


def main():
        cmdline_args = parse_arguments()
        html_doc = cmdline_args.html_doc
        output_file = cmdline_args.write

        print(clean_html(
            html_doc=html_doc,
            write_to_file=output_file
        ))


if __name__ == '__main__':
    main()
