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

'''
 * Tips:
 * 由於15題主要是By每一個unique的商品貨物編號算出它的庫存異動數,在資料處理上, 我們先對msgValue進行解析。
 * 然後可以利用一個"Map(key是part_no, value是庫存異動數)"來保存庫存值加減之後的結果。
 *
 * 公式: 期初庫存 + 庫存異動數 = 期末庫存
 *
 * 只要知道公式中的其中兩個值就可以知道剩下的那個值了。

'''

# 基本參數
KAFKA_BROKER_URL = 'localhost:9092'         # 設定要連接的Kafka群
STUDENT_ID       = 'ds0015'                 # 修改成你/妳的學員編號


# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


# 轉換msgKey或msgValue成為utf-8的字串
def try_decode_utf8(data):
    if data is not None:
        return data.decode('utf-8')
    else:
        return None


# 對dictionary物件以key值的順序來排序
def dict_sort(dictData):
    new_dict = {}
    for key in sorted(dictData.keys()):
        new_dict[key] = dictData[key]

    return new_dict

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
    topicName = 'ak02.hw.translog'
    # 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
    consumer.subscribe([topicName], on_assign=seek_to_begin) # ** Tips: 讓這支程式每次重起時都把offset移到最前面
    # 步驟5. 持續的拉取Kafka有進來的訊息
    record_counter = 0

    # 產生一個Map: key是part_no, value是qty balance <---- 存放 "題目#15" 庫存異動數的容器
    parts_transQtyBalance = {}

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
                    # 偵測是否己經讀到了partition的最尾端
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
                    msgKey = try_decode_utf8(record.key())      # << 這個是商品貨物編號
                    msgValue = try_decode_utf8(record.value())  # << 這個是商品貨物交易資料

                    # ** "題目#15" 的主要邏輯 **
                    # 把"商品貨物編號"與"計數"放進一個Dict(key是part_no, value是record count)的容器中

                    # *** 你要開發的Block在這裡 [Start] ***
                    # Tips: 在Python中把(key,value)放進"Dict"的collection, 使用的method是 dict_object[key]=value

                    # Tips: 解析msgValue, 根據spec: msgValue是交易的內容(例如 "+|123" , 資料用"|"做分隔
                    #                         第一個欄位"+"代表是庫存量的增加, "-"代表庫存量的減少
                    #                         第二個欄位代表庫存的異動量

                    elements = msgValue.split('|')

                    opType = elements[0]  # "+"代表是庫存量的增加, "-"代表庫存量的減少
                    transQty = int(elements[1])  # 庫存的異動量

                    # 檢查看Dict中是否存在msgKey
                    if msgKey in parts_transQtyBalance:
                        # 把之前的筆數拿回來, 加1之後再放去
                        transQtyBalance = parts_transQtyBalance[msgKey]
                        # 檢查opertion type是'+'或'-'
                        if opType == '+':
                            parts_transQtyBalance[msgKey] = (transQtyBalance + transQty)
                        else:
                            parts_transQtyBalance[msgKey] = (transQtyBalance - transQty)
                    else:
                        # 這是第1筆, 設定初始值
                        init_qty = 0
                        # 檢查opertion type是'+'或'-'
                        if opType == '+':
                            parts_transQtyBalance[msgKey] = (init_qty + transQty)
                        else:
                            parts_transQtyBalance[msgKey] = (init_qty - transQty)

                    # *** 你要開發的Block在這裡 [End] ***

            # 打印出最更新的結果 <---- "題目#15" 的答案
            print('Parts transQtyBalance: ' + '|'.join(f'{k}={v}' for k, v in dict_sort(parts_transQtyBalance).items()))

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
