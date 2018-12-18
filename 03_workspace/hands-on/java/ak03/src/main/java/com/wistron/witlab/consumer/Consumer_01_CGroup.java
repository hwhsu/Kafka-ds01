package com.wistron.witlab.consumer;

import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.record.TimestampType;

import java.time.Duration;
import java.util.Arrays;
import java.util.Properties;

public class Consumer_01_CGroup {
    public static void main(String[] args) {
        // 步驟1. 設定要連線到Kafka集群的相關設定
        Properties props = new Properties();

        props.put("bootstrap.servers", "localhost:9092"); // Kafka集群在那裡?
        props.put("group.id", "CG1"); // <-- 這就是ConsumerGroup
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer"); // 指定msgKey的反序列化器
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer"); // 指定msgValue的反序列化器
        props.put("auto.offset.reset", "earliest"); // 是否從這個ConsumerGroup尚未讀取的partition/offset開始讀

        // 步驟2. 產生一個Kafka的Consumer的實例
        Consumer<String, String> consumer = new KafkaConsumer<>(props);

        // 步驟3. 指定想要訂閱訊息的topic名稱
        String topicName = "ak03.fourpartition";

        // 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
        consumer.subscribe(Arrays.asList(topicName));

        // 步驟5. 持續的拉取Kafka有進來的訊息
        try {
            System.out.println("Start listen incoming messages ...");

            while (true) {
                // 請求Kafka把新的訊息吐出來
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));

                // 如果有任何新的訊息就會進到下面的迭代
                for (ConsumerRecord<String, String> record : records){

                    // ** 在這裡進行商業邏輯與訊息處理 **

                    // 取出相關的metadata
                    String topic = record.topic();
                    int partition = record.partition();
                    long offset = record.offset();
                    TimestampType timestampType = record.timestampType();
                    long timestamp = record.timestamp();

                    // 取出msgKey與msgValue
                    String msgKey = record.key();
                    String msgValue = record.value();

                    // 秀出metadata與msgKey & msgValue訊息
                    System.out.println(topic + "-" + partition + "-" + offset + " : (" + record.key() + ", " + record.value() + ")");
                }
            }
        } finally {
            // 步驟6. 如果收到結束程式的訊號時關掉Consumer實例的連線
            consumer.close();

            System.out.println("Stop listen incoming messages");
        }
    }
}
