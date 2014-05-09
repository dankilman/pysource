pysource
===

Execute python from bash scripts (sort of).

Example:


Installation
---

When (and if) this package will be not as half-baked as it is now, I will probably push it to PyPI.
```bash
pip install https://github.com/dankilman/pysource/archive/master.tar.gz
```

The following should probably be placed in `.bashrc` or something similiar.
The functions `pysource` and `def` are sourced in this shell script.
```bash
source $(which pysource.sh)
```

Controlling the daemon
---

To start/stop/restart the daemon
```bash
pysource daemon [start, stop, restart] [--force]
```

If the daemon was not stopped in a clean manner, pass `--force` to either `start` or `restart`.

This logic should probably be managed by `systemd` or something similiar, but this is what I have for now.


Usage
---



License
---

