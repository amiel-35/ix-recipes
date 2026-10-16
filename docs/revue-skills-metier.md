# Revue des skills métier : skill simple, recette cachée ou mélange

Revue du 2026-10-16 (chantier 2), à valider par Amiel. Aucun skill n'a été modifié.

## Périmètre et méthode

**47 skills** : tout `skills/` sauf les recettes-workflows (`brief-client`, `reponse-appel-offres`), `concepteur-recette`, `suivi-parcours` et `configuration-ix`.

Quatre catégories :

- **skill simple** : un seul geste, un seul passage suffit ;
- **recette cachée** : le skill enchaîne en fait plusieurs gestes qui gagneraient à être des étapes isolées (format de [`format-recette.md`](format-recette.md)) ;
- **mélange** : une partie s'extrait en recette, il reste un skill allégé qui devient une étape ;
- **à enrichir** : trop mince pour être classé ; ce qui manque est dit, rien n'est deviné.

Grille appliquée : celle de `concepteur-recette` (une recette doit acheter quelque chose : isolation, pause humaine, réponses d'un tiers, vérification séparée, coût maîtrisé ; pas de sandwich métier → atome → métier ; un skill métier qui recommande déjà rend `decision` redondant) et les décisions de [`cadrage-suite.md`](cadrage-suite.md) §3bis et §6bis. Chaque enchaînement proposé n'utilise que des skills qui existent dans ix-skills ou ix-recipes ; ce qui manque est écrit **MANQUE**.

Le travail a été découpé par famille, un sous-agent Opus par famille. Chacun a lu ses skills en entier et la description des atomes qu'il cite. Les résultats ont ensuite été relus et harmonisés. Point de comparaison : la revue du 2026-10-14 (A = 39, B = 5, C = 2, dont 13 skills « minces »). Elle a été faite avant la livraison des partials métier et avant le format de recette.

Un **parcours métier** (recrutement, achats, appel d'offres, cycle d'entretien) n'est pas une recette cachée dans le skill qui en est une étape. L'appartenance à un parcours est notée sans changer la catégorie.

## Verdict d'ensemble

| Catégorie | Nombre | Skills |
|---|---|---|
| Skill simple | 35 | tous les autres |
| Recette cachée | **0** | — |
| Mélange | 2 | `people-review` (à discuter), `persona` (seulement avec des données terrain) |
| À enrichir | 10 | `contrat-emploi`, `performance-review-helper`, `org-design-brief`, `compliance-checklist`, `budget-variance-analysis`, `strategie-prix`, `metriques-saas`, `analyse-concurrentielle`, `vendor-scorecard`, `mockup` |

Quatre constats :

1. **Aucun skill ne cache une recette.** Les plus longs (`interview-loop-planner`, 354 lignes ; `interview-guide-recruteur`, 196 ; `okr`, 162 ; `offre-commerciale`, 110) doivent leur taille à du contenu (partials transverses recopiés, modes, contraintes), pas à des gestes enchaînés. Les enchaînements qui achètent quelque chose relient **plusieurs skills** : ce sont des parcours. Aucun ne se cache dans un seul skill.
2. **Huit skills basculeraient en mélange selon une réponse d'Amiel** (questions du §3 final) : `offre-commerciale`, `prd`, `business-case-draft`, `cgv-checker`, `contrat-fournisseur`, `compliance-checklist`, `system-design` et `strategie-prix` une fois enrichi.
3. **Le besoin de moteur le plus fréquent n'est ni le parallèle ni la boucle, c'est l'accès d'une étape à la source d'origine.** Il touche 4 familles et 9 skills, et bloque déjà `persona`, qui avait été décidé au §6bis.
4. **10 des 13 skills minces du 2026-10-14 le restent.** Les partials `metier_*` sont des grilles de compétences par niveau. Ils ont relevé `fiche-poste` et `onboarding-plan`, mais rien hors RH. Un contenu juridique est **périmé** : `entretien-professionnel` ignore la loi n° 2025-989 du 24/10/2025 (annexe B).

---

## RH — recrutement et arrivée

| Skill (version) | Catégorie | Raison | Enchaînement proposé | Confiance |
|---|---|---|---|---|
| `fiche-poste` (1.3.0) | simple | Les 7 étapes produisent un seul artefact. Le partial calibre désormais les compétences par niveau (étape 4). Les zones grises (étape 7) sont une sortie, et la pause `validate` avec correction humaine suffit à les faire trancher. | — | sûr |
| `grille-remuneration` (1.2.0) | simple | Les 7 étapes sont toutes métier (familles, composantes, fourchettes, positionnement, gouvernance) et aboutissent à une seule grille. `research` en amont ne marche pas : les familles et niveaux doivent être posés avant la collecte. | — | sûr |
| `interview-guide-recruteur` (1.3.0) | simple | Les 10 étapes composent un seul guide pour **un** tour (STAR, mises en situation, grille 1-4, drapeaux, gabarit de notes). 81 lignes sur 196 sont le partial anti-biais recopié. Aucune étape ne gagne à ignorer les autres. | — | sûr |
| `interview-loop-planner` (1.2.0) | simple | Il conçoit un seul processus (tours, couverture, non-redondance, scorecard consolidée, `round_briefs`). 203 lignes sur 354 sont deux partials transverses recopiés. Les étapes 4-5 sont un contrôle interne lié au partial, pas `controle-qualite`. Les pauses réelles (les entretiens ont lieu) et le parallèle (N tours, N candidats) relèvent du parcours, pas du skill. | — | probable |
| `contrat-emploi` (1.1.0) | **à enrichir** | La méthode tient en 6 lignes génériques, sans droit du travail : mentions du CDD, période d'essai, 4 conditions de la non-concurrence, mobilité, forfait jours, promesse d'embauche, CCN. Deux modes (analyse, génération), plus un troisième, `revision`, déclaré dans `.mystaffy.json` et absent du corps. On ne peut pas dire si l'analyse doit rester ici ou céder la place à `legal-risk-flag`. | — | sûr |
| `onboarding-plan` (1.2.0) | simple | Les 7 étapes produisent un seul plan 30/60/90. Le partial calibre l'autonomie par niveau, et le plan consomme la scorecard et le debrief. Chaîner `indicateurs` pour les points d'étape serait du sur-chaînage. Contenu à compléter : prérequis d'arrivée (DPAE, visite d'information, mutuelle), alignement sur la fin de la période d'essai. | — | probable |

