# Import libraries.

# ---------------------------------------------------------------

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics

# ---------------------------------------------------------------

# import connection string from another file (.env here)
load_dotenv()
conn_string = os.getenv('mongo_string')

# Connect to MongoDB
cluster = MongoClient(conn_string)          # Connect to the cluster using connection string in the .env file.
db = cluster['Questions']                   # Connect to 'Questions' database in the cluster.
collection1 = db['MCQ']                     # Connect to 'MCQ' collection in 'Questions' database.
collection2 = db['One Word Answers']        # Connect to 'One Word Answers' collection in 'Questions' database.
collection3 = db['results']                 # Connect to 'results' collection in 'Questions' database.

# ---------------------------------------------------------------

mcq_score = 0                               # Score for MCQ questions.
owa_score = 0                               # Score for one word answer questions.

# Read data using Python from the MongoDB collection & display as questions.

print('Welcome to the quiz app\n')
print('------------------------\n')
name = input('Enter your name\n')

if input('press \'y\' to start\n'):
    mcq_questions = collection1.find({})
    owa_questions = collection2.find({})

    for mcq in mcq_questions:
        print(f"{mcq['_id']}. {mcq['Question']}")
        print(f"\ta: {mcq['Options']['a']}\n\tb: {mcq['Options']['b']}\n\tc: {mcq['Options']['c']}\n\td: {mcq['Options']['d']}")
        answer = input('Enter the correct option: ')
        if answer is mcq['Correct']:
            mcq_score+=1

    for owa in owa_questions:
        print(f"{owa['_id']}. {owa['Question']}")
        answer = input('Enter a one word answer: ').lower()
        if type(owa['Answer']) == list and answer in [answer_list.lower() for answer_list in owa['Answer']]:
            owa_score+=1
        elif answer == str(owa['Answer']).lower():
            owa_score+=1

# ---------------------------------------------------------------

# Display total marks achieved after questions are answered.
print('\nScoresheet')
print('------------------------')
print(f'Name: {name}')
print(f'MCQ score: {mcq_score}')
print(f'One word answer score: {owa_score}')

# ---------------------------------------------------------------

# Insert results into 'results' collection.
collection3.insert_one({'name': name, 'mcq_score': mcq_score, 'owa_score': owa_score})

# ---------------------------------------------------------------

# Retrieve past results data from 'results' collection.
data = collection3.find({})
df = pd.DataFrame(list(data))
df['total'] = df.mcq_score+df.owa_score

# Calculate mean of scores.
mcq_avg = statistics.mean(df['mcq_score'])
owa_avg = statistics.mean(df['owa_score'])
total_avg = statistics.mean(df['total'])
total_score = mcq_score + owa_score

# ---------------------------------------------------------------

# Create a dictionary for a dataframe of required format for the chart.
score_label = ['Your score', 'Average', 'Your score', 'Average', 'Your score', 'Average']
score_type = ['MCQs', 'MCQs', 'OWAs', 'OWAs', 'TOTAL', 'TOTAL']
scores = [mcq_score, mcq_avg, owa_score, owa_avg, total_score, total_avg]

new_data = {
    'score_label': score_label,
    'score_type': score_type,
    'scores': scores
}

# Create dataframe for chart
new_df = pd.DataFrame(new_data)

# ---------------------------------------------------------------

# Create chart
sns.set(style="darkgrid")
plt.style.use("dark_background")
plt.rcParams.update({"grid.linewidth": 0.5, "grid.alpha": 0.5})
plt.figure(figsize=(6, 6))

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