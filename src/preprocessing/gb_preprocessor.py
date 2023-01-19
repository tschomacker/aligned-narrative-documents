from PyPDF2 import PdfReader
import os
import pandas as pd
import json
import re
from preprocessor import Preprocessor
import warnings

class GBPreprocessor(Preprocessor):
        
    def __call__(self, document):     
        # create the original text
        with open(document['original_path']) as f:
            contents = f.readlines()
            document_started = False
            original_text_raw = ''
            original_end_of_text_marker_found = False
            for line in contents:
                if document['original_end_of_text_marker'] in line:
                # the documents has ended so stop
                    break
                
                original_end_of_text_marker_found = True
                # exclude 'Seite' to avoid start reading at the toc
                if (document['original_start_of_text_marker'] in line) & ('Seite' not in line):
                    document_started = True
                if document_started:
                    original_text_raw = original_text_raw +' '+line
        if not original_end_of_text_marker_found:
            warnings.warn(document['original_end_of_text_marker'], 'not found in',document['original_path'])

        original_text_raw= original_text_raw.replace('\n','')
        original_text_raw= original_text_raw.replace('  ','')
        # remove footnotes and metadata
        original_text_raw = re.sub(r'\[[a-zA-Z0-9]+\]', ' ', original_text_raw)
        
        

        original_text_raw = self._general_formatting(original_text_raw)
        return original_text_raw