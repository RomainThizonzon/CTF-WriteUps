# Writeup -- Local File Inclusion - Double encoding

## Catégorie

Web - Server

## Énoncé

Trouvez le mot de passe de validation dans le code source du site web.

## Choses à savoir 

Le double encodage, c'est encoder au format url les `/`, les `.` etc, puis réencoder les `%` dans le code URL de ces caractères.

Par exemple : j'encode ../ en URL : `%2E%2E%2F`

Je peux ensuite encoder les %, mon ../ devient donc : `%252E%252E%252F`

On peut utiliser cette technique lorsque le site filtre les encodages URL simples.

## Exploitation

On cherche le flag stocké dans le code source.