**Parcours recrutement** (documenté, pas une recette v1) : `fiche-poste` → [validation du manager] → `interview-loop-planner` → `interview-guide-recruteur` × N tours → [entretiens : scorecards de N intervieweurs] → **MANQUE : debrief consolidé** → [Go / No-go] → `contrat-emploi` → `onboarding-plan`. Ce parcours demande trois capacités que le moteur n'a pas (éventail, pause à plusieurs tiers, imbrication) et un skill de debrief qui manque. Réduit à `fiche-poste` → `interview-loop-planner`, il n'achèterait rien que la séquence manuelle ne donne déjà.

## RH — suivi des personnes et organisation

| Skill (version) | Catégorie | Raison | Enchaînement proposé | Confiance |
|---|---|---|---|---|
| `entretien-professionnel` (1.2.0) | simple | Les 7 gestes sont métier (cadre légal, 4 axes, questions au salarié, compte rendu, alertes). Aucune découpe n'achète d'isolation. **Contenu périmé** : voir annexe B. | — | sûr |
| `performance-review-helper` (1.3.0) | **à enrichir** | Une fois retirés les recoupements, il reste peu de métier. Les objectifs SMART (§3) recoupent `okr` et entrent en collision de déclenchement avec lui. Les questions de dialogue (§4) sont proches de `questioning`. Le plan de développement (§5) empiète sur `plan-developpement-competences`. Manquent : échelle d'appréciation et biais d'évaluation, auto-évaluation du salarié, « ne jamais inventer le point de départ », cadre légal (L1222-2/3, consultation du CSE sur le dispositif). | — | probable |
| `plan-developpement-competences` (1.2.0) | simple | Tous les gestes sont métier : renforcer / acquérir / maintenir, catalogue de formats, jalons, financement. L'indicateur de progrès n'est pas le travail d'`indicateurs`. | — | sûr |
| `analyse-entretien` (1.0.0) | simple | Il fait un seul geste : extraire des signaux de notes d'**entretien annuel** et les classer certain / probable / à confirmer, avec lecture par niveau via le partial. Il est classé à tort en recrutement par son déclencheur. Sa typologie de risques reste maigre (rien sur les risques psychosociaux, ni sur ce qu'il ne faut pas consigner). | — | probable |
| `people-review` (1.2.0) | **mélange** | Le cœur est métier : agrégation, 9-box, succession, actions par catégorie. Deux éléments du texte réclament pourtant une découpe. (a) La contrainte « pas de classement nominatif sans validation du sponsor » est une pause humaine écrite dans le skill : c'est le comité de calibrage, qui doit précéder la synthèse. (b) La règle « les signaux individuels sont des entrées, pas des sorties » serait garantie par l'isolation : le rédacteur de la synthèse ne voit pas les noms. `category: decision` est trompeur, le skill prépare des décisions, il ne tranche pas. | 1 `ix-recipes:people-review` allégé en dossier de calibrage (agrégats sans nom, dossier nominatif, actions candidates), fiche de contexte → **validate** (calibrage, le sponsor décide de ce qui reste nominatif) → 2 `ix-skills:deliver` (synthèse COMEX, ne reçoit jamais le dossier nominatif) → **validate** → 3 *(facultative)* `ix-skills:controle-qualite` (aucun nom, aucune réidentification par petit effectif, performance ≠ potentiel) → **validate**. Achète : la pause de calibrage, la confidentialité garantie par isolation, une vérification séparée. | à discuter |
| `lettre-cadrage-disciplinaire` (1.1.0) | simple | Contenu dense et propre : refus si les faits sont vagues, proportionnalité, gabarit, prescription de 2 mois, *non bis in idem*. Une étape `legal-risk-flag` après la lettre referait ses §4-5. La vraie vérification séparée est l'avocat, que le skill impose déjà. Manquent : procédure de l'entretien préalable (L1332-2), règle des 3 ans, risque de requalification en avertissement. | — | sûr |
| `offboarding-structure` (1.2.0) | simple | Une seule passe : savoirs, projets, accès, checklist administrative, entretien de sortie, dernière semaine. Les risques de continuité sont un sous-produit du plan : `contrarian` derrière ferait un sandwich. La checklist ne varie pas selon le mode de départ (démission, rupture conventionnelle, licenciement, fin de CDD). | — | sûr |
| `org-design-brief` (1.1.0) | **à enrichir** | 4 gestes sur 6 sont ceux d'atomes (`problem-framing`, `argumentation`, `contrarian`, `key-assumptions`). Les deux gestes métier (cible, séquencement) sont vides : ni vocabulaire d'organisation, ni **information-consultation du CSE** (L2312-8). Le skill se déclenche pourtant « avant toute annonce », ce qui expose à un délit d'entrave. Il faut l'enrichir avant de juger. Forme probable ensuite : mélange autour d'une pause `answers` (avis du CSE), mais avec le même skill avant et après la pause (voir besoins de moteur). | — | sûr (minceur) |

**Cycle d'entretien annuel** : la chaîne `performance-review-helper` → `plan-developpement-competences` de la revue du 2026-10-14 est fausse, car elle saute l'entretien lui-même. Le bon enchaînement passe par la pause de l'entretien et par `analyse-entretien`. C'est la première recette proposée au §2 final.

