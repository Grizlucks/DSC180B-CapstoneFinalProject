from config import OPENAI_API_KEY
import openai
import pandas as pd
openai.api_key = OPENAI_API_KEY

import urllib.request
import time

def create_images(outpath,occupations,num_occupations):
    print(outpath,occupations,num_occupations)
    sample_occupations = pd.Series(occupations)

    # Generate and Save Images Code
    for occupation in sample_occupations.values:
        occupation_file_name = occupation.replace(" ","_").lower()
        dalle_term = "Face of a " + occupation
        num_images = num_occupations
        # Code only works as generating images at a multiple of 10
        for i in range(num_images//10):
            time.sleep(5)
            response = openai.Image.create(
                prompt=dalle_term,
                n=10,
                size="256x256"
            )
            image_urls = response['data']
            for j,url in enumerate(image_urls):
                image_url = url["url"]
                urllib.request.urlretrieve(image_url, f"{outpath}image_data/{occupation_file_name}_{i}_{j}.png")

# IMAGES GENERATED HERE NEEDS TO BE ANNOTATED PRIOR TO CONTINUING PROCESSING
def dalle_processing(inpath, outpath, occupations, num_occupations):
    create_images(outpath,occupations,num_occupations)
