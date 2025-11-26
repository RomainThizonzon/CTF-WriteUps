# Writeup -- Kerberos

## Catégorie

Réseau

## Énoncé

Vous êtes mandaté par l’équipe SOC de l’entreprise Cat Corporation pour retrouver le mot de passe d’un utilisateur lié à une connexion Kerberos suspecte.
Format du flag : RM{userPrincipalName:password}

## Choses à savoir

Kerberos est un protocol qui permet de s'authentifier lors d'une connexion à un serveur.
Dans les environnements Windows, il est principalement utilisé pour les connexions à l’Active Directory
Il fonctionne en demandant au client voulant se connecter un ticket Kerberos. Ce ticket vérifie l'identité du client
Le sereur vérifie que le client a les droits d'accéder à ce qu'il demande.

Pour que le client ouvre une connexion avec le serveur, il envoie une requête SMB (Simple Message Block)
A l'aide de ce protocol, le client demande l'accès au serveur (ou dossier/fichier pour l'AD)

C'est à ce moment là que le serveur demande le ticket Kerberos du client.

Si le client n'arrive pas à envoyer son ticket, il peut s'authentifier d'une autre manière:
Grâce au protocol NTML (NT LAN Manager), utilisé pour les authentifications sur Windows
Le serveur envoie un "challenge", une chaine hexadécimale en gros, au client.

Le client stocke un Hash NTLM de son mot de passe, dans Windows. 
Le Domain Controller (Ce qui vérifie les connexions et les perms) le connait aussi.
Le client chiffre le challenge à l'aide de son hash, puis envoie le résultat au serveur. Il envoie également un username.
Le serveur demande au DC de vérifier si le username existe, et si le hash qui a chiffré le challenge est le bon (Comme le DC connait les usernames et hashes)
Si c'est bon, le client est connecté
