import scraper

transcripts = scraper.main()


def get_transcripts_without_duplicates(transcripts):
    """
    Eliminate duplicates.
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
    Remove unwanted words, including:
        SPEAKERS:
        Comments from this list: (CROSSTALK)

    """
    text = text.replace('\n', ' ')
    text = text.replace(r"[.,?!();:]", "")
    # text = text.replace("\'", " ")
    text = text.replace('(CROSSTALK)', " ")
    # text = re.sub(r'^[A-Z][A-Z()\s,.]+:', ' ', text)
    text = re.sub(r'[A-Z()\s,.-]+:', ' ', text)  # Drop speaker assignment.
    text = text[150:-600]
    text = re.sub(u'\u2014', ' ', text)  # Drop em-dash
    text = re.sub(u'\u2013', ' ', text)  # Drop en-dash

    return text


class Episode(object):
    def __init__(self, transcript_element):
        self.show = transcript_element['show']
        self.date = transcript_element['date']
        self.url = transcript_element['url']
        self.transcript = purge_transcript(transcript_element['transcript'])

    def purge_transcript(self, text):
        """
        Remove unwanted words, including:
            SPEAKERS:
            Comments from this list: (CROSSTALK)

        """
        text = text.replace('\n', ' ')
        text = text.replace(r"[.,?!();:]", "")
        # text = text.replace("\'", " ")
        text = text.replace('(CROSSTALK)', " ")
        # text = re.sub(r'^[A-Z][A-Z()\s,.]+:', ' ', text)
        text = re.sub(r'[A-Z()\s,.-]+:', ' ', text)  # Drop speaker assignment.
        text = text[150:-600]
        text = re.sub(u'\u2014', ' ', text)  # Drop em-dash
        text = re.sub(u'\u2013', ' ', text)  # Drop en-dash

        return text


def main():
    pass

if __name__ == "__main__":

    clean_transcripts = get_transcripts_without_duplicates(transcripts)