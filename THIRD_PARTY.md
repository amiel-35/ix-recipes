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
