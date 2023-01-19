from PyPDF2 import PdfReader
import os
import pandas as pd
import json
import re
from preprocessor import Preprocessor
from gb_preprocessor import GBPreprocessor
from pg_preprocessor import PGPreprocessor

from tqdm.auto import tqdm

class ReadingSamplePreprocessor(Preprocessor):
    
    def __init__(self):
        # Parser for the original version
        self.gb_preprocessor = GBPreprocessor()
        self.pg_preprocessor = PGPreprocessor()
        
    def _create_simple_text(self, document):
        """
        Create the simple text
        """
        
        reader = PdfReader(document['simple_path'])
        simple_text = ""
        page_number = document['simple_first_page_number_for_removal']
        clean_page_words = []
        # parse document pagewise
        ## skip pages with irrelevant information
        first_page = True
        for page in reader.pages[(document['simple_start_page']-1):]:
            page_text = page.extract_text()
            
            page_text = page_text.replace('\n',' ')
            
            #insert blank to improve page number removal
            page_text =  page_text.replace("1. kapitel",' 1.kapitel')

            page_text = page_text.replace("  ",' ')
            # remove the page numbers
            page_words = page_text.split(' ')
            
            for word in page_words:
                if 0 < len(word):
                    number_str = ''
                    for i in range(len(word)):
                        if word[i] in "0123456789":
                            number_str += word[i]
                        else:
                            break
                    if 0 < len(number_str):
                        if int(number_str) == page_number:
                            word = word.replace(number_str, '', 1)
                            page_number += 1
                clean_page_words.append(word)
        simple_text = ' '.join(clean_page_words)
        
        # remove irrelevant information
        if 'simple_start_of_text_marker' in document.keys():
            page_text_fragments = simple_text.split(document['simple_start_of_text_marker'])
            #print('fragments:',len(page_text_fragments),'remove:', page_text_fragments[0])
            if len(page_text_fragments) < 2:
                print('Warning: ', document['simple_start_of_text_marker'], 'does not seem to work as an simple_start_of_text_marker, in:\n', simple_text)
            simple_text = document['simple_start_of_text_marker'] + page_text_fragments[1]
        
        if 'simple_end_of_text_marker' in document.keys():
            simple_text_fragments = simple_text.split(document['simple_end_of_text_marker'])
            if len(simple_text_fragments) < 2:
                print('Warning: ', document['simple_end_of_text_marker'], 'does not seem to work as an simple_end_of_text_marker in', simple_text)
            simple_text = simple_text_fragments[0] + document['simple_end_of_text_marker'] 
        simple_text = simple_text.replace('Ende der Leseprobe','')
        
        if 'simple_text_in_boxes' in document.keys():
            for box_text in document['simple_text_in_boxes']:
                simple_text = simple_text.replace(box_text, '')
        
        simple_text = self._general_formatting(simple_text)
        return simple_text
        
    def __call__(self, data_path, csv_path, corpus, verbose):     
        # Opening JSON file
        f = open(data_path)

        # returns JSON object as 
        # a dictionary
        data = json.load(f)

        """ parser documents from eb corpus

        Parameters
        ----------
        original_end_of_text_marker : str
            First line of text after the original text matches the simple one
        original_start_of_text_marker : str
            Last line of text before the original text matches the simple one


        Returns
        -------
        DataFrame
            Each row containing the original and simple version of a document
        """

        eb_df = pd.DataFrame()
        for document in tqdm(data, desc="doc(s) from "+corpus,disable=not verbose):
            simple_text = self._create_simple_text(document)
            
            if type(document['original_url']) == list:
                # projekt-gutenberg.org original
                original_text = self.pg_preprocessor(document)
            elif ".txt" in document['original_url']:
                # gutenberg.org original
                original_text = self.gb_preprocessor(document)
            elif ".html" in document['original_url']:
                # projekt-gutenberg.org original
                original_text = self.pg_preprocessor(document)
            
            title = document['title']
            df_dictionary = pd.DataFrame([{'id':corpus+'-'+title, 
                                            'simple':simple_text,
                                            'corpus':corpus,
                                            'original': original_text,
                                            'title':title}])
            eb_df = pd.concat([eb_df, df_dictionary], ignore_index=True)
        eb_df.to_csv(csv_path,index=False)
        return eb_df
    
    
if __name__=='__main__':
    eb_preprocessor = ReadingSamplePreprocessor()
    eb_preprocessor(data_path="../../data/eb_data.json", csv_path="../../data/eb.csv", corpus='eb', verbose=True)
    eb_preprocessor(data_path="../../data/pv_data.json", csv_path="../../data/pv.csv", corpus='pv', verbose=True)
    eb_preprocessor(data_path="../../data/kv_data.json", csv_path="../../data/kv.csv", corpus='kv', verbose=True)