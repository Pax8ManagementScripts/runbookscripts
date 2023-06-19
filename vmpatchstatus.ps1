Param ($tenantId, $clientId, $clientSecret, $storageAccountName, $storageAccountKey, $containerName, $resourceGroup)

function Connect-toAzure{
  [CmdletBinding()]

  param (
      [Parameter(Mandatory = $true)]
      [string]
      $TenantId,

      [Parameter(Mandatory = $true)]
      [string]
      $ClientId,

      [Parameter(Mandatory = $true)]
      [string]
      $ClientSecret
  )

  $InformationPreference = "Continue"

  Disable-AzContextAutosave -Scope Process | Out-Null

  $creds = [System.Management.Automation.PSCredential]::new($ClientId, (ConvertTo-SecureString $ClientSecret -AsPlainText -Force))
  Connect-AzAccount -Tenant $TenantId -Credential $creds -ServicePrincipal | Out-Null
  Write-Information "Connected to Azure..."
}


Connect-toAzure -TenantId $tenantId -ClientId $clientId -ClientSecret $clientSecret


$vms = Get-AzVM -ResourceGroupName $resourceGroup


$command = "cat /usr/lib/os-release"


$parameters = @{
    "Outputter" = "Default"
}

$output = @()

foreach ($vm in $vms) {
    $vmName = $vm.Name
    Write-Output "Checking patch assessment for VM: $vmName"

if ($vm.StorageProfile.osDisk.osType -eq "Linux") {
    $osRelease = Invoke-AzVMRunCommand -ResourceGroupName $resourceGroup -VMName $vmName -CommandId "RunShellScript" -ScriptPath $null -Parameter $parameters -ScriptString $command
    if ($osRelease.value[0].message -notmatch 'Centos' -and $osRelease.value[0].message -notmatch 'RedHat') {
        $command = "apt list --installed"
        
        $patchInfo = Invoke-AzVMRunCommand -ResourceGroupName $resourceGroup -VMName $vmName -CommandId "RunShellScript" -ScriptPath $null -Parameter $parameters -ScriptString $command
        $output += [pscustomobject] @{
                "VMName" = $vmName
                "OS" = "Ubuntu"
                "Patches" = $patchInfo.value[0].message
              }
        Write-Output "$vmName is Ubuntu machine and Installed security patches:"
        Write-Output $patchInfo.value[0].message
    }
    elseif ($osRelease.value[0].message -notmatch 'Centos' -and $osRelease.value[0].message -match 'Red Hat Enterprise Linux') {
           $command = "yum list installed"
        
           $patchInfo = Invoke-AzVMRunCommand -ResourceGroupName $resourceGroup -VMName $vmName -CommandId "RunShellScript" -ScriptPath $null -Parameter $parameters -ScriptString $command
           $output += [pscustomobject] @{
                   "VMName" = $vmName
                   "OS" = "RedHat"
                   "Patches" = $patchInfo.value[0].message
               }
           Write-Output "$vmName is RedHat machine and Installed security patches:"
           Write-Output $patchInfo.value[0].message
    }
    else {
        $command = "yum list installed"
        
        $patchInfo = Invoke-AzVMRunCommand -ResourceGroupName $resourceGroup -VMName $vmName -CommandId "RunShellScript" -ScriptPath $null -Parameter $parameters -ScriptString $command
        $output += [pscustomobject] @{
                "VMName" = $vmName
                "OS" = "CentOS"
                "Patches" = $patchInfo.value[0].message
            }
        # Output the patch information
        Write-Output "$vmName is CentOS machine and Installed security patches:"
        Write-Output $patchInfo.value[0].message
     }
}
else {
    # If the VM is running Windows, run the Windows script
        $command = "Get-Hotfix"
        $parameters = @{
            "ComputerName" = $vmName
        }
        $patchInfo = Invoke-AzVMRunCommand -ResourceGroupName $resourceGroup -VMName $vmName -CommandId "RunPowerShellScript" -ScriptPath $null -Parameter $parameters -ScriptString $command
        $output += [pscustomobject] @{
            "VMName" = $vmName
            "OS" = "Windows"
            "Patches" = $patchInfo.value[0].message
        }
        Write-Output "$vmName is Windows machine and Installed security patches:"
        Write-Output $patchInfo.value[0].message
}
}

$BlobName = "$HOME/azure_vm_patching.csv"
$output | Export-Csv -Path $BlobName -NoTypeInformation 

$context = New-AzStorageContext -StorageAccountName $storageAccountName -StorageAccountKey $storageAccountKey

Set-AzStorageBlobContent -Context $context -Container $containerName -File $BlobName -Blob "azure_vm_patching.csv" -Force
