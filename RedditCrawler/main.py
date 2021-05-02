import praw
import dill
from os import listdir
from os.path import isfile, join
import os

SUBREDDITS = ["CryptoCurrency","Crypto_General", "CryptoCurrencies", "CryptoMarkets", "ethereum", "SatoshiStreetBets"]

SEARCH_KEYWORDS = ["moon", "shoot"]

FILES = []

def readDir():
    global FILES
    FILES = [f for f in listdir("Submissions\\") if isfile(join("Submissions\\", f))]

def writeSubmissionToFile(submission):
    dill.dump(submission, file=open("Submissions\\" + str(submission.id) + "_" + str(submission.num_comments) +".pickle", "wb"))

def readSubmissionFromFile(file):
    submission = dill.load(open("Submissions\\" + file, "rb"))
    return submission

def deleteFile(file):
    if os.path.exists("Submissions\\" + file):
        os.remove("Submissions\\" + file)


def checkNumberOfComments(file, submission):
    numberOfComment = file.split(".")[0].split("_")[-1]
    if int(numberOfComment) != submission.num_comments:
        oldSubmission = readSubmissionFromFile(file)
        submission.selftext = oldSubmission.selftext
        writeSubmissionToFile(submission)
        deleteFile(file)
        print("Update Submission")

def isSubmissionAlreadyFound(submission):
    global FILES
    for file in FILES:
        id = file.split(".")[0].split("_")[0]
        if id == submission.id:
            checkNumberOfComments(file, submission)
            return True
    return False

def checkForNewSubmissions():

    reddit = praw.Reddit(client_id="1qj4oWD-qEPmfw", client_secret="qVmFqcnheu0uyEkSFaCZcJ_AZAwyKg",
                         user_agent="VA Bot Agent")

    for subReddit in SUBREDDITS:
        for submission in reddit.subreddit(subReddit).new(limit=100):
            if any(keyword in submission.title for keyword in SEARCH_KEYWORDS) or any(keyword in submission.selftext for keyword in SEARCH_KEYWORDS):
                if not isSubmissionAlreadyFound(submission):
                    writeSubmissionToFile(submission)
                    print("New Submission stored")

if __name__ == '__main__':
    readDir()
    checkForNewSubmissions()









