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
a = 5
b = 4
c = a+b

score_label = ['Your score', 'Average', 'Your score', 'Average', 'Your score', 'Average']
score_type = ['MCQs', 'MCQs', 'OWAs', 'OWAs', 'TOTAL', 'TOTAL']
scores = [a, mcq_avg, b, owa_avg, c,total_avg]

new_data = {
    'score_label': score_label,
    'score_type': score_type,
    'scores': scores
}

sns.set(style="darkgrid")
plt.style.use("dark_background")
plt.rcParams.update({"grid.linewidth": 0.5, "grid.alpha": 0.5})
plt.figure(figsize=(6, 6))

new_df = pd.DataFrame(new_data)

sns.set_palette(sns.color_palette("Paired"))
ax = sns.barplot(x='score_type',
                 y='scores',
                 hue='score_label',
                 data=new_df,
                 edgecolor='black')

ax.set_title('Score Analysis')
ax.set_ylabel('Score Value')
ax.set_xlabel('Score Type')

plt.show()
