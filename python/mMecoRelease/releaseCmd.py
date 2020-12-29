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
## @file    mMecoRelease/releaseCmd.py @brief [ FILE   ] - Command module.
## @package mMecoRelease.releaseCmd    @brief [ MODULE ] - Command module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORT
# ----------------------------------------------------------------------------------------------------
import os
import argparse

import mCore.displayLib
import mCore.pythonVersionLib

import mFileSystem.directoryLib

import mMecoPackage.packageLib

import mMecoRelease.releaseCnt

import mProcess.dataLib

import mMecoSettings.envVariablesLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief Check a package.
#
#  @exception N/A
#
#  @return None - None.
def check():

    if not os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_PACKAGES_PATH):
        mCore.displayLib.Display.displayFailure('You must initialize development environment to check a development package for release.')
        mCore.displayLib.Display.displayBlankLine()
        return

    currentPath = os.getcwd()
    _package    = mMecoPackage.packageLib.Package()

    if not _package.setPackage(path=currentPath):
        mCore.displayLib.Display.displayFailure('Path doesn\'t seem to be a root of a package: {}'.format(currentPath))
        mCore.displayLib.Display.displayBlankLine()
        return

    _parser = argparse.ArgumentParser(description='Check a package to determine whether it contains errors before releasing it.')

    _parser.add_argument('-re',
                         '--raise-exceptions',
                         help='Whether to raise exceptions. Default value is False.',
                         default=False,
                         required=False,
                         action='store_true')

    _args = _parser.parse_args()

    _releaseData    = mProcess.dataLib.Data(runLevel=mProcess.dataLib.RunLevel.kPreDependenciesOnly,
                                            raiseExceptions=_args.raise_exceptions)
    _packageRelease = mMecoRelease.releaseCnt.Release(data=_releaseData, packageRoot=currentPath)

    _packageRelease.run()

#
## @brief Check all packages in development package environment.
#
#  @exception N/A
#
#  @return None - None.
def checkAll():

    developmentPackagePath = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_PACKAGES_PATH)
    if not developmentPackagePath:
        mCore.displayLib.Display.displayFailure('You must initialize development environment to check all development packages for release.')
        mCore.displayLib.Display.displayBlankLine()
        return

    if not os.path.isdir(developmentPackagePath):
        mCore.displayLib.Display.displayFailure('Development packages path does not exist: {}'.format(developmentPackagePath))
        mCore.displayLib.Display.displayBlankLine()
        return

    _directory      = mFileSystem.directoryLib.Directory(directory=developmentPackagePath)
    packagePathList = _directory.listDirectories()
    if not packagePathList:
        mCore.displayLib.Display.displayFailure('No package found in development packages path: {}'.format(developmentPackagePath))
        mCore.displayLib.Display.displayBlankLine()
        return

    _parser = argparse.ArgumentParser(description='Check all packages to determine whether they contain errors before releasing them.')

    _parser.add_argument('-re',
                         '--raise-exceptions',
                         help='Whether to raise exceptions. Default value is False.',
                         default=False,
                         required=False,
                         action='store_true')

    _args = _parser.parse_args()

    _package     = mMecoPackage.packageLib.Package()
    packageCount = 0

    for packagePath in packagePathList:

        if not _package.setPackage(packagePath):
            continue

        _releaseData    = mProcess.dataLib.Data(runLevel=mProcess.dataLib.RunLevel.kPreDependenciesOnly,
                                                raiseExceptions=_args.raise_exceptions)
        _packageRelease = mMecoRelease.releaseCnt.Release(data=_releaseData, packageRoot=packagePath)
        _packageRelease.run()

        packageCount += 1

    mCore.displayLib.Display.displaySuccess('{} packages have been checked'.format(packageCount))
    mCore.displayLib.Display.displayBlankLine()

#
## @brief Release a package.
#
#  @exception N/A
#
#  @return None - None.
def release():

    if not os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_PACKAGES_PATH):
        mCore.displayLib.Display.displayFailure('You must initialize development environment to release a development package.')
        return

    mMecoRelease.releaseCnt.Release.runInCommandLine()


