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
## @file    mMecoRelease/releaseCnt.py @brief [ FILE   ] - Package release module.
## @package mMecoRelease.releaseCnt    @brief [ MODULE ] - Package release module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
from   getpass import getuser

import mCore.platformLib

import mFileSystem.directoryLib

import mProcess.containerAbs
import mProcess.exceptionLib

import mMecoPackage.packageLib

import mMecoSettings.envVariablesLib
import mMecoSettings.settingsLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to release packages.
class Release(mProcess.containerAbs.Container):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param parent      [ QObject               | None      | in  ] - Parent.
    #  @param data        [ mProcess.dataLib.Data | None      | in  ] - Data.
    #  @param packageRoot [ str                   | os.getcwd | in  ] - Root of a package to be released.
    #  @param kwargs      [ dict                  | None      | in  ] - Keyword arguments.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, parent=None, data=None, packageRoot=os.getcwd(), **kwargs):

        ## [ str ] - Display name.
        self._name                     = 'Package Release'

        ## [ str ] - Description.
        self._description              = 'Release a package'

        ## [ str ] - Process list module.
        self._processListModule        = 'mMecoRelease.releaseProList'

        ## [ str ] - Whether this container requires user description to run.
        self._requiresUserDescription  = False

        #

        ## [ str ] - Package root.
        self._packageRoot              = packageRoot

        #

        mProcess.containerAbs.Container.__dict__['__init__'](self, parent, data, **kwargs)

    #
    ## @brief This method is invoked by the constructor.
    #
    #  Overwrite this method to customize _data member.
    #  @warning Do not delete anything in _data member.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _editData(self):

        _package = mMecoPackage.packageLib.Package(self._packageRoot)

        self._data['package'] = _package

    #
    ## @brief Whether this container should be initialized.
    #
    #  Implement this method to prevent child class instance from being initialized
    #  by raising mProcess.exceptionLib.ContainerError exception.
    #  Method must return True explicitly otherwise.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def shouldInitialize(self):

        developerName = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPER_NAME)
        if not developerName:
            raise mProcess.exceptionLib.ContainerError('No development environment has been set.')

        currentUser = getuser()
        if developerName != currentUser:
            raise mProcess.exceptionLib.ContainerError('Current user "{}" can not release a package behalf of user "{}".'.format(currentUser,
                                                                                                                                 developerName))

        if not mMecoSettings.envVariablesLib.MECO_MASTER_PROJECT_NAME in os.environ:
            raise mProcess.exceptionLib.ContainerError('No master project environment has been set.')

        if not mMecoSettings.envVariablesLib.MECO_PROJECT_NAME in os.environ:
            raise mProcess.exceptionLib.ContainerError('No project environment has been set.')

        if not self._packageRoot:
            raise mProcess.exceptionLib.ContainerError('No package root set.')

        if not os.path.isdir(self._packageRoot):
            raise mProcess.exceptionLib.ContainerError('Path doesn\'t exist: {}'.format(self._packageRoot))

        if not mMecoPackage.packageLib.Package.isRootOfAPackage(self._packageRoot):
            raise mProcess.exceptionLib.ContainerError('Path is not a root of a package: {}'.format(self._packageRoot))

        projectName        = os.environ.get(mMecoSettings.envVariablesLib.MECO_PROJECT_NAME       , None)
        masterProjectName  = os.environ.get(mMecoSettings.envVariablesLib.MECO_MASTER_PROJECT_NAME, None)

        packageReleasePath = ''

        if projectName == masterProjectName:
            # Release master project
            if self._data['package'].isExternal():
                packageReleasePath = os.environ.get(mMecoSettings.envVariablesLib.MECO_MASTER_PROJECT_EXTERNAL_PACKAGES_PATH, None)
            else:
                packageReleasePath = os.environ.get(mMecoSettings.envVariablesLib.MECO_MASTER_PROJECT_INTERNAL_PACKAGES_PATH, None)

        else:
            # Release project
            if self._data['package'].isExternal():
                packageReleasePath = os.environ.get(mMecoSettings.envVariablesLib.MECO_PROJECT_EXTERNAL_PACKAGES_PATH, None)
            else:
                packageReleasePath = os.environ.get(mMecoSettings.envVariablesLib.MECO_PROJECT_INTERNAL_PACKAGES_PATH, None)

        if not os.path.isdir(packageReleasePath):
            raise mProcess.exceptionLib.ContainerError('Release path does not exist: {}'.format(packageReleasePath))

        self._data['platform']              = mCore.platformLib.Platform.system()
        self._data['projectName']           = projectName
        self._data['masterProjectName']     = masterProjectName

        self._data['packageReleasePath']    = packageReleasePath
        self._data['newVersionPath']        = mFileSystem.directoryLib.Directory.join(packageReleasePath,
                                                                                      self._data['package'].getPackageReleaseRelativePath()
                                                                                      )

        self._data['releaseFilesWithAbsolutePath'] = self._data['package'].getReleaseFiles(relative=False)
        self._data['releaseFilesWithRelativePath'] = self._data['package'].getReleaseFiles(relative=True)

        return mProcess.containerAbs.Container.__dict__['shouldInitialize'](self)

