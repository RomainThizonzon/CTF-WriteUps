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

## Explotation

On cherche le mot de passe d'un utilisateur.

<img width="835" height="166" alt="image" src="https://github.com/user-attachments/assets/9eea905f-a477-4c6b-b55b-0a7c8b171864" />

Dans cette capture d'écran, on voit que le client envoie une requête AS REQ, refusée par le serveur (ERROR).
Ceci est expliqué par le fait que le premier AS REQ n'a pas de pré-authentification (pas de cipher)
Ensuite, le client renvoie un deuxième AS REQ, avec un cipher.

<img width="932" height="302" alt="image" src="https://github.com/user-attachments/assets/1995434b-faf7-466b-a19f-52ae8b07bcdc" />

C'est exactement ce qui nous intéresse ! C'est le seul moment ou le client prouve qu'il connaît le mot de passe, c'est ce qu'on veut récupérer.

Pour retrouver le mot de passe, on a besoin de plusieurs informations :

- Le username (cname): 
`
william.dupond
`

- Le domaine (realm):
`
CATCORP.LOCAL
`

- La méthode de chiffrement (etype):
`
AES256-CTS-HMAC-SHA1-96 (Code 18)
`
- Et le Cipher :
`
fc8bbe22b2c967b222ed73dd7616ea71b2ae0c1b0c3688bfff7fecffdebd4054471350cb6e36d3b55ba3420be6c0210b2d978d3f51d1eb4f
`

Ces informations permettent de créer notre hash, sous format :
```
$krb5pa$ETYPE$USERNAME$REALM$CIPHER
```
Pour le eTYPE, il faut utiliser le code, pas le nom. Ici, 18.
On utilise maintenant hashcat pour bruteforce le mot de passe avec la commande :
```
hashcat -m 19900 hash.txt /usr/share/wordlists/rockyou.txt
```

Ici, on utilise le mode 19900, qui correspond à notre eTYPE, on peut trouver quel mode utiliser sur ce site :

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
