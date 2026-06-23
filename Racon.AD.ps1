# Recon_AD.ps1 - Extrait les cibles prioritaires de l'AD
function Get-ADTargets {
    # Recherche des administrateurs du domaine via des requêtes LDAP brutes (plus discret que Get-ADUser)
    $searcher = [ADSISearcher]"(objectCategory=user)"
    $searcher.Filter = "(memberOf=CN=Domain Admins,CN=Users,DC=cyber,DC=local)"
    $results = $searcher.FindAll()
    
    $Targets = foreach ($user in $results) {
        [PSCustomObject]@{
            Username = $user.Properties.samaccountname[0]
            Email    = $user.Properties.mail[0]
            BadPwd   = $user.Properties.badpasswordcount[0]
        }
    }
    # Export en JSON pour l'exfiltration
    return $Targets | ConvertTo-Json -Compress
}