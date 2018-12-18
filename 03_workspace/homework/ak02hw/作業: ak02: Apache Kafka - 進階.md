# 作業: ak02: Apache Kafka - 進階

請依序回答以下的20個問題(單選), 並使用筆記本記錄每一題的答案。 完成後, 使用在ak02hw中的HomeworkAnswerPub程式來發送20筆訊息到指定Kafka Broker與Toipic。

Kafka Broker: 192.168.1.2:9092
Kafak Topic : ak02.wsds01.homework
這一次的作業分成觀念題(1~12)與實作題(13~20):

觀念題的Submit範例: msgKey= "{你/妳的學員ID}|{問題ID}", msgValue="{你/妳的答案}"
實作題的Submit範例: msgKey= "{你/妳的學員ID}|{問題ID}", msgValue則必須根據題目的要求
Tips: 實作題11~15
 ak02hwtips-java下載       ak02hwtips-python下載
HomeworkAnswerPub - 用來submit你/妳的答案
SeekToListener - 用來在每一次的consume同一個topic/consumer group時移動offset到每個partition的最前面(只有Java版本有)
Homework_q02 - 實作題02的提示
Homework_q02_pub - 實作題02的實驗訊息
Homework_q13 - 實作題13的提示
Homework_q14 - 實作題14的提示
Homework_q15 - 實作題15的提示
Homework_q16 - 實作題16的提示
Homework_q17 - 實作題17的提示
Homework_q18 - 實作題18的提示
Homework_q19 - 實作題19的提示
Homework_q20 - 實作題20的提示
HomeworkLoadData - 載入實作用的假資料
實作題#A
Topic: ak02.hw.translog 裡有著某些線上商品貨物的購買及退貨的交易資料, Kafka訊息的msgKey是商品貨物編號（例如 "part_xx") 而msgValue是購買及退貨的內容(例如 "+|123" , 資料用"|"做分隔, 第一個欄位"+"代表商品貨物的購買, "-"代表商品貨物的退貨, 而第二個欄位代表商品貨物交易的數量)。

實作題#B
在topic: ak02.hw.balancelog 與 ak02.hw.balancelog2 裡有著某個線上商品貨物的購買及退貨的交易(movement)及異動前後的結餘(balance)資料, Kafka訊息的msgKey是商品貨物編號（例如 "part_xx") 而msgValue是交易(movement)與結餘(balance)的內容(例如 "+|123|0|123" , 資料用"|"做分隔, 第一個欄位"+"代表商品貨物的購買, "-"代表商品貨物的退貨, 第二個欄位代表商品貨物交易的數量, 第三個欄位代表商品貨物交易前的結餘(balance)值, 第四個欄位代表商品貨物交易後的結餘(balance)值)。

×
請注意!
問題的設計是基於: Kafka version: 1.0.0 以上的版本 (含)

### 問題： 1
Kafka從那個一個版本開始支援Dynamic Update Mode

(1) 0.7
(2) 0.8
(3) 0.9
(4) 1
(5) 1.1

