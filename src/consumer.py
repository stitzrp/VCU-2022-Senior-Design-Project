from flask import jsonify
from alert_system import sendAlert
import joblib
from kafka import KafkaConsumer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import heapq


def display_topics(model, feature_names, no_top_features):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
              for i in topic.argsort()[:-no_top_features - 1:-1]]))


def get_topic(model, topic_idx, feature_names, no_top_features):
    topic = model.components_[topic_idx]
    return " ".join([feature_names[i] for i in topic.argsort()[:-no_top_features - 1:-1]])


def calculate_score(model, doc_topics, doc_idx, feature_idx):
    score = 0
    for topic_idx in range(doc_topics.shape[1]):
        score += doc_topics[doc_idx, topic_idx] * \
            model.components_[topic_idx, feature_idx]
    return score


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def getNumbersAndSymbols(inputString):
    outputNumbers = []
    for char in inputString:
        if not (char.isalpha()):
            outputNumbers.append(char)
    return outputNumbers


ldaModel = joblib.load('lda_model.jl')

# Define server with port
bootstrap_servers = ['localhost:9092']

# Define topic name from where the message will recieve
topicName = 'my-topic-output'

# Initialize consumer variable
consumer = KafkaConsumer(topicName,  group_id=None,
                         bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest')

for msg in consumer:
    log = msg.value.decode('utf-8')
    log = [log]

    countVector = CountVectorizer(
        token_pattern=r"(?u)\b\w+\b", lowercase=False)
    countVector.fit(log)
    feature_names = countVector.get_feature_names()
    print(feature_names)
    x = countVector.transform(log)
    ldaModel = LatentDirichletAllocation(
        n_components=5, random_state=0, learning_method="batch")

    joblib.dump(ldaModel, 'lda_model.jl')
    # then reload it with
    ldaModel = joblib.load('lda_model.jl')

    ldaModel.fit(x)
    doc_topics = ldaModel.transform(x)
    display_topics(ldaModel, feature_names, 5)

    h = []
    for lineIndex in range(x.shape[0]):
        doc = x.getrow(lineIndex)
        _, featureIndexes = doc.nonzero()

        for featureIndex in featureIndexes:
            score = calculate_score(
                ldaModel, doc_topics, lineIndex, featureIndex)
            feature_name = feature_names[featureIndex]
            if len(h) < 1:
                heapq.heappush(h, (-score, (lineIndex, feature_name)))
            else:
                heapq.heappushpop(h, (-score, (lineIndex, feature_name)))

    outliers = list(map(lambda x: (-x[0], x[1]), h))

    for outlier in sorted(outliers):
        if outlier[0] < 1.07:
            print("--------------------------------")
            print(outlier)
            dominantTopic = np.argmax(doc_topics[outlier[1][0]])

            topicDescription = get_topic(
                ldaModel, dominantTopic, feature_names, 3)
            print("Dominant topic in the anomaly line: %s" % topicDescription)

            sendAlert(msg.value.decode("utf-8"))
