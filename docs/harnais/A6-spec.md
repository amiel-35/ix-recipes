---
status: draft
piece: A6, volet « spec » (le volet « architecture » est dans A6-architecture.md)
format: spec fonctionnelle, au format du skill feature-spec d'ix-recipes (format de ce document seulement, pas une valeur d'association)
sources: trace/01e-cadrage-clos.md (« 01e ») ; corpus/procedure-traitement-sujet.md ; les pièces A1 à A5, A7, A8 telles que lues ; trace/02b-criteres.md, section « Issue visée »
---

# A6 : spec fonctionnelle des pièces sans harnais (partie A)

Volet « spec » de A6. Le volet « architecture » est dans `partie-a/A6-architecture.md`.

## 0. Découpage de ce sujet

Le sujet « A6 » est livré en deux documents, parce que la spec décide **ce que fait chaque pièce et ce qu'elle exige de ses voisines**, et l'architecture décide **comment les pièces et un harnais s'assemblent** :

| Volet | Contenu | Écrit par |
|---|---|---|
| **Spec (ce document)** | Pour A1 à A8 : ce que fait la pièce, ses entrées, ses sorties, l'étape qui la lit ou l'écrit, ses exigences et leurs critères d'acceptation. Où vit l'association « type de sujet → skills de format ». Ce que la spec exige d'un harnais futur **au niveau de l'interface**. | ce document |
| **Architecture** | Composants et flux des pièces. | `partie-a/A6-architecture.md` |

Périmètre de la spec (lecture retenue LR1 de 01e) : les pièces et leurs interfaces. **Pas** l'architecture d'un harnais, qui revient à la partie B, après le bilan du passage (01e, D1, D14).

## 1. Résumé

La partie A livre huit pièces qui permettent de mener à la main, sans harnais, un sujet de code de façon reproductible (même déroulé) et auditable (une trace par sujet). Cette spec compte 76 exigences, dont 52 Must, 13 Should, 3 Could et 8 Won't. Elle ne pose aucune question bloquante, ni pour la partie A ni pour le constructeur de la partie B ; les questions encore ouvertes (section 10) se règlent avant le prochain sujet de code. Les questions que la rédaction de la spec a fait apparaître sur les autres pièces ont été closes pendant la production, en corrigeant ces pièces (section 10).

## 2. Problème et objectifs

**Problème.** Traiter un sujet de bout en bout reposait sur la mémoire d'Amiel et sa présence. Deux étapes de la procédure n'avaient pas de méthode écrite (clore un cadrage, rédiger un goal), le jugement du cadrage n'avait pas de grille fixe, et rien ne disait où consigner ce qui s'était passé, ni quels réglages appliquer (01e, §1). Volume et fréquence : un seul passage réel à ce jour (celui qui produit la partie A) ; fréquence de traitement des prochains sujets : à mesurer.

**Objectifs** (des résultats, pas des livrables ; 01e, §1) :
1. Un passage se mène à la main, avec les mêmes étapes, entrées, modèles, skills et plafonds, et laisse une trace consultable à chaque étape (issue O1).
2. Les utilisateurs d'ix-skills, dont la recette `brief-client`, ne perdent rien du fait du nouveau mode de `cadrage` (O2).
3. Le constructeur de la partie B sait, sans poser de question à Amiel, ce que le harnais doit lire et écrire (O3).
4. Un client lit la trace de son sujet, et seulement la sienne, sans aide (O4).

**Hors du but, comme dans la demande** : produire un meilleur livrable.

## 3. Périmètre

**Dans la spec.** Les huit pièces A1 à A8 ; l'enchaînement des étapes 0 à 7 vu depuis les pièces ; la localisation de l'association type → skills de format ; l'exigence d'interface posée à un harnais futur.

**Hors périmètre (non-objectifs), chacun avec sa raison :**

| Non-objectif | Raison |
|---|---|
| Choisir ou décrire un harnais (enchaînement automatique, mise en forme d'un suivi, installation d'un gel) | Le harnais est choisi après le bilan du passage (01e, D1, D14). Une pièce peut nommer ce qu'un harnais doit faire, jamais comment (C1). |
| Les trois autres types de sujets (réponse commerciale, audit UX, formation) | Partie C (D3). Seul « code » est rempli dans A4. |
| Comment un client sans Claude Code **mène** un sujet | Relève du harnais, donc de B (LR2). Dans A, le client est un lecteur. |
| L'étape 7 (terrain) comme mécanisme outillé, et les sujets enfants gérés par la procédure | Hors périmètre confirmé (D14, D12). La trace garde seulement le renvoi aux sujets enfants (A3, T8). |
| Mesurer si la procédure donne de meilleurs livrables que d'autres, ou si Fable apporte plus qu'Opus | Hors du but (01e, §1 et §5.2). |

Toute exigence ajoutée plus tard retire une exigence ou décale la livraison.

## 4. Utilisateurs et histoires

| # | Histoire |
|---|---|
| U1 | En tant que **pilote d'un sujet de code** (Amiel, premier utilisateur), je veux dérouler les étapes 0 à 7 avec des pièces qui me disent quoi lire, quoi écrire et quoi décider, afin de ne rien inventer à la main. |
| U2 | En tant qu'**agent qui clôt un cadrage (étape 1e)**, je veux une méthode écrite et une grille à tenir, afin que mon cadrage clos permette d'écrire un goal et des critères sans reposer de question. |
| U3 | En tant qu'**agent qui rédige un goal (étape 2A)**, je veux recevoir un cadrage clos, des réglages et des skills de format, et ne pas voir les critères, afin d'écrire pour l'intention et pas pour la grille. |
| U4 | En tant qu'**auditeur (Amiel, ou un client pour son seul sujet)**, je veux retrouver pour une étape donnée l'entrée, la sortie, le modèle, la durée, les jetons et le coût avec sa source, afin de vérifier ce qui a été fait. |
| U5 | En tant que **mainteneur (Amiel)**, je veux changer un plafond, un modèle ou un skill de format en ne touchant qu'un fichier, afin de recaler la procédure après un essai sans casser les autres pièces. |
| U6 | En tant que **constructeur de la partie B**, je veux que la spec me dise ce qu'un harnais doit lire, écrire, sceller et geler, afin de choisir et construire un harnais sans réinterroger Amiel. |
| U7 | En tant qu'**utilisateur de la recette `brief-client`**, je veux que `cadrage` continue de rendre ce qu'elle rend aujourd'hui, afin que ma recette ne casse pas. |

## 5. Les pièces : fonction, entrées, sorties, étape

Les valeurs de réglage ne sont jamais recopiées ici : on renvoie à la clé d'A4 (`partie-a/A4-reglages.yaml`).

### 5.1 Fiche de chaque pièce

**A1. Mode `close` de `cadrage`** (ix-skills, branche dédiée)
- *Fait.* Ajoute au skill `cadrage` un second mode, choisi par le message : il transforme un cadrage soumis et les réponses données à la pause en un cadrage clos, dont on peut écrire un goal et des critères sans rien redemander.
- *Entrées.* Cadrage soumis (requis) ; réponses à la pause (requis) ; demande d'origine et sources citées (optionnelles, pour vérifier un fait, jamais pour rouvrir une décision) ; grille de référence (optionnelle ; en 1e c'est A5) ; tests de découpage (optionnels, quatre par défaut).
- *Sortie.* Un cadrage clos en douze sections, dans cet ordre : Intention ; Audience and situation of use ; Decisions ; Constraints with their rationale ; Scope ; Stakeholders ; Deliverables ; Remaining assumptions as accepted risks ; Splitting tests replayed ; Ready for the next step ; Retained readings ; Residual question. En tête : les entrées utilisées et la règle de priorité (la réponse prime sur le défaut).
- *Étape.* Lue à **1e** (clôture). Le mode par défaut, lui, est lu à **1a**.

