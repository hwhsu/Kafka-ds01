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
import sys, traceback

'''
 * Tips:
 * 由於要驗證在一個有5個partitions的topic, 如果msgKey是"whereami"的訊息會被推送到那一個partitions。可以依以下步驟來實驗:
 *
 * Step1. 先用kakfa-topics的command來產生一個有5個partitons的topic:
 * kafka-topics --create \
 *   --zookeeper zookeeper:2181 \
 *   --replication-factor 1 \
 *   --partitions 5 \
 *   --topic topic5p
 *
 * Step2. 再用Homework_q02_pub來推送一筆msgKey是"whereami"的訊息
 * Step3. 再用Homework_q02來訂閱這個topic, 然後看message的metadata就得到了解答
'''

# 基本參數
KAFKA_BROKER_URL = 'localhost:9092'         # 設定要連接的Kafka群
WORKSHOP_ID      = 'ds01'                   # 修改成tdea工作坊編號
STUDENT_ID       = 'ds0015'                 # 修改成你/妳的學員編號


# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


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
    topicName = 'topic5p'
    msgCounter = 1
    try:
        print('Start sending messages...')
        # 步驟4.產生要發佈到Kafka的訊息
        #      - 參數#1: topicName, 參數#2: msgValue, 參數#3: msgKey
        producer.produce(topicName, key='whereami', value='test')
        producer.poll(0)

        print('Send ' + str(msgCounter) + ' messages to Kafka')

    except BufferError as e:
        # 錯誤處理
        sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
    except KafkaException as e:
        traceback.print_exc(file=sys.stdout)

    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()
