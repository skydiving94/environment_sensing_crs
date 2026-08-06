"""
Please refer to notion page for details in how we generate evaluation dataset
https://www.notion.so/zhejian/Frame-Evaluation-Framework-d25377bd7e554df19d4770eef282d616?pvs=4

Steps Summary:
1. Select the user with more than 21 rating history. There 154,524 users with more than 21 rating history.
2. Use 21 as the target movie and previous 20 as browsing history ordering by timestamp.
3. Get browse_history_movieTitle, target_movieTitle, and target_movie_summary(using LLM) and save into dict.
4. Use user_simulator prompt to generate user_start seeking text.
"""

import pandas as pd
from openai import OpenAI
import argparse
import json
from tqdm import tqdm


def my_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument('--api_key', type=str, default=None)
    args = parse.parse_args()
    return args

SAMPLE_SIZE = 100
MOVIE_SUMMARY_PROMPT_PATH = "../../../resources/prompts/task_movie_summary/v0.txt"
MOVIE_SUMMARY_PROMPT = ""
USER_SIMULATOR_PROMPT_PATH = "../../../resources/prompts/task_user_simulator/v0.txt"
USER_SIMULATOR_PROMPT = ""
TEST_SAMPLE_PATH = "./test_sample.json"


with open(MOVIE_SUMMARY_PROMPT_PATH, 'r') as file:
    MOVIE_SUMMARY_PROMPT = file.read()

with open(USER_SIMULATOR_PROMPT_PATH, 'r') as file:
    USER_SIMULATOR_PROMPT = file.read()

ratings = pd.read_csv('../../../dataset/ml-25m/ratings.csv')
movies = pd.read_csv('../../../dataset/ml-25m/movies.csv')

user_gt_21 = ratings.groupby('userId').size().reset_index(name='count')
user_gt_21 = user_gt_21[user_gt_21["count"] > 21]

print("Number of user with greater than 21 movie rating sequence: ", user_gt_21.shape)    

args = my_parse()
client = OpenAI(api_key=args.api_key)

def get_target_movie_summary(movieTitle, llm=client):
    prompt = MOVIE_SUMMARY_PROMPT.format(target=movieTitle)
    message = [{"role": "user", "content": prompt}]

    response = llm.chat.completions.create(model="gpt-3.5-turbo",
        messages=message,
        stream=False,
        timeout=360,
        temperature=0)
    return response.choices[0].message.content
 

def get_user_simulator_start_text(movie_summary, browse_history, llm=client):
    prompt = USER_SIMULATOR_PROMPT.format(movie_summary=movie_summary, browse_history=browse_history)
    message = [{"role": "user", "content": prompt}]

    response = llm.chat.completions.create(model="gpt-3.5-turbo",
        messages=message,
        stream=False,
        timeout=360,
        temperature=0)
    return response.choices[0].message.content
    

# Sample 200 users with more than 21 rating history, cause some will been removed due to timestamp range
sampled_users = user_gt_21.sample(SAMPLE_SIZE * 4, random_state=42)
test_samples: list = []
# For each user, order the rating by timestamp and select the first 21 ratings
cnt = 0
for user_id in tqdm(sampled_users['userId']):
    temp_test_sample = {}
    user_ratings = ratings[ratings['userId'] == user_id].sort_values(by='timestamp', ascending=True)
    # Remove case when timestamps are too close to each other, assume at least 1 hour between each rating
    if user_ratings['timestamp'].max() - user_ratings['timestamp'].min() <= 60 * 60 * len(user_ratings): 
        # print(f"Timestamp range {user_ratings['timestamp'].max() - user_ratings['timestamp'].min()} too close, skip this user")
        continue
    
    temp_test_sample["userId"] = user_id
    movie_seq = user_ratings['movieId'].head(21).tolist()
    temp_test_sample["browse_history_movieId"] = movie_seq[:20]
    assert len(temp_test_sample["browse_history_movieId"]) == 20, "Incorrect number of browse history movies"
    temp_test_sample["target_movie"] = movie_seq[20]
    
    # movieId to title mapping
    browse_history_movieTitle = [str(movies[movies.movieId==x]['title'].values[0]) for x in temp_test_sample["browse_history_movieId"]]

    temp_test_sample["browse_history_movieTitle"] = browse_history_movieTitle
    
    # set target movieId and moiveTitle
    temp_test_sample["target_movieId"] = movie_seq[20] # the 21st movie as target
    temp_test_sample["target_movieTitle"] = str(movies[movies.movieId==movie_seq[20]]['title'].values[0])

    
    # Set target movie summary
    temp_test_sample["target_movie_summary"] = get_target_movie_summary(temp_test_sample["target_movieId"])
    
    # Set user starting text to start conversation from seeker.
    browseHistory = str(temp_test_sample["browse_history_movieTitle"])
    temp_test_sample["seeker_start"] = get_user_simulator_start_text(movie_summary=temp_test_sample["target_movieTitle"], 
                                            browse_history=browseHistory)
    

    test_samples.append(temp_test_sample)
    
    # Write to json file 
    json.dump(temp_test_sample, open(TEST_SAMPLE_PATH, 'a+'), indent=4)

    
    if len(test_samples) == SAMPLE_SIZE:
        break
    
print("Number of sample collected", len(test_samples))
assert len(test_samples) == SAMPLE_SIZE, "Incorrect number of samples"


print("Here is what sample looks like:\n", test_samples[:1])

