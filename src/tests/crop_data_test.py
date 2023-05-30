import unittest
import pandas as pd
import os
from crop_lca.crop_model import load_crop_farm_data, print_crop_data, print_crop_data_test
import io
from contextlib import redirect_stdout


def capture_stdout(function, *args, **kwargs):
    f = io.StringIO()
    with redirect_stdout(f):
        function(*args, **kwargs)

    return f.getvalue()


def read_expected_output(filename, path):
    with open(os.path.join(path, filename), "r") as file:
        return file.read()


class DatasetLoadingTestCase(unittest.TestCase):
    def setUp(self):
        self.txt_path = "./data"
        # Create the DataFrame with the provided data

        data = {
            'ef_country': ['ireland', 'ireland', 'ireland', 'ireland', 'ireland'],
            'farm_id': ['2020', '2020', '2020', '2020', '2020'],
            'year': ['2020', '2020', '2020', '2020', '2020'],
            'crop_type': ['barley', 'crops', 'maize', 'spring_wheat', 'winter_wheat'],
            'kg_dm_per_ha': [7.289189, 3.86546, 7.125387, 8.968263, 8.968263],
            'area': [5557.922952642, 200.003617085, 1299.493637777, 1634.363389845, 1634.363389845]
        }

        self.data_frame = pd.DataFrame(data)

    def test_data_set_creation(self):
        # Perform assertions or tests on the loaded DataFrame
        self.assertEqual(len(self.data_frame), 5)  # Example assertion

    def test_output_crop(self):
        data = load_crop_farm_data(self.data_frame)
        print(print_crop_data_test(data))
        output = capture_stdout(print_crop_data_test, data)

        # Validate the output
        expected_output = read_expected_output("crop.txt", self.txt_path)
        #self.assertEqual(output.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
