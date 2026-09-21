# IHAP-55 toolchain inventory — 2026-09-13

Input HEAD at intake: `f5c94a2429f27e88161305896eb5fb85566dd636`. Local worktree changes after intake are recorded separately by Git.

| Tool | Executed command | Result |
|---|---|---|
| Python | `python3 --version` | 3.13.5, exit 0 |
| Git | `git --version` | 2.47.3, exit 0 |
| Docker client/daemon | `docker --version`; `docker info --format '{{.ServerVersion}}'` | 26.1.5, daemon available with elevated local permission |
| KiCad CLI (host) | `kicad-cli --version` | absent from host PATH, exit 127 |
| KiCad Flatpak | `flatpak list --user` | `org.kicad.KiCad` 10.0.6/stable plus matching user libraries present |
| KiCad Flatpak CLI | `flatpak run --command=kicad-cli org.kicad.KiCad --version` | `10.0.6`, exit 0 when launched with required local Flatpak app-directory access; sandboxed workspace invocation failed before launch with `mkdirat(org.kicad.KiCad): Read-only file system` |
| KiCad Eeschema GUI | controlled `flatpak run --command=eeschema org.kicad.KiCad`; `xwininfo -root -tree` | X.Org display `:0` is accessible, but Eeschema process exited after a few seconds without a window or diagnostic output; no GUI capture performed |
| KiCad Docker exact tag | `docker run --rm kicad/kicad:10.0.6 kicad-cli --version` | manifest unknown, exit 125 |
| KiCad Docker moving tag | `docker run --rm kicad/kicad:10.0 kicad-cli --version` | failed registering a layer: no space left on root filesystem, exit 125; no KiCad version verified by Docker |
| ngspice | `/tmp/ihap55-ngspice/usr/bin/ngspice --version` | 44.2, exit 0; Debian `ngspice=44.2+ds-1` extracted under `/tmp`, no system install |
| ESP-IDF | `source /home/optimus/.espressif/v6.0.1/esp-idf/export.sh && idf.py --version` | v6.0.1, exit 0 |
| GitHub CLI | `gh --version`; `gh auth status` | 2.46.0; cached token invalid; public API used read-only for PR status |

The earlier Docker checks recorded above are historical intake evidence. The CI workflow has since been moved to the official KiCad PPA on Ubuntu 24.04 with an exact 10.0.6 version check; this removes the moving Docker-tag concern by design. Its installation step was **skipped** in [run 34757325971](https://github.com/pianic2/homeedge-ai-platform/actions/runs/34757325971) because no schematic/PCB exists, so CI PPA installation has not itself been verified. The user Flatpak installation and CLI version are verified. The downloaded TI model ZIPs are local and ignored by Git; their hashes are in `simulation-summary.md`.

## Current intake rerun — 2026-09-20

`python3 --version` returned 3.13.5; `git --version` returned 2.47.3; `docker --version` returned 26.1.5; and `gh --version` returned 2.46.0. Host `kicad-cli`, host `ngspice`, and host `idf.py` are absent. ESP-IDF v6.0.1 is available from `/home/optimus/.espressif/v6.0.1/esp-idf/` and produced the fresh firmware build recorded in `firmware-build-report.md`.

The user Flatpak KiCad CLI invocation was retried but failed before tool startup with `Unable to allocate instance id`; no ERC/DRC command was therefore executed. `gh pr view 37` could not reach `api.github.com`, and `git fetch origin` could not update the read-only `.git/FETCH_HEAD`. No remote or PR state is inferred from those failures.
