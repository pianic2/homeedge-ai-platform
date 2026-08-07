# IHAP-52 — Central Node Hardware Comparison

## Comparison rule

The comparison uses documented capabilities and HomeEdge architectural constraints. It does not use arbitrary numeric scoring. A device is not considered HomeEdge-validated until a reproducible project/community validation run exists.

## Minimum profile used for comparison

- 64-bit ARM64/AArch64 or x86_64 Linux-capable CPU;
- at least 4 logical processors;
- at least 4 GB RAM;
- nominal 64 GB persistent storage;
- Wi-Fi available and supported under Linux;
- Linux-exposed integrated/discrete graphics or compute device;
- manufacturer-supported power path;
- cooling/enclosure adequate for the validated workload;
- no Raspberry Pi GPIO dependency.

Storage endurance, final workload sufficiency and AI acceleration remain `[UNVALIDATED]`.

## Alternative matrix

| Platform | Documented strengths | Main constraint | HomeEdge disposition |
|---|---|---|---|
| Raspberry Pi 4 Model B >=4 GB | Quad-core 64-bit Cortex-A72; 4/8 GB variants; dual-band Wi-Fi; Gigabit Ethernet; USB 3; microSD; VideoCore VI; mature Linux ecosystem | Older generation than Pi 5; microSD endurance and final thermal/resource margin not yet measured | **First reference / validation candidate** |
| Raspberry Pi 5 >=4 GB | Quad-core 64-bit Cortex-A76 at 2.4 GHz; VideoCore VII; faster I/O; Wi-Fi; Gigabit Ethernet; PCIe; microSD; 4 GB+ variants | Higher peak-power/cooling considerations; no HomeEdge run yet | **Recommended newer compatible candidate**; community validation pending |
| Raspberry Pi 3 Model B+ | 64-bit quad-core Cortex-A53; dual-band Wi-Fi; Ethernet; microSD | Officially documented 1 GB RAM is below the 4 GB minimum; USB 2.0 only | **Not compliant / not recommended** |
| Raspberry Pi Zero 2 W | 64-bit quad-core Cortex-A53; Wi-Fi; very low cost/size | 512 MB RAM, limited USB/I/O, no onboard Ethernet | **Rejected for central node** |
| x86_64 mini-PC / thin client | Often 4+ GB RAM, internal SSD/eMMC, Wi-Fi/Ethernet, x86_64 Linux, stronger CPU options | Model-specific variability; some low-cost units omit Wi-Fi or have weak/unsupported graphics | **Compatible candidate when profile is met** |
| Reused laptop/desktop | Often strong CPU/RAM/storage; reuse can avoid immediate acquisition; laptops may have integrated battery | Reproducibility, power, aging and hardware support vary by unit | **Compatible candidate when profile is met** |
| Cloud-only runtime | Elastic remote compute/storage | Removes local central-node boundary and creates WAN dependency | **Rejected as MVP central-node replacement**; future architecture option only |

## Raspberry Pi 4 reference facts

Raspberry Pi official documentation describes the Pi 4 Model B with:

- Broadcom BCM2711 quad-core Cortex-A72 64-bit CPU;
- 4 GB and 8 GB LPDDR4 variants among the supported capacities;
- 2.4/5 GHz 802.11ac Wi-Fi;
- Gigabit Ethernet;
- two USB 3.0 and two USB 2.0 ports;
- microSD storage;
- 5 V USB-C power with a 3 A minimum in the primary specification;
- OpenGL ES/Vulkan graphics backed by VideoCore VI hardware.

Source: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/

The product page recommends a 15 W USB-C power supply for Raspberry Pi 4.

Source: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/

These facts establish hardware capability only. They do not prove HomeEdge workload sufficiency.

## Raspberry Pi 5 candidate facts

Raspberry Pi official documentation describes Pi 5 with:

- Broadcom BCM2712 quad-core 64-bit Cortex-A76 at 2.4 GHz;
- 4 GB and larger RAM variants;
- VideoCore VII graphics;
- dual-band 802.11ac Wi-Fi;
- Gigabit Ethernet;
- microSD SDR104 support;
- USB 3.0;
- PCIe 2.0 x1;
- 5 V / 5 A USB-C power support.