## Juridique

| Skill (version) | Catégorie | Raison | Enchaînement proposé | Confiance |
|---|---|---|---|---|
| `cgv-checker` (1.2.1) | simple | Un seul geste, lire des clauses depuis une position : position, clauses structurantes, test de chaque clause, risque global, « RAS ». Extraire le test vers `critique` ferait un sandwich. Mince en droit : il promet de repérer les « clauses abusives » sans citer aucune grille (R. 212-1 et R. 212-2 C. conso., 1171 C. civ., L. 442-1 C. com.). | — (mélange si vérification séparée, question 8) | probable |
| `contrat-fournisseur` (1.2.1) | simple | Même geste que `cgv-checker`, position acheteur fixée. Le classement par impact porte sur 3 à 8 points produits juste avant : en sortir un `prioritize` ferait un sandwich. Sa description promet la rédaction (« rédige un contrat fournisseur ») sans aucune méthode dans le corps, et la règle « RAS » manque. | — (idem `cgv-checker`) | probable |
| `legal-risk-flag` (1.2.1) | simple | C'est un triage rapide revendiqué (« one quick pass », « RAS » sous le niveau moyen). Une chaîne trahirait sa raison d'être. | — | sûr |
| `nda-draft` (1.1.1) | simple | Une seule production, et l'utilisateur connaît les informations manquantes : pas de tiers à interroger. Toujours mince en contenu (unilatéral ou mutuel, durées, informations résiduelles, non-sollicitation, *standstill*), mais l'enrichissement ajouterait du contenu, pas d'étape. | — | sûr |
| `compliance-checklist` (1.1.1) | **à enrichir** | L'étape 1 « identifier les domaines concernés » n'en nomme **aucun**. Manquent une table domaine → déclencheur (consommation, LCEN, ePrivacy, accessibilité, NIS2, AI Act, DSA, LCB-FT, sectoriel, facturation électronique), la règle de date que porte `conformite-rgpd`, et la frontière avec ce dernier. | — (mélange possible, question 8) | à discuter |
| `conformite-rgpd` (1.3.0) | simple | Le skill le plus riche des deux familles : 9 étapes article par article. L'erreur relevée le 2026-10-14 est corrigée. Le seul enchaînement envisageable serait de le rejouer avec les réponses de l'équipe produit, donc le même skill deux fois (voir besoins de moteur). | — | sûr |

**Fusion `contrat-fournisseur` / `cgv-checker`** (cadrage-suite §6 q5) : avis favorable, à une condition. Les deux méthodes sont identiques à la liste de clauses près, et les déclencheurs se marchent dessus sur « CGV fournisseur ». La fusion donnerait un seul skill, avec la position et le type de document en paramètres et les jeux de clauses par type de contrat en `references/`. La condition : régler d'abord le mode rédaction promis et absent (le retirer de la description, ou en faire un manque du catalogue).

## Finance, marché et stratégie

| Skill (version) | Catégorie | Raison | Enchaînement proposé | Confiance |
|---|---|---|---|---|
| `budget-variance-analysis` (1.1.0) | **à enrichir** | Il cite « volume, prix, mix, calendrier » sans formule de décomposition ni seuil de matérialité, donc sans dire ce qui est « significatif » (étape 1). Les étapes 3-5 sont génériques. Une fois enrichi, ce sera probablement un skill simple, ou l'étape 1 du parcours de clôture. | — | probable |
| `business-case-draft` (1.1.0) | simple | Il recommande déjà (étape 6) : conforme au §6bis, pas de `decision` → `deliver` derrière. Les parties du dossier se répondent. Reste le biais signalé le 2026-10-14, des chiffres construits pour la recommandation (question 9). | — | sûr |
| `financial-narrative` (1.1.1) | simple | L'interprétation (relier chaque variation à un facteur confirmé ou supposé) est le cœur du skill et ne se sépare pas de la rédaction. | — | sûr |
| `strategie-prix` (1.1.0) | **à enrichir** | Texte inchangé, toujours « `explorer` → `decision` avec un titre » : étape 2 = `explorer`, étapes 3-4 = `decision`, étape 5 = `key-assumptions`. Seul savoir propre : « ne pas mélanger prix, packaging et go-to-market ». Il n'y a ni catalogue de modèles, ni métrique de valeur, ni méthode de consentement à payer. | Si enrichi (mélange) : 1 `ix-recipes:strategie-prix` allégé (valeur, segments, modèles candidats, sans recommandation) → **choose** (l'humain retient les modèles et les critères) → 2 `ix-skills:decision` → **validate**. Achète : `decision` ne voit pas la demande, qui nomme souvent déjà le modèle. | sûr (minceur) |
| `note-strategique` (1.1.0) | simple | Conforme au §6bis, le texte ne le contredit pas. | — | sûr |
| `tam-sam-som` (1.1.0) | simple | Les gestes sont tous métier (périmètre, top-down, bottom-up, comparaison) ; `research` avant ferait un sandwich. Point nouveau : en un seul passage, le bottom-up s'ancre sur le top-down calculé juste avant. Les isoler demanderait deux branches parallèles (besoins de moteur), pas assez pour reclasser. | — | probable |
| `metriques-saas` (1.1.0) | **à enrichir** | La règle absolue exige « toujours donner les formules », mais le skill n'en contient aucune (MRR/ARR, NRR/GRR, CAC, LTV, payback, burn multiple, Rule of 40). Sa description dit « ne recommande rien », alors que son rôle et sa Definition of done relient les chiffres aux décisions. | — | sûr |
| `tableau-de-bord-kpi` (1.1.0) | simple | Savoir réel et suffisant : KPI avancés et de résultat, fiche par KPI, 5 à 10 KPI, refus d'un KPI sans cible. La frontière avec `indicateurs` est nette. | — | sûr |
| `analyse-concurrentielle` (1.1.0) | **à enrichir** | La seule distinction métier est « direct / indirect / substitut ». Il n'y a aucun cadre nommé (Porter, carte de positionnement, axes types). Le territoire est bien métier (`research` et `outside-in` l'excluent), mais il est vide. | — | probable |