**A2. Skill « rédiger un goal »** (ix-skills, même branche, id `goal-writing`)
- *Fait.* Rédige le goal d'un agent qui travaillera seul : le contenu d'un goal, pas la commande d'un outil.
- *Entrées.* Cadrage clos (requis) ; réglages (requis : plafond de tours, modèle de chaque rôle, limites des sous-agents, suites offertes à un plafond, gel du script et de la grille) ; skills de format par livrable (requis) ; noms de valeurs fixées plus tard (optionnels). **Ne sont pas des entrées** : les critères, la grille, tout ce qui est scellé.
- *Sortie.* Un goal (intention ; livrables avec lecteur, lieu d'écriture, skill de format reçu ; contraintes et interdits ; autorisations ; condition d'arrêt qui renvoie au script de recette par un emplacement nommé ; plafond de tours ; conduite au plafond ; ce qu'il faut tracer ; valeurs fixées plus tard) et des notes du rédacteur, hors goal (lacunes avec l'option la plus étroite, entrées ignorées, emplacements utilisés).
- *Étape.* Écrite à **2A** (modèle : clé `modeles.redaction_goal`), vérifiée à 2A (clé `modeles.verification_goal`, `critique` avec angles imposés). Lue par **3** (réconciliation) et par **4** (production).

