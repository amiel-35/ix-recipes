# Sources tierces

Ce que les skills d'ix-recipes doivent à des projets publics : la source, sa licence, ce qui en est repris. Établi le 2026-10-14 en comparant chaque skill à sa première version (projet ix-memory, mars 2026) et aux dépôts candidats.

Règle pour la suite : avant de reprendre quoi que ce soit d'un autre dépôt, vérifier sa licence et ajouter l'entrée ici dans le même commit.

---

## anthropics/knowledge-work-plugins (Anthropic)

- **Source :** https://github.com/anthropics/knowledge-work-plugins, état du 2026-03-13 (commit `7b2ea8ea53095665fc1dae68602bf64a57faffab`) ; état du 2026-10-15 (commit `33eeda1`) pour `nda-draft`. Vérifié le 2026-10-16 : les quatre fichiers sources repris en mars n'ont pas changé depuis `7b2ea8ea`.
- **Licence :** Apache License 2.0, copie dans [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt). Le dépôt n'a pas de fichier NOTICE (vérifié le 2026-10-16 ; depuis avril 2026, le fichier LICENSE racine porte une dizaine de lignes parasites après le texte Apache, sans effet sur les termes).
- **Skills adaptés :**

  | Skill ix-recipes | Fichier source | Ce qui en est repris |
  |---|---|---|
  | `feature-spec` | `product-management/skills/write-spec/SKILL.md` | MoSCoW avec « si tout est Must, rien n'est Must », critères Given/When/Then, indicateurs avancés et retardés, questions bloquantes et non bloquantes |
  | `system-design` | `engineering/skills/system-design/SKILL.md` | Les cinq étapes et leur ordre : exigences, conception d'ensemble, approfondissement, montée en charge et fiabilité, compromis |
  | `tech-debt` | `engineering/skills/tech-debt/SKILL.md` | Les trois axes notés de 1 à 5 et la formule Priorité = (Impact + Risque) × (6 − Effort) |
  | `ticket-triage` | `customer-support/skills/ticket-triage/SKILL.md` | Les définitions P1 à P4 ; « la cause racine détermine la catégorie » ; dans le doute, monter en priorité |
  | `nda-draft` (depuis 1.2.0) | `legal/skills/triage-nda/SKILL.md`, état du 2026-10-15 (commit `33eeda1e8fd856455b05479d13a0f85b5f803744`) | Les positions par défaut d'un NDA : durée des discussions et survie des obligations, degré de soin, confirmation écrite des divulgations orales, clause de « residuals » à refuser, repli de la non-sollicitation à 12 mois. Repris pour la rédaction et non pour le tri, et adapté au droit français (clause pénale admise, art. 1210 C. civ., clause attributive de juridiction) |

  Reprises du 2026-10-16, réécriture des skills métier (commit `33eeda1`, les fichiers sont lus en entier ; chaque skill porte une mention en fin de corps) :

  | Skill ix-recipes | Fichier source | Ce qui en est repris |
  |---|---|---|
  | `feature-spec` (complété en 1.2.0) | `product-management/skills/write-spec/SKILL.md` | En plus de la reprise de mars : test du P0 et « assurance d'architecture », erreurs de user stories, conseils de critères d'acceptation, règles de cible, non-objectifs avec raison, dérive du périmètre |
  | `prd` (1.2.0) | `product-management/skills/write-spec/SKILL.md` | Test du P0, P2 en assurance d'architecture, non-objectifs avec raison, règles de cible, dérive du périmètre |
  | `reformulation-us` (1.2.0) | `product-management/skills/write-spec/SKILL.md` | Erreurs de user stories (grille de diagnostic), conseils de critères d'acceptation |
  | `product-spec` (1.2.0) | `design/skills/design-handoff/SKILL.md` | Liste des états et des cas limites d'une vue |
  | `mockup` (1.2.0) | `design/skills/design-handoff/SKILL.md` | Les états à montrer |
  | `persona` (1.2.0) | `product-management/skills/synthesize-research/SKILL.md` | Comportement plutôt que démographie, variables qui distinguent les groupes, effectif par motif |
  | `okr` (2.2.0) | `product-management/skills/metrics-review/SKILL.md` | Test de trajectoire, norme d'atteinte d'environ 0,7, 2 à 4 KR par objectif |
  | `tableau-de-bord-kpi` (1.2.0) | `product-management/skills/metrics-review/SKILL.md` | Mesure de départ avant cible, cible engagée et cible haute, principes et erreurs de tableau de bord, alertes |
  | `analyse-concurrentielle` (1.2.0) | `product-management/skills/competitive-brief/SKILL.md`, `marketing/skills/competitive-brief/SKILL.md` | Niveaux de concurrents, axes de carte tirés des critères d'achat, échelle de notation, comparaison des prix |
  | `budget-variance-analysis` (1.2.0) | `finance/skills/variance-analysis/SKILL.md` | Décomposition prix / volume en deux termes avec exemple, seuils de matérialité et ordre d'investigation, gabarit et défauts de commentaire, pont avec contrôle de bouclage. Les formules « three-way », effectifs / salaires et rate / mix ne sont **pas** reprises : elles ne bouclent pas |
  | `financial-narrative` (1.2.0) | `finance/skills/variance-analysis/SKILL.md`, `finance/skills/financial-statements/SKILL.md` | Gabarit et défauts de commentaire, choix de la comparaison (budget, prévision, N-1), écarts de taux en points |
  | `fiche-poste` (1.4.0) | `small-business/skills/job-post-builder/SKILL.md` et `reference/job-post-structure.md` | Exigence vérifiable sur CV et test du « requis », rémunération chiffrée ou rien, longueur cible |
  | `interview-guide-recruteur` (1.4.0) | `small-business/skills/job-post-builder/reference/interview-guide-structure.md` | Ancrages comportementaux par niveau (ramenés à une échelle 1-4), conseils d'écriture des questions |
  | `contrat-emploi` (1.2.0) | `human-resources/skills/draft-offer/SKILL.md` | Tableau de rémunération de l'offre (adapté au droit français) |
  | `onboarding-plan` (1.3.0) | `human-resources/skills/onboarding/SKILL.md` | Liste avant J1, programme J1 et semaine 1, tableau des contacts, binôme distinct du manager |
  | `org-design-brief` (1.2.0) | `human-resources/skills/org-planning/SKILL.md` | Repères d'encadrement (5 à 8 subordonnés directs, alerte sous 3 ou au-delà de 12, équipes de 5 à 9) |
  | `performance-review-helper` (1.4.0) | `human-resources/skills/performance-review/SKILL.md` | Trame d'auto-évaluation, adaptée |
  | `people-review` (1.3.0) | `human-resources/skills/performance-review/SKILL.md` | Tableau de calibrage, sans actions de rémunération ; la distribution cible n'est qu'un repère indicatif, jamais un quota (illicite en France) |
  | `cgv-checker` (1.3.0) | `legal/skills/review-contract/SKILL.md` | Catégories de clauses, seuils vert / orange / rouge, format de constat avec repli, adaptés au droit français |
  | `contrat-fournisseur` (1.3.0) | `legal/skills/review-contract/SKILL.md` | Points de revue par clause côté acheteur, seuils, redline avec repli, trois niveaux de priorité et règle d'échange |
  | `negotiation-brief` (1.2.0) | `legal/skills/review-contract/SKILL.md` | Trois niveaux de priorité et règle d'échange des concessions |
  | `legal-risk-flag` (1.3.0) | `legal/skills/legal-risk-assessment/SKILL.md` | Ancres de gravité (ramenées de 5 à 3 niveaux), déclencheurs d'escalade à l'avocat |
  | `compliance-checklist` (1.2.0) | `legal/skills/compliance-check/SKILL.md` | Gabarit de verdict et validations nécessaires |
  | `analyse-cdc` (1.4.0) | `small-business/skills/grant-rfp-writer/reference/go_no_go.md` | Exigence obligatoire ou souhaitée (devenue éliminatoire / notée), compte à rebours depuis la date limite |
  | `offre-commerciale` (1.2.0) | `small-business/skills/proposal-builder/reference/` (`proposal_structure.md`, `pricing_method.md`, `gotchas.md`), `small-business/skills/grant-rfp-writer/reference/drafting.md` | Section « non compris », hypothèse avec sa conséquence, lignes de prix de décision, options, note interne séparée ; délais de paiement remplacés par le droit français |
  | `rfp-draft` (1.2.0) | `small-business/skills/job-post-builder/reference/job-post-structure.md` | Le test « rejetterait-on un excellent candidat sans cela ? », appliqué à l'exigence éliminatoire |
  | `total-cost-analysis` (1.2.0) | `operations/skills/vendor-review/SKILL.md` | Catégories de coûts (reprise légère) |
  | `system-design` (complété en 1.2.0) | `engineering/skills/architecture/SKILL.md` | Conséquences d'une décision : plus facile, plus difficile, à revoir quand |
  | `tech-debt` (complété en 1.3.0) | `engineering/skills/tech-debt/SKILL.md` | Tableau catégorie → risque, questions des trois échelles |
  | `ticket-triage` (complété en 1.2.0) | `customer-support/skills/ticket-triage/SKILL.md` | Délais par priorité (défauts à remplacer), déclencheurs de montée, conseils de catégorie, routage, réponses types Bug et Sécurité |

