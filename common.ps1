function Write-Header($msg) {
    Write-Host "`n=== $msg ===" -ForegroundColor Cyan
}

function Load-Config($path) {
    if (!(Test-Path $path)) {
        throw "Config not found: $path"
    }
    return Get-Content $path | ConvertFrom-Json
}

function Process-Items($config, $dryRun, $force) {
    $root = $config.target_root
    if (!(Test-Path $root) -and !$dryRun) {
        New-Item -ItemType Directory -Path $root | Out-Null
    }

    foreach ($name in $config.items.PSObject.Properties.Name) {
        Handle-Item $name $config.items.$name $root $dryRun $force
    }
}

function Handle-Item($name, $item, $root, $dryRun, $force) {
    Write-Host "`n[$name]" -ForegroundColor Yellow

    $src = [Environment]::ExpandEnvironmentVariables($item.src)
    $dst = Join-Path $root $item.dst

    Write-Host "SRC: $src"
    Write-Host "DST: $dst"
    Write-Host "TYPE: $($item.type)"

    if ($dryRun) {
        Write-Host "→ Dry-run mode, no changes"
        return
    }

    if ($item.type -eq "env") {
        if (Test-Path $src -and !(Test-Path $dst)) {
            Move-Item $src $dst -Force:$force
        }
        foreach ($envName in $item.env) {
            setx $envName $dst | Out-Null
        }
    }

    elseif ($item.type -eq "symlink") {
        if (Test-Path $src -and !(Test-Path $dst)) {
            Move-Item $src $dst -Force:$force
        }
        cmd /c "mklink /D `"$src`" `"$dst`"" | Out-Null
    }
}
