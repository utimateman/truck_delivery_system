
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
            
        
    def test_t1(self):
    
        # [ Single Request Case ] - Single Output
        t1_input = self.clean_test_cases_dict["t1_input"]
        t1_output = self.clean_test_cases_dict["t1_output"]
        # INPUT: tx_input[0] | OUTPUT: tx_output[0]
        self.assertEqual(t1_output, t1_output)
                    
    def test_t2(self):
    
        # [ Single Request Case ] - Single Output
        t2_input = self.clean_test_cases_dict["t2_input"]
        t2_output = self.clean_test_cases_dict["t2_output"]
        # INPUT: tx_input[0] | OUTPUT: tx_output[0]
        self.assertEqual(t2_output, t2_output)
                    
    def test_t3(self):
        # [ Mutiple Request Case ] - sucess, error, error
        t3_input = self.clean_test_cases_dict["t3_input"]
        t3_output = self.clean_test_cases_dict["t3_output"]
        # INPUT: tx_input[n] | OUTPUT: tx_output[n]
        self.assertEqual(t3_output, t3_output)
                    
        # [ Mutiple Request Case ] - sucess, error, error
        t3_input = self.clean_test_cases_dict["t3_input"]
        t3_output = self.clean_test_cases_dict["t3_output"]
        # INPUT: tx_input[n] | OUTPUT: tx_output[n]
        self.assertEqual(t3_output, t3_output)
                    
    def test_t4(self):
    
        # [ Multiple Request Case ] - Single Output
        t4_input = self.clean_test_cases_dict["t4_input"]
        t4_output = self.clean_test_cases_dict["t4_output"]
        # INPUT: tx_input[0:n] | OUTPUT: tx_output[0]
        self.assertEqual(t4_output, t4_output)
                    
if __name__ == '__main__':
    unittest.main()

        