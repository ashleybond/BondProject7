##################
#Ashley Bond:
#Retrieval based chatbot utilzing NLP 
# Source: https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e
#################
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import nltk
nltk.download('popular', quiet=True) # for downloading packages
from nltk import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
# uncomment the following only the first time
nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only


def preProcess(data):
  #Tokenisation
  sent_tokens = sent_tokenize(data)# converts to list of sentences 
  word_tokens = word_tokenize(data)# converts to list of words
  return sent_tokens, word_tokens
  

def lemTokens(tokens):
  #WordNet is a semantically-oriented dictionary of English included in NLTK.
    lemmer = WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]


def LemNormalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return lemTokens(word_tokenize(text.lower().translate(remove_punct_dict)))


def greeting(sentence):
    # Keyword Matching
    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
    GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating chatbot response
def response(sent_tokens,user_response):
    robo_response=''
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens) #inputs sentence tokens
    
    # computes the lexical distance between our user message and each element in tfidf (determines similarity b/w user input and dataset)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    #TODO 6: print the words "THIS IS THE INDEX OF THE SENTENCE THAT'S SIMILAR TO THE USER INPUT"
    print("THIS IS THE INDEX OF THE SENTENCE THAT'S SIMILAR TO THE USER INPUT")
    #TODO 7: Print idx
    print(idx)
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        #TODO 8: print the words "THIS IS SENTENCE MOST SIMILAR TO THE USER INPUT"
        print("THIS IS SENTENCE MOST SIMILAR TO THE USER INPUT")
        # TODO 9: print sent_tokens at position idx
        print(sent_tokens[idx])
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

def chatbot():
  f=open('chatbot.txt','r')
  raw = f.read().lower()
  #TODO 2: print the words "THIS IS THE RAW DATA". Hint: to print words use the print command with the text you want to print contained within quotes inside the parenthesis
  print("THIS IS THE RAW DATA")
  #TODO 3: print the raw data - contained in the variable raw.  Hint: to print a variable, use the print command with the name of the variable you want to print inside the parenthesis
  print(raw)
  sent_tokens, word_tokens=preProcess(raw)
  #TODO 4: print the words "THESE ARE THE SENTENCE TOKENS"
  print("THESE ARE THE SENTENCE TOKENS")
  #TODO 5: Print sent_tokens
  print(sent_tokens)
  print(f'ROBO: My name is Robo.\nI will answer your queries about Chatbots.\nIf you want to exit, type Bye!\n')
  while(True):
      user_response = input('\n>>').lower()
      if(user_response=='bye'):
        print("ROBO: Bye! take care..") 
        break 
      else:
        if(greeting(user_response)!=None):
            print(f'\nROBO: {greeting(user_response)}')
        else:
            print(f'\nROBO: ',end="")
            robo_response=response(sent_tokens, user_response)
            # TODO 1: Comment out the line of code below
            #print(f'{robo_response}\n')
            sent_tokens.remove(user_response)

chatbot()

