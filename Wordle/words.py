import random
import nltk
nltk.download('words')
from nltk.corpus import words
from rawWords import *
from settings import *


#Filtered List
wordsList = []

#Feature Flags
REPEAT = True #FALSE DISABLES REPEATING CHARACTERS IN THE WORDS
STANDARD = True #SET TO TRUE TO ONLY PRODUCE 5 LETTER WORDS
MAX_LEN = 7 #DO NOT EDIT
MIN_LEN = 3


for i in range(len(rawWordsList)):
    currentWord = rawWordsList[i]

    #Settings logic
    lenCheck = MIN_LEN <= len(currentWord) <= MAX_LEN
    repCheck =  "".join(dict.fromkeys(currentWord)) != currentWord
    standardCheck = len(currentWord) == 5 and repCheck

    #Flags if we must discard the word due to settings
    validWord = True

    if(not REPEAT and repCheck):
        validWord = False
    if(STANDARD and not standardCheck):
        validWord = False
    if(not lenCheck):
        validWord = False

    if(validWord):
        wordsList.append(currentWord)


def get_word():
    word = random.choice(wordsList).upper()
    print(word)
    return word

def is_english_word(word):
    return word.lower() in words.words() or word.lower() in rawWordsList
