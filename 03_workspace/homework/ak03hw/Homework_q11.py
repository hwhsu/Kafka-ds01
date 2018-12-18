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

from confluent_kafka import Producer, KafkaException
import time
import sys


'''
 * Tips:
 * 由於11題主要是要練習Row(行)的方式讀取CSV並將之拋轉進Kafka, 目的只是為了產生q12所需要的event data。
 * 這個程式只能跑一次, 不然資料會重覆。如果有問題, 則需要使用kafka-topic的command來移除topic再重拋!
'''

# 基本參數
KAFKA_BROKER_URL = 'localhost:9092'    # 修改成要連接的Kafka群
WORKSHOP_ID      = 'ds01'              # 修改成tdea工作坊編號
STUDENT_ID       = 'dsxxxx'            # 修改成你/妳的學員編號


# 用來取得現在時間的（millis)
def current_milli_time():
    return int(round(time.time() * 1000))


# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)

# 用來取得每一筆訊息(per-message)傳送到Kafka的delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently failed delivery (after retries).
def delivery_cb(err, msg):
    if err:
        sys.stderr.write('Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('[%s]:[%s]:[%s] -- Row Number: %s \n' %
                         (msg.topic(), msg.partition(), msg.offset(), msg.key().decode('utf-8')))


# 主程式進入點
if __name__ == '__main__':
    # 步驟1. 設定要連線到Kafka集群的相關設定
    props = {
        # Kafka集群在那裡?
        'bootstrap.servers': KAFKA_BROKER_URL,  # Kafka集群在那裡? (置換成要連接的Kafka集群)
        'error_cb': error_cb                    # 設定接收error訊息的callback函數
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(**props)

    # 步驟3. 指定想要發佈訊息的topic名稱
    topicName = 'ak03.ws' + WORKSHOP_ID + '.hw1.' + STUDENT_ID

    # 步驟4: 讀取讀取CSV的檔案(注意: nyc_taxi_data.csv必需要在專案的根目錄
    csv_file = 'nyc_taxi_data.csv'

    validRecordCount = 0 # 用來計算有效的資料筆數
    invalidRecordCount = 0 # 用來計算無效的資料筆數
    rowNumber = 0 # 用來產生一個遞增的row_id

    # 逐行讀取CSV的每一行資料
    dataFile = open(csv_file)

    lineContent = dataFile.readline()
    rowNumber += 1

    while lineContent:
        if rowNumber==1:
            lineContent = dataFile.readline()  # 再讀一筆
            rowNumber += 1
            continue # 由於第一行是header, 所以我們要ignore

        # 進行每一行的資料檢查或相對應的處理
        if lineContent is None or len(lineContent) <= 0:
            invalidRecordCount+=1
        else:
            validRecordCount+=1 # 這是一筆有效的資料
            producer.produce(topicName, key=str(rowNumber-1), value=lineContent.rstrip(), callback=delivery_cb)
            print(str(rowNumber) + ',' + lineContent)

        # 呼叫poll來讓client程式去檢查內部的Buffer
        producer.poll(0)

        lineContent = dataFile.readline() # 再讀一筆
        if lineContent is not None and len(lineContent.rstrip())>0:
            rowNumber+=1


    print('Total CSV records: ' + str(rowNumber-1))
    print('Total Valid records: ' + str(validRecordCount))
    print('Total Invalid records: ' + str(invalidRecordCount))

    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush(10) # 最長等待10秒
