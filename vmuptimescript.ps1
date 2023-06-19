Param ($tenantId, $clientId, $clientSecret, $storageAccountName, $storageAccountKey, $containerName)

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

$startTime = Get-Date (Get-Date).AddDays(-7) -Hour 0 -Minute 0 -Second 0 -Millisecond 0
$endDate = Get-Date -Hour 0 -Minute 0 -Second 0 -Millisecond 0

$vmsUsage = (Get-UsageAggregates -ReportedStartTime $startTime.DateTime -ReportedEndTime $endDate.DateTime -ShowDetails $true).UsageAggregations | Where-Object {$_.Properties.MeterCategory -eq  'Virtual Machines'}  

$output = foreach($usage in $vmsUsage){
  $usage.Properties
}

## CSV
$csvData = @()
foreach($usage in $vmsUsage){
    $csvData += $usage.Properties
}
$BlobName = "$HOME/azure_vm_uptime.csv"
$csvData | Export-Csv -Path $BlobName -NoTypeInformation

# Set the context to the storage account
$context = New-AzStorageContext -StorageAccountName $storageAccountName -StorageAccountKey $storageAccountKey

# Upload the CSV file to the container
Set-AzStorageBlobContent -Context $context -Container $containerName -File $BlobName -Blob "azure_vm_uptime.csv" -Force