**Vérification des chiffres** : cinq skills produisent des chiffres repris tels quels. Une vérification isolée achèterait vraiment quelque chose, mais elle bute sur deux manques. `fact-check` vérifie la présence d'un chiffre dans la source, pas un calcul : un écart, un NRR ou un ROI dérivé sortirait « pas dans la source » (**MANQUE : vérification de calcul**). Et la source (le tableau de l'utilisateur) est interdite après l'étape 1. Meilleur candidat une fois ces deux points réglés : le **parcours de clôture** `ix-recipes:budget-variance-analysis` → **answers** (responsables budgétaires) → `ix-recipes:financial-narrative` → vérification.

## Commercial et achats

| Skill (version) | Catégorie | Raison | Enchaînement proposé | Confiance |
|---|---|---|---|---|
| `analyse-cdc` (1.3.0) | simple | Un seul geste, la lecture critique d'une source côté répondant. Les étapes 2-6 (explicite, implicite, contradictions, risques, questions) demandent toutes le texte sous les yeux. La part d'atome (`questioning`) est déjà sortie dans `reponse-appel-offres`. | — (étape 1 de `reponse-appel-offres`) | sûr |
| `offre-commerciale` (1.1.0) | simple | Son geste propre est la rédaction du contenu client. Les étapes 1, 2 et 4 (nature de la réponse, ce qui est assez stable pour engager, position) sont du choix, déjà fait en amont par `decision` et `brief` dans `reponse-appel-offres`. En usage seul, une passe suffit pour une petite proposition. Savoir métier mince malgré 110 lignes : 5 contraintes sur 7 sont des « ne pas » ; le savoir propre aux appels d'offres est dans la mission de la recette, pas dans le skill. | — (mélange selon la question 3) | probable |
| `negotiation-brief` (1.1.0) | simple | Un seul geste : préparer une position (ouverture, cible, ligne rouge, leviers, concessions, BATNA). Une relecture `red-team` côté fournisseur se lance à la main après coup : ni pause ni tiers entre les deux. Côté acheteur seulement. | — | sûr |
| `rfp-draft` (1.1.0) | simple | Une production : passer d'un besoin interne à un cahier des charges, avec un gabarit métier. `cadrage` en amont seulement si le besoin est flou. Manque clé : il n'impose ni cadre de réponse ni bordereau de prix, ce qui rend les offres difficiles à comparer, et il ne prévoit pas de recevoir une grille existante. | — | probable |
| `vendor-scorecard` (1.1.0) | **à enrichir** | Sans savoir métier, la méthode se ramène à « construire une grille pondérée ». Manquent : dimensions par défaut selon le type d'achat, exemples d'éliminatoires, formules de notation du prix, repères d'échelle, règle des pondérations figées **avant** les offres. Son déclencheur « comment noter ces offres reçues » est le travail d'`offer-comparison`. | — | sûr (minceur) |
| `total-cost-analysis` (1.1.0) | simple | Un geste entièrement métier : coût sur le cycle de vie, coûts cachés, sensibilité. Il compare sans recommander, ce qui le distingue de `decision` et d'`offer-comparison`. | — | sûr |
| `offer-comparison` (1.1.0) | simple | Tranché au §6bis : il reste le skill de notation et recommande déjà. Deux trous : il fixe lui-même les pondérations si aucune grille n'est fournie, et rien n'interdit de repondérer après avoir vu les offres. | — | sûr |

**Parcours achats** : il ne tient pas en l'état. `vendor-scorecard` → **validate** (pondérations) → `rfp-draft` → [offres reçues] → **MANQUE : normaliser une offre reçue** × N → `total-cost-analysis` → `offer-comparison`. Il bute sur trois points : le manque de normalisation (`offer-comparison` refuse les offres brutes), le parallèle (une branche par offre), et l'accès à la source (`rfp-draft` en étape 2 doit connaître le besoin en détail, que la fiche de contexte ne porte pas).

## Produit et UX

