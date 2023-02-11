import numpy as np
import pandas as pd
import scipy.stats as st

import warnings
warnings.filterwarnings("ignore")

def one_prop_sample_size(p0, p1, alpha, power):
    """
    Input:
    - p0: Historical/known proportion to compare to
    - p1: Desired proportion to test against
    - alpha: Desired p-value
    - power: Likelihood of avoiding type II error
    
    Output:
    - return: Sample size
    
    Notes:
    - Created using "Sample Size for One Sample, Dichotomous Outcome" taken from tinyurl.com/jyym9d9f
    """
    z_score_a = st.norm.ppf((1 - alpha)/2)
    z_score_b = st.norm.ppf(power)
    ES = (p1 - p0)/np.sqrt(p1*(1 - p1))
    return ((z_score_a + z_score_b)/ES)**2

def analysis(bls):
    bls = bls[~(bls["Occupations"].str.contains("occupation",case=False).fillna(False))]
    full_bls = bls.dropna(how='all').iloc[:-1]
    # return bls
    full_bls['Count'] = full_bls['Count'].str.replace(',','').astype(int)
    # Looking at occupations that are in the upper half in count in our dataset
    clean_bls = full_bls[full_bls['Count'] > 85]
    # return clean_bls
    clean_bls['Women'] = clean_bls['Women'].replace('–',np.nan).astype(float)
    # return clean_bls
    clean_bls['Black or African American'] = clean_bls['Black or African American'].replace('–',np.nan).astype(float)
    clean_bls['Asian'] = clean_bls['Asian'].replace('–',np.nan).astype(float)
    clean_bls['Hispanic or Latino'] = clean_bls['Hispanic or Latino'].replace('–',np.nan).astype(float)

    lst = []
    for prop in clean_bls['Women']:
        lst += [one_prop_sample_size(prop/100, 0.5, 0.05, 0.99)]

    bias_w = clean_bls.reset_index()[['Occupations', 'Women']]

    w_samples = bias_w.assign(Sample=pd.Series(lst))

    w_samples["Sample"] = w_samples["Sample"].apply(np.ceil)
    
    potential = w_samples[(w_samples["Women"] <= 65) & (w_samples["Women"] >= 45) & (w_samples["Sample"] <= 206)].sort_values(by="Sample",ascending=False)

    return w_samples

def power_analysis(inpath, outpath):
    bls = pd.read_csv(inpath+'blsdata.csv')
    jobs_of_interest = analysis(bls)

    jobs_of_interest.to_csv(outpath + "jobs_of_interest.csv", index=False)