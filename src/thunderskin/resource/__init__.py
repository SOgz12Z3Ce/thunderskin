from pathlib import Path
import hashlib

from thunderskin.escape import escape


# This class does not actually process resource content now.
class Resource:
    def __init__(self, path: str, sha256: str):
        self.path = path
        self.sha256 = sha256

    def key(self):
        return escape(self.path)

    def sha256(self):
        return self.sha256

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return NotImplemented
        return self.sha256 == other.sha256


def load_dir(directory: Path, root: Path) -> list[Resource]:
    res = []
    files = [p for p in directory.rglob("*") if p.is_file()]
    for file in files:
        res.append(
            Resource(
                file.relative_to(root).with_suffix("").as_posix(),
                hashlib.sha256(file.read_bytes()).hexdigest(),
            )
        )
    return res
