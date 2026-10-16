# Atome « vérification de calcul » (`ix-skills:calc-check`)

Spécification du 2026-10-16, décision 8 d'Amiel (« Vérification séparée : oui, contrats et chiffres : créer l'atome « vérification de calcul » dans ix-skills et une étape de contrôle isolée, avec accès à la source »). **L'atome n'existe pas encore** : il se crée dans ix-skills, dans une session ouverte sur `~/Projets/ix-skills`, à partir de ce document. Ce dépôt l'a seulement préparé (§6).

## 1. Le manque

La revue des skills métier (2026-10-16, « Vérification des chiffres ») a relevé cinq skills qui produisent des chiffres dérivés repris tels quels par la suite : `budget-variance-analysis` (écarts, décomposition volume / prix / mix), `business-case-draft` (ROI, VAN, retour sur investissement), `metriques-saas` (MRR, NRR, CAC, LTV, payback), `financial-narrative` (variations commentées), `tam-sam-som` (marchés calculés de haut en bas et de bas en haut).

Aucun atome ne vérifie un calcul. `fact-check` vérifie qu'une affirmation est **dans** la source : un écart de 12,4 % calculé à partir de deux montants n'y est pas, il sortirait « absent de la source » qu'il soit juste ou faux. `quality-check` juge la fiabilité des sources, `controle-qualite` la conformité à des règles. Le geste manquant est cognitif et vaut pour tout contenu chiffré, donc il appartient à ix-skills (CLAUDE.md §2), pas à ce dépôt.

## 2. Identité

| Champ | Valeur proposée |
|---|---|
| `id` | `calc-check` (libre dans ix-skills et ix-recipes au 2026-10-16 ; même famille de nom que `fact-check` et `quality-check`) |
| `label` | Vérification de calcul |
| `category` | `critique` (comme `fact-check`) |
| `domain` | `cognitif` |
| `input_types` | `markdown`, `reference`, `analysis`, `table` |
| `output_types` | `calc_check` |

Description à écrire dans le style des atomes : ce qu'il fait (recalcule chaque chiffre dérivé d'un texte à partir des valeurs de la source et signale les écarts), ses déclencheurs (« vérifie les calculs de cette analyse », « ces pourcentages sont-ils justes », « recalcule les écarts du reporting », « le ROI tient-il »), ce qu'il ne fait pas (vérifier qu'un chiffre est dans la source : `fact-check` ; juger la source : `quality-check` ; corriger le texte : il signale, il ne réécrit pas).

## 3. Entrées

| Entrée | Obligatoire | Contenu |
|---|---|---|
| texte à vérifier | oui | Le livrable qui contient des chiffres dérivés (analyse d'écarts, business case, note financière). |
| source | oui | Les valeurs de départ : le tableau, l'export, la demande. **Jamais la mémoire du modèle** : une valeur absente de la source rend le chiffre « non recalculable », elle n'est pas devinée. |
| définitions | non | Les formules imposées par l'organisation (une définition maison du NRR, un taux de change, une règle d'arrondi). À défaut, la formule standard, nommée. |

Dans une recette, la source est la demande brute : l'étape déclare `reads_source: true` (format 2) et reçoit le livrable par un champ de l'amont.

## 4. Méthode