Raspberry Pi states that Pi 5 delivers approximately 2–3x CPU performance over the previous generation. That manufacturer statement is useful for relative positioning but is not HomeEdge benchmark evidence.

Source: https://www.raspberrypi.com/products/raspberry-pi-5/

## Lower-end Raspberry Pi closure

### Raspberry Pi 3 Model B+

The official product brief documents a quad-core 64-bit Cortex-A53 and dual-band Wi-Fi, but only 1 GB RAM. It therefore fails the accepted HomeEdge minimum RAM profile and does not require a more elaborate comparison.

Source: https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-b-plus-product-brief.pdf

### Raspberry Pi Zero 2 W

The official product page documents a 1 GHz quad-core 64-bit Cortex-A53 and Wi-Fi but only 512 MB SDRAM. It is therefore far below the accepted RAM minimum and is rejected for the central-node role.

Source: https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/

## Storage comparison

| Storage | Advantages | Trade-offs | HomeEdge position |
|---|---|---|---|
| 64 GB A2 microSD | Native Pi boot/storage path, low component count, low cost, easy replacement, reproducible | Flash endurance depends on write workload; recovery requires image/backup process | **Reference MVP baseline**; endurance `[UNVALIDATED]` |
| USB SSD | Better performance/headroom for sustained writes in many products; straightforward replacement | Extra cost, cable/device, USB power budget and enclosure complexity | **Optional upgrade**; may become preferred if evidence justifies it |
| eMMC | Integrated and compact on devices that provide it | Not available on Pi 4 Model B; replacement/serviceability varies | **Compatible alternative** |
| Internal SATA/NVMe SSD | Strong option for mini-PC/laptop and some Pi 5 configurations | Platform-specific; may increase acquisition cost | **Compatible alternative** |

No storage medium is declared universally superior. HomeEdge requires the accepted capacity and future evidence appropriate to the workload.

## Networking comparison

Wi-Fi is mandatory because the central node must support the project's wireless local communication model with edge nodes without requiring wired placement. Ethernet remains desirable and is available on the Raspberry Pi 4/5 reference family, but is optional under the minimum contract.

A compliant device must expose a supported Wi-Fi interface under Linux. The final application protocol and topology remain separate software decisions.

## Cooling and enclosure

Heatsinks and/or a fan are optional but recommended for the reference build because low-cost Raspberry Pi kits commonly provide them and they can increase thermal margin. They are not evidence that the workload requires active cooling.

The validation run must record thermal behavior. A later result may strengthen the cooling requirement if sustained throttling or unacceptable temperatures are observed.

The reference demonstrator should use a ventilated case suitable for ordinary development/demo handling. No IP rating, industrial, fire-safety, appliance or production-readiness claim is made.

## AI-readiness boundary

The hardware profile deliberately reserves:

- >=4 GB RAM;
- at least four logical CPU processors;
- a Linux-exposed graphics/compute device;
- optional high-speed external expansion where the platform provides it.

This is a forward-compatibility baseline, not proof of AI acceleration. Raspberry Pi 4 VideoCore VI is documented graphics hardware, but no HomeEdge AI framework/model has been selected or benchmarked against it. CPU-only small-model inference remains the portable fallback direction until future evidence proves a supported GPU/NPU/USB accelerator path.

## Equivalent-device rule

A substitute machine does not require a new architectural decision when all of the following are true:

1. it satisfies every mandatory minimum-profile requirement;
2. it runs a supported 64-bit Linux environment;
3. HomeEdge software/IaC does not need device-specific application behavior;
4. its power and storage are manufacturer-supported for the selected configuration;
5. it does not expand the MVP or introduce a new trust/deployment boundary;
6. any claim of `Community validated` or `Recommended reference` is withheld until equivalent evidence passes review.

A new ADR is required only when replacement would change the accepted hardware contract or architectural boundary rather than merely selecting another compliant implementation.
