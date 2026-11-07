import os
import subprocess
import sys

import pytest

from aigcm.procs import Busy, FolderLock, pid_alive


def test_pid_alive_tells_live_from_dead():
    assert pid_alive(os.getpid())
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    assert not pid_alive(proc.pid) and not pid_alive(0)


def test_a_job_folder_is_held_by_one_live_process(tmp_path):
    other = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        (tmp_path / "run.lock").write_text(str(other.pid))
        with pytest.raises(Busy):
            with FolderLock(tmp_path):
                pass
    finally:
        other.kill()
        other.wait()
    # The holder is gone: its lock is taken over, and released on the way out.
    with FolderLock(tmp_path):
        assert (tmp_path / "run.lock").read_text() == str(os.getpid())
    assert not (tmp_path / "run.lock").exists()
