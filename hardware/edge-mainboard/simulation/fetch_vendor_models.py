#!/usr/bin/env python3
"""Fetch exact public TI model packages into the Git-ignored local vendor directory."""

from __future__ import annotations

import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / "vendor-model-manifest.json").read_text())
VENDOR = HERE / "vendor-models"


def checked(data: bytes, expected: str, label: str) -> None:
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise ValueError(f"{label} SHA-256 mismatch: {actual}")


def main() -> None:
    VENDOR.mkdir(exist_ok=True)
    for model in MANIFEST["models"]:
        archive = VENDOR / model["vendor_package"]
        if archive.exists():
            data = archive.read_bytes()
        else:
            with urllib.request.urlopen(model["url"], timeout=60) as response:
                data = response.read()
            checked(data, model["zip_sha256"], model["vendor_package"])
            archive.write_bytes(data)
        checked(data, model["zip_sha256"], model["vendor_package"])
        with zipfile.ZipFile(archive) as package:
            library = package.read(model["library_in_zip"])
        checked(library, model["library_sha256"], model["subcircuit"])
        output = VENDOR / Path(model["library_in_zip"]).name
        output.write_bytes(library)
        print(f"VERIFIED {model['part']}: {archive.name}, {output.name}")


if __name__ == "__main__":
    main()
