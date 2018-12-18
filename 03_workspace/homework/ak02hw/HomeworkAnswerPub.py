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
import sys
import traceback

# 用來接收從Consumer instance發出的error訊息


def error_cb(err):
    print('Error: %s' % err)


# 基本參數
KAFKA_BROKER_URL = '192.168.1.2:9092'         # 設定要連接的Kafka群
WORKSHOP_ID = 'ds01'                   # 修改成tdea工作坊編號
STUDENT_ID = 'ds0015'                 # 修改成你/妳的學員編號


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
    topicName = 'ak02.ws' + WORKSHOP_ID + '.homework'  # 個人作業繳交的Topic
    msgCounter = 20  # ak01的作業總共有20題
    try:
        print('Start sending messages...')
        # 步驟4.產生要發佈到Kafka的訊息
        #      - 參數#1: topicName, 參數#2: msgValue, 參數#3: msgKey

        producer.produce(topicName, '5', STUDENT_ID+'|1')  # 第 1題
        producer.produce(topicName, '5', STUDENT_ID+'|2')  # 第 2題
        producer.produce(topicName, '1', STUDENT_ID+'|3')  # 第 3題 ?
        producer.produce(topicName, '2', STUDENT_ID+'|4')  # 第 4題
        producer.produce(topicName, '1', STUDENT_ID+'|5')  # 第 5題 刪除失敗？
        producer.produce(topicName, '4', STUDENT_ID+'|6')  # 第 6題 ?
        producer.produce(topicName, '1', STUDENT_ID+'|7')  # 第 7題
        producer.produce(topicName, '4', STUDENT_ID+'|8')  # 第 8題
        producer.produce(topicName, '5', STUDENT_ID+'|9')  # 第 9題
        producer.produce(topicName, '2', STUDENT_ID+'|10') # 第10題
        producer.produce(topicName, '2', STUDENT_ID+'|11') # 第11題
        producer.produce(topicName, '1', STUDENT_ID+'|12') # 第12題
        producer.produce(topicName, 'part_01|part_02|part_03|part_04|part_05|part_06|part_07|part_08|part_09|part_10', STUDENT_ID+'|13') # 第13題
        producer.produce(topicName, 'part_01=29940|part_02=30127|part_03=29640|part_04=30207|part_05=29930|part_06=30160|part_07=29564|part_08=30114|part_09=30311|part_10=29966', STUDENT_ID+'|14') # 第14題
        producer.produce(topicName, 'part_01=-53996|part_02=70700|part_03=150980|part_04=23869|part_05=-26012|part_06=47989|part_07=-12093|part_08=-19516|part_09=-2037|part_10=-17266', STUDENT_ID+'|15') # 第15題
        producer.produce(topicName, 'part_01=53996|part_02=-70700|part_03=-150980|part_04=-23869|part_05=26012|part_06=-47989|part_07=12093|part_08=19516|part_09=2037|part_10=17266', STUDENT_ID+'|16') # 第16題
        producer.produce(topicName, 'balancelog=10|balancelog2=10', STUDENT_ID+'|17') # 第17題
        producer.produce(topicName, '1', STUDENT_ID+'|18') # 第18題
        producer.produce(topicName, 'part_01=-26843|part_02=24253|part_03=78644|part_04=47302|part_05=-27951|part_06=281|part_07=-13432|part_08=-45876|part_09=26466|part_10=-33698', STUDENT_ID+'|19') # 第19題
        producer.produce(topicName, 'part_01=-66940|part_02=76279|part_03=165482|part_04=12135|part_05=-29397|part_06=38428|part_07=-5960|part_08=-11542|part_09=12274|part_10=-6943', STUDENT_ID+'|20') # 第20題

        producer.poll(0)
        print('Send ' + str(msgCounter) + ' messages to Kafka')
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
    except KafkaException as e:
        traceback.print_exc(file=sys.stdout)

    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()
