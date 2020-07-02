import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

from MLE import MLE_TDOA
from BLUE import BLUE_TDOA
from CRLB import CRLB


def MSE_MLE(noisy_distances, anchor_location, x_0, target_location):
    """
    Calculates the Mean Squared Error of MLE estimate
    :param noisy_distances: Noisy measurements
    :param anchor_location: Anchor locations
    :param x_0: Initial estimate
    :param target_location: Target location
    :return: MSE over 1000 realizations
    """

    (xdim, ydim, zdim) = noisy_distances.shape
    mse = np.zeros(zdim)

    for i in range(zdim):
        for j in range(ydim):
            x_estimate = MLE_TDOA(noisy_distances[:, j, i], anchor_location, x_0)
            u = x_estimate - target_location
            mse_y = np.linalg.norm(u) ** 2
            mse[i] = mse[i] + mse_y

    mse = mse / ydim

    return mse


def MSE_BLUE(noisy_distances, anchor_location, sigma2, target_location):
    """
    Calculates the Mean Squared Error of BLUE estimate
    :param noisy_distances: Noisy measurements
    :param anchor_location: Anchor locations
    :param sigma2: Variance list
    :param target_location: Target location
    :return: MSE over 1000 realizations
    """

    (xdim, ydim, zdim) = noisy_distances.shape
    mse = np.zeros(zdim)

    for i in range(zdim):
        for j in range(ydim):
            x_estimate = BLUE_TDOA(noisy_distances[:, j, i], anchor_location, sigma2[i])
            u = x_estimate - target_location
            mse_y = np.linalg.norm(u) ** 2
            mse[i] = mse[i] + mse_y

    mse = mse / ydim

    return mse


def main():
    os.makedirs('./results', exist_ok=True)

    TDOA_data = scipy.io.loadmat('./data/TDOA_data.mat')
    anchor_location = TDOA_data['anchor_location']
    anchor_location = anchor_location.astype(int)
    noisy_distances = TDOA_data['noisy_distances']
    target_location = TDOA_data['target_location']
    target_location = target_location.astype(float)
    target_location = [target_location[0][0], target_location[1][0]]
    sigma2 = TDOA_data['sigma2']

    # Problem 1
    x_0 = [0, 0]
    x = MLE_TDOA(noisy_distances[:, 1, 1], anchor_location, x_0)
    map = plt.imread('./data/mapimage.jpeg')
    filename = './results/MLE_map_loc.png'

    plt.figure()
    plt.imshow(map)
    plt.plot(x[0], x[1], '+', color='red', markersize=12)
    plt.savefig(filename, dpi=300)

    # Problem 2
    x = BLUE_TDOA(noisy_distances[:, 1, 1], anchor_location, sigma2[1])
    map = plt.imread('./data/mapimage.jpeg')
    filename = './results/BLUE_map_loc.png'

    plt.figure()
    plt.imshow(map)
    plt.plot(x[0], x[1], '+', color='green', markersize=12)
    plt.savefig(filename, dpi=300)

    # Problem 3
    MSE_MLE_value = MSE_MLE(noisy_distances, anchor_location, x_0, target_location)
    MSE_BLUE_value = MSE_BLUE(noisy_distances, anchor_location, sigma2, target_location)
    CRLB_value = CRLB(target_location,anchor_location,sigma2)
    filename = './results/MSE.png'

    # Plot and save the results
    plt.figure()
    plt.plot(sigma2, MSE_MLE_value, color='red', label='MLE')
    plt.plot(sigma2, MSE_BLUE_value, color='blue', label='BLUE')
    plt.plot(sigma2, CRLB_value, 'g--', label = 'CRLB')
    plt.title('Comparison of CRLB and MSE of MLE and BLUE estimators')
    plt.xlabel('Noise Variance')
    plt.ylabel('Mean Squared Errors (MSE)')
    plt.legend()
    plt.savefig(filename, dpi=300)

    
if __name__ == '__main__':
    main()
