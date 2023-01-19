from PyPDF2 import PdfReader
import os
import pandas as pd
import json
import re

class Preprocessor:
    
    def _general_formatting(self, raw_text):
        # unify Quotation marks
        quotation_mark = "'"
        raw_text= raw_text.replace('«',quotation_mark)
        raw_text= raw_text.replace('»',quotation_mark)
        raw_text= raw_text.replace('»',quotation_mark)
        raw_text= raw_text.replace('„',quotation_mark)
        raw_text= raw_text.replace('“',quotation_mark)
        raw_text= raw_text.replace('"',quotation_mark)


        # remove metadata
        raw_text= raw_text.replace('_',quotation_mark)

        # remove new lines and tabs
        raw_text=raw_text.replace('\n',' ')
        raw_text=raw_text.replace('\t',' ')
        raw_text=raw_text.replace('\xa0',' ')
        raw_text=raw_text.replace('     ',' ')
        raw_text=raw_text.replace('    ',' ')
        raw_text=raw_text.replace('  ',' ')

        raw_text=raw_text.replace('  ',' ')


        # remove leading white space
        if raw_text[:1] == ' ':
            raw_text = raw_text.replace(' ', '',1)

        return raw_text