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
    edm_root = os.path.join(workspace(), "edm-root")
    if not os.path.exists(edm_root):
        try:
            os.makedirs(edm_root)
        except OSError:
            pass
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


def remote_repo_to_edm_egg(repo_url, clone_dir, name, version, build):
    """Deprecated. use remote_repo_to_edm_egg

    Shortcut that can be used for trivially python repositories.
    Goes from the repo to the final uploadable egg, provided that the
    repo egg can be created with a simple 'python setup.py bdist_egg'.

    Returns the path of the EDM egg.
    """
    if not os.path.exists(clone_dir):
        run("git clone --branch "+version+" "+repo_url+" "+clone_dir)

    return local_repo_to_edm_egg(clone_dir, name, version, build)


def local_repo_to_edm_egg(repo_path, name, version, build):
    """Shortcut that can be used for trivially python repositories.
    Like the above, but works with an embedded repo, instead of downloading it.
    Requires the repo egg to be created with a simple
    'python setup.py bdist_egg'.

    Returns the path of the EDM egg.
    """
    with cd(repo_path):
        edmenv_run("python setup.py bdist_egg")

    try:
        os.makedirs("edmdist")
    except OSError:
        pass

    run("edm repack-egg -b {build} dist/{name}-{version}-py2.7.egg".format(
        name=name, version=version, build=build))

    edm_egg_filename = "{name}-{version}-{build}.egg".format(
        name=name, version=version, build=build)

    shutil.move(
        os.path.join(repo_path, "dist", edm_egg_filename),
        os.path.join("edmdist", edm_egg_filename)
        )

    return os.path.join("edmdist", edm_egg_filename)


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
