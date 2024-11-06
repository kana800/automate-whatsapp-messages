$pythonScriptPath = Resolve-Path -Path "G:\repositories\automate-whatsapp-messages\automater\wa_server.py"
$pythonExecPath = Resolve-Path -Path "G:\repositories\automate-whatsapp-messages\.venv\Scripts\python.exe"
$pythonOutput = & $pythonExecPath $pythonScriptPath