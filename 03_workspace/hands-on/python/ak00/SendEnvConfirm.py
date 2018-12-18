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
import sys
import platform
import json
from model.StudentEnv import StudentEnv

'''
 * 一個發佈訊息到Kafka的範例程式。使用前請先修改：
 * (1) KAFKA_BROKER_URL
 * (2) WORKSHOP_ID
 * (3) STUDENT_ID
'''

# 基本參數
KAFKA_BROKER_URL = 'streamgeeks.org:9092'     # 設定要連接的Kafka群
WORKSHOP_ID = 'ds01'                      # 修改成這次的工作坊編號
STUDENT_ID = 'ds0015'               # 修改成你/妳的學生編號


# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


# 檢查學員的Python環境與O.S
def buildStudentEnv():
    os = platform.system() + ' ' + platform.release()

    studentEnv = StudentEnv(STUDENT_ID, os, platform.release())
    studentEnv.setEnvAttr('langName', 'Python')
    studentEnv.setEnvAttr('langVersion', platform.python_version())
    return studentEnv


# 主程式進入點
if __name__ == '__main__':
    # 步驟1. 設定要連線到Kafka集群的相關設定
    props = {
        # Kafka集群在那裡?
        'bootstrap.servers': KAFKA_BROKER_URL,  # <-- 置換成要連接的Kafka集群
        'error_cb': error_cb  # 設定接收error訊息的callback函數
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(**props)

    # 步驟3. 指定想要發佈訊息的topic名稱
    topicName = 'ak00.ws'+WORKSHOP_ID+'.env'

    msgCounter = 0
    try:
        studentEnv = buildStudentEnv()
        # 轉換成JSON字串
        studentEnvJson = json.dumps(studentEnv.__dict__)
        print(studentEnvJson)

        # 發佈學員系統環境訊息到Kakfa以便助教幫助學員解決環境問題
        producer.produce(topicName, key=STUDENT_ID, value=studentEnvJson)

        msgCounter+=1
        print('Send ' + str(msgCounter) + ' messages to Kafka')
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
    except Exception as e:
        print(e)
    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()



