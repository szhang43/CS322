"""
Nose test for mongo.py
"""

import sys
sys.path.append("..")
from mongo import get_data, insert_new
import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)
 
def test_insert_and_fetch1():
    # insert test data
    distance = 100
    other = {"km": 50, "open_time": '2021-01-01T01:28', "close_time": '2021-01-01T03:30', 
    "begin_date": '2021-01-01T00:00',"miles": '31.068550'}

    insert_new(distance, other)
    
    # fetch data using get_data function
    result_distance, result_other = get_data()
    
    # compare the fetched data with inserted data
    assert result_distance == distance
    assert result_other == other

def test_insert_and_fetch2():
    # insert test data
    distance = 100
    other = {"km": 200, "open_time": '2021-01-01T07:53', "close_time": '2021-01-01T15:20', 
    "begin_date": '2021-01-01T02:00', "miles": '124.274200', "location": "CP1"}

    insert_new(distance, other)
    
    # fetch data using get_data function
    result_distance, result_other = get_data()
    
    # compare the fetched data with inserted data
    assert result_distance == distance
    assert result_other == other

test_insert_and_fetch1()
test_insert_and_fetch2()