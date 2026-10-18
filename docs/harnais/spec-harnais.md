---
status: draft
skill: ix-recipes:feature-spec
piece: L5, volet « spec » du harnais (le volet « architecture » est dans architecture-harnais.md)
sources: le cadrage clos de la partie B (CB1 à CB41, DB1 à DB24, LR1 à LR10) ; docs/harnais/A6-architecture.md §11 (O1 à O14) ; docs/harnais/A3 à A8 ; docs/format-4.md
---

# Spec fonctionnelle du harnais de la procédure « traiter un sujet de bout en bout »

Le harnais est l'ensemble de ce que la partie B a construit pour tenir la procédure sans dépendre de la discipline du pilote : la recette de l'amont (`skills/amont-sujet.md`), le format 4 de l'exécuteur, les outils de l'aval (`harnais/harnais.py`, `harnais/hook.py`), le code de la trace (`harnais/trace_a3.py`) et les pièces migrées de la partie A (`docs/harnais/`). Cette spec dit ce qu'il fait et ce qu'il refuse. Comment il est fait est dans `architecture-harnais.md`.

## 1. Problème utilisateur

Au premier passage de la procédure, quatre points ont cédé parce que seule la discipline du pilote les tenait :

| Point | Ce qui s'est passé |
|---|---|
| un plafond de passes dépassé | la session de production avait elle-même proposé une suite « Relancer » au-delà du plafond ; elle a été choisie ; une passe hors plafond, non tracée, a écrasé des versions et modifié la grille |
| un livrable non gelé | le livrable n'était ni commité ni étiqueté avant le jugement |
| la part cachée d'une grille | son emplacement a fui deux fois : par la trace, puis par les dossiers temporaires de `claude -p` |
| un coût jamais relevé en dollars | seul `claude -p` rend un coût par appel, et la procédure ne l'a pas relevé |

Le pilote est Amiel, seul utilisateur dans B. Il mène un passage sur plusieurs heures ; l'attente de ses propres réponses en est la plus grosse part. Un client ne fait que lire la trace de son sujet, après B.

## 2. Objectif

Des résultats, pas des livrables :

