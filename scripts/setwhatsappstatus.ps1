# add the status and the time here
$statusList = @{
    "10:00" = "Working"
    "23:00" = "Sleeping"
}

$pythonScriptPath = Resolve-Path -Path "G:\repositories\automate-whatsapp-messages\automater\wa_status.py"
$pythonExecPath = Resolve-Path -Path "G:\repositories\automate-whatsapp-messages\.venv\Scripts\python.exe"
$currentTime = Get-Date -Format "HH:mm"

foreach($time in $statusList.Keys)
{
    if ($currentTime -eq $time)
    {
        $pythonOutput = & $pythonExecPath $pythonScriptPath $statusList[$time] 
    }
}