Set objShell = CreateObject("WScript.Shell")
objShell.Run "CMD /C START /B " & objShell.ExpandEnvironmentStrings("%SystemRoot%") & "\System32\WindowsPowerShell\v1.0\powershell.exe -file " & "C:\Users\quyen.le\git\private\python\django\ams_dev\shells\scan.ps1", 0, False
Set objShell = Nothing