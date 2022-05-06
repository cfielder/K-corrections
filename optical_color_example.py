import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from astropy.io import fits
from kcorrection_functions_v2 import calc_correction_fit

#Load in catalog
catalogsdr = Path.home() / "Catalogs"
gswlc = pd.read_pickle(catalogsdr/"Kcorrect_gswlc_opt_initial.pkl")

#Clean catalog; remove where values are undefined
gswlc = gswlc[gswlc['observed_r_ab']!=np.inf]
gswlc = gswlc[gswlc['kcorrect_r'].notna()]
i_fit_df = gswlc[gswlc['i']!=0]
#Only fit in the higher redshift to avoid selection effects
i_fit_df = i_fit_df[i_fit_df['salim_z']>0.04]

i_a1_model,i_a1s = calc_correction_fit(
    i_fit_df.observed_i_ab.values-i_fit_df.observed_r_ab.values,
    i_fit_df.gabs.values - i_fit_df.rabs.values,
    i_fit_df.salim_z,
    sample_per_bin = 5350,
    color_name="i-r"
)
#Determine a1 for each galaxy
computed_a1s = i_a1_model.predict(
    (gswlc.gabs.values-gswlc.rabs.values).reshape(-1,1))
#Determine rest-frame color
imr = (gswlc.observed_i_ab - gswlc.observed_r_ab) - \
        (computed_a1s * gswlc.salim_z)
