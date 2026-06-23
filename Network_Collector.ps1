# Network_Collector.ps1
function Get-NetworkConnections {
    # Récupère les connexions établies et exporte en JSON pour Python
    Get-NetTCPConnection -State Established | 
        Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess | 
        ConvertTo-Json | 
        Out-File -FilePath "network_log.json" -Encoding utf8
}

function Block-AttackersIP ($IPAddress) {
    # Fonction de remédiation : Bloque l'IP suspecte dans le Pare-feu Windows
    New-NetFirewallRule -DisplayName "EDR_Block_Attack" -Direction Inbound -RemoteAddress $IPAddress -Action Block
    Write-Host "[!] IP $IPAddress bloquée par le pare-feu." -ForegroundColor Red
}

# Exécuter la collecte
Get-NetworkConnections