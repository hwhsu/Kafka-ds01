package com.wistron.witlab.producer;

import org.apache.kafka.clients.producer.*;

import java.util.Properties;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * 示範: Sending a Message Asynchronously (非同步)
 */
public class Producer_03_Async {
    public static void main(String[] args) {
        // 步驟1. 設定要連線到Kafka集群的相關設定
        Properties props = new Properties();

        props.put("bootstrap.servers", "localhost:9092"); // Kafka集群在那裡?
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer"); // 指定msgKey的序列化器
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer"); // 指定msgValue的序列化器

        props.put("acks","all");
        props.put("max.in.flight.requests.per.connection","1");
        props.put("retries",Integer.MAX_VALUE+"");

        // 步驟2. 產生一個Kafka的Producer的實例
        Producer<String, String> producer = new KafkaProducer<>(props);

        // 步驟3. 指定想要發佈訊息的topic名稱
        String topicName = "ak03.asyncsending";

        int msgCount = 100000; // 10萬筆

        try {
            System.out.println("Start sending messages ...");
            long time_start = System.currentTimeMillis(); // 記錄一下開始時間點

            // 步驟4. 產生要發佈到Kafka的訊息 (把訊息封裝進一個ProducerRecord的實例中)
            //    - 參數#1: topicName
            //    - 參數#2: msgKey
            //    - 參數#3: msgValue

            // ** 示範: Asynchronous Send **
            // 透過一個我們自己定義的Callback函式我們可以非同步地取得由Broker回覆訊息發佈的ack結果
            // 這種方法可以取得Broker回覆訊息發佈的ack結果, 同時又可以取得好的throughput (建議的作法)

            AtomicInteger atomicInteger = new AtomicInteger();
            CountDownLatch countDownLatch = new CountDownLatch(msgCount);

            for(int i=0; i<msgCount; i++) {
                // 回呼函式會在Broker送回ack的時候自動去呼叫
                producer.send(new ProducerRecord<>(topicName, ""+i, "msg_" + i),
                        new BrokerAckCallback(atomicInteger, countDownLatch));
            }

            countDownLatch.await(); // 等待所有的msg的Broker ack

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
