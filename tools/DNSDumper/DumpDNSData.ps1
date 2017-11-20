cd $PSScriptRoot
$default_recorder = $PSScriptRoot + "\DNSLogs\rr"
$time_stamp = Get-Date -format yyyyMMddHHmmss
$recorder = $default_recorder + "-" + $time_stamp
New-Item $recorder -type file;
$lines = Get-DhcpServerv4Scope -ComputerName HAN-DCS-01
foreach ($line in $lines) {
    $scopeId = $line.ScopeId;
    $records = Get-DhcpServerv4Lease $scopeId;
    foreach ($record in $records) {
        $record.HostName + ";" + $record.ClientId + ";" + $record.IPAddress + ";" + $record.LeaseExpiryTime|Add-Content $recorder;
    }
}
Copy-Item $recorder $default_recorder
python updateIP.py
$rr_files =  Get-ChildItem .\DNSLogs\* -include rr-*|Sort-Object Name -Descending|%{$_. Name }
$keep_file =0;
foreach ($file in $rr_files) {
    if ($keep_file -eq 5) {
        #echo "Remove file .\DNSLogs\$file"
        Remove-Item .\DNSLogs\$file
    } else {
        #echo "Don't remove. count = " + $keep_file
        $keep_file += 1
    }
}