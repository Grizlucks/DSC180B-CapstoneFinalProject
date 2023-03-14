import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def perform_test(outpath,lablel_results, occupations):
    stats_df = {}

    OCCUPATIONS_NAMES = pd.Series(occupations)
    OCCUPATIONS = pd.Series(occupations).str.lower().str.replace(" ","_")
    proportions = {}

    for i,occupation in enumerate(OCCUPATIONS):
        occupation_in_file = occupation.lower().replace(" ","_")
        subset = lablel_results[lablel_results["Img"].str.contains(occupation_in_file)]
        obs = (subset["Gender"] == "Male").mean()
        proportions[OCCUPATIONS_NAMES[i]] = obs
        obs = np.abs(.5 - (subset["Gender"] == "Male").mean())
        sample_stats = np.abs(.5 - np.random.choice([True,False],(subset.shape[0],1000000,)).mean(axis=0))
        p_value = np.mean(sample_stats >= obs)
        stats_df[occupation] = p_value
        

        p_value = p_value if p_value > 0 else "< 1e-06"
        hist = sns.histplot(sample_stats,stat = "probability",bins=40)
        ax = hist.axes
        plt.axvline(x=obs, color='red', linewidth=2)
        plt.title(f"Sample Distribution of Absolute Difference from 50% for {OCCUPATIONS_NAMES[i]} (p-value: {p_value})",)
        ax.set(xlabel='Absolute Difference of Proportions', ylabel='Density')
        plt.savefig(f"./{outpath}/plot_data/{occupation}_plot",bbox_inches='tight', dpi=300)
        plt.cla()

    prop_df = pd.Series(proportions).to_frame().reset_index()
    prop_df.columns = ["Occupation", "Proportion of Males"]
    prop_df["Occupation"] = OCCUPATIONS_NAMES
    prop_df.to_csv(f"./{outpath}/plot_data/obs_props.csv",index=False)


    prop_df = prop_df.sort_values(by="Proportion of Males", ascending=False)


    #distance from equal proportion
    prop_df["Proportion of Males"] -= 0.5 


    ax = plt.hlines(y = prop_df["Occupation"],
                xmin = 0,
                xmax = prop_df["Proportion of Males"],
                linewidth = 5,
                color = "#1f77b4")
    plt.title("Proportion of Images Labeled Male Compared to Demographic Parity")
    plt.axvline(x = 0, color = "red")
    plt.xlim(-0.5, 0.5)
    loc, labels = plt.xticks()
    plt.xticks(loc, [round(i + 0.5, 1) for i in loc])
    plt.xlim(-0.5, 0.5)
    plt.savefig(f"./{outpath}/plot_data/proportion_plot", bbox_inches="tight", dpi=300)
    
    return pd.Series(stats_df)


def statistical_testing(inpath, outpath, occupations, num_occupations):
    lablel_results = pd.read_csv(inpath+'labeled_results.csv')
    statistical_results = perform_test(outpath,lablel_results,occupations)

    statistical_results.to_csv(outpath + "statistical_results.csv")