# Interface de suivi des parcours (lot 3)

Conception v0 du 2026-10-15, révisée après une relecture adverse (Fable) avant implémentation ; implémentée le jour même (`scripts/interface.py`, `scripts/interface.html`, tests dans `tests/test_interface.py` — voir §8 pour ce qui s'écarte de la conception). Refaite le même jour en **version produit** (§3) : on y crée ses dossiers, on lit chaque livrable comme un document mis en forme, et la mécanique (moteurs, coûts par étape, champs transmis, messages reçus, journal) est masquée derrière un interrupteur « Détails techniques ». Elle s'adresse à la personne qui utilise les recettes, sans ligne de commande ; le partage avec un client ou un collègue viendra plus tard.

## 1. Principes

1. **L'exécuteur reste la seule source de vérité.** La page ne réimplémente rien : chaque action appelle `scripts/parcours.py` (même code, mêmes contrôles d'isolation, même `state.json`). Ce qu'on peut faire dans la page, on peut le faire en ligne de commande, et inversement.
2. **Local et fermé.** Un serveur Python de la bibliothèque standard (`ThreadingHTTPServer`, pour que le suivi ne gèle pas pendant une action), lié à `127.0.0.1`, sur un **port fixe** par défaut (8765, modifiable). Lier à 127.0.0.1 ne protège ni du navigateur ni des autres sessions du Mac, d'où :
   - un **jeton** aléatoire conservé dans un fichier en mode 0600 (stable entre relances), transmis à la page dans le **fragment** de l'URL (`#t=…`, jamais envoyé au serveur), gardé en mémoire de la page, et **exigé en en-tête `X-Parcours-Token` sur toutes les routes `/api`, lecture comprise** — une page piégée qui ferait pointer un nom vers 127.0.0.1 (DNS rebinding) ne lit rien ;
   - l'en-tête `Host` doit valoir `127.0.0.1:<port>` ou `localhost:<port>` ;
   - aucune réponse à `OPTIONS`, aucun en-tête CORS ; un POST sans `Content-Type: application/json` est refusé ;
   - en-têtes `Content-Security-Policy: default-src 'none'; script-src 'nonce-…'; style-src 'nonce-…'; connect-src 'self'` et `Referrer-Policy: no-referrer`.
3. **Les sorties des moteurs sont du texte non fiable** (elles peuvent reprendre un cahier des charges hostile). Le rendu échappe `& < > " '` avant tout et n'insère jamais de HTML brut ; il gère titres, listes (cases à cocher, numérotation de départ), gras, italique, barré, blocs de code, citations et tableaux, et se replie sur `<pre>` sinon. Aucune image ; un lien n'est rendu que pour une adresse `http(s)` et s'ouvre dans un nouvel onglet sans référent (`rel="noopener noreferrer"`). Le message exact reçu par une étape (`.in.md`) s'affiche en `<pre>`. Le rendu est testé sous node (`RendererTests`).
4. **Arguments contrôlés.** Slug, nom d'étape et nom de fichier passent une liste blanche (`^[a-z0-9][a-z0-9.-]{0,79}$` pour les fichiers, sans `.lock` ni fichiers temporaires), doivent exister dans le dossier du parcours, et le chemin résolu doit rester dedans ; les appels à `parcours.py` passent `--` avant les arguments positionnels et `--parcours-dir` en chemin absolu.
5. **Aucune dépendance nouvelle.** Python : bibliothèque standard + `pyyaml` (règle du dépôt). Page : un seul fichier HTML, CSS et JavaScript sans framework ni appel externe — elle doit marcher hors ligne.
6. **Les appels longs ne bloquent pas la page et survivent au serveur.** `next` tourne dans un processus détaché (`start_new_session`), sa sortie va dans `<parcours>/.next.log` (relu par la page) — jamais dans un tube vers le serveur, pour qu'un arrêt du serveur ne casse pas un appel payant. « En cours » se détecte par le verrou du parcours (`parcours.py status --json` expose `locked`), pas par une table en mémoire : un redémarrage du serveur retrouve un `next` qui tourne. La page affiche depuis quand l'état a été lu et signale un serveur injoignable.
7. **Le plan lancé est celui calculé, et le coût reste visible.** Dans la version produit, « Valider et continuer » enchaîne le geste (valider, répondre, choisir, refaire) puis le lancement, sans écran de confirmation intermédiaire : la carte d'action nomme d'avance les étapes qui vont tourner jusqu'à la prochaine relecture ; le plafond engagé s'affiche en mode technique, le coût cumulé dans l'en-tête du dossier. Sous le capot, rien ne change : La page appelle `parcours.py plan --json` (sans rien écrire), qui renvoie les étapes jusqu'à la prochaine pause, moteur, modèle, taille des entrées, le **plafond engagé** (étapes Claude × plafond par appel × 2 pour la relance éventuelle), le nombre d'appels Codex/agy (abonnements, non chiffrés), un avertissement si agy reçoit le message en argument (visible dans `ps`), et une **empreinte** de l'état (`state.json` + fiche). Confirmer appelle `next --yes --if-state <empreinte>`, revérifiée sous le verrou : si l'état a changé entre-temps, rien n'est lancé. Le coût cumulé s'affiche « X $ Claude + N appels Codex/agy ».
8. **Le moteur `fake`** n'apparaît que si le serveur est lancé avec `--dev`.

## 2. Lancement

```bash
python3 scripts/interface.py [--parcours-dir ~/.ix-recipes/parcours] [--port 8765] [--theme <dossier>] [--dev] [--no-browser]
```

