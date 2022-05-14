# Import libraries.
import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
import os

# import connection string from another file (.env here)
load_dotenv()
conn_string = os.getenv('mongo_string')

# Connect to MongoDB
cluster = MongoClient(conn_string)
db = cluster['Questions']
collection1 = db['MCQ']                     # The collection in your database
collection2 = db['One Word Answers']        # The collection in your database
collection3 = db['results']

# Read data using Python from the MongoDB collection
#print(collection1.find_one({'_id': 1}))

# Display questions for user in appropriate form using any Python code
mcq_score = 0
owa_score = 0
print(type(collection2.find_one({'_id': 5})['Answer'][0]))


print('Welcome to the quiz app\n')
print('------------------------\n')
name = input('Enter your name')

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
            print(answer)
            owa_score+=1
        elif answer == str(owa['Answer']).lower():
            owa_score+=1
print(mcq_score)
print(owa_score)

# (Use numbered bullets for MCQ options for user to enter number corresponding to their answer,
# mention 'one word only' for the remaining questions and accept only a one word answer)

# AND

# Allot 1 mark for each correct MCQ, 2 marks for each correct single word answer.
# Store the marks for each question in a list/dictionary/set or any other data structure you deem fit.





# After all questions are answered, display total marks achieved.



# Use matplotlib or seaborn to create a graph highlighting performance in MCQ vs single word answers for
# no. of questions answered correctly.
# Use any type of graph you deem fit.

