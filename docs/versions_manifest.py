import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Tuple, Union


@dataclass
class VersionManifest:
    stable: str
    dev: List[str]
    released: List[str]


def parse_version(version_str: str) -> Union[Tuple[int, int, int]]:
    if not version_str.startswith("v"):
        raise ValueError("version string must start with 'v'")

    parts = [int(x) for x in version_str[1:].split(".", maxsplit=3)]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def format_version(version: Tuple[int, ...]) -> str:
    return ".".join(str(x) for x in version)


def scan_versions(path: Path) -> VersionManifest:
    dev_versions = []
    released_versions = []

    for child in path.iterdir():
        if child.is_dir() and child.name != "stable":
            try:
                version = parse_version(child.name)
                released_versions.append(version)
            except ValueError:
                dev_versions.append(child.name)

    released_versions.sort(reverse=True)

    return VersionManifest(
        stable=format_version(released_versions[0])
        if len(released_versions) > 0
        else "",
        dev=dev_versions,
        released=[format_version(v) for v in released_versions],
    )


def main():
    parser = argparse.ArgumentParser(
        description="Create a versions.json manifest for the documentation's version selector."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=("versions.json",),
        nargs=1,
        help="output file",
    )
    parser.add_argument("directory", type=str, nargs=1, help="directory to process")
    parser.add_argument("--link-stable", action="store_true")
    args = parser.parse_args()

    path = Path(args.directory[0])
    manifest = scan_versions(path)

    with open(args.output[0], "w") as f:
        json.dump(asdict(manifest), f)
        f.write("\n")

    if args.link_stable and manifest.stable:
        target_path = path / f"v{manifest.stable}"
        stable_path = path / "stable"
        if stable_path.exists():
            shutil.rmtree(stable_path)
        stable_path.symlink_to(target_path.relative_to(path), True)


if __name__ == "__main__":
    main()
