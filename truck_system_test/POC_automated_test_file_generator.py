import sys
import json
import unittest
import math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta



class POCAutomateTestFileGenerator(unittest.TestCase):

    def __init__(self, test_case_csv_file):

        self.filename = test_case_csv_file
        self.readTestCaseFile()

    def readTestCaseFile(self):
        test_cases_df = pd.read_csv(self.filename)
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

        # print(test_cases)
        self.test_cases = test_cases
        self.test_case_id_list = test_cases_df['test_case_id'].unique().tolist()

    def traversingTestCases(self):
        test_case_string = '''
import unittest
import math
import json
import unittest
import pandas as pd

class MyPOCTest(unittest.TestCase):
    def setUp(self):
        test_cases_df = pd.read_csv('/Users/krai/truck_delivery_system/truck_system_test/example_test_cases/testcase1.csv')

        # [ REFRACTOR ] - combinable
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
                    input_list = []
                    output_list = []
                 

                input_list.append(row[['warehouse_id', 'warehouse_manager_id', 'receiver_id','receiver_manager_id','travel_time','goods_list','truck_order','delivery_time_interval']].to_list())
                output_list.append(row[['output']].tolist())

            test_cases.update({prev_case_id:{"input":input_list, "output":output_list}})

        # Test Cases Traversal
        test_case_id_list = test_cases_df['test_case_id'].unique().tolist()

        self.clean_test_cases_dict = {}
        for test_case_id in test_case_id_list:
            # remove NaN
            clean_output_value = []
            for output_value in test_cases[test_case_id]['output']:
                if type(output_value[0]) is not float or not math.isnan(output_value[0]):
                    output_value = json.loads(output_value[0])
                    clean_output_value.append(output_value)
                
            # just for future cleaning
            clean_input_value = []
            for input_value in test_cases[test_case_id]['input']:
                clean_input_value.append(input_value)

            self.clean_test_cases_dict.update({str(test_case_id)+"_input":clean_input_value, str(test_case_id)+"_output":clean_output_value})
            
        '''
        # Test Cases Traversal
        for test_case_id in self.test_case_id_list:
            print("INPUT:\n")
            for input_value in self.test_cases[test_case_id]['input']:
                print(input_value)

            print("OUTPUT:\n")
            clean_output_value = []
            for output_value in self.test_cases[test_case_id]['output']:
                # print("HAEK HERE")
                # print(output_value[0], output_value)# 
                if type(output_value[0]) is not float or not math.isnan(output_value[0]):
                    output_value = json.loads(output_value[0])
                    print(output_value)
                    clean_output_value.append(output_value)
                # print("OR HERE")
             

            if len(self.test_cases[test_case_id]['input']) == len(clean_output_value) and len(clean_output_value) > 1:
                # generate
                test_case_string += '''
    def test_''' + str(test_case_id) + '''(self):'''
                for i in range(len(self.test_cases[test_case_id]['input'])):
                    test_case_string += '''
        # [ Mutiple Request Case ] - sucess, error, error
        ''' + str(test_case_id) + '''_input = self.clean_test_cases_dict["''' + str(test_case_id) + '''_input"]
        ''' + str(test_case_id) + '''_output = self.clean_test_cases_dict["''' + str(test_case_id) + '''_output"]
        # INPUT: tx_input[n] | OUTPUT: tx_output[n]
        self.assertEqual(''' + str(test_case_id) + '''_output, ''' + str(test_case_id) + '''_output)
                    '''
            
            elif len(self.test_cases[test_case_id]['input']) == 1:
                # self.assertEqual("Hello", "Hello")
                test_case_string += '''
    def test_''' + str(test_case_id) + '''(self):
    '''
                test_case_string += '''
        # [ Single Request Case ] - Single Output
        ''' + str(test_case_id) + '''_input = self.clean_test_cases_dict["''' + str(test_case_id) + '''_input"]
        ''' + str(test_case_id) + '''_output = self.clean_test_cases_dict["''' + str(test_case_id) + '''_output"]
        # INPUT: tx_input[0] | OUTPUT: tx_output[0]
        self.assertEqual(''' + str(test_case_id) + '''_output, ''' + str(test_case_id) + '''_output)
                    '''

            elif len(self.test_cases[test_case_id]['input']) > len(clean_output_value):
                # self.assertEqual(self.test_cases[test_case_id]['input'], output_value)
                test_case_string += '''
    def test_''' + str(test_case_id) + '''(self):
    '''
                test_case_string += '''
        # [ Multiple Request Case ] - Single Output
        ''' + str(test_case_id) + '''_input = self.clean_test_cases_dict["''' + str(test_case_id) + '''_input"]
        ''' + str(test_case_id) + '''_output = self.clean_test_cases_dict["''' + str(test_case_id) + '''_output"]
        # INPUT: tx_input[0:n] | OUTPUT: tx_output[0]
        self.assertEqual(''' + str(test_case_id) + '''_output, ''' + str(test_case_id) + '''_output)
                    '''

        test_case_string += '''
if __name__ == '__main__':
    unittest.main()

        '''
        self.createTestFile(test_case_string)

    def createTestFile(self, test_case_string):
        file_path = '/Users/krai/truck_delivery_system/truck_system_test/example_test_file/test1.py'  # Specify the file path where you want to save the .py file

        with open(file_path, 'w') as file:
            file.write(test_case_string)



filename = '/Users/krai/truck_delivery_system/truck_system_test/example_test_cases/testcase1.csv'

atfg = POCAutomateTestFileGenerator(filename)
atfg.traversingTestCases()