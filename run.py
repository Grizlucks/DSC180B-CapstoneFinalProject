import sys
import json

from src.power_analysis import power_analysis

def main(targets):
    if "test" in targets:
        with open("test-params.json") as fh:
            data_params = json.load(fh)
    else:
        with open("data-params.json") as fh:
            data_params = json.load(fh)
    power_analysis(**data_params)
    # get_features(**data_params)
    # perform_modeling(**data_params)
    # create_visualizations(**data_params)

if __name__ == "__main__":
    targets = sys.argv[1:]
    main(targets)