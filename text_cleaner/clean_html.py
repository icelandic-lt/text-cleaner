import argparse
import re
from typing import Union, TextIO
from bs4 import BeautifulSoup as beautiful_soup, element

import text_cleaner
from text_cleaner import constants as consts

PUNCTUATION = '[,.:;?!]'
# HTML
TOP_TABLE_ELEM = 'table'
TABLE_ROW = 'tr'
TABLE_HEADER = 'th'
TABLE_CELL = 'td'


class HtmlCleaner:
    """
    Cleans html as a preprocessing step before the text cleaning performed in clean.TextCleaner.
    The input can be an html-document or an html-string. The parsing in this class is designed to
    parse the accessible EPUB-format.
    """

    def __init__(self, tag_replacements={}, content_parent_div={"class": "content-text"}, top_elem='div'):
        """
        Sets the values for the parsing.

        :param tag_replacements: a dictionary of html-tags and their replacements. Default is in constants.py
        :param content_parent_div: the parent div of the content of the html-doc
        :param top_elem: top element to look for within the content_parent_div
        """
        # a map of tags and their replacement strings
        if tag_replacements:
            self.tag_replacements = tag_replacements
        else:
            self.tag_replacements = consts.html_closing_tag_replacement
        # the parent div of the content of the html-document
        self.content_parent_div = content_parent_div
        # top element to look for within content_parent_div
        self.top_elem = top_elem

    def clean_html(self, html: str, from_file=False) -> str:
        """
        Parse the html and remove/replace html-tags, preparing for further text cleaning of the content.
        :param html: an html string or filename
        :param from_file: if True, 'html' is a filename
        :return: plain text extracted from the html, with html tag replacements as defined in self.tag_replacements
        """
        if from_file:
            html_soup = self.extract_html_from_file(html)
        else:
            html_soup = self.extract_html_from_string(html)

        html_soup = self.clean_html_tables(html_soup)
        html_soup = self.append_punctuation_to_tag_content(html_soup)

        text = html_soup.get_text()
        text = tidy_up_text_format(text)

        return text

    def extract_html_from_file(self, html_doc) -> element.Tag:
        html_doc_content = open(html_doc)
        soup = self.extract_html_from_string(html_doc_content)
        return soup.find(self.top_elem, self.content_parent_div)

    def extract_html_from_string(self, html_str: Union[str, TextIO]) -> element.Tag:
        soup = beautiful_soup(html_str, features='html.parser')
        return soup

    @staticmethod
    def clean_html_tables(soup) -> element.Tag:
        """
        Organizes text in tables to a more readable form for TTS engines.
        This function does so by prepending a table header to each data
        cell in the same column and removes all original text in headers.
        """
        tables = soup.find_all(TOP_TABLE_ELEM)

        for table in tables:
            table_row = table.find_all(TABLE_ROW)
            # used by each cell to reference it's header content
            table_headers = table.find_all(TABLE_HEADER)

            for row, in table_row:
                # list of cells for current row
                table_cell = row.find_all(TABLE_CELL)
                for idx2, cell in enumerate(table_cell):
                    if idx2 < len(table_headers):
                        cell = cell.insert_before(table_headers[idx2].get_text() + ': ')

            # remove headers after they've been prepended to each cell in their column
            for th in table_headers:
                th.decompose()

        return soup

    def append_punctuation_to_tag_content(self, text_tag: element.Tag) -> element.Tag:
        """
        Appends a string to closing html tags as described
        by 'html_closing_tag_replacement' in constants.py
        """
        for tag in self.tag_replacements:
            for text_within_tag in text_tag.find_all(tag):
                text_within_tag.append(self.tag_replacements[tag] + ' ')

        return text_tag


def tidy_up_text_format(text):
    """
    Removes duplicate punctuation marks, whitespaces or newlines.
    """
    text = text.replace('\\s\n', '\n')
    text = re.sub(r'\n+', '\n', text).strip()
    text = re.sub(' +', ' ', text)

    text = remove_whitespace_before_punctuation(text)
    text = remove_consecutive_punct_marks(text)
    text = clean_up_urls(text)

    return text


def remove_whitespace_before_punctuation(text) -> str:
    # the following regex demarks a string with 1 or more 
    # whitespaces followed by a punctuation mark
    return re.sub(r'\s+(' + PUNCTUATION + ')', r'\1', text)


def remove_consecutive_punct_marks(text) -> str:
    # note that currently this gets rid of all consecutive 
    # punctuation marks while that might not be desired for all tasks.
    
    # the following regex demarks a string with 1 punctuation 
    # mark followed by 1 or more punctuation marks
    return re.sub(r'(' + PUNCTUATION + ')' + PUNCTUATION + '+', r'\1', text)


def clean_up_urls(text):
    # demarks a string starting with "http", "https" or "www." followed by any 
    # string up untill a full-stop/comma, followed by one or more whitespace/newline.
    return re.sub(r'(' + text_cleaner.URL_PATTERN + ')(.*)([.,])+([\s\n])', r'\1\2 \3 ', text)












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


def clean_html_string(
        html_str: str,
        replace_html_closing_tag_with={},
        content_parent_div={"class": "content-text"},
        top_elem="div"
) -> str:
    """
    Preprocess html string input for text cleaning by parsing text content
    specified by input, by removing and replacing html tags based on dictionary input.
    The parent div of the content to be parsed and cleaned has to be specified so the
    html cleaner can distinct between what's relevant.

    Args:
        html_str                        : html string to extract from
        replace_html_closing_tag_with   : dictionary of html tags to be convert
        content_parent_div              : the parent div of all the content to be parsed
    """

    if replace_html_closing_tag_with:
        consts.html_closing_tag_replacement.update(replace_html_closing_tag_with)

    html_soup = extract_html_from_string(html_str, content_parent_div, top_elem)
    html_soup = clean_html_tables(html_soup)
    html_soup = append_punctuation_to_tag_content(html_soup)

    text = html_soup.get_text()
    text = tidy_up_text_format(text)

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
