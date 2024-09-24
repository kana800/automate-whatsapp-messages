$pythonScriptPath = Resolve-Path -Path ""
$pythonExecPath = Resolve-Path -Path ""
$currentTime = Get-Date -Format "HH:mm"
if ($currentTime.Equals('22:58'))
{
    $output = & $pythonExecPath $pythonScriptPath "Sleeping"
}
elseif ($currentTime.Equals('23:00')) 
{
    $output = & $pythonExecPath $pythonScriptPath "Working"
}