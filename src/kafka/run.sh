#!/bin/bash
java -jar /usr/local/lib/src/kafka/producer/target/producer-1.0-SNAPSHOT.jar &
java -jar /usr/local/lib/src/kafka/streams/target/streams-1.0-SNAPSHOT.jar