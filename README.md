# _Machine Learning Tool for Identifying Anomalies in Application Logs_

## _Capital One_

### _From the software applications, network infrastructure, and a variety of technical tooling use across the enterprise come a deluge of log data that is consumed downstream by an even broader set of applications, security tools, and reporting capabilities. Sometimes changes in the data provider will alter the format or contents of the logs they generate, having unintended and sometimes undetected impacts on these downstream consumers. The variety of log sources and volume of log entries makes it difficult to create individual monitoring capabilities to verify the output of each data provider, however without monitoring there is a high risk of failure as applications are upgraded and evolved over time. This project is to develop a single solution that can consume a stream of log records without prior knowledge of the log source or record format and adapt over time to recognize the log entries and then detect potential material changes in their contents or format. Specific care would need to be made to prioritize solutions that can work at high volume without introducing significant delay to data pipelines that leveraged the final solution._

The directory structure in this GitHub is to allow the project to have all its resources self-contained.
Open Source software should not just be a repository of code. There are a number of directories to help you and others that will
follow in your foot steps. It'll also allow the Linux Foundation OMP Mentorship program to keep track of your project and get
a better understanding of the problems you encountered during the developmemnt of this project.

| Folder             | Description                                                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Documentation      | all documentation the project team has created to describe the architecture, design, installation and configuratin of the peoject |
| Notes and Research | Relavent information useful to understand the tools and techniques used in the project                                            |
| Status Reports     | Project management documentation - weekly reports, milestones, etc.                                                               |
| scr                | Source code - create as many subdirectories as needed                                                                             |

## Project Team

- _Lee Adcock_ - _Capital One_ - Mentor
- _Gregory Layton_ - _Capital One_ - Mentor
- _Sean Jepson_ - _Capital One_ - Mentor
<!-- *Technical Advisor Name* - *Company Affliation* - Technical Advisor-->
- _Changqing Luo_ - _Computer Science_ - Faculty Advisor
- _Adrienne Hembrick_ - _Computer Science_ - Student Team Member
- _Dylan Pierce_ - _Computer Science_ - Student Team Member
- _Sean Stitzer_ - _Computer Science_ - Student Team Member
- _Samuel Sunvold_ - _Computer Science_ - Student Team Member

## How to Run the Pipeline Using Ansible Playbook

- NEED TO HAVE BITNAMI KAFKA/ZOOKEEPER IMAGES PULL: "docker pull bitnami/kafka:latest"

1. Navigate to src
2. Run "ansible-playbook setup.yml"
- (Optional). To stop Kafka Broker/Zookeeper, kafkaclients, and modelcontainer containers, run "./clean_up.sh"

## How to Run the Pipeline Manually

- NEED TO HAVE BITNAMI KAFKA/ZOOKEEPER IMAGES PULL: "docker pull bitnami/kafka:latest"

1. Navigate to src
2. Run "docker-compose up -d"
3. Create First Topic "docker exec -it src_kafka_1 kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic my-topic"
4. Create Second Topic "docker exec -it src_kafka_1 kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic my-topic-output"
5. Build kafkaclients and modelcontainer images
6. Run kafkaclients container "docker run -d --network=host kafkaclients:latest"

- (Optional). View Topic events "docker exec -it src_kafka_1 kafka-console-consumer.sh --topic my-topic --from-beginning --bootstrap-server localhost:9092"

7. Run modelcontainer container "docker run -d --network=host modelcontainer:latest"

- (Optional). To stop Kafka Broker/Zookeeper, kafkaclients, and modelcontainer containers, run "./clean_up.sh"

## How to Run the Model Training script


1. Navigate to `src/model_generator`
2. Place whatever log file you would like to train on in the `logs` folder within the `model_generator folder`
3. Change the `BGL_2k.log` in this line: `logPath = currentDir + "/logs/BGL_2k.log"` with whatever log file you would like to train on
4. Run the model generation script with `python modelGenerationLDA.py`
Please Note: In order to run this script, you need to download the appropriate scripts via conda or pip, please find requirements in the `requirements.txt` text file in `src`
5. This script will train and predict on the same dataset, please note that these predictions may not be completely accurate due to it training and testing on the same data (and this is unsupervised learning)
6. The model file should be output as `lda_model.jl` that can be used for predictions
Please note: in order to find the desired results, you may need to experiment with the different components within the training script to see where the most accurate model for the desired input data
Also: I have included an example log dataset for testing purposes