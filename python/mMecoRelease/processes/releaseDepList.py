#
# Copyright 2020 Safak Oner.
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    mMecoRelease/processes/releaseDepList.py @brief [ FILE   ] - Dependency list module.
## @package mMecoRelease.processes.releaseDepList    @brief [ MODULE ] - Dependency list module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORT
# ----------------------------------------------------------------------------------------------------


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
## [ list of str ] - Pre dependency list.
PRE_DEPENDENCY_LIST  = ['mMecoRelease.processes.releasePreDep.genericDisplayPackageInfoDep',

                        'mMecoRelease.processes.releasePreDep.genericCheckEndOfWeekDep',
                        'mMecoRelease.processes.releasePreDep.genericCheckPackageDevelopmentLocationDep',
                        'mMecoRelease.processes.releasePreDep.genericCheckPackageVersionForReleasingDep',

                        ]

## [ list of str ] - Post dependency list.
POST_DEPENDENCY_LIST = ['mMecoRelease.processes.releasePostDep.genericSendNotificationDep'
                        ]

