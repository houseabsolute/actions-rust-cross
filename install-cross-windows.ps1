cd $Env:RUNNER_TEMP
Invoke-WebRequest -URI 'https://raw.githubusercontent.com/houseabsolute/ubi/master/bootstrap/bootstrap-ubi.ps1' -UseBasicParsing | Invoke-Expression
.\ubi --project cross-rs/cross --in .

