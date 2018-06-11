# Text Mining: Ballad Lyrics Analyzer
Use `scrapy`, `pandas` and `gensim` to analyze the lyrics of thousands of **Chinese ballads**. Use statistical features and word2vec to analyze the lyrics.

The results and part of the key processes are wrote in [jupyter notebook](http://jupyter.org). Visual results contain the distribution of mentioned cities, the seasons with the top hit and etc.

Also, `word2vec` model is derived to compute the similarity of two singers and hence can be used for recommendation.

## Dataset
All the lyrics are in **CHINESE** and hence the final jupyter notebook is writen in **CHINESE**.

## Setup
```shell
pip3 install jieba scrapy matplotlib gensim pandas
```

## Jupyter Notebook
You can run `jupyter notebook` directly to view the corresponding analysis if you have installed `jupyter notebook` in your environment. Also, you can browse the converted `notebook.html` if you cannot run `jupyter`. However, all the contents are static in `notebook.html`.
```shell
jupyter notebook
```

## Acknowledgement
This project serves as the submission of SJTU CS086 curriculum assignment.