### 問題： 2
在一個有著5個partition的topic中送進一筆message key是"whereami"的訊息時, 請問這個訊息會被送到那一個partition id (0,1,2,3,4)? (假設使用Kafka預設的partitioner）

(1) 0
(2) 1
(3) 2
(4) 3
(5) 4

### 問題： 3

在一個partition為3的topic, 在尚未開始有任何訊息放進去之前, 使用kafka-topic的命令去修改partitions=1, 請問會發生什麼情形?

(1) kafka raise exception and fail to change
(2) change successfully

### 問題： 4

在一個partition為1的topic, 在尚未開始有任何訊息放進去之前, 使用kafka-topic的命令去修改partitions=3, 請問會發生什麼情形?

(1) kafka raise exception and fail to change
(2) change successfully

> The Kafka documentation states we can't reduce the number of partitions per topic once created. Can we then increase them or is it a documentation mistake? If we are allowed to add new partitions and use keys to get our messages wouldn't the old messages be unreachable?

### 問題： 5
在一個partition為1的topic中送進一筆message key是"whereami"的訊息後, 再使用kafka-topic的命令去修改partitions=3, 請問會發生什麼情形?

(1) kafka raise exception and fail to change
(2) change successfully

> Will success but with warning.


### 問題： 6
增加topic的partition的數量時, 以下那些敘述是錯的?

(1) added latency to replicate
(2) better parallelism
(3) better resilience
(4) more files opened on system
(5) better throughput

### 問題： 7

增加topic的replicators的數量時, 以下那些敘述是錯的?

(1) better parallelism
(2) more network overhead
(3) better resilience
(4) more diskspace
(5) longer replication

### 問題： 8
以上那一種設定的修改是需要重新啟動Kafka Broker才能生效?

(1) background.threads
(2) principal.builder.class
(3) listeners
(4) offsets.topic.segment.bytes
(5) num.replica.fetchers

### 問題： 9
topic的compression.type設成"lz4"後, 那一種訊息的資料對幫助Kafka提升傳送效率沒有太大的意義?

(1) plain text
(2) json
(3) xml
(4) comma delimited text
(5) avro

### 問題： 10
在一個有5個brokers的kafka集群中, 有一個topic(replicator-factor=5, min.insync.replicas=3)， 請問當Producer(acks=ALL)在發佈訊息時卻收到NotEnoughReplicasException。請問最有可能發生了何種情況？

(1) one broker is down or fail
(2) two brokers are down or fail
(3) topic's ISR less than 3
(4) the network between producer and brokers is broken
(5) the network between brokers are down

> `replicator-factor=5` => 可容許 4 台壞掉

### 問題： 11
假設kafka的compaction JOB看到一個topic的non-active segment有著以下的訊息: (0, K1, V1), (1, K2, V2), (2, K1, V3), (3, K1, V4), (4, K3, V5), (5, K2, V6), (6, K4, V7), (7, K5, V8), (8, K5, V9), (9, K2, V10), (10, K6, V11)。請問經過成功的compaction之後, non-active segment會剩下幾個訊息?

(1) 5
(2) 6
(3) 7
(4) 8
(5) 9

### 問題： 12

一個topic經過log compaction之後, 重新從頭開始consume就不會讀到有相同msgKey的record, 對或不對?

(1) true
(2) false

> 可能還會有 active segment 的資料進來

### 問題： 13
實作題#A
請問總共有多少個unique的商品貨物編號, 請把這些商品貨物編號列出?

 請用Java Producer 送一筆資料到作業指定的Kafka Topic, msgKey是你的學員號碼加題目id (比如"dsxxxx|13"), msgValue是你/妳找到每個商品貨物編號 (比如"part_xxx|part_yyy|part_zzz")。



### 問題： 14
實作題#A
請問每個商品貨物編號各發生了幾筆交易(count)?

 請用Java Producer 送一筆資料到"作業指定的Kafka Topic, msgKey是你的學員號碼加題目id (比如"dsxxxx|14"), msgValue是你/妳找到每個商品貨物編號與交易的count (比如"part_xxx=134|part_yyy=23|part_zzz=77")。用"="來分隔商品貨物編號與count, 用"|"來分隔每個資料。



### 問題： 15
實作題#A
假如每個商品貨物編號的初始庫存結餘(balance)都是0, 請問當你/妳consume完topic中最後一個offset的訊息後, 請計算出最後每一個商品貨物編號的庫存值為多少?

 請用Java Producer 送一筆資料到作業指定的Kafka Topic, msgKey是你的學員號碼加題目id (比如"dsxxxx|15"), msgValue是你/妳找到每個商品貨物編號與最後的庫存值結餘 (比如 "part_xxx=134|part_yyy=-23|part_zzz=77" )。用"="來分隔商品貨物編號與最後的庫存值結餘, 用"|"來分隔每個資料。這個題目允許庫存結餘(balance)為負數, 同時在回答時若庫存值為負值時, 記得在答案使用"-" (比如 "part_yyy=-23" )。



### 問題： 16
實作題#A
請問當你/妳consume完topic中最後一個offset的訊息後, 假如每個商品貨物編號的最後庫存的結餘(balance)都是0的話, 請問每一個商品貨物編號的期初庫存結餘值為多少?

 請用Java Producer 送一筆資料到作業指定的Kafka Topic, msgKey是你的學員號碼加題目id (比如 "dsxxxx|16" ), msgValue是你/妳計算出來每個商品貨物編號與它的期初庫存值 (比如 "part_xxx=134|part_yyy=-23|part_zzz=77" )。用"="來分隔商品貨物編號與期初庫存值, 用"|"來分隔每個資料。這個題目允許庫存結餘(balance)為負數, 在回答時若庫存值為負值時, 記得在答案使用"-" (比如 "part_yyy=-23" )。


### 問題： 17

**實作題#B**
請問 "ak02.hw.balancelog"與 "ak02.hw.balancelog2"裡各有多少個unique的商品貨物編號?
請用Java Producer 送一筆資料到"作業指定的Kafka Topic, msgKey是你的學員號碼加題目id (比如"dsxxxx|17"), msgValue是你/妳找到unique商品貨物編號的count (比如 "balancelog=10|balancelog2=13" )。


### 問題： 18
實作題#B

請問 "ak02.hw.balancelog" 與 "ak02.hw.balancelog2" 這兩個topics裡那一個topic的訊息筆數比較多?

(1) ak02.hw.balancelog
(2) ak02.hw.balancelog2
(3) they have same record count

> `ak02.hw.balancelog2` 有經過 compaction，所以訊息筆數較少

### 問題： 19
實作題#B
當你/妳consume完topic "ak02.hw.balancelog"最後一個offset的訊息後, 請問每一個unique商品貨物編號最後的商品數量的結餘(balance)數量是多少?

 請用Java Producer 送一筆資料到"作業指定的Kafka Topic, msgKey是你的學員號碼加題目id (比如"dsxxxx|19"),msgValue是你/妳找到每個商品貨物編號與最後的balance值 (比如 "part_xxx=134|part_yyy=-23|part_zzz=77" )。用"="來分隔商品貨物編號與最後的balance值 , 用"|"來分隔每個資料。

### 問題： 20
實作題#B
當你/妳consume完topic "ak02.hw.balancelog2"最後一個offset的訊息後, 請問每一個unique商品貨物編號最後的商品數量的結餘(balance)是多少?

 請用Java Producer 送一筆資料到作業指定的Kafka Topic, msgKey是你的學員號碼加題目id (比如"dsxxxx|20"), msgValue是你/妳找到每個商品貨物編號與最後的balance值 (比如 "part_xxx=134|part_yyy=-23|part_zzz=77" )。用"="來分隔商品貨物編號與最後的balance值 , 用"|"來分隔每個資料。


