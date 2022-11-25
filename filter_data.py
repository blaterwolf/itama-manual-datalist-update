import enum
import os
import pandas as pd
import re
from tl_stopwords import tl_stopwords
from nltk.corpus import stopwords
english_stopwords = set(stopwords.words('english'))

unnecessary_words = set(
    ['aniya', 'noong', 'haynako', 'fact', 'check', 'philippines', 'false', 'hindi', 'totoo', 'fake', 'news', 'although', 'link', 'send', 'click', 'report', 'yes', 'according', 'dont', 'shouldnt'])


df = pd.read_csv('raw_dataset.csv')

new_result = []

month_name = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

for index, row in df.iterrows():
    # gawing list yung each text
    os.system("cls")
    current_text = str(row['text']).split("\n")
    without_blanks = [x for x in current_text if x != '']
    without_links = [x for x in without_blanks if not re.search(
        r'^https?:\/\/.*[\r\n]*', x)]
    without_hashtag = [x for x in without_links if not re.search(
        r'^#\w+$', x)]
    without_sources = [x for x in without_hashtag if not re.search(
        r'(?:^|\W)Sources(?:$|\W)', x)]

    # ito yung magpapakita sa flutter.
    current_text = ' '.join(without_sources)
    print(index, "\n")

    # reference lang.
    current_id = str(row['fb_link'].split('/')[-1])

    # create tags.
    tag_text = current_text.split(' ')
    without_links = [x for x in tag_text if not re.search(
        r'^https?:\/\/.*[\r\n]*', x)]
    without_puncs = [re.sub(r'[^\w\s]', '', x) for x in without_links]
    # current_text = row['text'].lower()
    title_case_only = [word for word in without_puncs if word.istitle()]
    remove_repeating = sorted(set(title_case_only),
                              key=lambda x: title_case_only.index(x))
    remove_months = [x for x in remove_repeating if x not in month_name]
    lower_case_and_stopwords = [
        word.lower() for word in remove_months if not word.lower() in tl_stopwords]
    filter_stopwords = list(filter(lambda x: x not in english_stopwords,
                                   lower_case_and_stopwords))
    filter_unnecessary_words = list(
        filter(lambda x: x not in unnecessary_words, filter_stopwords))

    tags = ", ".join(filter_unnecessary_words)

    data_needed = {
        'fb_link': row['fb_link'],
        'text': current_text,
        'post_date': row['post_date'],
        'image_link': row['image_link'],
        'tags': tags,
        'fb_link_id': current_id,
    }

    new_result.append(data_needed)

print("ALL DONE. Saving to csv.")
dataset = pd.DataFrame.from_records(new_result)
dataset.to_csv(f'final_dataset.csv', index=False)
