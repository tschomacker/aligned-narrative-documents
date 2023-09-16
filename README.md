
# Aligned Narrative Documents :books:
A collection of scripts to create a Document-aligned corpus of German Narrative Texts from four different sources of Simple Language Texts and three different sources of Standard Language Texts. Each sample in the corpus is a pair consisting of a Text in its Standard Language Version (Original) and it's Simple Language Version. The texts can be obtained from PDF, TXT, and HTML-files. Additionally, the original version is truncated to match the extent of the simplified version. 

## Getting started :rocket:

```bash
pip install -r -q requirements.txt
```

## Configure the input :card_index_dividers:
each of the scripts uses the same json-format to load data, the following table describes the json-attributes:
|Parameter| Type | Explaination | Example |
|-|-|-|-|
| simple_path |str| Local File Path to the simplified document. Should be preferred over simple_url as input source.  | `<...>/simple.pdf`|
| simple_start_page | int | PDF-pagenumber of the first PDF-page of the simple version that is processed | `6` |
| simple_first_page_number_for_removal | int | This parameter helps to remove the in-text page numbers from the actual text. This is page number written on the page of first PDF-page of the simple version. | `6` |
|simple_start_of_text_marker | str |  Text snippet, from which the simple text starts.  | `Nathan schreibt` | 
| simple_end_of_text_marker | str | Text snippet, up to which the simple text goes. | `Bis bald.` |
| simple_url | str | URL to the simplified document. |`https://www.<...>/simple.pdf`|
| original_url | str | URL to the original document. |`https://www.<...>/original.txt`|
| original_start_of_text_marker | str | Text snippet, from which the original text starts. | `Nathanael an Lothar` |
| original_end_of_text_marker | str | Last text snippet of the aligned original document. | `Lebe wohl etc. etc.` |
| title | str | Title or identifier for the text. Can be left blank if the text's source gave it a title. | `mytext` |
|simple_text_in_boxes|str| Text snippet, that should be deleted. | `Mehr Informationen` |

## The sub-datasets :jigsaw:
Our dataset contains one full-text source (MILS) and three fragment-text source (EB, KV, PV). Two scripts and four configuration json-files are needed to create these sub-datasets. They are merged in a final step.  
### MILS Corpus :construction:
uses the described json-format, stored in the file: `../../data/mils_data.json` (texts from https://www.ndr.de/fernsehen/barrierefreie_angebote/leichte_sprache/Maerchen-in-Leichter-Sprache,maerchenleichtesprache100.html)
```bash
cd src/preprocessing
python mils_preprocessor.py 
```
if you make any changes to the parser, use the corresponding unit-tests:
```bash
cd src/preprocessing
python mils_preprocessor_test.py 
```

### EB, PV, KV Corpus :construction:
uses the described json-format, stored in the files:</br>
 `../../data/eb_data.json` (texts from  https://einfachebuecher.de), </br>
  `../../data/pv_data.json`(texts from https://www.passanten-verlag.de), </br>
  and `../../data/kv_data.json`(texts from https://www.kindermannverlag.de) </br>
```bash
cd src/preprocessing
python reading_sample_preprocessor.py
```
if you make any changes to the parser, use the corresponding unit-tests:
```bash
cd src/preprocessing
python reading_sample_preprocessor_test.py
```

## Complete Corpus :books: :world_map:
Merge all previous sub-dataset in a complete corpus, and separates them in train, validate and test data. All previous scripts had to be run successfully to create the corpus. This scripts results in six files: </br>
`/val-source.txt` (Validation dataset, Original Texts) `/val-target.txt` (Validation dataset, Simple Texts)</br>
`/train-source.txt` (Train dataset, Original Texts) `/train-target.txt` (Train dataset, Simple Texts)</br>
`/test-source.txt` (Test dataset, Original Texts) `/test-target.txt` (Test dataset, Simple Texts)</br>

```bash
cd src/preprocessing
python gnats.py
```
to better download it: `tar -cvf gnats.tar.gz gnats`

## License & Acknowledments
[![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by]. The texts are partially under other licenses. We used texts from [Gutenberg-DE](https://www.projekt-gutenberg.org/info/texte/info.html) and from the [NDR Märchen in Leichter Sprache](https://www.ndr.de/fernsehen/barrierefreie_angebote/leichte_sprache/Rotkaeppchen,rotkaeppchenleichtesprache100.html) project. We would like to thank NDR very much for giving us the opportunity to make this data publicly available for the first time.

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

## Citation
Please have a look out our [CITATION file](https://github.com/tschomacker/aligned-narrative-documents/blob/main/CITATION.cff) or use the followong bibtex:
```latex
@inproceedings{SchomackerExploringAutomatic2023,
title = {{Exploring Automatic Text Simplification of German Narrative Documents}},
author = {Schomacker, Thorben and Dönicke, Tillmann and Tropmann-Frick, Marina},
booktitle = {Proceedings of the 19th Conference on Natural Language Processing (KONVENS 2023)},
language = {eng},
month = sep,
year = {2023},
copyright = {Creative Commons Attribution 4.0 International},
address = {Ingolstadt, Germany}
}
```