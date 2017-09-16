import nltk
from collections import defaultdict

    
hashtablepos = []
hashtableneg = []

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
    
        with open(positives) as lines:
            for line in lines:
                if not line.startswith(';'):
                    hashtablepos.append(line.strip())
                    
        with open(negatives) as lines:
            for line in lines:
                if not line.startswith(';'):
                    hashtableneg.append(line.strip())
                

    def analyze(self, text):
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(str(text).lower())
        total = 0
        for i in range(len(tokens)):
            if tokens[i] in hashtablepos:
                total = total + 1
            if tokens[i] in hashtableneg:
                total = total - 1
        return total