1. Les quatre points ci-dessus tiennent **par construction**, sans que le pilote ait à s'en souvenir.
2. Le harnais garde les quatre qualités de la procédure : **reproductible** (même déroulé, le livrable peut varier), **partageable** (pour Amiel seul dans B), **auditable** (chaque étape garde son entrée, sa sortie, son modèle et son coût, mesuré ou marqué estimé), **documentée** (un humain qui ne connaît pas la procédure apprend à s'en servir avec le seul guide).
3. Un réglage se change dans un seul fichier (A4), avec une trace.
4. Les recettes aux formats 1 à 3, la page de suivi et ix-skills ne changent pas.

Hors du but : produire de meilleurs livrables.

## 3. Périmètre

**Dans la spec.** Les étapes 1 à 6 avec leurs pauses (l'étape 0 est une entrée, l'étape 7 est faite par Amiel) ; la recette de l'amont ; le format 4 minimal ; les outils de l'aval ; la trace au format A3 ; le contrat étendu et le niveau de garantie de chaque obligation.

**Hors périmètre**, chacun avec sa raison (CB30 à CB35, CB39) :

| Non-objectif | Raison |
|---|---|
| les trois autres types de sujet (partie C) | seul le type « code » a ses réglages, ses annexes de critères et ses skills de format ; les trois autres portent `statut: "partie C"` et le harnais les refuse |
| un front nouveau, dont l'affichage du format 4 par la page de suivi | Amiel répond aux pauses dans sa session de travail ; la page ne joue que les formats 1 à 3 et refuse de créer un parcours au format 4 |
| un client qui mène un sujet sans Claude Code ; les données d'un client chez le fournisseur du modèle | Amiel éprouve d'abord l'outil sur ses sujets avant d'y exposer des clients |
| plusieurs sujets à la fois | un pilote, un sujet à la fois (A6 §13, H1) : traces, gels et scellés se croiseraient |
| le format 4 complet (parallèle, étape qui écrit, modèle `fable`) et une production sans `/goal` | coût de construction, et l'étape qui écrit va contre l'isolation de l'exécuteur |
| la fusion et la publication de la branche, le relèvement de la version du plugin et de la page, le CHANGELOG | laissés au pilote à la livraison |
| la traduction des documents A3 et A4 vers une forme propre au harnais | le harnais n'a pas de forme propre : il lit A4 et écrit A3 tels quels |
| de meilleurs livrables | hors du but |

## 4. Décisions que le cadrage laissait à cette spec

| # | Question du cadrage | Décision | Pourquoi |
|---|---|---|---|
| D-L1 | comment livrer le hook (LR3) | des **fichiers de la branche** : `harnais/hook.py` (le code), `harnais/hooks.json` (la déclaration, au format des réglages de Claude Code). Rien n'est installé dans la configuration de la machine. Au gel d'un sujet, `geler` déclare la commande du hook dans `.claude/settings.json` du dossier **de ce sujet** | un hook installé dans la configuration de la machine changerait tous les projets ; un hook déclaré au gel ne vit que pour le sujet gelé |
| D-L2 | nom et place du fichier de trace d'un sujet (Q8) | `trace.md`, à la racine du dossier du sujet (une table par titre `### Tn.`, colonnes d'A3) | un seul fichier, lisible sans outil, trouvé sans chercher |
| D-L3 | place du fichier d'empreintes (Q8, E8) | `.harnais/empreintes.sha256` dans le dossier du sujet, **et une copie dans le scellé** : seule la copie fait foi pour un écart | un producteur qui récrit l'un ne rattrape pas l'autre qu'il ne voit pas |
| D-L4 | le parallèle du juge (Q9) | des **sous-agents ordinaires** (outil Agent) avec un modèle explicite pris dans A4 (`sous_agents_lecture`, `sous_agents_verification`, `verification_mecanique`, `nouveau_venu`) ; jamais un Workflow, jamais `fable` | un Workflow ne passe pas par le hook qui impose `model`, et Fable ne s'appelle qu'après accord, à part |
| D-L5 | comment le champ caché tient sous l'isolation de l'exécuteur | le champ est déclaré caché sur l'étape (`hidden`) : l'exécuteur le sort du HANDOFF, le range au scellé, et ne laisse dans le dossier qu'une marque et son empreinte ; aucune étape jouée par l'exécuteur ne le reçoit | l'isolation de l'exécuteur décide ce que chaque étape reçoit ; elle ne protège pas les fichiers que l'exécuteur écrit lui-même, d'où le scellé |
| D-L6 | comment les étapes 1 à 3 tournent avec la seule lecture | chaque étape est un appel neuf `claude -p --tools Read` dans un dossier jetable (exécuteur, `docs/executeur.md` §4) : elle ne peut que lire. Le harnais écrit tout ce qui doit être écrit | c'est l'isolation de l'exécuteur, inchangée ; il n'y a donc pas d'étape qui écrit (format 4 minimal) |
| D-L7 | comment la session de travail pilote l'exécuteur | par la ligne de commande : `CMD_LANCER`, puis `parcours.py next`, `validate`, `answer`, `status --json`, `supply` (par `CMD_CONTRE_VERIF`), `suite` (par `CMD_SUITE`). `status --json` dit où le parcours est arrêté (`pending`) | pas de front nouveau (CB28) ; l'état est un fichier JSON lu par programme |
| D-L8 | comment A1 et A2 se lisent sur `645a599` | l'exécuteur résout `ix-skills:<id>` dans `IX_SKILLS_PATH`. Le pilote y met un dossier `dist/skills` extrait par `git archive 645a599` (cadrage, goal-writing) et par `git archive` de la branche de `criteres-reussite` ; rien n'est écrit dans ix-skills | B ne modifie rien dans ix-skills (CB20) |
| D-L9 | comment le résultat d'une contre-vérification revient dans la boucle bornée | l'étape `contre_verif` est **externe** : l'exécuteur s'arrête avant elle et écrit le message à donner au modèle ; le pilote appelle Fable après accord ; `CMD_CONTRE_VERIF` rend la sortie à l'exécuteur, qui lit son verdict : `OK` continue, `REPRENDRE` renvoie en 2B. Chaque sortie rendue compte une passe dans `plafonds.passes_verification_max` | la recette n'appelle jamais Fable (CB9, CB10) et la boucle reste bornée |
| D-L10 | où est « le goal du sujet » que `CMD_TOUR` contrôle | `goal.md` à la racine du sujet s'il existe, sinon la sortie de l'étape du goal de l'amont (champ `goal`) | le pilote peut poser un goal rédigé à la main ; à défaut, celui de l'amont |
| D-L11 | boucle 1d | le renvoi se fait vers l'étape qui écrit le cadrage soumis (`fusion`, 1c), non vers 1a | renvoyer en 1a rejouerait la fiche de contexte et sa validation ; le verdict ne porte que sur le cadrage soumis |

