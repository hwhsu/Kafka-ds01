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

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
import sys
from datetime import datetime
from json import JSONEncoder
import json
from model.Taxidata import Taxidata

'''
 * 一個從Kafka訂閱訊息的範例程式。使用前請先修改：
 * (1) KAFKA_BROKER_URL
 * (2) STUDENT_ID
'''

# 基本參數
KAFKA_BROKER_URL = 'localhost:9092'    # 修改成要連接的Kafka群
WORKSHOP_ID = 'ds01'              # 修改成tdea工作坊編號
STUDENT_ID = 'ds0015'            # 修改成你/妳的學生編號


# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


# 轉換msgKey或msgValue成為utf-8的字串
def try_decode_utf8(data):
    if data != None:
        return data.decode('utf-8')
    else:
        return None

# 轉換Taxidata的物件成為JSON字串
class TaxidataEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, Taxidata):
            return object.__dict__
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)


if __name__ == '__main__':
    # 步驟1.設定要連線到Kafka集群的相關設定
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

    # 步驟1. 設定Producer要連線到Kafka集群的相關設定
    producer_props = {
        # Kafka集群在那裡?
        'bootstrap.servers': KAFKA_BROKER_URL,  # Kafka集群在那裡? (置換成要連接的Kafka集群)
        'error_cb': error_cb  # 設定接收error訊息的callback函數
    }

    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(**producer_props)

    # 步驟3. 設定Consumer要連線到Kafka集群的相關設定
    consumer_props = {
        'bootstrap.servers': KAFKA_BROKER_URL,          # Kafka集群在那裡? (置換成要連接的Kafka集群)
        'group.id': STUDENT_ID,                             # ConsumerGroup的名稱 (置換成你/妳的學員ID)
        'auto.offset.reset': 'earliest',                # Offset從最前面開始
        'session.timeout.ms': 6000,
        'error_cb': error_cb                            # 設定接收error訊息的callback函數
    }

    # 步驟4. 產生一個Kafka的Consumer的實例
    consumer = Consumer(consumer_props)

    # 步驟5. 指定想要訂閱訊息的topic名稱
    topicName_Sub = "ak03.ws" + WORKSHOP_ID + ".hw1." + STUDENT_ID

    # 步驟6. 指定想要發佈訊息的topic名稱
    topicName_Pub = "ak03.ws" + WORKSHOP_ID + ".hw2." + STUDENT_ID

    # 步驟7. 讓Consumer向Kafka集群訂閱指定的topic
    consumer.subscribe([topicName_Sub])

    # 步驟8. 持續的拉取Kafka有進來的訊息
    recordCounter = 0  # 用來累積收到的record數
    validRecordCount = 0  # 用來計算有效的資料筆數
    invalidRecordCount = 0  # 用來計算無效的資料筆數

    # 一個用來計錄那些row_number為不符合規定的容器 (key: 是row number, value: 是error message)
    invalid_records = {}

    # 一個用來將Date的文字字串轉換成Date物件的格式
    dateStringFormat = '%Y/%m/%d %H:%M'

    taxidataJsonEncoder = TaxidataEncoder()

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
                    # Error or event
                    if record.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (record.topic(), record.partition(), record.offset()))
                    else:
                        # Error
                        raise KafkaException(record.error())
                else:
                    # ** 在這裡進行商業邏輯與訊息處理 **
                    # 取出相關的metadata
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    timestamp = record.timestamp()
                    # 取出msgKey與msgValue
                    msgKey = try_decode_utf8(record.key())
                    msgValue = try_decode_utf8(record.value())

                    # ** 根據Spec解析msgValue

                    # 檢查資料是否有值且不能空白
                    if msgValue is None or len(msgKey) <= 0:
                        # 記錄
                        invalidRecordCount += 1
                        invalid_records[msgKey] = 'Record is either null or empty'
                        continue

                    # 解析內容 (應該要有21個欄位值)
                    elements = msgValue.split(',')

                    if len(elements) < 20 or len(elements) > 21:
                        # 記錄
                        invalidRecordCount += 1
                        invalid_records[msgKey] = 'Record elements size is not correct'
                        continue

                    try:
                        # 進行每個欄位的DataType的轉換與解析
                        row_id = msgKey
                        medallion = elements[0]
                        hack_license = elements[1]
                        vendor_id = elements[2]
                        payment_type = elements[3]
                        fare_amount = float(elements[4])
                        surcharge = float(elements[5])
                        mta_tax = float(elements[6])
                        tip_amount = float(elements[7])
                        tolls_amount = float(elements[8])
                        total_amount = float(elements[9])
                        rate_code = int(elements[10])

                        pickup_datetime = int(datetime.strptime(elements[11], dateStringFormat).timestamp() * 1000)
                        dropoff_datetime = int(datetime.strptime(elements[12], dateStringFormat).timestamp() * 1000)

                        passenger_count = int(elements[13])
                        trip_time_in_secs = int(elements[14])
                        trip_distance = float(elements[15])
                        pickup_longitude = float(elements[16])
                        pickup_latitude = float(elements[17])
                        dropoff_longitude = float(elements[18])
                        dropoff_latitude = float(elements[19])
                        credit_card = ''
                        if (len(elements) == 21):
                            credit_card = elements[20]

                        # 建立Taxidata的實例
                        taxidata = Taxidata(row_id, medallion, hack_license, vendor_id, payment_type,
                                            fare_amount, surcharge, mta_tax, tip_amount, tolls_amount, total_amount, rate_code,
                                            pickup_datetime, dropoff_datetime, passenger_count, trip_time_in_secs, trip_distance,
                                            pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, credit_card)

                        json_string = taxidataJsonEncoder.encode(taxidata)  # 使用客製的JSON encoder來處理datetime的物件

                        # 打印JSON
                        print(json_string)

                        # 發佈訊息到新的Topic
                        producer.produce(topicName_Pub, key=msgKey, value=json_string)
                        producer.poll(0)

                        validRecordCount += 1

                    except Exception as e:
                        # 記錄
                        invalidRecordCount += 1
                        if hasattr(e, 'message'):
                            invalid_records[msgKey] = e.message
                            print(e.message)
                        else:
                            invalid_records[msgKey] = str(e)

            print('Total received records: ' + str(recordCounter))
            print('Total Valid records: ' + str(validRecordCount))
            print('Total Invalid records: ' + str(invalidRecordCount))
            print('Invalid record numbers: ' + str(invalid_records))
            print('--------------------------------------------')

            # ** 觀察產生的 "Total received records"的數值, 如果沒有持續增加就代表
            # 程式己經把現在topic裡有的訊息全部都收進來並且你看到的結果就是問題的答案 **

    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')
    except Exception as e:
        sys.stderr.write(e)

    finally:
        # 步驟6.關掉Consumer實例的連線
        consumer.close()
        producer.flush(10)