#
## @brief Release all packages in development package environment.
#
#  @exception N/A
#
#  @return None - None.
def releaseAll():

    developmentPackagePath = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_PACKAGES_PATH)
    if not developmentPackagePath:
        mCore.displayLib.Display.displayFailure('You must initialize development environment to release all development packages.')
        return

    if not os.path.isdir(developmentPackagePath):
        mCore.displayLib.Display.displayFailure('Development packages path does not exist: {}'.format(developmentPackagePath))
        return

    _directory      = mFileSystem.directoryLib.Directory(directory=developmentPackagePath)
    packagePathList = _directory.listDirectories()
    if not packagePathList:
        mCore.displayLib.Display.displayFailure('No package found in development packages path: {}'.format(developmentPackagePath))
        return

    projectName        = os.environ.get(mMecoSettings.envVariablesLib.MECO_PROJECT_NAME       , None)
    masterProjectName  = os.environ.get(mMecoSettings.envVariablesLib.MECO_MASTER_PROJECT_NAME, None)

    internalPackagesPath = os.environ.get(mMecoSettings.envVariablesLib.MECO_PROJECT_INTERNAL_PACKAGES_PATH, None)
    externalPackagesPath = os.environ.get(mMecoSettings.envVariablesLib.MECO_PROJECT_EXTERNAL_PACKAGES_PATH, None)

    question = 'Do you want to release all packages in your development environment?\n\n'
    question = '{}Development Packages Path      : {}\n\n'.format(question, developmentPackagePath)
    question = '{}Project Internal Packages Path : {}\n\n'.format(question, internalPackagesPath)
    question = '{}Project External Packages Path : {}\n\n'.format(question, externalPackagesPath)
    question = '{}Answer (YES, NO): \n'.format(question)
    mCore.displayLib.Display.displayWarning(question)

    confirmation = None
    if mCore.pythonVersionLib.isPython3():
        confirmation = input()
    else:
        confirmation = raw_input()

    if not confirmation in ['y', 'yes', 'Yes', 'YES']:
        mCore.displayLib.Display.displayFailure('Release all has been aborted.\n', startNewLine=True)
        return

    _package                  = mMecoPackage.packageLib.Package()
    preDependencyResult       = True

    internalPackageCount                = 0
    internalPreDependencyFailureCount   = 0

    externalPackageCount                = 0
    externalPreDependencyFailureCount   = 0

    for packagePath in packagePathList:

        if not _package.setPackage(packagePath):
            continue

        _releaseData    = mProcess.dataLib.Data(runLevel=mProcess.dataLib.RunLevel.kPreDependenciesOnly)
        _packageRelease = mMecoRelease.releaseCnt.Release(data=_releaseData, packageRoot=packagePath)

        if not _packageRelease.run():
            preDependencyResult = False

        if _package.isExternal():
            externalPackageCount                += 1
            externalPreDependencyFailureCount   += 1
        else:
            internalPackageCount                += 1
            internalPreDependencyFailureCount   += 1

    if not preDependencyResult:

        mCore.displayLib.Display.displayBlankLine()
        
        if internalPackageCount:
            mCore.displayLib.Display.displayFailure('{} of {} internal packages have failed in pre-dependency step, release process is aborted.'.format(internalPreDependencyFailureCount,
                                                                                                                                                        internalPackageCount))

        if externalPackageCount:
            mCore.displayLib.Display.displayFailure('{} of {} external packages have failed in pre-dependency step, release process is aborted.'.format(externalPreDependencyFailureCount,
                                                                                                                                                        externalPackageCount))
        
        return


    internalPackageCount = 0
    externalPackageCount = 0

    _packageRelease = None

    for packagePath in packagePathList:

        if not _package.setPackage(packagePath):
            continue

        _releaseData    = mProcess.dataLib.Data(runLevel=mProcess.dataLib.RunLevel.kProcessAndPostDependenciesOnly)
        _packageRelease = mMecoRelease.releaseCnt.Release(data=_releaseData, packageRoot=packagePath)

        _packageRelease.run()

        if _package.isExternal():
            externalPackageCount += 1
        else:
            internalPackageCount += 1
    
    if internalPackageCount:
        mCore.displayLib.Display.displaySuccess('{} internal packages have been released to: {}'.format(internalPackageCount,
                                                                                                        internalPackagesPath))    
    
    if externalPackageCount:
        mCore.displayLib.Display.displaySuccess('{} external packages have been released to: {}'.format(externalPackageCount,
                                                                                                        externalPackagesPath))