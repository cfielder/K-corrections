import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from astropy.io import fits
from kcorrection_functions_v2 import calc_correction_fit

#Load in catalog
catalogsdr = Path.home() / "Catalogs"
gswlc = pd.read_pickle(catalogsdr/"GSWLC_M2_ir.pkl")

#Clean catalog; remove where values are undefined
gswlc = gswlc.replace([np.inf, -np.inf, -99], np.nan).dropna(axis="index",how="any")
#Only fit in the higher redshift to avoid selection effects
w4_fit_df = gswlc[gswlc['salim_z']>0.04]
#Error cut
w4_fit_df = w4_fit_df[w4_fit_df['observed_e_w4_ab']<0.25]

w4_a1_model_kcor,w4_a1s_kcor = calc_correction_fit(
    w4_fit_df.observed_r_ab.values-w4_fit_df.observed_w4_ab.values,
    w4_fit_df.kcorrect_g.values - w4_fit_df.kcorrect_r.values,
    w4_fit_df.salim_z,
    sample_per_bin = 1030,
    color_name = "r-W4"
)
#Determine a1 for each galaxy
computed_a1s = w4_a1_model_kcor.predict(
    (gswlc.kcorrect_g.values-gswlc.kcorrect_r.values).reshape(-1,1))
#Determine rest-frame color
rmW4 = (gswlc.observed_r_ab - gswlc.observed_w4_ab) - \
        (computed_a1s * gswlc.salim_z)