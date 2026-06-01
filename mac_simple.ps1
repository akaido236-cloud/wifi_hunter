param($action = "menu")

$RegistryPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"

function CheckAdmin {
    $isAdmin = [bool]([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    return $isAdmin
}

function ShowBanner {
    Clear-Host
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "    WiFi Hunter - MAC Address Changer       " -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
}

function ListAdapters {
    Write-Host "Active Network Adapters:" -ForegroundColor Yellow
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    
    $adapters = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}
    
    if ($adapters.Count -eq 0) {
        Write-Host "No active adapters found" -ForegroundColor Red
        return $null
    }
    
    $i = 1
    $list = @()
    
    foreach ($adapter in $adapters) {
        Write-Host "[$i] $($adapter.Name)" -ForegroundColor Green
        Write-Host "    MAC: $($adapter.MacAddress)" -ForegroundColor Yellow
        Write-Host "    Type: $($adapter.InterfaceDescription)" -ForegroundColor White
        Write-Host ""
        
        $list += @{Index=$i; Name=$adapter.Name; MAC=$adapter.MacAddress}
        $i++
    }
    
    return $list
}

function ValidateMAC {
    param([string]$mac)
    $mac = $mac -replace '[-:]', ''
    return ($mac -match '^[0-9a-fA-F]{12}$')
}

function FormatMAC {
    param([string]$mac)
    return ($mac -replace '[-:]', '').ToUpper()
}

function SaveBackup {
    param([string]$adapter, [string]$mac)
    $backup = "MAC:$adapter=$mac"
    Add-Content -Path "$PSScriptRoot\mac_backup.txt" -Value $backup
    Write-Host "Backup saved" -ForegroundColor Green
}

function ChangeMAC {
    param([string]$adapterName, [string]$newMAC)
    
    $adapter = Get-NetAdapter -Name $adapterName
    if (-not $adapter) {
        Write-Host "Adapter not found" -ForegroundColor Red
        return
    }
    
    $newMACFormatted = FormatMAC $newMAC
    Write-Host "Searching for device..." -ForegroundColor Yellow
    
    $regItems = Get-ChildItem -Path $RegistryPath -ErrorAction SilentlyContinue
    $deviceId = $null
    
    foreach ($item in $regItems) {
        $driver = Get-ItemProperty -Path $item.PSPath -Name "DriverDesc" -ErrorAction SilentlyContinue
        if ($driver -and $driver.DriverDesc -like "*$($adapter.InterfaceDescription)*") {
            $deviceId = Split-Path -Leaf $item.PSPath
            break
        }
    }
    
    if (-not $deviceId) {
        Write-Host "Device not found in registry" -ForegroundColor Red
        return
    }
    
    Write-Host "Device found: $deviceId" -ForegroundColor Green
    SaveBackup -adapter $adapterName -mac $adapter.MacAddress
    
    $regPath = "$RegistryPath\$deviceId"
    Write-Host "Changing MAC to: $newMACFormatted" -ForegroundColor Yellow
    Set-ItemProperty -Path $regPath -Name "NetworkAddress" -Value $newMACFormatted -Force
    
    Write-Host "Registry updated. Restarting adapter..." -ForegroundColor Yellow
    Disable-NetAdapter -Name $adapterName -Confirm:$false
    Start-Sleep -Seconds 2
    Enable-NetAdapter -Name $adapterName -Confirm:$false
    Start-Sleep -Seconds 2
    
    $newAdapter = Get-NetAdapter -Name $adapterName
    Write-Host "New MAC: $($newAdapter.MacAddress)" -ForegroundColor Green
    Write-Host "Done!" -ForegroundColor Green
}

function RestoreMAC {
    param([string]$adapterName)
    
    $backupFile = "$PSScriptRoot\mac_backup.txt"
    if (-not (Test-Path $backupFile)) {
        Write-Host "No backup found" -ForegroundColor Red
        return
    }
    
    $content = Get-Content $backupFile | Select-Object -Last 1
    $originalMAC = $content.Split("=")[1]
    
    Write-Host "Restoring MAC: $originalMAC" -ForegroundColor Yellow
    ChangeMAC -adapterName $adapterName -newMAC $originalMAC
}

function ShowMenu {
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "1. Show adapters" -ForegroundColor Green
    Write-Host "2. Change MAC" -ForegroundColor Green
    Write-Host "3. Restore MAC" -ForegroundColor Green
    Write-Host "4. Exit" -ForegroundColor Red
    Write-Host ""
}

if (-not (CheckAdmin)) {
    Write-Host "ERROR: Admin privileges required!" -ForegroundColor Red
    Write-Host "Run as Administrator" -ForegroundColor Yellow
    exit
}

ShowBanner
Write-Host "Admin privileges OK" -ForegroundColor Green

while ($true) {
    ShowMenu
    $choice = Read-Host "Select option"
    
    switch ($choice) {
        "1" {
            $adapters = ListAdapters
        }
        "2" {
            $adapters = ListAdapters
            if ($adapters) {
                $num = Read-Host "Adapter number"
                $sel = $adapters | Where-Object {$_.Index -eq [int]$num} | Select-Object -First 1
                if ($sel) {
                    $mac = Read-Host "New MAC"
                    if (ValidateMAC $mac) {
                        $conf = Read-Host "Confirm (y/n)"
                        if ($conf -eq "y") {
                            ChangeMAC -adapterName $sel.Name -newMAC $mac
                        }
                    } else {
                        Write-Host "Invalid MAC format" -ForegroundColor Red
                    }
                }
            }
        }
        "3" {
            $adapters = ListAdapters
            if ($adapters) {
                $num = Read-Host "Adapter number"
                $sel = $adapters | Where-Object {$_.Index -eq [int]$num} | Select-Object -First 1
                if ($sel) {
                    $conf = Read-Host "Restore (y/n)"
                    if ($conf -eq "y") {
                        RestoreMAC -adapterName $sel.Name
                    }
                }
            }
        }
        "4" {
            Write-Host "Goodbye!" -ForegroundColor Green
            exit
        }
        default {
            Write-Host "Invalid option" -ForegroundColor Red
        }
    }
}
