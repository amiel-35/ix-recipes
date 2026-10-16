# Décision : la notion de corpus dans les recettes

Document de décision du 2026-10-16. Amiel a tranché les questions (§3, §7) ; **pas de code avant les vérifications du §8**. Il remplace l'approche du commit `a27a922` (format 3 : `items` et `mode`), retiré le même jour (gardé sur la branche locale `sauvegarde-format3-a27a922`) ; seule la vérification de calcul en a été conservée.

## 1. Le problème

Aujourd'hui le moteur ne connaît qu'une entrée, « la demande brute » (`input.md`), réservée à l'étape 1 et protégée par le contrôle de fuite. Or ce texte mélange deux choses :

- **la demande** : ce que l'utilisateur veut obtenir (« fais-moi les personas », « réponds à cet appel d'offres ») ;
- **le matériau** : ce sur quoi on travaille (verbatims, tableau budget / réel, contrat, cahier des charges, offres reçues).

La règle d'isolation vient d'ix-memory : les étapes aval qui relisaient le brief le réinterprétaient et refaisaient tout. Ce danger vient de la demande. En protégeant les deux ensemble, on prive les étapes aval du matériau dont elles ont besoin : c'est la cause commune des besoins relevés par la revue des skills métier (§1.1) — vérifier une absence dans un contrat, vérifier des chiffres contre un tableau, donner le détail d'un besoin à une étape 2, citer des verbatims sans les réécrire.

## 2. La notion de corpus

| | La demande | Le corpus |
|---|---|---|
| Ce que c'est | ce qu'on veut obtenir | les pièces sur lesquelles on travaille |
| Qui la sépare | l'humain, à la création du dossier (la demande tapée, les pièces jointes) | idem |
| Qui la voit | l'étape 1, et une étape qui vérifie et déclare `reads_source` (déjà sur main) | l'étape 1, et les étapes que la recette autorise, nommément |
| Comment | dans le message | **consulté** : les pièces sont copiées dans le dossier jetable de l'étape, qui lit ce dont elle a besoin |
| Protection | contrôle de fuite | aucune : c'est du matériau ; ce que l'étape produit reste contrôlé contre la demande |

