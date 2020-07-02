import numpy as np


def CRLB(x, anchor_location, sigma2):
    """
    Calculates the CRLB bound
    :param x: Location
    :param anchor_location: Anchor locations
    :param sigma2: Variance
    :return: CRLB
    """

    CRLB_value = np.zeros(len(sigma2))
    DIMENSIONS = 2
    num_anchors = anchor_location.shape[1]

    for ind in range(len(sigma2)):
        d = np.zeros(num_anchors)
        h = np.zeros(num_anchors - 1)
        I = np.zeros([DIMENSIONS, DIMENSIONS])
        delH = np.zeros([DIMENSIONS, (num_anchors - 1)])

        C = sigma2[ind] * np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
        C_inverse = np.linalg.inv(C)

        for j in range(num_anchors):
            d[j] = np.linalg.norm(x - anchor_location[:, j])

        for j in range(num_anchors - 1):
            h[j] = d[j] - d[j + 1]

        for j in range(num_anchors - 1):
            for k in range(DIMENSIONS):
                delH[k, j] = ((x[k] - anchor_location[k, j]) / d[j]) - ((x[k] - anchor_location[k, j + 1]) / d[j + 1])

        for i in range(num_anchors - 1):
            for j in range(num_anchors - 1):
                I[0, 0] = I[0, 0] + C_inverse[i, j] * (delH[0, i] * delH[0, j] + delH[0, j] * delH[0, i])
                I[0, 1] = I[0, 1] + C_inverse[i, j] * (delH[1, i] * delH[0, j] + delH[1, j] * delH[0, i])
                I[1, 1] = I[1, 1] + C_inverse[i, j] * (delH[1, i] * delH[1, j] + delH[1, j] * delH[1, i])
                I[1, 0] = I[0, 1]

        I_inverse = np.linalg.inv(I / 2)

        CRLB_value[ind] = I_inverse[0, 0] + I_inverse[1, 1]

    return CRLB_value
