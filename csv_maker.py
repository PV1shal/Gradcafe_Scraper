import csv

class CsvMaker(object):
    def make(self, data_dict):
        if not data_dict:
            print("No data to write.")
            return

        if isinstance(data_dict, dict):
            # Convert the dictionary to a list of dictionaries
            data_list = [data_dict]
        elif isinstance(data_dict, list):
            data_list = data_dict
        else:
            print("Invalid data structure.")
            return

        # print(data_list)
        keys = data_list[0].keys()

        with open('gradcafe.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data_list)