Sans pièces séparées (tout collé d'un bloc), rien ne change : tout est « demande », protégée comme aujourd'hui.

## 3. Décisions d'Amiel (2026-10-16)

1. **Le corpus est lu à la demande**, pas poussé dans le message. Trace de lecture : **déclarative toujours** (c'est la base : l'étape dit ce qu'elle a lu et ce qu'elle n'a pas ouvert), **mécanique en plus quand le moteur le permet**.
2. **Une étape qui produit peut consulter le corpus**, mais seulement si la recette l'autorise sur cette étape. **C'est l'exécuteur qui donne le droit** : il copie les pièces dans le dossier de l'étape, ou non.
3. **`verbatim` est gardé** tel quel : il reste utile sans corpus séparé, pour une sélection validée à l'étape 1, et en conversation, où il n'y a pas de dossier.

## 4. Ce que les tests ont montré (2026-10-16)

Dossier jetable contenant une référence et une pièce ; à côté, un faux dossier de parcours avec sa demande.

| Moteur | Lit son dossier | Lit hors de son dossier | Trace mécanique |
|---|---|---|---|
| Claude (`claude -p --tools Read`, options de l'exécuteur) | oui | **non** : refusé par Claude, en chemin absolu comme en `../` ; le refus remonte dans `permission_denials` | **oui** en `--output-format stream-json --verbose` : chaque `Read` avec son chemin et son résultat. Le format `json` actuel ne donne que les refus |
| Codex, avant (`-s read-only`, testé par `codex sandbox`, sans appel au modèle) | oui | **oui** : son bac à sable interdit d'écrire, pas de lire ; il lit la demande d'un dossier, et tout le disque | — |
| Codex, depuis le plugin 2.13.0 (profil de permission `ixetape`, [exécuteur](executeur.md) §4 ; vrai appel `codex exec`, codex-cli 0.155.1) | oui | **non**, sauf `/tmp`, `/var/tmp` et des fichiers système : la demande à côté du dossier, celle d'un dossier de parcours et `~/.zshrc` sont refusées | **partielle** : `--json` donne les commandes lancées et leur sortie, pas les fichiers lus ; une commande refusée par le bac à sable n'y figure pas |
| Antigravity, Vibe | — | non testé (pas de crédit le 2026-10-16, §9.2) | non testé : trace déclarative seule |

Conséquence pour Claude : « une étape ne voit que ce que l'exécuteur lui copie » est vrai, le droit se donne en copiant ou non. Conséquence pour Codex : **c'était un trou dans l'isolation**, corpus ou pas ; une étape Codex qui cherchait `input.md` sur le disque le trouvait. Refermé par le plugin 2.13.0 : un profil de permission limite ses lectures au dossier de l'étape, vérifié avant chaque appel ; le droit se donne alors en copiant ou non, comme pour Claude. Reste lisible `/tmp` (rien du parcours n'y est).

## 5. Ce que ça changerait (proposition)

- **Création du dossier** : la demande d'un côté, des pièces de l'autre (page : une zone « votre demande », une zone « vos pièces » ; ligne de commande : `new --input demande.md --corpus piece1.md piece2.xlsx`). Les pièces vont dans `./parcours/<slug>/corpus/`.
- **Recette** : une étape déclare `receives: [corpus]` pour consulter les pièces. Une nouvelle source dans `receives` : un exécuteur plus ancien ne saurait pas la jouer, donc **format 3** (le critère du §2bis de `format-recette.md`).
- **Exécuteur** : copie `corpus/` dans le dossier jetable des seules étapes autorisées ; annonce les pièces dans le message (comme les `references/`) ; demande une section `### sources_read` (lues / non ouvertes) ; avec Claude, passe en `stream-json` et enregistre les lectures réelles, signale les écarts avec la déclaration.
- **Citer** : Claude lit les fichiers avec leurs numéros de ligne ; une étape cite `entretiens.md:12`. Le regroupement donne des références, l'étape persona relit les lignes. Le handoff par identifiants du commit `a27a922` devient inutile.
- **`reads_source`** reste : il donne la **demande** à une étape qui vérifie (contrôler ce qui a été demandé, les mots du demandeur). Le corpus donne les **pièces**. Deux choses différentes.

## 6. Ce que ça règle

| Besoin | Avec le corpus |
|---|---|
| `persona` cite les verbatims | l'étape consulte le corpus et cite par fichier et ligne — **réglé** |
| vérifier des chiffres (`budget-variance-analysis`, `calc-check`) | la vérification consulte le tableau — **réglé** |
| vérifier une absence (`cgv-checker`, `contrat-fournisseur`) | la vérification relit tout le contrat — **réglé** |
| `rfp-draft`, `offer-comparison` ont besoin du détail | étapes qui produisent, autorisées nommément — **réglé, risque de dérive le plus fort** |
| `people-review` : ne rien inventer sur une personne | une vérification consulte les notes — **réglé** |
| `brief-client` (le mail est demande et matériau) | pas de pièces séparées : comme aujourd'hui |

Hors du sujet : les deux phases d'un même skill (décision 2) n'ont pas besoin du corpus ni d'un format ; assouplir la règle de `concepteur-recette` et dire le mode dans la mission suffit probablement.

## 7. Décidé le 2026-10-16

1. **Codex lit tout le disque** : on l'accepte et on le dit dans la page, au moment de choisir Codex comme moteur. En parallèle, une session cherche un réglage qui limite ses lectures au dossier de l'étape (note attendue : `codex-lecture.md` dans les notes partagées). **Suite (plugin 2.13.0)** : le réglage existe (profils de permission de Codex) et l'exécuteur l'utilise ; la page dit désormais, au choix de Codex, ce qui reste lisible (`/tmp`, `/var/tmp`, fichiers système).
2. **La page attendra** : le corpus arrive d'abord en ligne de commande (`new --input demande.md --corpus pièces…`), pour le tester sur un cas réel ; les deux zones « votre demande » et « vos pièces » viendront dans la page ensuite, si le test de dérive (§8) passe.

## 8. À vérifier avant de coder

- **La dérive** : sur un cas réel (notes de terrain → regroupement → personas), jouer l'étape persona avec et sans le corpus, et regarder si elle reste dans sa mission ou refait le regroupement. Quelques appels Sonnet, comme la preuve de `reads_source`.
- **Codex** : ~~lire ses évènements `--json` ; chercher un réglage qui restreint ses lectures~~ — fait (plugin 2.13.0, [exécuteur](executeur.md) §4) : le profil `ixetape` limite les lectures au dossier de l'étape ; `--json` est gardé comme trace, partielle (commandes lancées, pas les refus). Reste ouvert : `/tmp` lisible, profils en bêta (vérifiés avant chaque appel), sous-agents de Codex non testés.
- **Antigravity, Vibe** : lecture hors du dossier.
- **Les pièces non textuelles** (xlsx, pdf) : Claude lit les PDF ; un tableur demande une conversion à la création du dossier.

## 9. Résultats des vérifications (2026-10-16)

Joués sans toucher à l'exécuteur ; protocoles, scripts et traces dans [`preuve-corpus/`](preuve-corpus/README.md). Codex : autre session (note `codex-lecture.md`).

### 9.1 La dérive : l'étape persona reste dans sa mission

Le dépôt n'a pas de notes de terrain réelles (`tests/cas-skills/persona.md` est fictif et tient en six lignes). Amiel a choisi dans ses archives la restitution d'une vraie étude UX de terrain ; ses verbatims et constats ont été mis en 113 notes, une par ligne, thèmes retirés, ordre mélangé. **Biais** : la source était déjà regroupée par thème ; le regroupement par comportement, celui des personas, restait à faire. Le matériau reste hors du dépôt public. Recette à deux étapes (`affinity-mapping` puis `persona`), étape persona jouée deux fois sans et deux fois avec le corpus, jugée par une grille écrite avant les sorties ([`grille.md`](preuve-corpus/derive/grille.md)) ; 1,28 $. Détail : [`resultats.md`](preuve-corpus/derive/resultats.md).

- **Verdict** : avec le corpus, l'étape persona **reste dans sa mission** dans les deux passages : mêmes 4 groupes, mêmes comptes, aucun motif nouveau, les notes d'autres groupes citées seulement en contraste. Elle le fait alors que le skill `persona` dit lui-même de former les groupes (« You form the groups yourself from the material »).
- **Gain** : sans corpus, pas de verbatim (un passage en invente, signalés comme paraphrases ; l'autre renvoie au corpus) ; avec, 11 et 19 verbatims exacts, chacun avec l'identifiant de sa note. Le besoin du §6 est réglé sur ce cas.
- **Coût** : +45 % par appel, parce que l'étape lit le fichier entier (10 500 caractères) pour en citer quelques lignes. La section `sources_read` déclarée correspond au flux (un `Read`).
- **Fragile, avec ou sans corpus** : des formules inventées mises entre guillemets (titres de personas).
- **Trouvé en route** : le premier regroupement a donné 10 groupes pour 4 personas au plus ; avec « une persona par groupe », l'étape suivante aurait dû fusionner, donc regrouper. Une recette doit borner le nombre de groupes de l'étape qui regroupe au plafond de l'étape qui suit.
- **Non joué** : une mission qui n'interdit pas en toutes lettres de regrouper ; un corpus trop gros pour être lu en entier ; des notes brutes non structurées.

### 9.2 Antigravity, Vibe : non testé, pas de crédit

- **Antigravity** (`agy` 1.4.0, options de l'exécuteur) : « Individual quota reached », remise à zéro annoncée dans 69 h 44 ; même refus avec un autre modèle (`gemini-3.8-flash-low`). Aucun appel n'a abouti.
- **Vibe** (2.25.8, `vibe -p --output text`) : « Vibe budget exhausted » (402).

Sorties : [`preuve-corpus/antigravity-vibe/sorties.txt`](preuve-corpus/antigravity-vibe/sorties.txt) ; [`rejouer.sh`](preuve-corpus/antigravity-vibe/rejouer.sh) rejoue le protocole du §4 (un appel par moteur) quand le crédit revient. Ce que disent les aides, sans appel : `agy` a une notion d'espace de travail (`--add-dir`) et un `--sandbox` « with terminal restrictions » que l'exécuteur ne passe pas ; Vibe a `--workdir`, `--add-dir` et `--disabled-tools`. Rien n'y dit que la lecture hors du dossier est refusée. Jusqu'à l'essai, les traiter comme Codex : **le droit donné en copiant n'est garanti qu'avec Claude**.

### 9.3 Les pièces non textuelles

Six appels `claude -p` (Sonnet, options de l'exécuteur, sortie `stream-json`), un par pièce, chacune seule dans un dossier jetable ; 0,256 $ au total. Pièces fabriquées : [`fabriquer.py`](preuve-corpus/pieces-non-textuelles/fabriquer.py).

| Pièce | Résultat | Trace |
|---|---|---|
| PDF texte, 2 pages, un tableau | **passe** : tout lu, tableau compris, en images de pages (`pages: "1-10"`). Cite par page et article ; refuse de donner des numéros de ligne (« serait de ma part une invention ») | [contrat-pdf](preuve-corpus/pieces-non-textuelles/traces/contrat-pdf.md) |
| PDF de 25 pages | **passe** : deux lectures (20 pages au plus par lecture), trouve la phrase de la page 23. 0,148 $ pour 25 pages presque vides : le rendu en images coûte | [pdf-25-pages](preuve-corpus/pieces-non-textuelles/traces/pdf-25-pages.md) |
| le même, sans poppler dans le `PATH` | **casse** : au-delà de 10 pages, `Read` exige `pages`, qui exige `pdftoppm` (« pdftoppm is not installed ») ; rien lu, rien inventé | [sans-poppler](preuve-corpus/pieces-non-textuelles/traces/pdf-25-pages-sans-poppler.md) |
| PDF scanné (une image, aucun texte) | **passe** : lu comme document (sans `pages`), citation exacte | [pdf-scanne](preuve-corpus/pieces-non-textuelles/traces/pdf-scanne.md) |
| `.xlsx` (2 onglets, formules, date, fusion) | **casse** : « This tool cannot read binary files » ; ne répond à rien, n'invente rien, propose un CSV | [xlsx](preuve-corpus/pieces-non-textuelles/traces/xlsx.md) |
| le même converti en CSV | **passe** : tout lu, cite `budget-t3.T3.csv:6` ; `Read` numérote les lignes | [csv-converti](preuve-corpus/pieces-non-textuelles/traces/csv-converti.md) |

Ce qui en découle pour la création du dossier :

1. **Tableur : conversion obligatoire**, un CSV par onglet (`<classeur>.<onglet>.csv`), valeurs calculées et non formules, dates en ISO d'après les styles, cellule fusionnée = valeur dans la première, formule sans valeur calculée signalée (fichier jamais ouvert dans un tableur). Faisable en bibliothèque standard (`zipfile`, `xml.etree`) : l'essai [`xlsx_vers_csv.py`](preuve-corpus/pieces-non-textuelles/xlsx_vers_csv.py) (115 lignes) donne le même contenu que LibreOffice sur le classeur de test et sur sa copie réenregistrée par LibreOffice. Perdus : les formules elles-mêmes, les formats (k€), les commentaires de cellule, les graphiques. `.xls` et `.ods` : non couverts, à refuser avec un message (« enregistrez en .xlsx ou .csv »).
2. **PDF : gardé tel quel**, Claude le lit, scans compris. Mais un PDF de plus de 10 pages demande poppler sur le poste : la création du dossier doit le vérifier (nombre de pages, `pdftoppm` présent) et le dire, avec la commande d'installation. Pas d'extraction de texte fiable en bibliothèque standard ; `pdftotext` demande poppler aussi.
3. **Citer** (§5) : `fichier:ligne` vaut pour le texte et le CSV ; pour un PDF, c'est `fichier, p. N` (et l'article). La consigne de l'exécuteur doit le dire selon le type de pièce.
4. **Trace mécanique** : confirmée. En `stream-json`, chaque `Read` apparaît avec son chemin, ses `pages` et la réponse de l'outil, erreurs comprises : de quoi comparer à la section `sources_read` déclarée.
5. Non testés : `.docx` (probablement refusé comme binaire ; c'est aussi du zip + XML, convertible en bibliothèque standard), images seules (`.png`, `.jpg`), pièces très lourdes.

Incident utile, hors corpus : sur le CSV, Sonnet a signalé comme faux un total juste (« 1 900 » pour 960 + 720 + 120 + 30 + 90, qui font 1 920). Une addition de tête fausse, présentée comme une anomalie à vérifier : un argument de plus pour `calc-check`, qui recalcule au lieu de lire.

### 9.4 Recommandation

**Coder le corpus en ligne de commande comme au §5, ajusté.** Le test de dérive ne montre pas le risque qui aurait fait renoncer (une étape qui refait le regroupement avec le corpus et pas sans), et montre le gain attendu. Ajustements :

1. **Conversion à la création du dossier** (`new --corpus`) : `.xlsx` → un CSV par onglet, en bibliothèque standard ; PDF gardé, avec la vérification de poppler au-delà de 10 pages ; texte gardé ; tout autre binaire refusé avec un message. Les étapes voient les pièces converties ; l'original reste dans `corpus/` pour l'humain (proposition).
2. **Citer selon le type** : `fichier:ligne` pour le texte et le CSV, `fichier, p. N` pour le PDF, ou l'identifiant que la pièce porte déjà (`N012`).
3. **Guillemets contrôlés** : la consigne dit qu'un passage entre guillemets est une citation exacte d'une pièce ; l'exécuteur cherche chaque passage entre guillemets dans le corpus et signale ceux qu'il ne trouve pas (le contrôle de fuite à l'envers, bibliothèque standard).
4. **Missions** : une étape qui produit et reçoit le corpus dit en toutes lettres ce qu'elle ne refait pas (« the groups are decided ») ; `concepteur-recette` l'écrit ainsi, et borne le nombre de groupes de l'étape amont au plafond de l'étape aval.
5. **Moteurs** : le droit par copie tient avec Claude, et avec Codex depuis le plugin 2.13.0 (profil de permission, §4), sauf `/tmp` et `/var/tmp`. Antigravity et Vibe restent à tester. La page et la ligne de commande le disent au choix du moteur.

**Reste à décider par Amiel** : jouer d'abord le cas d'une mission vague (sans « ne regroupe pas »), ou le couvrir par le point 4 et le vérifier sur le premier vrai dossier en ligne de commande ; garder ou non l'original à côté des pièces converties. Antigravity se rejoue quand son quota revient (vers le 2026-10-19), Vibe quand il a du crédit ([`rejouer.sh`](preuve-corpus/antigravity-vibe/rejouer.sh)).
