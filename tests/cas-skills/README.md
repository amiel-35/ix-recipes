# Cas de test des skills métier

Un fichier par skill : une ou plusieurs demandes réalistes, ce que doit contenir une bonne sortie (critères vérifiables, valeurs de référence quand il y a des calculs), et les résultats des passages. Méthode et grille : [`docs/etat-de-l-art-skills.md`](../../docs/etat-de-l-art-skills.md).

Le banc s'exécute avec [`banc.py`](banc.py) (bibliothèque standard, CLI `claude` connectée) ; il n'écrit rien dans le dépôt :

```bash
python3 tests/cas-skills/banc.py --skills cgv-checker,ticket-triage --base cbe271c --models sonnet,haiku --passages 3 --out /tmp/banc
```

Comment un cas est joué :

- la version avant est `dist/skills/<id>/` au commit de départ, la version après est `dist/skills/<id>/` régénéré ; chacune est copiée dans un dossier à part, avec ses `references/` ;
- `claude -p --model <sonnet|haiku> --system-prompt-file <skill> --tools Read --strict-mcp-config --setting-sources "" --disable-slash-commands`, lancé depuis ce dossier, la demande du cas en entrée : le modèle n'a que le skill et la lecture de ses fichiers ;
- chaque sortie est renommée au hasard, puis un juge (Opus par défaut) la note seule, critère par critère (1 ou 0), et relève les erreurs, sans savoir quelle version ni quel modèle l'a produite ;
- chaque cas est joué plusieurs fois (`--passages`, 3 par défaut) : le rapport donne la moyenne et l'étendue, parce qu'une seule exécution varie d'un ou deux points d'un tirage à l'autre.

Un cas « de contrôle » suit un autre chemin que celui sur lequel la réécriture a été pensée. Les cas notés « contrôle indépendant » (n° 3) ont été écrits par un agent qui n'a vu que la description du skill, ni son corps ni sa réécriture : c'est la mesure la plus honnête du gain.

Ces fichiers ne sont pas lus par `build.py` ni par les tests Python.
