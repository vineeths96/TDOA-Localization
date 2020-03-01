import numpy as np


def BLUE_TDOA(noisy_distances, anchor_location, sigma2):
    r = np.zeros(6)
    r_dash = np.zeros(6)
    H = np.zeros([6, 5])
    gamma_vec = np.zeros(6)

    C = np.array([[4, 1, 1, 1, 1, 0], [1, 4, 1, 1, 0, 1], [1, 1, 4, 0, 1, 1], [1, 1, 0, 4, 1, 1], [1, 0, 1, 1, 4, 1], [0, 1, 1, 1, 1, 4]])
    C_inverse = np.linalg.inv(C)

    num_anchors = anchor_location.shape[1]

    ind = 0
    for i in range(num_anchors):
        for j in range(i + 1, num_anchors):
            r[ind] = noisy_distances[i] - noisy_distances[j]
            gamma_vec[ind] = np.linalg.norm(anchor_location[:, i]) ** 2 - np.linalg.norm(anchor_location[:, j]) ** 2
            r_dash[ind] = r[ind]**2 - gamma_vec[ind] - 2*sigma2
            ind = ind + 1

    ind = 0
    for anchor_ind in range(num_anchors - 1):
        ls = list(range((anchor_ind), num_anchors-1))
        for loc in ls:
            H[ind, 0] = -2*(anchor_location[0, anchor_ind] - anchor_location[0, (loc+1)])
            H[ind, 1] = -2*(anchor_location[1, anchor_ind] - anchor_location[1, (loc+1)])

            H[ind, (loc+2)] = -2*r[ind]
            ind = ind + 1

    H_transpose = np.transpose(H)
    W = np.linalg.inv(H_transpose @ C_inverse @ H) @ H_transpose @ C_inverse
    x = W @ r_dash
    xy = x[:2]

    return xy


if __name__ == '__main__':
    BLUE_TDOA()