| Skill (version) | Catégorie | Raison | Enchaînement proposé | Confiance |
|---|---|---|---|---|
| `prd` (1.1.0) | simple | Les 9 étapes remplissent un gabarit sous la règle « le quoi et le pourquoi, jamais le comment ». Ses entrées supposent un matériau déjà cadré : on va donc droit au skill. Les questions sortent en fin de livrable, sans attente intermédiaire. | — (mélange selon la question 4) | probable |
| `product-spec` (1.1.0) | simple | Une seule production. Le texte porte surtout sur la forme (6 artefacts compagnons), presque pas sur le savoir produit. Son entrée `spec_plan` ne correspond plus à aucune sortie d'`analysis`. | — | probable |
| `feature-spec` (1.1.1) | simple | C'est le skill de la famille qui porte le plus de discipline métier (US, MoSCoW, « si tout est Must, rien ne l'est », Given/When/Then, cas limites). En sortir MoSCoW vers `prioritize` ferait un sandwich. | — | sûr |
| `reformulation-us` (1.1.0) | simple | Un seul geste, réécrire sans reconstruire. Ce n'est pas `rephrase`. C'est un **point d'entrée** sur un backlog existant, pas une étape après la spec. | — | sûr |
| `okr` (2.1.0) | simple | Deux modes qui ne fusionnent jamais. Les tests du mode relecture demandent du jugement, pas l'application d'une règle (`controle-qualite`). Le mode rédaction n'est ni `explorer` ni `questioning`. La longueur est du contenu. La séquence mode 2 → séance humaine → mode 1 reste manuelle. | — | sûr |
| `persona` (1.1.0) | **mélange** (seulement avec des données terrain) | Les étapes 1-2 (repérer les motifs, grouper en segments) sont le geste d'`affinity-mapping` en mode `open`. Les étapes 3-6 (portrait, besoins non exprimés, observé / inféré / supposé) sont métier. La décision du §6bis n'est **pas reportée** dans le texte : persona regroupe toujours lui-même. | 1 `ix-skills:affinity-mapping` (corpus brut, fiche de contexte) → **validate** (l'humain retient au plus 4 groupes) → 2 `ix-recipes:persona` allégé (portraits, besoins, statut des preuves). Achète : les groupes naissent des données avant que le cadre persona les colore, et l'humain choisit les groupes. **Bloqué par le moteur** : `affinity-mapping` recopie chaque item tel quel, ce que le contrôle de fuite refuse (besoins de moteur). | probable |
| `journey-map` (1.1.0) | simple | Un seul geste du point de vue de l'utilisateur. Trier des verbatims par étape via `affinity-mapping` ferait un sandwich, puisque les étapes sont posées par le skill lui-même. | — | sûr |
| `mockup` (1.1.0) | **à enrichir** | Les 5 étapes ne contiennent aucun savoir de design (fidélité, hiérarchie, accessibilité, états, responsive, marquage du provisoire, design system). La comparaison avec `frontend-design` (anthropics/skills), prévue depuis le 2026-10-14, n'est toujours pas faite. | — | à discuter |

**Fusion `feature-spec` / `product-spec`** (chantier H) : avis favorable. Les deux font « une spec actionnable » avec critères d'acceptation, et leurs déclencheurs vont entrer en collision. Le savoir utile est dans `feature-spec`, et `product-spec` n'apporte que les artefacts compagnons. L'argument du 2026-10-14 pour garder l'id `product-spec` (renvois depuis `analysis` et `cadrage`) n'existe plus : ces renvois ont été retirés d'ix-skills. Avant de fusionner, faire le test « la source Anthropic est-elle bien plus riche ? » sur `write-spec` (chantier I).

**Parcours produit** : il existe, mais comme parcours documenté. Chaque passage est un événement humain : validation du PRD, revue de design, séance d'OKR. Chemin des README : `brief` → `prd` → `feature-spec`. Le seul segment qui achète quelque chose comme recette est `affinity-mapping` → `persona`.

## Tech

| Skill (version) | Catégorie | Raison | Enchaînement proposé | Confiance |
|---|---|---|---|---|
| `system-design` (1.1.1) | simple | Les étapes ressemblent à des atomes (exigences ≈ `cadrage`, arbitrages ≈ `decision`, hypothèses ≈ `key-assumptions`), mais elles portent sur un objet unique en construction qu'un même contexte doit tenir de bout en bout. Pour choisir entre architectures concurrentes, le chemin est `explorer` → `decision`. | — (mélange selon la question 8) | probable |
| `tech-debt` (1.2.1) | simple | Un seul geste outillé par une formule maison : (Impact + Risque) × (6 − Effort), seuils 28 / 15. Extraire la notation vers `prioritize` ferait un sandwich. | — | sûr |
| `ticket-triage` (1.1.2) | simple | Un ticket, un passage : catégorie, P1-P4 aux définitions dures, routage, réponse type. Rien à isoler, pas de tiers à attendre. | — | sûr |

---

## Manques du catalogue

Gestes qu'aucun skill ne couvre, révélés par la revue. Aucun n'est conçu ici.

| Manque | Révélé par | Bloque |
|---|---|---|
| **Debrief de recrutement consolidé** (N scorecards pour un candidat → score pondéré, écarts > 1,5 point, drapeaux confirmés, ordre du jour du debrief ; ne tranche pas) | `interview-loop-planner`, `interview-guide-recruteur`, `onboarding-plan` | parcours recrutement |
| **Vérification de calcul** (recalculer chaque chiffre dérivé à partir des valeurs sources). Geste cognitif, donc atome **ix-skills** | `budget-variance-analysis`, `business-case-draft`, `metriques-saas`, `financial-narrative`, `tam-sam-som` | toute queue de vérification chiffrée |
| **Normaliser une offre fournisseur reçue** (prix décomposé, périmètre, réserves, pièces manquantes) | `offer-comparison`, `total-cost-analysis` | parcours achats |
| **Conduite d'une AIPD** (art. 35(7), questions au responsable, avis du DPO) : vraie recette potentielle, avec un tiers qui répond | `conformite-rgpd` | — |
| **Rédaction d'un contrat de prestation ou de fournisseur** | `contrat-fournisseur` (le promet sans le faire) | fusion avec `cgv-checker` |
| **Convocation à l'entretien préalable disciplinaire** (L1332-2) | `lettre-cadrage-disciplinaire` | procédure disciplinaire complète |
| **Dossier d'information-consultation du CSE** (ou intégré à `org-design-brief`) | `org-design-brief` | réorganisation |
| **Négociation côté vendeur** (ou élargir `negotiation-brief`) | `reponse-appel-offres`, qui s'arrête à la remise | — |
| Revue d'ergonomie et d'accessibilité (à discuter) | `mockup`, `journey-map` | — |
| Partials manquants (pas des skills) : formules financières ; potentiel et 9-box (`talent_review`) ; jeux de clauses par type de contrat ; règles US partagées | finance, `people-review`, juridique, produit | enrichissement des « à enrichir » |

---

## 1. Besoins de moteur révélés

Classés par nombre de skills et de familles concernés. « Déjà couvert » indique ce que l'exécuteur sait déjà faire ([`executeur.md`](executeur.md)).

### 1.1 Accès d'une étape à la source d'origine — le plus fréquent

Le format interdit la demande brute après l'étape 1, et l'exécuteur le vérifie (contrôle de fuite). Le champ `verbatim` ne suffit pas : il plafonne à 85 % de la source et refuse une ligne de 40 mots ou plus. C'est le cas déjà vu du fact-check qui ne pouvait pas vérifier par rapport à la demande d'origine. Quatre formes du même besoin :

| Forme | Skills | Pourquoi `verbatim` ne suffit pas |
|---|---|---|
| **Vérifier une absence** | `cgv-checker`, `contrat-fournisseur`, `compliance-checklist` | Les skills signalent des clauses ou des sections **absentes**, ce qu'on ne vérifie qu'en relisant tout le document. |
| **Vérifier contre un tableau de données** | `budget-variance-analysis`, `business-case-draft`, `financial-narrative` | Le tableau budget / réel **est** toute la source. |
| **Travailler sur le détail du besoin en étape 2** | `rfp-draft` dans le parcours achats ; `offer-comparison` (critères qualitatifs, qui exigent le texte des offres) | La fiche de contexte porte des faits courts, pas un périmètre détaillé. |
| **Citer sans réécrire** | `persona` (après `affinity-mapping`) ; `people-review` (vérifier qu'aucun fait individuel n'est inventé) | `affinity-mapping` recopie chaque item par construction : le contrôle de fuite **bloquerait** la recette décidée au §6bis. |

Deux réponses possibles : (a) une **lecture seule de la source déclarée sur une étape nommée** (ex. `receives: [source]` réservé aux étapes de contrôle), distincte du passage du brief ; (b) un **handoff par identifiants** (I1, I2…), où l'étape aval reçoit les items désignés et non une recopie. La forme (a) couvre la vérification, la forme (b) couvre `persona`.

### 1.2 Branches parallèles (éventail, puis jonction)

| Éventail | Skills | Jonction |
|---|---|---|
| Un guide par tour d'entretien | `interview-loop-planner` → `interview-guide-recruteur` × N | — |
| Un sous-parcours par candidat | parcours recrutement | debrief consolidé (**MANQUE**) |
| Une analyse par collaborateur | `analyse-entretien` × N → `people-review` ; mode collectif de `plan-developpement-competences` | `people-review` |
| Une branche par offre reçue | normalisation (**MANQUE**) × N | `total-cost-analysis` → `offer-comparison` |
| Un lot à la fois | `analyse-cdc`, `offre-commerciale` (appel d'offres alloti) | — |
| Deux estimations isolées | `tam-sam-som` (top-down / bottom-up, contre l'ancrage) | comparaison |
| Une fiche par concurrent | `analyse-concurrentielle` (mode approfondi) | comparaison |
| Une spec par lot | `ix-skills:analysis` → `product-spec` × N | `controle-qualite` (cohérence avec le PRD) |

Le parallèle est le plus souvent demandé par un **parcours**, rarement par un skill seul. Il conditionne les parcours recrutement et achats, et la version complète de `people-review`.

### 1.3 Rejouer un même skill après une pause (phases, boucles)

| Cas | Skills |
|---|---|
| **Deux phases d'un même skill autour d'une pause** | `people-review` (positionner → calibrage → actions), `org-design-brief` (cible → avis du CSE → mise en œuvre), procédure disciplinaire (convoquer → entretien préalable → notifier), `okr` (mode 2 → séance → mode 1) |
| **Itérer avec les réponses d'un tiers** | `conformite-rgpd` (traitements inférés confirmés par l'équipe produit), `tech-debt` (impact fourni par le PM), `negotiation-brief` (un passage par tour de négociation) |
| **Refaire jusqu'à conformité** | `reponse-appel-offres` : `controle-qualite` → `offre-commerciale` |

Déjà couvert à la main : `rerun <étape> --extra <étape>.<champ>` relance une étape avec un champ supplémentaire (c'est l'exemple « l'offre avec les verdicts »). Ce qui manque, c'est une boucle déclarée dans la recette. Le premier obstacle n'est d'ailleurs pas le moteur : c'est la règle de `concepteur-recette` « même skill deux fois = manque du catalogue » (question 2).

### 1.4 Autres besoins

- **Pause à plusieurs tiers** : recueillir N réponses séparées, sans que l'une voie l'autre (scorecards de N intervieweurs, réponses de N responsables budgétaires, offres de N fournisseurs). Aujourd'hui, `answers` est un seul collage. L'idée `answer --append` (cadrage-suite) en est le premier pas, sans l'isolation entre tiers.
- **Taille des réponses collées** : 3 à 5 offres de plusieurs dizaines de pages rendent bloquant le constat du lot 1 (réponses transmises en entier). Le « résumé borné des réponses longues » est hors v0 dans `executeur.md`.
- **Confidentialité par champ et rétention de la trace** : notes d'entretien, scorecards de candidats, dossier nominatif de `people-review`. La trace `./parcours/<slug>/` devient une donnée RGPD (la CNIL recommande 2 ans au plus pour un candidat non retenu). Il faut un fichier à part pour les champs sensibles et une purge par dossier. Le cloisonnement par `receives` existe déjà.
- **Étape 1 facultative ou double point d'entrée** : `persona`, avec données terrain (`affinity-mapping` d'abord) ou sans (persona seul, en mode hypothèse).
- **Imbrication** (un parcours qui en lance d'autres) : parcours recrutement (conception, puis un sous-parcours par candidat). Déjà prévue au §5 du format, attendue après la v1.
- **Déjà couvert, pas un besoin** : les pauses de plusieurs semaines (entretien tenu, avis du CSE, consultation fournisseurs). L'état est sur disque (`state.json`) et la page de suivi garde les dossiers ouverts.

**Conséquence pour l'ordre des chantiers moteur** : l'accès à la source (§1.1) débloque `persona`, la queue de vérification (juridique, finance) et le démarrage du parcours achats. Le parallèle (§1.2) débloque surtout des parcours entiers (recrutement, achats), qui demandent aussi des skills manquants. Proposition : **accès à la source d'abord, parallèle ensuite, boucles déclarées en dernier** (le `rerun` manuel couvre le besoin en attendant).

## 2. Ordre de priorité des recettes à construire

Critère : faisable en v1 sans moteur nouveau d'abord, puis dans l'ordre de ce que débloque chaque chantier moteur. Une recette dont l'utilité dépend d'une question reste conditionnelle.

| # | Recette | Enchaînement | Ce qu'elle achète | Prérequis | Faisable en v1 |
|---|---|---|---|---|---|
| 1 | **Entretien annuel** | `ix-recipes:performance-review-helper` (ou `entretien-professionnel`) → **answers** (l'entretien a lieu, notes collées) → `ix-recipes:analyse-entretien` → **validate** → `ix-recipes:plan-developpement-competences` → **validate** | un tiers qui répond (le salarié) ; l'analyse lit ce qui a été dit sans voir les hypothèses de préparation, ce qui coupe le biais de confirmation | mettre `entretien-professionnel` à jour (loi 2025-989) ; enrichir `performance-review-helper` ; écrire la frontière entre axes **présumés** et axes **constatés** | oui |
| 2 | **Proposition commerciale** (si question 3 = oui) | étapes de `brief-client` (`ix-skills:cadrage` → `ix-skills:questioning` → **answers** client → `ix-skills:brief`, **validate** : l'humain fixe la position et le prix) → `ix-recipes:offre-commerciale` allégé → `ix-skills:controle-qualite` → **validate** → `ix-skills:deliver` | la pause sur la position et le prix avant la rédaction ; une vérification séparée que le chemin informel n'a pas | `offre-commerciale` réduit à la rédaction ; 6 étapes, la limite. Recopier aussi les étapes facultatives `explorer` → `decision` de `brief-client` mènerait à 8 : à laisser dehors, ou à choisir à la place du contrôle | oui |
| 3 | **PRD depuis une demande de sponsor** (si question 4 = oui) | `ix-skills:cadrage` → `ix-skills:questioning` → **answers** (parties prenantes) → `ix-recipes:prd` → **validate** | l'isolation protège « jamais le comment » contre les solutions glissées dans la demande ; les réponses des parties prenantes | aucun : `prd` reste tel quel, en dernière étape | oui |
| 4 | **Persona** (décidé au §6bis) | `ix-skills:affinity-mapping` → **validate** → `ix-recipes:persona` allégé | groupes issus des données ; choix humain des groupes | moteur §1.1 (citer sans réécrire) ; `persona` allégé ; double point d'entrée | non |
| 5 | **People review** (si question 5 = oui) | voir le tableau RH | calibrage avant synthèse ; confidentialité par isolation | rétention de la trace (§1.4) ; version complète avec le parallèle (§1.2) | oui, version réduite |
| 6 | **Clôture et reporting** | `ix-recipes:budget-variance-analysis` → **answers** (responsables budgétaires) → `ix-recipes:financial-narrative` → vérification | réponses des responsables ; vérification séparée des chiffres | enrichir `budget-variance-analysis` ; **MANQUE** vérification de calcul (ix-skills) ; moteur §1.1 | non |
| 7 | **Achats** | voir le tableau commercial | pondérations figées avant les offres ; comparaison sur offres normalisées | enrichir `vendor-scorecard` ; **MANQUE** normalisation ; moteur §1.1 et §1.2 | non |
| 8 | **Recrutement** | voir le tableau RH | — | moteur §1.2, pause à plusieurs tiers, imbrication ; **MANQUE** debrief consolidé | non : parcours documenté en attendant |

Hors recette, et à mener avant les recettes qui en dépendent : enrichir les 10 skills « à enrichir » (les manques sont dans les tableaux) et corriger les défauts de l'annexe B, en commençant par `entretien-professionnel` (repo public, contenu juridique périmé).

## 3. Questions à trancher par Amiel

**Moteur et format**

1. **Accès à la source** : faut-il le traiter avant les branches parallèles et les boucles (proposition du §1) ? Sous quelle forme : (a) lecture seule déclarée sur une étape de contrôle, (b) handoff par identifiants, ou les deux ?
2. **Même skill deux fois** : faut-il assouplir la règle de `concepteur-recette` pour les phases d'un même skill autour d'une pause (`people-review`, `org-design-brief`, `okr`, itération de `conformite-rgpd`), ou scinder ces skills ?

**Classements qui basculent selon ta réponse**

3. **`offre-commerciale`** : rédacteur autonome qui choisit sa position (skill simple), ou réduit à la rédaction derrière une position choisie, avec la recette « proposition commerciale » (mélange, priorité 2) ?
4. **`prd`** : tes PRD partent-ils souvent d'une demande brute de sponsor, avec des parties prenantes à interroger ? Si oui, recette 3.
5. **`people-review`** : la séance de calibrage existe-t-elle chez les utilisateurs visés ? Si non (une DRH de PME seule face au COMEX), il redevient un skill simple, et il suffit de requalifier `category: decision`.
6. **`persona`** : les personas se font-ils le plus souvent avec des verbatims et des notes de terrain ? Si c'est rare, la recette ne vaut pas le chantier moteur qu'elle exige.
7. **Cycle d'entretien annuel** : est-il dans la cible ? Si oui, il devient la recette prioritaire et entraîne la mise à jour d'`entretien-professionnel`, l'enrichissement de `performance-review-helper` et la frontière avec `plan-developpement-competences`.
8. **Vérification séparée** : veux-tu une étape de vérification isolée derrière les lectures de contrat (`cgv-checker`, `contrat-fournisseur` → `ix-skills:fact-check` en mode `closed`) et derrière les skills chiffrés (vérification de calcul) ? Si oui, ils passent en mélange une fois l'accès à la source disponible. Même logique, plus marginale : `compliance-checklist` → `conformite-rgpd` après une pause sur les domaines, et `ix-skills:questioning` → **answers** → `system-design` quand le brief technique est flou.
9. **`business-case-draft`** : faut-il une validation humaine des hypothèses chiffrées **avant** la recommandation ? Si oui, il devient un mélange (chiffrage → **validate** → `ix-skills:decision`), ce qui revient sur le §6bis.
10. **`strategie-prix`** : l'enrichir (mélange, voir tableau) ou le retirer, puisqu'il double aujourd'hui `explorer` + `decision` ?

**Catalogue**

11. **Fusions** : `contrat-fournisseur` + `cgv-checker` (avis favorable, après avoir réglé le mode rédaction) ; `feature-spec` + `product-spec` (avis favorable, id survivant à choisir). On fusionne ?
12. **Périmètres** : `contrat-emploi` doit-il porter le droit du travail français, ou être réduit à la rédaction (l'analyse revenant à `legal-risk-flag`) ? `analyse-entretien` doit-il couvrir les notes d'entretien de recrutement, et devenir le debrief qui manque ? `vendor-scorecard` doit-il couvrir le marché public ? `mockup` : l'enrichir ou le retirer, après la comparaison avec `frontend-design` ?

---

## Annexe A — Les 13 skills « minces » du 2026-10-14

| Skill | 2026-10-14 | 2026-10-16 |
|---|---|---|
| `fiche-poste` | mince (partial absent) | **simple** : relevé par le partial |
| `onboarding-plan` | mince | **simple** : relevé par le partial ; reste les prérequis légaux d'arrivée |
| `nda-draft` | mince | **simple**, contenu toujours mince (classable : l'enrichissement n'ajoute pas d'étape) |
| `contrat-emploi`, `performance-review-helper`, `org-design-brief`, `compliance-checklist`, `budget-variance-analysis`, `strategie-prix`, `vendor-scorecard`, `analyse-concurrentielle`, `metriques-saas`, `mockup` | minces | **à enrichir**, textes inchangés depuis (sauf `performance-review-helper`, relevé par le partial sans en sortir) |

Nouveaux skills minces en contenu, mais classables : `cgv-checker` (aucune grille légale), `offre-commerciale` (savoir propre aux offres absent), `product-spec` (règles de forme seulement), `analyse-entretien` (typologie maigre).

## Annexe B — Défauts relevés en passant (non corrigés, hors périmètre)

À traiter dans un chantier de contenu ; aucun ne change un classement.

- **`entretien-professionnel` — contenu juridique périmé.** La loi n° 2025-989 du 24/10/2025 remplace l'entretien professionnel par l'« entretien de parcours professionnel » : dans l'année de l'embauche puis tous les 4 ans (au lieu de 2), état des lieux à 8 ans (au lieu de 6), plus systématique au retour d'une longue absence s'il y en a eu un dans les 12 mois. Le skill dit encore « biennal » et « 6 ans ». Sources relevées : [Centre Inffo](https://www.centre-inffo.fr/site-droit-formation/actualites-droit/entretiens-de-parcours-professionnels-mise-a-jour-du-questions-reponses), [Lefebvre Dalloz](https://formation.lefebvre-dalloz.fr/actualite/entretien-de-parcours-professionnel-ce-qui-change-en-2025-et-comment-sy-preparer). Le repo est public : c'est le plus urgent.
- **`org-design-brief`** : il se déclenche « avant toute annonce » sans mentionner la consultation du CSE (risque de délit d'entrave).
- **`tech-debt`** : l'effort est inversé deux fois (« effort (inverted) » à l'étape 2, puis « 6 − Effort » à l'étape 3) ; les items faciles peuvent tomber sous le seuil.
- **`ticket-triage`** : l'étape 4 vérifie les doublons sans recevoir de base de tickets.
- **`contrat-fournisseur`** : sa description promet la rédaction, absente du corps ; il n'a pas de règle « RAS ».
- **`contrat-emploi`** : le mode `revision` est déclaré dans `.mystaffy.json` mais absent du corps.
- **`metriques-saas`** : sa description dit « ne recommande rien », alors que son rôle et sa Definition of done relient les chiffres aux décisions.
- **`tam-sam-som`, `metriques-saas`, `analyse-concurrentielle`** : ils invoquent des modes flash / standard / deep sans les définir (ce sont ceux de `research`).
- **`persona`** : la décision du §6bis n'est pas reportée dans le texte.
- **`product-spec`** : son entrée `spec_plan` est morte. **`prd`** cite « feature spec » en entrée, alors qu'elle est en aval.
- **`reponse-appel-offres`** : les « main risks » d'`analyse-cdc` ne sont transmis à aucune étape, alors que le go / no-go juge le risque prix.
- **`interview-guide-recruteur`** : le `round_brief` manque dans les entrées attendues ; sa Definition of done se place à l'échelle du rôle et non du tour. Les partials transverses (anti-biais, debrief) sont recopiés dans `interview-guide-recruteur` et `interview-loop-planner` au lieu d'être dans `partials/` (CLAUDE.md §3bis).
- **`offer-comparison`** : rien n'interdit de repondérer après avoir vu les offres. **`vendor-scorecard`** : son déclencheur chevauche celui d'`offer-comparison`.
- **`performance-review-helper`** et **`okr`** se disputent le déclencheur « objectifs SMART ». **`analyse-entretien`** : son déclencheur « notes d'entretien » capte aussi les notes de recrutement.
- **`lettre-cadrage-disciplinaire`** : le README le présente comme un écrit avant procédure, alors que le skill rédige des sanctions.
