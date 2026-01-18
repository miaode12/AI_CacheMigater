import os
from pathlib import Path

CHECKS = {
    "HF_HOME": "huggingface",
    "HUGGINGFACE_HUB_CACHE": "huggingface",
    "MODELSCOPE_CACHE": "modelscope",
    "TORCH_HOME": "torch",
}

print("=== AI Cache Verification ===")

ok = True

for env, name in CHECKS.items():
    val = os.environ.get(env)
    if not val:
        print(f"[FAIL] {env} not set")
        ok = False
        continue

    path = Path(val)
    if not path.exists():
        print(f"[FAIL] {env} -> {val} (path missing)")
        ok = False
    else:
        print(f"[OK]   {env} -> {val}")

if ok:
    print("\n✔ All cache paths valid.")
else:
    print("\n✖ Some checks failed.")
