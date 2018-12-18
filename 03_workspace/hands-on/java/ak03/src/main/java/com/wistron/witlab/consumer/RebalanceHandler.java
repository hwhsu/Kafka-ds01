package com.wistron.witlab.consumer;

import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.clients.consumer.ConsumerRebalanceListener;
import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.common.TopicPartition;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

public class RebalanceHandler implements ConsumerRebalanceListener {
    private Map<TopicPartition, OffsetAndMetadata> currentOffsets = new HashMap<>();
    private Consumer consumer;

    public RebalanceHandler(Consumer consumer, Map<TopicPartition, OffsetAndMetadata> currentOffsets){
        this.consumer = consumer;
        this.currentOffsets = currentOffsets;
    }

    // 當Rebalance被觸發後, Consumer被取回被assigned的partitions
    @Override
    public void onPartitionsRevoked(Collection<TopicPartition> partitions) {
        System.out.println("Lost partitions in rebalance. Commiting current Offsets: " + currentOffsets);
        consumer.commitSync(currentOffsets);
    }

    // 當Rebalance被觸發後, Consumer被通知有那些partition被assigned
    @Override
    public void onPartitionsAssigned(Collection<TopicPartition> partitions) {

    }
}
