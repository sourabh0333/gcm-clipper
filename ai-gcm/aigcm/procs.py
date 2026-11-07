"""Process helpers: is a process alive, and a lock file that keeps a job folder to one run at a time.

Two engine runs on one job folder corrupt it (both write the same checkpoints and clips); this happened
when a second worker took over a stream the first was still running (M2.4 check, 7 Nov)."""

import os
from pathlib import Path


def pid_alive(pid):
    if not pid or pid <= 0:
        return False
    if os.name == "nt":
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x1000, False, int(pid))  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            return False
        code = ctypes.c_ulong()
        ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
        kernel32.CloseHandle(handle)
        return bool(ok) and code.value == 259  # STILL_ACTIVE
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class Busy(RuntimeError):
    pass


class FolderLock:
    """`with FolderLock(folder):` holds folder/run.lock for this process. A lock left by a dead process is
    taken over; one held by a live process raises Busy."""

    def __init__(self, folder):
        self.path = Path(folder) / "run.lock"

    def __enter__(self):
        try:
            holder = int(self.path.read_text().strip() or 0)
        except (FileNotFoundError, ValueError):
            holder = 0
        if holder and holder != os.getpid() and pid_alive(holder):
            raise Busy(f"This job is already being processed (process {holder}).")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(str(os.getpid()))
        return self

    def __exit__(self, *exc):
        try:
            if int(self.path.read_text().strip() or 0) == os.getpid():
                self.path.unlink()
        except (FileNotFoundError, ValueError):
            pass
        return False
