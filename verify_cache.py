import os
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

print("=== AI Cache Verification ===")

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config not found: {CONFIG_PATH}")

config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
target_root = Path(config["target_root"]).resolve()

ok = True

def is_symlink(path: Path) -> bool:
    try:
        return path.is_symlink()
    except OSError:
        return False

for name, item in config["items"].items():
    src = Path(os.path.expandvars(item["src"]))
    cache_type = item["type"]

    print(f"\n[{name}]")

    if cache_type == "env":
        envs = item.get("env", [])
        for env in envs:
            val = os.environ.get(env)
            if not val:
                print(f"  [FAIL] env {env} not set")
                ok = False
                continue

            p = Path(val)
            if not p.exists():
                print(f"  [FAIL] {env} -> {p} (path missing)")
                ok = False
                continue

            try:
                resolved = p.resolve()
                if target_root in resolved.parents:
                    print(f"  [OK]   {env} -> {resolved}")
                else:
                    print(f"  [WARN] {env} -> {resolved} (not under {target_root})")
            except OSError:
                print(f"  [WARN] {env} -> {p} (cannot resolve)")

    elif cache_type == "symlink":
        if not src.exists():
            print(f"  [FAIL] path missing: {src}")
            ok = False
            continue

        if not is_symlink(src):
            print(f"  [FAIL] not a symlink: {src}")
            ok = False
            continue

        try:
            target = src.resolve()
            if target.exists():
                print(f"  [OK]   symlink -> {target}")
            else:
                print(f"  [FAIL] symlink target missing: {target}")
                ok = False
        except OSError as e:
            print(f"  [FAIL] cannot resolve symlink: {e}")
            ok = False

    else:
        print(f"  [WARN] unknown type: {cache_type}")

print("\n==============================")

if ok:
    print("✔ All cache checks passed.")
else:
    print("✖ Some cache checks failed.")
