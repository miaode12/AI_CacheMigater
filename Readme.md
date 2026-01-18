# AI Cache Migrator (Windows)

One-click migration of HuggingFace / ModelScope / Torch cache
from C: to another disk.

## Features
- Safe move (no deletion)
- Environment-variable based
- Idempotent
- Rollback supported

## Usage

### 1. Edit config
Modify `config.json` target_root.
(注意一定要调整一下)

### 2. Run migration (Admin PowerShell)
(项目下载到Pycharm里面直接运行migrate_cache.ps1文件,
然后再运行验证文件)
或者cd到对应文件目录下
```powershell
# 允许当前用户运行脚本（一次即可）
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# 运行脚本
.\migrate_cache.ps1
