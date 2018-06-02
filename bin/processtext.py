# import scraper
import pickle

import re

#transcripts = scraper.main()


def load_transcripts():
    """

    :return: List of dictionaries.
        Each dictionary contains the following fields:
        'show': str. 'Hannity', 'Ingraham', 'Maddow', 'ODonnell'
        'url': str.
        'date': str.
        'transcript': str.
    """

    data_path = 'data/'

    fox_filename = data_path + 'fox_news_transcripts3.pkl'
    msnbc_filename = data_path + 'msnbc_transcripts2.pkl'

    with open(fox_filename, 'rb') as picklefile:
        fox_transcripts = pickle.load(picklefile)

    with open(msnbc_filename, 'rb') as picklefile:
        msnbc_transcripts = pickle.load(picklefile)

    return msnbc_transcripts + fox_transcripts


def get_transcripts_without_duplicates(transcripts):
    """
    Eliminate duplicates from the list of transcripts.

    """
    except_urls = \
        ['http://www.msnbc.com/transcripts/rachel-maddow-show/2018-04-12-0',
        'http://www.msnbc.com/transcripts/rachel-maddow-show/2017-12-27',
        'http://www.msnbc.com/transcripts/the-last-word/2018-04-13']

    valid_url_list = []
    clean_transcripts = []
    for i in transcripts:
        if (i['url'] not in valid_url_list) and (i['url'] not in except_urls):
            valid_url_list.append(
                i['url'])  # List is checked to avoid duplication
            clean_transcripts.append(i)

    hist = {}
    for transcript in clean_transcripts:
        hist[transcript['show']] = hist.get(transcript['show'], 0) + 1

    # Print the number of transcriptst for each show:
    print(hist)
    return clean_transcripts


def purge_transcript(text):
    """
    Remove unwanted words and characters. Combine common variants, e.g.
    "Donald J. Trump" and "President Trump" and "The President".

    """
    text = text.replace('\n', ' ')
    text = text.replace(r"[.,?!();:]", "")
    text = re.sub(u'\u2019', "'", text)  # Replace right quot mark

    # text = text.replace("\'", " ")
    text = text.replace('(CROSSTALK)', " ")
    # text = re.sub(r'^[A-Z][A-Z()\s,.]+:', ' ', text)
    text = re.sub(r'[A-Z()\s,.-]+:', ' ', text)  # Drop speaker assignment.
    text = text[150:-600]
    text = re.sub(u'\u2014', ' ', text)  # Drop em-dash
    text = re.sub(u'\u2013', ' ', text)  # Drop en-dash

    return text


