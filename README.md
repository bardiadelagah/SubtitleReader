# subtitleReader

This python code help to learn forieng language like english with subtitle of movies.

## Usage

You must put your subtitle file (i.e., .str or .vtt) in root directory of the project. Then run the code.

aftter run you see something like bellow in terminal.
```bash
0 .idea
1 ensub.srt
2 ensub.vtt
3 database
4 requirements.txt
5 subtitleReader.py
please_enter_one_number between 0 to 9
```

choose number of file that your subtitle(here is number 1 or 2)
Then project print something like bellow and create 4 new excel file(i.e. .xlsx) in root directory.

```bash
number of all_sentences_in_order 64
number of all_sentences_unique 64
number of all_words_in_order 996
number of all_words_unique 408
word_per_minutes 166
number of dict_in_order_new_words 328
number of dict_unique_new_words 200
```

## How it works

File and directories are something like bellow:

```bash
├── datebase                          # Test files (alternatively `spec` or `tests`)
│   ├── basic_knowledge.xlsx          # 
├── ensub.srt 
├── ensub.vtt
├── requirements.txt
└── subtitleReader.py
```
if you any word and thire meaning please insert in rows of basic_knowledge.xlsx.


after run the code subtitleReader get all words and sentences in choosen subtitle and 4 new file names like bellow are created:


```bash
ensub_dict_in_order.xlsx         
ensub_dict_unique.xlsx   
ensub_dict_in_order_new_words.xlsx
ensub_dict_unique_new_words.xlsx
```

first 2 new file create just by subtitle file.

```bash
ensub_dict_in_order.xlsx is a file that has all words base on order of showing in subtitle.
ensub_dict_unique.xlsx is a file that has all unique words base on order of showing in subtitle.
```

second 2 new file create base on words that exist in basic_knowledge.xlsx file in datebase folder.

```bash
.
├── datebase                           
│   ├── basic_knowledge.xlsx          
```

```bash
ensub_dict_in_order_new_words.xlsx is a file that has all new words base on order of showing in subtitle.
ensub_dict_unique_new_words.xlsx is a file that has all new unique words base on order of showing in subtitle.
```



## Donate us
if you like our project and it's useful, feel free to donate us.
BTC:
ETH:
TRX:
BTT:
USDT:
DOGE:
SHIB:
XMR:
Decentraland (MANA):
Please make sure to update tests as appropriate.


