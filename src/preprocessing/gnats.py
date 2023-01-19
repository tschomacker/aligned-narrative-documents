import pandas as pd
import os
import warnings

def main(output_dir="../../data/gnats"):
    corpora_strs = ['mils', 'eb', 'pv']
    
    val_doc_ids = ['mils-stadtmusikanten','eb-jekyll','pv-schimmelreiter']
    test_doc_ids = ['mils-bruder','eb-christo','pv-sandmann']
    
    src_lang = "de_OR"
    trg_lang = "de_SI"
    
    gnats_df = pd.DataFrame()
    for corpus_str in corpora_strs:
        gnats_df = pd.concat([gnats_df, 
                              pd.read_csv(os.path.join('..','..','data',corpus_str+'.csv'))], 
                             ignore_index=True)
    val_src_texts = []
    val_trg_texts = []
    
    test_src_texts = []
    test_trg_texts = [] 
    
    train_src_texts = []
    train_trg_texts = [] 
    for _, row in gnats_df.iterrows():
        if row['id'] in val_doc_ids:
            val_src_texts.append(src_lang+' '+row['original']+'\n')
            val_trg_texts.append(trg_lang+' '+row['simple']+'\n')
        elif row['id'] in test_doc_ids:
            test_src_texts.append(src_lang+' '+row['original']+'\n')
            test_trg_texts.append(trg_lang+' '+row['simple']+'\n')
        else:
            train_src_texts.append(src_lang+' '+row['original']+'\n')
            train_trg_texts.append(trg_lang+' '+row['simple']+'\n')
    
    if len(val_src_texts) != len(val_doc_ids):
        warnings.warn("Defined no val documents is "+str(len(val_src_texts))+" but "+str(len(val_doc_ids))+" where found")
    if len(test_src_texts) != len(test_doc_ids):
        warnings.warn("Defined no test documents is "+str(len(test_doc_ids))+" but "+str(len(test_src_texts))+" where found")
    
    for file_name, lines in zip(['/val-source.txt','/val-target.txt', 
                                 '/test-source.txt','/test-target.txt',
                                '/train-source.txt','/train-target.txt'], 
                                [val_src_texts, val_trg_texts,
                                test_src_texts, test_trg_texts,
                                train_src_texts, train_trg_texts]):
        
        with open(output_dir+file_name, "w") as output_file:
            output_file.writelines(lines)
    
if __name__=='__main__':
    main()