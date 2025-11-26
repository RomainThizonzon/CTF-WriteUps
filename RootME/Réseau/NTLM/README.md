# Writeup -- NTLM

## Catégorie

Réseau

## Énoncé

Vous êtes mandaté par l’équipe SOC de l’entreprise Cat Corporation pour retrouver le mot de passe d’un utilisateur lié à une connexion NTLM over SMB suspecte.
Format du flag : RM{userPrincipalName:password}

## Choses à savoir (Même chose que pour Kerberos)

Kerberos est un protocol qui permet de s'authentifier lors d'une connexion à un serveur.
Dans les environnements Windows, il est principalement utilisé lors des connexions aux services d'un domaine Active Directory
Le client, pour s'authentifier, va demander au KDC (Key Distribution Center), qui gère l'envoi des tickets (Pour l'AD, c'est dans le Domain Controller) un ticket signé.
Pour que le KDC donne le ticket signé, il vérifie si le client existe et si son mdp est bon. Pour ça :
Le client chiffre un timestamp (l'heure actuelle) avec une clé dérivée de son mdp (Genre AES256_StringToKey du mdp).
Il envoit au KDC son username, ainsi que son timestamp chiffré.
Le KDC (DC pour l'AD) déchiffre le timestamp à l'aide de la clé dérivée du mdp, qu'il détient.
Si la clé est bonne pour déchiffrer, il délivre au client un ticket signé.
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

## Exploitation

On cherche le mot de passe d'un utilisateur.

<img width="1168" height="103" alt="image" src="https://github.com/user-attachments/assets/b106841e-262b-48e6-82dd-869c241fa941" />

Dans cette capture d'écran, on voit que le client envoie deux requêtes SMB qui ne passent pas. Il manque des informations
Ensuite, le client renvoie une troisième requête SMB, et pas de message d'erreur renvoyé côté serveur.

On cherche donc dans cette requête les informations importantes pour bruteforce le mot de passe.

Dans un premier temps, on cherche le challenge envoyé par le serveur, que le client doit chiffrer :

<img width="591" height="13" alt="image" src="https://github.com/user-attachments/assets/e78deb0e-d601-4a7f-9fa5-4163cfbf06f2" />

<img width="946" height="239" alt="image" src="https://github.com/user-attachments/assets/d521c901-575c-42c5-a51a-dd8f61a0b5f2" />

Dans ce paquet, envoyé par le serveur avec l'erreur pour la précédente tentative de connexion, on retrouve le challenge.

challenge : `1944952f5b845db1`

Ensuite, on cherche les autres informations nécessaires pour retrouver le mot de passe, dans la requête envoyée par le client :

<img width="515" height="49" alt="image" src="https://github.com/user-attachments/assets/3fe01ffe-60f0-4dc0-9441-0baccf9fd88c" />

<img width="493" height="316" alt="image" src="https://github.com/user-attachments/assets/9d56a17d-bcde-4504-bfa5-33efdb2314bb" />

Dans ces captures d'écran, toutes les informations nécessaires sont trouvées.
On retrouve:

- Le username : 
`
john.doe
`

- Le domaine (realm):
`
catcorp.local
`

Ainsi que la NTLM Response, le chiffrement du challenge, qui contient :

- Le NTProofStr (Les 16 premiers octetcs) :
`
5c336c6b69fd2cf7b64eb0bde3102162
`
- Et le blob, qui est toute la suite de la réponse :
`
01010000000000001a9790044b63da0175304c546c6f34320000000002000e0043004100540043004f005200500001000800440043003000310004001a0063006100740063006f00720070002e006c006f00630061006c000300240044004300300031002e0063006100740063006f00720070002e006c006f00630061006c0005001a0063006100740063006f00720070002e006c006f00630061006c00070008001a9790044b63da010900120063006900660073002f0044004300300031000000000000000000
`

Ces informations permettent de créer notre hash, sous format :
```
USERNAME::DOMAIN:SERVER_CHALLENGE:NTPROOFSTR:BLOB
```

On utilise maintenant hashcat pour bruteforce le mot de passe avec la commande :
```
 hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt -O
```
Le "-O" permet d'optimiser la commande, elle se finit plus rapidement, mais ne fonctionne que pour des mdp de moins de 31 caractères, ce qui est suffisant dans notre cas (rockyou.txt)

Ici, on utilise le mode 5600, qui correspond à notre type, on peut trouver quel mode utiliser sur ce site :

https://hashcat.net/wiki/doku.php?id=example_hashes

La commande hashcat nous permet de retrouver le mot de passe, qui va nous servir pour le flag, qui est de la forme :
```
RM{userPrincipalName:password}
```
Le UserPrincipamName (UPN) est utilisé dans l'Active Directory, on le compose de la forme suivante :
```
username@domain
```
On a toutes les informations nécessaires pour reconstruire le flag, le challenge est validé.

