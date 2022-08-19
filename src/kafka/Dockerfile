FROM maven:3.8.4-jdk-11 AS build
COPY producer /home/code/producer
COPY streams /home/code/streams
COPY run.sh /home/scripts/run.sh
RUN mvn -f /home/code/producer/pom.xml clean package
RUN mvn -f /home/code/streams/pom.xml clean package

FROM openjdk:11
COPY --from=build /home/code/producer /usr/local/lib/src/kafka/producer
COPY --from=build /home/code/streams /usr/local/lib/src/kafka/streams
COPY --from=build /home/scripts /usr/local/lib/src/scripts
ENTRYPOINT [ "/usr/local/lib/src/scripts/run.sh" ]