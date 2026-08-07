# IHAP-52 — Central Node Hardware Comparison

## Comparison rule

The comparison uses documented capabilities and HomeEdge architectural constraints. A device is not HomeEdge-validated until a reproducible project/community validation run exists.

## Minimum profile used for comparison

- 64-bit ARM64/AArch64 or x86_64 Linux-capable CPU;
- at least 4 logical processors;
- at least 4 GB RAM;
- nominal **32 GB** persistent storage;
- Wi-Fi available and supported under Linux;
- Linux-exposed integrated/discrete graphics or compute device;
- manufacturer-supported power path;
- adequate cooling/enclosure for the validated workload;
- no Raspberry Pi GPIO dependency.

Storage endurance, final workload sufficiency and AI acceleration remain `[UNVALIDATED]`.

## Alternative matrix

| Platform | Documented strengths | Main constraint | HomeEdge disposition |
|---|---|---|---|
| Raspberry Pi 4 Model B >=4 GB | Quad-core 64-bit Cortex-A72; 4/8 GB variants; dual-band Wi-Fi; Gigabit Ethernet; USB 3; microSD; VideoCore VI | Older than Pi 5; final thermal/resource/storage evidence pending | **First reference / validation candidate** |
| Raspberry Pi 5 >=4 GB | Newer Cortex-A76 platform; stronger CPU/GPU/I/O; Wi-Fi; Gigabit Ethernet; PCIe | No HomeEdge validation run yet | **Recommended newer compatible candidate** |
| Raspberry Pi 3 Model B+ | 64-bit quad-core; Wi-Fi; Ethernet | 1 GB RAM below minimum | **Not compliant** |
| Raspberry Pi Zero 2 W | 64-bit quad-core; Wi-Fi; compact | 512 MB RAM and limited I/O | **Rejected for central node** |
| x86_64 mini-PC / thin client | Often 4+ GB RAM and SSD/eMMC; Linux; Wi-Fi/Ethernet options | Model-specific variability | **Compatible candidate when profile is met** |
| Reused laptop/desktop | Often strong CPU/RAM/storage; reuse path | Reproducibility/power/support vary | **Compatible candidate when profile is met** |
| Cloud-only runtime | Elastic remote resources | Removes local central-node boundary and adds WAN dependency | **Rejected as MVP central-node replacement** |

## Storage comparison

| Storage | Advantages | Trade-offs | HomeEdge position |
|---|---|---|---|
| **32 GB A2 microSD** | Already available, native Pi boot path, low component count, easy replacement | Lower capacity and write-endurance uncertainty | **MVP reference baseline**; retention/endurance `[UNVALIDATED]` |
| 64 GB+ A2 microSD | More capacity/headroom with same form factor | Extra acquisition cost when not already available | Compatible upgrade |
| USB SSD | Better sustained-write/headroom potential | Extra cost, cable, USB power and enclosure complexity | Optional upgrade |
| eMMC / internal SATA/NVMe | Strong platform-specific options | Not available on Pi 4 Model B in the same form | Compatible alternative |

Raspberry Pi documentation states Raspberry Pi OS Lite needs at least 8 GB to get started, so 32 GB is comfortably above the OS installation floor. That does **not** prove final HomeEdge retention or endurance. Official source: https://www.raspberrypi.com/documentation/computers/getting-started.html#recommended-minimum-storage-requirements

## Reference OS comparison

| Distribution | Strengths | Trade-offs | HomeEdge position |
|---|---|---|---|
| **Raspberry Pi OS Lite 64-bit** | Official Pi distro; minimal/headless; Raspberry Pi Imager handles Wi-Fi/SSH setup; strongest first-party Pi integration | Debian-family baseline rather than ultra-minimal distro | **First reference/validation OS** |
| Alpine Linux aarch64 | Very small footprint; Pi 4/5 supported; flexible diskless/system-disk modes | Different persistence/install modes add reproducibility choices; must be validated separately | **Compatible lightweight candidate** |
| Other supported 64-bit Linux | Preserves portability | Per-distro package/network/service differences | Compatible candidate when future IaC and validation pass |

Official installation documentation:

- Raspberry Pi OS / Imager: https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system
- Alpine Linux on Raspberry Pi: https://wiki.alpinelinux.org/wiki/Raspberry_Pi

For the first MVP, Raspberry Pi OS Lite 64-bit is preferred because the central node is headless and the official Raspberry Pi documentation explicitly recommends Lite for headless setup.

## Networking

Wi-Fi is mandatory because the central node must support the project's wireless local communication model with edge nodes. Ethernet remains optional.

## Cooling and enclosure

Heatsinks and/or a fan are optional but recommended. They provide inexpensive thermal margin but are not evidence that the workload requires active cooling. The validation run records thermal behavior and throttling evidence.

## AI-readiness boundary

The hardware profile reserves >=4 GB RAM, at least four logical processors, a Linux-exposed graphics/compute device and optional external expansion. This is a forward-compatibility baseline only; Raspberry Pi 4 VideoCore VI is not yet proven as a HomeEdge AI accelerator.

## Equivalent-device rule

A substitute machine does not require a new architectural decision when:

1. it satisfies every mandatory minimum-profile requirement;
2. it runs a supported 64-bit Linux environment;
3. HomeEdge software/IaC does not need device-specific application behavior;
4. power and storage are supported for the selected device;
5. it does not change the MVP trust/deployment boundary;
6. `Community validated` / `Recommended reference` labels are withheld until evidence passes review.

A different Linux distro may also be used without changing the hardware ADR when the future IaC/runtime contract supports it, but that distro must be validated before being promoted as a HomeEdge reference image.
