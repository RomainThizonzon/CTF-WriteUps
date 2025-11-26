# Writeup -- Kerberos

## Catégorie

Réseau

## Énoncé

Vous êtes mandaté par l’équipe SOC de l’entreprise Cat Corporation pour retrouver le mot de passe d’un utilisateur lié à une connexion Kerberos suspecte.
Format du flag : RM{userPrincipalName:password}

## Choses à savoir

Kerberos est un protocol qui permet de s'authentifier lors d'une connexion à un serveur.
Dans les environnements Windows, il est principalement utilisé lors des connexions aux services d'un domaine Active Directory
Le client, pour s'authentifier, va demander au KDC (Key Distribution Center), qui gère l'envoi des tickets (Pour l'AD, c'est dans le Domain Controller) un ticket signé.
Pour que le KDC donne le ticket signé, il vérifie si le client a le droit d'accéder à ce qu'il demande. Pour ça :
Le client chiffre un timestamp (l'heure actuelle) avec son hash de mot de passe.
Il envoit au KDC son username, ainsi que son timestamp chiffré.
Le KDC (DC pour l'AD) déchiffre le timestamp à l'aide du hash du client, qu'il détient.
Si le hash est bon pour déchiffrer, il délivre au client un ticket signé.
Le client envoie ce ticket au serveur, pour s'authentifier.
Le serveur vérifie la signature du ticket. Si tout est bon, il donne l'accès au client.

Pour que le client ouvre une connexion avec le serveur, il envoie une requête SMB (Simple Message Block)
A l'aide de ce protocol, le client demande l'accès au serveur (ou dossier/fichier pour l'AD)


Si la connexion via Kerberos ne fonctionne pas, on peut s'authentifier autrement :
Grâce au protocol NTML (NT LAN Manager), utilisé pour les authentifications sur Windows
Le serveur envoie un "challenge", une chaine hexadécimale en gros, au client.

Le client stocke un Hash NTLM de son mot de passe, dans Windows. 
Le Domain Controller (Ce qui vérifie les connexions et les perms) le connait aussi.
Le client chiffre le challenge à l'aide de son hash, puis envoie le résultat au serveur. Il envoie également un username.
Le serveur demande au DC de vérifier si le username existe, et si le hash qui a chiffré le challenge est le bon (Comme le DC connait les usernames et hashes)
Si c'est bon, le client est connecté
