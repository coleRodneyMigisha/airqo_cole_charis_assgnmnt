param([string]$Docx)
$base = [System.IO.Path]::ChangeExtension($Docx, $null).TrimEnd('.')
$w = New-Object -ComObject Word.Application; $w.Visible = $false; $w.DisplayAlerts = 0; $w.AutomationSecurity = 3
try {
  $d = $w.Documents.Open($Docx, $false, $false, $false)
  "opened"
  $d.Repaginate()
  "PAGES: " + $d.ComputeStatistics(2)
  "WORDS: " + $d.ComputeStatistics(0)
  $d.RemovePersonalInformation = $true
  $d.ExportAsFixedFormat("$base.pdf", 17); "pdf saved"
  $d.SaveAs2("$base.doc", 0); "doc saved"
  $d.Close(0)
} catch { "ERR " + $_.Exception.Message } finally { $w.Quit() }
