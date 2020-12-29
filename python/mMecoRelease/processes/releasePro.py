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
## @file    mMecoRelease/processes/packageReleasePro.py @brief [ FILE   ] - Process module.
## @package mMecoRelease.processes.packageReleasePro    @brief [ MODULE ] - Process module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import stat

import mFileSystem.directoryLib
import mFileSystem.fileLib

import mProcess.processAbs


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Process class.
class PackageRelease(mProcess.processAbs.Process):
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

        ## [ str ] - Name of the process.
        self._name                   = 'Package Release'

        ## [ str ] - Description about the process.
        self._description            = 'Release a package'

        ## [ str ] - Dependency list module.
        self._dependencyListModule   = 'mMecoRelease.processes.releaseDepList'

        mProcess.processAbs.Process.__dict__['__init__'](self, parent, data, **kwargs)

    #
    ## @brief Run the process for terminal.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _runForTerminal(self):

        self._package = self._data['package']

        releaseFilesWithRelativePath = self._data['releaseFilesWithRelativePath']

        if not releaseFilesWithRelativePath:
            return self._setFailure('No files found in the package: {}'.format(self._package.name()))


        _file = mFileSystem.fileLib.File()


        for rf in releaseFilesWithRelativePath:

            if not _file.setFile(mFileSystem.directoryLib.Directory.join(self._package.path(),
                                                                         rf)):
                return self._setFailure('File doesn\'t exist: {}'.format(rf))

            destinationFile = mFileSystem.directoryLib.Directory.join(self._data['newVersionPath'], rf)

            try:

                _file.copy(destinationFile, True)
                self._setInfo(destinationFile)

                os.chmod(destinationFile, os.stat(destinationFile).st_mode & 0o0777 ^ (stat.S_IWRITE | stat.S_IWGRP | stat.S_IWOTH))

            except Exception as error:
                return self._setFailure(str(error))


        return self._setSuccess()
