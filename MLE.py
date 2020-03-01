import numpy as np


def MLE_TDOA(noisy_distances, anchor_location, x_0):
    ALPHA = 0.5
    NUM_ITER = 100
    DIMENSIONS = 2

    num_anchors = anchor_location.shape[1]

    x = np.zeros([2, NUM_ITER])
    d = np.zeros(num_anchors)
    h = np.zeros(num_anchors-1)
    r = np.zeros(num_anchors-1)
    delH = np.zeros([DIMENSIONS, (num_anchors-1)])

    x[:, 0] = x_0
    C = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    C_inverse = np.linalg.inv(C)

    for iter in range(NUM_ITER - 1):
        for j in range(num_anchors):
            d[j] = np.linalg.norm(x[:, iter] - anchor_location[:, j])

        for j in range(num_anchors - 1):
            h[j] = d[j] - d[j + 1]
            r[j] = noisy_distances[j] - noisy_distances[j + 1]

        for j in range(num_anchors - 1):
            for k in range(DIMENSIONS):
                delH[k, j] = ((x[k, iter] - anchor_location[k, j]) / d[j]) - ((x[k, iter] - anchor_location[k, j + 1]) / d[j + 1])

        x[:, iter + 1] = x[:, iter] + ALPHA * delH @ C_inverse @ (r - h)

    return x[:, -1]


if __name__ == '__main__':
    MLE_TDOA()
