package com.wistron.witlab.producer;

import org.apache.kafka.clients.producer.Callback;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

public class BrokerAckCallback implements Callback {
    // 使用AtomicInteger來做為非同步的counter, 可以避免blocking及contention
    AtomicInteger atomicInteger;
    // 使用CountdownLatch來讓主線程知道所有的訊息都己經處理完了
    CountDownLatch countDownLatch;

    public BrokerAckCallback(AtomicInteger atomicInteger, CountDownLatch countDownLatch) {
        this.atomicInteger = atomicInteger;
        this.countDownLatch = countDownLatch;
    }

    @Override
    public void onCompletion(RecordMetadata recordMetadata, Exception exception) {
        // 增加1再取出
        int counter = atomicInteger.incrementAndGet();
        if(counter%100000==0) {
            // 為了不讓打印訊息拖慢速度, 我們每10萬打印一筆recordMetata來看
            System.out.println(counter + " messages sent!");
            System.out.println("Topic:Partition:Offset: [" + recordMetadata.topic() + "]:["
                    + recordMetadata.partition() + "]:["
                    + recordMetadata.offset() + "]");
        }
        this.countDownLatch.countDown(); // 倒數
    }
}


