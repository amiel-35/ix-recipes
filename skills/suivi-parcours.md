---
id: suivi-parcours
label: Suivi des parcours
version: 1.3.0
description_fr: "Démarre sur cet ordinateur la page de suivi des parcours ix-recipes — une page web locale (pas un artifact claude.ai) qui liste vos dossiers de recettes-workflows (réponse à appel d'offres, brief client…), en crée un à partir d'une demande collée, fait tourner chaque étape isolée et affiche le livrable comme un document à valider, corriger ou refaire ; on y conçoit aussi ses propres recettes, qu'on teste et garde dans son recueil personnel avant de pouvoir les proposer au dépôt. Déclenche sur \"ouvre la page de suivi\", \"lance la page de suivi des parcours\", \"ouvre mes dossiers ix-recipes\", \"démarre un dossier appel d'offres dans la page\", \"reprends mon dossier dans l'interface\", \"crée une recette personnelle dans la page\". Ne joue aucune étape lui-même : il lance la page et en donne l'adresse. Nécessite Claude Code sur l'ordinateur (pas Cowork, d'où la page serait injoignable)."
description_en: "Starts the ix-recipes tracking page on this computer — a local web page (not a claude.ai artifact) listing your workflow-recipe dossiers (tender response, client brief…), creating one from a pasted request, running each step isolated and showing the deliverable as a document to validate, correct or redo; you also design your own recipes there, test them and keep them in your personal recueil before proposing them to the repository. Triggers on \"open the tracking page\", \"start the parcours tracking page\", \"open my ix-recipes dossiers\", \"start a tender response dossier in the page\", \"resume my dossier in the interface\", \"create my own recipe in the page\". Runs no step itself: it starts the page and gives its address. Needs Claude Code on the computer (not Cowork, from which the page would be unreachable)."
icon: ▤
domain: ops
category: production
input_types:
- demande
output_types:
- page_locale
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
scripts:
- scripts/parcours.py
- scripts/recettes.py
- scripts/interface.py
- scripts/interface.html
- themes/inflexion
---

# Role

You start the local tracking page of the ix-recipes workflow recipes and hand its address to the user. The page does the rest: creating dossiers, running each step in a fresh engine call, pauses, reading the deliverables. You never run a step, never read or summarise a dossier, and never paste a request into the page yourself.

# Absolute rules

- **Local only.** The page is a server bound to 127.0.0.1 on the user's computer. If you are not running on the user's own machine (a cloud or remote sandbox such as Cowork), say so and stop: the address would be unreachable.
- **The address is private.** It carries an access key after `#t=`. Give it to the user once; never post it anywhere else, never put it in a file.
- **Never stop a page the user already runs.** If the port is taken, the page is probably already open: say so, and offer to start another one on a free port only if the user asks.

# Steps

1. **Where the files are.** The page and its runner are in the `scripts/` folder next to this file (the skill's base directory). Check that `scripts/interface.py`, `scripts/parcours.py` and `scripts/interface.html` exist there.
2. **Prerequisites.** `python3` must exist (Python 3.9 or later; the standard library is enough). The steps call the `claude` command line, which must be installed and signed in; the ix-skills plugin must be installed too (the recipes chain its skills). Check `python3 --version` and `claude --version`; if one is missing, say what to install and stop.
3. **Start the page in the background**, so the conversation goes on: `python3 "<base>/scripts/interface.py"` (add `--parcours-dir <folder>` only if the user names one; the default is `$PARCOURS_DIR`, else `~/.ix-recipes/parcours` (or `~/Parcours` if that older folder still holds dossiers)). It prints two lines: the dossier folder and `Page de suivi : http://127.0.0.1:<port>/#t=…`, then opens the browser itself.
4. **Answer in a few lines:** the page is open (or the address to open), dossiers are kept in the folder printed (the user's own recipes, under "Recettes" in the page, in the `recettes` folder next to it: `~/.ix-recipes/recettes`), and how to stop the page (stop the background command, or close the terminal). Mention that a step uses paid engine calls (a full tender response cost about one to two dollars in tests).

# If something fails

- `Address already in use`: a page is probably already running on that port. Its address can be rebuilt without restarting anything: read the access key in `<dossier folder>/.interface-token` (the folder printed by the page; `$PARCOURS_DIR`, else `~/.ix-recipes/parcours`) and give `http://127.0.0.1:8765/#t=<key>` — it works if that page serves the same folder. Otherwise, `--port 0` starts a second page on a free port, if the user wants one. Never show the key anywhere but in your answer to the user.
- `ModuleNotFoundError`: say which module; the bundled runner needs none beyond the standard library, so this means an older copy is being run — reinstall the plugin.
- Any other error: show its last line, plainly, without guessing a fix.

# Output format

Three to five short lines, in the user's language: what was started, where to click, where the dossiers are kept, how to stop. No technical details unless something failed.
