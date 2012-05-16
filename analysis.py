from twython import Twython
import json
import operator
import pickle

businessList = []
userList = []
reviewList = []
wordRatingDict = {}

pkl_file = open('wordRatingDict.pkl','rb')
wordRatingDict = pickle.load(pkl_file)
pkl_file.close()
pkl_file = open('nameRatingDict.pkl','rb')
nameRatingDict = pickle.load(pkl_file)
pkl_file.close()

twitter = Twython()
print "If the input store is in the Yelp data set, then the actual rating will also be displayed."
print "Otherwise, it will predict what a store with that name would be rated."
restaurantName = raw_input('Please enter input store (exit to end):')

while restaurantName != 'exit':
    twitterSearch = twitter.search(q = restaurantName)
    results = None
    if twitterSearch:
        results = twitterSearch['results']
    averageList = []
    if results:
        for result in results:
            # print result
            for word in result['text'].split():
                if word in wordRatingDict:
                    # print word, wordRatingDict[word][0]
                    # averageList.append(sum(wordRatingDict[word])/len(wordRatingDict[word]))
                    averageList.append(wordRatingDict[word][0])
    
    if averageList == []:
        print "No prediction."
    else:
        print "Predicted rating: ", float(sum(averageList))/len(averageList)
        if restaurantName in nameRatingDict:
            print "Actual rating: ", nameRatingDict[restaurantName]
            
    restaurantName = raw_input('Please enter input store (exit to end):')
    