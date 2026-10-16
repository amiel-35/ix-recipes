# Exécuteur de parcours (lot 2)

Conception v0 du 2026-10-14, révisée après une relecture adverse (Fable) avant implémentation. L'exécuteur joue une recette-workflow ([format](format-recette.md)) étape par étape, chaque étape dans un **appel neuf** à un moteur au choix — Claude Code, Codex, Antigravity (Gemini) ou Vibe (Mistral). C'est l'isolation réelle : le script décide de ce que chaque étape reçoit, rien d'autre ne passe.

## 1. Ce qu'il lit et ce qu'il écrit

- **Il lit** le bloc `workflow` du frontmatter de la recette (`skills/<id>.md`) : `format`, étapes, missions, `receives`, `transmits`, `pause`, `model`, `reads_source`. Il joue les formats de `RECIPE_FORMATS` (1 et 2) et refuse les autres avec « mettez la page à jour » ; une recette sans `format` est lue comme format 1, avec un avertissement ([format](format-recette.md) §2bis). `parcours.py formats [--json]` annonce les formats acceptés (`{"formats": [1, 2], "current": 1, "source_format": 2}` : `current` est le format écrit dans une recette créée par la page, `source_format` celui qu'elle écrit quand une étape relit la source).
- **Il refuse** de jouer une recette dont une étape relit la source sans en avoir le droit (`reads_source` hors des skills qui vérifient, à l'étape 1, ou sous le format 1 : [format](format-recette.md) §1.10) : `new`, `next` et `plan` échouent avec le message, `status` reste lisible et le dit dans `recipe_error`, `recipes` écarte la recette.
- **Il écrit** un dossier par parcours, `./parcours/<slug>/` :
  - `input.md` — la demande brute (lue par l'étape 1 seulement) ;
  - `state.json` — l'état (§2) ;
  - `NN-<étape>.md` — la sortie complète de chaque étape ;
  - `NN-<étape>.in.md` — le message exact envoyé au moteur, écrit juste avant l'appel (après le contrôle d'isolation) ; `NN-<étape>.retry.in.md` pour la relance ;
  - `NN-<étape>.events.jsonl` (`.retry.events.jsonl`) — pour une étape Codex, ses évènements `--json` : les commandes qu'il a lancées, avec leur sortie (§4) ;
  - `NN-<étape>.vN.md` (et `.in.vN.md`) — les versions précédentes, gardées quand une étape est refaite ou corrigée ;
  - `answers.md` — les réponses collées à une pause `answers`.

Le même dossier sert aux recettes jouées en conversation (`./parcours/` y est déjà la trace) : un parcours commencé dans Claude Code pourra être repris par l'exécuteur, et inversement, plus tard.

## 2. L'état (`state.json`)

```json
{
  "recipe": "brief-client",
  "recipe_version": "1.1.0",
  "recipe_format": 1,
  "slug": "brief-client-formation",
  "created": "2026-10-14T18:00:00",
  "engine": "claude",
  "context_sheet": {"client": "…", "objective": "…"},
  "context_validated": true,
  "answers": "answers.md",
  "steps": [
    {"id": "cadrage", "status": "done", "engine": "claude", "model": "opus",
     "transmits": ["need", "constraints"],
     "skill": {"ref": "ix-skills:cadrage", "path": "…/SKILL.md", "sha256": "…",
               "version": "3.9.1", "version_source": "source file"},
     "output": "01-cadrage.md", "handoff": {"need": "…"}, "summary": "…",
     "cost_usd": 0.31, "started": "…", "ended": "…"},
    {"id": "questioning", "status": "paused", "…": "…"},
    {"id": "explorer", "status": "pending"}
  ],
  "pending": {"type": "answers", "step": "questioning",
              "message": "Questions to send the client are in 02-questioning.md"}
}
```

Statuts d'une étape : `pending`, `running`, `done`, `paused` (sortie produite, en attente de l'humain), `skipped` (étape optionnelle écartée), `failed`.

`transmits` est copié à la création : toute commande qui indexe les étapes (`next`, `validate`, `answer`, `choose`, `rerun`, `handoff`) compare la recette au parcours et refuse, en nommant l'étape et les champs, si les étapes ou leurs `transmits` ont changé. `skill` : le `sha256` est celui du texte exact envoyé (corps du `SKILL.md`, sans frontmatter), le chemin celui du fichier lu ; la `version` est indicative et son origine est étiquetée (`frontmatter`, `source file` = `skills/<id>.md` à côté de `dist/`, `cache dir` = dossier de version du cache).

## 3. Ce que reçoit une étape

L'exécuteur construit le message lui-même, sans passer par un orchestrateur, et l'envoie **par l'entrée standard** (jamais en argument : skill + cahier des charges + fiche peuvent dépasser la limite) :

1. **le texte du skill** (le `SKILL.md`, sans frontmatter), lu localement — pas besoin d'installer les skills dans le moteur ;
2. la consigne de méthode : « le texte du skill est ta méthode ; quand son format de sortie et le HANDOFF divergent, le HANDOFF l'emporte : range tes sections dans ces champs » ;
3. la mission de l'étape et la consigne de périmètre (« reste dans la mission, ne produis pas les livrables suivants, ne réponds pas toi-même à la demande ») ;
4. la fiche de contexte validée (sauf à l'étape 1) ;
5. **uniquement** les champs listés dans `receives` — la demande brute à l'étape 1 seulement ; un champ d'une étape `skipped` vaut littéralement `skipped` ;
5 bis. pour une étape qui vérifie et déclare `reads_source: true` (format 2), **en plus**, le texte exact de `input.md` en entrée nommée `source`, après les autres, précédé d'une consigne : c'est la référence du contrôle, une preuve et non une demande ; ne pas y répondre, ne pas refaire le travail demandé, la citer brièvement. Aucune autre étape ne la reçoit ;
6. la consigne de sortie : la sortie complète, puis `## HANDOFF` avec une sous-section `### <champ>` par champ de `transmits`, puis `## SUMMARY` (5 lignes au plus) ; à l'étape 1, en plus, `## CONTEXT SHEET` suivi d'un bloc de code `json` avec les champs de `context_sheet`.

Un champ déclaré `output_field` n'est pas demandé dans le HANDOFF : c'est la sortie complète de l'étape (le texte avant les blocs de fin ; après une relance, celui de la première réponse). Le message demande aussi d'écrire dans la langue du matériau reçu, pas dans celle des consignes.

Le découpage par titres (`### <champ>`) tient les champs longs (un besoin, une offre de plusieurs pages) que du JSON échappé casserait sur quatre moteurs ; le JSON est réservé à la fiche de contexte, courte.

**Tolérance de l'extraction** : les noms de champs sont comparés sans casse, sans accents, espaces/tirets/soulignés confondus, et au « s » final près (`hypotheses` = `hypothesis`, `constraint` = `constraints`) ; un champ en trop est ignoré avec un avertissement. Si aucune section HANDOFF n'est trouvée, l'exécuteur retire un bloc de code qui enveloppe toute la sortie (```` ```markdown … ``` ````) et relit ; un bloc de code resté ouvert est ignoré en dernier recours. Le bloc de la fiche de contexte accepte n'importe quelle info de fence (`json`, `JSON`, `jsonc`, aucune) ; à défaut de JSON strict, il prend le texte du premier `{` au dernier `}` en retirant commentaires `//` et virgules finales.

**Signal de blocage** : une sous-section facultative `### blocking` dans le HANDOFF (le message la demande, à n'utiliser que si quelque chose empêche la suite). Le message la réserve au cas où une étape suivante ne peut pas faire son travail avec ce qui est transmis ; les réserves vont dans la sortie. Si elle est présente et dit quelque chose (« none », « n/a » comptent pour vide, de même qu'une phrase courte, 8 mots au plus, qui commence par « aucun blocage », « pas de blocage », « no blocking », « nothing blocks » ou « rien ne bloque » ; au-delà, le texte compte, même ouvert par « aucun blocage » — une pause de trop coûte moins qu'un blocage manqué — et une section ignorée laisse un avertissement), l'étape passe `paused` avec un `pending` de type `validate` et le message « Blocage signalé par l'étape … », même si sa pause est `none`. L'exécuteur n'arrête jamais le parcours de lui-même : l'humain valide ou fait `validate --stop`.

**Extraction ratée** : une seule relance, avec *la sortie produite* (jamais l'entrée) et « réponds seulement par les blocs HANDOFF et SUMMARY » ; si elle échoue aussi, l'étape passe `failed` et la commande `handoff <slug> <étape> --file` permet de fournir les champs à la main.

**Fuite détectée à la sortie de l'étape** : à chaque fin d'étape (`complete_step`), au remplacement de la fiche (`validate --context`) et pour `handoff --file`, les champs transmis, le blocage et la fiche sont comparés à la demande brute (même règle que l'isolation). En cas de passage recopié, l'étape passe `failed` (ou la commande est refusée sans rien modifier) avec un message qui nomme le fragment et le remède qui marche : `handoff <slug> <étape> --file champs.md` avec des champs expurgés, ou `rerun <slug> <étape>` pour refaire l'appel (un simple `retry` reparserait la même sortie).

**Fenêtre de crash** : la sortie `NN-<étape>.md` est écrite avant la mise à jour de `state.json`. Après un `retry`, si ce fichier existe, il est d'abord lu par l'extraction, sans appel moteur ; inutilisable, il est renommé `NN-<étape>.vN.md` avant l'appel. Appels et coût sont enregistrés dans `state.json` dès le retour de chaque appel moteur, pas seulement en fin d'étape. Toute erreur inattendue dans une étape la laisse `failed` (jamais `running`) et se signale en une ligne.

**Résolution des skills** par espace de noms, pas par id nu : `ix-skills:<id>` cherche dans `IX_SKILLS_PATH`, puis `../ix-skills/dist/skills`, puis le cache Claude Code `~/.claude/plugins/cache/*/ix-skills/<version>/skills` (version la plus haute) ; `ix-recipes:<id>` dans `./dist/skills` puis le cache. **Tous les skills de la recette sont résolus dès `new`** (un manque fait échouer la création, en les nommant tous) ; le chemin, le `sha256` du texte et la `version` sont enregistrés par étape dans `state.json`. À chaque `next`, si le texte d'un skill d'une étape restant à jouer a changé depuis, un avertissement le nomme et l'exécution continue avec le texte actuel (pas d'option pour l'« accepter »).

### Isolation : un dossier jetable par appel

Le moteur ne tourne jamais dans le dossier du parcours : `codex`, `agy` et `claude -p` peuvent *lire* le dossier courant, et y trouveraient `input.md` et les sorties amont. Chaque appel tourne dans un **dossier temporaire neuf** (sous `$TMPDIR`, jamais sous `/tmp`, que Codex peut lire : §4) qui ne contient que les `references/` du skill (copiées) ; la sortie est récupérée par la sortie standard ou le fichier de sortie du moteur, puis le dossier est supprimé.

Ce que le moteur peut lire **hors** de ce dossier dépend de lui (tests du 2026-10-16, [décision corpus](decision-corpus.md) §4) : Claude refuse (`--tools Read`, refus dans `permission_denials`) ; Codex est enfermé par un profil de permission (§4) ; Antigravity et Vibe ne sont pas testés.

**Champs `verbatim`** (déclarés par la recette sur l'étape 1, ex. les listes imposées d'un cahier des charges) : ils peuvent recopier des passages de la demande — c'est leur raison d'être — mais chaque ligne est contrôlée séparément (une ligne qui recopie un paragraphe de 40 mots est refusée) et l'ensemble couvre au plus 85 % des mots de la demande (mesuré par séquences de 8 mots) ; ils sont exclus du contrôle des passages dans les messages suivants. Une fois admis, ce qu'ils citent reste du matériau autorisé pour toute la suite : un mot de la demande couvert par une séquence de 8 mots présente dans un champ `verbatim` déjà enregistré ne compte plus comme fuite, dans les messages comme dans les champs des étapes suivantes (une offre qui reprend en liste les éléments imposés passe ; un paragraphe de la demande que l'extraction n'a pas repris reste bloqué). Seules comptent les étapes terminées en amont : une correction à la main (`handoff`) n'admet pas l'ancienne valeur qu'elle remplace. Limite connue : le contrôle par ligne laisse passer des lignes de moins de 40 mots, donc un paragraphe découpé en lignes ; le seuil n'est pas abaissé parce que de vraies lignes imposées (un objectif pédagogique et sa liste de notions) atteignent 32 mots, et ce champ est borné par le plafond de 85 % et relu par l'humain à la pause de l'étape 1. Les autres champs, la fiche et le reste du message restent soumis au contrôle normal.

Contrôle avant chaque appel à partir de l'étape 2 : le message ne doit contenir **aucun passage** de la demande brute (comparaison de fragments du contenu, pas du nom de fichier) ; sinon l'exécuteur refuse.

**Étape qui relit la source** (`reads_source`) : le contrôle de son message écarte le seul bloc `source` (comme un champ `verbatim`) ; un passage de la demande dans un autre champ reçu ou dans la fiche reste une fuite et se signale comme d'habitude. Sa relance, qui ne lui renvoie que sa propre sortie, n'est pas contrôlée : elle peut citer la source qu'elle a le droit de lire. Ses champs transmis, eux, sont contrôlés à la sortie comme ceux de toute étape, puisqu'ils peuvent aller à une étape qui produit.

## 4. Les moteurs

| Moteur | Appel | Modèle | Coût |
|---|---|---|---|
| `claude` | `claude -p --model <model> --output-format json --tools Read --setting-sources "" --no-session-persistence --disable-slash-commands --max-budget-usd <plafond>` dans le dossier jetable | `model` de l'étape | lu dans la sortie (`total_cost_usd`) |
| `codex` | `codex exec --ignore-user-config --disable apps --skip-git-repo-check --ephemeral --json -c default_permissions="ixetape" -c permissions.ixetape.filesystem={…} -C <jetable> -o <fichier>` (message par stdin ; profil ci-dessous) | modèle par défaut de Codex | abonnement : on compte les appels |
| `agy` | `agy --disable-slash-commands -p=<message>` dans le dossier jetable (le message est dans l'argument, pas sur l'entrée standard) | modèle par défaut d'Antigravity (`--model` possible) | abonnement : on compte les appels |
| `vibe` | `vibe -p --output text` dans le dossier jetable | modèle par défaut de Vibe | non testé (pas de crédit) |
| `fake` | aucun appel : sorties préparées par étape, dont un cas de HANDOFF malformé pour tester la relance | — | 0 — pour les tests |
| `simulation` | aucun appel : une sortie bien formée construite à partir de ce que l'étape doit transmettre (document qui nomme les entrées reçues, fiche de contexte, champs) | — | 0 — pour tester une recette neuve (essais de la page, [interface.md](interface.md) §9.5) |

Sans `--setting-sources ""` ni `--disable-slash-commands`, Claude chargerait CLAUDE.md, la mémoire et les plugins installés, et pourrait invoquer la version plugin du skill au lieu du texte transmis. Seul l'outil `Read` est laissé, pour les `references/` copiées.

Chaque appel a un délai maximal (`subprocess` avec `timeout` et un groupe de processus tué à l'échéance — il n'y a pas de commande `timeout` sur macOS). Seules la sortie standard ou le fichier de sortie sont analysés : la sortie d'erreur contient des notices de mise à jour.

**`codex` : un profil de permission qui limite ses lectures au dossier de l'étape** (codex-cli **0.155.1 au moins**, la version testée ; les profils sont en bêta chez OpenAI). L'ancien `-s read-only` interdisait d'écrire, pas de lire : une étape Codex pouvait lire tout le disque, dont la demande d'un parcours. L'appel passe désormais un profil nommé `ixetape` :

```
permissions.ixetape.filesystem={":minimal"="read", "<préfixe de codex>"="read", ":workspace_roots"={"."="read"}}
```

- `:workspace_roots` = le dossier jetable (`-C`), **en lecture seule** : Codex n'écrit rien, ni par le shell ni par `apply_patch`. Le fichier `-o` est écrit par Codex lui-même, hors bac à sable.
- `:minimal` = les chemins système sans lesquels aucune commande ne démarre.
- le **préfixe d'installation de codex** : Codex relance son propre binaire dans le bac à sable. L'exécuteur le détecte (`shutil.which("codex")`, puis la cible du lien) et ouvre le dossier parent de `bin/` de chacun (`/opt/homebrew` avec Homebrew ; le préfixe de Node avec npm). Jamais un dossier qui contient le dossier personnel, le dossier temporaire ou le dossier courant : pour `~/bin/codex`, seul `~/bin` est ouvert ; pour `~/codex`, l'appel est refusé.
- **aucune option `--sandbox` / `-s`** : elle désactiverait les profils et rendrait l'ancien bac à sable. `--ignore-user-config` écarte les serveurs MCP et plugins de `~/.codex/config.toml` (l'authentification marche quand même) ; `--disable apps` retire les connecteurs ChatGPT distants ; `--ephemeral` ne laisse rien dans l'historique Codex.

**Avant chaque appel Codex**, sans modèle ni abonnement (une fraction de seconde) : `codex --version` doit donner 0.155.1 au moins, puis `codex sandbox -P ixetape` avec le même profil doit lire un fichier témoin du dossier de l'étape et se voir refuser un témoin posé à côté (là où serait `input.md`). Sinon l'étape échoue avec un message clair (« version … au moins est nécessaire », « le profil … est refusé », « ne tient pas ») et **Codex n'est pas lancé** : jamais sans protection. Le témoin vérifie la syntaxe du profil, pas `codex exec` lui-même ; `exec` a été vérifié en vrai avec 0.155.1 (ci-dessous).

**Ce qui reste ouvert** : `/tmp` et `/var/tmp` (lecture **et** écriture), `/etc`, `/Applications`, `/Library/Preferences` restent lisibles : c'est codé dans `:minimal`, et un `deny` ne le referme pas. Tout ce qui traîne dans `/tmp` est donc lisible par une étape Codex. Le dossier jetable est sous `$TMPDIR` (`/var/folders/…`), hors de `:minimal` : ses voisins sont protégés ; il ne doit jamais aller sous `/tmp`. La recherche web hébergée (`web__run`) reste disponible au modèle, sans accès au disque ; le réseau des commandes est coupé. Testé sur macOS seulement.

**Trace des lectures** : `--json` fait sortir les évènements de Codex ; l'exécuteur les garde dans `NN-<étape>.events.jsonl` et annonce le nombre de commandes. Une commande lancée y figure (`command_execution` : la commande, son code de sortie, sa sortie), même en échec ordinaire. Deux limites : c'est une **commande**, pas une liste de fichiers (un `grep -r` lit tout un dossier) ; et une commande **refusée par le bac à sable n'y figure pas** (5 essais sur 5, codex-cli 0.155.1) : elle n'apparaît que dans le journal de session, que `--ephemeral` n'écrit pas. La réponse du modèle ne prouve rien (il a déjà « recopié » une erreur sans lancer la commande) ; seule la trace le fait.

**Vérifié en vrai le 2026-10-16** (codex-cli 0.155.1, un appel `codex exec` par `call_engine`, dossier jetable de l'exécuteur, un script copié dans `references/` et lancé par le modèle ; résultats lus dans la sortie de la commande, dans `--json`) : la référence copiée se lit ; une demande posée à côté de `work/` (en `../input.md` et en chemin absolu), la demande d'un dossier `./parcours/<slug>/` et `~/.zshrc` sont refusées (« Operation not permitted ») ; un fichier sous `/tmp` se lit ; écrire dans `work/` et à côté est refusé. Aucun journal de session laissé.

**`agy`, deux particularités.** (1) Pas de `--mode plan` : essayé, agy avertit « `--mode plan` has no effect while slash command expansion is disabled » ; et en mode non interactif agy refuse d'office tout outil qui demande une permission, donc il ne peut rien écrire ni exécuter de lui-même — le dossier jetable fait le reste de l'isolation. (2) Le message passe en argument : il est **visible dans `ps`** pour tout utilisateur de la machine pendant l'appel, et sa taille est limitée à 200 000 **octets** UTF-8 (pas des caractères : les accents comptent double) ; au-delà, l'appel est refusé avant de partir.

**Coût de `claude`** : lu dans `total_cost_usd` du JSON de sortie, y compris quand l'appel échoue (`is_error`, code de sortie non nul) ; il est ajouté au coût de l'étape et du parcours, et l'appel est compté. La sortie du moteur est décodée avec remplacement des octets invalides.

Le moteur se choisit pour tout le parcours (`--engine`) ou par étape (`--engine-step questioning=agy`).

## 5. Les commandes

```bash
python3 scripts/parcours.py new brief-client --input demande.md [--slug …] [--title "…"] [--engine claude]   # --input - : stdin
python3 scripts/parcours.py archive <slug> | unarchive <slug> | archives [--json]   # sortir un parcours de la liste (.archives/), l'y remettre, les lister
python3 scripts/parcours.py recipes [--json]               # les recettes-workflows disponibles (celles du recueil personnel marquées), avec libellés et étapes
python3 scripts/parcours.py formats [--json]               # les formats de recette que cet exécuteur sait jouer
python3 scripts/parcours.py next <slug> [--yes] [--if-state <empreinte>]   # joue jusqu'à la prochaine pause
python3 scripts/parcours.py plan <slug> --json           # le plan de ce que ferait `next`, sans rien écrire
python3 scripts/parcours.py status <slug> [--json]
python3 scripts/parcours.py validate <slug> [--context fiche.json] [--stop]   # pause validate ; --stop pour un No-go
python3 scripts/parcours.py answer <slug> --file reponses.md | --none         # pause answers (valide aussi la fiche si c'est l'étape 1)
python3 scripts/parcours.py choose <slug> --run explorer,decision | --skip    # embranchement avant des étapes optionnelles
python3 scripts/parcours.py rerun <slug> <étape> [--extra <étape>.<champ>]     # relancer une étape, ex. l'offre avec les verdicts
python3 scripts/parcours.py retry <slug>                                      # reprendre une étape restée « running » après un arrêt
python3 scripts/parcours.py handoff <slug> <étape> --file champs.md          # fournir ou corriger les champs à la main (étape en échec, terminée ou en pause)
```

- **Embranchement** : `choose` n'est pas une pause d'étape ; l'exécuteur crée un `pending` de type `choose` dès que la prochaine étape est `optional`. `choose --run` refuse un choix où une étape retenue reçoit un champ d'une étape optionnelle écartée dans le même choix (ex. `--run decision` sans `explorer`).
- **Fiche de contexte** : écrite dans `00-context.md` ; chaque modification par `validate --context` garde la version précédente (`00-context.v1.md`…). `--context` est accepté à **toute** pause `validate` (les étapes déjà jouées ont reçu l'ancienne fiche ; `rerun` pour les refaire) et, pour l'étape 1, à sa pause `answers`.
- **Étape 1 avec `pause: answers`** : après l'étape 1, le `pending` est de type `answers`, la fiche est affichée avec le résumé (les questions sont dans `01-<étape>.md`) ; `validate --context` corrige la fiche sans lever la pause ; `answer` lève la pause et valide aussi la fiche.
- **Correction humaine** : `handoff <slug> <étape> --file` est accepté sur une étape en échec, terminée ou en pause. La sortie précédente est gardée en `.vN`, la fuite est recontrôlée, et les étapes déjà jouées qui ont consommé les champs de l'étape (directement ou par une étape elle-même refaite ; toutes, si l'étape produit la fiche) repassent `pending`, comme `rerun`. Une étape `done` reste `done` (la main fait foi, aucune pause rouverte) ; une étape `paused` reste en pause.
- **Fin du parcours** : la phrase « Parcours terminé. Sortie finale : … » s'affiche dès que le parcours devient `completed`, y compris après `validate`, `answer` ou `choose`.
- **`next` sur un parcours `stopped` ou `completed`** répond sans regarder les étapes (une étape restée `failed` n'y change rien).
- **Statut du parcours** : `active`, `completed` ou `stopped` (No-go, y compris après un signal de blocage), distinct du statut des étapes.
- **Robustesse** : `state.json` écrit de façon atomique (fichier temporaire puis renommage) ; un verrou empêche deux `next` simultanés ; un slug déjà pris reçoit un suffixe.
- `status` affiche aussi le nombre d'appels par moteur.
- **Pour l'interface locale ([`interface.md`](interface.md))** :
  - `plan <slug> --json` ne prend pas le verrou et ne crée aucun fichier : étapes jusqu'à la prochaine pause (moteur, modèle, taille du message en caractères et en octets — la source comprise pour une étape qui la relit —, champs à venir, `reads_source`), `claude_steps`, **plafond engagé** (`claude_steps × --max-budget-usd × 2`, la relance éventuelle comptant double), `calls` par moteur et `subscription_calls` (hors claude et fake), `agy_argv_warning` (un appel agy mettrait le message en argument, visible dans `ps`) et `agy_over_limit`, `changes_default_engine` (si `--engine` change le défaut ; les surcharges de moteur ne valent que pour le plan, en mémoire), les avertissements de skills modifiés, et l'**empreinte**. Quand rien ne peut tourner : `runnable: false`, avec `reason` (`stopped`, `completed`, `pending`, `failed`, `running`, `nothing`) et le message.
  - L'**empreinte** est `sha256(state.json + NUL + 00-context.md)` (fiche absente = vide), lue en une fois. `next --if-state <empreinte>` la recalcule **sous le verrou**, avant toute écriture (même pas la surcharge `--engine`) : si elle diffère, rien ne tourne, erreur `state_changed`.
  - `status <slug> --json` : tout ce qu'une page montre en un objet (titre, libellé de la recette, `context_labels`, marqueur `not_stated`, étapes avec libellé, mission, moteur, modèle, pause, `reads_source`, résumé, champs, erreur, blocage, coût, fichiers `trace` / `retry_trace` et, pour Codex, `events` / `retry_events`, fiche, `pending`, `files`, `final_output`, `recipe_error` si la recette a changé — sans échouer — , `fingerprint`, `max_budget_usd`) et `locked`, sonde non bloquante et sans écriture du verrou (`flock` partagé sur un `.lock` existant, relâché aussitôt ; pas de `.lock`, pas de verrou).
  - `--json` (ou `--json-errors`, accepté aussi avant la commande) : une erreur attendue sort en `{"error": code, "message": …}` sur la sortie standard, code de sortie 1 ; l'erreur est la dernière ligne (le texte de progression de `next` peut la précéder). Codes : `error`, `locked`, `state_changed`, `not_found`, `engine`, `timeout`, `parse`, `leak`, `missing_input`, `unexpected` (exception non prévue). Un code de sortie **2** vient d'argparse : une ligne de commande mal construite, donc un bug de l'appelant. Tous les arguments positionnels peuvent suivre un `--`.
  - `recipes --json` : les recettes du dépôt qui ont un bloc `workflow` (id, `label`, `description_fr`, icône, version, `format`, `warnings` — le format absent, lu comme 1 —, étapes avec `label`, pause effective, caractère facultatif et `reads_source`), et `formats`, les formats acceptés. `status --json` donne `recipe_format` ; une recette passée à un format inconnu laisse le dossier lisible, avec la raison dans `recipe_error`. `new --title "…"` garde un titre lisible dans `state.json` ; `new --json` répond `{"slug", "title"}`. `output_document(texte)` (fonction, pour la page) rend le document d'une sortie d'étape : ce qui précède ses blocs de fin, sans l'en-tête YAML éventuel, rendu à part.
  - **SIGTERM pendant `next`** devient une sortie propre : l'appel au moteur en cours (groupe de processus à part) est tué, l'étape reste `running` (`retry` la reprend) et le verrou se libère.

Avant de lancer des étapes, `next` affiche ce qu'il va faire — étapes, moteur, modèle, taille des entrées — et demande confirmation (sauf `--yes`) : les abonnements Codex et Antigravity sont petits.

### Recettes personnelles

Une recette se cherche dans le dépôt ou le plugin, puis — jamais à leur place — dans le recueil de l'utilisateur, `recettes/<id>.md` à côté du dossier des parcours s'il s'appelle `parcours` (`~/.ix-recipes/recettes` pour la page), dedans sinon, et, pour un dossier de test, dans le brouillon qu'il essaie ([interface.md](interface.md) §9). Le fichier se lit sans pyyaml (lecteur YAML de la bibliothèque standard, aussi utilisé en repli pour les recettes du dépôt). `recipes --json` les marque `personal: true` et liste à part celles qu'il écarte (`personal_problems`) ; `state.json` garde `recipe_sha256` et `recipe_origin`, `status --json` dit `recipe_current`. Le dossier `recettes` n'est jamais un parcours (`new --slug recettes` → `recettes-dossier`).

## 6. Règles reprises du format

- La demande brute ne part qu'à l'étape 1, et aux étapes qui vérifient et déclarent `reads_source` ; l'exécuteur le **vérifie** avant chaque appel (le message ne contient pas `input.md` hors de ce bloc déclaré) et refuse sinon.
- Une étape optionnelle ne tourne que si l'humain l'a choisie (`choose --run`).
- Un champ absent du HANDOFF déclenche la relance unique, puis `failed` — il ne passe jamais vide.
- Rien n'est décidé sur le fond par l'exécuteur : il enchaîne, s'arrête aux pauses, échoue proprement.

## 7. Hors v0

Serveur MCP et page de suivi (lot 3) ; résumé borné des réponses longues ; reprise d'un parcours commencé en conversation ; exécution d'une même étape sur deux moteurs pour comparaison.
