"""
Helmoltz coils
==============

A script that computes the magnetic field generated by a pair of Helmoltz
coils.
"""

import numpy as np
from scipy import special, linalg

##############################################################################
# Function to caculate the field of a loop


def base_vectors(n):
    """ Returns 3 orthognal base vectors, the first one colinear to n.
    """
    # normalize n
    n = n / np.sqrt(np.square(n).sum(axis=-1))

    # choose two vectors perpendicular to n
    # choice is arbitrary since the coil is symetric about n
    if abs(n[0]) == 1:
        l = np.r_[n[2], 0, -n[0]]
    else:
        l = np.r_[0, n[2], -n[1]]

    l = l / np.sqrt(np.square(l).sum(axis=-1))
    m = np.cross(n, l)
    return n, l, m


def B_field(r, n, r0, R):
    """
    returns the magnetic field from an arbitrary current loop calculated from
    eqns (1) and (2) in Phys Rev A Vol. 35, N 4, pp. 1535-1546; 1987.

    Parameters
    ----------
        n is normal vector to the plane of the loop at the center, current
            is oriented by the right-hand-rule.
        r is a position vector where the Bfield is evaluated:
            [x1 y2 z3 ; x2 y2 z2 ; ... ]
        r is in units of d
        r0 is the location of the center of the loop in units of d: [x y z]
        R is the radius of the loop

    Returns
    -------
        B is a vector for the B field at point r in inverse units of
    (mu I) / (2 pi d)
    for I in amps and d in meters and mu = 4 pi * 10^-7 we get Tesla
    """
    # Translate the coordinates in the coil's frame
    n, l, m = base_vectors(n)

    # transformation matrix coil frame to lab frame
    trans = np.vstack((l, m, n))
    # transformation matrix to lab frame to coil frame
    inv_trans = linalg.inv(trans)

    r = r - r0  # point location from center of coil
    r = np.dot(r, inv_trans)  # transform vector to coil frame

    # calculate field

    # express the coordinates in polar form
    x = r[:, 0]
    y = r[:, 1]
    z = r[:, 2]
    rho = np.sqrt(x**2 + y**2)
    theta = np.arctan(x / y)
    # NaNs are generated where y is zero.
    theta[y == 0] = np.pi / 2

    E = special.ellipe((4 * R * rho) / ((R + rho)**2 + z**2))
    K = special.ellipk((4 * R * rho) / ((R + rho)**2 + z**2))
    dist = ((R - rho)**2 + z**2)
    Bz = 1 / np.sqrt((R + rho)**2 + z**2) * (
        K
        + E * (R**2 - rho**2 - z**2) / dist
    )
    Brho = z / (rho * np.sqrt((R + rho)**2 + z**2)) * (
        -K
        + E * (R**2 + rho**2 + z**2) / dist
    )
    # On the axis of the coil we get a divided by zero here. This returns a
    # NaN, where the field is actually zero :
    Brho[dist == 0] = 0
    Brho[rho == 0] = 0
    Bz[dist == 0] = 0

    B = np.c_[np.cos(theta) * Brho, np.sin(theta) * Brho, Bz]

    # Rotate the field back in the lab's frame
    B = np.dot(B, trans)
    return B


##############################################################################
# The grid of points on which we want to evaluate the field
X, Y, Z = np.mgrid[-0.15:0.15:31j, -0.15:0.15:31j, -0.15:0.15:31j]
# Avoid rounding issues :
f = 1e4  # this gives the precision we are interested in:
X = np.round(X * f) / f
Y = np.round(Y * f) / f
Z = np.round(Z * f) / f

# The (x, y, z) position vector
r = np.c_[np.ravel(X), np.ravel(Y), np.ravel(Z)]


##############################################################################
# The coil positions

# The center of the coil
r0 = np.r_[0, 0, 0.1]
# The normal to the coils
n = np.r_[0, 0, 1]
# The radius
R = 0.1

# Add the mirror image of this coils relatively to the xy plane :
r0 = np.vstack((r0, -r0))
R = np.r_[R, R]
n = np.vstack((n, n))	    # Helmoltz like configuration

##############################################################################
# Calculate field
# First initialize a container matrix for the field vector :
B = np.zeros_like(r)
# Then loop through the different coils and sum the fields :
for this_n, this_r0, this_R in zip(n, r0, R):
    this_n = np.array(this_n)
    this_r0 = np.array(this_r0)
    this_R = np.array(this_R)
    B += B_field(r, this_n, this_r0, this_R)
