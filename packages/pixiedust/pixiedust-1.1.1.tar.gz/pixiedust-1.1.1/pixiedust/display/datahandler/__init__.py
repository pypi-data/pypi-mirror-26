# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2017
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------
from pixiedust.utils.environment import Environment
if Environment.hasSpark:
    from .pysparkDataFrameHandler import PySparkDataFrameDataHandler
from .pandasDataFrameHandler import PandasDataFrameDataHandler
import pixiedust.utils.dataFrameMisc as dataFrameMisc
from pixiedust.display.streaming import *

def getDataHandler(options, entity):
    if dataFrameMisc.isPySparkDataFrame(entity):
        return PySparkDataFrameDataHandler(options, entity)
    elif dataFrameMisc.isPandasDataFrame(entity):
        return PandasDataFrameDataHandler(options, entity)
    elif isinstance(entity, StreamingDataAdapter):
        return entity.getDisplayDataHandler(options, entity)

    return None