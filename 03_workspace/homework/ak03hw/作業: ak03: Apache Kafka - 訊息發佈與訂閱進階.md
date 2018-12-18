# 作業: ak02: Apache Kafka - 進階

請依序回答以下的 20 個問題 (單選), 並使用筆記本記錄每一題的答案。 完成後, 使用在 ak02hw 中的 HomeworkAnswerPub 程式來發送 20 筆訊息到指定 Kafka Broker 與 Toipic。

Kafka Broker: 192.168.1.2:9092
Kafak Topic : ak02.wsds01.homework
這一次的作業分成觀念題 (1~12) 與實作題(13~20):

觀念題的 Submit 範例: msgKey= "{你 / 妳的學員 ID}|{問題 ID}", msgValue="{你 / 妳的答案}"
實作題的 Submit 範例: msgKey= "{你 / 妳的學員 ID}|{問題 ID}", msgValue 則必須根據題目的要求
Tips: 實作題 11~15
 ak02hwtips-java 下載       ak02hwtips-python 下載
HomeworkAnswerPub - 用來 submit 你 / 妳的答案
SeekToListener - 用來在每一次的 consume 同一個 topic/consumer group 時移動 offset 到每個 partition 的最前面 (只有 Java 版本有)
Homework_q02 - 實作題 02 的提示
Homework_q02_pub - 實作題 02 的實驗訊息
Homework_q13 - 實作題 13 的提示
Homework_q14 - 實作題 14 的提示
Homework_q15 - 實作題 15 的提示
Homework_q16 - 實作題 16 的提示
Homework_q17 - 實作題 17 的提示
Homework_q18 - 實作題 18 的提示
Homework_q19 - 實作題 19 的提示
Homework_q20 - 實作題 20 的提示
HomeworkLoadData - 載入實作用的假資料
實作題 #A
Topic: ak02.hw.translog 裡有著某些線上商品貨物的購買及退貨的交易資料, Kafka 訊息的 msgKey 是商品貨物編號（例如 "part_xx") 而 msgValue 是購買及退貨的內容 (例如 "+|123" , 資料用 "|" 做分隔, 第一個欄位 "+" 代表商品貨物的購買, "-" 代表商品貨物的退貨, 而第二個欄位代表商品貨物交易的數量)。

實作題 #B
在 topic: ak02.hw.balancelog 與 ak02.hw.balancelog2 裡有著某個線上商品貨物的購買及退貨的交易 (movement) 及異動前後的結餘 (balance) 資料, Kafka 訊息的 msgKey 是商品貨物編號（例如 "part_xx") 而 msgValue 是交易 (movement) 與結餘 (balance) 的內容 (例如 "+|123|0|123" , 資料用 "|" 做分隔, 第一個欄位"+" 代表商品貨物的購買, "-" 代表商品貨物的退貨, 第二個欄位代表商品貨物交易的數量, 第三個欄位代表商品貨物交易前的結餘 (balance) 值, 第四個欄位代表商品貨物交易後的結餘 (balance) 值)。

×
請注意!
問題的設計是基於: Kafka version: 1.0.0 以上的版本 (含)
 問題 ID： 1
Kafka 從那個一個版本開始支援 Dynamic Update Mode

(1) 0.7
(2) 0.8
(3) 0.9
(4) 1
(5) 1.1
 問題 ID： 2
