## Fletcher MVP 

Author: Tim Rappold

# Project:

Political and Linguistic Polarization in Network News

## MVP Summary:

The goal of this project is to quantify, contextual, and (moonshot) model differences among news shows on two news broadcast networks, Fox News and MSNBC, respectively known for their conservative and liberal political leanings. We'll be looking at two show from each network which are broadcast weeknights in competing time slots:

| Time | FOX News           | MSNBC                                |
| ---- | ------------------ | ------------------------------------ |
| 9pm  | Hannity            | Rachel Maddow Show                   |
| 10pm | The Ingraham Angle | The Last Word with Lawrence O'Donnel |

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