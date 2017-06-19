import os
import subprocess


def workspace():
    """Returns the workspace as defined by jenkins, or a convenient directory
    if we are not running under jenkins"""
    # This is the jenkins workspace, or if not running on jenkins, a local dir.
    return os.getenv("WORKSPACE", os.path.join(os.getenv("HOME"), "workspace"))


def edmenv_setup():
    """Sets up an edm environment in the workspace.
    Must be called before using edmenv_run"""
    if not os.path.exists(os.path.join(workspace(), "edm-root")):
        subprocess.check_call(["edm", "-r", os.path.join(workspace, "edm-root"),
            "environments", "create", "edmenv"])


def edmenv_run(command_line):
    """Runs the given command (passed as a string) under the edm environment.
    Note: will not work with filenames containing spaces."""

    return subprocess.check_call(["edm", "-r", os.path.join(workspace(), "edm-root"),
        "run", "--environment", "edmenv"]+command_line.split())


def run(command_line):
    """Convenience method. Executes the command line. Equivalent to
    subprocess.check_call, but splits the string.

    Note: will not work with filenames containing spaces."""
    return subprocess.check_call(command_line.split())
