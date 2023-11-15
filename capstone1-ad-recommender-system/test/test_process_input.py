import dill
import json
import csv
import random

# Tools for debugging
from icecream import ic

with open("data/input_processor.pickle", "rb") as f:
    input_processor = dill.load(f)
with open("data/deploy_data.csv", "r") as f:
    test_data = list(csv.DictReader(f))

test_input_data = test_data[random.randint(0, len(test_data) - 1)]


def test_process_input():
    ic(test_input_data)
    formatted = input_processor.process_input(json.dumps(test_input_data))
    assert formatted.shape[1] == 1856
