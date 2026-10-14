# ix-recipes

Recettes métier construites sur [ix-skills](https://github.com/amiel-35/ix-skills) : livrables RH, juridiques, financiers, achats, produit et tech, et workflows qui enchaînent les atomes d'ix-skills.

*[English version](README.md)*

## À propos

[ix-skills](https://github.com/amiel-35/ix-skills) fournit les ingrédients : des gestes cognitifs atomiques (critique, decision, explorer, fact-check…) qui s'appliquent à n'importe quel contenu. ix-recipes fournit les recettes :

- **des skills métier** : ils reposent sur une connaissance de domaine qui peut être fausse ou périmée (droit du travail, RGPD, pratiques RH, formules financières, méthodes produit), ou ils produisent un artefact défini par une profession (PRD, NDA, fiche de poste, TCO) ;
- **des workflows** : des enchaînements d'atomes ix-skills pour un travail récurrent. Le format est en cours de conception ; les deux premiers candidats sont listés plus bas.

ix-recipes dépend d'ix-skills, jamais l'inverse : une recette peut renvoyer vers un atome ix-skills, un atome ix-skills ne renvoie jamais vers une recette.

48 skills, déplacés depuis ix-skills le 2026-10-14 avec leur historique git.

## Démarrage rapide

```bash
claude plugin marketplace add amiel-35/ix-recipes
claude plugin install ix-recipes@ix-recipes
```

Installer aussi [ix-skills](https://github.com/amiel-35/ix-skills) : les recettes et les workflows s'appuient sur ses atomes. Redémarrer Claude Code. Les skills sont préfixés (`/ix-recipes:contract-review`), et Claude les déclenche aussi depuis une demande ordinaire.

> Transition : jusqu'à ix-skills 4.0.0, les mêmes skills sont aussi livrés dans ix-skills. Si les deux plugins sont installés, chacun de ces skills apparaît deux fois.

**Cowork** : « Ajouter depuis un dépôt » avec `amiel-35/ix-recipes`. **Codex CLI** : `bash scripts/install-codex.sh`.

## Convention du corpus : la sortie nulle

Un skill qui n'a rien à produire ouvre sa réponse par « RAS — » suivi de la raison, et s'arrête. Le jeton est littéral et identique dans ix-skills et ix-recipes, ce qui le rend cherchable et testable.

## Skills disponibles

<details>
<summary><b>👥 RH</b> — 13 skills</summary>

| Skill | Ce qu'il fait |
|---|---|
| `contrat-emploi` | Analyse ou rédige un contrat de travail, une offre d'embauche ou un avenant RH, avec points de vigilance et limite légale rappelée |
| `entretien-professionnel` | Prépare l'entretien professionnel obligatoire (art. L6315-1) — trame en 4 axes, questions d'exploration, gabarit de compte-rendu signable |
| `fiche-poste` | Produit une fiche de poste structurée et publiable — mission, responsabilités, compétences requises/souhaitables, critères de succès |
| `grille-remuneration` | Structure une grille de rémunération par famille de métier et niveau — fourchettes, critères de positionnement, règles de gouvernance |
| `interview-guide-recruteur` | Prépare le guide d'entretien recruteur pour UN round — questions STAR, annotations recruteur, mises en situation, grille de scoring 1-4, red flags gradués, fiche Go/No-go |
| `interview-loop-planner` | Conçoit la boucle d'entretien complète d'un recrutement — nombre de rounds, compétences par round, scorecard consolidé, planning, protocole de débrief collectif |
| `lettre-cadrage-disciplinaire` | Rédige un projet de courrier disciplinaire (avertissement, mise en garde, blâme) à partir de faits datés et documentés, à faire valider par un juriste avant envoi |
| `offboarding-structure` | Structure un plan d'offboarding — passation de connaissances et projets, checklist administrative, entretien de sortie, risques de continuité |
| `onboarding-plan` | Construit un plan d'intégration 30-60-90 jours pour un nouveau collaborateur — objectifs, actions, réunions, livrables et points de contrôle par phase |
| `org-design-brief` | Formalise une cible organisationnelle — diagnostic actuel, rationale, risques humains, séquencement — avant toute annonce ou mise en œuvre d'une réorganisation |
| `people-review` | Structure une revue de talents collective — matrice de positionnement, risques, plans de succession, actions prioritaires par catégorie |
| `performance-review-helper` | Prépare l'entretien annuel individuel — bilan structuré (réussites, axes de tension) et objectifs SMART pour N+1 |
| `plan-developpement-competences` | Construit un plan de développement des compétences, individuel ou collectif — actions concrètes, calendrier trimestriel, indicateurs, budget et financement |

</details>

<details>
<summary><b>⚖️ Juridique</b> — 7 skills</summary>

| Skill | Ce qu'il fait |
|---|---|
| `cgv-checker` | Repère les clauses déséquilibrées, inhabituelles ou sensibles d'un CGV ou CGU selon une position de lecture donnée (client, fournisseur, utilisateur) |
| `compliance-checklist` | Génère une checklist de conformité multi-domaines à partir d'un projet ou d'un contexte — obligations légales, contractuelles, réglementaires et sectorielles, chacune avec sa priorité et son statut de vérification |
| `conformite-rgpd` | Produit une checklist de conformité RGPD à partir d'une spec technique ou d'une description de traitement de données personnelles — bases légales, DPIA, DPO, transferts hors UE |
| `contract-review` | Analyse un contrat clause par clause — déviations par rapport aux positions standard, classification GREEN/YELLOW/RED, redlines prioritaires avec position de repli |
| `contrat-fournisseur` | Analyse ou rédige un contrat fournisseur du point de vue acheteur — SLA, pénalités, résiliation, exclusivité, prix, renouvellement — avec points de renégociation classés par impact |
| `legal-risk-flag` | Repère en un flash rapide les red flags juridiques d'un document — contrat, correspondance, tout texte — avec niveau de risque gradué (haut/moyen/bas) et action recommandée |
| `nda-draft` | Génère un projet de NDA adapté au contexte — parties, objet, durée, territoire — et calibré au type de relation (prestataire, partenariat, salarié, discussion M&A) |

</details>

<details>
<summary><b>💶 Finance et pricing</b> — 4 skills</summary>

| Skill | Ce qu'il fait |
|---|---|
| `budget-variance-analysis` | Analyse des écarts budget/réel ligne par ligne avec causes probables, hypothèses explicitement marquées et actions correctrices |
| `business-case-draft` | Structure une décision d'investissement en business case chiffré — coûts, bénéfices attendus, risques, hypothèses financières explicites |
| `financial-narrative` | Transforme des chiffres financiers bruts (résultats, budget, trésorerie) en récit clair et hiérarchisé pour une direction ou un board |
| `strategie-prix` | Formule une recommandation de pricing reliant valeur perçue, segmentation et modèles tarifaires possibles, avec trade-offs explicites et hypothèses critiques assumées |

</details>

<details>
<summary><b>🤝 Commercial et achats</b> — 6 skills</summary>

| Skill | Ce qu'il fait |
|---|---|
| `analyse-cdc` | Analyse un cahier des charges reçu du point de vue du répondant — exigences explicites et implicites, zones floues, contradictions, questions bloquantes avant tout engagement |
| `offre-commerciale` | Rédige le contenu d'une offre ou d'une réponse client structurée et argumentée, prête à intégrer avant mise en forme finale |
| `negotiation-brief` | Prépare une position de négociation achat avant la réunion — objectif, faits utiles, leviers, concessions possibles, BATNA, position d'ouverture, cible et ligne rouge assumée |
| `rfp-draft` | Génère un appel d'offres structuré — contexte, périmètre, exigences obligatoires et souhaitées, critères d'évaluation, conditions de réponse — depuis un brief achat ou métier |
| `total-cost-analysis` | Structure un TCO — coûts directs, coûts cachés, hypothèses, risques — sur un horizon donné, en distinguant coûts confirmés, estimés et non chiffrés |
| `vendor-scorecard` | Construit une grille d'évaluation fournisseur réutilisable — critères pondérés, échelle de notation, espace de commentaire qualitatif — l'outil de scoring, pas la décision finale |

</details>

<details>
<summary><b>🧭 Produit et UX</b> — 8 skills</summary>

| Skill | Ce qu'il fait |
|---|---|
| `feature-spec` | Produit la spec fonctionnelle complète d'une feature — user stories, exigences MoSCoW, critères d'acceptation Given/When/Then, métriques de succès |
| `journey-map` | Produit une carte de parcours utilisateur — étapes, actions, émotions, points de friction et opportunités — depuis le point de vue de l'utilisateur, pas du système |
| `okr` | Vérifie des lignes d'Objectif/Résultat clé déjà écrites, ou fait émerger un matériau à discuter depuis un brief flou |
| `persona` | Produit des personas utilisateurs structurés depuis des données de recherche, interviews ou un brief produit, en distinguant ce qui est observé de ce qui est supposé |
| `prd` | Produit un Product Requirements Document complet — problème, vision, utilisateurs cibles, périmètre inclus/exclu, exigences, métriques de succès — le quoi et le pourquoi, jamais le comment |
| `product-spec` | Transforme un brief ou un besoin déjà cadré en spécification exploitable — parcours, écrans, modèle de données, cas limites, critères d'acceptation — pour une équipe produit, design ou eng |
| `reformulation-us` | Réécrit des user stories existantes mal formulées en US propres, testables, avec critères d'acceptation Given/When/Then, en respectant l'intention d'origine |
| `tam-sam-som` | Estime TAM, SAM et SOM avec méthodes top-down et bottom-up, hypothèses explicites et limites de fiabilité assumées |

</details>

<details>
<summary><b>⚙️ Tech</b> — 5 skills</summary>

| Skill | Ce qu'il fait |
|---|---|
| `code-review` | Relit du code (diff, PR, fichiers ou extrait) sur quatre dimensions — sécurité, performance, correction, maintenabilité — avec constats classés critiques vs suggestions et référence de code précise |
| `system-design` | Conçoit un système ou une architecture technique — composants, flux de données, contrats d'API, stockage — avec trade-offs explicites et hypothèses de scale assumées |
| `tech-debt` | Inventorie la dette technique, la score sur impact, risque et effort, et produit un plan de remédiation entrelaçable avec les features, chaque item justifié par un impact métier et non seulement technique |
| `ticket-triage` | Catégorise, priorise P1 à P4 et route un ticket support entrant, avec les informations nécessaires à une prise en charge immédiate |
| `mockup` | Produit un mockup HTML autonome et présentable depuis un brief, une spec ou des références visuelles — un livrable de production visuelle, pas un prototype fonctionnel |

</details>

<details>
<summary><b>📊 Data et marché</b> — 3 skills</summary>

| Skill | Ce qu'il fait |
|---|---|
| `analyse-concurrentielle` | Construit un socle factuel sur le paysage concurrentiel — acteurs, forces, différenciation, positionnement |
| `metriques-saas` | Analyse les métriques clés d'un SaaS — CAC, LTV, NRR, churn — et produit un diagnostic factuel de la santé du modèle économique, formules et hypothèses à l'appui |
| `tableau-de-bord-kpi` | Définit et structure un tableau de bord KPI complet — métrique, unité, cible, fréquence, source — à partir d'objectifs ou d'un contexte métier |

</details>

<details>
<summary><b>🔗 Futurs workflows</b> — 2 skills</summary>

Encore des skills autonomes, à réécrire en enchaînements d'atomes ix-skills (`decision` → `deliver` ; `vendor-scorecard` → `decision`).

| Skill | Ce qu'il fait |
|---|---|
| `note-strategique` | Produit une note stratégique structurée et argumentée, qui commence par la conclusion et rend visibles les trade-offs, pour un destinataire décideur |
| `offer-comparison` | Compare des offres fournisseurs déjà normalisées sur une grille pondérée et conclut par une recommandation argumentée, en laissant visibles les scores fragiles et les critères non comparables |

</details>

## Structure du repo

| Chemin | Rôle |
|---|---|
| `skills/` | Source canonique : un `.md` par skill + surcharges `.mystaffy.json` |
| `dist/` | Racine du plugin, **commitée** : `.claude-plugin/plugin.json` + `skills/<id>/SKILL.md` générés par `build.py` |
| `.claude-plugin/marketplace.json` | Manifeste marketplace, pointe sur `./dist` |
| `build.py` | Packaging (agentskills, cowork, mystaffy, ix-memory, codex), copie du builder d'ix-skills |

```bash
python3 build.py --validate                 # valider sans écrire
python3 build.py --target agentskills       # régénérer dist/skills/
claude plugin validate dist
```

## Crédits

Plusieurs skills s'inspirent de sources publiques. Elles sont listées dans [THIRD_PARTY.md](THIRD_PARTY.md), avec ce qui en est repris et sous quelle licence.

## Licence

MIT, voir [LICENSE](LICENSE).
