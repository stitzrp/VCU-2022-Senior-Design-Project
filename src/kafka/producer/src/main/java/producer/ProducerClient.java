package producer;

import java.io.File;
import java.util.Properties;
import java.util.Scanner;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

public class ProducerClient {
   // Variable for the name of the topic that we will be sending to.
   private static final String topicName = "my-topic";

   public static void main(String[] args) {
      // Property object used for the KafkaProducer.
      Properties props = new Properties();

      // Assign localhost id (The broker address).
      props.put("bootstrap.servers", "localhost:9092");

      // Class used for the serialization of the message key and value.
      props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
      props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

      // Create the KafkaProducer (a Kafka client that publishes records to the Kafka
      // cluster).
      try (KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props)) {
         File file = new File("/usr/local/lib/src/kafka/producer/BGLtest.log");
         // File file = new File("src/kafka/producer/BGLtest.log");
         Scanner scan = new Scanner(file);

         while (scan.hasNextLine()) {
            String line = scan.nextLine();
            // Record sent to Kafka consisting of the topic name and the message being sent.
            ProducerRecord<String, String> message = new ProducerRecord<String, String>(topicName, line);
            producer.send(message);
         }
         scan.close();
      } catch (Exception e) {
         System.out.println("Failed to send message: " + e);
      }
   }
}
