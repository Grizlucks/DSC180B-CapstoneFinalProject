import sys
import json

from src.power_analysis import power_analysis
from src.dalle_processing import dalle_processing
from src.statistical_testing import statistical_testing

def main(targets):
    if "test" in targets:
        with open("test-params.json") as fh:
            data_params = json.load(fh)
    else:
        with open("data-params.json") as fh:
            data_params = json.load(fh)

    power_analysis(**data_params)
    dalle_processing(**data_params)
    # This cell should only run if the images are annotated
    statistical_testing(**data_params)

if __name__ == "__main__":
    targets = sys.argv[1:]
    main(targets)