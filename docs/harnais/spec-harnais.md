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

1. Les quatre points ci-dessus sont **interdits et détectés** (niveau défini en §6), sans que le pilote ait à s'en souvenir pour ce que le harnais refuse ; ce que le refus laisse passer est écrit en §6.2, avec ce qui le détecte.
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
| D-L1 | comment livrer le hook (LR3) | des **fichiers de la branche** : `harnais/hook.py` (le code), `harnais/hooks.json` (la déclaration, au format des réglages de Claude Code). Rien n'est installé dans la configuration de la machine. Au gel d'un sujet, `geler` déclare les hooks (`PreToolUse`, `Stop`, `UserPromptSubmit`) dans `.claude/settings.json` du dossier **de ce sujet** | un hook installé dans la configuration de la machine changerait tous les projets ; un hook déclaré au gel ne vit que pour le sujet gelé |
| D-L2 | nom et place du fichier de trace d'un sujet (Q8) | `trace.md`, à la racine du dossier du sujet (une table par titre `### Tn.`, colonnes d'A3) | un seul fichier, lisible sans outil, trouvé sans chercher |
| D-L3 | place du fichier d'empreintes (Q8, E8) | `.harnais/empreintes.sha256` dans le dossier du sujet, **et une copie dans le scellé** : seule la copie fait foi pour un écart | un producteur qui récrit l'un des deux est vu ; qui récrit le fichier figé **et** ses deux copies d'un même geste (par le résidu de §6.2) n'est vu par rien dans le harnais |
| D-L4 | le parallèle du juge (Q9) | des **sous-agents ordinaires** (outil Agent) avec un modèle explicite pris dans A4 (`sous_agents_lecture`, `sous_agents_verification`, `verification_mecanique`, `nouveau_venu`) ; jamais un Workflow, jamais `fable` | un Workflow ne passe pas par le hook qui impose `model`, et Fable ne s'appelle qu'après accord, à part |
| D-L5 | comment le champ caché tient sous l'isolation de l'exécuteur | le champ est déclaré caché sur l'étape (`hidden`) : l'exécuteur le sort du HANDOFF, le range au scellé, et ne laisse dans le dossier qu'une marque et son empreinte ; aucune étape jouée par l'exécuteur ne le reçoit | l'isolation de l'exécuteur décide ce que chaque étape reçoit ; elle ne protège pas les fichiers que l'exécuteur écrit lui-même, d'où le scellé |
| D-L6 | comment les étapes 1 à 3 tournent avec la seule lecture | chaque étape est un appel neuf `claude -p --tools Read` dans un dossier jetable (exécuteur, `docs/executeur.md` §4) : elle ne peut que lire. Le harnais écrit tout ce qui doit être écrit | c'est l'isolation de l'exécuteur, inchangée ; il n'y a donc pas d'étape qui écrit (format 4 minimal) |
| D-L7 | comment la session de travail pilote l'exécuteur | par la ligne de commande : `CMD_LANCER`, puis `parcours.py next`, `validate`, `answer`, `status --json`, `supply` (par `CMD_CONTRE_VERIF`), `suite` (par `CMD_SUITE`). `status --json` dit où le parcours est arrêté (`pending`) | pas de front nouveau (CB28) ; l'état est un fichier JSON lu par programme |
| D-L8 | comment A1 et A2 se lisent sur `645a599` | l'exécuteur résout `ix-skills:<id>` dans `IX_SKILLS_PATH`. Le pilote y met un dossier `dist/skills` extrait par `git archive 645a599` (cadrage, goal-writing) et par `git archive` de la branche de `criteres-reussite` ; rien n'est écrit dans ix-skills | B ne modifie rien dans ix-skills (CB20) |
| D-L9 | comment le résultat d'une contre-vérification revient dans la boucle bornée | l'étape `contre_verif` est **externe** : l'exécuteur s'arrête avant elle et écrit le message à donner au modèle ; le pilote appelle Fable après accord ; `CMD_CONTRE_VERIF` rend la sortie à l'exécuteur, qui lit son verdict : `OK` continue, `REPRENDRE` renvoie en 2B. Chaque sortie rendue compte une passe dans `plafonds.passes_verification_max` | la recette n'appelle jamais Fable (CB9, CB10) et la boucle reste bornée |
| D-L10 | où est « le goal du sujet » que le contrôle avant un tour (`CMD_TOUR`, hook de début de tour) lit | `goal.md` à la racine du sujet s'il existe, sinon la sortie de l'étape du goal de l'amont (champ `goal`) | le pilote peut poser un goal rédigé à la main ; à défaut, celui de l'amont |
| D-L11 | boucle 1d | le renvoi se fait vers l'étape qui écrit le cadrage soumis (`fusion`, 1c), non vers 1a | renvoyer en 1a rejouerait la fiche de contexte et sa validation ; le verdict ne porte que sur le cadrage soumis |
| D-L12 | qui lance quoi, et ce qui exige `IX_SCELLE_DIR` | la session de production **ne lance aucune commande du harnais**, sauf, si elle le veut, `fin-production` (qui n'exige rien). Les tours sont comptés par les hooks (D-L13). Toutes les autres commandes, `tour` et `tour-correction` comprises, exigent `IX_SCELLE_DIR`, et huit d'entre elles exigent de plus le jeton du scellé (§6.1) | l'emplacement du scellé doit être hors de l'environnement de la session de production (O11) ; avant ce tour 2, `tour` était lancé par la production, et le compte n'existait que si elle le lançait |
| D-L13 | qui compte les tours (O5) | la **garde**, `garde.json` au scellé du sujet : le compteur de chaque phase, les plafonds copiés au lancement, ce que `suite` y ajoute, la phase (avant le gel, production, correction, ouvert), les fichiers figés. Trois hooks de Claude Code l'appliquent sans que la production lance quoi que ce soit : `Stop` compte un tour à **chaque fin de tour** (la boucle `/goal` est un hook `Stop` : les deux se déclenchent après chaque tour) et arrête la boucle (`continue: false`) au plafond, sur un écart de compteur ou d'empreinte ; `UserPromptSubmit` refuse de commencer un tour dans ces cas ; `PreToolUse` refuse **tout outil** dans ces cas. `tour` et `tour-correction` font le même compte à la main, pour le pilote et pour les essais (un tour compté deux fois ne fait qu'avancer le plafond) | un compte qui dépend de ce que la production lance n'est même pas interdit (rejugement du tour 1) ; l'état du sujet, que la production peut écrire, n'est plus qu'un affichage recopié de la garde |
| D-L14 | où est la référence du compteur et du jeton | la garde est au **scellé** ; `.harnais/temoin.json`, dans le sujet, en garde la séquence et la tête (sha256 du contenu). Chaque écriture de la garde récrit le témoin. Les hooks et les commandes du pilote refusent sur tout écart entre les deux. `pilote_sha256` (la référence du jeton) est dans la garde, plus dans l'état | un compteur remis à zéro dans l'un des deux se voit avant l'outil suivant ; le remettre à zéro dans les deux d'un même geste demande de trouver la garde ; rien dans le harnais ne le voit, c'est un geste du résidu et son détecteur est un contrôle du pilote (§6.2) |
| D-L15 | comment les hooks trouvent le scellé sans `IX_SCELLE_DIR` | le **pointeur** : `geler` écrit le scellé du sujet, en hexadécimal, dans l'argument `--garde` des hooks `Stop` et `UserPromptSubmit` déclarés dans `.claude/settings.json` ; le hook `PreToolUse` le relit de ces réglages. Le nom du dossier scellé du sujet est **tiré au hasard** au lancement et gardé dans `index.json`, à la racine du scellé : il ne se calcule plus depuis le chemin du sujet et n'est écrit dans aucun autre fichier | le hook doit connaître l'emplacement exact pour le refuser par chemin ; l'hexadécimal n'est pas un secret, il évite qu'un `grep` écrive l'emplacement en clair ; ce qui le garde de la production est le refus de lire ces réglages |

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

Le contrat est O1 à O14 d'`A6-architecture.md` §11, plus P2, P3, P4, P5, P10 et P12 comme obligations du harnais (CB2, CB3). Le niveau visé par le cadrage (CB4) était un **mécanisme** (qui empêche l'écart) pour O5 (plafonds), O10 (gel) et O11 (scellé) ; le **natif** pour O12 (les pauses) ; un **contrôle par script** pour le reste.

**Révision 2B du 19/10/2026 (ligne 55 de la grille, décision d'Amiel après le rejugement du tour 2).** Pour O5 (tours et suite), O10 et O11, le niveau exigé n'est plus un mécanisme qui empêche, mais **« interdit et détecté »**, et P2, P3 et P10, qui les suivent, ont le même niveau. Un vrai empêchement demanderait une isolation par le système (compte séparé, bac à sable), hors de B-a : il devient une suite (B-b ou une partie à part). « Interdit et détecté » veut dire : un moyen qui refuse l'écart sous les formes qu'il reconnaît (le hook, ou l'outil du pilote qui exige le scellé), plus, pour chaque geste que ce refus laisse passer, un détecteur nommé avec le moment où il détecte, ou la mention « rien dans le harnais ». Rien de ce qui n'est qu'interdit n'est appelé « impossible ».

**Le niveau réel, dit sans rien annoncer de plus que ce qui existe.** Les niveaux qui suivent emploient cinq mots, toujours dans le même sens :

| Mot | Sens |
|---|---|
| **interdit et détecté** | le refus vaut pour les formes que le hook ou l'outil reconnaît ; un processus qui prend une autre forme n'est pas empêché ; §6.2 écrit chaque geste qui reste possible, ce qui le détecte et quand, ou « rien dans le harnais » |
| **mécanisme** | l'écart est refusé par le code d'un outil du harnais, sur les formes que ce code connaît, et non par la discipline de la production ; même réserve que ci-dessus : le résidu de §6.2 n'est pas empêché |
| **hook** | l'écart est refusé quand l'appel a une forme que le hook reconnaît ; une autre forme lui échappe |
| **discipline** | l'écart n'est empêché que si la session de production fait ce que le goal lui demande ; le harnais ne peut pas l'y contraindre |
| **contrôle du pilote** | l'écart est vu, après coup, par une commande ou une lecture du pilote ; il n'est pas empêché |

**Après le tour 3 de correction**, O5 (tours et suite), O10 et O11 sont « interdits et détectés », sous la réserve que §6.2 dit : le **résidu**, qui n'est pas empêché, et dont chaque geste a son détecteur et son moment, ou « rien dans le harnais ». Une autre réserve est d'une autre nature : les hooks sont **essayés** en les appelant avec des événements d'essai, comme B le fait de tout moyen (aucun appel de modèle) ; leur comportement dans une vraie session `/goal` repose sur la documentation de Claude Code (le `Stop` d'une session et `/goal` se déclenchent après chaque tour ; `continue: false` arrête la boucle) et n'est **pas éprouvé** : à confirmer au premier passage réel (B-b). Tout ce qui suit suppose que les hooks du projet se chargent : `R` exporté, session lancée dans le dossier du sujet, dossier de confiance, `disableAllHooks` absent. Si la session ne les charge pas, rien ne compte ; le pilote le voit à la trace (aucune ligne `tour n` après une session) et `empreintes` vérifie que les hooks déclarés désignent bien le scellé.

| Obligation | Niveau | Ce qui la tient | Où |
|---|---|---|---|
| O1 lire A4, relever sa version et son empreinte, copier les plafonds, refuser un type absent ou « partie C » | contrôle par script | `lancer` lit A4, écrit T1 et T2, et refuse sans rien créer | `harnais.py lancer` |
| O2 modèle explicite = clé du rôle ; Fable après accord, à part | contrôle par script | `role` et `model` de chaque étape sont comparés à A4 par `build.py` et à la création du parcours ; `fable` est refusé en format 4 ; la contre-vérification est une étape externe | `build.py`, `parcours.py new` |
| O3 écrire A3 | contrôle par script | la trace est reconstruite de l'état et **contrôlée** (colonnes, cellules, coûts) avant d'être écrite ; une trace qui ne tient pas A3 n'est pas écrite | `trace_a3.py` |
| O4 confiner | contrôle par script | la trace ne cite que des chemins relatifs au sujet ; le scellé n'y figure jamais | `trace_a3.py` |
| O5 plafonds : compter, s'arrêter, offrir exactement les suites d'A4, ne jamais choisir | passes : **mécanisme** ; tours : **interdit et détecté** (hooks `Stop`, `UserPromptSubmit`, `PreToolUse`, garde au scellé), non éprouvé en session réelle ; la suite : **interdit et détecté** | passes : l'exécuteur s'arrête et ne rejoue rien au plafond ; tours : chaque fin de tour est comptée par le hook `Stop`, sans que la production lance quoi que ce soit ; au plafond la boucle s'arrête, aucun tour ne peut commencer et aucun outil n'est permis, tant qu'aucune suite n'a ajouté de tours ; le compteur remis à zéro dans la garde seule ou dans le témoin seul est vu avant l'outil suivant ; remis à zéro ou relevé dans l'état, il ne change rien (les hooks lisent la garde) et l'état est écrasé par la garde au geste suivant du pilote ; la suite n'est consignée que par `suite`, qui refuse tout appelant qui ne tient pas le scellé du sujet (§6.1) et dont l'effet vit dans la garde ; un appelant qui tient le scellé par le résidu consigne une suite que rien n'empêche : la ligne T7 qu'elle laisse la fait voir au pilote (§6.2) | `parcours.py`, `garde.py`, `hook.py`, `harnais.py` |
| O6 séparer 2A et 2B | contrôle par script | chaque étape ne reçoit que ce que sa ligne `receives` liste ; un test vérifie que le goal ne reçoit rien des critères et inversement | recette, `tests/test_harnais.py` |
| O7 alimenter A2 avec les seules entrées prévues, remplir les emplacements avant le premier tour | **mécanisme** (le hook de début de tour) | `UserPromptSubmit` refuse de commencer un tour tant que le goal contient un emplacement réservé non rempli hors de sa section « valeurs fixées plus tard » ; `tour` fait le même contrôle pour le pilote | `garde.py`, `hook.py`, `harnais.py tour` |
| O8 demander explicitement le mode `close` | contrôle par script | la mission de l'étape de clôture le demande en toutes lettres | recette |
| O9 appliquer A5 au bon moment | contrôle par script | l'étape d'évaluation reçoit A5 comme pièce du dossier et sa mission nomme les points qui s'appliquent avant la pause | recette |
| O10 geler | **interdit et détecté** : hook + empreintes vérifiées par les hooks (pause 2 ; niveau « interdit et détecté » depuis la révision 2B) | empreintes relevées au gel ; hook qui refuse l'écriture quand il en reconnaît la forme ; empreintes comparées à la copie du scellé par les hooks **avant chaque outil, à chaque début et à chaque fin de tour**, sans que la production lance quoi que ce soit : un fichier figé changé par une forme que le hook ne reconnaît pas arrête la boucle et refuse tous les outils jusqu'à ce que le pilote le règle ; et à chaque `empreintes`, `tour` et `juge` du pilote ; un fichier figé récrit avec ses deux copies, ou modifié puis restauré entre deux contrôles, n'est pas vu (§6.2) | `geler`, `hook.py`, `garde.py`, `empreintes`, `juge` |
| O11 sceller | **interdit et détecté** | le champ caché sort du dossier au moment où il est produit ; le scellé est un dossier donné par `IX_SCELLE_DIR`, refusé s'il est dans un dépôt git ou lié à un chemin que lit le producteur ; **aucun emplacement par défaut ni suggéré** ; le sous-dossier de chaque sujet porte un nom **tiré au hasard**, jamais calculé depuis le chemin du sujet et écrit dans aucun fichier du sujet ; la session de production ne reçoit pas la variable ; le hook refuse l'accès au scellé **par son chemin**, pour `Read`, `Glob`, `Grep`, les outils d'écriture et les formes shell qui désignent, listent ou cherchent (§6.2) ; une lecture par une forme que le hook ne résout pas n'est pas empêchée, et rien dans le harnais ne la voit ; seule la recherche du pilote dans la transcription (§6.2) peut la faire voir, après coup | `parcours.py`, `commun.py`, `hook.py` |
| O12 faire attendre les pauses | natif | `pause: validate` et `pause: answers` de l'exécuteur | exécuteur |
| O13 mesurer sans inventer | contrôle par script | coût `mesuré` seulement quand l'outil le rend (`total_cost_usd`), sinon `n.c.` avec la raison ; jamais `estimé` sans méthode | `trace_a3.py` |
| O14 rendre le déroulé rejouable | contrôle par script | T3 à T5 gardent entrée, sortie, modèle, skill (version, empreinte), réglages | `trace_a3.py` |
| P2 tout référentiel qui juge le producteur est figé et tenu hors de lui | comme O10 | comme O10 | |
| P3 la production ne propose jamais de suite | **interdit et détecté** (comme O5) | l'arrêt au plafond dit que la main revient au pilote et ne liste aucune suite ; `suite` est un outil du pilote, qui se refuse de lui-même à tout appelant qui ne tient pas le scellé, et dont l'effet vit au scellé ; une suite consignée par le résidu est vue en T7 (§6.2) | `hook.py`, `harnais.py`, `commun.py` |
| P4 les essais qui comptent appartiennent au juge | contrôle par script | `juge` relance le script de recette dans la session du juge, depuis un dossier jetable neuf, supprimé après l'appel ; une sortie du producteur ne compte jamais | `harnais.py juge` |
| P5 la fin de la production gèle le livrable par commit et étiquette | **mécanisme** | `fin-production` ; `juge` refuse si le livrable a bougé depuis son étiquette | `harnais.py` |
| P10 aucun emplacement caché dans un fichier que le producteur lit ; essais cachés depuis un dossier neutre ; le juge nettoie | **interdit et détecté** (comme O11) | le chemin du scellé n'est écrit en clair dans aucun fichier (T9 : `non écrit` ; le pointeur des réglages est en hexadécimal, et les réglages sont refusés à la lecture) ; le nom du sous-dossier est tiré au hasard ; le juge tourne dans un dossier jetable neuf, supprimé après l'appel avec le dossier de projet que `claude` aurait créé | `harnais.py juge`, `commun.py` |
| P12 tout retour en 2B rouvre le gel | **mécanisme** (même réserve du résidu que O5 : un « contourner » consigné par le résidu rouvre le gel, et se voit en T7, §6.2) | `regeler` ne passe que si un « contourner » est consigné depuis le dernier gel ; il relève de nouvelles empreintes et remet à zéro les compteurs de la garde | `harnais.py regeler` |

### 6.1 Les commandes du pilote se refusent d'elles-mêmes (E13)

Le hook reconnaît un appel à sa **forme** : la chaîne de la commande du manifeste, ou le nom du script (ou du module) suivi, dans la même commande simple, d'un mot du pilote (guillemets et antislash ôtés). Une autre forme lui échappe : un chemin construit, une variable qui porte le mot, un script copié sous un autre nom, `python3 -c "import harnais; …"`, `runpy`. **Le refus des commandes du pilote ne repose donc pas sur le hook, ni sur la forme de l'appel.** Il tient à deux choses :

1. **L'outil exige de tenir le scellé du sujet.** `sceau`, `suite`, `contre-verif`, `geler`, `regeler`, `juge`, `ouvrir` et `empreintes` demandent que `IX_SCELLE_DIR` désigne le dossier où `lancer` a écrit un jeton dont la **garde** (au scellé) garde le sha256, et que ce dossier soit celui que les hooks déclarés au gel désignent. La session de production ne reçoit pas la variable. Le sha256 du jeton n'est plus dans `.harnais/etat.json` ni dans aucun fichier du sujet : un faux dossier de scellé, un faux jeton et une référence récrite dans l'état ne font plus de l'appelant le pilote (essayé : `PilotProofTests`, l'essai de forge du relecteur du tour 1). Un faux scellé **complet** (index, garde et jeton qui s'accordent) est refusé parce que les hooks déclarés au gel désignent le vrai ; le récrire demande de récrire les réglages, qui sont fermés (§6.2).
2. **Ce qu'une commande du pilote change vit au scellé.** `suite` relève la limite dans la garde, que les hooks lisent ; les empreintes qui font foi sont la copie du scellé ; `pilote.json` garde ce que seul le pilote écrit dans l'état. Une copie de l'outil dont on aurait retiré le contrôle du jeton, lancée sans le scellé, n'a rien où écrire : le plafond que les hooks appliquent ne bouge pas (essayé : `test_a_copy_of_the_tool_without_its_own_guard_changes_nothing_the_hooks_apply`).

Pour un appelant qui ne tient pas le scellé, le refus ne dépend donc ni de la chaîne de la commande, ni du chemin du script, ni de l'interpréteur, ni de la façon dont l'outil est importé ou copié. Le hook garde son rôle de premier message, en clair, pour les formes qu'il connaît.

**Ce que le jeton ne couvre pas.** Une session qui détiendrait déjà `IX_SCELLE_DIR`, ou qui atteindrait le scellé par le résidu de §6.2, est le pilote pour l'outil : ce geste a sa ligne dans le tableau de §6.2, avec son détecteur et son moment.

**La suite consignée vit dans `.harnais/etat.json` (un affichage) et dans la garde (ce qui s'applique).** L'état peut être écrit par la production ; la garde non, sauf par le résidu. Ce que le pilote y met est recopié au scellé (`pilote.json` pour les suites, les drapeaux, le gel ; `garde.json` pour la limite de tours et les drapeaux). `empreintes`, `juge`, `ouvrir`, `suite`, `regeler` et `geler` refusent au premier écart entre l'état et ces copies (« l'état a été modifié autrement que par les commandes du pilote », « écart de compteur »). Une suite ou des tours ajoutés à la main dans l'état **ne changent aucun plafond** (les hooks lisent la garde) et sont vus au geste suivant du pilote.

### 6.2 Ce que le hook refuse, le résidu, et ce qui le détecte

**Ce que le hook refuse, par chemin.** Une fois le sujet gelé, le hook connaît le scellé (D-L15) et refuse à la production :
- `Read` d'un chemin du dossier des scellés (le parent du scellé du sujet : il tient tous les scellés, leurs noms aussi) ; `Glob` et `Grep` dont le dossier est dedans, ou en est un parent (la recherche descendrait dedans), ou dont le motif, une fois comparé composante par composante, peut y atteindre (`**/jeton`, `/…/s*/*/jeton`) ; les outils d'écriture ;
- les commandes shell dont un mot, une fois les `~`, les variables d'environnement et les jokers résolus, tombe dans le dossier des scellés (`cat`, `ls`, `cd`…), ou en est un parent sur lequel la commande descend (`find`, `grep -r`, `rg`, `ag`, `fd`, `ls -R`, `du`, `tree`, `tar`, `zip`, `rsync`, `cp -r`…), y compris celles qu'enferment `$( )`, les accents graves, les parenthèses et `sh -c '…'`, et un chemin que le hook ne sait pas résoudre donné à `find`, `tree`, `du`, `tar`… ; `mdfind` et `locate`, qui cherchent partout sans chemin ;
- la lecture des réglages de projet (`.claude/settings.json`, `.claude/settings.local.json`), qui portent le pointeur : `Read`, `Glob`, `Grep`, et toute commande qui les nomme ou les désigne par joker ;
- l'écriture de ces mêmes réglages, du fichier qui déclare le hook, des fichiers figés, de `.harnais/`, du code du harnais ;
- **tout outil**, une fois le sujet gelé, tant que la garde n'est pas intacte, que le plafond n'est pas levé ou qu'un fichier figé a changé (O5, O10).

**Le résidu.** Un processus du même utilisateur système, lancé par la session de production, qui atteint la garde, le scellé ou les réglages par une forme que le hook ne sait pas résoudre : un interpréteur (`python3 -c`, `perl`, `node`, `awk`…) qui construit le chemin ou lit les réglages, le résultat d'une substitution, une variable que le hook ne connaît pas, un programme écrit puis lancé. **Le système ne le lui interdit pas** : c'est le même compte. Ce niveau est donc « interdit et détecté », non « empêché ». Chaque geste que ce processus peut faire est dans le tableau qui suit, avec ce qui le détecte et le moment, ou « rien dans le harnais » :

| Ce que fait le processus | Détecté par | Quand | Éprouvé ? |
|---|---|---|---|
| récrire la garde **seule** ou le témoin seul : remettre un compteur à zéro, relever un plafond | la tête de la garde et le témoin (`garde.controle`), par les hooks | avant l'outil suivant, au début et à la fin du tour | essayé avec des événements d'essai (`CounterHookTests`) ; pas en session réelle |
| récrire l'état (`.harnais/etat.json`) : tours, suites, plafond | rien à détecter pour les hooks, qui ne le lisent pas : le plafond appliqué ne bouge pas ; `synchroniser` refuse un état qui annonce plus de tours que la garde, et recopie la garde | au geste suivant du pilote | essayé (`CounterHookTests`) |
| récrire la garde **et** son témoin d'un même geste (en retrouvant la garde) | **rien dans le harnais.** Contrôle du pilote **CP1** : comparer le nombre de lignes `tour n` de T3 au nombre d'événements `Stop` de la transcription de la session de production (dossier de transcriptions de Claude Code pour le dossier du sujet ; les rejugements y ont relevé des entrées `stop_hook_summary`) ; un écart (plus d'événements `Stop` que de lignes) dit que des tours ont été effacés de la garde | à chaque retour de la main, et au plus tard avant `fin-production`, avant `juge` et avant `ouvrir` | **CP1 non éprouvé : jamais fait**, et aucun code du harnais ne le fait. Le geste lui-même est joué et son absence de détection écrite dans un essai (`CounterHookTests`, `test_the_one_residual_…`) |
| fabriquer un faux scellé complet et faire pointer l'outil du pilote dessus | `exiger_pilote` (le scellé donné n'est pas celui que les réglages déclarent) ; récrire les réglages est détecté par `empreintes` (les hooks déclarés ne désignent plus le scellé) | à chaque commande du pilote ; à chaque `empreintes` | essayé (`PilotProofTests`) |
| lancer une commande du pilote (`suite`…) avec le vrai scellé, atteint par le résidu, ou par `IX_SCELLE_DIR` laissée dans l'environnement de la production | pour `suite` : la ligne de T7 qu'elle écrit (`décideur` : l'utilisateur git, qui est le même compte ; `date` : le jour), (l'outil écrit aussi `pilote.json` au scellé, mais un processus qui tient le scellé le récrit de la même façon : ce n'est pas un détecteur). Contrôle du pilote **CP3** : relire T7 et la comparer aux suites qu'il a lui-même consignées. Pour les autres commandes (`sceau`, `empreintes`, `contre-verif`, `geler`, `regeler`, `juge`, `ouvrir`) : **rien dans le harnais** ne dit qui les a lancées ; leur effet (un jugement ou une fin de production en T3, une ouverture en T9) est ce que le pilote reconnaît ou non à la lecture. `IX_SCELLE_DIR` laissée dans l'environnement : non détectée ; le pilote la prévient en vérifiant `env \| grep -c IX_SCELLE_DIR` avant de lancer la session (A7 §2) | CP3 : à chaque retour de la main, avant le geste suivant du pilote (donc avant toute nouvelle `suite` ou `fin-production`) ; la vérification de l'environnement : avant chaque lancement de la session | **non éprouvé : CP3 n'a jamais été fait** ; la ligne T7 est essayée, pas la comparaison |
| récrire un fichier figé **et** `.harnais/empreintes.sha256` **et** la copie du scellé, d'un même geste | **rien dans le harnais** : ni les hooks, ni `empreintes`, ni `juge` ne le voient, puisqu'ils comparent le fichier à ces deux copies | — | — |
| modifier un fichier figé puis le restaurer entre deux contrôles | non détecté : les hooks comparent avant chaque outil et à chaque début et fin de tour ; ce qui revient à l'identique entre deux de ces moments ne laisse pas d'empreinte différente | — | — |
| **lire** la part cachée ou le jeton | **rien dans le harnais** n'en voit le moment : une lecture ne laisse pas de trace, et `juge` ne compare rien de la sortie du producteur à la part cachée. Contrôle du pilote **CP2** : chercher dans la transcription de la session de production les noms du scellé (le sous-dossier du sujet et `index.json`) et le marqueur de la part cachée | à chaque retour de la main, et au plus tard avant `juge` et avant `ouvrir` (après l'ouverture, la part est versée au sujet et la recherche ne dit plus rien) | **non éprouvé comme outil** : le pilote l'a fait à la main au rejugement du tour 2 ; aucun code du harnais ne le fait |

**Le contrôle du pilote (CP1 à CP3).** Ces trois contrôles sont faits **par le pilote, à la main**, à chaque retour de la main (un plafond atteint, une session arrêtée) et au plus tard avant `fin-production`, `juge` et `ouvrir`. Ils ne sont pas dans le code du harnais, et le harnais ne les rappelle pas. Aucun n'a été éprouvé comme contrôle du harnais ; CP1 et CP3 n'ont jamais été faits. Une transcription que la session ne produit pas, ou dans un format qui change, les rend inopérants sans que le harnais le dise.

Pour passer de « interdit et détecté » à un empêchement, il faut un cloisonnement du système : un compte séparé qui possède le scellé, ou le **bac à sable de la commande Bash** de Claude Code (`sandbox.enabled`, `sandbox.filesystem.denyRead` sur le dossier des scellés, `allowUnsandboxedCommands: false`, d'après la documentation de Claude Code), que le système applique, quelle que soit la forme de la commande. C'est hors de B-a (révision 2B) et **non livré, non éprouvé** : il change ce que la production peut faire (réseau, écritures) et B n'a aucun essai de session réelle ; à examiner au premier passage réel (B-b) ou dans une partie à part. Même alors, les outils `Read`, `Glob` et `Grep` ne sont pas dans le bac à sable : ils restent refusés par le hook et par une règle de refus de lecture.

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
| A1 | Les plafonds de la production et de la correction sont comptés par le harnais, **par les hooks de Claude Code à chaque fin de tour**, sans que la production lance quoi que ce soit ; au plafond la boucle s'arrête, le tour suivant ne commence pas et aucun outil n'est permis ; un appel refusé de `tour` ne compte pas de tour | Must | decided (CB13) ; le moyen : rejugement du tour 1 et décision d'Amiel du 19/10/2026 |
| A2 | Le gel : empreintes relevées, vérifiées par les hooks avant chaque outil et chaque tour, écriture refusée, regel à tout retour en 2B | Must | decided (P2, P12) |
| A3 | Le scellé : hors de tout dépôt, dans le dossier de `IX_SCELLE_DIR`, sous un nom tiré au hasard, juge lancé d'un dossier neutre puis nettoyé, versement dans la trace à la fin du jugement | Must | decided (P10) |
| A4 | Le gel du livrable en fin de production : commit et étiquette | Must | decided (P5) |
| A5 | Le lancement du juge : refusé si le livrable a bougé depuis son étiquette ; sa sortie est rangée au scellé ; le constat du producteur nomme l'exigence de chaque ligne cachée en échec sans rien de son contenu | Must | decided (CB15) |
| A6 | `IX_SCELLE_DIR` est une entrée donnée à l'exécution au pilote, exportée pour ses commandes (amont compris) ; le harnais refuse de travailler si elle manque, si elle désigne un dossier dans un dépôt git ou sous un chemin que lit le producteur ; le code n'en contient aucune valeur. La session de production ne la reçoit pas et ne lance rien qui l'exige (D-L12). Le code n'en suggère aucun emplacement | Must | decided (CB15, rejugement du tour 1) |
| A7 | Le hook refuse l'écriture des fichiers figés, de l'état du harnais, des réglages qui déclarent des hooks, du fichier qui déclare le hook, la lecture, la liste et la recherche du scellé (`Read`, `Glob`, `Grep`, formes shell) et des réglages qui portent le pointeur, tout appel qui a la forme d'une commande du pilote, et tout outil quand la garde n'est pas intacte, que le plafond est atteint ou qu'un fichier figé a changé | Must | decided |
| A7b | Les commandes du pilote refusent tout appelant qui ne tient pas le scellé du sujet, quelle que soit la forme de l'appel ; la référence de leur jeton n'est dans aucun fichier du sujet ; ce qu'elles changent vit au scellé ; l'état modifié autrement que par elles est refusé au jugement, à l'ouverture et à la suite suivante | Must | decided (E13) |
| A8 | Les hooks sont livrés comme fichiers de la branche et ne sont installés dans aucune configuration de machine ni de session | Must | decided (LR3) |
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
| A1 | un sujet gelé, des fins de tour | le hook `Stop` (rien d'autre n'est lancé) | un tour compté à chaque fin de tour ; au plafond `continue: false`, `UserPromptSubmit` refuse, `PreToolUse` refuse tout outil ; après `suite … relancer N`, N tours de plus |
| A1 | un sujet gelé au plafond de tours | `CMD_TOUR` | refus, le compteur ne bouge pas |
| A1 | un sujet gelé, après le jugement | le hook `Stop` | compté à part, avec `tours_correction_max` |
| A1 | un compteur remis à zéro dans la garde seule ou dans le témoin seul | un outil, un début ou une fin de tour | refus de tout outil, tour refusé, boucle arrêtée ; la garde et le témoin récrits ensemble : non vu (§6.2) ; l'état récrit : sans effet sur le plafond, écrasé par la garde |
| A2 | un fichier figé modifié | `CMD_EMPREINTES`, `CMD_TOUR`, un hook | refus, le premier fichier en cause est nommé ; la boucle s'arrête, aucun outil jusqu'à la restauration |
| A2 | le hook, un fichier figé | un événement d'écriture | code 2 ; une écriture d'un autre fichier : code 0 |
| A2, P12 | aucun « contourner » consigné | `CMD_REGELER` | refus ; après un « contourner », nouvelles empreintes et compteurs remis à zéro |
| A3 | un juge qui rend une ligne cachée en échec | `CMD_JUGE` | le constat nomme l'exigence, jamais la preuve ; la sortie est au scellé ; une ligne de T3 d'étape 5 est écrite |
| A4, A5 | un livrable modifié après son étiquette | `CMD_JUGE` | refus |
| A6 | `IX_SCELLE_DIR` absente, dans un dépôt git, ou sous le dossier du sujet | une commande autre que `fin-production` | refus, aucune valeur par défaut |
| A7 | un événement `Bash` qui lance `CMD_SCEAU`, ou un mot du pilote derrière le nom du script, guillemets ôtés | le hook | code 2 |
| A7 | `Read`, `Glob`, `Grep` sur le scellé, son parent ou un motif qui l'atteint ; `find "$TMPDIR" -name jeton`, `grep -r … /`, `cat …/*/jeton`, `mdfind`, `sh -c '…'` ; la lecture des réglages | le hook | code 2 ; les lectures et recherches ordinaires du sujet : code 0 |
| A7b | le plafond de tours atteint ; un appelant sans `IX_SCELLE_DIR`, ou avec un dossier fabriqué, ou un scellé complet fabriqué | `suite tours_goal_max relancer 9` par le manifeste, par un chemin construit, par un script copié, par `python3 -c "import harnais…"`, par `runpy` | refus (« commande du pilote »), aucune suite ni aucun tour ajouté |
| A7b | une suite et des tours ajoutés écrits à la main dans `.harnais/etat.json` | `suite`, `empreintes`, `juge`, `regeler` ou `ouvrir` | refus (« ne correspond pas à ce que le pilote a scellé ») ; le plafond que les hooks appliquent n'a pas bougé |
| A7b, D-L14 | le faux scellé et la référence récrite dans l'état (l'essai de forge du relecteur) | `suite tours_goal_max relancer 9` | refus ; le plafond tient |
| D-L12 | un sujet gelé, un appelant sans `IX_SCELLE_DIR` | `tour`, `tour-correction` | refus (les tours sont comptés par les hooks) ; `fin-production` : accepté |
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
| Q4 | Tranchée (D-L12, D-L15) : `IX_SCELLE_DIR` reste hors de l'environnement de la session de production ; le hook refuse le scellé par son chemin, connu par le pointeur des réglages | — | — |
| Q5 | Le modèle de l'étape externe (Fable chez Amiel) n'est consigné dans la trace que si le pilote le donne (`IX_MODELE_EXTERNE`) : sinon `n.c.` | non | Amiel |
| Q6 | Tranchée par Amiel le 19/10/2026 (révision 2B de la ligne 55) : O5, O10 et O11 sont au niveau **« interdit et détecté »**, non « mécanisme qui empêche » ; un vrai empêchement demande une isolation par le système, hors de B-a (§6). Reste à confirmer dans une vraie session `/goal` que `Stop` compte chaque tour et qu'un `continue: false` arrête la boucle, à faire une première fois les contrôles CP1 à CP3 (§6.2), et à décider si le bac à sable de Bash ferme le résidu | non | Amiel, à B-b |

## 11. Décisions laissées au pilote

La version du plugin, la version de la page de suivi et le CHANGELOG ne sont pas touchés par B : le pilote les fait à la livraison, avec le commit et l'étiquette `b-a-livrable`. La copie de `build.py` d'ix-skills n'est pas mise à jour (CB20).
