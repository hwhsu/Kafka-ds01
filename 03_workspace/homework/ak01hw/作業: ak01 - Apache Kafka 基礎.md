# 作業: ak01 - Apache Kafka 基礎

請依序回答以下的20個問題(單選), 並使用筆記本記錄每一題的答案。 完成後, 使用在ak01hw中的HomeworkAnswerPub程式來發送20筆訊息到指定Kafka Broker與Toipic。

Kafka Broker: 192.168.1.2:9092
Kafak Topic : ak01.wsds01.homework

注意: 每一條訊息包含msgKey與msgValue, msgKey放的是{學員ID}與{問題ID}(使用"|")來分隔, 而msgValue放的是"{你/妳的答案}"。

> 請注意!
> 問題的設計是基於: Kafka version: 1.0.0 以上的版本 (含)

 問題 ID： 1
在Kafka的ecosystem元件中, 何者是用來做為不同Kafka集群中資料同步的元件?

(1)   zookeeper
(2)   schme-registry
(3)   ksql
(4)   mirror maker
(5)   kafka streams
 問題 ID： 2
透過Schema Registry, Kafka 會使用何種資料格式來讀寫message?

(1)   json
(2)   avro
(3)   thrift
(4)   protobuf
(5)   parquet
 問題 ID： 3
在一個有著3個節點的Kafka集群正式環境中，一般會安裝幾個節點的zookeeper?

(1)   1
(2)   2
(3)   3
(4)   4
(5)   5
 問題 ID： 4
一筆要推送到Kafka topic的訊息在Kafka內部稱之為?

(1)   message
(2)   key-value pair
(3)   packet
(4)   record
(5)   field
 問題 ID： 5
一筆從Kafka topic中擷取出來的record不會包含那些訊息?

(1)   key
(2)   value
(3)   ISR
(4)   timestamp
(5)   offset
 問題 ID： 6
當把不包含"key"的訊息推送到一個有著多個partitions的topic中裡, Kafka會如何決定要把這筆record派送到那個partition中?

(1)   round-bin
(2)   key.hashCode() % numberOfPartitions
(3)   random
(4)   weighted-dispatch
(5)   partition with less records
 問題 ID： 7
在Kafka中的Broker的ID是用什麼資料型別定義?

(1)   double
(2)   float
(3)   string
(4)   decimal
(5)   integer
 問題 ID： 8
寫到Kafka的訊息"預設"會被保留多久?

(1)   1 hour
(2)   12 hours
(3)   1 day
(4)   7 days
(5)   14 days
 問題 ID： 9
一個被設置為partitions=3, replication-factor=3的topic, 在一個有著5個brokers的Kafka集群中, 可以允計同時有多少個brokers離線而仍然提供正常的運作?

(1)   1
(2)   2
(3)   3
(4)   4
(5)   5
 問題 ID： 10
當Kafka producer在發佈訊息時, 那一種broker ack的設置的throught put最高? (partitions=3, replication-factor=2的topic, brokers=3)

(1)   acks=0
(2)   acks=1
(3)   acks=-1
(4)   acks=all
(5)   acks=none
 問題 ID： 11
一個被設置為partitions=3, replication-factor=2的topic, 在一個有5個brokers的Kafka集群中, 如果要取得最大的through put來說, 最多可部署幾個相同"ConsumerGroup"的active "Consumer實例"?

(1)   1
(2)   2
(3)   3
(4)   4
(5)   5
 問題 ID： 12
那一種訊息壓縮型態(compression type)是Kafka不支援的？

(1)   none
(2)   gzip
(3)   lz4
(4)   snappy
(5)   7zip

Valid values are none, gzip, snappy, lz4, or zstd

 問題 ID： 13
Kafka對於訊息是先進先出(FIFO)的保證是基於以下那一種的概念的組合?

(1)   broker
(2)   topic+partition
(3)   partition
(4)   topic
(5)   broker+topic

 問題 ID： 14
Kafka把每一個consumer group對於每一個topic+partition的最後committed的offset紀錄, 儲放在那裡?

(1)   mysql
(2)   rocksdb
(3)   zookeeper
(4)   topic "__consumer_offsets"
(5)   sqllite

 問題 ID： 15
什麼是Kafka?

(1)   A new communication protocol
(2)   A middle layer to decouple your real time data pipeline
(3)   A database
(4)   A new computer language
(5)   A new operating system

 問題 ID： 16
Kafka 不擅長那個方面?

(1)   batch processing
(2)   data streaming
(3)   de-coupling data pipeline
(4)   storing data in a distributed logs
(5)   streaming computation

 問題 ID： 17
Kafka沒有那一個特質?

(1)   distributed system
(2)   horizontal scaling
(3)   fault tolerance
(4)   high performance
(5)   SQL semantics

 問題 ID： 18
Zookeeper沒有為Kafka集群提供那一個功能?

(1)   to perform a leader election
(2)   to maintain the list of all the brokers in the cluster
(3)   to send notifications to kafka in case of any changes
(4)   to maintain consumer offsets
(5)   to store ACL metadata

 問題 ID： 19
兩個有著相同group.id (consumer group id)的Consumer實例去讀取同一個topic的時候, 絕對不會同時讀到同一個partition的訊息 (mutually exclusive partitions), 對不對?

(1)   true
(2)   flase

 問題 ID： 20
每一個partition只能有一個leader與可能很多個的replicas, 對不對?

(1)   true
(2)   flase
