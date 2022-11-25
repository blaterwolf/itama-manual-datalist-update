import pandas as pd
from nltk.corpus import stopwords

df = pd.read_csv('dataset_with_filtered_tags.csv')

english_stopwords = set(stopwords.words('english'))

unnecessary_words = set(
    ['fact', 'check', 'philippines', 'false', 'hindi', 'totoo', 'fake', 'news', 'although', 'link', 'send', 'click', 'report', 'yes', 'according', 'dont', 'shouldnt'])

new_result = []

for index, row in df.iterrows():
    filter_stopwords = list(filter(lambda x: x not in english_stopwords,
                                   row['tags'].split(', ')))
    filter_unnecessary_words = list(
        filter(lambda x: x not in unnecessary_words, filter_stopwords))
    if len(filter_unnecessary_words) > 5:
        final_tags = ", ".join(filter_unnecessary_words)
        # pasok sa dataset ulit
        data_needed = {
            'fb_link': row['fb_link'],
            'text': row['text'],
            'post_date': row['post_date'],
            'image_link': row['image_link'],
            'tags': final_tags,
        }

        new_result.append(data_needed)
        print(index, "\n")
    else:
        continue

print("ALL DONE. Saving to csv.")
dataset = pd.DataFrame.from_records(new_result)
dataset.to_csv(f'final_dataset.csv', index=False)
