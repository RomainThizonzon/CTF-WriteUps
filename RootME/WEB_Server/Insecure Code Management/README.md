# Writeup -- SQL Insecure Code Management

## Catégorie

Web - Server

## Énoncé

Retrouvez le mot de passe de l’administrateur.

## Choses à savoir 

Dans certains cas, l'admin du site peut faire une erreur. Si le site est d'abord développé en local, sur un repo github, l'admin peut lors de la mise en ligne du site, prendre tous les dossiers/fichiers de son repo (y compris le .git). C'est une erreur, car si no a accès au .git, on peut reconstruire son repo, et donc avoir accès à ses anciens commits, fichiers supprimés etc.

## Exploitation

On cherche le mot de passe de l'admin.

On vérifie si l'admin a laissé par erreur son .git sur le site :
```
http://challenge01.root-me.org/web-serveur/ch61/.git/
```
<img width="978" height="415" alt="image" src="https://github.com/user-attachments/assets/3ac1898a-5a76-40b0-90f4-50762bd699af" />

On voit bien que le .git est disponible sur le site. On peut donc récupérer le repo entier en local sur notre machine :
```
wget -r -np -R "index.html*" http://challenge01.root-me.org/web-serveur/ch61/.git/
```

J'explique les paramètres :

`-r` : Récursive, donc ca télécharge également tous les sous dossiers etc

`-np` : noparent,  ca remonte pas dans les dossiers parents, ca reste strictement dans .git et ses sous dossiers

`-R "index.html*"` : Ca rejette tous les fichiers de la forme index.html, parce que ca seraient des fichiers inutiles que le serveur peut créer pour chaque dossier.

Après avoir récupéré le repo en local, on va extraire tous les fichiers du repo, ils ne sont pas visibles pour le moment.

Je me déplace dans le tout dernier dossier, là ou les sources devraient être :
```
cd challenge01.rootme.org/web-serveur/ch61/
```
Une fois dans ce dossier, je peux extraire tous les fichiers sources :
```
git checkout .
```
Après l'exécution de ces commandes, on retrouve :

<img width="516" height="198" alt="image" src="https://github.com/user-attachments/assets/4c9e12eb-4f31-4fe8-8b76-ab3ecfabc393" />

Les fichiers sources du site sont disponibles, en ouvrant le fichier config.php, on retrouve l'username `admin` and son mot de passe hashé : `0c25a741349bfdcc1e579c8cd4a931fca66bdb49b9f042c4d92ae1bfa3176d8c`

On ne veut pas le hash de son mot de passe, mais son mot de passe en clair. On veut donc rechercher dans les anciens commits pour savoir si le mot de passe est apparu en clair à un moment :
```
git grep -I "pass" $(git rev-list --all)
```
La commande est complexe, j'explique donc les différents paramètres :

`-I "pass"` : On recherche le string "pass" dans tous les fichiers

`$(git rev-list --all)` : c'est les fichiers dans lequel je cherche "pass", `git rev-list --all` correspond à tous les commits de toutes les branches, même les fichiers supprimés etc.

Cette commande permet de retrouver le mot de passe en clair de l'admin, qui permet de valider le challenge
