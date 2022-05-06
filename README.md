# K-corrections
[![Python 3.7][python-image]][python-link]
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
[![Sklearn][sklearn-image]][sklearn-link]
![GitHub last commit](https://img.shields.io/github/last-commit/cfielder/K-corrections?style=for-the-badge)
[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]


[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

[python-image]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-link]: https://www.python.org/downloads/release/python-3710/

[sklearn-image]: https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white
[sklearn-link]: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html


Repository for functions and sample code to derive K-corrections for Fielder et al. 2022

## Installing

### Directly from Repository

`git clone https://github.com/cfielder/K-corrections`

## Usage

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa]. 
If you use this code or associated data products for your own work, we ask that you give proper credit to Fielder et al. 2022.


This code is constructed in tandem with the Fielder et al. 2022 publication, which thoroughly steps through the algorithm. 
We will provide a generalised summary here, but strongly recommend reviewing Section 2.3 of the publication before employing 
`kcorrection_function_v2.py`. 

The purpose of this code is to construct a function for the K-correction as a function of a galaxy's rest-frame colour determined in 
well-constrained bands (e.g., <sup>0</sup>(<i>g-r</i>)) and redshift, exploiting the fact that galaxy SEDs can be described as a one parameter 
family at low redshift. This is an epirically-driven approach that mitigates dependance on template SED, limiting to ranges that are
very well constrained. Our code is especially useful for determining K-corrections for bands that are not well-constrained by templates,
such as the WISE (Wright et al. 2011) mid-infrared bands. For example, the standard K-correction software Kcorrect doe not implement
dust emission models, which can result in incorrect K-corrections for bands W2, W3, and W4. With this code WISE band K-corrections
can still be determined. For an example of this in practice see e.g., Fielder et al. 2021.

For those interested in just the original photometry and K-corrected results please refer to the Catalogs folder.

## Description of Script
**The calc_correction_fit() Function**

This function is the only function in within the file `kcorrection_function_v2.py`.
This funtion performs the series of fits necessary to ultimately determine K-corrections. However, a few final steps need to be taken in
order to calculate a final rest-frame color.

As described in the header of the function, this function takes in:
  - The observed-frame color which needs to be K-corrected. Must be an array.
  - The rest-frame color used for the binning. Must be an array. This is the color which we use to quantify the SED shape. We use the simple assumption that K-corrections a polynomial function of redshift. The coefficient of redshift is in itself a function of this rest-frame color. 
  - Redshift of the galaxies. Must be an array.
  - The sample number in each bin. The function placed the galaxies into bins of the rest-frame color for the initial fits. The user should aim to have approximately 20 bins with an approximately equal number of objects per bin. Therefore it is imperative that for the first run of this script the default boolean behaviour is left as it with ```check_bins = True```. 
  - Color name. This is a string label for book-keeping and for labeling the y-axis of the initial fit plots. It is useful to pass this in to keep track of what band is being K-corrected.
The function also has a boolean option for checking the fits which also defaults to True. It is important to check the fits to 
ensure nothing is going wrong with the fits.

The function then proceeds in the following manner.
<ol type="i">
  <li>Determine the rest-frame color bining scheme and indices for placing objects in those bins.</li>
  <li>Loop over each of these rest-frame color bins. For each iteration of the loop the </li>
   <ul>
   <li>data is shuffled into the correct bin and sorted by redshift</li>
   <li>fit weights are determined</li>
   <li>a linear Huber regression is performed for observed-frame color as a function of redshift </li>
   <li>the NMAD of the residual is determined and stored in addition to the fit coefficient
   </ul>
   If the user wishes to change the parameter that determines how sensitive the regression is to outliers (epsilon) or the regularization parameter (alpha) then this must be changed manually in the function.
   <li>The NMAD cuttof is calculated, and the <i>a<sub>1</sub></i>'s</li> that do not pass the cutoff are removed.
   <li>A linear Huber regression is performed for the <i>a<sub>1</sub></i>'s</li> as a function of mean rest-frame color.</li>
