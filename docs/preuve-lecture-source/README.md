# Preuve : un fact-check qui relit la source (format 2, `reads_source`)

Rejouée le 2026-10-16 avec l'exécuteur de cette branche ([format](../format-recette.md) §1.10). Deux appels Claude Sonnet, 0,119 $ au total (0,061 $ avant, 0,058 $ après).

## Le cas

Un tableau budget / réel du T3 d'une entreprise fictive, avec trois phrases de la demande : la cause de l'écart marketing, celle des achats, et une consigne (« ne pas présenter la baisse du chiffre d'affaires comme définitive : deux commandes, environ 80 k€, ont glissé sur octobre »). C'est [`source.md`](source.md).

Une recette de trois étapes : analyse des écarts (`ix-recipes:budget-variance-analysis`, lit la demande, produit la fiche de contexte), commentaire pour le comité (`ix-recipes:financial-narrative`), fact-check du commentaire (`ix-skills:fact-check`). Deux versions identiques à une ligne près :

- [`commentaire-ecarts-avant`](recettes/commentaire-ecarts-avant.md) : format 1, le fact-check reçoit la fiche, `analyse.variances` et `commentaire.commentary` ;
- [`commentaire-ecarts-apres`](recettes/commentaire-ecarts-apres.md) : format 2, la même chose plus `reads_source: true`.

Les sorties des étapes 1 et 2 sont écrites à la main (moteur `fake`) pour que l'écart soit connu d'avance et identique dans les deux essais. Elles reproduisent des dérives ordinaires d'une chaîne :

- l'analyse ([`fake/analyse.md`](fake/analyse.md)) recopie mal le marketing (128 k€ au lieu de 138, donc +8 au lieu de +18) et range les déplacements (+11 k€, +37 %) dans « autres postes proches du budget » ; la fiche de contexte ne garde pas la consigne sur le chiffre d'affaires (une fiche contient des faits, jamais une demande d'action) ;
- le commentaire ([`fake/commentaire.md`](fake/commentaire.md)) reprend ces chiffres, déclare les déplacements « conformes », et présente la baisse du chiffre d'affaires comme un « ralentissement durable ».

Seul le fact-check est un vrai appel, avec la même mission dans les deux recettes. Le message exact envoyé ne diffère que par la consigne sur la source et le bloc `=== INPUT: source ===`.

## Résultat

| | Avant (format 1) | Après (format 2, `reads_source`) |
|---|---|---|
| Bilan | 15 affirmations : 9 confirmées, **0 contredite**, 3 absentes de la source, 3 non vérifiables | 14 affirmations : 8 confirmées, **4 contredites**, 1 absente, 1 non vérifiable |
| Marketing +8 k€ (+6,7 %) | **confirmé**, en citant l'analyse (« réel 128 k€ ») | **contredit** : « \| Marketing \| 120 \| 138 \| +18 \| », soit +15 % |
| Déplacements « conformes » | absent de la source (« la source ne cite aucun poste déplacements ») ; « autres postes conformes » **confirmé** | **contredit** : « \| Déplacements \| 30 \| 41 \| +11 \| » |
| « Ralentissement durable » | absent de la source | **contredit** par la consigne de la demande (les commandes glissées sur octobre) |
| Tolérance de 10 % (inventée) | absente de la source | absente de la source, « fausse de toute façon avec +15 % » |
| Conclusion | « le commentaire ne contredit aucun chiffre repris de l'analyse » | « `analyse.variances` contient l'erreur marketing (128 k€) que le commentaire a reprise » |

Avant, le fact-check ne peut que vérifier la cohérence de la chaîne avec elle-même : un chiffre faux recopié de bout en bout sort **confirmé**, et ce que l'étape 1 a laissé de côté ne peut être qu'« absent ». Après, il voit les trois écarts avec la demande d'origine, et remonte l'erreur jusqu'à l'étape qui l'a introduite. Sorties complètes : [`resultats/avant-03-verification.md`](resultats/avant-03-verification.md), [`resultats/apres-03-verification.md`](resultats/apres-03-verification.md).

Ce que la preuve ne dit pas : le fact-check ne recalcule pas (le +15 % est ici un rapport simple qu'il a fait de lui-même) ; la vérification de calcul reste un manque du catalogue (revue des skills métier, §1.1).

## Rejouer

Depuis la racine du dépôt, ix-skills cloné à côté (`../ix-skills`) ou installé :

```bash
P=docs/preuve-lecture-source; D=/tmp/preuve/parcours; mkdir -p "$D" && cp -r "$P/recettes" "$P/fake" /tmp/preuve/
export PARCOURS_FAKE_DIR=/tmp/preuve/fake IX_SKILLS_PATH="$PWD/../ix-skills/dist/skills"
for v in avant apres; do
  python3 scripts/parcours.py new commentaire-ecarts-$v --input "$P/source.md" --slug $v --engine claude \
    --engine-step analyse=fake --engine-step commentaire=fake --parcours-dir "$D"
  python3 scripts/parcours.py next $v --yes --parcours-dir "$D" && python3 scripts/parcours.py validate $v --parcours-dir "$D"
  python3 scripts/parcours.py next $v --yes --max-budget-usd 1 --parcours-dir "$D"   # un appel Claude Sonnet
done
```

La recette personnelle se trouve dans `/tmp/preuve/recettes`, à côté du dossier des parcours ; le moteur `fake` y lit les sorties préparées et écrit les messages reçus dans `/tmp/preuve/fake/received/`.