## 5. Utilisateurs et histoires

| # | Histoire |
|---|---|
| U1 | En tant que **pilote d'un sujet de code** (Amiel), je veux lancer un sujet, répondre aux pauses et choisir une suite aux plafonds, afin que les garde-fous tiennent sans que je les surveille. |
| U2 | En tant que **session de production sous `/goal`**, je veux un contrôle avant chaque tour et un hook qui m'empêche de modifier ce qui me juge, afin de travailler pour l'intention sans pouvoir écrire pour la grille. |
| U3 | En tant que **juge d'un sujet**, je veux le livrable tel qu'à son étiquette et la part cachée hors de portée du producteur, afin que mon verdict vaille. |
| U4 | En tant qu'**auditeur** (Amiel, ou un client pour son seul sujet), je veux retrouver pour chaque étape l'entrée, la sortie, le modèle, la durée et le coût avec sa source, dans un fichier lisible sans Claude Code. |
| U5 | En tant que **mainteneur**, je veux changer un plafond, un modèle ou un skill de format dans A4 seul, et savoir quelle brique entretenir pour le reste. |
| U6 | En tant qu'**auteur de recettes d'ix-recipes**, je veux que le format 4 soit refusé, avec la cause, par tout lecteur qui ne le joue pas, et que les formats 1 à 3 tournent comme avant. |

## 6. Le contrat étendu et son niveau de garantie

