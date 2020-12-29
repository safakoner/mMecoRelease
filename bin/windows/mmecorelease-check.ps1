# DESCRIPTION Check a package to determine whether its suitable for release
& $env:MECO_PYTHON_EXECUTABLE_PATH -c "import mMecoRelease.releaseCmd;mMecoRelease.releaseCmd.check()" $args