在一個有著 5 個 partition 的 topic 中送進一筆 message key 是 "whereami" 的訊息時, 請問這個訊息會被送到那一個 partition id (0,1,2,3,4)? (假設使用 Kafka 預設的 partitioner）

(1) 0
(2) 1
(3) 2
(4) 3
(5) 4
 問題 ID： 3
在一個 partition 為 3 的 topic, 在尚未開始有任何訊息放進去之前, 使用 kafka-topic 的命令去修改 partitions=1, 請問會發生什麼情形?

(1) kafka raise exception and fail to change
(2) change successfully
 問題 ID： 4
在一個 partition 為 1 的 topic, 在尚未開始有任何訊息放進去之前, 使用 kafka-topic 的命令去修改 partitions=3, 請問會發生什麼情形?

(1) kafka raise exception and fail to change
(2) change successfully
 問題 ID： 5
在一個 partition 為 1 的 topic 中送進一筆 message key 是 "whereami" 的訊息後, 再使用 kafka-topic 的命令去修改 partitions=3, 請問會發生什麼情形?

(1) kafka raise exception and fail to change
(2) change successfully
 問題 ID： 6
增加 topic 的 partition 的數量時, 以下那些敘述是錯的?

(1) added latency to replicate
(2) better parallelism
(3) better resilience
(4) more files opened on system
(5) better throughput

> broker 死掉跟 rebalance 無關

 問題 ID： 7
增加 topic 的 replicators 的數量時, 以下那些敘述是錯的?

(1) better parallelism
(2) more network overhead
(3) better resilience
(4) more diskspace
(5) longer replication
 問題 ID： 8
以上那一種設定的修改是需要重新啟動 Kafka Broker 才能生效?

(1) background.threads
(2) principal.builder.class
(3) listeners
(4) offsets.topic.segment.bytes
(5) num.replica.fetchers
 問題 ID： 9
topic 的 compression.type 設成 "lz4" 後, 那一種訊息的資料對幫助 Kafka 提升傳送效率沒有太大的意義?

(1) plain text
(2) json
(3) xml
(4) comma delimited text
(5) avro
 問題 ID： 10
在一個有 5 個 brokers 的 kafka 集群中, 有一個 topic(replicator-factor=5, min.insync.replicas=3)， 請問當 Producer(acks=ALL) 在發佈訊息時卻收到 NotEnoughReplicasException。請問最有可能發生了何種情況？

(1) one broker is down or fail
(2) two brokers are down or fail
(3) topic's ISR less than 3
(4) the network between producer and brokers is broken
(5) the network between brokers are down

> 實作就知道

 問題 ID： 11
假設 kafka 的 compaction JOB 看到一個 topic 的 non-active segment 有著以下的訊息: (0, K1, V1), (1, K2, V2), (2, K1, V3), (3, K1, V4), (4, K3, V5), (5, K2, V6), (6, K4, V7), (7, K5, V8), (8, K5, V9), (9, K2, V10), (10, K6, V11)。請問經過成功的 compaction 之後, non-active segment 會剩下幾個訊息?

(1) 5
(2) 6
(3) 7
(4) 8
(5) 9
 問題 ID： 12
一個 topic 經過 log compaction 之後, 重新從頭開始 consume 就不會讀到有相同 msgKey 的 record, 對或不對?

(1) true
(2) false
 問題 ID： 13
實作題 #A
請問總共有多少個 unique 的商品貨物編號, 請把這些商品貨物編號列出?

 請用 Java Producer 送一筆資料到作業指定的 Kafka Topic, msgKey 是你的學員號碼加題目 id (比如 "dsxxxx|13"), msgValue 是你 / 妳找到每個商品貨物編號 (比如 "part_xxx|part_yyy|part_zzz")。


 問題 ID： 14
實作題 #A
請問每個商品貨物編號各發生了幾筆交易 (count)?

 請用 Java Producer 送一筆資料到 "作業指定的 Kafka Topic, msgKey 是你的學員號碼加題目 id (比如"dsxxxx|14"), msgValue 是你 / 妳找到每個商品貨物編號與交易的 count (比如"part_xxx=134|part_yyy=23|part_zzz=77")。用"="來分隔商品貨物編號與 count, 用"|" 來分隔每個資料。


 問題 ID： 15
實作題 #A
假如每個商品貨物編號的初始庫存結餘 (balance) 都是 0, 請問當你 / 妳 consume 完 topic 中最後一個 offset 的訊息後, 請計算出最後每一個商品貨物編號的庫存值為多少?

 請用 Java Producer 送一筆資料到作業指定的 Kafka Topic, msgKey 是你的學員號碼加題目 id (比如 "dsxxxx|15"), msgValue 是你 / 妳找到每個商品貨物編號與最後的庫存值結餘 (比如 "part_xxx=134|part_yyy=-23|part_zzz=77" )。用 "=" 來分隔商品貨物編號與最後的庫存值結餘, 用 "|" 來分隔每個資料。這個題目允許庫存結餘 (balance) 為負數, 同時在回答時若庫存值為負值時, 記得在答案使用 "-" (比如 "part_yyy=-23" )。


 問題 ID： 16
實作題 #A
請問當你 / 妳 consume 完 topic 中最後一個 offset 的訊息後, 假如每個商品貨物編號的最後庫存的結餘 (balance) 都是 0 的話, 請問每一個商品貨物編號的期初庫存結餘值為多少?

 請用 Java Producer 送一筆資料到作業指定的 Kafka Topic, msgKey 是你的學員號碼加題目 id (比如 "dsxxxx|16"), msgValue 是你 / 妳計算出來每個商品貨物編號與它的期初庫存值 (比如 "part_xxx=134|part_yyy=-23|part_zzz=77" )。用 "=" 來分隔商品貨物編號與期初庫存值, 用 "|" 來分隔每個資料。這個題目允許庫存結餘 (balance) 為負數, 在回答時若庫存值為負值時, 記得在答案使用 "-" (比如 "part_yyy=-23" )。


 問題 ID： 17
實作題 #B
請問 "ak02.hw.balancelog" 與 "ak02.hw.balancelog2" 裡各有多少個 unique 的商品貨物編號?

 請用 Java Producer 送一筆資料到 "作業指定的 Kafka Topic, msgKey 是你的學員號碼加題目 id (比如"dsxxxx|17"), msgValue 是你 / 妳找到 unique 商品貨物編號的 count (比如"balancelog=10|balancelog2=13" )。


 問題 ID： 18
實作題 #B
請問 "ak02.hw.balancelog" 與 "ak02.hw.balancelog2" 這兩個 topics 裡那一個 topic 的訊息筆數比較多?


(1) ak02.hw.balancelog
(2) ak02.hw.balancelog2
(3) they have same record count
 問題 ID： 19
實作題 #B
當你 / 妳 consume 完 topic "ak02.hw.balancelog" 最後一個 offset 的訊息後, 請問每一個 unique 商品貨物編號最後的商品數量的結餘 (balance) 數量是多少?

 請用 Java Producer 送一筆資料到 "作業指定的 Kafka Topic, msgKey 是你的學員號碼加題目 id (比如"dsxxxx|19"),msgValue 是你 / 妳找到每個商品貨物編號與最後的 balance 值 (比如"part_xxx=134|part_yyy=-23|part_zzz=77")。用"="來分隔商品貨物編號與最後的 balance 值 , 用"|" 來分隔每個資料。


 問題 ID： 20
實作題 #B
當你 / 妳 consume 完 topic "ak02.hw.balancelog2" 最後一個 offset 的訊息後, 請問每一個 unique 商品貨物編號最後的商品數量的結餘 (balance) 是多少?

 請用 Java Producer 送一筆資料到作業指定的 Kafka Topic, msgKey 是你的學員號碼加題目 id (比如 "dsxxxx|20"), msgValue 是你 / 妳找到每個商品貨物編號與最後的 balance 值 (比如 "part_xxx=134|part_yyy=-23|part_zzz=77" )。用 "=" 來分隔商品貨物編號與最後的 balance 值 , 用 "|" 來分隔每個資料。


