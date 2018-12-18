package com.wistron.witlab.consumer;

import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRebalanceListener;
import org.apache.kafka.common.TopicPartition;

import java.util.Collection;

public class SeekToListener implements ConsumerRebalanceListener {
    Consumer consmer;

    public SeekToListener(Consumer consmer){
        this.consmer = consmer;
    }


    @Override
    public void onPartitionsRevoked(Collection<TopicPartition> partitions) {

    }

    @Override
    public void onPartitionsAssigned(Collection<TopicPartition> partitions) {
        consmer.seekToBeginning(partitions);
    }
}
