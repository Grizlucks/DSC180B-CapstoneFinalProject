import sys
import json

from src.power_analysis import power_analysis
from src.dalle_processing import dalle_processing
from src.statistical_testing import statistical_testing

def main(targets):
    if "test" in targets:
        with open("test-params.json") as fh:
            data_params = json.load(fh)
        targets = [i for i in targets if i != "test"]
    else:
        with open("data-params.json") as fh:
            data_params = json.load(fh)

    if len(targets) == 0 or "power" in targets:
        power_analysis(**data_params)
    if len(targets) == 0 or "images" in targets:
        dalle_processing(**data_params)
    # This cell should only run if the images produced from the "images" target
    # are annotated and formatted in a result similar to test/raw/labeled_results.csv
    if len(targets) == 0 or "analysis" in targets:
        statistical_testing(**data_params)

if __name__ == "__main__":
    targets = sys.argv[1:]
    targets = [i.lower() for i in targets]
    
    main(targets)