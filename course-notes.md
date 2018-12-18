# DS01: Kafka 核心基石

## AK01

- Kafka connect (source): 透過萬用接頭，只要調整 config，就能串接各種各式的來源
- Disk based 儲存
- 觀念:
    - streaming 沒有辦法控制資料的流量、流速，只能作反應
- Topic: 頻道的概念，類似 DB 的 Table
    - 每個 partition 是有順序性的，類似 FIFO queue。其中的 id 稱為 "offset"
    - 資料預設保留 7 天
    - 資料是 immutable (無法更改)
- Partition
    - 資料夾的概念，裡面可存放資料
    - 一個 topic 可以切分不同 partition (放到不同 broker?)
    - 其中有一個 Leader 會幫忙處理 replication，同步資料到其他 ISA (in-sync replica)
- Brokers: 叢集中的每台機器
    - 可以設定 replication: 最多可允許 N-1 台機器掛掉
- Producer
    - which producer? which topic?
    - acks = 0, 1, -1 (all)
        - 0: 不確認
        - 1: 只確認 leader 收到
        - -1: 確認 replicas 都有收到
    - message key: 可給、可不給。如果有 key 就能確保放在同一個 partition，就有全局順序性
        - 有 key: hashs
        - 當把不包含"key"的訊息推送到一個有著多個partitions的topic中裡，Kafka會如何決定要把這筆record派送到那個partition中? round-bin
- Consumer
    - 訂閱制
    - consumer group:
        - 一個 partition 只能給同一個 consumer group 中的一個 consumer 消費
- Consumer offset
    - 自動生成 `__consumer_offset` 的 topic 來記錄 consumer 消費到哪裡
    - `[topic, partition, consumer_group]`
- Replay
    - 從某個點之後再讀一次資料

### Example Commands

List all topics:

```
kafka-topics --list --zookeeper zookeeper:2181
```

Delete a topic

```

```

## AK02

- "partition" cand "replication" settings
    - 中途增加 partition: 造成 hash 改變
    - 中途增加 replication: 造成效能影響
- partition
    - 代表平行度
    - 太大: 有很多 file 需要維護，一個 leader 要管很多 replica，影響效能
    - 太小: 平行度不足
    - 建議: (1 ~ 2) * (number of brokers)
- replication factor
    - `>=2`, maximum `3`
    - 當設定到 N-1 broker 時可能 fail
- Segment: 實體檔案的概念，存放多筆 records
    - active segment: 正在寫入的 segment
    - 可設定 單位大小 or 單位時間
    - 有 index 記錄 offsets: `[xxxxxx ~ xxxxxx, xxxxxx ~ xxxxxx]`
    - 單位大小設太小的話，會形成很多 segment，造成效能影響 (頻繁地 log compaction, ...)
- log cleanup policies `cleanup.policy`:
    1. `delete`:
        - 時間 `log.retention.hours` (預設 7 天)
        - max size for each partition `log.retention.bytes`
    2. `compact`:
        - 只依照 key 來運作，依據當下 partition 中的 key，刪除前面同一個 key 的資料，__只保留最後一筆資料__
        - 不會改變 order 和 offset value
        - 因為只保留結果，可減少 replay 的時間
        - 可利用 update 一筆相同的 key，值是 null，最後 `compact` 後會只留下那一筆 null 的資料。當要 consume 時過濾掉 null 時，可視為 delete 的應用
        - Very useful if we just require a SNAPSHOT instead of full history
        - 限制: 只能用在過程不重要，只需要結果的資料
- Log compression 壓縮
    - 只能針對 text 的資料壓縮 (json, xml, csv, txt)
    - `max.message.bytes` (default 1MB)
    - `min.isync.replicas` (default 1): 當 `acks=all` 時，確認幾個 ISR 收到資料再回覆

### Topic Configuration

https://kafka.apache.org/documentation/#topicconfigs

Example config:

```
Topic:my-topic  PartitionCount:3    ReplicationFactor:1 Configs:max.message.bytes=64000,flush.messages=1  <-- here the config
    Topic: my-topic Partition: 0    Leader: 1   Replicas: 1 Isr: 1
    Topic: my-topic Partition: 1    Leader: 1   Replicas: 1 Isr: 1
    Topic: my-topic Partition: 2    Leader: 1   Replicas: 1 Isr: 1
```

- update config: `--alter`

### Broker configuration

https://kafka.apache.org/documentation/#brokerconfigs

- 臨時要調整某個 topic 的 keep policy?
- dynamuc update mode: 是否需要重開機設定才能生效
    - read-only: need to restart
    - per-broker
    - cluster-wide

## AK03

- 如何傳送訊息
    - fire-and-forget
    - async: 一直傳送資料，帶 "callback function" 去確認資料是否收到
    - 即使設定 `enable.idempotence=True`，也要用 callback function 確認是否有重複的 key 去處理
- Rebalence
    - 當 partition 或 consumer 的數量、狀態有變，兩邊不平衡，就會自動 rebalance
    - 先 **revoke** 收回權限，重新 **assign** "produce-consume" 的配對
- Commits and Oddsets: 每消費過的資料就會 commit 已消費資料的 offset 回去 `__consumer_offset`
    - auto-commit (NOT recommended!!!)
        - 設定 interval，時間到就 commit
        - 不太有彈性處理例外狀況，例如：當一批資料還在傳送過程中時間就到了，還沒收到資料或正在處理資料就 commit 了，後端就會漏資料。
    - sync-commit
        - `offset.reset=earliest`, `auto.commit=False`
        - 處理完商業邏輯後才 commit
        - timeout, mini-batch
        - 失敗時會不斷 retry 拿資料
        - 缺點: 會鎖住，throughput 低
    - async-commit
        - 失敗時不會 retry，等 Broker 回應時才觸發 callback
    - manual-commit
        - 手動回傳 `[topic, partition, offset]` 的值回去
        - 例如: 一個批次 1000 筆資料，每處理完 200 筆資料就 commit
- Config consumer
    - latest: 從最後一筆資料 consume
    - earliest: 從還沒有 commit 的資料之中，最早的那一筆
- Rebalance Listeners
    - 自訂當發生 revoke 或 assign 時要執行什麼事
    - rebalence 是個 killer，所以 offset 的管理很重要

## Question

- 如何分配 consumer group?
- 
