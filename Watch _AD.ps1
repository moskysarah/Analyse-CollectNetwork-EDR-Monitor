# Watcher_AD.ps1 - Exécuté via une tâche planifiée sur le DC
$TriggerEvent = Get-WinEvent -LogName "Security" -FilterXPath "*[System[(EventID=4728)]]" -MaxEvents 1

if ($TriggerEvent) {
    $Message = $TriggerEvent.Message
    # Extraction des détails (Qui a ajouté qui ?)
    $Details = @{
        "EventID" = 4728
        "Time"    = $TriggerEvent.TimeCreated.ToString()
        "Details" = $Message
    } | ConvertTo-Json
    
    # Envoi immédiat au SOC (Python)
    Invoke-RestMethod -Uri "http://localhost:5000/siem-alert" -Method Post -Body $Details -ContentType "application/json"
}