1. **Inventorier les chiffres dérivés** du texte : tout nombre qui résulte d'une opération sur d'autres (somme, différence, écart en %, ratio, moyenne, taux de croissance, cumul, conversion, part, projection). Un chiffre recopié tel quel de la source n'est pas dérivé : il relève de `fact-check`, le dire et passer.
2. **Pour chacun, reconstituer le calcul** : les valeurs d'entrée, chacune **citée** de la source (cellule, ligne, passage exact), et l'opération, celle que le texte annonce ou, à défaut, la plus plausible — dite comme hypothèse. Unités, périodes et périmètres alignés (HT / TTC, mensuel / annuel, avec ou sans une entité).
3. **Recalculer pas à pas**, chaque opération intermédiaire écrite, sans sauter d'étape. Arrondir seulement à la fin, à la précision du texte.
4. **Comparer** au chiffre du texte, avec une tolérance d'arrondi explicite (une demi-unité de la dernière décimale affichée) :
   - `exact` — égal à l'arrondi près ;
   - `écart` — différent : donner la valeur recalculée, l'écart absolu et relatif, et la cause probable (mauvaise base, inversion du signe, période décalée, total qui omet une ligne, pourcentage de pourcentage) ;
   - `non recalculable` — une entrée manque dans la source, ou la formule est indécidable entre deux lectures : dire laquelle manque, ou donner les deux résultats ;
   - `incohérent` — juste isolément mais contredit par un autre chiffre du texte (la somme des écarts ne fait pas l'écart total).
5. **Propager** : un chiffre faux qui en nourrit d'autres rend ceux-ci suspects ; les marquer, les recalculer avec la valeur corrigée.
6. **Conclure** sur ce qui change une décision : un écart qui inverse un signe, franchit un seuil de matérialité donné, ou change le classement de deux options passe en tête.

## 5. Règles absolues et sortie

- Toute valeur d'entrée est citée de la source ; aucune n'est inventée, complétée ou « supposée raisonnable ».
- Le calcul est montré, pas affirmé : un verdict sans opérations écrites ne compte pas.
- Le skill signale, il ne corrige pas le livrable (une étape `correction` ou `rerun --extra` le fait en aval).
- Si le texte n'a aucun chiffre dérivé : « RAS — aucun chiffre dérivé dans le texte : {pourquoi} », et il s'arrête (convention du corpus).
- Limite à dire en tête de sortie : un modèle calcule de façon faillible ; les opérations écrites servent à ce qu'un humain refasse le compte d'un coup d'œil. Quand un outil de calcul est disponible dans l'environnement, s'en servir et le dire.

Sortie : un résumé de trois à cinq lignes (nombre de chiffres vérifiés, écarts, non recalculables, le plus grave), puis un tableau `chiffre | où dans le texte | entrées citées de la source | opération | recalculé | annoncé | écart | verdict`, puis la propagation, puis les points qui changent une décision. Champs de HANDOFF prévus pour une recette : `calc_verdicts` (le tableau), `blocking` réservé à un écart qui rend le livrable inutilisable en l'état.

**Definition of done** : chaque chiffre dérivé a un verdict ; chaque `exact` et chaque `écart` montre ses entrées citées et ses opérations ; aucune valeur hors source ; les écarts qui changent une décision sont en tête.

## 6. Ce qui est prêt dans ix-recipes

- `ix-skills:calc-check` est ajouté le 2026-10-16 à la **liste fermée** des skills qui peuvent relire la source (`VERIFICATION_SKILLS` dans `scripts/parcours.py` et `build.py`, avec un test). Une recette peut donc déclarer `reads_source: true` sur une étape `calc-check` dès que l'atome existe ; tant qu'il n'existe pas, `requires` le refuse (skill introuvable) et le concepteur de la page ne l'annonce pas (il ne nomme que les skills du catalogue).
- La copie de `build.py` dans ix-skills doit recevoir la même liste (CLAUDE.md §7 ; patch fourni avec ce changement).
- Première recette visée, une fois l'atome créé et `budget-variance-analysis` enrichi : le **parcours de clôture** `ix-recipes:budget-variance-analysis` → **answers** (responsables budgétaires) → `ix-recipes:financial-narrative` → `ix-skills:calc-check` (`reads_source: true`) → **validate**.

## 7. À faire dans la session ix-skills

1. Écrire `skills/calc-check.md` (frontmatter canonique, corps en anglais) et `skills/calc-check.mystaffy.json`, d'après les §2 à §5.
2. Des cas de contrôle tirés des skills de la revue : un tableau budget / réel avec un écart mal calculé (base inversée), un total qui omet une ligne, un NRR calculé sur la mauvaise cohorte, une projection TAM dont un facteur manque dans la source (doit sortir « non recalculable », pas une valeur devinée), un texte sans chiffre dérivé (RAS).
3. Vérifier qu'aucun atome existant (`fact-check`, `quality-check`, `controle-qualite`, `indicateurs`) ne change de frontière ; ajuster leurs renvois (« voir `calc-check` ») sans faire pointer un atome vers ix-recipes.
4. Reconstruire `dist/`, relever la version du plugin ix-skills.
