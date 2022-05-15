# Import libraries.
import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics

# import connection string from another file (.env here)
load_dotenv()
conn_string = os.getenv('mongo_string')

# Connect to MongoDB
cluster = MongoClient(conn_string)
db = cluster['Questions']
collection1 = db['MCQ']                     # The collection in your database.
collection2 = db['One Word Answers']        # The collection in your database.
collection3 = db['results']

mcq_score = 0                               # Score for MCQ questions.
owa_score = 0                               # Score for one word answer questions.

# Read data using Python from the MongoDB collection
"""
Project segment aim:
Display questions for user in appropriate form using any Python code

(Use numbered bullets for MCQ options for user to enter number corresponding to their answer,
mention 'one word only' for the remaining questions and accept only a one word answer)
AND
Allot 1 mark for each correct MCQ, 2 marks for each correct single word answer.
Store the marks for each question in a list/dictionary/set or any other data structure you deem fit.
"""

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

# After all questions are answered, display total marks achieved.
print('\nScoresheet')
print('------------------------')
print(f'Name: {name}')
print(f'MCQ score: {mcq_score}')
print(f'One word answer score: {owa_score}')

# Insert results into 'result' collection.
collection3.insert_one({'name': name, 'mcq_score': mcq_score, 'owa_score': owa_score})

"""
Aim for the analysis section:
Use matplotlib or seaborn to create a graph highlighting performance in MCQ vs single word answers for
no. of questions answered correctly.
Create a comparison of current user's scores with the average scores for each type and total.
Use any type of graph you deem fit.
"""

# Retrieve past results data from 'result' collection.
data = collection3.find({})
df = pd.DataFrame(list(data))
df['total'] = df.mcq_score+df.owa_score

# Calculate mean of scores.
mcq_avg = statistics.mean(df['mcq_score'])
owa_avg = statistics.mean(df['owa_score'])
total_avg = statistics.mean(df['total'])
total_score = mcq_score + owa_score

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