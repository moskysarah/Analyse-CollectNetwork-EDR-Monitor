# Audit_AD.ps1
function Invoke-ADAudit {
    $WeakAccounts = Get-ADUser -Filter "PasswordNeverExpires -eq 'True' -and Enabled -eq 'True'" | 
        Select-Object Name, SamAccountName
        
    $AuditResult = @{
        "ScanTime" = (Get-Date).ToString()
        "PasswordNeverExpiresCount" = ($WeakAccounts).Count
        "SuspectAccounts" = $WeakAccounts
    }
    
    $AuditResult | ConvertTo-Json | Out-File -FilePath "ad_audit_report.json" -Encoding utf8
}
Invoke-ADAudit