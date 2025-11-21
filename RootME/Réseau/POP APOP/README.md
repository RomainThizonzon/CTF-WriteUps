# 📝 Write-up --- POP APOP

## 🔎 Enoncé

Retrouver le mot de passe de l’utilisateur dans la trame réseau.

Un fichier pcapng est à télécharger pour ce chall

------------------------------------------------------------------------

## 📥 Analyse du fichier

Lors de l'ouverture du fichier, on remarque des échanges avec le protocol POP.

pour ce chall, deux lignes nous intéressent :

<img width="705" height="157" alt="wireshark_popapop" src="https://github.com/user-attachments/assets/4320d19b-c177-4269-b040-e2a5ad3356c5" />

Ces deux lignes permettent l'envoi d'un identifiant et d'un mot de passe pour le client. Plusieurs informations sont importantes :

- Le "challenge", envoyé par le serveur et utilisé dans la création du hash md5:
  ```
  <1755.1.5f403625.BcWGgpKzUPRC8vscWn0wuA==@vps-7e2f5a72>
  ```

- L'identifiant, envoyé dans la seconde ligne du screen par le client:
  ```
  bsmith
  ```

- Le "Digest APOP", le hash MD5 qui contient le challenge et le mot de passe
  ```
  4ddd4137b84ff2db7291b568289717f0
  ```

Le digest APOP est construit en faisant le md5 du challenge+password.
Il est donc possible de bruteforce le mot de passe si on a le challenge et le digest APOP

## 📥 Récupération du mot de passe

Le script python utilisé est disponible en fichier dans ce repo, voici le code:

<img width="624" height="500" alt="image" src="https://github.com/user-attachments/assets/84bcbc43-0821-4cdf-b3d4-5ec15ecce6c4" />

Ce code fait simplement le bruteforce du mot de passe, à partir d'une wordlist.
Ici, j'ai utilisé rockyou.txt, et voici le résultat :

<img width="521" height="80" alt="flag" src="https://github.com/user-attachments/assets/b0766e78-9065-4fa7-9d92-0fa8da36ba60" />

On retrouve le mot de passe, qui nous permet de valider le chall 🔥

------------------------------------------------------------------------
