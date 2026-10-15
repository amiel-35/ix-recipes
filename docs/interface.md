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
| GET | `/api/recipes` | `parcours.py recipes --json` : recettes-workflows, libellés, étapes |
| POST | `/api/parcours` | créer un dossier : `{"recipe", "text", "title"?, "engine"?}` → `parcours.py new --input -` (texte sur l'entrée standard) |
| POST | `/api/parcours/<slug>/<action>` | `next` (avec l'empreinte), `stop`, `validate`, `answer`, `choose`, `retry`, `rerun` |

Toutes les routes `/api` exigent le jeton ; les réponses d'erreur reprennent le message de `parcours.py` (format JSON), un code de sortie 2 (erreur d'arguments) étant traité comme un bug de l'interface.

Les POST exigent le jeton (en-tête `X-Parcours-Token`) et un corps JSON ; les fichiers fournis (fiche, réponses, champs) sont écrits dans un dossier temporaire puis passés à `parcours.py`. Le nom de fichier demandé en lecture ne peut pas sortir du dossier du parcours.

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