**A3. Format de trace** (ix-pilote)
- *Fait.* Définit la trace d'un sujet : Markdown, onze tableaux T1 à T11 aux titres fixes et aux colonnes nommées, un champ par colonne. T1 sujet ; T2 plafonds appliqués ; T3 étapes ; T4 skills ; T5 sous-agents ; T6 pauses et décisions ; T7 plafonds atteints et suites ; T8 sujets enfants ; T9 gel et scellés ; T10 lancements du script de recette ; T11 points à confirmer et écarts.
- *Entrées (à l'usage).* Pour chaque étape : ce qu'elle a reçu et produit, le modèle, les mesures de l'outil, les skills avec version et empreinte, la version et l'empreinte d'A4.
- *Sortie.* Une trace par sujet, dans le dossier du sujet, lisible sans Claude Code et exploitable par un programme.
- *Étape.* **Écrite** à l'étape 0 (ouverture : T1 et première ligne de T3) puis à chaque étape ; **lue** pour auditer, pour rejouer, par un client (pour son sujet), et par le harnais de B.

**A4. Fichier de réglages** (ix-pilote)
- *Fait.* Seul endroit où s'écrit une valeur de réglage. Une clé `version` à la racine ; `plafonds` ; `production` ; `gel` ; `modeles` (dont `sous_agents_verification` et `contre_verification`) ; `suites_au_plafond` et `definition_des_suites` ; `sujets_enfants` ; `types_de_sujet` (une entrée par type, seul `code` rempli).
- *Entrées.* Aucune au sens d'un flux : il est édité par le mainteneur, hors passage.
- *Sorties.* Les valeurs lues par les étapes (voir 5.2).
- *Étape.* **Lu** à presque toutes les étapes ; **écrit** seulement par le mainteneur (A8).

**A5. Grille fixe du cadrage** (ix-pilote)
- *Fait.* Neuf règles, G1 à G9, valables pour tous les sujets, qu'on juge conformes ou en infraction avec `controle-qualite` en mode `verdict` ; l'en-tête dit qui l'applique, quand, avec quel skill.
- *Entrées.* Le cadrage à juger (livrable) ; la grille est le référentiel.
- *Sorties.* Un verdict par point.
- *Étape.* **Lue** à **1d** (sept points avant la pause 1 ; G3 et G9 ne s'appliquent pas), par l'auteur de **1e**, qui écrit pour la tenir, et par un agent distinct qui applique les neuf points au cadrage clos.

**A6. Spec et architecture des pièces** (ix-pilote)
- *Fait.* Ce document et son volet architecture : ce que fait chaque pièce, ce qu'elle lit et rend, quelle étape la lit ou l'écrit, où vit l'association type de sujet → skills de format, et le contrat qu'un harnais devra tenir.
- *Entrées.* Les pièces A1 à A5, A7, A8, le cadrage clos, la procédure.
- *Sortie.* Le dossier de conception (spec ; architecture).
- *Étape.* Aucune étape d'un passage ne la lit. Elle est **lue au cadrage de la partie B** (par Amiel et le constructeur), et **mise à jour** quand une pièce change.

**A7. Guide d'usage** (ix-pilote, deux fichiers)
- *Fait.* Explique comment mener un sujet de code à la main : étapes 0 à 7, réponses aux pauses, choix d'une suite à un plafond. Un texte à part, « lire une trace », se lit seul.
- *Entrées.* A3, A4, A5 et les skills nommés par la procédure.
- *Sorties.* Aucune pièce de passage ; un lecteur qui sait agir.
- *Étape.* **Lu** par le pilote avant et pendant le passage, et par un client pour sa trace (partie « lire une trace » seule).

**A8. Note de maintenance** (ix-pilote)
- *Fait.* Où vit chaque pièce (deux dépôts) ; comment changer un plafond, un modèle, un skill de format ; comment publier un skill d'ix-skills ; ce qui migrera à la partie B ; le renvoi depuis le `README.md` d'ix-pilote.
- *Entrées.* Les règles de publication d'ix-skills ; A4.
- *Sorties.* Aucune pièce de passage.
- *Étape.* Aucune étape ne la lit. Lue par le **mainteneur** entre deux passages.

### 5.2 Qui lit ou écrit quoi, étape par étape

| Étape | Pièces lues | Pièces écrites | Clés d'A4 concernées |
|---|---|---|---|
| 0 Brief | A3, A4 | T1, première ligne de T3 | `version` |
| 1a Cadrer | A1 (mode par défaut), A4 | ligne T3, T4 | `modeles.cadrage_et_criteres` |
| 1b Questionner | A4 | ligne T3, T4 | `modeles.cadrage_et_criteres` |
| 1c Taille | A4 | ligne T3, T4, éventuellement T8 | `modeles.cadrage_et_criteres` |
| 1d Évaluation | A5, A4 | ligne T3, T4 | `modeles.evaluation_cadrage`, `plafonds.passes_verification_max`, `suites_au_plafond.passes_verification` |
| Pause 1 | — | T6 (T7 si un plafond est atteint) | — |
| 1e Clôture | A1 (mode `close`), A5, A4 | ligne T3, T4 | `modeles.cadrage_et_criteres` |
| 2A Goal | A2, A4 | ligne T3, T4 | `plafonds.tours_goal_max`, `modeles.redaction_goal`, `modeles.verification_goal`, `production.*`, `gel.*`, `suites_au_plafond.tours_goal`, `types_de_sujet.<type>.skills_de_format` |
| 2B Critères | A4 (le skill de critères n'est pas une pièce de A) | ligne T3, T4, T5 | `modeles.cadrage_et_criteres`, `modeles.contre_verification`, `types_de_sujet.<type>.annexes_criteres` |
| 3 Réconciliation | A4 | ligne T3 | `modeles.reconciliation` |
| Pause 2 | — | T6 | — |
| Gel | A4 | T9 | `gel.*` |
| 4 Production | goal (issu d'A2), A4, A3 (pour tracer) | T3 (session), T4, T5, T10 ; T7 si plafond | `production.*`, `modeles.production`, `modeles.sous_agents_lecture`, `plafonds.tours_goal_max` |
| 5 Jugement | A4, A3 | T3 (étape), T5, T9 (trace du juge scellée) | `modeles.juge`, `modeles.nouveau_venu` |
| 6 Correction | A4, A3 | T3 (session), T10, T7 si plafond | `plafonds.tours_correction_max`, `suites_au_plafond.tours_correction` |
| 7 Terrain | aucune pièce de A | aucune | — |

Vérification de A5 par le modèle de contre-vérification : après la production et avant le juge (clé `modeles.contre_verification`, accord demandé au pilote).

### 5.3 L'association « type de sujet → skills de format »

- **Elle vit dans A4**, sous `types_de_sujet.<type>` : `skills_de_format` (un skill par genre de livrable : spécification, architecture, documentation), `skills_facultatifs`, `annexes_criteres`. Pour le type « code » seul. Les trois autres types portent `statut: "partie C"`.
- **A6 la décrit** (ici) et renvoie à la clé ; A6 ne recopie pas les identifiants de skills comme valeurs, pour qu'un changement d'A4 ne laisse pas une valeur périmée ailleurs (A8, §3).
- **Aucun skill d'ix-skills ne nomme un skill d'ix-recipes** (C9). Concrètement : A1 prévoit une ligne « spec et architecture » sans dire qui la produit ; A2 reçoit les skills de format **en entrée** et ne choisit, n'ajoute ni ne retire aucun skill.
- **Qui fait le pont** : le pilote (à la main) ou un harnais lit A4 et assemble, pour chaque livrable du cadrage clos, la liste « livrable → skill de format » qu'il remet à A2. Comment il range un livrable dans un genre (clé de `skills_de_format`) n'est écrit nulle part : voir Q5.

## 6. Exigences

Étiquettes : **decided** (avec sa source), **hypothesis**, **proposed** (à confirmer, par qui). Sigles : 01e = `trace/01e-cadrage-clos.md` ; C, D, LR, RA = contrainte, décision, lecture retenue, risque accepté de 01e ; « Amiel, pause 2 » = décisions consignées dans l'en-tête de `trace/02b-criteres.md`.

Aucun Must n'est une hypothèse. Le seul Must non validé est écrit « Must (proposed, to confirm) » (X5).

### 6.1 Transversales

| ID | Exigence | MoSCoW | Label | Source / responsable |
|---|---|---|---|---|
| X1 | Aucune pièce ne suppose un harnais. Une pièce peut nommer ce qu'un harnais devra faire (geler un fichier, écrire une ligne de trace), jamais comment. | Must | decided | C1 ; D1, D14 |
| X2 | Aucun skill d'ix-skills ne nomme un skill d'ix-recipes. L'association type → skills de format vit dans A4 seulement. | Must | decided | C9 ; règle de dépendance d'ix-skills |
| X3 | A1 et A2 sont produits dans ix-skills sur une branche à elle, au format d'ix-skills, sans fusion dans `main` ; la fusion revient à Amiel. | Must | decided | C11, C12, LR6 |
| X4 | A3 à A8 vivent dans ix-pilote, hors de `trace/` et de `corpus/` ; `corpus/` n'est pas modifié. | Must | decided | 01e §7, règle de placement |
| X5 | Chaque élément que le goal demande au producteur de consigner a une place dans A3 (les points « à confirmer », les chemins hors périmètre et les écarts au cadrage vont en T11). | Must | decided | skill `goal-writing`, « What to trace » ; A3 T11 |
| X6 | Les pièces d'ix-pilote sont écrites en français. | Should | decided | RA10 (risque accepté) |
| X7 | Les trois autres types de sujets (partie C). | Won't (cette fois) | decided | D3, C2 |
| X8 | Le choix et l'architecture d'un harnais, y compris comment un client sans Claude Code mène un sujet. | Won't (cette fois) | decided | D1, D14, LR1, LR2 |
| X9 | L'étape 7 comme mécanisme outillé ; des sujets enfants gérés par la procédure. | Won't (cette fois) | decided | D14, D12 |
| X10 | Viser un meilleur livrable ; mesurer Fable contre Opus. | Won't (cette fois) | decided | 01e §1 et §5.2 |

*Assurance d'architecture (X8, X9)* : A3 garde la table T8 et la colonne `sujet_parent` pour ne pas fermer la porte aux sujets enfants ; A4 garde une entrée par type pour ne pas fermer la porte à la partie C.

### 6.2 A1, mode `close` de `cadrage`

| ID | Exigence | MoSCoW | Label | Source |
|---|---|---|---|---|
| A1-1 | Sur un message qui demande de clore, avec un cadrage soumis et les réponses à la pause, A1 rend un cadrage clos aux douze sections de 5.1, dans l'ordre, chacune non vide ou disant pourquoi elle l'est, avec en tête les entrées utilisées et la règle de priorité. | Must | decided | 01e §7 A1 |
| A1-2 | Le mode est choisi par le message. Sans demande de clore, `cadrage` se comporte comme avant (même méthode, même format), et reste utilisable par `brief-client`. La version monte d'un cran mineur. | Must | decided | C10 ; semver d'ix-skills |
| A1-3 | A1 énonce les trois règles de clôture : la réponse de pause prime sur le défaut et devient une décision qui la cite ; un défaut accepté sans remarque est marqué « défaut accepté » et rappelé au décideur ; une question bloquante restée sans réponse devient la question résiduelle, avec la raison pour laquelle elle bloque ou non. | Must | decided | 01e, en-tête et §3 |
| A1-4 | Quand le sujet construit un outil ou un système, la section des livrables contient une ligne « spec et architecture » avec son lecteur ; sinon elle dit pourquoi. Elle ne dit jamais quel skill produit un livrable. | Must | decided | C9, LR5, D9 |
| A1-5 | Le cadrage clos que A1 rend tient A5 : chaque point G1 à G9 a sa section dans la sortie, et le jugement après la pause ne donne aucune infraction. | Must | decided | 01e §7 A1 et A5 |
| A1-6 | Quand les réponses sont muettes et que le cadrage soumis n'a pas de défaut, A1 n'invente aucune décision : il prend l'option qui engage le moins, marquée « à confirmer » ; une réponse à deux lectures devient une lecture retenue avec l'alternative et la raison. | Should | decided | skill `cadrage`, mode `close` |
| A1-7 | A1 rejoue les tests de découpage (les quatre par défaut, ou ceux du message) un par un, avec un verdict (vrai, faux, en partie vrai) et sa raison ; un test conditionnel dans le cadrage soumis reçoit son verdict définitif. | Should | decided | skill `cadrage` ; 01e §9 |
| A1-8 | Rouvrir une décision de la pause, ou en ajouter une que les réponses ne soutiennent pas. | Won't | decided | skill `cadrage`, contraintes du mode |

### 6.3 A2, skill « rédiger un goal »

| ID | Exigence | MoSCoW | Label | Source |
|---|---|---|---|---|
| A2-1 | A2 prend un cadrage clos, des réglages et les skills de format par livrable. Les critères, la grille et tout ce qui est scellé ne sont pas des entrées ; si le message en fournit, A2 les ignore et le dit dans les notes du rédacteur. | Must | decided | 01e §7 A2 ; D5 |
| A2-2 | Le goal rendu contient : valeurs fixées plus tard ; intention ; livrables (chacun avec son lecteur, son lieu d'écriture, son skill de format reçu ou « aucun skill de format ») ; contraintes et interdits ; autorisations ; condition d'arrêt ; plafond de tours ; conduite au plafond ; ce qu'il faut tracer. | Must | decided | 01e §7 A2 ; skill |
| A2-3 | La condition d'arrêt renvoie au script de recette par son emplacement nommé, sans dire ce qu'il vérifie, et ne contient aucun critère ni seuil hors le plafond de tours, qui égale la valeur de la clé `plafonds.tours_goal_max` au moment de la rédaction. Le goal interdit de modifier le script ou la grille. | Must | decided | 01e §7 A2, C14 ; D10 |
| A2-4 | Toute autorisation de sous-agent porte un modèle explicite pris dans les réglages selon le rôle ; le livrable s'écrit sur un seul fil, jamais par un sous-agent. | Must | decided | C13 ; 01e §10 |
| A2-5 | A2 décrit le contenu d'un goal ; il ne donne la syntaxe d'aucune commande, option ou format d'un outil, sauf comme exemple signalé. | Must | decided | RA7 |
| A2-6 | Les skills de format cités dans le goal viennent tous de l'entrée : A2 n'en choisit, n'en ajoute et n'en retire aucun, et ne nomme aucun skill d'ix-recipes dans son propre texte. | Must | decided | C9 |
| A2-7 | Si un emplacement nommé n'est pas rempli au départ, le goal dit au producteur de ne rien produire et de rendre la main avec la raison. | Should | decided | skill `goal-writing` |
| A2-8 | Chaque lacune du cadrage clos est listée à part avec l'option la plus étroite retenue, marquée « à confirmer ». | Should | decided | skill `goal-writing` |
| A2-9 | Écrire les critères ou le script de recette, ou choisir un skill de format. | Won't | decided | skill `goal-writing` ; 01e §10 |

### 6.4 A3, format de trace

| ID | Exigence | MoSCoW | Label | Source |
|---|---|---|---|---|
| A3-1 | Une trace par sujet, en Markdown, avec les tableaux T1 à T11 aux titres fixes, aux colonnes nommées, un champ par colonne ; lisible sans Claude Code ni programme, exploitable par un programme sans heuristique. | Must | decided | C7, LR2 ; Amiel, pause 2 |
| A3-2 | La trace consigne, par ligne d'étape : entrée, sortie, modèle, durée, jetons, coût et source du coût ; pour chaque skill utilisé : version et empreinte ; pour le sujet : version des réglages, empreinte d'A4 et plafonds appliqués. De quoi rejouer le même déroulé. | Must | decided | C3, C5 ; D4 |
| A3-3 | Le coût porte toujours sa source : `mesuré`, `estimé` (avec la méthode, la date du tarif et ce qu'on ignore) ou `n.c.` (avec la raison). Une estimation ne se présente jamais comme une mesure. | Must | decided | C4 ; D6 |
| A3-4 | Trois granularités : `appel` aux étapes 0 à 3 ; `session` aux étapes 4 et 6 (durée et jetons relevés, coût estimé) ; `étape` à l'étape 5. Les sous-agents d'une session ou d'une étape sont listés en T5 avec leur modèle, sans coût individuel. | Must | decided | D6, LR3 |
| A3-5 | La part cachée et la trace du juge ont une place scellée : tant qu'elles sont scellées, la trace ne porte que leur empreinte et pas leur chemin ; à la fin du jugement elles passent à `ouvert` et entrent dans la trace complète. | Must | decided | D5, C6 |
| A3-6 | Aucune copie hors du dossier du sujet, aucun renvoi à une pièce d'un autre sujet ; seul le nom du dossier d'un sujet enfant est permis (T8). | Must | decided | C7 ; D12, D13 |
| A3-7 | La première ligne de T3 est l'étape 0 : la demande, séparée des pièces. | Must | decided | 01e §7 A3 |
| A3-8 | Une valeur absente s'écrit `n.c.`, `inclus dans la session` ou `sans objet`, avec la raison ; jamais une cellule vide, jamais une valeur inventée. | Must | decided | Amiel, pause 2 (forme de A3) |
| A3-9 | Les décisions de pause (T6) disent leur source (`réponse`, `défaut accepté`, `confirmé en bloc`), le décideur, la date et si elles sont à rappeler ; chaque plafond atteint (T7) porte le constat, les suites proposées, la suite choisie et ses détails (tours ajoutés, dérogation, réserve). | Must | decided | D8, LR4 ; 01e §3 |
| A3-10 | T10 consigne chaque lancement du script de recette pendant la production et la correction ; le nombre de vérifications ne baisse jamais d'un lancement à l'autre. | Should | decided | skill `goal-writing` (condition d'arrêt) ; A3 |
| A3-11 | A3 décrit la lecture par programme : trouver le titre T3, lire les noms de colonnes, choisir la ligne par `étape` et `occurrence` ou par `ligne`, lire le modèle et le coût avec sa source. | Should | proposed (à confirmer : Amiel) | A3, §6 |
| A3-12 | La trace peut tenir en plusieurs extraits (un par phase) qui suivent les mêmes titres et colonnes. | Could | decided | A3, §1 |

### 6.5 A4, fichier de réglages

| ID | Exigence | MoSCoW | Label | Source |
|---|---|---|---|---|
| A4-1 | Un seul fichier YAML commenté, avec une clé `version` à la racine, qu'un programme charge. | Must | decided | C8, D7 ; Amiel, pause 2 (forme d'A4) |
| A4-2 | Il contient chaque valeur de C8 : les trois plafonds, le mode de production, le gel du script et de la grille, le modèle de chaque rôle (dont la contre-vérification, chez Amiel et ailleurs, et l'accord demandé), les suites à chaque plafond, l'absence de sujets enfants. | Must | decided | C8 ; D7, D8, D10, D11, D12 |
| A4-3 | Chaque valeur est commentée : ce qu'elle règle, d'où vient sa valeur. | Must | decided | 01e §7 A4 ; D7 |
| A4-4 | Une entrée par type de sujet ; seul « code » est rempli (skills de format, skills facultatifs, annexes de critères) ; les trois autres portent « partie C ». | Must | decided | C2, D3 |
| A4-5 | « Contourner » n'est offert qu'aux plafonds qui suivent le jugement (tours de correction) et au plafond des tours du goal ; au plafond des passes de vérification, trois suites sont offertes. Le nombre de tours de « relancer » n'est pas un réglage : le pilote le fixe et il est tracé. | Must | decided | D8, LR4 |
| A4-6 | Une valeur de réglage s'écrit dans A4 et nulle part ailleurs. Les autres pièces renvoient à la clé. Seule exception : la trace copie la valeur appliquée au lancement (T2). | Must | decided | C8, D7 ; A4, en-tête |
| A4-7 | Règle de version : majeure si une clé change de sens ou disparaît, mineure si une clé s'ajoute, correctif si seule une valeur change. | Should | proposed (à confirmer : Amiel) | A4 |
| A4-8 | Un skill facultatif peut s'ajouter sous `skills_facultatifs` (la maquette est notée « à confirmer »). | Could | proposed (à confirmer : Amiel) | A4 ; procédure |
| A4-9 | Un plafond en dollars ou une échéance. | Won't | decided | D10 |

### 6.6 A5, grille fixe du cadrage

| ID | Exigence | MoSCoW | Label | Source |
|---|---|---|---|---|
| A5-1 | Neuf règles G1 à G9, chacune au sens du point de la procédure, sans l'affaiblir, avec ses critères conforme, infraction, douteux ; valables pour tous les sujets. | Must | decided | 01e §7 A5 ; procédure |
| A5-2 | L'en-tête dit qui l'applique, quand et avec quel skill (`controle-qualite`, mode `verdict`) et, pour chaque point, s'il s'applique avant la pause 1 : G3 et G9 ne s'appliquent qu'après. | Must | decided | 01e §7 A5 ; 01d |
| A5-3 | Le point sur les livrables (G7) couvre la spec et l'architecture quand le sujet s'y prête, et exige une raison écrite sinon. | Must | decided | LR5 |
| A5-4 | A5 est relue une fois par le modèle de contre-vérification, après accord du pilote, et dit où en est cette relecture. | Must | decided | C13, D11 ; Amiel, pause 2 |
| A5-5 | Dans chaque verdict, le juge sépare ce qui attend la pause 1 de ce qui est un défaut corrigeable. | Should | decided | A5, en-tête |
| A5-6 | Rendre un verdict d'infraction sur G3 ou G9 avant la pause 1. | Won't | decided | A5 ; 01d |

### 6.7 A6, spec et architecture des pièces

| ID | Exigence | MoSCoW | Label | Source |
|---|---|---|---|---|
| A6-1 | Pour chacune des pièces A1 à A8, A6 dit ce qu'elle fait, ses entrées, ses sorties et l'étape qui la lit ou l'écrit. | Must | decided | LR1 ; 01e §7 A6 |
| A6-2 | A6 dit où vit l'association type → skills de format (A4) et la décrit sans recopier les identifiants de skills comme valeurs. | Must | decided | C9 ; A8 §3 |
| A6-3 | A6 expose le contrat d'un harnais au niveau de l'interface : lire A4, écrire A3, sceller la part cachée, geler le script et la grille, sans dire comment. | Must | decided | LR1 ; D9 |
| A6-4 | La spec suit le format d'une spec fonctionnelle et l'architecture celui d'une conception de système, deux documents. | Should | decided | D9 |

### 6.8 A7, guide d'usage

| ID | Exigence | MoSCoW | Label | Source |
|---|---|---|---|---|
| A7-1 | Le guide dit comment mener un sujet de code à la main, de l'étape 0 à 7 : pour chaque étape la pièce lue, la pièce écrite, et qui agit aux pauses. | Must | decided | 01e §7 A7 ; D9 |
| A7-2 | La partie « lire une trace » se lit seule, sans le guide, sans Claude Code, sans autre document. | Must | decided | LR2 ; D13 |
| A7-3 | Le guide explique les réponses aux pauses, dont la règle du défaut accepté et de son rappel, et l'accord demandé avant la contre-vérification. | Must | decided | 01e §3 ; D11 |
| A7-4 | Le guide dit quelles suites s'offrent à chaque plafond et qui fixe le nombre de tours de « relancer ». | Must | decided | D8, LR4 |
| A7-5 | Le guide aide à choisir une suite (quand relancer, contourner, livrer avec réserve, abandonner). | Should | proposed (à confirmer : Amiel) | A7 |
| A7-6 | Le guide ne recopie aucune valeur d'A4. | Should | decided | A4, en-tête ; A8 §2 |
| A7-7 | Le guide signale le conseil de plusieurs voix comme option en pause 1. | Could | decided | procédure, étape 1 |

### 6.9 A8, note de maintenance

| ID | Exigence | MoSCoW | Label | Source |
|---|---|---|---|---|
| A8-1 | La note dit où vit chaque pièce, sur quel dépôt et quelle branche, et que la fusion d'ix-skills est à la main d'Amiel. | Must | decided | 01e §7 A8, LR6 |
| A8-2 | La note dit comment changer un plafond, un modèle ou un skill de format : en ne touchant qu'A4 et en montant sa version. | Must | decided | 01e §7 A8 ; C8 |
| A8-3 | La note dit comment publier un skill d'ix-skills (version, entrée au journal des changements, validation puis construction, dossier construit commité, versions du paquet, deux README) sans contredire les règles d'ix-skills. | Must | decided | 01e §7 A8 ; C11 |
| A8-4 | La note dit ce qui migrera à la partie B, et le `README.md` d'ix-pilote renvoie à elle. | Must | decided | 01e §7 A8 |
| A8-5 | La note rappelle deux limites : un goal déjà rédigé garde la valeur qu'il porte ; le gel prime sur toute modification pendant la production. | Should | proposed (à confirmer : Amiel) | A8 |

### 6.10 Exigences d'interface posées à un harnais futur

Une exigence d'interface dit **ce que le harnais doit tenir**, jamais **comment**. Elle s'évalue au cadrage de la partie B, sur la trace et le comportement observés.

| ID | Exigence | MoSCoW | Label | Source |
|---|---|---|---|---|
| H1 | **Lire A4.** Le harnais prend toutes ses valeurs (plafonds, modèles, suites, gel, skills de format) dans A4 par leur clé, consigne `version` et l'empreinte d'A4 au lancement (T1) et copie les plafonds appliqués (T2). Il n'en porte aucune valeur propre. | Must | decided | C8 ; D7 |
| H2 | **Écrire A3.** Le harnais écrit la trace à ce format : mêmes tableaux, mêmes colonnes, mêmes marques d'absence, une trace par sujet dans son dossier. S'il impose sa propre forme, il la traduit vers A3 et le dit (RA1). | Must | decided | C3 à C7 ; RA1 |
| H3 | **Sceller.** Jusqu'à la fin du jugement, la part cachée et la trace du juge sont hors de ce que le producteur lit, leur chemin n'est pas écrit dans la trace qu'il lit, seule leur empreinte l'est (T9) ; ensuite elles sont versées au dossier. | Must | decided | D5, C6 |
| H4 | **Geler.** Le script de recette, la grille visible et leurs fixtures sont figés avant la production : empreinte relevée (T9), contrôle de l'empreinte avant chaque tour, arrêt au premier écart ; un critère à revoir passe seulement par la suite « contourner ». | Must | decided | procédure, étape 3 ; D8 ; clé `gel.*` |
| H5 | **Tenir les plafonds.** À un plafond atteint, le harnais s'arrête, consigne le constat, offre exactement les suites de A4 pour ce plafond, laisse le pilote choisir et trace son choix (T7). | Must | decided | D8, LR4 |
| H6 | **Modèle explicite et accord.** Chaque appel d'agent porte un modèle explicite pris dans A4 ; l'appel au modèle de contre-vérification est précédé de l'accord de la personne qui pilote le sujet, et fait à part. | Must | decided | C13 ; D11 ; clés `production.modele_explicite_obligatoire`, `modeles.contre_verification` |

## 7. Critères d'acceptation

Un comportement par ligne. Types : nominal, erreur, limite, négatif (ce qui ne doit pas arriver). Chaque Must a au moins une ligne « négatif ».

| Exigence | Étant donné (Given) | Quand (When) | Alors (Then) | Type |
|---|---|---|---|---|
| X1 | A1 à A8 | on lit chaque occurrence des mots désignant un harnais ou une mécanique d'enchaînement | aucune ne prescrit comment le construire | négatif |
| X1 | la clé `production.mode` d'A4 | on la lit | elle est une valeur de réglage, admise, et non une prescription de harnais | limite |
| X2 | les corps de A1 et A2 | on y cherche les identifiants des skills d'ix-recipes | aucun n'est trouvé | négatif |
| X2 | un lecteur qui cherche l'association type → skills de format | il ouvre A4 | il la trouve sous `types_de_sujet.<type>.skills_de_format` | nominal |
| X3 | le dépôt ix-skills | on compare la branche dédiée à `main` | A1 et A2 sont sur la branche ; `main` n'a reçu aucun de leurs commits | négatif |
| X3 | les deux skills | on valide et on construit avec l'outil du dépôt | la validation passe et le dossier construit est commité | nominal |
| X4 | le dépôt ix-pilote | on liste les fichiers de A3 à A8 | tous sont sous `partie-a/`, aucun sous `trace/` ni `corpus/` | négatif |
| X4 | `corpus/` | on compare à l'état avant le passage | aucune différence | négatif |
| X5 | la liste « ce qu'il faut tracer » du goal et A3 | on met chaque élément en face d'une colonne ou d'une note d'A3 | chaque élément a sa place ; un élément sans place est un écart signalé | négatif |
| A1-1 | un cadrage soumis, des réponses, et un message qui demande de clore | A1 s'exécute | la sortie a les douze sections dans l'ordre, et l'en-tête des entrées | nominal |
| A1-1 | une section sans rien à dire | A1 l'écrit | la section est présente et dit qu'elle n'a rien à rapporter, et pourquoi | limite |
| A1-1 | un message sans demande de clore | A1 s'exécute | la sortie n'a aucune section propre au cadrage clos | négatif |
| A1-2 | un cadrage soumis fourni sans demande de clore | le skill s'exécute | il suit le mode par défaut et ne passe pas en mode `close` de lui-même | négatif |
| A1-2 | la recette `brief-client` | elle appelle `cadrage` | elle reçoit encore `need`, `constraints`, `hypotheses`, `open_points` | nominal |
| A1-3 | une réponse qui contredit le défaut du cadrage soumis | A1 clôt | la décision cite la réponse entre guillemets et n'applique pas le défaut | nominal |
| A1-3 | un défaut sans aucune remarque | A1 clôt | la décision a pour source « défaut accepté » et figure dans le rappel adressé au décideur | nominal |
| A1-3 | une question bloquante sans réponse ni défaut | A1 clôt | elle devient la question résiduelle ; si elle bloque, le document ne se dit pas prêt pour l'étape suivante | négatif |
| A1-4 | un sujet qui construit un outil | A1 écrit les livrables | une ligne « spec et architecture » avec son lecteur est présente et ne nomme aucun skill producteur | nominal |
| A1-4 | la sortie d'A1 | on y cherche un nom de skill présenté comme producteur d'un livrable | aucun n'est trouvé | négatif |
| A1-4 | un sujet qui ne construit aucun système | A1 écrit les livrables | la section dit pourquoi aucune spec ni architecture n'est prévue | limite |
| A1-5 | un cadrage clos produit sur un cas de code d'essai | A5 est appliquée après la pause | aucune infraction parmi G1 à G9 ; au plus la tolérance de douteux fixée par le critère de recette | nominal |
| A1-5 | un point G absent de la sortie | on juge | verdict d'infraction sur ce point | négatif |
| A1-6 | des réponses muettes et pas de défaut | A1 clôt | l'option qui engage le moins est prise, marquée « à confirmer » | nominal |
| A1-6 | la même situation | A1 clôt | aucune décision n'est inventée | négatif |
| A1-7 | un cadrage clos | A1 rejoue les tests | chaque test a un verdict et sa raison ; un test conditionnel est rejoué | nominal |
| A2-1 | un message qui fournit aussi les critères | A2 s'exécute | il ne les utilise pas et le dit dans les notes du rédacteur | négatif |
| A2-1 | les trois entrées requises | A2 s'exécute | un goal est rendu | nominal |
| A2-2 | un livrable sans skill de format dans l'entrée | A2 l'écrit dans le goal | l'entrée dit « aucun skill de format » et A2 n'en suppose pas | négatif |
| A2-2 | le goal rendu | on le lit | chaque section de A2-2 est présente avec un contenu | nominal |
| A2-3 | le goal rendu | on lit la condition d'arrêt | elle nomme le script par son emplacement, ne dit rien de ce qu'il vérifie, et le plafond égale la valeur de `plafonds.tours_goal_max` | nominal |
| A2-3 | le goal rendu | on y cherche un critère, une commande du script ou un seuil autre que le plafond | aucun n'est trouvé | négatif |
| A2-3 | le goal rendu | on y cherche l'interdit de modifier le script et la grille | il est écrit | négatif |
| A2-4 | le goal rendu | on lit les autorisations | chaque sous-agent autorisé porte un modèle explicite pris dans les réglages | nominal |
| A2-4 | le goal rendu | on y cherche une autorisation sans modèle ou un sous-agent qui écrit un livrable | aucune n'est trouvée | négatif |
| A2-5 | le corps d'A2 | on y relève les mentions propres à un outil | aucune, ou chacune est donnée comme exemple | négatif |
| A2-6 | une liste de skills de format où manque un skill que le rédacteur croit utile | A2 s'exécute | le goal n'ajoute aucun skill | négatif |
| A2-7 | un emplacement non rempli | le producteur démarre | le goal lui dit de ne rien produire et de rendre la main avec la raison | nominal |
| A2-8 | une lacune du cadrage clos | A2 s'exécute | la lacune est listée à part avec l'option la plus étroite « à confirmer » | nominal |
| A3-1 | une trace | un programme cherche le titre T3 et lit la ligne d'en-tête | il trouve les colonnes nommées et lit une ligne par `étape` et `occurrence` | nominal |
| A3-1 | une trace | on la regarde | une colonne renommée, ou deux valeurs dans une cellule, sont une infraction | négatif |
| A3-1 | une trace ouverte dans un éditeur de texte | un lecteur sans Claude Code la lit | il y trouve ses tableaux | limite |
| A3-2 | une ligne d'étape de T3 | on la lit | entrée, sortie, modèle, durée, jetons, coût et source du coût sont présents | nominal |
| A3-2 | un skill utilisé par une ligne | on cherche sa ligne en T4 | version et empreinte y sont, ou `n.c.` avec la raison | négatif |
| A3-2 | une empreinte de skill ou d'A4 qui a changé depuis | on rejoue | la trace montre que le rejeu n'est plus identique | limite |
| A3-3 | un coût calculé à partir des jetons et d'un tarif | on lit la ligne | `source_coût` vaut `estimé` et `méthode_coût` donne le tarif, sa date et ce qu'on ignore | nominal |
| A3-3 | la même ligne | on la lit | `estimé` n'est pas écrit comme `mesuré` | négatif |
| A3-4 | les étapes 4 et 6 | on lit T3 et T5 | une ligne de granularité `session` ; chaque sous-agent en T5 avec son modèle | nominal |
| A3-4 | un sous-agent en T5 | on cherche son coût | il n'a aucun coût individuel | négatif |
| A3-5 | un jugement en cours | on lit T9 | la part cachée est `scellé`, avec son empreinte et l'emplacement `non écrit` | nominal |
| A3-5 | la trace lisible par le producteur | on y cherche le chemin d'un élément scellé | il n'y est pas | négatif |
| A3-5 | le jugement est fini | on lit T9 | les éléments sont `ouvert` avec leur emplacement | nominal |
| A3-6 | une trace | on y cherche une pièce d'un autre sujet | aucune ; seul un nom de dossier d'enfant en T8 | négatif |
| A3-7 | une trace neuve | on lit la première ligne de T3 | c'est l'étape 0, la demande séparée des pièces | nominal |
| A3-7 | la première ligne de T3 | elle porte une autre étape | c'est une infraction | négatif |
| A3-8 | une valeur absente | on la lit | elle porte l'une des trois marques, avec la raison | nominal |
| A3-8 | la trace | on cherche une cellule vide ou une valeur sans mesure | aucune | négatif |
| A3-9 | une décision venue d'un silence | on lit T6 | source `défaut accepté`, à rappeler `oui` | nominal |
| A3-9 | un plafond atteint | on lit T7 | constat, suites lues dans A4 pour ce plafond, suite choisie, et ses détails | nominal |
| A3-9 | le plafond des passes de vérification atteint | on lit T7 | « contourner » n'est ni proposé ni choisi | négatif |
| A3-9 | aucun plafond atteint | on lit T7 | la phrase « aucun plafond atteint », sans tableau | limite |
| A3-10 | des lancements du script | on lit T10 | une ligne par lancement ; le nombre de vérifications ne baisse pas | nominal |
| A3-11 | A3 | un développeur extrait modèle et coût d'une étape | la méthode est sans heuristique, avec les noms de colonnes d'A3 | nominal |
| A4-1 | A4 | un programme le charge | il se charge et porte `version` | nominal |
| A4-1 | A4 avec une clé dupliquée ou une erreur de syntaxe | on le charge | le chargement échoue | négatif |
| A4-2 | la liste de C8 | on cherche chaque valeur dans A4 | chacune a sa clé | nominal |
| A4-2 | A4 | une valeur de C8 manque | c'est une infraction | négatif |
| A4-3 | chaque valeur d'A4 | on lit ses commentaires | elle dit ce qu'elle règle et sa source | nominal |
| A4-3 | A4 | on cherche une valeur sans commentaire | aucune | négatif |
| A4-4 | les types de sujet | on lit A4 | `code` est rempli ; les trois autres portent « partie C » | nominal |
| A4-4 | un type marqué « partie C » | on le lit | il ne contient aucune valeur de skill inventée | négatif |
| A4-5 | `suites_au_plafond` | on lit la clé des passes de vérification | trois suites, sans « contourner » | négatif |
| A4-5 | `suites_au_plafond` | on lit les clés des tours de correction et des tours du goal | quatre suites dont « contourner » | nominal |
| A4-6 | une demande de changer un plafond | le mainteneur suit A8 | le changement ne touche qu'A4 (un fichier) et monte `version` | nominal |
| A4-6 | A3, A5, A6, A7, A8 et un goal | on y cherche la valeur d'un réglage écrite comme source | aucune ; seule la copie appliquée en T2 est admise | négatif |
| A4-7 | une valeur modifiée seule | on monte `version` | c'est un correctif | nominal |
| A5-1 | A5 et les neuf points de la procédure | on les compare | neuf sur neuf au même sens, aucun affaibli | nominal |
| A5-1 | une règle d'A5 qui affaiblit son point | on juge | infraction | négatif |
| A5-2 | A5 appliquée avant la pause 1 | on juge | G3 et G9 sont notés « attente de la pause 1 », sans verdict ; les autres sont jugés | nominal |
| A5-2 | la même situation | on cherche un verdict d'infraction sur G3 ou G9 | aucun | négatif |
| A5-2 | A5 appliquée après la pause 1 | on juge | les neuf points sont jugés | nominal |
| A5-3 | un sujet qui construit un outil, un cadrage clos sans ligne « spec et architecture » ni raison | on juge G7 | infraction | négatif |
| A5-3 | le même cadrage avec la raison écrite | on juge G7 | conforme | nominal |
| A5-4 | A5 | on lit où en est sa relecture | l'état est dit | nominal |
| A5-4 | une relecture faite sans accord du pilote | on la constate | c'est une infraction | négatif |
| A5-5 | un verdict avant la pause | on le lit | attente de la pause 1 et défaut corrigeable sont séparés | nominal |
| A6-1 | A6 | on prend chaque pièce de A1 à A8 | fonction, entrées, sorties et étape y sont, huit sur huit | nominal |
| A6-1 | A6 | une pièce manque d'un de ces quatre éléments | c'est une infraction | négatif |
| A6-2 | A6 | on demande où vit l'association | la réponse renvoie à la clé d'A4 | nominal |
| A6-2 | A6 | on y cherche des identifiants de skills présentés comme valeurs de l'association | aucun | négatif |
| A6-3 | un développeur qui n'a que A6 | il liste ce qu'un harnais doit faire | lire A4, écrire A3, sceller la part cachée, geler script et grille, et placer l'association dans A4 : cinq sur cinq | nominal |
| A6-3 | A6 | on cherche une prescription de comment faire | aucune | négatif |
| A6-4 | A6 | on la compare aux formats d'une spec et d'une architecture | chaque élément est présent ou écarté avec sa raison | nominal |
| A7-1 | un lecteur qui n'a que A7 | il dit, pour chaque étape de 0 à 7, la pièce lue ou écrite et qui agit aux pauses | aucune étape ne manque ; pour l'étape 7 : « aucune pièce de la partie A » | nominal |
| A7-1 | A7 | une étape est mal attribuée à une pièce | c'est une infraction | négatif |
| A7-2 | un lecteur qui n'a que « lire une trace » | il cherche pour une étape l'entrée, la sortie, le modèle, le coût et sa source | il les trouve | nominal |
| A7-2 | ce texte | on cherche une dépendance à un autre document ou à Claude Code | aucune | négatif |
| A7-3 | un silence à la pause 1 | on suit le guide | le défaut est gardé, marqué « défaut accepté », rappelé à la clôture | nominal |
| A7-3 | le guide | on cherche un silence traité comme un « oui » sans rappel | aucun | négatif |
| A7-4 | les plafonds | un lecteur dit les suites de chacun | passes de vérification : trois suites sans « contourner » ; les deux autres : quatre suites | nominal |
| A7-4 | le guide | on cherche « contourner » offert au plafond des passes de vérification | non | négatif |
| A7-4 | « relancer » | un lecteur dit qui fixe le nombre de tours | le pilote, et le nombre est tracé | nominal |
| A7-6 | le guide | on y cherche une valeur d'A4 recopiée | aucune | négatif |
| A8-1 | A8 | on y cherche chaque pièce | le fichier et le dépôt de chacune y sont | nominal |
| A8-1 | A8 | une pièce n'y figure pas | c'est une infraction | négatif |
| A8-2 | un lecteur qui n'a que A8 | il fait passer le plafond du goal à une autre valeur dans une copie jetable | le diff montre un fichier modifié, A4 | nominal |
| A8-2 | A8 | on y cherche l'instruction de modifier une autre pièce pour un réglage | aucune | négatif |
| A8-3 | A8 et les règles d'ix-skills | on compare | aucune contradiction, aucune étape manquante | nominal |
| A8-3 | A8 | on y cherche une consigne d'ajouter tous les fichiers d'un coup | aucune | négatif |
| A8-4 | A8 | on lit ce qui migre | chaque pièce a son devenir | nominal |
| A8-4 | le `README.md` d'ix-pilote | on y cherche le chemin de la note | il y est | négatif |
| A8-5 | A8 | on y cherche les deux limites | elles sont écrites | nominal |
| H1 | un harnais qui lance un sujet | on lit sa trace | T1 porte `version` et l'empreinte d'A4 ; T2 porte les plafonds | nominal |
| H1 | le harnais | une valeur de plafond ou de modèle est codée en dur et diffère d'A4 | non conforme | négatif |
| H2 | un passage mené par un harnais | on lit la trace | T1 à T11 conformes à A3 | nominal |
| H2 | la trace d'un sujet | elle contient une pièce d'un autre sujet | non conforme | négatif |
| H3 | un jugement en cours | on regarde ce que le producteur peut lire | ni la part cachée, ni la trace du juge, ni leur chemin ; T9 ne porte que l'empreinte | nominal |
| H3 | la même situation | un chemin d'élément scellé est trouvé | non conforme | négatif |
| H3 | le jugement est fini | on regarde T9 | les éléments sont `ouvert` et versés au dossier | nominal |
| H4 | le gel accompli | on lit T9 | script, grille et fixtures ont une empreinte | nominal |
| H4 | un fichier figé modifié | le tour suivant commence | le harnais s'arrête au premier écart | négatif |
| H4 | un critère jugé faux | on veut le revoir | le seul chemin est « contourner », avec retour en 2B et dérogation tracée | limite |
| H5 | un plafond atteint | on observe | le harnais s'arrête, consigne le constat, offre exactement les suites d'A4 pour ce plafond | nominal |
| H5 | le harnais | il poursuit sans rendre la main, ou choisit seul la suite | non conforme | négatif |
| H6 | un appel d'agent | on lit sa trace | le modèle est explicite et égal à la clé d'A4 du rôle | nominal |
| H6 | un appel d'agent sans modèle explicite | on le constate | non conforme | négatif |
| H6 | l'appel au modèle de contre-vérification | on le constate sans accord préalable du pilote | non conforme | négatif |

## 8. Objets, cycles de vie et règles de calcul

Le sujet n'a aucun écran ; la section « vues et états » est omise. Les objets qu'il manipule :

| Objet | Cycle de vie | Propriétaire et visibilité | Suppression | Statut dérivé et règle |
|---|---|---|---|---|
| **Réglages (A4)** | modifié par le mainteneur → `version` montée → consigné par la trace du sujet suivant | propriétaire : Amiel ; lisible par le pilote, le mainteneur, un harnais | non spécifié (suivi par le dépôt) | *valeur appliquée* = valeur lue au lancement, copiée en T2 ; elle ne change pas même si A4 change ensuite |
| **Trace** | ouverte à l'étape 0 → complétée ligne par ligne → complète quand plus aucune ligne de T9 n'est `scellé` | propriétaire : le pilote ; lisible par Amiel, et par un client pour son seul sujet | non spécifié par A3 | *trace complète* ⇔ aucune ligne `scellé` en T9. *Rejeu identique* ⇔ pour chaque skill de T4 et pour A4, version et empreinte sont celles du moment du rejeu. *Fiabilité d'un coût* = `source_coût` (`mesuré` > `estimé` > `n.c.`) |
| **Élément figé ou scellé** (script, grille, fixtures, part cachée, trace du juge) | `figé` ou `scellé` au gel → pas de modification → `ouvert` à la fin du jugement ; un figé ne change que par « contourner » (retour en 2B) | la part cachée et la trace du juge : hors de portée du producteur jusqu'à la fin du jugement | non applicable | *Autorisé à la lecture par le producteur* ⇔ état `figé` ou `ouvert`. Pour un `scellé`, l'emplacement vaut `non écrit` |
| **Plafond** | non atteint → atteint → suite choisie (relancer, contourner, livrer avec réserve, abandonner) | le pilote choisit | non applicable | *Suites offertes* = la liste d'A4 sous `suites_au_plafond` pour ce plafond |
| **Point de la grille (G1 à G9)** | jugé avant la pause 1 (sept points) puis après (neuf) | l'agent d'évaluation ; l'auteur de 1e écrit pour les tenir | non applicable | *S'applique* ⇔ moment = après la pause 1, ou point ∉ {G3, G9} |

## 9. Métriques de succès

Les quatre issues viennent de `trace/02b-criteres.md`, section « Issue visée ». Seuils confirmés tels quels par Amiel à la pause 2 (17/10/2026, réponse 2). Aucun n'a de valeur de départ mesurée : « baseline to be measured » pour tous. Le classement leading ou lagging est une proposition de cette spec, pas celle de la source.

| Métrique | Leading ou lagging | Valeur de départ | Seuil de réussite (en dessous : échec) | Cible | Méthode de mesure | Date d'évaluation |
|---|---|---|---|---|---|---|
| **O1.** Sur le prochain vrai sujet de code mené avec A1 à A5, nombre d'endroits où le pilote invente une étape ou une valeur absente d'A7 ou d'A4 | lagging | à mesurer | au plus 3 endroits (échec au-dessus) | 0 endroit, et aucune pièce modifiée avant de commencer | le pilote compte les endroits | au bilan de ce prochain sujet (fixé par Amiel) |
| **O2.** `brief-client` après la fusion de `cadrage` | leading | à mesurer | une exécution réelle rend les quatre champs, sans reprise manuelle | aucune différence de forme perçue par Amiel avec la version précédente de `cadrage` | exécution réelle de la recette | à la première exécution après la fusion (fixé par Amiel) |
| **O3.** Au démarrage de la partie B, nombre de questions posées à Amiel sur ce que le harnais doit lire ou écrire | lagging | à mesurer | au plus 3 questions (échec au-dessus) | 0 question de ce type | comptage au cadrage de B | au cadrage de la partie B (fixé par Amiel) |
| **O4.** Première trace remise à un client : retrouve-t-il, pour une étape, l'entrée, la sortie, le modèle et le coût avec sa source ? | leading | à mesurer | le client les retrouve | il les retrouve sans poser de question | observation de la lecture | à la première remise (fixé par Amiel) |

Les dates d'évaluation sont des événements, pas des dates de calendrier : aucune échéance n'est fixée (D10).

## 10. Questions ouvertes et décisions ouvertes

La rédaction de cette spec a relevé dix questions sur les autres pièces. Six ont été closes pendant la production en corrigeant ces pièces ; quatre restent ouvertes. Aucune ne bloque la partie A, ni le constructeur de la partie B.

**Closes pendant la production** (la pièce corrigée est entre parenthèses) :

| # | Question | Réponse |
|---|---|---|
| Q1 | Qui sélectionne `chez_amiel` ou `ailleurs` ? | Le pilote du sujet : `chez_amiel` quand il est Amiel, `ailleurs` sinon (A4, commentaire de `contre_verification`). |
| Q2 | Quelle valeur d'`étape` pour le gel, les pauses, l'étape 7 ? | Les pauses : `pause 1`, `pause 2` ; le gel : étape `3`, occurrence `gel` ; l'étape 7 : une ligne faite par une personne. Une ligne faite par une personne prend la granularité `appel` (A3, T3). |
| Q3 | Où vont les points « à confirmer » et les chemins hors périmètre ? | Dans la nouvelle table T11 (A3). |
| Q4 | Quelle écriture des suites est normative ? | Les noms des clés d'A4 (`relancer`, `contourner`, `livrer_avec_reserve`, `abandonner`), repris par `suite_choisie` de T7 (A3). |
| Q6 | Faut-il une annexe de critères pour les documents ? | Oui : `criteres_document` est ajoutée sous `annexes_criteres` du type « code » (A4). |
| Q8 | Qui juge G3 et G9 après la pause ? | Un agent distinct de l'auteur, une fois le cadrage clos écrit (A5, en-tête ; A7, étape 1e). |

**Restent ouvertes** :

| # | Question | Bloquante ? | Qui répond | Quand |
|---|---|---|---|---|
| Q5 | Qui range un livrable d'un cadrage clos dans un genre de `skills_de_format` (spécification, architecture, documentation), et comment, pour remettre à A2 la liste « livrable → skill » ? Aucune pièce ne l'écrit ; le pilote le fait à la main. | Non | Amiel | avant le prochain sujet |
| Q7 | A2 choisit le modèle d'un sous-agent « par rôle » (mécanique, lecture et expertise cadrée, vérification) ; A4 ajoute la clé `sous_agents_verification`, mais aucune table ne fait correspondre ces rôles aux clés `modeles`. | Non | Amiel | avant le prochain sujet |
| Q9 | A5 n'est relue par le modèle de contre-vérification qu'après la production du passage : au premier sujet réel, elle sera appliquée avant sa relecture. Faut-il exiger la relecture avant le premier sujet réel ? | Non | Amiel | avant le prochain sujet |
| Q10 | La méthode d'estimation du coût demande le « tarif public » daté, mais aucune pièce ne dit où ce tarif est consigné (ni si c'est un réglage de C8). | Non | Amiel | avant le prochain sujet |

**Décisions ouvertes**, à part des exigences stables : aucune décision n'est tenue pour tranchée dans cette spec qui ne soit déjà dans 01e. Les cinq décisions venues d'un silence (D5, D6, D7, D11, D12) restent à rappeler à Amiel à la clôture ; une correction rouvrirait A3 et A4.

## 11. Prochaines actions

| Quoi | Qui | Quand |
|---|---|---|
| Répondre à Q5, Q7, Q9 et Q10 | Amiel | avant le prochain sujet de code |
| Mesurer O1 à O4 | Amiel | aux événements du tableau 9 |