- **Modifications :** chaque skill a été condensé (de 1 700–2 000 mots à environ 300 pour `feature-spec` et `ticket-triage`), réécrit dans le gabarit ix (rôle, règle absolue, entrées, méthode, contraintes, format de sortie, définition de fini), rédigé en français puis traduit en anglais, débarrassé des connecteurs propres à Claude, et complété de règles maison (sortie nulle « RAS », séparation faits / hypothèses). Chaque fichier modifié porte une mention en fin de corps.
- `code-review` et `contract-review`, issus du même dépôt, ont été retirés d'ix-recipes en 2.0.0 : la source fait mieux, et Claude Code a déjà un `/code-review` intégré.

## wshobson/agents (Seth Hobson)

- **Source :** https://github.com/wshobson/agents
- **Licence :** MIT, « Copyright (c) 2024 Seth Hobson »
- **Skills inspirés :** `metriques-saas` (`plugins/startup-business-analyst/skills/startup-metrics-framework`), `analyse-concurrentielle` (`…/competitive-landscape`), `tam-sam-som` (`…/market-sizing-analysis`), `contrat-emploi` (`plugins/hr-legal-compliance/skills/employment-contract-templates`), `tableau-de-bord-kpi` (`plugins/business-analytics/skills/kpi-dashboard-design`)
- **Ce qui en est repris :** le périmètre et l'idée de chaque skill, importés en mars 2026 via l'annuaire agentskill.sh. Aucun passage du texte d'origine ne subsiste dans les versions actuelles ; crédit donné par prudence.

## davila7/claude-code-templates (Daniel Ávila)

- **Source :** https://github.com/davila7/claude-code-templates, `cli-tool/components/skills/business-marketing/pricing-strategy`
- **Licence :** MIT, « Copyright (c) 2025 Daniel (San) Ávila »
- **Skill inspiré :** `strategie-prix` (modèles freemium, paliers, Van Westendorp). Aucun passage du texte d'origine ne subsiste ; le dépôt est un agrégateur et l'auteur d'origine du contenu n'est pas établi.

---

Les méthodes publiques citées dans les skills (MoSCoW, RICE, Given/When/Then, OKR, TAM/SAM/SOM, Van Westendorp…) ne sont pas des sources tierces et ne sont pas listées ici.

## Polices du thème Inflexion (`themes/inflexion/`)

Le thème par défaut de la page de suivi embarque trois familles de polices, non modifiées, chacune sous SIL Open Font License 1.1 (texte de la licence à côté des fichiers : `OFL-*.txt`) :

- **Archivo** — Omnibus-Type, via google/fonts.
- **Source Sans 3** — Adobe, via google/fonts.
- **IBM Plex Mono** (Regular) — IBM, via google/fonts.
