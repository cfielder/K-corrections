# K-corrections
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Sklearn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![GitHub last commit](https://img.shields.io/github/last-commit/cfielder/K-corrections?style=for-the-badge)
[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg


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
well-constrained bands (e.g., <sup>0</sup><i>(g-r)</i>) and redshift, exploiting the fact that galaxy SEDs can be described as a one parameter 
family at low redshift. This is an epirically-driven approach that mitigates dependance on template SED, limiting to ranges that are
very well constrained. Our code is especially useful for determining K-corrections for bands that are not well-constrained by templates,
such as the WISE (Wright et al. 2011) mid-infrared bands. For example, the standard K-correction software Kcorrect doe not implement
dust emission models, which can result in incorrect K-corrections for bands W2, W3, and W4. With this code WISE band K-corrections
can still be determined. For an example of this in practice see e.g., Fielder et al. 2021.

For those interested in just the original photometry and K-corrected results please refer to the Catalogs folder.

## Description of Script
**The calc_correction_fit() function**






   

## Authors

* **Catherine Fielder** - *Code constriction* 

With additional assistance from Brett Andrews and Jeff Newman.
