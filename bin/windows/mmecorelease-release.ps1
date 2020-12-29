# DESCRIPTION Release a package in development environment via command line
& $env:MECO_PYTHON_EXECUTABLE_PATH -c "import mMecoRelease.releaseCmd;mMecoRelease.releaseCmd.release()" $args