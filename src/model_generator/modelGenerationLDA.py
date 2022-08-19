import os
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
import numpy as np
import heapq
import joblib


def display_topics(model, feature_names, no_top_features):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_features - 1:-1]]))

def get_topic(model, topic_idx,feature_names,no_top_features):
    topic=model.components_[topic_idx]
    return " ".join([feature_names[i] for i in topic.argsort()[:-no_top_features - 1:-1]])

def calculate_score(model,doc_topics,doc_idx,feature_idx):
    score=0
    for topic_idx in range(doc_topics.shape[1]):
        score+=doc_topics[doc_idx,topic_idx] * model.components_[topic_idx,feature_idx]
    return score

currentDir = os.getcwd()

logPath = currentDir + "/logs/BGL_2k.log"

file = open(logPath, "r")

listString = []
for line in file:
	listString.append(line)

listAnomalies = []
for i, x in enumerate(listString):
    if not(x.startswith("-")):
        listAnomalies.append(tuple((i, x)))

countVector = CountVectorizer(token_pattern=r"(?u)\b\w+\b", lowercase = False)
countVector.fit(listString)
feature_names=countVector.get_feature_names()
# print(feature_names)
x=countVector.transform(listString)
ldaModel = LatentDirichletAllocation(n_components=5,random_state=0,learning_method="batch")

joblib.dump(ldaModel, 'lda_model.jl')
# then reload it with
ldaModel = joblib.load('lda_model.jl')

ldaModel.fit(x)
doc_topics=ldaModel.transform(x)
display_topics(ldaModel,feature_names,10)

h=[]
for lineIndex in range(x.shape[0]):
    doc=x.getrow(lineIndex)
    _,featureIndexes=doc.nonzero()
    # print(lineIndex)

    for featureIndex in featureIndexes:
        score=calculate_score(ldaModel,doc_topics,lineIndex,featureIndex)
        feature_name=feature_names[featureIndex]
        if len(h) < 10:
            heapq.heappush(h,(-score, (lineIndex,feature_name)))
        else:
            heapq.heappushpop(h, (-score, (lineIndex,feature_name)))

outliers=list(map(lambda x: (-x[0],x[1]), h))
            
for outlier in sorted(outliers):
    print("--------------------------------")
    print(outlier)
    #print(listString[outlier[1][0]])
    dominantTopic=np.argmax(doc_topics[outlier[1][0]])

    topicDescription=get_topic(ldaModel, dominantTopic,feature_names,3)
    print("Dominant topic in the anomaly line: %s" % topicDescription)

anomalyIndexes = [x[0] for x in listAnomalies]
outlierIndexes = [o[1][0] for o in outliers]
outlierIndexes = list(set(outlierIndexes))

numCorrect = 0
for index in outlierIndexes:
    if anomalyIndexes.count(index):
        numCorrect += 1

results = "Correctly identified {} logs out of {} predictions out of {} total logs"
print(results.format(numCorrect, len(outliers), len(anomalyIndexes)))