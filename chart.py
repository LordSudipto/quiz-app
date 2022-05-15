# Create the desirable chart before adding the snippet into main

import seaborn as sns
import matplotlib.pyplot as plt
from pymongo import MongoClient
import os
from dotenv import load_dotenv

import pandas as pd

# import connection string from another file (.env here)
load_dotenv()
conn_string = os.getenv('mongo_string')

# Connect to MongoDB
cluster = MongoClient(conn_string)
db = cluster['Questions']
collection3 = db['results']


data = collection3.find({})
df = pd.DataFrame(list(data))
df['total'] = df.mcq_score+df.owa_score
mcq_avg = sum(df['mcq_score'])/len(df['mcq_score'])
owa_avg = sum(df['owa_score'])/len(df['owa_score'])
total_avg = sum(df['total'])/len(df['total'])
print(df)
a = 3
b = 4
c = a+b

score_label = ['Your MCQ score', 'Avg MCQ score', 'Your OWA score', 'Avg OWA score', 'Your total score', 'Av/g total score']
score_type = ['MCQs', 'MCQs', 'OWAs', 'OWAs', 'TOTAL', 'TOTAL']
scores = [a, b, mcq_avg, owa_avg, c,total_avg]

new_data = {
    'score_label': score_label,
    'score_type': score_type,
    'scores': scores
}

new_df = pd.DataFrame(new_data)
print(new_df)

sns.barplot(x = 'score_label',
            y = 'scores',
            hue = 'score_type',
            data = new_df)

plt.show()
