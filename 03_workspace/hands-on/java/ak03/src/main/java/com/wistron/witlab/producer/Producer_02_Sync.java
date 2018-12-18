package com.wistron.witlab.producer;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.Properties;

/**
 * 示範: Sending a Message Synchronously
 */
public class Producer_02_Sync {
    public static void main(String[] args) {
        // 步驟1. 設定要連線到Kafka集群的相關設定
        Properties props = new Properties();

        props.put("bootstrap.servers", "localhost:9092"); // Kafka集群在那裡?
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer"); // 指定msgKey的序列化器
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer"); // 指定msgValue的序列化器

        // 步驟2. 產生一個Kafka的Producer的實例
        Producer<String, String> producer = new KafkaProducer<>(props);

        // 步驟3. 指定想要發佈訊息的topic名稱
        String topicName = "ak03.syncsending";

        int msgCount = 100000; // 10萬筆

        try {
            System.out.println("Start sending messages ...");
            long time_start = System.currentTimeMillis(); // 記錄一下開始時間點

            // 步驟4. 產生要發佈到Kafka的訊息 (把訊息封裝進一個ProducerRecord的實例中)
            //    - 參數#1: topicName
            //    - 參數#2: msgKey
            //    - 參數#3: msgValue

            // ** 示範: Synchronous Send **
            // 在以下的"send().get()"的同步發佈訊息的過程, 透過同步我們可以取得由Broker回覆訊息發佈的ack結果
            // 由於這種方法是一筆一筆的送與等待Broker的回應。因此這種方法的throughput最差 (通常不會用Kafka來做這種事)

            for(int i=0; i<msgCount; i++) {
                // Broker回覆訊息包含了訊息落在topic的那個partition及offset
                RecordMetadata recordMetadata = producer.send(new ProducerRecord<>(topicName, ""+i, "msg_"+i)).get();

                if((i+1)%10000==0) {
                    // 為了不讓打印訊息拖慢速度, 我們每1萬打印一筆recordMetata來看
                    System.out.println((i+1) + " messages sent!");
                    System.out.println("Topic:Partition:Offset: [" + recordMetadata.topic() + "]:["
                            + recordMetadata.partition() + "]:["
                            + recordMetadata.offset() + "]");
                }
            }

            long time_spend = System.currentTimeMillis() - time_start;
            System.out.println("Send        : " + msgCount + " messages to Kafka");
            System.out.println("Total spend : " + time_spend + " milli-seconds");
            System.out.println("Throughput  : " + msgCount/(float)time_spend * 1000 + " msg/sec");
        } catch (Exception e) {
            // 錯誤處理
            e.printStackTrace();
        }

        // 步驟5. 關掉Producer實例的連線
        producer.close();

        System.out.println("Message sending completed!");
    }
}
