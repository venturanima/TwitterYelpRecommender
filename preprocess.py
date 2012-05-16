from twython import Twython
import json
import operator
import pickle

# businessList = []
userList = []
reviewList = []
nameRatingDict = {}
reducedIdToBusiness = {}
# businesses = []
wordRatingDict = {}
# print "opening yelp data"

for line in open('data/yelpdata.txt'):
    item = json.loads(line)
    if item['type'] == 'business':
        nameRatingDict[item['name']] = item['stars']
        if 'Restaurants' in item['categories'] \
            and 'Fast Food' in item['categories']:
            # print item
            # businessList.append(item)
            reducedIdToBusiness[item['business_id']] = item['name']
            # businesses.append((item['stars'],item['name']))
    elif item['type'] == 'user':
        userList.append(item)
    elif item['type'] == 'review':
        reviewList.append(item)
        for word in item['text'].split():
            # if len(word) > 4:
            if word in wordRatingDict:
                get = wordRatingDict[word]
                wordRatingDict[word] = ((get[0]*get[1] + item['stars'])/(get[1]+1),get[1]+1)
            else:
                wordRatingDict[word] = (float(item['stars']),1)
            # print wordRatingDict.get(word,[]) + [item['stars']]
            # wordRatingDict[word] = wordRatingDict.get(word,[]) + [item['stars']]
    
# print "yelp data read"
# print reviewList[0]
output = open('wordRatingDict.pkl','wb')
pickle.dump(wordRatingDict,output)
output.close()
output = open('nameRatingDict.pkl','wb')
pickle.dump(nameRatingDict,output)
output.close()


#reduced
restaurantDict = {}
for review in reviewList:
    busId = review['business_id']
    if busId in reducedIdToBusiness:
        if reducedIdToBusiness[busId] not in restaurantDict:
            restaurantDict[reducedIdToBusiness[busId]] = {}
        restaurantReview = review['text']
        for word in restaurantReview.split(' '):
            restaurantDict[reducedIdToBusiness[busId]][word] = restaurantDict[reducedIdToBusiness[busId]].get(word,0) + 1
        
# print restaurantDict
# cooccurenceDict = {}
dumbWordList = ['the', 'was', 'of', 'a', 'and', 'to', 'is', 'so', 'in', 'for', 'they' \
                    ,'you', 'that', 'but', 'it', 'with', 'their', 'has', ' ', '', 'at', 'get', 'have', 'my', 'this', 'i', 'on'\
                    ,'are', 'food', 'place', 'not', 'had', 'like', 'very', 'were', 'which', 'be', 'me', \
                    'as', 'from', 'like', 'if', 'we', 'your', 'as', '-']

csvFile = open('data/yelp.csv','w')                    
csvFile.write('restaurant,word,times\n')
                    
for restaurant in restaurantDict:
    maxTimes = 0
    maxWord = 'empty'
    for word in restaurantDict[restaurant]:
        if restaurantDict[restaurant][word] >= maxTimes and word.lower() not in dumbWordList \
            and word not in restaurant.split(' '):
            maxTimes = restaurantDict[restaurant][word]
            maxWord = word
        # print unicode(word)
    csvFile.write(restaurant+","+ maxWord + "," + unicode(maxTimes)+'\n')
    
csvFile.close()
# print len(restaurantDict)
    

# twitter = Twython()

# for stars, restaurant in businesses:
    # print "searching: " + restaurant.encode('utf-8')
    # restaurantDict[restaurant] = {}
    # results = twitter.search(q = restaurant)['results']

    # max = 0
    # maxWord = 'fillerfillerfillerfillerfillerfillerfiller'
    # for result in results:
        # tweet = result['text'].encode('utf-8')
        # for word in tweet.split(' '):
            # get = restaurantDict[restaurant].get(word,0) + 1
            # restaurantDict[restaurant][word] = get
            # if get > max and word.lower() not in restaurant.encode('utf-8').lower() and word not in ['a','the','of','and']:
                # max = get
                # maxWord = word
    # restaurantDict[restaurant]['__stars__'] = stars
    # restaurantDict[restaurant]['__max__'] = max
    # restaurantDict[restaurant]['__maxWord__'] = maxWord
            
# for restaurant in restaurantDict:
    # if restaurantDict[restaurant]['__max__'] != 0:
        # print 'Restaurant:' + restaurant + ', '+\
            # str(restaurantDict[restaurant]['__stars__']) + ' stars, "'+ \
            # restaurantDict[restaurant]['__maxWord__'] + '" used most often,'+\
            # str(restaurantDict[restaurant]['__max__']) + ' times'