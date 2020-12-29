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
## @file    mMecoRelease/processes/releasePreDep/genericCheckPackageDevelopmentLocationDep.py @brief [ FILE   ] - Dependency module.
## @package mMecoRelease.processes.releasePreDep.genericCheckPackageDevelopmentLocationDep    @brief [ MODULE ] - Dependency module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORT
# ----------------------------------------------------------------------------------------------------
import os

import mProcess.dependencyAbs

import mMecoSettings.envVariablesLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ DEPENDENCY CLASS ] - Dependency class.
class GenericCheckPackageDevelopmentLocation(mProcess.dependencyAbs.Dependency):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param parent [ QObject               | None | in  ] - Parent.
    #  @param data   [ mProcess.dataLib.Data | None | in  ] - Data.
    #  @param kwargs [ dict                  | None | in  ] - Keyword arguments.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, parent=None, data=None, **kwargs):

        mProcess.dependencyAbs.Dependency.__dict__['__init__'](self, parent, data, **kwargs)

        ## [ str ] - Name of the dependency.
        self._name          = 'Generic    - Check Package Development Location'

        ## [ str ] - Description of the dependency.
        self._description   = 'Check package location, whether its located in development environment.'

        ## [ bool ] - Whether this dependency is currently active.
        self._isActive      = True

        #
        ## [ mMecoPackage.packageLib.Package ] - mMecoPackage.packageLib.Package class instance.
        self._package       = None

    #
    # ------------------------------------------------------------------------------------------------
    # REIMPLEMENTED PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Run the dependency for terminal.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _runForTerminal(self):

        self._package = self._data['package']

        developmentPackagePath = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_PACKAGES_PATH, '')

        if not self._package.path().startswith(developmentPackagePath):
            return self._setFailure('Package is not under relevant development environment path: {}'.format(self._package.path()))

        return self._setSuccess()