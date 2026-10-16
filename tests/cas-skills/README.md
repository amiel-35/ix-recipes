# Cas de test des skills métier

Un fichier par skill : une ou plusieurs demandes réalistes, ce que doit contenir une bonne sortie (critères vérifiables, valeurs de référence quand il y a des calculs), et les résultats des passages. Méthode et grille : [`docs/etat-de-l-art-skills.md`](../../docs/etat-de-l-art-skills.md).

Comment un cas est joué (pilote du 2026-10-16) :

- la version avant est `dist/skills/<id>/` au commit de départ, la version après est `dist/skills/<id>/` régénéré ; chacune est copiée dans un dossier à part, avec ses `references/` ;
- `claude -p --model <sonnet|haiku> --system-prompt-file <skill> --tools Read --strict-mcp-config --setting-sources "" --disable-slash-commands`, lancé depuis ce dossier, la demande du cas en entrée : le modèle n'a que le skill et la lecture de ses fichiers ;
- les sorties sont renommées au hasard et mélangées, puis un juge Opus note chaque critère (1 ou 0) et relève les erreurs, sans savoir quelle version a produit quoi.

Un cas « de contrôle » suit un autre chemin que celui sur lequel la réécriture a été pensée ; c'est la mesure la plus honnête du gain. Une seule exécution par cas et par modèle : un écart d'un point n'est pas significatif.

Ces fichiers ne sont pas lus par `build.py` ni par les tests Python.
