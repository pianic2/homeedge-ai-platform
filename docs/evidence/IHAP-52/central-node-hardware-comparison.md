# IHAP-52 — Central Node Hardware Comparison

## Comparison rule

A platform is compared against the HomeEdge vendor-neutral minimum profile. Documented hardware capability is not the same as HomeEdge validation: `Community validated` requires a reproducible project run and review.

## Minimum profile used for comparison

- 64-bit ARM64/AArch64 or x86_64 Linux-capable CPU;
- >=4 logical processors;
- >=4 GB RAM;
- nominal >=32 GB persistent storage;
- Wi-Fi available and supported under Linux;
- manufacturer-supported power path;
- cooling/enclosure adequate for the validated bounded workload;
- no Raspberry Pi GPIO dependency;
- no mandatory GPU/NPU requirement for the current MVP.

Storage endurance/retention, final workload sufficiency and AI acceleration remain `[UNVALIDATED]`.

## Platform matrix

| Platform | Documented strengths | Main constraint | HomeEdge disposition |
|---|---|---|---|
| Raspberry Pi 4 Model B >=4 GB | quad-core 64-bit CPU, 4/8 GB variants, dual-band Wi-Fi, Gigabit Ethernet, USB 3, microSD | older than Pi 5; physical HomeEdge run still pending | **first reference / validation candidate** |
| Raspberry Pi 5 >=4 GB | newer/faster CPU/GPU/I/O, Wi-Fi, Ethernet, PCIe | no HomeEdge validation run yet | compatible newer candidate |
| Raspberry Pi 3 Model B+ | 64-bit quad-core, Wi-Fi, Ethernet | 1 GB RAM below minimum | not compliant |
| Raspberry Pi Zero 2 W | 64-bit quad-core, Wi-Fi, compact | 512 MB RAM below minimum | rejected for central node |
| x86_64 mini-PC / thin client | frequently 4+ GB RAM with SSD/eMMC and Linux | model-specific variability | compatible when profile is met and validated |
| reused laptop/desktop | strong reuse path and often ample resources | reproducibility, power and support vary | compatible when profile is met |
| cloud-only runtime | elastic remote resources | removes local central-node boundary and introduces WAN dependency | rejected as MVP central-node replacement |

## Storage matrix

| Storage | Advantages | Trade-offs | HomeEdge position |
|---|---|---|---|
| **32 GB A2 microSD** | already available, native Pi boot path, low component count | lower headroom and write-endurance uncertainty | **MVP reference baseline**; endurance/retention `[UNVALIDATED]` |
| 64 GB+ A2 microSD | more capacity with same form factor | additional acquisition cost when unnecessary | compatible upgrade |
| USB SSD | better sustained-write/headroom potential | cost, cable, USB power and enclosure complexity | optional upgrade |
| eMMC / SATA / NVMe | strong platform-specific storage options | platform dependent | compatible alternative |

The current Raspberry Pi OS download page is linked as a live installation source rather than freezing an image-size number into the ADR. A 32 GB HomeEdge storage decision must not be justified as final retention/endurance merely because the OS itself fits.

Official image page:

https://www.raspberrypi.com/software/operating-systems/

## Reference OS matrix

| Distribution | Strengths | Trade-offs | HomeEdge position |
|---|---|---|---|
| **Raspberry Pi OS Lite 64-bit** | official Pi distro, headless/minimal path, Imager supports network/SSH setup | Debian-family reference rather than ultra-minimal distro | **first reference/validation OS** |
| Alpine Linux aarch64 | small footprint and flexible installation modes | different persistence/install modes add reproducibility choices | compatible lightweight candidate; separate validation required |
| other supported 64-bit Linux | preserves portability | per-distro package/network/service differences | compatible when future IaC and validation pass |

Official setup sources:

- Raspberry Pi headless/getting started: https://www.raspberrypi.com/documentation/computers/getting-started.html
- Raspberry Pi OS images: https://www.raspberrypi.com/software/operating-systems/
- Alpine Raspberry Pi: https://wiki.alpinelinux.org/wiki/Raspberry_Pi

## Networking

Wi-Fi is mandatory for the current reference profile because the central node must participate in the local wireless HomeEdge topology. Ethernet remains optional.

The validation gate requires an active wireless interface with a non-link-local address; Internet access is not required.

## Cooling and enclosure

Heatsinks and/or a fan are optional. The exact tested configuration is evidence. IHAP-52 does not invent a CPU-temperature threshold; Raspberry Pi power/throttle diagnostics, stress stability and observed temperatures are reviewed together.

## GPU / AI boundary

The current MVP central node does **not** require a GPU/NPU. Graphics/render-device exposure may be recorded for future compatibility, but it is not a hardware PASS gate and does not establish AI acceleration.

## Equivalent-device rule

A substitute machine can satisfy this hardware ADR without a new architecture decision when:

1. every mandatory minimum-profile requirement is met;
2. a supported 64-bit Linux environment is available;
3. HomeEdge application/IaC does not require Raspberry Pi-specific behavior;
4. power and storage are supported for that device;
5. the local-first trust/deployment boundary is unchanged;
6. `Community validated` / `Recommended reference` labels are withheld until equivalent evidence passes review.

A different Linux distro may remain compatible with the hardware ADR, but reference promotion requires its own reproducible validation.
