$whatsappScript = "G:\repositories\automate-whatsapp-messages\scripts\setwhatsappstatus.ps1"
$whatsappDirectory = "G:\repositories\automate-whatsapp-messages\scripts"

$taskTrigger1 = New-ScheduledTaskTrigger -Daily -At '10:00'
$taskTrigger2 = New-ScheduledTaskTrigger -Daily -At '23:00'

$trigger = @(
    $taskTrigger1,
    $taskTrigger2
)

$taskAction = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File '$whatsappScript'" -WorkingDirectory $whatsappDirectory

Register-ScheduledTask 'whatsapp-update-status' -Action $taskAction -Trigger $trigger
