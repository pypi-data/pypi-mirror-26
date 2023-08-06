# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2017 Satellogic SA
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from math import radians, sqrt, cos, sin

from sgp4.earth_gravity import wgs84

from orbit_predictor.predictors.keplerian import KeplerianPredictor
from orbit_predictor.angles import ta_to_M, M_to_ta
from orbit_predictor.keplerian import coe2rv

MU_E = wgs84.mu
R_E_KM = wgs84.radiusearthkm
J2 = wgs84.j2


def pkepler(argp, delta_t_sec, ecc, inc, p, raan, sma, ta):
    """Perturbed Kepler problem (only J2)

    Notes
    -----
    Based on algorithm 64 of Vallado 3rd edition

    """
    # Mean motion
    n = sqrt(MU_E / sma ** 3)

    # Initial mean anomaly
    M_0 = ta_to_M(ta, ecc)

    # Update for perturbations
    delta_raan = (
        - (3 * n * R_E_KM ** 2 * J2) / (2 * p ** 2) *
        cos(inc) * delta_t_sec
    )
    raan = raan + delta_raan

    delta_argp = (
        (3 * n * R_E_KM ** 2 * J2) / (4 * p ** 2) *
        (4 - 5 * sin(inc) ** 2) * delta_t_sec
    )
    argp = argp + delta_argp

    M0_dot = (
        (3 * n * R_E_KM ** 2 * J2) / (4 * p ** 2) *
        (2 - 3 * sin(inc) ** 2) * sqrt(1 - ecc ** 2)
    )
    M_dot = n + M0_dot

    # Propagation
    M = M_0 + M_dot * delta_t_sec

    # New true anomaly
    ta = M_to_ta(M, ecc)

    # Position and velocity vectors
    position_eci, velocity_eci = coe2rv(MU_E, p, ecc, inc, raan, argp, ta)

    return position_eci, velocity_eci


class J2Predictor(KeplerianPredictor):
    """Propagator that uses secular variations due to J2.

    """
    def _propagate_eci(self, when_utc=None):
        """Return position and velocity in the given date using ECI coordinate system.

        """
        # TODO: Remove duplicated code
        # Orbit parameters
        sma = self._sma
        ecc = self._ecc
        p = sma * (1 - ecc ** 2)
        inc = radians(self._inc)
        raan = radians(self._raan)
        argp = radians(self._argp)
        ta = radians(self._ta)

        # Time increment
        delta_t_sec = (when_utc - self._epoch).total_seconds()

        # Propagate
        position_eci, velocity_eci = pkepler(argp, delta_t_sec, ecc, inc, p, raan, sma, ta)

        return tuple(position_eci), tuple(velocity_eci)
