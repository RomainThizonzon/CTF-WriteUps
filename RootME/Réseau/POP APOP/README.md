# 📝 Write-up --- POP APOP

## 🔎 Enoncé

Retrouver le mot de passe de l’utilisateur dans la trame réseau.

Un fichier pcapng est à télécharger pour ce chall

------------------------------------------------------------------------

## 📥 Analyse du fichier

Lors de l'ouverture du fichier, on remarque des échanges avec le protocol POP.

pour ce chall, deux lignes nous intéressent :

<img width="1152" height="648" alt="wireshark apop" src="https://github.com/user-attachments/assets/f2aedf10-27f9-4b2b-9af2-7fc82066c6f8" />


------------------------------------------------------------------------

## 💡 Conclusion cruciale

La présence d'une **seule** trame egress implique :

-   Seule **une** ingress a généré une réponse\
-   Donc seules ses valeurs doivent être utilisées\
-   Ingress 1 et 3 doivent être écartées\
-   **Ingress 2 est la seule trame authentique et exploitable**

Ce point constitue la clé du challenge.

------------------------------------------------------------------------

## 🔧 Reconstruction de la trame egress

La trame egress correspond à une **ICMPv6 Echo Reply** (réponse au
ping).\
Pour la reconstruire à partir d'ingress 2 :

### 1. Inverser les adresses

  Champ         Ingress 2               Egress reconstruite
  ------------- ----------------------- -----------------------
  MAC source    `00:50:56:9E:7B:F9`     `00:50:56:9E:7B:F7`
  MAC dest      `00:50:56:9E:7B:F7`     `00:50:56:9E:7B:F9`
  IPv6 source   `2002:c000:203::b00b`   `2002:c000:203::fada`
  IPv6 dest     `2002:c000:203::fada`   `2002:c000:203::b00b`

### 2. Conserver les champs réseau

-   VLAN ID\
-   Next Header (ICMPv6)\
-   Hop Limit\
-   Payload Length

### 3. Réutiliser les champs ICMPv6

-   Identifiant\
-   Numéro de séquence\
-   Data\
-   Checksum (ou recalculé si nécessaire)

La seule modification du protocole ICMPv6 est :

    Type 128 (Echo Request) → Type 129 (Echo Reply)

------------------------------------------------------------------------

## ✅ Résultat et validation

En reconstruisant la trame egress **exclusivement** à partir de la trame
ingress 2,\
on obtient une trame complète et cohérente, permettant d'extraire le mot
de passe attendu (10 octets → 20 hex chars).

Les deux autres trames ingress étaient **volontairement incorrectes** :\
une fois ignorées, le challenge devient logique et entièrement
déterministe.

------------------------------------------------------------------------

## 🏁 Conclusion

Le challenge reposait sur un piège classique en analyse réseau :

> **Ne jamais assumer que toutes les entrées sont valides.\
> Seule la trame ingress ayant réellement généré une egress doit être
> utilisée.**

En identifiant que seule l'ingress 2 était correcte, la reconstruction
devient immédiate.
