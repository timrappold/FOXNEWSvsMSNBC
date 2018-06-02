Author: Tim Rappold

# Project:

Political and Linguistic Polarization in Network News

## Summary:

In this project, I analyze patterns in the langauge of four current affairs shows on MSNBC and Fox News.

My goal is to identify political polarization between the two news broadcast networks, which are respectively known for their liberal and conservative political leanings. We'll be looking at two shows from each network, broadcast weeknights in competing time slots:

| Time | FOX News           | MSNBC                                |
| ---- | ------------------ | ------------------------------------ |
| 9pm  | Hannity            | Rachel Maddow Show                   |
| 10pm | The Ingraham Angle | The Last Word with Lawrence O'Donnel |

## Quick Start:

To run this project, open `client.ipynb`. This will import all the necessary modules.

Be sure to have the following dependencies installed:

`gensim`

`nltk`

`LDA



**Tools and Analysis**: All show transcripts were scraped from *foxnews.com* and *msnbc.com* using  `BeautifulSoup` and `Selenium`.  All data acquisition is kept in `scraper.py`.  Text processing was partly done in `



I'll do an exploratory data analysis and attempt a number of analyses and models.

**Domain:**  Topic modeling, sentiment analysis, text classification.

**Data:** We're looking at episode transcripts from the four different shows for the last 6 months or so. Each show was broadcast about 120 times in that time span, so the total corpus will comprise speech transcripts from about 480 hour-long episodes.

**Modes of analysis**: 

* Topic Modeling. Explore a variety of topics; e.g:

  * Trump
  * Mueller
  * Stormy Daniels
  * (North) Korea
  * (GOP) Memo
  * (Steele) Dossier
  * Putin
  * Net Neutrality

* Sentiment analysis

  

**Work Flow / Pipeline**: 

* Define a document. Could be either a paragraph in an episode, the episode itself, or the corpus of a show. Create a `document`/ `Episode` class?

   

**Known unknowns:** 

- Not sure where this is all going to go!