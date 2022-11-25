from os import remove
import pandas as pd
import re
from collections import Counter
from tl_stopwords import tl_stopwords

df = pd.read_csv('dataset_text_edited.csv')

month_name = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

new_result = []

punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

for index, row in df.iterrows():
    # >> Seperate data for word counting
    current_text = row['text'].split(" ")
    without_links = [x for x in current_text if not re.search(
        r'^https?:\/\/.*[\r\n]*', x)]
    without_puncs = [re.sub(r'[^\w\s]', '', x) for x in without_links]
    # current_text = row['text'].lower()
    title_case_only = [word for word in without_puncs if word.istitle()]
    remove_repeating = sorted(set(title_case_only),
                              key=lambda x: title_case_only.index(x))
    remove_months = [x for x in remove_repeating if x not in month_name]
    lower_case_and_stopwords = [
        word.lower() for word in remove_months if not word.lower() in tl_stopwords]

    tags = ", ".join(lower_case_and_stopwords)

    data_needed = {
        'fb_link': row['fb_link'],
        'text': row['text'],
        'post_date': row['post_date'],
        'image_link': row['image_link'],
        'tags': tags,
    }

    new_result.append(data_needed)
    print(index, "\n")

print("ALL DONE. Saving to csv.")
dataset = pd.DataFrame.from_records(new_result)
dataset.to_csv(f'dataset_with_tags.csv', index=False)
