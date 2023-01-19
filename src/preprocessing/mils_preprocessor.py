from bs4.element import Tag, NavigableString
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from preprocessor import Preprocessor
from pg_preprocessor import PGPreprocessor
import json

class MILSPreprocessor(Preprocessor):

        
    def __call__(self, data_path="../../data/mils_data.json", csv_path="../../data/mils.csv", verbose=False):
        
        pg_preprocessor = PGPreprocessor()
        
        # Opening JSON file
        f = open(data_path)

        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        
        mils_df = pd.DataFrame()

        for document in tqdm(data,disable=not verbose):
            URL = document['simple_url']
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")

            title = URL.split(',')[1]
            title = title.replace('leichtesprache100.html','')
            corpus = 'mils'
            identifier = corpus+'-'+title

            mils_disclaimer = ' Der NDR macht Nachrichten in Leichter Sprache. Diese Nachrichten sind aus Norddeutschland. Hier können Sie diese Nachrichten lesen. Und hören. Barrierefreie Angebote ermöglichen Menschen mit Behinderung die Teilhabe am audiovisuellen Angebot des NDR.'


            sentences = []
            for paragraph in soup.find_all("p"):
                for content in paragraph.contents:
                    if type(content) == NavigableString:
                        # removes the intendation
                        content = content.replace('\xa0', '')
                        # remove sillable separation
                        content = content.replace('∙', '')
                        content = content.replace('·', '')
                        # remove line breaks
                        content = content.replace('\n', '')
                        # remove leading white space
                        if content[:1] == ' ':
                            content = content.replace(' ', '',1)
                        content = content.replace('  ', '')
                        # remove empty strings
                        if len(content) > 0:
                            sentences.append(content)
                    # add strong (emphasized) words
                    elif type(content) == Tag:
                        if content.name == 'strong':
                            if content.string is not None:
                                if len(content.string) > 0:
                                    sentences.append(content.string)

            simple_text = ' '.join(sentences)
            simple_text = simple_text.replace('  ', ' ')

            simple_text = simple_text.replace(mils_disclaimer, '')

            # remove introduction
            simple_text = simple_text.split("Das Märchen geht so:")[1]
            # remove outro
            simple_text = simple_text.split("Das war das Märchen")[0]
            
            
            # create the original text
            
            original_text = pg_preprocessor(document['original_url'])

            df_dictionary = pd.DataFrame([{'id':identifier, 
                                           'simple':simple_text,
                                          'corpus':corpus,'title':title, 'original':original_text}])
            mils_df = pd.concat([mils_df, df_dictionary], ignore_index=True)
        mils_df.to_csv(csv_path,index=False)
        return mils_df
    
if __name__=='__main__':
    mils_preprocessor = MILSPreprocessor()
    mils_preprocessor()