package com.wistron.witlab.producer;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Properties;

/**
 * 示範: 用來持續產生event來給Consumer_01_CGroup進行Rebalance的演示
 */
public class Producer_05_CGroup {
    public static void main(String[] args) {
        // 步驟1. 設定要連線到Kafka集群的相關設定
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092"); // Kafka集群在那裡?
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer"); // 指定msgKey的序列化器
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer"); // 指定msgValue的序列化器
        // 步驟2. 產生一個Kafka的Producer的實例
        Producer<String, String> producer = new KafkaProducer<>(props);
        // 步驟3. 指定想要發佈訊息的topic名稱
        String topicName = "ak03.fourpartition";
        int msgCount = 10000; // 1萬筆
        try {
            System.out.println("Start sending messages ...");
            // 步驟4. 產生要發佈到Kafka的訊息 (把訊息封裝進一個ProducerRecord的實例中)
            for(int i=0; i<msgCount; i++) {
                producer.send(new ProducerRecord<>(topicName, ""+i, "msg_"+i));
                Thread.sleep(3000); // 註執行緒停個3秒
            }
        } catch (Exception e) {
            // 錯誤處理
            e.printStackTrace();
        }
        // 步驟5. 關掉Producer實例的連線
        producer.close();
        System.out.println("Message sending completed!");
    }
}
