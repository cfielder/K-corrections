# K-corrections
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub last commit](https://img.shields.io/github/last-commit/cfielder/K-corrections?style=for-the-badge)


Repository for functions and sample code to derive K-corrections for Fielder et al. 2022

## Installing

### Directly from Repository

`git clone https://github.com/cfielder/K-corrections`

## Usage

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa]. 
If you use this code or associated data products for your own work, we ask that you give proper credit to Fielder et al. 2022.


This code has been sepcifically built to work around a cleaned sample. For example in Licquia et al. 2015
the sample contains all objects in SDSS-III DR8 and MPA-JHU of which a significant portion was then discarded 
due to various flags. Of these a volume-limited sample is then selected. Fielder et al. 2021 utilises cross matches to 
this sample. Those catalogs are provided in this repository: https://github.com/cfielder/Catalogs


## Description of Scripts

Gaussian Process Regression (GPR) is a machine learning approach to performing a fit. GPR is a statistical technique that 
leverages information from both local information and global trends. In our application, the GPR uses a wide variety of 
galaxies to capture information from global trends between galaxy structural properties and galaxy photometric properties.
This allows us to predict an SED derived from photometric prediction based on the Milky Way's measured parameters.

We also provide some code for determining systematics - specifically Eddington bias. For those interested in obtaining
k-corrections please refer to Fielder et al. 2021. In addition we provide code for calculating derivates as described by
Fielder et al. 2021.

For ease of use of all of these scripts, we will provide an example for a basic photometric prediction. We also provide 
some functions for those interested in constructing SEDs.

### Step 1:
**Understand how mw_gp.py works**
  - This entire function is built around the scikit-learn implementation of a Gaussian process regression algorithm. For more details
    please refer to the documentation before proceeding: 
    https://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.GaussianProcessRegressor.html
  

### Step 2:
**Perform your photometric predictions** 




   

## Authors

* **Catherine Fielder** - *Code constriction* 

With additional assistance from Brett Andrews and Jeff Newman.
