from bs4.element import Tag, NavigableString
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import json
from preprocessor import Preprocessor

class PGPreprocessor(Preprocessor):
    """
    Preprocessor for data from projekt-gutenberg.de
    """

    def __call__(self, document):
        input_data = document['original_url']
        if type(input_data) == str:
            input_data = [input_data]
        raw_text = ''
        for URL in input_data:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            for paragraph in soup.find_all(["p","h4"]):
                for content in paragraph.contents:
                    if type(content) == NavigableString:
                        # skip toc information
                        if content not in ['Inhalt']:
                            raw_text = raw_text + ' ' + content
                    elif type(content) == Tag:
                        # convert the images to text
                        if content.name == 'img':
                            # Get first letter from image name
                            first_letter = content["src"].replace('bilder/','')
                            first_letter = first_letter.replace('-1.gif','')
                            first_letter= first_letter.upper()
                            raw_text = raw_text + ' ' + first_letter + content.string
                        # add formatted text
                        elif content.name in ['i', 'tt', 'span']:
                            raw_text = raw_text + ' ' + content.string
                        # tags that usually have no content or only the title and author of the document
                        elif content.name in ['br','h5','a','div']:
                            pass
                        else:
                            print('Warning! unparsed tag:', content.name,' - ', content.string)
        # truncate original to fit the simple version
        if 'original_start_of_text_marker' in document.keys():
            original_start_of_text_marker = document['original_start_of_text_marker']
            if original_start_of_text_marker is not None:
                raw_text_fragments = raw_text.split(original_start_of_text_marker)
                if len(raw_text_fragments) < 2:
                    print('Warning: ', original_start_of_text_marker, 'does not seem to work as an original_start_of_text_marker')
                raw_text = original_start_of_text_marker + raw_text_fragments[1]
        
        if 'original_end_of_text_marker' in document.keys():
            original_end_of_text_marker = document['original_end_of_text_marker']
            if original_end_of_text_marker is not None:
                raw_text_fragments = raw_text.split(original_end_of_text_marker)
                if len(raw_text_fragments) < 2:
                    print('Warning: ', original_end_of_text_marker, 'does not seem to work as an original_end_of_text_marker in', raw_text)
                raw_text = raw_text_fragments[0] + original_end_of_text_marker
        return self._general_formatting(raw_text)