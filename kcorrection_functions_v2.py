import numpy as np
import pandas as pd
import scipy.interpolate
from sklearn import linear_model
from scipy import stats
import matplotlib.pyplot as plt

def calc_correction_fit(
        observed_color,
        restframe_color,
        redshift,
        sample_per_bin = 5000,
        color_name = "",
        check_bins = True,
        check_fits = True

):
    """Assuming a rest-frame colour 0(X-Y) = (X-Y) - a1*z this function returns a1 where a1 is
     a function of another rest-frame color. This is done by first splitting the data into bins
     of that rest-frame colour and solving a fit as a function of redshift in each of those bins.
     We take the fit coefficients, called a1's, and then fit for them as a function of the mean
     rest-frame colour of each of the bins.

     Args:
        observed_color (array): An array that contains the observed colour which will be K-
            corrected. Must be 1-D.
        restframe_color (array): An array that contains the rest frame colour which will be
            used to determine K-corrections from. Must be 1-D. We recommend a very well-behaved
            colour such as the SDSS (g-r).
        redshift (array): An array that contains the redshift of each galaxy. Must be 1-D.
        sample_per_bin (int): Default of 5000. The approximate number of objects per bin.
            The function will do its best to put that many objects in each rest-frame color bin.
            Use the check_bins option to make sure the bins are equal in size and adjust this
            parameter accordingly.
        color_name (string): Default is blank. The y-axis label for the initial fits. Also serves as
            a means to stay organized and keep track of the function call if desired.
        check_bins (bool): Default True. Returns print statements of the number of objects in the given
            bin. Check these to ensure an approximate equal number of objects are in each bin, as sometimes
            the last bin can become sparse. Aim to have approximately 20 bins.
        check_fits (bool): Default True. This will return two different plots. First one of the initial
            fits in 3 of the rest-frame color bands. Then the fit for a1 as a function of mean color.
            We recommend checking these fits to ensure the behaviour is as expected.

    Returns:
        A fitted HuberRegressor estimator from the scikit-learn implementation of the Huber regression.
        Please see the documentation for additional details:
        https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html

        An array of the a1s from the initial fit that pass the NMAD cut-off. These are the a1's used to
        define fit the HuberRegressor returned.

     """
    df = pd.DataFrame({'observed_color': observed_color,
                       'restframe_color': restframe_color,
                       'redshift': redshift
                        })
    # define narrow bins of equal no of points per bin in rest-frame color
    color = np.sort(np.array(df.restframe_color))
    ksort = np.argsort(color)
    npoints = sample_per_bin
    color_bins = color[ksort[0::npoints]]
    color_bins = np.append(color_bins, color[ksort[-1]])
    # Now bin the galaxies
    wh_color_bins = np.digitize(df.restframe_color, color_bins)
    #Reminder to check that there is approximately an equal number per bin!
    #The last bin is not useable

    #Define empty arrays to place calculations into
    a1s = np.zeros((len(color_bins)-1))
    nmads = np.zeros((len(color_bins)-1))
    mean_color = np.zeros((len(color_bins)-1))

    general_model = linear_model.HuberRegressor(epsilon=1.01)

    #Some nice organizational print statements
    if check_fits:
        fig = plt.figure()
        if color_name == "":
            print("You didn't give me an observed color name. Your y-axis on the initial fit plot will be blank.")

    if color_name != "":
        print("Solving for observed ({}) color.".format(color_name))

    #Iterate over the bins and do the initial fits
    for i in range(1, len(color_bins)):
        #Grab the galaxy subsample sorted by redshift
        subsample = df.loc[wh_color_bins == i, :]
        subsample = subsample.sort_values(by="redshift")

        #check that there's an equal number per bin
        if check_bins:
            print("{} objects in bin {}".format(len(subsample.redshift),i))

        mean_color[i-1] = (np.mean(subsample.restframe_color.values))
        y = subsample.observed_color.values

        #Determine weights
        subsample_nmad = stats.median_absolute_deviation(y)
        redshift_bin_no = 40
        redshift_bin_edges = np.linspace(subsample.redshift.values.min(),subsample.redshift.values.max(),redshift_bin_no)
        redshift_bin_centers = [redshift_bin_edges[n] + ((redshift_bin_edges[n+1]-redshift_bin_edges[n])/2) for n in range(redshift_bin_no-1)]
        redshift_bin_edges = redshift_bin_edges[1:-1] #cleanup for numpy digitize
        wh_redshift_bin = np.digitize(subsample.redshift.values, redshift_bin_edges)
        n_in_bin = np.bincount(wh_redshift_bin)
        n_z = scipy.interpolate.interp1d(redshift_bin_centers,n_in_bin,fill_value='extrapolate')
        gal_nz = n_z(subsample.redshift.values)
        weight = (1/(subsample_nmad**2)) * (np.mean(n_in_bin)/gal_nz)
        subsample["weight"] = weight

        #Do the initial fits
        X = subsample.redshift.values.reshape(-1,1)
        general_model.fit(X, y, sample_weight=subsample.weight.values)

        #Look at the initial fits, plotting 3 of the bins
        if i == 1 or i == 10 or i == 20:
            if check_fits:
                plt.scatter(subsample.redshift.values, y, s=1,
                            label=r"$^0(g-r) \sim$ {}".format(np.round(mean_color[i - 1], 2)),
                            alpha=0.6)
                plt.plot(subsample.redshift.values, general_model.predict(X),
                         color="black", linestyle='--')

        #calculate the nmad of the residual
        pred_y = general_model.predict(X)
        resid = y - pred_y
        mad = stats.median_absolute_deviation(resid)
        nmads[i-1] = (mad)
        a1s[i-1] = (general_model.coef_[0])

    #Finish the plot
    if check_fits:
        plt.xlabel("Redshift")
        plt.ylabel("({})".format(color_name))
        for lh in plt.legend().legendHandles:
            lh.set_alpha(1)
            lh._sizes = [20]
        plt.tight_layout()
        plt.show()

    # exclude from fitting objects where nmad > 2.5 times the minimim
    min_nmad = np.min(nmads)
    wh_good = np.where(nmads < 2.5 * min_nmad)
    selected_a1s = a1s[wh_good]
    mean_color = mean_color[wh_good]
    mean_color = np.array(mean_color).flatten().reshape(-1,1)
    print("The minimum NMAD is {}".format(min_nmad))
    print("{0} a1's were excluded from the secondary fit by the 2.5*NMAD cutoff of {1}".format(
        len(a1s)-len(selected_a1s),np.round(2.5 * min_nmad,3))
    )

    # Fit the fit coefficients linearly
    model_a1 = linear_model.HuberRegressor(epsilon=1.01)
    model_a1.fit(mean_color, selected_a1s)

    if check_fits:
        fig = plt.figure()
        plt.plot(mean_color, np.array(model_a1.predict(mean_color)), color="black", linestyle="--")
        plt.scatter(mean_color, selected_a1s)
        plt.xlabel(r"Mean $^{0}(g-r)$")
        plt.ylabel(r"$a_{1}$")
        plt.tight_layout()
        plt.show()

    return model_a1,selected_a1s

