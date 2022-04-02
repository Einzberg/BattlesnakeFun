import numpy as np
from matplotlib import pyplot as plt

def gkern(l=5, sig=3., scale=10):
    """\
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return scale * kernel / np.max(kernel)

plt.imshow(gkern(15))
plt.show()