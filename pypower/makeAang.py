# Copyright (C) 1996-2011 Power System Engineering Research Center
# Copyright (C) 2010-2011 Richard Lincoln
#
# PYPOWER is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# PYPOWER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PYPOWER. If not, see <http://www.gnu.org/licenses/>.

from numpy import array, ones, zeros, r_, Inf, pi, arange
from numpy import flatnonzero as find
from scipy.sparse import csr_matrix as sparse

from idx_brch import F_BUS, T_BUS, ANGMIN, ANGMAX


def makeAang(baseMVA, branch, nb, ppopt):
    """Construct constraints for branch angle difference limits.

    Constructs the parameters for the following linear constraint limiting
    the voltage angle differences across branches, where Va is the vector
    of bus voltage angles. NB is the number of buses.

        LANG <= AANG * Va <= UANG

    IANG is the vector of indices of branches with angle difference limits.

    @see: U{http://www.pserc.cornell.edu/matpower/}
    """
    ## options
    ignore_ang_lim = ppopt['OPF_IGNORE_ANG_LIM']

    if ignore_ang_lim:
        Aang  = zeros((0, nb))
        lang  = array([])
        uang  = array([])
        iang  = array([])
    else:
        iang = find(((branch[:, ANGMIN] > -360) & (branch[:, ANGMIN] > -360)) |
                    ((branch[:, ANGMAX] < 360) & (branch[:, ANGMAX] < 360)))
        iangl = find(branch[iang, ANGMIN])
        iangh = find(branch[iang, ANGMAX])
        nang = len(iang)

        if nang > 0:
            ii = arange(nang) + arange(nang)
            jj = r_[branch[iang, F_BUS], branch[iang, T_BUS]]
            Aang = sparse((r_[ones(nang), -ones(nang)],
                           (ii, jj)), nang, nb)
            uang = Inf * ones(nang)
            lang = -uang
            lang[iangl] = branch[iang[iangl], ANGMIN] * pi / 180
            uang[iangh] = branch[iang[iangh], ANGMAX] * pi / 180
        else:
            Aang  = zeros((0, nb))
            lang  = array([])
            uang  = array([])

    return Aang, lang, uang, iang
