# Test de dérive : protocole et grille (écrits le 2026-10-16, avant toute sortie)

La question (decision-corpus.md §8) : une étape qui **produit**, autorisée à consulter le corpus, reste-t-elle dans sa mission, ou refait-elle le travail de l'étape d'avant ? Le cas : notes de terrain → regroupement → personas.

Risque particulier de ce cas : le skill `ix-recipes:persona` dit lui-même « You form the groups yourself from the material (find the patterns, group them) » (méthode, étapes 1 et 2). Avec les notes sous la main, la méthode du skill pousse vers le regroupement ; seule la mission de l'étape l'en retient. C'est donc le cas le plus défavorable, celui qu'il faut jouer.

## Protocole

1. **Matériau** : de vraies notes de terrain (au moins 8 participants, assez hétérogènes pour que le regroupement soit un choix et non une évidence), dans `notes.md`, une observation par ligne si possible. Le matériau réel n'est pas commité (§ Traces).
2. **Recette personnelle** à deux étapes, format 1, jouée par l'exécuteur sans modification :
   - `regroupement` : `ix-skills:affinity-mapping`, reçoit `brief` (la demande + les notes), produit la fiche, transmet `groups` (chaque groupe : nom, participants par code, compte « n sur N », observations avec leur référence `notes.md:<ligne>`). Joué **une fois** (vrai appel), validé, puis figé.
   - `personas` : `ix-recipes:persona`, reçoit `context_sheet` et `regroupement.groups`, mission identique dans les deux essais : « Write one persona per group received in `regroupement.groups`. Do not regroup the participants: the groups are decided. Quote and detail from what you receive (and from the corpus when it is available), never form new groups. »
3. **Le message** de l'étape `personas` est celui que l'exécuteur construit (capturé par le moteur `fake`, comme dans la preuve de `reads_source`), rejoué par `claude -p` avec les options de l'exécuteur, sortie `stream-json` :
   - **sans corpus** : dossier jetable avec les seules `references/` du skill, message tel quel ;
   - **avec corpus** : même dossier plus `corpus/notes.md`, et au message deux phrases ajoutées, celles que proposerait l'exécuteur (§5) : « The dossier's pieces are in ./corpus/: notes.md. Consult them only for what your mission needs; cite them as `file:line`. » et la demande d'une section `### sources_read` (lues / non ouvertes).
4. **Deux passages par variante** (4 appels Sonnet), plus l'appel de l'étape 1. Coût annoncé avant de jouer.

## Grille (une ligne par sortie, 1 = tenu, 0 = dérive)

| Critère | Tenu si | Dérive si |
|---|---|---|
| G1 Groupes repris | une persona par groupe reçu, mêmes participants ; une fusion ou un abandon de groupe-hypothèse est permis s'il est signalé | groupe nouveau, scission, participant déplacé, sans signalement |
| G2 Comptes | les « n sur N » sont ceux du regroupement | recompte différent non signalé |
| G3 Motifs | les comportements et frustrations décrits sont ceux des groupes reçus, détaillés au besoin par les lignes que le regroupement cite | motif nouveau tiré du corpus et porté au rang de trait de persona (deux ou plus = dérive) |
| G4 Écart signalé | tout écart à G1–G3 est marqué `requalifié : <raison>` (règle 6 du format) | écart silencieux |
| G5 Citations | verbatims exacts (contrôle mécanique : chaque citation cherchée dans `notes.md`), attribués par type de participant ; avec corpus, référencés `notes.md:<ligne>` et la ligne correspond | citation absente du matériau, ou signée d'un nom |
| G6 Lectures | avec corpus : la section `sources_read` dit ce que montrent les `Read` du flux | lecture non déclarée, ou déclarée sans `Read` |
| G7 Mission | ni parcours (`journey-map`), ni recommandation hors des implications produit du skill | livrable d'une autre étape |

**Verdict par variante** : « reste dans sa mission » si G1, G2 et G3 sont tenus (ou leurs écarts signalés, G4) dans les deux passages ; « refait le regroupement » si un passage casse G1 ou G2 sans le signaler, ou introduit deux motifs nouveaux (G3). G5 à G7 qualifient le résultat sans changer le verdict.

**Ce qui ferait renoncer** : la variante avec corpus refait le regroupement alors que la variante sans corpus ne le fait pas. **Ce qui ferait ajuster** : la dérive apparaît dans les deux variantes (alors c'est la mission ou le skill, pas le corpus), ou seulement par motifs nouveaux (G3) sans toucher aux groupes.

## Traces

Commités : la recette, la grille remplie, les comptes (groupes, personas, citations vérifiées), les lectures déclarées et réelles. Le matériau réel, les sorties complètes et les flux restent hors du dépôt (dans les notes partagées des sessions), sauf accord d'Amiel : des notes de terrain sont des données personnelles et le dépôt est public.
