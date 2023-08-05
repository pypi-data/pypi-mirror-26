##
# Copyright 2014-2017 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/easybuilders/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
CrayCCE toolchain: Cray compilers (CCE) and MPI via Cray compiler drivers + LibSci (PrgEnv-cray) and Cray FFTW

:author: Petar Forai (IMP/IMBA, Austria)
:author: Kenneth Hoste (Ghent University)
"""
from easybuild.toolchains.compiler.craype import CrayPECray
from easybuild.toolchains.linalg.libsci import LibSci
from easybuild.toolchains.mpi.craympich import CrayMPICH
from easybuild.tools.toolchain import DUMMY_TOOLCHAIN_NAME


class CrayCCE(CrayPECray, CrayMPICH, LibSci):
    """Compiler toolchain for Cray Programming Environment for Cray Compiling Environment (CCE) (PrgEnv-cray)."""
    NAME = 'CrayCCE'
    SUBTOOLCHAIN = DUMMY_TOOLCHAIN_NAME
