#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from confluent_kafka import Consumer, KafkaException, KafkaError

import sys
import json

'''
 * Tips:
 * 由於13題主要是要練習如何利用簡單的判斷來得到某種觀測值的"最大值"與"最小值"。同時透過過濾的手法在
 * 串流資料中得到想要處理的資料。
 * （Select Max(observe_value), Min(observe_value) From xxx Where a='yy' and b='zz' Group By field_A ...)
 * 另如, 這題也是來對如何從串流中對JSON反序例化, 然後計算。
'''

# 基本參數
KAFKA_BROKER_URL = 'localhost:9092'    # 修改成要連接的Kafka群
WORKSHOP_ID      = 'ds01'              # 修改成tdea工作坊編號
STUDENT_ID       = 'ds0015'            # 修改成你/妳的學生編號


# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


# 轉換msgKey或msgValue成為utf-8的字串
def try_decode_utf8(data):
    if data is not None:
        return data.decode('utf-8')
    else:
        return None

# 用來記錄是否為第一次的Rebalance事件
isFirstTime = True

# 一個callback函式, 用來重設某一個ConsumerGroup的offset值到一個Topic/Partition的最小值。方便測試與教學
def seek_to_begin(consumer, partitions):
    global isFirstTime
    # 監聽Kafka的Consumer Rebalance的event, 如果是程式跑起來的第一次
    # 我們重新對每一個partition的offset來進行重置到現在partition最小的offset值
    if isFirstTime:
        for p in partitions:
            p.offset = 0
        print('assign', partitions)
        consumer.assign(partitions)
        isFirstTime = False
        print('Reset offset to beginning')


# 主程式進入點 <---
if __name__ == '__main__':
    # 步驟1.設定要連線到Kafka集群的相關設定
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    props = {
        'bootstrap.servers': KAFKA_BROKER_URL,          # Kafka集群在那裡? (置換成要連接的Kafka集群)
        'group.id': STUDENT_ID,                         # ConsumerGroup的名稱 (置換成你/妳的學員ID)
        'auto.offset.reset': 'earliest',                # Offset從最前面開始
        'session.timeout.ms': 6000,
        'error_cb': error_cb                            # 設定接收error訊息的callback函數
    }

    # 步驟2. 產生一個Kafka的Consumer的實例
    consumer = Consumer(props)
    # 步驟3. 指定想要訂閱訊息的topic名稱
    topicName = 'ak03.ws' + WORKSHOP_ID + '.hw2.' + STUDENT_ID;
    # 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
    consumer.subscribe([topicName], on_assign=seek_to_begin) # ** Tips: 讓這支程式每次重起時都把offset移到最前面
    # 步驟5. 持續的拉取Kafka有進來的訊息

    record_counter = 0 # 用來累積收到的record數

    # 用來記錄最大與最小的"fare_amount" <---- 存放 "題目#13" 答案的容器
    min_fare_amount = None
    max_fare_amount = None

    try:
        while True:
            # 請求Kafka把新的訊息吐出來
            records = consumer.consume(num_messages=500, timeout=1.0)  # 批次讀取
            if records is None:
                continue

            for record in records:
                # 檢查是否有錯誤
                if record is None:
                    continue
                if record.error():
                    # 偵測是否己經讀到了partiton的最尾端
                    if record.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (record.topic(), record.partition(), record.offset()))
                    else:
                        # Error
                        raise KafkaException(record.error())
                else:
                    record_counter += 1
                    # ** 在這裡進行商業邏輯與訊息處理 **
                    # 取出相關的metadata
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    timestamp = record.timestamp()
                    # 取出msgKey與msgValue
                    msgKey = try_decode_utf8(record.key())      # << 這個是row_id編號
                    msgValue = try_decode_utf8(record.value())  # << 這個是taxidata資料

                    taxidata = json.loads(msgValue)

                    # 根據題義取出以下3個欄位vendor_id, payment_type及fare_amount
                    vendor_id = taxidata['vendor_id']
                    payment_type = taxidata['payment_type']
                    fare_amount = taxidata['fare_amount']

                    if vendor_id=='VTS' and payment_type=='CRD':
                        # *** 你要開發的Block在這裡 [Start] ***

                        # Tips: 比較fare_amount與min_fare_amount及比較fare_amount與max_fare_amount
                        #       把最小與最大的值保留下來

                        # ...
                        print('...') # 移除這行不必要的print('...')
                        # ...

                        # *** 你要開發的Block在這裡 [End] ***
            # 打印出最更新的結果 <---- "題目#13" 的答案
            print('Total received records: ' + str(record_counter))
            print('fare_amount-Min: ' + str(min_fare_amount))
            print('fare_amount-Max: ' + str(max_fare_amount))

            # 觀察Consumer是否己經抵達topic/partiton的最尾端的offset
            # 如果程式己經把現在topic裡有的訊息全部都吃進來你看到的結果就是問題的答案

    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')
    except KafkaException as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

    finally:
        # 步驟6.關掉Consumer實例的連線
        consumer.close()