Le contrat est O1 à O14 d'`A6-architecture.md` §11, plus P2, P3, P4, P5, P10 et P12 comme obligations du harnais (CB2, CB3). Le niveau de garantie est celui de CB4 : un **mécanisme** (qui empêche l'écart) pour O5 (plafonds), O10 (gel) et O11 (scellé) ; le **natif** pour O12 (les pauses) ; un **contrôle par script** pour le reste. Pour le gel, le hook plus les empreintes vérifiées avant chaque tour tiennent le niveau « mécanisme » (décision d'Amiel, pause 2).

| Obligation | Niveau | Ce qui la tient | Où |
|---|---|---|---|
| O1 lire A4, relever sa version et son empreinte, copier les plafonds, refuser un type absent ou « partie C » | contrôle par script | `lancer` lit A4, écrit T1 et T2, et refuse sans rien créer | `harnais.py lancer` |
| O2 modèle explicite = clé du rôle ; Fable après accord, à part | contrôle par script | `role` et `model` de chaque étape sont comparés à A4 par `build.py` et à la création du parcours ; `fable` est refusé en format 4 ; la contre-vérification est une étape externe | `build.py`, `parcours.py new` |
| O3 écrire A3 | contrôle par script | la trace est reconstruite de l'état et **contrôlée** (colonnes, cellules, coûts) avant d'être écrite ; une trace qui ne tient pas A3 n'est pas écrite | `trace_a3.py` |
| O4 confiner | contrôle par script | la trace ne cite que des chemins relatifs au sujet ; le scellé n'y figure jamais | `trace_a3.py` |
| O5 plafonds : compter, s'arrêter, offrir exactement les suites d'A4, ne jamais choisir | **mécanisme** | passes : l'exécuteur s'arrête et ne rejoue rien au plafond ; tours : `tour` et `tour-correction` refusent au plafond et ne comptent pas l'appel refusé ; la suite n'est consignée que par `suite`, hors de la session de production | `parcours.py`, `harnais.py` |
| O6 séparer 2A et 2B | contrôle par script | chaque étape ne reçoit que ce que sa ligne `receives` liste ; un test vérifie que le goal ne reçoit rien des critères et inversement | recette, `tests/test_harnais.py` |
| O7 alimenter A2 avec les seules entrées prévues, remplir les emplacements avant le premier tour | **mécanisme** (le tour) | `tour` refuse tant que le goal contient un emplacement réservé non rempli hors de sa section « valeurs fixées plus tard » | `harnais.py tour` |
| O8 demander explicitement le mode `close` | contrôle par script | la mission de l'étape de clôture le demande en toutes lettres | recette |
| O9 appliquer A5 au bon moment | contrôle par script | l'étape d'évaluation reçoit A5 comme pièce du dossier et sa mission nomme les points qui s'appliquent avant la pause | recette |
| O10 geler | **mécanisme** | empreintes relevées au gel ; hook qui refuse l'écriture ; empreintes vérifiées avant **chaque** tour, comparées à la copie du scellé | `geler`, `hook.py`, `empreintes`, `tour` |
| O11 sceller | **mécanisme** | le champ caché sort du dossier au moment où il est produit ; le scellé est un dossier donné par `IX_SCELLE_DIR`, refusé s'il est dans un dépôt git ou lié à un chemin que lit le producteur ; le chemin n'est écrit nulle part ; le hook ferme l'accès | `parcours.py`, `commun.py`, `hook.py` |
| O12 faire attendre les pauses | natif | `pause: validate` et `pause: answers` de l'exécuteur | exécuteur |
| O13 mesurer sans inventer | contrôle par script | coût `mesuré` seulement quand l'outil le rend (`total_cost_usd`), sinon `n.c.` avec la raison ; jamais `estimé` sans méthode | `trace_a3.py` |
| O14 rendre le déroulé rejouable | contrôle par script | T3 à T5 gardent entrée, sortie, modèle, skill (version, empreinte), réglages | `trace_a3.py` |
| P2 tout référentiel qui juge le producteur est figé et tenu hors de lui | **mécanisme** | comme O10 | |
| P3 la production ne propose jamais de suite | **mécanisme** | le refus d'un tour au plafond dit que la main revient au pilote et ne liste aucune suite ; `suite` est un outil du pilote | `harnais.py` |
| P4 les essais qui comptent appartiennent au juge | contrôle par script | `juge` relance le script de recette dans la session du juge ; une sortie du producteur ne compte jamais | `harnais.py juge` |
| P5 la fin de la production gèle le livrable par commit et étiquette | **mécanisme** | `fin-production` ; `juge` refuse si le livrable a bougé depuis son étiquette | `harnais.py` |
| P10 aucun emplacement caché dans un fichier que le producteur lit ; essais cachés depuis un dossier neutre ; le juge nettoie | **mécanisme** | le chemin du scellé n'est écrit dans aucun fichier (T9 : `non écrit`) ; le juge tourne dans un dossier jetable neuf, supprimé après l'appel avec le dossier de projet que `claude` aurait créé | `harnais.py juge` |
| P12 tout retour en 2B rouvre le gel | **mécanisme** | `regeler` ne passe que si un « contourner » est consigné depuis le dernier gel ; il relève de nouvelles empreintes et remet les compteurs de tours à zéro | `harnais.py regeler` |

**Ce que le hook ne voit pas.** Un hook de la famille `PreToolUse` reçoit l'appel d'un outil avant qu'il ne s'exécute. Pour `Write`, `Edit`, `MultiEdit` et `NotebookEdit` il lit le chemin et décide. Pour `Bash` il ne lit qu'une chaîne : il reconnaît la redirection `>`, `tee`, `sed -i`, `mv`, `cp`, `rm`, `chmod`, `git checkout`, et les interpréteurs qui écrivent dans leur code, mais **nul motif ne reconnaît toutes les écritures possibles d'une commande shell** (un script écrit puis lancé, une variable d'environnement, un chemin construit à l'exécution, un autre outil du système). Ce que le hook laisse passer, les **empreintes vérifiées avant chaque tour** le rattrapent au tour suivant : `tour` refuse au premier écart et nomme le fichier, avec une copie des empreintes que la session de production ne voit pas. Ce que ni l'un ni l'autre ne peut empêcher : qu'un fichier figé soit modifié puis restauré entre deux tours, ou qu'une lecture du scellé ait lieu par un chemin que le hook ne connaît pas (le hook ne connaît le scellé que si la variable `IX_SCELLE_DIR` figure dans l'environnement de la session). Une écriture rendue **impossible** demanderait un compte système séparé qui possède ces fichiers, ce qui est hors de B.

## 7. Exigences

Étiquettes : **decided** (avec sa source dans le cadrage), **proposed** (à confirmer). MoSCoW : Must, Should, Could, Won't.

### 7.1 Recette de l'amont (L1)

| ID | Exigence | MoSCoW | Label |
|---|---|---|---|
| R1 | La recette joue 1a à 1e, 2A et 2B séparées, la réconciliation et la pause 2, avec les pauses 1 et 2 | Must | decided (L1) |
| R2 | Les trois boucles de vérification (1d, vérification du goal, contre-vérification) sont bornées par `plafonds.passes_verification_max` ; chaque passe de contre-vérification, celle de Fable comprise, compte | Must | decided (CB12) |
| R3 | Au plafond, la recette s'arrête, trace le constat et offre exactement `suites_au_plafond.passes_verification` (jamais « contourner ») | Must | decided (CB12, A4) |
| R4 | La recette s'arrête avant la contre-vérification ; elle n'appelle jamais Fable | Must | decided (CB9, CB10) |
| R5 | Entre 1e et 2A, une vérification de forme compare la liste « livrable vers skill de format » à celle d'A4 avec le modèle `verification_mecanique` ; si elle ne correspond pas, la recette ne passe pas à 2A | Must | decided (CB36) |
| R6 | La part cachée vit dans un champ qui ne va à aucune étape jouée par l'exécuteur | Must | decided (CB14) |
| R7 | Chaque étape prend le modèle de son rôle dans A4 | Must | decided (CB8) |
| R8 | Les skills sont ceux d'`A4` et de la procédure ; `goal-writing` et `cadrage` (mode `close`) se lisent sur `645a599` ; `criteres-reussite` sur sa branche | Must | decided (DB5, CB20) |

### 7.2 Format 4 (L2)

| ID | Exigence | MoSCoW | Label |
|---|---|---|---|
| F1 | Boucles bornées, champ caché, arrêt avant une étape jouée à part ; ni parallèle, ni étape qui écrit ou lance des commandes, ni modèle `fable` | Must | decided (CB16) |
| F2 | `build.py` refuse en format 4 une étape `parallel: true`, une étape `writes: true`, un modèle `fable`, avec un message qui nomme la cause | Must | decided |
| F3 | Les formats 1 à 3 ne changent pas ; un lecteur qui ne connaît pas le format 4 le refuse au lieu de le jouer à moitié | Must | decided (CB19) |
| F4 | La page de suivi continue d'annoncer et d'accepter les formats 1 à 3 seulement ; elle refuse de créer un parcours au format 4 | Must | decided (CB19, CB28) |
| F5 | Sous le moteur `simulation`, une étape qui vérifie écrit `OK` en première ligne de son champ de verdict | Must | decided |
| F6 | L'acceptation de `model: fable` par l'exécuteur pour les formats 1 à 3 n'est pas corrigée dans B (notée pour le bilan) | Won't | decided |

### 7.3 Outils de l'aval (L3)

| ID | Exigence | MoSCoW | Label |
|---|---|---|---|
| A1 | Les plafonds de la production et de la correction sont comptés par le harnais ; un appel refusé ne compte pas de tour | Must | decided (CB13) |
| A2 | Le gel : empreintes relevées, vérifiées avant chaque tour, écriture refusée, regel à tout retour en 2B | Must | decided (P2, P12) |
| A3 | Le scellé : hors de tout dépôt, dans le dossier de `IX_SCELLE_DIR`, juge lancé d'un dossier neutre puis nettoyé, versement dans la trace à la fin du jugement | Must | decided (P10) |
| A4 | Le gel du livrable en fin de production : commit et étiquette | Must | decided (P5) |
| A5 | Le lancement du juge : refusé si le livrable a bougé depuis son étiquette ; sa sortie est rangée au scellé ; le constat du producteur nomme l'exigence de chaque ligne cachée en échec sans rien de son contenu | Must | decided (CB15) |
| A6 | `IX_SCELLE_DIR` est une entrée donnée à l'exécution, exportée pour toutes les commandes (amont compris) ; le harnais refuse de travailler si elle manque, si elle désigne un dossier dans un dépôt git ou sous un chemin que lit le producteur ; le code n'en contient aucune valeur | Must | decided (CB15) |
| A7 | Le hook refuse l'écriture des fichiers figés, de l'état du harnais, des réglages qui déclarent des hooks, du fichier qui déclare le hook, et tout appel de `CMD_SCEAU` depuis la session de production | Must | decided |
| A8 | Le hook est livré comme fichiers de la branche et n'est installé dans aucune configuration de machine ni de session | Must | decided (LR3) |
| A9 | La fin du jugement (`ouvrir`) couvre toute la boucle des étapes 5 et 6 : refusée avant la fin des tours de correction | Must | decided (DB10) |

### 7.4 Trace (L4)

| ID | Exigence | MoSCoW | Label |
|---|---|---|---|
| T1 | La trace de chaque sujet suit A3 : onze tables, aucune cellule vide, coût `mesuré` seulement quand l'outil le rend | Must | decided (CB25, CB38) |
| T2 | La trace de l'amont est traduite vers A3 : étapes 0, 1a à 3, une ligne par passage d'une étape, `passe n` pour une étape qui vérifie | Must | decided |
| T3 | La trace est reconstruite de l'état : l'écrire deux fois donne le même fichier | Should | decided |
| T4 | Une trace qui ne tient pas A3 n'est pas écrite ; le refus nomme l'écart | Should | proposed |

## 8. Critères d'acceptation

Un cas qui passe et un cas refusé pour chaque mécanisme (CB37).

| Exigence | Étant donné | Quand | Alors |
|---|---|---|---|
| R2, R3 | un cadrage dont l'évaluation répond `REPRENDRE` | l'évaluation a joué le nombre de passes du plafond | l'exécuteur s'arrête, `pending.type` vaut `ceiling`, les suites sont exactement celles d'A4 sans « contourner » ; `next` ne rejoue rien |
| R2 | A4 avec un autre plafond | on ne modifie que A4 | le nombre de passes change, sans autre édition |
| R4 | la recette au point de la contre-vérification | `next` s'exécute | le parcours est arrêté, `pending.step` vaut l'étape de contre-vérification, aucun appel n'a été fait |
| R4, D-L9 | la sortie de la contre-vérification, `REPRENDRE` | `CMD_CONTRE_VERIF` la rend | l'étape 2B est rejouée avec le verdict, une passe de plus est comptée |
| R5 | une liste qui ne correspond pas à A4 | l'étape de vérification de forme rend `REPRENDRE` sans boucle | le parcours attend le pilote, 2A n'est pas jouée |
| R6 | un champ caché rempli par une étape | le parcours a tourné | aucun fichier du dossier du sujet ne contient son contenu ; le scellé le contient ; aucune étape jouée ne le reçoit |
| F2 | une copie de la recette avec `parallel: true`, `writes: true` ou un modèle `fable` sur sa première étape | `build.py <id> --validate` | refus, le message nomme la cause |
| F3, F4 | la page de suivi | on crée un parcours sur une recette au format 4 | 422 `recipe_refused` ; `recipe_formats` vaut `[1, 2, 3]` |
| A1 | un sujet gelé au plafond de tours | `CMD_TOUR` | refus, le compteur ne bouge pas ; après `suite … relancer N`, N tours de plus |
| A1 | un sujet gelé | `CMD_TOUR_CORRECTION` | compté à part, avec `tours_correction_max` |
| A2 | un fichier figé modifié | `CMD_EMPREINTES` ou `CMD_TOUR` | refus, le premier fichier en cause est nommé |
| A2 | le hook, un fichier figé | un événement d'écriture | code 2 ; une écriture d'un autre fichier : code 0 |
| A2, P12 | aucun « contourner » consigné | `CMD_REGELER` | refus ; après un « contourner », nouvelles empreintes et compteurs remis à zéro |
| A3 | un juge qui rend une ligne cachée en échec | `CMD_JUGE` | le constat nomme l'exigence, jamais la preuve ; la sortie est au scellé ; une ligne de T3 d'étape 5 est écrite |
| A4, A5 | un livrable modifié après son étiquette | `CMD_JUGE` | refus |
| A6 | `IX_SCELLE_DIR` absente, dans un dépôt git, ou sous le dossier du sujet | n'importe quelle commande | refus, aucune valeur par défaut |
| A7 | un événement `Bash` qui lance `CMD_SCEAU` | le hook | code 2 |
| A9 | un jugement avec une ligne cachée en échec et des tours de correction restants | `CMD_OUVRIR` | refus ; à la fin des tours, la part cachée et la trace du juge sont versées, T9 passe à `ouvert` avec l'emplacement relatif |
| T1 | une trace écrite | on lit T3 | aucune cellule vide ; un coût simulé est `n.c.` avec sa raison, jamais `mesuré` |

## 9. Métriques de succès

| Métrique | Leading ou lagging | Valeur de départ | Seuil | Méthode | Quand |
|---|---|---|---|---|---|
| nombre de plafonds dépassés par la production sur un passage réel | lagging | à mesurer | 0 | lecture de T7 et de T3 (tours) | au bilan de B-b |
| nombre de livrables jugés sans étiquette | lagging | à mesurer | 0 | lecture de T9 | au bilan de B-b |
| nombre de fuites de la part cachée vers le dossier du sujet | lagging | à mesurer | 0 | recherche d'un marqueur dans le dossier du sujet après le passage | au bilan de B-b |
| part des lignes de T3 dont le coût est connu en dollars quand l'outil le rend | leading | à mesurer | 100 % | contrôle de la trace | à chaque trace |

Les dates d'évaluation sont des événements, pas des dates de calendrier.

## 10. Questions ouvertes

| # | Question | Bloquante ? | Qui répond |
|---|---|---|---|
| Q1 | Le lancement réel du juge (`claude -p --allowedTools …`) n'est pas éprouvé : aucun essai n'appelle de modèle réel. Les options exactes sont à confirmer au premier passage réel | non | Amiel, à B-b |
| Q2 | Les jetons ne sont relevés par aucun outil que le harnais appelle : T3 écrit `n.c.`. Faut-il lire le total de jetons de `claude -p --output-format json` ? | non | Amiel |
| Q3 | La boucle 1d renvoie en 1c et non en 1a (D-L11) : à confirmer | non | Amiel |
| Q4 | Le hook ne connaît le scellé que si `IX_SCELLE_DIR` est dans l'environnement de la session de production ; le garder hors de cet environnement protège mieux la variable mais ferme moins de chemins | non | Amiel |
| Q5 | Le modèle de l'étape externe (Fable chez Amiel) n'est consigné dans la trace que si le pilote le donne (`IX_MODELE_EXTERNE`) : sinon `n.c.` | non | Amiel |

## 11. Décisions laissées au pilote

La version du plugin, la version de la page de suivi et le CHANGELOG ne sont pas touchés par B : le pilote les fait à la livraison, avec le commit et l'étiquette `b-a-livrable`. La copie de `build.py` d'ix-skills n'est pas mise à jour (CB20).
