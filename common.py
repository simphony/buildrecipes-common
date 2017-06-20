import contextlib
import os
import subprocess
import shutil
import tempfile

_workspace = []

def workspace():
    """Returns the workspace as defined by jenkins, or a convenient directory
    if we are not running under jenkins"""
    # This is the jenkins workspace, or if not running on jenkins, a local dir.
    ws = os.getenv("WORKSPACE")
    if ws is None:
        if len(_workspace) == 0:
            _workspace.append(tempfile.mkdtemp(prefix="workspace-"))
        ws = _workspace[0]
    return ws


def edmenv_setup():
    """Sets up an edm environment in the workspace.
    Must be called before using edmenv_run"""
    if not os.path.exists(os.path.join(workspace(), "edm-root")):
        subprocess.check_call(["edm", "-r", os.path.join(workspace(), "edm-root"),
            "environments", "create", "edmenv"])
        edmenv_run("pip install hatcher")


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


def upload_egg(filename):
    """Uploads an egg file using hatcher"""
    edmenv_run("hatcher eggs upload enthought simphony-dev rh5-x86_64 "+filename)


@contextlib.contextmanager
def cd(path):
    """A context manager which changes the working directory to the given
       path, and then changes it back to its previous value on exit.
    """
    cur = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cur)


def clean(entities):
    """Removes the specified entities. If dir, will remove the dir
    recursively. If file, will remove the files.
    entities must be a list.
    """

    for entity in entities:
        print("Removing {}".format(entity))
        try:
            if os.path.isdir(entity):
                shutil.rmtree(entity)
            elif os.path.isfile(entity):
                os.unlink(entity)
        except Exception as e:
            print("Could not delete {}. {}".format(entity, e))
