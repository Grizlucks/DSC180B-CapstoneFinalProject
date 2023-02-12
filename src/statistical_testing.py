import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def perform_test(lablel_results, occupations):
    stats_df = {}
    for occupation in occupations:
        occupation_in_file = occupation.lower().replace(" ","_")
        subset = lablel_results[lablel_results["Img"].str.contains(occupation_in_file)]
        obs = (subset["Gender"] == "Male").mean()
        sample_stats = (np.random.choice(subset["Gender"].unique(),(subset.shape[0],100000)) == "Male").mean(axis=0)
        p_value = np.mean(sample_stats >= obs)
        stats_df[occupation] = p_value
    
    return pd.Series(stats_df)


def statistical_testing(inpath, outpath, occupations, num_occupations):
    lablel_results = pd.read_csv(inpath+'labeled_results.csv')
    statistical_results = perform_test(lablel_results,occupations)

    statistical_results.to_csv(outpath + "statistical_results.csv")