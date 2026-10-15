---
id: suivi-parcours
label: Suivi des parcours
version: 1.0.0
description_fr: "Ouvre la page de suivi des recettes-workflows (réponse à appel d'offres, brief client…) : une page locale où l'on crée un dossier en collant la demande, où chaque étape tourne isolée, et où l'on relit, valide, répond ou refait chaque étape, le livrable affiché comme un document. Déclenche sur \"ouvre la page de suivi\", \"lance un dossier appel d'offres\", \"je veux suivre mon brief client dans la page\", \"reprends mon dossier dans l'interface\". Ne joue aucune étape lui-même et ne lit pas les dossiers : il démarre la page et en donne l'adresse. Nécessite Claude Code sur l'ordinateur (pas un environnement distant comme Cowork, d'où la page serait injoignable)."
description_en: "Opens the tracking page for workflow recipes (tender response, client brief…): a local page where you create a dossier by pasting the request, each step runs isolated, and you review, validate, answer or redo each step, the deliverable shown as a document. Triggers on \"open the tracking page\", \"start a tender response dossier\", \"I want to follow my client brief in the page\", \"resume my dossier in the interface\". Runs no step itself and reads no dossier: it starts the page and gives its address. Needs Claude Code on the user's computer (not a remote environment such as Cowork, from which the page would be unreachable)."
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
- scripts/interface.py
- scripts/interface.html
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
3. **Start the page in the background**, so the conversation goes on: `python3 "<base>/scripts/interface.py"` (add `--parcours-dir <folder>` only if the user names one; the default is `~/Parcours`). It prints two lines: the dossier folder and `Page de suivi : http://127.0.0.1:<port>/#t=…`, then opens the browser itself.
4. **Answer in a few lines:** the page is open (or the address to open), dossiers are kept in the folder printed, and how to stop the page (stop the background command, or close the terminal). Mention that a step uses paid engine calls (a full tender response cost about one to two dollars in tests).

# If something fails

- `Address already in use`: a page is already running on that port — give the user the address of that page if you know it, otherwise say it is likely already open in their browser, and that `--port 0` starts a second one on a free port.
- `ModuleNotFoundError`: say which module; the bundled runner needs none beyond the standard library, so this means an older copy is being run — reinstall the plugin.
- Any other error: show its last line, plainly, without guessing a fix.

# Output format

Three to five short lines, in the user's language: what was started, where to click, where the dossiers are kept, how to stop. No technical details unless something failed.