class Episode(object):
    """
    Container and methods for individual episode transcripts.
    """
    def __init__(self, transcript_element):
        """

        :param transcript_element:
        """
        self.show = transcript_element['show']

        if self.show == 'ODonnel':
            self.show = 'ODonnell'  # Fix spelling error

        if self.show in ['Hannity', 'Ingraham']:
            self.network = 'FOX'
        elif self.show in ['Maddow', 'ODonnell']:
            self.network = 'MSNBC'
        else:
            self.network = None

        self.date = transcript_element['date']
        self.url = transcript_element['url']
        self.transcript = self.purge_transcript(transcript_element['transcript'])

    def purge_transcript(self, text):
        """
        Remove unwanted words and characters. Combine common variants, e.g.
        "Donald J. Trump" and "President Trump" and "The President".

        :param text: str.
        :return: text (str).
        """

        text = text.replace('\n', ' ')
        # text = text[170:-600]             # Drop first and last chunk of chars.
        text = re.sub(u'\u2014', ' ', text)  # Drop em-dash
        text = re.sub(u'\u2013', ' ', text)  # Drop en-dash
        text = re.sub(u'\u201C', ' ', text)  # Drop left double quot mark
        text = re.sub(u'\u201D', ' ', text)  # Drop right double quot mark
        text = re.sub(u'\u2019', "'", text)  # Replace right quot mark

        text = re.sub("`", "'", text)  # Drop en-dash
        text = re.sub(u'\u2035', "'", text)  # Drop left single apost mark

        text = re.sub(r'[.,?!();"\-]', "", text)  # Drop most punctuation

        # Drop apostrophe only if NOT using a Lemmatizer (drop if Stemmer):
        text = re.sub(r"'", "", text)  # Replace apostrophe with space.

        text = text.replace("O'DONNELL", "ODONNELL")
        text = text.replace('CROSSTALK', " ")
        text = re.sub(r'[A-Z()\s,.-]+:', ' ', text)   # Drop speaker assignment
        text = re.sub(r'[$:/]', " ", text)  # Drop ':' after drop speaker assignment

        text = text.lower()

        if self.show == 'Hannity':
            text = re.sub(r'hannity', ' ', text)
            text = re.sub(r'sean', ' ', text)

        if self.show == 'Ingraham':
            text = re.sub(r'ingraham', ' ', text)
            text = re.sub(r'laura', ' ', text)

        if self.show == 'Maddow':
            text = re.sub(r'maddow', ' ', text)
            text = re.sub(r'rachel', ' ', text)

        if self.show == 'ODonnell':
            text = re.sub(r'odonnell', ' ', text)
            text = re.sub(r"o'donnell", ' ', text)
            text = re.sub(r"o donnell", ' ', text)
            text = re.sub(r'lawrence', ' ', text)

        def _custom_replacements(text):
            text = text.replace('president trump', 'president_trump')
            text = text.replace('president obama', 'president_obama')
            text = text.replace('michelle obama', 'michelle_obama')
            text = text.replace('obama care', ' obama_care')
            text = text.replace('obamacare', ' obama_care')

            text = text.replace(' obama ', ' president_obama ')

            text = text.replace('trump university', 'trump_university')
            text = text.replace('trump organization', 'trump_organization')
            text = text.replace('trump tower', 'trump_tower')

            text = text.replace('donald trump jr', 'donald_trump_jr')
            text = text.replace(' trump jr ', ' donald_trump_jr ')
            text = text.replace('donald trump', 'president_trump')

            text = text.replace(' the president ', ' president_trump ')

            text = text.replace('ivanka trump', 'ivanka_trump')
            text = text.replace('ivanka ', ' ivanka_trump ')

            text = text.replace(' trump ', ' president_trump ')

            text = text.replace('roy moore', 'roy_moore')
            text = text.replace(' moore ', ' roy_moore ')

            text = text.replace('michael avenatti', 'michael_avenatti')
            text = text.replace(' avenatti', ' michael_avenatti')

            text = text.replace('hillary clinton', ' hillary_clinton')
            text = text.replace('hillary ', ' hillary_clinton ')

            text = text.replace('michael cohen', 'michael_cohen')

            text = text.replace('stormy daniels', 'stormy_daniels')
            text = text.replace('stormy daniel', 'stormy_daniels')

            text = text.replace('robert mueller', 'robert_mueller')
            text = text.replace('bob mueller', 'robert_mueller')
            text = text.replace('mueller investigation', 'mueller_investigation')
            text = text.replace(' mueller', ' robert_mueller')

            text = text.replace('rod rosenstein', 'rod_rosenstein')
            text = text.replace(' rosenstein', ' rod_rosenstein')

            text = text.replace('james comey', 'james_comey')
            text = text.replace(' comey', ' james_comey')

            text = text.replace('john kelly', 'john_kelly')

            text = text.replace('deep state', 'deep_state')
            text = text.replace('white house', 'white_house')
            text = text.replace('fake news', 'fake_news')

            text = text.replace('liberal media', 'liberal_media')
            text = text.replace('left wing media', 'liberal_media')
            text = text.replace('left wing media', 'liberal_media')

            text = text.replace('conservative media', 'conservative_media')
            text = text.replace('right wing media', 'conservative_media')

            text = text.replace(' media', ' media_')

            return text

        text = _custom_replacements(text)

        return text


def main():
    transcripts = load_transcripts()
    transcripts = get_transcripts_without_duplicates(transcripts)

    return transcripts


if __name__ == "__main__":

    main()