**Depuis le plugin installé**, sans clone : `build.py` copie `scripts/parcours.py`, `interface.py` et `interface.html` dans `dist/skills/suivi-parcours/scripts/` (champ `scripts` du skill) et écrit à côté de chaque recette son `recipe.json` (le bloc `workflow`, l'id, le libellé, la version, `summary_fr`) ; l'exécuteur ainsi embarqué lit les recettes dans les dossiers voisins et tourne sur la bibliothèque standard seule (`pyyaml` est facultatif). Le skill `suivi-parcours` démarre la page quand on le demande à Claude. Testé avec le Python 3.9 de macOS, `yaml` bloqué. **Thème** (`--theme <dossier>` ou `$PARCOURS_THEME`) : le dossier contient un `theme.css`, ajouté après les styles de la page (il redéfinit ses variables `--bg`, `--primary`, `--sans`… et peut restyler ses classes), et ses polices ou images (`.ttf`, `.otf`, `.woff`, `.woff2`, `.svg`, `.png`), servies sous `/theme/<fichier>` sans jeton (une feuille de style ne peut pas en envoyer), noms contrôlés, sans sortir du dossier ; la CSP ajoute alors `font-src 'self'; img-src 'self'`. Par défaut, la page prend le thème **Inflexion** livré avec elle (`themes/inflexion/`, copié dans le plugin sous `scripts/themes/inflexion/` ; polices Archivo, Source Sans 3 et IBM Plex Mono sous SIL OFL 1.1, licences jointes) ; `--theme none` (ou `PARCOURS_THEME=none`) rend l'apparence neutre, et un autre dossier de thème remplace Inflexion. Les dossiers sont rangés par défaut dans `~/.ix-recipes/parcours`, un dossier caché qui n'encombre pas le dossier personnel (`$PARCOURS_DIR` s'il est défini ; l'ancien défaut `~/Parcours` reste utilisé tant qu'il contient des dossiers et que le nouveau n'existe pas, et la page invite alors à le déplacer), quel que soit l'endroit d'où l'on lance la page ; l'exécuteur en ligne de commande garde `./parcours` par défaut (ou `$PARCOURS_DIR`). Le serveur affiche l'URL (avec le jeton, `http://127.0.0.1:<port>/#t=…`) et l'ouvre dans le navigateur, sauf `--no-browser`. `--port 0` laisse le système choisir. `--dev` ajoute le moteur `fake` à la liste des moteurs (il lit `PARCOURS_FAKE_DIR`, comme l'exécuteur). Le jeton est dans `<dossier des parcours>/.interface-token` (0600), le même d'une relance à l'autre ; il n'est conservé dans la page que pour l'onglet (sessionStorage) et retiré de la barre d'adresse dès le chargement.

## 3. Ce que montre la page (version produit)

Une recette s'appelle ici un **dossier** pour la personne qui l'utilise. Trois écrans.

- **Vos dossiers** (`#/`) : des cartes groupées en « À traiter » (une relecture, des réponses ou un choix attendus, une étape à reprendre), « En cours », « Terminés », « Arrêtés ». Chaque carte : titre, recette, une phrase d'état (« À valider : Décision de répondre »), une barre de progression par étape, la dernière activité. État vide : une invitation à créer le premier dossier.
- **Nouveau dossier** (`#/nouveau`) : choix de la recette (cartes : `label` et `summary_fr` de la recette), titre facultatif, la demande collée ou importée d'un fichier texte (glisser-déposer accepté ; un PDF ou un Word se copie-colle), puis « Créer et démarrer » — la première étape part aussitôt. Le moteur ne se choisit qu'en mode technique.
- **Un dossier** (`#/p/<slug>[/<étape>]`), mise en page tranchée par Amiel le 2026-10-15 (option A) :
  - à gauche, les étapes avec leur nom en français (`label` de la recette), une icône et un état lisible (« À valider », « Réponses attendues », « En cours… », « À reprendre », « Écartée », « Livrable final »), et « Votre demande » pour relire le texte de départ ;
  - en haut à droite, **une seule carte d'action**, celle de ce qui est attendu maintenant : « Valider et continuer » (avec « Refaire l'étape » et « Arrêter le dossier »), « Envoyer les réponses et continuer » (avec « Copier les questions » et un brouillon gardé dans le navigateur), le choix des étapes facultatives, « Reprendre » ou « Refaire » après un échec (seul « Refaire » quand l'échec vient d'un passage recopié de la demande), « Interrompre » pendant qu'une étape tourne, et « Votre livrable est prêt » à la fin. La carte nomme les étapes qui suivront jusqu'à la prochaine relecture ;
  - au centre, **le livrable de l'étape choisie, mis en forme comme un document** (texte en serif, tableaux, listes), sans les blocs HANDOFF, SUMMARY, CONTEXT SHEET ni l'en-tête YAML (`GET …/document/<fichier>`, extrait par `parcours.output_document`) ; outils Copier, Télécharger (`.md`), Imprimer ou PDF (une feuille de style d'impression ne garde que le document), et « Refaire » sur une étape jouée, y compris dans un dossier terminé ;
  - la **fiche de contexte** de l'étape 1 en tableau lisible (rubriques nommées par la recette, `context_labels` ; « not stated » affiché « non indiqué »), modifiable champ par champ quand c'est elle qu'on valide — elle passe alors au-dessus du document ; une liste se corrige à raison d'un élément par ligne ;
  - **Détails techniques** (interrupteur en haut, mémorisé dans le navigateur) : moteur et modèle, coût, horaires, mission, résumé et champs transmis, sortie brute, message exact reçu, relance, versions précédentes, journal, plafond de coût, et le choix du moteur des prochaines étapes.
- **Beaucoup de dossiers** : ce qui est à traiter ou en cours s'affiche toujours ; les groupes « Terminés » et « Arrêtés » montrent leurs 6 dossiers les plus récents et « Voir les N autres » ; au-delà de 12 dossiers, une recherche (titre, recette) filtre la liste. Un dossier terminé ou arrêté s'**archive** depuis sa page (`parcours.py archive`, déplacé dans `<dossier>/.archives/`, rien n'est effacé) et se **restaure** depuis « Dossiers archivés » (`#/archives`, `unarchive`). Le serveur ne relit un `state.json` que s'il a changé (cache par date et taille) : 300 dossiers se listent en une dizaine de millisecondes.
- Le titre de l'onglet porte l'état (« (À valider) … ») ; les confirmations passent par une boîte de dialogue, les erreurs par un bandeau en langage courant ; mode sombre et affichage téléphone (les étapes deviennent une frise horizontale).

### Version v0 (avant la refonte)

- **Liste des parcours** du dossier : recette, statut (`active`, `completed`, `stopped`), pause en attente, coût, appels par moteur, date ; un dossier sans `state.json` (création interrompue) est listé à part, sans erreur.
- **Un parcours** :
  - la frise des étapes : statut, moteur, modèle, coût ; les étapes optionnelles écartées apparaissent grisées ;
  - la **fiche de contexte**, éditable à une pause `validate` (enregistrée via `validate --context`, versions précédentes conservées) ;
  - pour chaque étape terminée : le résumé, les champs transmis, la sortie complète (rendu Markdown simple) et le message exact reçu (`NN-<étape>.in.md`) ;
  - le **panneau de pause**, selon le type :
    - `validate` : « Valider », « Valider avec la fiche corrigée », « Arrêter le parcours » (No-go) ; correction des champs d'une étape (`handoff --file`) ;
    - `answers` : bouton « Copier les questions » (sortie de l'étape), zone pour coller les réponses du tiers — **brouillon conservé dans le navigateur** tant qu'il n'est pas soumis, les réponses d'un acheteur arrivant souvent en plusieurs fois —, ou « Continuer sans réponses » ;
    - `choose` : cases à cocher pour les étapes optionnelles, ou « Les écarter » ;
    - signal de blocage : le texte du blocage, puis les mêmes gestes que `validate` ;
  - **Lancer la suite** : moteur du parcours (un changement **devient le défaut du parcours**, la page le dit), plan affiché, confirmation, exécution en arrière-plan ; bouton « Arrêter l'étape en cours » (tue le groupe de processus ; l'étape se reprend par `retry`) ;
  - après une **fiche corrigée** alors que des étapes l'ont déjà reçue, ou après un `rerun` : un bandeau liste les étapes concernées ou remises en file ;
  - en cas d'échec : le message d'erreur, « Réessayer » (`retry`) et « Fournir les champs à la main ».
- *Création d'un parcours* : hors v0, faite depuis dans la version produit.

## 4. Points d'entrée du serveur

| Méthode | Chemin | Effet |
|---|---|---|
| GET | `/` | la page |
| GET | `/api/parcours` | liste et résumé des parcours |
| GET | `/api/parcours/<slug>` | `state.json` + fiche + liste des fichiers |
| GET | `/api/parcours/<slug>/file/<nom>` | un fichier du dossier du parcours (lecture seule, noms contrôlés) |
| GET | `/api/parcours/<slug>/plan` | `parcours.py plan --json` |
| GET | `/api/parcours/<slug>/log` | `.next.log` |
| GET | `/api/parcours/<slug>/document/<nom>` | le document d'une sortie d'étape, sans ses blocs de fin ni son en-tête YAML (`{document, meta}`) |
| GET | `/api/recipes` | `parcours.py recipes --json` : recettes-workflows, libellés, étapes (+ `page`) |
| GET | `/api/version` | `{"version", "recipe_formats"}` : la version de la page et les formats de recette qu'elle joue (aussi sous `page` dans `/api/parcours` et `/api/recipes`) |
| POST | `/api/parcours` | créer un dossier : `{"recipe", "text", "title"?, "engine"?}` → `parcours.py new --input -` (texte sur l'entrée standard) |
| POST | `/api/parcours/<slug>/<action>` | `next` (avec l'empreinte), `stop`, `validate`, `answer`, `choose`, `retry`, `rerun` |

Toutes les routes `/api` exigent le jeton ; les réponses d'erreur reprennent le message de `parcours.py` (format JSON), un code de sortie 2 (erreur d'arguments) étant traité comme un bug de l'interface.

Les POST exigent le jeton (en-tête `X-Parcours-Token`) et un corps JSON ; les fichiers fournis (fiche, réponses, champs) sont écrits dans un dossier temporaire puis passés à `parcours.py`. Le nom de fichier demandé en lecture ne peut pas sortir du dossier du parcours.

### Version de la page (ajouté le 2026-10-16)

La page a sa propre version, `PAGE_VERSION` dans `scripts/interface.py` (1.0.0 au 2026-10-16, 1.1.0 avec le format 2 le même jour, 1.1.1 quand le concepteur n'annonce plus que les skills de vérification présents dans le catalogue), distincte de celle du plugin (`dist/.claude-plugin/plugin.json`) et de celle du skill `suivi-parcours`. Elle couvre le serveur, `interface.html` et l'API. Elle s'affiche discrètement en bas de la page (« Page de suivi 1.1.0 · recettes au format 1, 2 », écrit par le serveur dans la page, masqué à l'impression), au démarrage du serveur, et dans l'API (`GET /api/version`, et `page` dans `/api/parcours` et `/api/recipes`). Elle se relève en x.y.z : **majeure** quand un appelant de l'API (la page d'une autre version, le futur serveur MCP) doit changer — une route ou un champ retiré ou changé de sens, un format de recette qu'elle cesse de lire ; **mineure** pour une fonctionnalité ou une route de plus, ou un format de recette de plus ; **correctif** sinon. Chaque relève est notée dans la section « Page » du CHANGELOG.

Les formats de recette joués sont ceux de l'exécuteur qu'elle embarque (`parcours.RECIPE_FORMATS`, [format-recette.md](format-recette.md) §2bis). Une recette personnelle d'un format trop récent n'est pas proposée à la création ; la demander répond 422 `recipe_refused` avec le message de l'exécuteur (« mettez la page à jour ») ; dans « Mes recettes », elle est marquée « Mettez la page à jour pour la lancer » (`format_error` dans `recettes.py list`), au lieu du conseil de la modifier.

## 5. Concurrence

Le verrou de `parcours.py` empêche deux exécutions simultanées sur un même parcours ; la page affiche « étape en cours » et désactive les actions tant qu'un `next` tourne. Un seul `next` en arrière-plan par parcours ; son journal (sortie de la commande) est consultable dans la page.

## 6. Ce que l'exécuteur a dû ajouter (fait, voir [`executeur.md`](executeur.md) §5)

- `plan <slug> --json` : le plan sans rien écrire (ni verrou, ni `.lock`, ni état) ;
- `status <slug> --json` avec `locked` (sonde non bloquante du verrou) ;
- `next --if-state <empreinte>` vérifié sous le verrou ;
- `--json` / `--json-errors` : erreurs en `{"error": code, "message": …}` sur la sortie standard, code de sortie 1, pour que l'interface ne lise pas le texte français ;
- un gestionnaire de SIGTERM dans `next`, pour que « Arrêter l'étape en cours » tue aussi l'appel au moteur (chaque moteur tourne dans sa propre session, un simple `kill` du `next` le laisserait orphelin et payant).

## 7. Hors v0

Serveur MCP « parcours » ; partage en lecture seule ; moteur différent par étape ; `rerun --extra` et correction des champs (`handoff --file`) depuis la page ; `answer --append` pour compléter des réponses déjà soumises ; comparaison d'une étape sur deux moteurs ; notifications.

## 8. Ce qui est construit, et où cela s'écarte de la conception

**Fichiers.** `scripts/interface.py` (serveur, bibliothèque standard + l'import de `parcours.py` pour des lectures seulement : la sonde `is_locked`, les libellés de `load_recipe` dans la liste, `output_document` pour le document d'une étape), `scripts/interface.html` (page unique, CSS et JS en ligne, aucune requête externe, aucun `style=` ni `on…=` en ligne : la CSP les bloquerait), `tests/test_interface.py`.

**Routes** (toutes sous `/api`, jeton exigé) : `GET /parcours` (liste ; les dossiers sans `state.json` dans `without_state`, ceux dont l'état est illisible dans `broken`), `GET /parcours/<slug>` (= `status --json` + moteurs proposés + dossier), `GET /parcours/<slug>/plan[?engine=…]`, `GET …/file/<nom>`, `GET …/log` (queue de `.next.log`), `POST …/<action>` avec un corps JSON :

| action | corps |
|---|---|
| `next` | `{"fingerprint": "<64 hex>", "engine": "claude"}` (moteur facultatif) ; réponse `{"started", "finished"}` |
| `stop` | `{}` |
| `validate` | `{}`, `{"stop": true}` ou `{"context": {…}}` |
| `answer` | `{"text": "…"}` ou `{"none": true}` |
| `choose` | `{"run": ["explorer", …]}` ou `{"skip": true}` |
| `retry` | `{}` |
| `rerun` | `{"step": "<id>"}` |

Les erreurs sont `{"error": code, "message": …}` : 400 argument refusé par l'interface, 403 jeton/Host/Origin, 404 introuvable, 405 méthode, 409 verrou pris ou état changé (`locked`, `state_changed`, `running`, `not_running`, `not_owned`), 415 pas du JSON, 422 refus de l'exécuteur (message repris tel quel), 500 bug de l'interface (code de sortie 2 de `parcours.py`) ou erreur inattendue.

**`next` détaché.** Lancé avec `start_new_session=True`, sortie dans `<parcours>/.next.log`, pid dans `<parcours>/.next.pid`. Le serveur le surveille 2,5 s : un refus immédiat (état changé, verrou pris, étape en échec rapide) revient en erreur dans la réponse ; sinon `finished: false` et la page suit par le verrou. Une table en mémoire (un `Popen` par parcours) n'empêche que le double lancement dans la seconde de démarrage, avant que le processus ait pris le verrou ; « en cours » reste lu sur le verrou. `stop` exige : verrou tenu, `.next.pid` désignant un processus vivant qui dirige son groupe et dont la ligne de commande est `parcours.py … <slug>` (un pid recyclé est refusé), puis SIGTERM au groupe, SIGKILL après 15 s ; l'étape reste `running` et se reprend par `retry`. Un verrou tenu par un `next` lancé depuis un terminal n'est pas arrêté depuis la page (`not_owned`).

**Écarts.**
- La liste des parcours lit `state.json` directement (et la sonde `is_locked`) au lieu d'appeler `status --json` par parcours : un sous-processus par parcours toutes les 3 s aurait été lourd. Les actions et la vue d'un parcours passent bien par `parcours.py`.
- **Correction des champs (`handoff --file`) : pas dans la page** (§7 le met hors v0 ; §3 le mentionnait). Sur une étape en échec, la page propose « Réessayer » et affiche la commande `handoff` à copier pour « fournir les champs à la main ».
- Les bandeaux « fiche corrigée alors que des étapes l'ont reçue » et « étapes remises en file » sont calculés par le serveur (état avant/après l'action), pas lus dans le texte de l'exécuteur ; ils sont conservés en mémoire de la page jusqu'à « Fermer ».
- « Refaire cette étape » (`rerun`, sans `--extra`) est proposé sur toute étape terminée, en pause ou en échec.
- Un POST dont le corps dépasse 4 Mo est refusé ; un fichier lu depuis la page est tronqué à 2 Mo ; l'en-tête `Origin`, s'il est présent, doit être celui du serveur (en plus du jeton).
- La CSP ajoute `base-uri 'none'; form-action 'none'; frame-ancestors 'none'` à celle de la conception.
- Le moteur `vibe` est proposé (marqué « non testé ») avec claude, codex et agy.
- La sonde de verrou (`flock` partagé non bloquant, relâché aussitôt) peut, une fois sur plusieurs milliers, faire échouer au même instant une commande lancée depuis un terminal avec « verrou pris » : il suffit de la relancer.

## 9. Recettes personnelles (ajouté le 2026-10-15)

Demande d'Amiel : créer une recette personnelle depuis la page, hors du dépôt — partir d'un besoin, regarder le catalogue, modifier la recette, la tester, la ranger dans le recueil de l'utilisateur une fois validée, et pouvoir la proposer au dépôt par git. Code : `scripts/recettes.py` (commandes), `scripts/parcours.py` (lecture, vérification, moteur `simulation`), `scripts/interface.py` (routes `/api/recettes`, `/api/essais`), `scripts/interface.html` (écrans « Recettes »). Tests : `tests/test_recettes.py`, `RecipeBookTests` dans `tests/test_interface.py`.

### 9.1 Où sont les fichiers (tranché)

```
~/.ix-recipes/recettes/                     le recueil : vos recettes, hors du dépôt
  <id>.md                                   une recette validée, au format de skills/<id>.md
  .versions/<id>.<date>.md                  les versions remplacées ou retirées (rien n'est effacé)
  brouillons/<brouillon>/                   une recette en cours
    brouillon.json                          état : titre, verdict du concepteur, conception (moteur, coût, erreur), origine, validation
    besoin.md                               le besoin collé (lu par le concepteur seulement)
    conception.in.md, conception.md         le message exact envoyé au concepteur, sa réponse (versions .vN gardées)
    recipe.md, recipe.vN.md                 le fichier de la recette, ses versions précédentes
    essais/<slug>/                          les dossiers de test : un dossier des parcours à part entière
  .contribution/                            les propositions au dépôt : état par recette, copies de travail, clones
```

Le recueil se déduit du dossier des parcours (`recueil_dir`), sans réglage de plus : `parcours.py`, `recettes.py` et la page le trouvent sans option. Tranché le 2026-10-15, avec le passage des dossiers dans `~/.ix-recipes/parcours` (« rien de visible dans le dossier personnel ») :

- dossier des parcours nommé `parcours` → le recueil est **à côté** : `~/.ix-recipes/parcours` → `~/.ix-recipes/recettes` (défaut de la page), `./parcours` → `./recettes` (défaut de la ligne de commande ; ignoré par git) ;
- autre nom (un ancien `~/Parcours` encore utilisé, un `$PARCOURS_DIR` choisi) → **dedans** : `<dossier>/recettes`, pour ne rien créer dans un dossier que l'utilisateur n'a pas choisi. Le nom `recettes` y est alors réservé : aucun dossier ne le prend (`new --slug recettes` donne `recettes-dossier`), la liste des dossiers l'ignore.

Un `~/Parcours/recettes` créé avant le passage à `~/.ix-recipes` n'est pas déplacé : il reste lu tant que la page sert `~/Parcours`.

### 9.2 Lire et jouer une recette personnelle

- **Ordre de recherche** (`recipe_origin`) : le dépôt ou le plugin d'abord — une recette personnelle ne masque jamais une recette livrée —, puis le brouillon en essai, puis le recueil. Un fichier du recueil dont l'en-tête porte un autre id est refusé.
- **Sans pyyaml** : le fichier est lu par un lecteur YAML de la bibliothèque standard (`load_yaml_subset` : correspondances et listes en bloc, listes et objets entre crochets, chaînes simples, entre guillemets ou en bloc `|` `>`, commentaires ; ancres, alias et étiquettes refusés), le même en développement et dans le plugin. Testé contre pyyaml sur tous les en-têtes d'ix-recipes et d'ix-skills. Il sert aussi de repli quand pyyaml manque pour les recettes du dépôt (les 19 tests de l'interface qui échouaient sans pyyaml, `HOME` changé, passent désormais).
- **Dossier de test** : un dossier des parcours dont le chemin est `<recueil>/brouillons/<b>/essais` voit aussi le brouillon `recipe.md`, sous l'id de son en-tête (`recipe_places`). Ailleurs, le brouillon n'existe pas.
- `parcours.py recipes [--json]` liste les recettes personnelles avec `personal: true` et `origin` (`plugin`, `personal`, `draft`) ; une recette du recueil illisible, invalide ou masquée n'est pas proposée et figure dans `personal_problems` (id, raison).
- `state.json` garde `recipe_sha256` (empreinte du fichier joué) et `recipe_origin` ; `status --json` dit `recipe_current` : l'essai a-t-il joué la version actuelle ?

### 9.3 Concevoir (`recettes.py design`)

**En deux temps, ajouté le 2026-10-15 à la demande d'Amiel** (« montrer visuellement la recette pour permettre de la commenter ; si on valide le principe, on code ») :

1. `design --mode propose` (défaut) : le concepteur rend son verdict et, si une recette se justifie, une **proposition** seulement — un bloc JSON (titre, résumé, rubriques de la fiche de contexte, étapes : id, nom, skill, rôle, entrées, ce qu'elle produit, pause, facultative) —, sans fichier. La page l'affiche comme un enchaînement d'étapes (onglet « Proposition »), avec un commentaire possible par étape et un commentaire sur l'ensemble (gardés dans le navigateur jusqu'à l'envoi). `proposition.json` ; les versions précédentes en `proposition.vN.json`.
2. « Revoir avec mes commentaires » : `comments` enregistre `commentaires.json`, puis `design --mode revise` envoie la proposition précédente et les commentaires ; la nouvelle version garde `after_comments`, et les commentaires envoyés passent en `commentaires.vN.json`. Autant d'allers-retours qu'il faut, un appel chacun.
3. « Valider le principe et écrire la recette » : `design --mode write` envoie la proposition validée et demande le fichier complet qui la suit exactement. Refusé tant que la proposition a un défaut que la recette aurait aussi (`proposal_problems` : skill hors du catalogue, entrée impossible, champ non produit plus haut, étape 1 sans `brief`, plus de 6 étapes). Après l'écriture, l'écart entre le fichier et la proposition (étapes, skills, pauses) est relevé (`drift`) et affiché au-dessus des onglets. Le fichier se retouche ensuite dans l'éditeur, comme avant.

Relancer une proposition sur un brouillon qui a déjà son fichier le met de côté (`recipe.vN.md`) : on repart de la chaîne. « Partir du modèle » et « Modifier » (une recette du recueil) passent directement au fichier.

Ce qui suit décrit l'appel lui-même, commun aux trois modes.

Un appel moteur neuf, comme une étape : dossier jetable, message par l'entrée standard, `conception.in.md` écrit avant l'appel, coût compté. Le message contient le texte du skill `ix-recipes:concepteur-recette`, **le catalogue réel** (chaque skill résolu par l'exécuteur avec sa description : `IX_SKILLS_PATH`, dépôt voisin, cache du plugin — **version en cours seulement**, un skill qu'une ancienne version en cache garde encore n'est pas proposé ; ni `concepteur-recette`, ni `suivi-parcours`, ni `configuration-ix`), le modèle de recette comme référence de format, le besoin, et la consigne de sortie : la recette dans un bloc de code ouvert par quatre accents graves, puis un bloc `## VERDICT` (`recipe`, `single_skill`, `manual_sequence`, `catalogue_gap`). Modèle Opus par défaut (un jugement sur tout le travail : la règle de l'étape 1).

- Le bloc dont le contenu commence par `---` devient `recipe.md` (l'ancien gardé en `.vN`) ; la réponse sans ce bloc devient l'« Avis du concepteur ».
- **Un skill seul suffit** : la page l'écrit en tête (« Le concepteur ne propose pas de recette — son avis : un skill seul suffit »), montre la réponse, et propose « Concevoir quand même une recette » (`design --insist` : un nouvel appel qui reçoit sa réponse précédente et la consigne de proposer la chaîne la plus courte) ou « Partir du modèle » (`template`).
- **Rien n'est inventé** : chaque skill de `requires` doit être dans ce catalogue, sinon l'enregistrement est en erreur (« le skill 'ix-skills:fiche-poste' n'existe pas dans le catalogue »). Constaté le 2026-10-15 sur un vrai besoin : le concepteur, qui voyait encore les anciennes versions en cache, avait cité `ix-skills:fiche-poste` ; d'où la règle « version en cours seulement ».
- Le moteur `simulation` ne conçoit rien (refusé) ; `fake` (en `--dev`) lit `PARCOURS_FAKE_DIR/concepteur-recette.md`.

### 9.4 Modifier : la même vérification que build.py

`check_recipe_text` (dans `parcours.py`) renvoie `errors` (bloquent l'essai et la validation), `contribution` (ce que le dépôt demande en plus : champs canoniques de CLAUDE.md §3, `version` en x.y.z, `domain` connu, `category: workflow` — bloquent seulement la proposition) et la vue lisible des étapes. Les erreurs :

- syntaxe de l'en-tête, avec la ligne du fichier ;
- id : minuscules sans accents, chiffres, tirets, et libre — ni recette du plugin, ni skill du catalogue (ix-skills ou ix-recipes) ;
- `workflow_errors` : **les règles de `validate_workflow` de build.py, une à une** (requires, ids uniques, skill cité dans le corps entre accents graves, mission, label, model, pause, output_field, verbatim, fiche de contexte à l'étape 1 seulement, brief à l'étape 1 seulement, champs reçus transmis par une étape antérieure, answers après une pause answers, context_labels, summary_fr), en français. `build.py` n'est pas modifié : `WorkflowCheckParityTests` compare les deux, sur toutes les recettes du dépôt et vingt variantes cassées de chacune (même nombre d'erreurs) ;
- ce dont l'exécuteur et la page ont besoin en plus : `transmits` non vide, skill avec son espace de noms, ids d'étape en minuscules, chiffres, tirets ou soulignés, `context_sheet` non vide.

Chaque enregistrement (`save --if-sha`) garde la version précédente et refuse d'écraser un fichier qui a changé depuis son ouverture (une nouvelle conception) : `state_changed`.

### 9.5 Tester

« Lancer l'essai » crée un dossier dans `essais/` (`parcours.py new --parcours-dir <brouillon>/essais`) avec l'exemple collé, puis le joue comme un vrai dossier : mêmes écrans, mêmes routes sous `/api/essais/<brouillon>/parcours/…`, mêmes contrôles d'isolation. Différences :

- **moteur `simulation` par défaut** (proposé seulement aux essais dans la page ; accepté par `parcours.py`) : aucun appel, coût nul, une sortie bien formée par étape — un document qui nomme les entrées reçues (jamais leur contenu, la demande brute ne doit pas voyager), la fiche de contexte, chaque champ à transmettre. On vérifie ainsi l'enchaînement, les pauses, la fiche. `fake` exige des sorties préparées par étape, inutilisable pour une recette neuve : d'où ce moteur ;
- un **essai réel** (Claude, Codex, agy, Vibe) se choisit dans le formulaire ; avant chaque lancement, la page montre les étapes jusqu'à la prochaine relecture, le moteur et le plafond engagé (`plan --json`, `ceiling_usd`), et attend « Lancer » ;
- un essai se **supprime** (`recettes.py essai-delete`, action `delete` réservée aux espaces d'essai ; un vrai dossier s'archive, jamais ne s'efface) ; supprimer le brouillon supprime ses essais ;
- un bandeau rappelle qu'il s'agit d'un essai et si la recette a changé depuis.

### 9.6 Valider : le recueil

« Valider dans mon recueil » (`recettes.py promote`) : refusé tant qu'il reste une erreur ; copie `recipe.md` vers `<recueil>/<id>.md` (version remplacée dans `.versions/`). Si le recueil a déjà ce id et que le brouillon n'en vient pas : refus `exists`, la page demande s'il faut remplacer (`--replace`). Sans essai concluant sur la version actuelle, la page demande confirmation. La recette apparaît dans « Nouveau dossier » avec la mention « Personnelle », se lance comme les autres ; « Modifier » la rouvre en brouillon (le même s'il n'a pas changé), « Retirer du recueil » la range dans `.versions/`. Les dossiers déjà créés avec une recette modifiée suivent la règle commune (`recipe_drift`).

### 9.7 Proposer au dépôt (`recettes.py contribute <id> prepare | push | cancel | status`)

1. **Préparer** (rien ne sort de l'ordinateur) : la recette doit être sans erreur et complète pour le dépôt. Source : le chemin d'un clone local d'ix-recipes, ou une adresse git (défaut : `https://github.com/amiel-35/ix-recipes.git`, clonée une fois dans `.contribution/clones/`) ; la dernière utilisée est retenue. Une **copie de travail à part** (`git worktree add`, dossier nommé `ix-recipes` pour que build.py y lise son espace de noms) sur une branche `recette/<id>` partie de `origin/HEAD` : le clone de l'utilisateur n'est pas touché. Refus si le dépôt a déjà `skills/<id>.md`. On y écrit `skills/<id>.md`, un `skills/<id>.mystaffy.json` minimal (catégorie workflow), on lance `build.py <id> --validate` puis `build.py <id>` (CLAUDE.md §5 et §7 ; un Python qui a pyyaml et jsonschema : `IX_RECIPES_PYTHON`, celui de la page, ou `python3`), on ajoute ces fichiers et `dist/skills/<id>/`, et on commite localement. La page montre le diff complet (`git show`) et le journal de build.
2. **Envoyer**, après confirmation dans la page : `git push -u origin recette/<id>`, refusé si la branche a bougé depuis le diff affiché ; puis, si l'adresse d'origin est sur GitHub et `gh` installé, `gh pr create` (titre, description qui rappelle que version du plugin, CHANGELOG et README restent au mainteneur). Sinon l'adresse de comparaison GitHub, ou la consigne d'ouvrir la demande à la main.
3. **Annuler / Terminer** : copie de travail et branche locale supprimées ; une branche déjà poussée reste sur le dépôt distant.

Ce qui échoue est dit en clair, sans rien laisser à moitié (la branche locale est retirée si la préparation échoue) : git absent (comment l'installer, ou envoyer le fichier au mainteneur), dépendances de build.py absentes (`pip install -r requirements.txt`, ou `IX_RECIPES_PYTHON`), identité git inconnue (les deux `git config`), envoi refusé (droits d'écriture : forker avec `gh repo fork … --remote`, la branche reste prête), réseau. git tourne sans invite (`GIT_TERMINAL_PROMPT=0`, ssh en `BatchMode`) : il échoue au lieu d'attendre un mot de passe que personne ne tape. Testé contre un dépôt nu jetable ; le chemin GitHub contre un faux `gh`.

### 9.7 bis Organigramme, recettes fournies, copie (retours d'Amiel du 2026-10-15)

- **Organigramme standard** (formes ISO 5807, de haut en bas) partout où une recette s'affiche — recette fournie, recette du recueil, brouillon, proposition : terminateurs Début / Fin, « Votre demande » en entrée (parallélogramme), chaque étape en processus prédéfini (un skill ; pointillés si facultative, trait épais pour la dernière), « Vous validez » en opération manuelle (trapèze), « Vous apportez les réponses » en entrée manuelle, les étapes facultatives derrière un losange de décision (Oui à droite, Non tout droit), le livrable en document. Dessiné par la page (SVG construit élément par élément, textes en `textContent`, aucune bibliothèque). Cliquer une étape affiche sa mission, ce qu'elle reçoit — les étapes d'où ça vient passent en vert — et ce qu'elle transmet ; dans une proposition, c'est là qu'on la commente (un point marque les étapes commentées). Le détail de toutes les étapes reste dépliable sous le schéma.
- **Page Recettes en trois blocs** : « Recettes fournies » (celles du plugin, lues par `parcours.py recipes`), « Mes recettes » (le recueil, avec un état vide qui invite à copier ou créer) et « Brouillons ».
- **Une recette fournie** (`#/recettes/f/<id>`, `recettes.py provided <id>`) : son organigramme, « Lancer un dossier » et « Copier pour modifier » (`recettes.py fork <id>`) : un brouillon avec le fichier de la recette sous un id libre (`<id>-perso`, puis `-perso-2`…), libellé « (ma version) », version 0.1.0 ; l'originale ne change pas. Dans le plugin, où seul `recipe.json` est livré, le fichier est reconstruit (`recipe.json` + corps du SKILL.md, `requires` déduit des étapes) : il est valide, et ce qui manque pour le dépôt (description_en, domain…) s'affiche comme d'habitude.
- **Une recette du recueil** : « Nouveau dossier avec cette recette », « Modifier », comme avant.

### 9.7 ter Cartes et construction en blocs (2026-10-15, « un système à la Scratch »)

Après comparaison avec l'organigramme, Amiel retient les **cartes** comme vue principale (lisibles par un non-spécialiste, texte entier, natives en HTML) et l'organigramme normé comme vue secondaire (bouton « Cartes / Organigramme », mémorisé dans le navigateur). Les cartes reprennent ce que l'organigramme exprime : « Votre demande » en tête, chaque étape en carte (bordure violette pour ix-skills, verte pour ix-recipes), les arrêts en blocs ambrés entre deux cartes, les étapes facultatives dans un bloc en C « Si vous choisissez de les jouer », le livrable cerclé ; un clic ouvre la carte (mission, entrées — les cartes d'où elles viennent s'éclairent — et, dans une proposition, le commentaire).

**Construire en blocs** (onglet « Blocs » d'un brouillon au stade de la proposition ; « Construire moi-même en blocs » sur Nouvelle recette ; « Retravailler en blocs » sur un brouillon qui a déjà son fichier) :

- une **palette** : le catalogue réel (`recettes.py catalogue`, mêmes racines que la conception), rangé en « Raisonnement (ix-skills) » et « Métiers (ix-recipes) », avec recherche ; des blocs « Vous validez », « Réponses d'un tiers » et « Si vous choisissez… » à déposer sur une étape ;
- on **clique** un skill (il s'ajoute à la fin, ou à l'endroit choisi par un « + ») ou on le **glisse** entre deux cartes ; une carte se déplace (glisser, ou flèches), se retire, se renomme, reçoit sa mission en une phrase, son arrêt, sa case « Facultative » (jamais la première) ; six étapes au plus ;
- le **câblage des données est automatique** : l'étape 1 lit la demande, chaque suivante reçoit la fiche de contexte, tout ce qu'ont produit les étapes au-dessus d'elle, et les réponses du tiers après une pause « réponses ». En « Réglages avancés », on renomme les champs transmis et on décoche ce qu'une étape ne doit pas voir (elle passe alors en câblage manuel) ;
- chaque changement est enregistré (`recettes.py proposal`, au fil de l'eau) et vérifié (`proposal_problems`) ;
- **« Écrire la recette »** (`recettes.py write-file`) produit le fichier sans appel au modèle : en-tête qui suit exactement la chaîne (l'étape 1 produit la fiche et s'arrête toujours ; la dernière étape non facultative donne le livrable ; Opus pour l'étape 1, Sonnet ensuite), corps d'orchestration générique (§4 du format), missions reprises des phrases saisies. Le fichier passe la vérification de build.py (testé). « Faire écrire par le concepteur » reste possible : il rédige en plus les missions.

Une proposition du concepteur se reprend aussi en blocs (« Modifier moi-même en blocs »). Une recette remise en blocs perd au réécrire ses retouches manuelles du corps : la page le dit avant.

### 9.7 quater Les étapes qui relisent la demande (format 2, 2026-10-16)

Une étape qui vérifie et déclare `reads_source` ([format](format-recette.md) §1.10) relit le texte de départ ; la page le montre partout où une recette s'affiche, pour que le circuit des données reste lisible :

- **cartes** : un badge vert « Relit votre demande » sur la carte (bulle d'explication au survol), et le bloc « Votre demande » dit qui le lit (« la première étape le lit, et l'étape « Vérification des faits » le relit pour vérifier (sans rien produire) ») ; sélectionner l'étape éclaire « Votre demande », comme la source de toute entrée ;
- **organigramme** : une pastille « relit votre demande » sur l'étape, une entrée de légende, et le même éclairage ;
- **détail d'une étape** (cartes, organigramme, liste dépliable) : « Reçoit » se termine par « votre demande, relue pour vérifier (le texte brut) » ;
- **listes de recettes** (Recettes fournies, choix de la recette d'un nouveau dossier) : « · vérifie sur votre demande » dans le pied de la carte ; le chapeau de « Nouveau dossier » nomme l'étape qui relira le texte ;
- **dossier** : « Source : relit votre demande pour vérifier » dans les détails techniques de l'étape (le message exact reçu montre le bloc `source`) ;
- **construction en blocs** : un skill qui vérifie (`verifies` dans `recettes.py catalogue`) déposé après une autre étape arrive coché « Relit votre demande pour vérifier » ; la case se décoche, et l'explication dit ce que l'étape perd sans elle et que la recette passe au format 2. Elle n'existe pas pour un skill qui produit ni pour l'étape 1 (une proposition venue d'ailleurs qui la coche sur une étape qui produit est signalée par `proposal_problems`). « Écrire la recette » écrit `reads_source: true` et `format: 2`, et le corps dit qu'aucune étape qui produit ne relit la demande ;
- **conception** : le message au concepteur porte la règle (poser `reads_source` sur une vérification placée après une étape qui produit, jamais ailleurs) et la forme de la proposition a le champ ; un fichier écrit avec `format: 1` et une étape qui relit la source passe en `format: 2` ; un oubli du réglage prévu par la proposition est signalé comme écart (« ne relit pas la demande, alors que la proposition le prévoyait »).

### 9.8 Routes ajoutées

| Méthode | Chemin | Effet |
|---|---|---|
| GET | `/api/recettes` | `recettes.py list` : recueil, brouillons, moteurs de conception |
| POST | `/api/recettes/brouillons` | `{need, title?, engine?}` → brouillon + conception détachée ; `{template: true}` → brouillon depuis le modèle |
| GET | `/api/recettes/brouillons/<b>` | `recettes.py show` (+ `essai_engines`) ; `…/log` : journal de la conception |
| POST | `/api/recettes/brouillons/<b>/<action>` | `proposal {proposal, replace_file?}`, `to-blocks`, `write-file`, `comments {comments}`, `design {mode?, comments?, insist?, engine?}`, `stop`, `save {text, sha?}`, `template`, `promote {replace?}`, `delete`, `essai {text, title?, engine?}`, `essai-delete {slug}` |
| GET | `/api/recettes/fournies/<id>` | `recettes.py provided` ; POST `…/fork` : `recettes.py fork` |
| GET | `/api/recettes/catalogue` | `recettes.py catalogue` : la palette des blocs |
| GET | `/api/recettes/personnelles/<id>` | `recettes.py personal` |
| POST | `/api/recettes/personnelles/<id>/<action>` | `edit`, `retire`, `contribute {step: prepare\|push\|cancel\|status, source?}` |
| GET/POST | `/api/essais/<b>/parcours/…` | les routes des dossiers, sur les essais du brouillon (création par `…/essai` seulement ; action `delete` en plus) |

Mêmes protections que le reste : jeton exigé partout, noms contrôlés (brouillon et essai : `^[a-z0-9][a-z0-9-]{0,79}$` ; recette : 60 caractères), chemins résolus sans lien symbolique ni sortie du recueil, une source de contribution refusée si elle commence par `-` ou contient un saut de ligne, valeurs passées en argument après `--`, jamais dans un shell. La conception tourne détachée comme `next` (journal `.design.log`, pid `.design.pid`, « en cours » lu sur le verrou du brouillon, « Interrompre » limité au processus lancé par la page). Les ids d'étape et les noms de fichiers acceptent désormais le souligné (`fiche_poste`), que le concepteur emploie volontiers.
