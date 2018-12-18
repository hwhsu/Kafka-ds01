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

# 一個Employee的類別, 用來作DTO (Data Tranfer Object)使用
class Employee:

    def __init__(self, id='', firstName='', lastName='', deptId='',
                 hireDate=None, terminationDate=None, wage=0.0,
                 age=0, sex=False):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.deptId = deptId
        self.hireDate = hireDate
        self.terminationDate = terminationDate
        self.wage = wage
        self.age = age
        self.sex = sex
