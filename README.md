# Relais des Loupiotes — Système de détection de passage

Système d'éclairage automatique utilisé au **Relais des Loupiotes** de l'UCLouvain FUCaM Mons et la HELHa.

Un capteur PIR détecte les personnes qui franchissent un portail. À chaque détection, un signal OSC est envoyé à QLC+ pour déclencher une scène lumineuse aléatoire.

---

## Architecture

```
Capteur BERM (GPIO 27)
       │
       ▼
 Raspberry Pi
 auto_scene.py
       │  OSC UDP (127.0.0.1:7701)
       ▼
     QLC+
  (chasers 1–5)
```

---

## Fonctionnement

1. Le capteur PIR est câblé sur le **GPIO 27** du Raspberry Pi (pull-up interne activé).
2. `auto_scene.py` surveille en continu le signal du capteur.
3. Lors d'un **front descendant** (passage détecté), le script sélectionne aléatoirement l'une des 5 adresses OSC (`/chaser/1` à `/chaser/5`) et envoie la valeur `255`.
4. Un **délai anti-rebond de 2 secondes** évite les déclenchements multiples pour un même passage.
5. QLC+ reçoit le message OSC et exécute le chaser correspondant.

---

## Prérequis

- Raspberry Pi avec Raspbian
- Python 3
- Librairies Python :
  ```bash
  pip install RPi.GPIO python-osc
  ```
- QLC+ installé et configuré (voir [qlc_plus/](qlc_plus/))

---

## Configuration QLC+

Dans QLC+, chaque chaser (`/chaser/1` à `/chaser/5`) doit être **associé à un bouton OSC** pour pouvoir être déclenché par le signal entrant.

1. Ouvrir QLC+ et charger le fichier `.qxw` correspondant depuis le dossier [qlc_plus/](qlc_plus/).
2. Dans **Inputs/Outputs**, activer le plugin OSC en écoute sur le port `7701`.
3. Pour chaque chaser, assigner le bouton OSC à l'adresse `/chaser/N` (valeur `255` = déclencher).

---

## Lancement

```bash
python3 auto_scene.py
```

Arrêt propre avec `Ctrl+C` (le GPIO est libéré automatiquement).

---

## Fichiers

| Fichier | Description |
|---|---|
| `auto_scene.py` | Script principal — détection PIR + envoi OSC |
| `qlc_plus/` | Fichiers de configuration QLC+ (`.qxw`) |
