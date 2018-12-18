package com.wistron.witlab.producer;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.wistron.witlab.model.Employee;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Date;
import java.util.Properties;
import java.util.Random;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * 示範: 如何將資料包成物件並轉換成JSON字串送入Kafka
 */
public class Producer_04_Json {
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
        String topicName = "ak03.json";

        int msgCount = 100000; // 10萬筆

        // 一個用來將DTO物件轉換成(JSON String)的物件 <-- 重要
        ObjectMapper om = new ObjectMapper();

        Random random = new Random();
        try {
            System.out.println("Start sending messages ...");
            long time_start = System.currentTimeMillis(); // 記錄一下開始時間點

            // 步驟4. 產生要發佈到Kafka的訊息 (把訊息封裝進一個ProducerRecord的實例中)
            //    - 參數#1: topicName
            //    - 參數#2: msgKey
            //    - 參數#3: msgValue

            // ** 示範: 如何將資料包成物件並轉換成JSON字串送入Kafka **
            // 由於一般應用場景的資料都是包括了很多的資料欄位及不同的資料型別。通常都會使用一個類別物件來做為資料傳遞的容器。
            // 因此如何把一個Data Transfer Object (DTO)序列化送進Kafka是相當關鍵的步驟

            AtomicInteger atomicInteger = new AtomicInteger();
            CountDownLatch countDownLatch = new CountDownLatch(msgCount);

            for(int i=0; i<msgCount; i++) {
                // 讓我們產生假的Employee資料
                Employee employee = new Employee("empid_"+i, "fn_"+i, "ln_"+i,
                        "deptid_"+i%10, new Date(), 100000*random.nextFloat(), random.nextBoolean());

                // 把Employee轉換成JSON字串(String)
                String employeeJSON = om.writeValueAsString(employee);

                // 送出訊息
                producer.send(new ProducerRecord<>(topicName, employee.getId(), employeeJSON),
                        new BrokerAckCallback(atomicInteger, countDownLatch)); // 回呼函式會在Broker送回ack的時候自動去呼叫
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
