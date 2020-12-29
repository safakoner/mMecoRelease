# DESCRIPTION Check all packages to determine whether they are suitable for release
& $env:MECO_PYTHON_EXECUTABLE_PATH -c "import mMecoRelease.releaseCmd;mMecoRelease.releaseCmd.checkAll()" $args