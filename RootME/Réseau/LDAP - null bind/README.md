# 🔐 Writeup -- LDAP Anonymous (Root‑Me)

## 📌 Catégorie

Réseau

## 🧩 Énoncé

Un administrateur soupçonne qu'un membre des Anonymous s'est infiltré
dans une **nouvelle branche de l'annuaire LDAP** à l'intérieur de :

    dc=challenge01,dc=root-me,dc=org

Objectif :\
➡️ **Trouver la branche créée par l'Anonymous et récupérer son adresse
email.**

### Paramètres de connexion

  Paramètre   Valeur
  ----------- -------------------------
  Host        challenge01.root-me.org
  Port        54013
  Protocole   LDAP

------------------------------------------------------------------------

# 🧠 Comprendre le challenge

LDAP est une base de données arborescente.\
Le point de départ est :

    dc=challenge01,dc=root-me,dc=org

Mais le serveur n'autorise **aucun listing global** :\
toute tentative de recherche générale retourne :

    result: 50 Insufficient access

➡️ Cela signifie qu'il faut trouver **manuellement** la branche où
l'Anonymous s'est caché.

------------------------------------------------------------------------

# 🔍 Recherche

On tente des noms d'OU probables.\
D'après l'énoncé, il s'agit d'un membre des Anonymous → nom évident :

    ou=anonymous

On teste donc cette branche directement.

## 🧪 Commande utilisée

``` bash
ldapsearch -x -H ldap://challenge01.root-me.org:54013  -b "ou=anonymous,dc=challenge01,dc=root-me,dc=org" "(objectClass=*)"
```

### Explication rapide :

-   `-x` → authentification simple/anonyme\
-   `-H` → URL du serveur LDAP\
-   `-b` → point de départ dans l'arborescence\
-   `(objectClass=*)` → rechercher **tous les objets**

------------------------------------------------------------------------

# ✅ Résultat obtenu

Le serveur retourne deux entrées :

### 1. L'unité organisationnelle :

    dn: ou=anonymous,dc=challenge01,dc=root-me,dc=org
    objectClass: organizationalUnit
    ou: anonymous

### 2. Un utilisateur dans cette branche :

*(Adresse email masquée pour éviter le spoil)*

    dn: uid=sabu,ou=anonymous,dc=challenge01,dc=root-me,dc=org
    uid: sabu
    mail: ***************

➡️ Bingo : l'intrus est **sabu**, un membre connu d'Anonymous.

------------------------------------------------------------------------

# 🏁 Flag

    ***************

------------------------------------------------------------------------

# 📚 Notes & compréhension

-   LDAP ne permet pas toujours d'explorer l'arbre librement.
-   Mais on peut interroger une branche **même si on ne sait pas si elle
    existe**.
-   Le challenge repose sur l'intuition que les Anonymous utilisent
    souvent des noms de dossiers évidents (`ou=anonymous`).

------------------------------------------------------------------------

# 🎉 Challenge terminé !