</ol>
The function returns the second fit, which we describe as <i>a<sub>1</sub> = b<sub>0</sub> + b<sub>1</sub><sup>0</sup>(X-Y)</i> where 
   <i><sup>0</sup>(X-Y)</i> is the rest-frame color.

The function also returnes the <i>a<sub>1</sub></i>'s that pass the NMAD cutoff.


**Using the <i>a<sub>1</sub></i> Function to Determine K-corrected Color**

We provide two pieces of sample code `optical_color_example.py` and `wise_color_example.py` to reference for determination of a K-corrected color. 
In either script we first load in and clean the catalog such that un-defined quantities (e.g., Nan and infinity) do not effect the fit in any way. We then define a subset of the data frame above redshift of 0.04 such that selection effects do not drive out fits. 


Then we call on `calc_correction_fit()` to perform our fits. In the SDSS optical band example we are determining <sup>0</sup>(<i>i-r</i>) which means we pass in (<i>i-r</i>). In this example we are using bins of <sup>0</sup>(<i>g-r</i>) for the calculation.


Do determine the final <sup>0</sup>(<i>i-r</i>) we then need to take a couple more steps.
   - Determine the <i>a<sub>1</sub></i> for each galaxy. This is done by passing the rest-frame colour for each galaxy into the returned <i>a<sub>1</sub></i> function. In the optical example <i>a<sub>1</sub> = b<sub>0</sub> + b<sub>1</sub><sup>0</sup>(g-r)</i> so we pass in the <sup>0</sup>(<i>g-r</i>) of each galaxy.
   - Deterine the rest-frame color <sup>0</sup>(<i>X-Y</i>). We do this by solving the equation <i><sup>0</sup>(X-Y) = (X-Y)<sub>obs</sub> - a<sub>1</sub>z</i>. In the optical example this calculation is <i><sup>0</sup>(i-r) = (i-r)<sub>obs</sub> - a<sub>1</sub>z</i>.


For a detailed discussion on this algorithm refer to Section 2.3 of Fielder et al. 2022.
   
## Description of Catalogs

In the catalog folder we have provided our photometry and K-corrected results in the four splits described in Section 2.1 of Fielder et al. 2022. They are named with the relevant data. These files are provided as BZ2 compressed pickle files. In each catalog we provide:
  - The GSWLC-M2 coordinates RA and Dec in degrees
  - The GSWLC-M2 redshift (```GSWLC_z```)
  - The relevant observed photometry in mJy (columns labelled as e.g., ```u``` or ```FUV```) and their errors in mJy (e.g., ```e_u``` or ```e_FUV```)
  - The relevant observed photometry in AB magnitudes (e.g., ```observed_u_ab```) and their errors (e.g., ```observed_e_u_ab```)
  - The rest-frame absolute magnitude (K-corrected) photometry in AB magnitudes calculated for GSWLC-M2, as described in <a href="https://ui.adsabs.harvard.edu/abs/2016ApJS..227....2S/abstract">Salim et al. 2016</a> and <a href="https://ui.adsabs.harvard.edu/abs/2018ApJ...859...11S/abstract">Salim et al. 2018</a> and Section 2.2 of Fielder et al. 2022. Labelled as e.g., ```uabs``` or ```fabs```. We also include the associated errors (e.g., ```uabs_err``` or ```fabs_err  ```)
  - The rest-frame absolute magnitude (K-correct) photometry in AB magnitudes calculated in <a href="http://kcorrect.org">Kcorrect v4.3</a> (e.g., ```kcorrect_u```)
  - Our derived rest-frame colors, labelled according to the catalog they were derived from (e.g., ```restframe_rmu_gswlc``` or ```restframe_rmu_kcorrect```)

Note that there is a <i>h = 5log<sub>10</sub>(0.7)</i> offset between Kcorrect absolute magnitudes and GSWLC-M2 magnitudes.

## Authors

* **Catherine Fielder** - *Code development* 

With additional assistance from Brett Andrews and Jeff Newman.
