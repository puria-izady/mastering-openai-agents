from __future__ import annotations

from sandbox_sampler.run_sandbox_demo import main


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
