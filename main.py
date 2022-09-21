'''
Written by: Eternal Dusk

Scrapes reddit for content and creates a spoken video
You will need to create a praw.ini file containing your bot information
Information on setting up a praw.ini file can be found here: https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#:~:text=Let%E2%80%99s%20get%20started.-,Prerequisites,-%EF%83%81
'''

import praw

import pickle
import json

# Settings
#disallow nsfw posts
nsfw_flag = True


def scrape_subreddits():

    #log in to reddit
    print("Logging into reddit...")

    #logs in using praw.ini file
    reddit = praw.Reddit("bot")

    #list of subreddits to scrape
    subreddits = {"AskReddit" : "hot"}
    # key = subreddit
    # value = type of post to get (controversial, gilded, hot, new, rising, top)

    #list of data to be worked with
    response_data = {}
    # key = subreddit name
    # value = [id, title, author, score, [top comments]]

    for sub in subreddits:
        scraped_data = reddit.subreddit(sub)
        print(f'Scraping subreddit {scraped_data.display_name} - {scraped_data.title}')

        for submission in scraped_data.hot(limit=15):
            if nsfw_flag == True:
                if submission.over_18 == True:
                    #skips if post is nsfw and flag is on
                    continue
            #get the top comments
            submission.comment_sort = "top"
            top_comments = list(submission.comments)

            submission_comments = []
            # [author, body, score]

            #get up to 10 top comments
            if len(top_comments) >= 10:
                for i in range(10):
                    comment = top_comments[i]
                    submission_comments.append([comment.author.name, comment.body, comment.score])
            else:
                for comment in top_comments:
                    submission_comments.append([comment.author.name, comment.body, comment.score])

            #save the data
            if sub in response_data:
                response_data[sub].append([submission.id, submission.title, submission.author.name, submission.score, submission_comments])
            else:
                response_data[sub] = [submission.id, submission.title, submission.author.name, submission.score, submission_comments]

            print(f'{submission.author.name} - {submission.title}')

    return response_data

def main():

    # Setting to test functionality
    get_new_data = False

    if get_new_data == True:
        scraped_dictionary = scrape_subreddits()
        with open('saved_dictionary.pkl', 'wb') as f:
            pickle.dump(scraped_dictionary, f)
    else:
        with open('saved_dictionary.pkl', 'rb') as f:
            loaded_dictionary = pickle.load(f)
            # key = subreddit name
            # value = [id, title, author, score, [top comments]]
            print(f'{json.dumps(loaded_dictionary)}')

if __name__ == '__main__':
    main()
