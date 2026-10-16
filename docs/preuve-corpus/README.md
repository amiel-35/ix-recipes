# Vérifications avant de coder le corpus

Les essais du §8 de [`decision-corpus.md`](../decision-corpus.md), joués le 2026-10-16 sans toucher à l'exécuteur. Résultats et verdicts : §9 du même document. Codex est traité par une autre session.

| Dossier | Essai | État |
|---|---|---|
| [`derive/`](derive/grille.md) | l'étape persona avec et sans le corpus | fait : l'étape reste dans sa mission, verbatims exacts avec le corpus ; 6 appels, 1,28 $ ([résultats](derive/resultats.md)) ; matériau hors du dépôt |
| [`antigravity-vibe/`](antigravity-vibe/) | lecture hors du dossier de l'étape | **non testé** : quota Antigravity épuisé, budget Vibe épuisé ([`sorties.txt`](antigravity-vibe/sorties.txt)) ; [`rejouer.sh`](antigravity-vibe/rejouer.sh) le rejoue |
| [`pieces-non-textuelles/`](pieces-non-textuelles/) | ce que Claude lit d'un PDF et d'un tableur dans le dossier d'une étape | fait : 6 appels Sonnet, 0,256 $ |

## Pièces non textuelles

[`fabriquer.py`](pieces-non-textuelles/fabriquer.py) écrit les pièces dans `pieces/` (bibliothèque standard, Pillow pour le scan) : un contrat PDF de 2 pages avec un tableau, une annexe PDF de 25 pages dont une seule phrase compte (page 23), un avenant scanné (une image, aucun texte), un classeur `.xlsx` écrit comme Excel l'enregistre (deux onglets, formules avec leur valeur calculée, une date, une cellule fusionnée). [`xlsx_vers_csv.py`](pieces-non-textuelles/xlsx_vers_csv.py) est l'essai de conversion (bibliothèque standard), qui a produit `converti/`.

[`lancer.py`](pieces-non-textuelles/lancer.py) joue un appel `claude -p` par pièce, dans un dossier jetable qui ne contient que la pièce, avec les options de l'exécuteur sauf la sortie (`stream-json`, pour garder chaque `Read`). Les traces `traces/<essai>.md` donnent la consigne, chaque lecture avec la réponse de l'outil, la réponse du modèle et le coût ; les flux bruts (`.jsonl`, images des pages en base64, chemins du compte) ne sont pas commités.

```bash
cd docs/preuve-corpus/pieces-non-textuelles
python3 fabriquer.py pieces && python3 xlsx_vers_csv.py pieces/budget-t3.xlsx converti
python3 lancer.py                      # 6 appels Sonnet, environ 0,25 $
```
