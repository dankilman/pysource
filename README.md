pysource
===

Execute python from bash scripts (sort of).

Example:
TODO


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
TODO


License
---
Copyright 2014 Dan Kilman

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
