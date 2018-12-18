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

from confluent_kafka import Producer
import time


# 用來取得現在時間的（millis)
def current_milli_time():
    return int(round(time.time() * 1000))


# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


# 基本參數
KAFKA_BROKER_URL = 'localhost:9092'         # 設定要連接的Kafka群

# 主程式進入點
if __name__ == '__main__':
    # 步驟1. 設定要連線到Kafka集群的相關設定
    props = {
        # Kafka集群在那裡?
        'bootstrap.servers': KAFKA_BROKER_URL,  # Kafka集群在那裡? (置換成要連接的Kafka集群)
        'queue.buffering.max.messages': 5000000,
        'queue.buffering.max.ms': 60000,
        'batch.num.messages': 100,
        'error_cb': error_cb                    # 設定接收error訊息的callback函數
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(**props)

    # 步驟3. 指定想要發佈訊息的topic名稱
    translog = 'ak02.hw.translog'
    balancelog = 'ak02.hw.balancelog'
    balancelog2 = 'ak02.hw.balancelog2'

    print('Start loading data...')

    dataFile = open('Homework_s02_DataFile.txt')
    line = dataFile.readline()
    while line:
        elements = line.split('|')
        part_no = elements[0]               # 料號
        opType = elements[1]                # "+"代表是庫存量的增加, "-"代表庫存量的減少
        transQty = int(elements[2])         # 庫存的異動量
        balanceBeforeOp = int(elements[3])  # 做交易前的結餘(balance)值
        balanceAfterOp = int(elements[4])   # 做交易後的結餘(balance)值

        # 發佈資料到不同的Kafka topics
        producer.produce(translog, key=part_no, value='{0}|{1}'.format(opType, transQty))
        producer.produce(balancelog, key=part_no, value='{0}|{1}|{2}|{3}'.format(opType, transQty, balanceBeforeOp, balanceAfterOp))
        producer.produce(balancelog2, key=part_no, value='{0}|{1}|{2}|{3}'.format(opType, transQty, balanceBeforeOp, balanceAfterOp))

        # 呼叫poll來讓client程式去檢查內部的Buffer
        producer.poll(0)
        line = dataFile.readline()

    print('Hands on data has loaded to Kafka!')

    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()
