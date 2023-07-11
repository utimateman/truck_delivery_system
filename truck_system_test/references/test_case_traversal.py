import sys
import json
import math
import unittest
import pandas as pd
from datetime import datetime, timedelta




test_cases_df = pd.read_csv('/Users/krai/truck_delivery_system/truck_system_test/example_test_cases/testcase1.csv')
print(test_cases_df)


if len(test_cases_df) > 1:
    input_list = []
    output_list = []
    test_cases = {}
    fieldnames = ['test_case_id', 'test_case_description', 'warehouse_id', 'warehouse_manager_id', 'receiver_id','receiver_manager_id','travel_time','goods_list','truck_order','delivery_time_interval','output']

    prev_case_id = test_cases_df.loc[0,'test_case_id']
    for index, row in test_cases_df.iterrows():
        test_case_id = row['test_case_id']
        if prev_case_id != test_case_id:
            test_cases.update({prev_case_id:{"input":input_list, "output":output_list}})
            prev_case_id = test_case_id
            # print(test_cases)
            input_list = []
            output_list = []
            # continue merging
            # break

        print(row[['test_case_id','warehouse_id', 'warehouse_manager_id', 'receiver_id','receiver_manager_id','travel_time','goods_list','truck_order','delivery_time_interval']])
        input_list.append(row[['warehouse_id', 'warehouse_manager_id', 'receiver_id','receiver_manager_id','travel_time','goods_list','truck_order','delivery_time_interval']].to_list())
        output_list.append(row[['output']].tolist())

    test_cases.update({prev_case_id:{"input":input_list, "output":output_list}})

# Test Cases Traversal
test_case_id_list = test_cases_df['test_case_id'].unique().tolist()

for test_case_id in test_case_id_list:
    print("INPUT:\n")
    for input_value in test_cases[test_case_id]['input']:
        print(input_value)

    print("OUTPUT:\n")
    clean_output_value = []
    for output_value in test_cases[test_case_id]['output']:
        if type(output_value[0]) is not float or not math.isnan(output_value[0]):
            output_value = json.loads(output_value[0])
            print(output_value)
            clean_output_value.append(output_value)