from __future__ import annotations

import shutil
import tarfile
from pathlib import Path

from agents.sandbox.session.base_sandbox_session import BaseSandboxSession


async def export_workspace(session: BaseSandboxSession, output_dir: Path) -> Path:
    archive = await session.persist_workspace()
    temp_dir = output_dir.with_name(f".{output_dir.name}.tmp")

    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)

    try:
        with tarfile.open(fileobj=archive, mode="r:*") as tar:
            tar.extractall(temp_dir, filter="data")
        if output_dir.exists():
            shutil.rmtree(output_dir)
        temp_dir.replace(output_dir)
    except BaseException:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        raise
    finally:
        archive.close()

    return output_dir
