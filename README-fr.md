<p align="center">
  <img src="docs/assets/banner.svg" alt="ix-recipes : recettes métier construites sur ix-skills" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence" src="https://img.shields.io/github/license/amiel-35/ix-recipes?color=7f9a96"></a>
  <img alt="Version du plugin" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Famiel-35%2Fix-recipes%2Fmain%2Fdist%2F.claude-plugin%2Fplugin.json&query=%24.version&label=plugin&color=7fc8bd">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-plugin-D97757">
  <img alt="Skills" src="https://img.shields.io/badge/skills-49-3d6b73">
  <a href="https://github.com/amiel-35/ix-skills"><img alt="requires ix-skills" src="https://img.shields.io/badge/requires-ix--skills-7fc8bd"></a>
  <img alt="Platforms" src="https://img.shields.io/badge/also-Codex%20%C2%B7%20GPT%20%C2%B7%20Gemini%20%C2%B7%20mystaffy-56707a">
</p>

<p align="center">
  <a href="#démarrage-rapide"><b>Démarrage rapide</b></a> ·
  <a href="#skills-disponibles"><b>Catalogue</b></a> ·
  <a href="#workflows"><b>Workflows</b></a> ·
  <a href="#contribuer"><b>Contribuer</b></a> ·
  <a href="README.md"><b>English</b></a>
</p>

---

<details>
<summary><b>Sommaire</b></summary>

- [À propos](#à-propos)
- [Démarrage rapide](#démarrage-rapide)
- [Convention de corpus — la sortie nulle](#convention-de-corpus--la-sortie-nulle)
- [Skills disponibles](#skills-disponibles)
- [Workflows](#workflows)
- [Installation](#installation)
- [Structure](#structure)
- [Packager](#packager)
- [Projets frères](#projets-frères)
- [Contribuer](#contribuer)
- [Crédits](#crédits)
- [Licence](#licence)

</details>

## À propos

Recettes métier construites sur [ix-skills](https://github.com/amiel-35/ix-skills) — portables sur Claude, GPT, Gemini, mystaffy.

51 skills en 9 familles, dont 2 workflows, un concepteur de workflows et la page de suivi. ix-skills fournit les ingrédients : des gestes cognitifs atomiques (critique, decision, explorer, fact-check…) qui s'appliquent à n'importe quel contenu. ix-recipes fournit les recettes :

- **des skills métier** — ils reposent sur une connaissance de domaine qui peut être fausse ou périmée (droit du travail, RGPD, pratiques RH, formules financières, méthodes produit), ou produisent un artefact qu'une profession définit (PRD, NDA, fiche de poste, TCO) ;
- **des workflows** — des enchaînements d'atomes ix-skills pour un travail récurrent, un concepteur pour en créer, et un exécuteur avec une page de suivi locale (voir [Workflows](#workflows)).

ix-recipes dépend d'ix-skills, jamais l'inverse : une recette peut renvoyer vers un atome, un atome ne renvoie jamais vers une recette. Les skills viennent d'ix-skills, déplacés le 2026-10-14 avec leur historique git.

---

## Démarrage rapide

Installer les deux plugins dans Claude Code — ix-recipes s'appuie sur les atomes d'ix-skills :

```bash
claude plugin marketplace add amiel-35/ix-recipes
claude plugin install ix-recipes@ix-recipes
claude plugin marketplace add amiel-35/ix-skills
claude plugin install ix-skills@ix-skills
```

Ou depuis le [catalogue amiel-35](https://github.com/amiel-35/plugins), une seule marketplace pour ix-skills, ix-recipes et ghost-council (installer chaque plugin depuis une seule marketplace) :

```bash
claude plugin marketplace add amiel-35/plugins
claude plugin install ix-recipes@amiel-35
claude plugin install ix-skills@amiel-35
```

Redémarrer Claude Code. Les skills sont namespacés (`fiche-poste` devient `/ix-recipes:fiche-poste`), et Claude les déclenche aussi depuis une demande ordinaire :

- *« Passe ce contrat fournisseur en revue avant que je signe, côté acheteur. »*
- *« Prépare la fiche de poste pour un product manager senior. »*
- *« Estime le TAM, SAM et SOM de ce marché. »*

Autres plateformes (Cowork, Codex CLI, Antigravity CLI, mystaffy, GPT, Gemini) : voir [Installation](#installation).

---

## Convention de corpus — la sortie nulle

Un skill qui n'a rien à produire ouvre sa réponse par « RAS — » suivi de la raison, et s'arrête. Le jeton est littéral et identique dans ix-skills et ix-recipes : c'est ce qui le rend greppable et testable.

---

## Skills disponibles

Cliquer sur une famille pour la déplier.

<details>
<summary><b>👥 RH & People</b> — 14 skills</summary>

Outils pour l'ensemble du cycle de vie des collaborateurs — recrutement, intégration, développement, évaluation, organisation et droit du travail. Le contexte droit du travail français est intégré là où c'est pertinent.

---

#### `fiche-poste` — Fiche de poste structurée

**Ce qu'il fait :** Produit une fiche de poste structurée et publiable depuis un brief RH ou un besoin de recrutement. Distingue requis et souhaitable, identifie les zones floues, et produit un livrable qui alimente le workflow de recrutement en aval.

**Quand l'utiliser :** Au lancement d'un processus de recrutement. Le livrable alimente `interview-loop-planner`.

---

#### `interview-loop-planner` — Conception du processus de recrutement complet

**Ce qu'il fait :** Conçoit la boucle d'entretien complète pour un recrutement — nombre de rounds, compétences par round, scorecard consolidé et planning. Produit des round_briefs qui alimentent directement `interview-guide-recruteur`.

**Quand l'utiliser :** Avant de démarrer les entretiens pour un recrutement significatif. Garantit que chaque round évalue des dimensions différentes.

> Pipeline : `fiche-poste` → `interview-loop-planner` → `interview-guide-recruteur` (un par round).

---

#### `interview-guide-recruteur` — Guide d'entretien côté recruteur

**Ce qu'il fait :** Produit un guide d'entretien complet pour recruteur ou manager — questions STAR structurées, annotations recruteur, mises en situation, grille de scoring pondérée 1–4, red flags gradués, et fiche de synthèse Go/No-go.

**Quand l'utiliser :** Pour un round d'entretien spécifique. S'utilise idéalement en aval de `interview-loop-planner` qui définit les rounds et compétences.

---

#### `onboarding-plan` — Plan d'intégration 30-60-90 jours

**Ce qu'il fait :** Construit un plan d'intégration structuré couvrant les 30, 60 et 90 premiers jours — objectifs, relations clés, livrables et critères de succès par phase.

**Quand l'utiliser :** Avant l'arrivée d'un nouveau collaborateur, pour donner au manager et au collaborateur une feuille de route commune.

---

#### `entretien-professionnel` — Entretien professionnel obligatoire

**Ce qu'il fait :** Prépare un entretien professionnel obligatoire (Code du Travail, art. L6315-1) — obligatoire tous les 2 ans pour tout salarié. Produit une trame, des questions et un gabarit de compte-rendu conformes aux exigences légales.

**Ce qu'il ne fait pas :** Pas la même chose qu'un entretien annuel d'évaluation. C'est un entretien de développement professionnel obligatoire légalement, pas une évaluation de performance.

**Quand l'utiliser :** Tous les 2 ans par salarié, ou après certains événements spécifiques (retour de congé maternité, longue maladie…) selon la loi française.

---

#### `analyse-entretien` — Les signaux d'un entretien déjà tenu

**Ce qu'il fait :** Lit une grille d'entretien remplie ou des notes brutes et en extrait les signaux : points forts, axes de développement, risques RH (démotivation, intention de départ, surcharge, conflit), besoins exprimés. Sépare ce qui est dit de ce qui est inféré, et lit les signaux au niveau du poste grâce à la référence de la famille de métier.

**Ce qu'il ne fait pas :** Ne prépare pas un entretien à venir (`performance-review-helper`, `entretien-professionnel`) et ne porte aucun jugement sur la personne.

**Quand l'utiliser :** Après un entretien annuel, pour en tirer une synthèse actionnable pour le manager ou les RH.

---

#### `performance-review-helper` — Préparation de l'entretien annuel

**Ce qu'il fait :** Prépare un entretien annuel avec bilan structuré de l'année écoulée et objectifs SMART pour la suivante. Supporte la préparation du manager et l'auto-évaluation du collaborateur.

**Ce qu'il ne fait pas :** Pas l'entretien professionnel obligatoire (`entretien-professionnel`). Celui-ci est sur la performance — résultats, objectifs, contexte de rémunération.

**Quand l'utiliser :** En amont des campagnes d'entretiens annuels.

---

#### `people-review` — Revue talent collective

**Ce qu'il fait :** Structure une revue de talents collective avec matrice de positionnement (performance × potentiel), plan de succession, évaluation des risques de rétention et départ, et actions prioritaires par profil.

**Quand l'utiliser :** Revues talents annuelles ou bi-annuelles, avant un changement organisationnel, ou lors de la préparation d'un workforce plan.

---

#### `plan-developpement-competences` — Plan de développement des compétences

**Ce qu'il fait :** Construit un plan de développement individuel ou collectif avec actions de formation, calendrier, indicateurs de succès et budget. Relie les lacunes identifiées à des parcours de développement concrets.

**Quand l'utiliser :** Après un entretien annuel, une people review, ou un diagnostic de compétences.

---

#### `grille-remuneration` — Grille de rémunération

**Ce qu'il fait :** Structure une grille de rémunération par famille de métier et niveau de séniorité — fourchettes salariales, critères de positionnement (équité interne, benchmarks marché) et règles de gouvernance (qui peut proposer quoi).

**Quand l'utiliser :** Lors de la montée en échelle d'une équipe, pour avoir des décisions de rémunération cohérentes et défendables sur les recrutements et collaborateurs existants.

---

#### `contrat-emploi` — Contrat de travail

**Ce qu'il fait :** Analyse ou rédige un contrat de travail, une offre d'embauche ou un avenant RH. Surface les clauses clés et les points d'attention. Produit un langage contractuel conforme.

**Ce qu'il ne fait pas :** Ne fournit pas de conseil juridique. Nécessite une validation par un avocat en droit du travail avant utilisation.

**Quand l'utiliser :** Rédaction d'un nouveau contrat, revue d'un contrat reçu, ou préparation d'un avenant (changement de poste, temps partiel…).

---

#### `lettre-cadrage-disciplinaire` — Lettre de cadrage disciplinaire

**Ce qu'il fait :** Rédige un projet de courrier de cadrage disciplinaire factuel et proportionnel — documentant les faits observés, leur impact et le changement de comportement attendu. Calibré à la gravité de la situation.

**Ce qu'il ne fait pas :** Ne produit pas une lettre de sanction formelle. Doit être validé par un avocat en droit du travail avant envoi.

**Quand l'utiliser :** Quand un entretien documenté est nécessaire avant une procédure disciplinaire formelle, ou pour créer une trace écrite d'un problème comportemental.

---

#### `offboarding-structure` — Plan de départ avec continuité

**Ce qu'il fait :** Structure un plan d'offboarding couvrant la passation de connaissances, la checklist administrative, le guide d'entretien de sortie et la cartographie des risques de continuité.

**Quand l'utiliser :** Dès qu'un collaborateur donne sa démission. Plus tôt on commence, meilleur est le transfert de connaissances.

---

#### `org-design-brief` — Brief de réorganisation

**Ce qu'il fait :** Formalise une cible organisationnelle avec diagnostic de l'état actuel, rationale du design, risques humains et séquencement — avant toute annonce ou mise en œuvre. Surface ce que la nouvelle structure résout, les nouveaux risques qu'elle crée, et comment phaser la transition.

**Quand l'utiliser :** Avant d'annoncer une réorganisation. Utile aussi comme pré-travail avant d'impliquer l'équipe de direction dans le design.

</details>

<details>
<summary><b>⚖️ Juridique & Contrats</b> — 6 skills</summary>

Outils pré-juridiques — tous nécessitent une validation professionnelle avant utilisation. Ils orientent les revues, font surface les risques et produisent des projets. Aucun ne remplace un juriste.

---

#### `legal-risk-flag` — Scan rapide des signaux d'alerte

**Ce qu'il fait :** Lit rapidement un document juridique ou contractuel et extrait les signaux de risque prioritaires avec des niveaux de sévérité gradués (haut / moyen / bas). Conçu pour la rapidité — une évaluation flash avant de décider si une revue approfondie est nécessaire.

**Ce qu'il ne fait pas :** Ne réalise pas une analyse complète. Signale, ne conclut pas. Ne remplace jamais un juriste.

**Quand l'utiliser :** Vous recevez un document et devez décider en quelques minutes s'il faut escalader à un juriste, ou sur quelles clauses concentrer la revue.


---

#### `cgv-checker` — Clauses déséquilibrées dans les CGV/CGU

**Ce qu'il fait :** Identifie les clauses déséquilibrées, inhabituelles ou sensibles dans des conditions générales de vente ou d'utilisation, selon la position de lecture (acheteur, utilisateur, abonné).

**Ce qu'il ne fait pas :** N'évalue pas la validité juridique complète des CGV. Ne remplace pas un conseil juridique.

**Quand l'utiliser :** Avant d'accepter les CGV d'un fournisseur ou d'une plateforme significatifs, ou lors de la rédaction de ses propres CGV.


---

#### `conformite-rgpd` — Checklist conformité RGPD

**Ce qu'il fait :** Produit une checklist de conformité RGPD depuis une spécification technique, une description produit ou un document de traitement de données. Distingue traitements observés, traitements inférés, et obligations à confirmer.

**Ce qu'il ne fait pas :** Ne remplace pas un DPO ou un professionnel juridique qualifié. Nécessite une validation experte avant utilisation opérationnelle.

**Quand l'utiliser :** Avant de lancer un produit ou une feature traitant des données personnelles. Un auto-diagnostic structuré en premier passage avant la revue DPO.

---

#### `compliance-checklist` — Checklist de conformité légale

**Ce qu'il fait :** Génère une checklist de conformité couvrant les obligations légales, contractuelles et réglementaires — RGPD, droit du travail, réglementation sectorielle — depuis un contexte projet ou un document.

**Ce qu'il ne fait pas :** Ne remplace pas un conseil juridique ou réglementaire professionnel. Nécessite toujours une validation experte avant utilisation opérationnelle.

**Quand l'utiliser :** Avant tout lancement produit, contractualisation, ou changement opérationnel à implications légales. Une pré-validation structurée pour orienter la conversation avec un juriste, pas la remplacer.

---

#### `nda-draft` — Projet de NDA adapté au contexte

**Ce qu'il fait :** Génère un projet d'accord de confidentialité adapté au contexte — type de parties, sujet des échanges, durée. Produit un document prêt pour revue juridique, pas pour signature immédiate.

**Ce qu'il ne fait pas :** Ne fournit pas de conseil juridique. Nécessite toujours une validation par un juriste avant signature.

**Quand l'utiliser :** Vous avez besoin d'un point de départ pour une négociation NDA et ne voulez pas partir d'un template générique.

---

#### `contrat-fournisseur` — Contrat fournisseur côté acheteur

**Ce qu'il fait :** Analyse **ou** rédige un contrat fournisseur ou prestataire depuis la perspective de l'acheteur. Surface les conditions déséquilibrées, les clauses à renégocier (SLA, responsabilité, résiliation, pénalités, exclusivité, renouvellement) et les risques contractuels. Peut aussi produire un premier projet quand aucun contrat n'existe encore.

**Ce qu'il ne fait pas :** Ne remplace pas un conseil juridique. Nécessite une validation professionnelle avant utilisation.

**Quand l'utiliser :** Avant de signer un contrat fournisseur, avant d'entrer en négociation, ou lors de la rédaction des conditions initiales d'une nouvelle relation fournisseur.

</details>

<details>
<summary><b>💶 Finance & Pricing</b> — 4 skills</summary>

Chiffrer, expliquer et défendre une décision d'argent — écarts budgétaires, business case, narratif financier, prix. Les hypothèses financières sont toujours explicites.

---

#### `budget-variance-analysis` — Diagnostic budget vs réel

**Ce qu'il fait :** Analyse les écarts entre budget et réalisé. Identifie les variances significatives, les qualifie par nature (volume, prix, mix, timing, opérationnel), et produit des hypothèses correctives et des points de vigilance.

**Ce qu'il ne fait pas :** N'invente pas de causes ou de chiffres. Ne prend pas de décisions de gestion — produit un diagnostic factuel.

**Quand l'utiliser :** Revue mensuelle ou trimestrielle, analyse P&L, ou quand il faut expliquer la performance à un board ou contrôleur.

---

#### `business-case-draft` — Structure de décision d'investissement

**Ce qu'il fait :** Structure une décision d'investissement avec coûts explicites, bénéfices attendus, scénarios de risque et hypothèses financières. Distingue coûts certains et coûts estimés. Marque clairement ce qui est hypothèse vs fait. Si les données sont trop fragiles, le dit et suggère `note-strategique` comme alternative allégée.

**Ce qu'il ne fait pas :** N'invente pas de chiffres.

**Quand l'utiliser :** Vous avez des chiffres et devez cadrer une décision achat/build/invest. Sans chiffres, utilisez `note-strategique`.

---

#### `financial-narrative` — Chiffres → histoire exécutive

**Ce qu'il fait :** Transforme des données financières brutes (P&L, KPIs, reporting) en narrative claire et message-first pour un board ou dirigeant. Commence par les messages clés, contextualise les chiffres, relie les variations à des facteurs explicatifs.

**Ce qu'il ne fait pas :** N'invente pas de chiffres ou de tendances. Ne reproduit pas les données brutes. Ne déforme pas les chiffres pour raconter une meilleure histoire.

**Quand l'utiliser :** Présentations board, updates investisseurs, revues trimestrielles — chaque fois que des chiffres doivent être communiqués à une audience qui a besoin du "so what" avant le détail.

---

#### `strategie-prix` — Stratégie de prix avec trade-offs

**Ce qu'il fait :** Formule une stratégie de pricing en liant valeur perçue, segmentation client et trade-offs business. Compare les modèles de prix (freemium, value-based, usage-based, tiered…) et produit une recommandation avec hypothèses explicites.

**Ce qu'il ne fait pas :** Ne produit pas une grille tarifaire. Ne recommande pas un prix sans énoncer les hypothèses qui le sous-tendent.

**Quand l'utiliser :** Lancement produit, repositionnement, ou pression concurrentielle sur les prix. Nécessite du contexte sur l'offre, les clients cibles et les benchmarks concurrentiels si disponibles.

</details>

<details>
<summary><b>🤝 Commercial & Achats</b> — 6 skills</summary>

Les deux côtés d'une consultation : répondre à un cahier des charges et rédiger une offre, ou piloter un appel d'offres, comparer les coûts et noter les fournisseurs.

---

#### `analyse-cdc` — Analyse d'un cahier des charges

**Ce qu'il fait :** Analyse un CDC reçu depuis la perspective du répondant. Surface les exigences explicites, implicites, les zones grises, les contradictions, et les questions bloquantes à poser avant tout engagement.

**Ce qu'il ne fait pas :** Ne résume pas le CDC — il le critique. Ne produit pas de plan de réponse.

**Quand l'utiliser :** Vous recevez un CDC, un appel d'offres ou un document d'exigences et devez comprendre ce qui est vraiment demandé avant de vous engager. Le livrable alimente une stratégie de réponse ou une réunion de clarification.

---

#### `offre-commerciale` — Contenu d'une offre client

**Ce qu'il fait :** Produit le contenu structuré d'une offre client — compréhension du contexte, solution proposée, argument de valeur, logique de prix et prochaines étapes. Focus sur le contenu et l'argument, pas la mise en forme finale.

**Ce qu'il ne fait pas :** Ne formate pas le document final (utilisez `deliver` pour ça). Ne négocie pas.

**Quand l'utiliser :** En réponse à une demande entrante, après un call de découverte, ou quand une proposition doit être structurée avant d'être mise en deck ou document.

---

#### `negotiation-brief` — Position structurée avant une négociation

**Ce qu'il fait :** Prépare une position de négociation complète — objectifs, non-négociables, points tradables, BATNA (meilleure alternative en cas d'absence d'accord) et logique de concession. Conçu pour la préparation, pas pour être remis à l'autre partie.

**Ce qu'il ne fait pas :** Pas un script de négociation. Pas un template pour l'autre partie.

**Quand l'utiliser :** Avant toute négociation achat à fort enjeu — fournisseur, prestataire, sous-traitant. Plus la position est claire en entrant, meilleur est le résultat.

---

#### `rfp-draft` — Appel d'offres

**Ce qu'il fait :** Génère un appel d'offres structuré — contexte, périmètre, exigences, critères d'évaluation, livrables attendus et calendrier.

**Quand l'utiliser :** Vous êtes l'acheteur et devez solliciter des offres structurées auprès de plusieurs fournisseurs. Le livrable alimente `offer-comparison` et `vendor-scorecard`.

---

#### `total-cost-analysis` — Coût total sur le cycle de vie (TCO)

**Ce qu'il fait :** Structure une analyse TCO couvrant coûts directs, coûts cachés (implémentation, formation, intégration, migration, sortie) et risques financiers sur un horizon donné. Distingue coûts confirmés, estimés et risques non quantifiés.

**Ce qu'il ne fait pas :** Ne regarde pas le prix affiché seul. N'invente pas de chiffres sans les marquer comme hypothèses.

**Quand l'utiliser :** Avant tout achat ou décision fournisseur significatif où le prix visible ne capture pas l'impact économique réel. Complément essentiel de `offer-comparison` et `vendor-scorecard`.

---

#### `vendor-scorecard` — Grille d'évaluation fournisseur réutilisable

**Ce qu'il fait :** Construit une grille de scoring fournisseur depuis un contexte achat — critères, pondérations, échelle de scoring, zones de commentaires qualitatifs. Produit l'**outil** de scoring, pas la décision.

**Ce qu'il ne fait pas :** Ne score pas les fournisseurs (c'est `offer-comparison`). N'invente pas de pondérations sans les justifier.

**Quand l'utiliser :** Avant le lancement d'une consultation, pour aligner les parties prenantes sur les critères d'évaluation. Réutilisable pour les consultations futures du même type.

</details>

<details>
<summary><b>🧭 Produit & UX</b> — 8 skills</summary>

Du besoin cadré au document que l'équipe produit attend — PRD, specs, user stories, personas, parcours, OKR, taille de marché. Le cadrage en amont (`cadrage`, `brief`, `analysis`) reste dans ix-skills.

---

#### `prd` — Product Requirements Document complet

**Ce qu'il fait :** Produit un PRD complet — contexte, formulation du problème, objectifs, exigences fonctionnelles et non-fonctionnelles, périmètre exclu, métriques de succès et questions ouvertes.

**Quand l'utiliser :** Vous avez besoin d'un document produit complet pour aligner l'équipe, communiquer avec l'ingénierie ou cadrer un investissement significatif.

---

#### `feature-spec` — Spécification fonctionnelle au niveau feature

**Ce qu'il fait :** Produit une spec fonctionnelle complète pour une feature — user stories, exigences MoSCoW, critères d'acceptation, cas limites et métriques de succès.

**Quand l'utiliser :** Une feature est validée et doit être spécifiée pour l'ingénierie. Plus granulaire qu'un PRD — opère au niveau d'une feature ou d'un epic.

---

#### `product-spec` — Spec actionnable allégée

**Ce qu'il fait :** Produit une spec actionnable depuis un brief ou un besoin cadré. Plus légère qu'un PRD, plus structurée qu'un brief — une spec rapide sur laquelle les équipes peuvent agir.

**Quand l'utiliser :** Vous avez besoin de quelque chose entre un brief et un PRD complet. Bien adapté aux petites features, MVPs ou contextes d'itération rapide.

> Hiérarchie : `brief` → `prd` (le quoi et le pourquoi) → `product-spec` / `feature-spec` (le comment, de plus en plus détaillé).

---

#### `reformulation-us` — Réécriture de user stories mal rédigées

**Ce qu'il fait :** Réécrit des user stories existantes vagues, centrées développeur ou non testables en user stories propres et testables avec structure correcte et critères d'acceptation explicites.

**Quand l'utiliser :** En backlog refinement, quand des stories sont tirées dans un sprint sans être prêtes, ou après une phase de découverte où les stories ont été rédigées informellement.

---

#### `persona` — Personas utilisateurs structurés

**Ce qu'il fait :** Produit des personas utilisateurs structurés depuis des données de recherche ou un brief produit — objectifs, frustrations, comportements, contexte et déclencheurs de décision. Conçu pour être actionnable, pas décoratif.

**Quand l'utiliser :** Au début d'une initiative produit, ou quand l'équipe a des hypothèses divergentes sur pour qui elle construit.

---

#### `journey-map` — Parcours utilisateur avec frictions et opportunités

**Ce qu'il fait :** Produit une carte de parcours utilisateur couvrant étapes, actions, émotions, points de friction et opportunités d'amélioration. Structurée depuis la perspective de l'utilisateur, pas des features du produit.

**Quand l'utiliser :** Avant de redesigner une expérience, d'identifier où investir en UX, ou d'aligner une équipe transverse sur la façon dont les utilisateurs vivent réellement le produit.

---

#### `okr` — Relire des lignes d'O/KR, ou faire émerger un matériau à discuter

**Ce qu'il fait :** Deux modes distincts. *Gabarit* : relit des lignes d'Objectif/Résultat clé déjà écrites, ligne par ligne — conformité à la formule (O = verbe d'action + quoi + impact recherché ; KR = verbe de mesure + quoi + de X à Y + échéance), tâche déguisée en KR, outcome ou output, baseline sourcée ou manquante, profil de calibrage (sandbagged / aspirationnel / stretch). *Matériau à discuter* : depuis un brief flou, produit des Objectifs candidats avec ce que chacun exclut, et des familles de résultats clés avec leurs pièges et leurs mécanismes de forçage.

**Ce qu'il ne fait pas :** Ne rend jamais un OKR fini tout seul — l'Objectif est choisi par la personne, les KR se discutent. N'invente jamais une baseline manquante : un X absent se déclare « à chiffrer », jamais remplacé par un chiffre plausible. En mode gabarit, ne réécrit pas les lignes de l'auteur.

**Quand l'utiliser :** Planning trimestriel, alignement stratégique, ou contre-check d'un OKR déjà rédigé. Le livrable alimente `tableau-de-bord-kpi` et `indicateurs`.

---

#### `tam-sam-som` — Sizing de marché avec méthode

**Ce qu'il fait :** Estime le TAM, SAM et SOM via des méthodes top-down et bottom-up avec hypothèses explicites. Surface la méthode, les chiffres et le degré d'incertitude. Web search obligatoire en mode standard/deep.

**Ce qu'il ne fait pas :** Ne produit pas de chiffres de mémoire sans le signaler. Un TAM/SAM/SOM sans hypothèses n'est pas un sizing, c'est une supposition.

**Quand l'utiliser :** Préparation d'un pitch, validation d'une opportunité de marché, ou construction d'un business case.

</details>

<details>
<summary><b>💻 Tech</b> — 4 skills</summary>

Concevoir et entretenir du logiciel — architecture, dette technique, triage support, maquette HTML.

---

#### `system-design` — Conception d'architecture technique

**Ce qu'il fait :** Conçoit un système ou une architecture technique — composants, flux de données, contrats API, stockage, décisions de scalabilité et trade-offs explicites. Documente ce qui a été décidé et pourquoi, y compris les options rejetées.

**Quand l'utiliser :** Avant de construire un nouveau système, lors d'une refonte d'architecture existante, ou quand une équipe a besoin d'un blueprint technique partagé.

---

#### `tech-debt` — Audit de dette technique avec plan de remédiation

**Ce qu'il fait :** Identifie, catégorise (structurelle / qualité de code / dépendances / documentation / couverture de tests) et priorise la dette technique avec un plan de remédiation réaliste. Distingue les quick wins du travail structurel.

**Quand l'utiliser :** Avant un sprint significatif, en planning ingénierie trimestriel, quand la vélocité a dégradé, ou avant une due diligence d'acquisition.


---

#### `ticket-triage` — Catégorisation et routing de tickets support

**Ce qu'il fait :** Catégorise un ticket support entrant, lui attribue une priorité P1–P4 basée sur l'impact et l'urgence, identifie les informations manquantes pour la prise en charge, et route vers l'équipe ou la file appropriée.

**Quand l'utiliser :** Traitement de tickets support ou bugs entrants, particulièrement dans les contextes à fort volume où une priorisation cohérente est nécessaire.

---

#### `mockup` — Mockup HTML autonome

**Ce qu'il fait :** Produit un mockup HTML autonome et présentable depuis un brief, une spec ou des références visuelles. Un livrable visuel pour l'alignement et le feedback.

**Ce qu'il ne fait pas :** Pas un prototype fonctionnel. Pas du code prêt pour la production.

**Quand l'utiliser :** Vous avez besoin de quelque chose de visuel pour présenter à des stakeholders, valider avec des utilisateurs ou communiquer un layout avant d'investir en design ou ingénierie.

</details>

<details>
<summary><b>📊 Data & Marché</b> — 3 skills</summary>

Lire un marché et un modèle économique avec des chiffres — concurrence, métriques SaaS, tableau de bord KPI.

---

#### `analyse-concurrentielle` — Paysage concurrentiel avec logique de différenciation

**Ce qu'il fait :** Structure une analyse concurrentielle autour de la logique de différenciation — pas une liste de concurrents. Identifie les forces en présence, compare les acteurs sur un framework commun, surface les zones de différenciation et les risques de positionnement. Web search obligatoire en mode standard/deep.

**Ce qu'il ne fait pas :** Ne produit pas une liste à puces de concurrents. Ne fait pas de recommandations stratégiques — utilisez `decision` pour ça.

**Quand l'utiliser :** Avant une entrée marché, une décision de positionnement ou une narrative fundraising. Se combine avec `note-strategique` ou `decision` en aval.

---

#### `metriques-saas` — Santé du modèle économique SaaS

**Ce qu'il fait :** Lit les métriques clés SaaS ensemble — CAC, LTV, NRR, churn, payback — et les interprète comme un système, pas en isolation. Surface les implications pour la santé du modèle, la soutenabilité de la croissance et les priorités de pilotage.

**Ce qu'il ne fait pas :** Ne produit pas de benchmarks de mémoire en mode standard/deep. Ne recommande pas d'actions — produit un diagnostic.

**Quand l'utiliser :** Préparation board, fundraising, revue opérationnelle, ou quand les tendances métriques sont contradictoires et qu'on veut comprendre ce qu'elles signifient ensemble.

---

#### `tableau-de-bord-kpi` — Structure d'un dashboard KPI

**Ce qu'il fait :** Définit et structure un dashboard KPI depuis des objectifs business, OKRs ou un contexte métier. Distingue KPIs directement mesurables, KPIs estimables (avec hypothèses), et KPIs problématiques (source fiable manquante). Refuse les métriques de vanité.

**Quand l'utiliser :** Après que les OKRs sont définis, ou quand un dispositif de pilotage doit être mis en place pour une équipe, un produit ou une BU.

</details>

<details>
<summary><b>⇢ Workflows</b> — 4 skills</summary>

Des recettes qui enchaînent plusieurs skills, chaque étape isolée dans son propre contexte, avec des pauses où l'humain valide, répond ou choisit. Format : [`docs/format-recette.md`](docs/format-recette.md).

---

#### `brief-client` — D'une demande floue à un brief exploitable

**Ce qu'il fait :** Enchaîne `cadrage` → `questioning` → réponses du client → [`explorer` → `decision`] → `brief`. Seule la première étape lit la demande brute (mail, notes, transcription) ; elle produit une fiche de contexte que tu valides et qui accompagne la suite. La recette s'arrête sur les questions à envoyer au client et reprend avec ses réponses.

**Ce qu'il ne fait pas :** Ne rédige pas l'offre (`offre-commerciale`) et ne lit pas un cahier des charges formel de consultation (`reponse-appel-offres`, `analyse-cdc`).

**Quand l'utiliser :** Une demande client trop floue pour être chiffrée ou produite telle quelle.

---

#### `reponse-appel-offres` — Répondre à une consultation de bout en bout

**Ce qu'il fait :** Enchaîne `analyse-cdc` → questions à l'acheteur → go / no-go → stratégie de réponse → `offre-commerciale` → contrôle de conformité (`controle-qualite`) → mise en forme (`deliver`). Le dossier de consultation n'est lu qu'à l'étape 1 ; le contrôle vérifie l'offre exigence par exigence contre ce que l'étape 1 a extrait. Tu tranches le go / no-go.

**Ce qu'il ne fait pas :** Ne remplace pas la décision de répondre ni la relecture finale ; ne gère pas le dépôt sur une plateforme.

**Quand l'utiliser :** Un appel d'offres ou un cahier des charges reçu qui appelle une réponse complète.

---

#### `concepteur-recette` — Concevoir une recette-workflow, ou la déconseiller

**Ce qu'il fait :** À partir d'un travail récurrent (idéalement avec un exemple réel), vérifie d'abord qu'un skill existant ou un enchaînement manuel ne suffit pas ; si une chaîne se justifie, propose le fichier de recette complet au format ix-recipes, sa justification et les questions à trancher avant de l'exécuter. Travaille uniquement sur le catalogue réel d'ix-skills et d'ix-recipes.

**Ce qu'il ne fait pas :** N'exécute pas la recette et n'écrit aucun fichier : il propose, tu enregistres. N'invente jamais de skill.

**Quand l'utiliser :** Tu refais souvent le même travail en plusieurs étapes et tu te demandes s'il mérite une recette.

---

#### `suivi-parcours` — Ouvrir la page de suivi

**Ce qu'il fait :** Démarre la page de suivi locale embarquée dans le plugin et t'en donne l'adresse : créer un dossier en collant la demande, relire et valider chaque étape, lire le livrable comme un document. Voir [Exécuter un workflow hors de la conversation](#exécuter-un-workflow-hors-de-la-conversation--la-page-de-suivi).

**Ce qu'il ne fait pas :** Ne joue aucune étape et ne lit aucun dossier lui-même. Pas depuis Cowork : la page tourne sur ton ordinateur.

**Quand l'utiliser :** Tu veux jouer une recette étape par étape, avec ses pauses, hors d'une conversation.

</details>

<details>
<summary><b>📝 Recommandation</b> — 2 skills</summary>

Des livrables de recommandation pour un décideur. Un temps prévus pour devenir des workflows, ils restent des skills : une chaîne n'y apporterait ni isolation, ni pause humaine, ni tiers à interroger (décision du 2026-10-15, après un banc d'essai du concepteur de recettes).

---

#### `note-strategique` — Note stratégique, conclusion en premier

**Ce qu'il fait :** Produit une note stratégique structurée et directement partageable — pour un décideur, un board ou un dirigeant. Commence par la conclusion, puis l'argument, les options, la recommandation avec trade-offs explicites. Deux pages maximum sans justification.

**Ce qu'il ne fait pas :** Ne commence pas par le contexte pour enterrer la recommandation à la fin. Si vous n'avez pas encore de position claire, lancez `decision` d'abord.

**Quand l'utiliser :** Vous avez une recommandation à faire et devez la packager pour un décideur. Le livrable est directement partageable.

---

#### `offer-comparison` — Comparaison pondérée avec recommandation

**Ce qu'il fait :** Compare des offres fournisseurs déjà reçues sur une grille pondérée normalisée et produit une recommandation argumentée. Rend la méthode de scoring et l'incertitude visibles — ne cache pas les trade-offs.

**Ce qu'il ne fait pas :** N'évalue pas des offres qu'on n'a pas encore reçues. Si les propositions sont trop différentes en scope, une normalisation manuelle est nécessaire d'abord.

**Quand l'utiliser :** Après réception de plusieurs devis pour un achat significatif.

> Pipeline : `vendor-scorecard` → `offer-comparison` → `total-cost-analysis` → `decision`.

</details>

---

## Workflows

Un workflow enchaîne des skills pour un travail récurrent. Format : [`docs/format-recette.md`](docs/format-recette.md). Chaque étape tourne isolée (un sous-agent sous Claude Code) et ne reçoit que ce dont elle a besoin ; seule la première lit la demande brute ; une fiche de contexte validée par l'humain la remplace ensuite ; les pauses font valider, répondre (client, acheteur) ou choisir. Une trace de chaque étape est écrite dans `./parcours/` quand c'est possible.

Disponibles : `brief-client`, `reponse-appel-offres` (voir le catalogue). Tous deux testés de bout en bout sur du matériau réel (une transcription de réunion client, un cahier des charges de consultation). `concepteur-recette` en conçoit de nouvelles.

### Exécuter un workflow hors de la conversation : la page de suivi

Dans une conversation, la recette s'orchestre elle-même par sous-agents. Pour une isolation réelle, une trace qu'on peut reprendre et aucune ligne de commande, utilisez la page de suivi : chaque étape tourne dans un **appel neuf** à un moteur (Claude Code par défaut ; Codex ou Antigravity en mode technique) qui ne reçoit que ses entrées, et la page s'arrête à chaque pause pour vous.

**Avec les plugins installés** (ix-recipes et ix-skills, dans Claude Code sur votre ordinateur), demandez à Claude : « ouvre la page de suivi ». Le skill `suivi-parcours` la lance depuis le plugin lui-même : il suffit de Python 3.9 ou plus et de la CLI Claude Code connectée. **Depuis un clone** de ce dépôt (ix-skills cloné à côté, ou installé en plugin) :

```bash
python3 scripts/interface.py
```

La page s'ouvre dans votre navigateur (en local seulement, protégée par une clé dans son adresse). Pas depuis Cowork : la page tourne sur votre ordinateur, hors de portée d'un environnement distant. On y trouve :

- **Nouveau dossier** : choisir une recette, coller la demande (mail du client, notes, cahier des charges) ou importer un fichier texte, puis « Créer et démarrer ».
- **Un dossier** : les étapes à gauche ; en haut, la seule chose attendue de vous (« Valider et continuer », « Envoyer les réponses et continuer », « Refaire l'étape »…) ; au centre, le résultat de chaque étape lu comme un document mis en forme, à copier, télécharger ou imprimer en PDF. La fiche de contexte, seule chose que les étapes suivantes savent de votre demande, se vérifie et se corrige champ par champ après la première étape.
- **Détails techniques** (interrupteur en haut) : moteur et modèle, coût par étape, champs transmis, sorties brutes, messages exacts reçus, journal.

Les dossiers sont rangés dans `~/Parcours` (`--parcours-dir` ou `PARCOURS_DIR` pour changer). Spécifications : [`docs/interface.md`](docs/interface.md), [`docs/executeur.md`](docs/executeur.md). Mesuré : une réponse complète à un appel d'offres (7 étapes, Claude) a coûté de 0,86 $ à 1,53 $ selon les reprises.

Le même exécuteur s'utilise en ligne de commande, pour des scripts :

```bash
python3 scripts/parcours.py new reponse-appel-offres --input cdc.md --slug ao --parcours-dir ~/Parcours
python3 scripts/parcours.py next ao --parcours-dir ~/Parcours        # jusqu'à la prochaine pause
```

À venir :

```
choix fournisseur     vendor-scorecard → pause pondérations → rfp-draft → offres reçues → total-cost-analysis → offer-comparison
relecture avant envoi critique → fact-check → correction → fact-check → deliver → controle-qualite
```

Enchaînements déjà praticables à la main :

```
research → analyse-concurrentielle → decision
brief    → prd → feature-spec
fiche-poste → interview-loop-planner → interview-guide-recruteur
```

---

## Installation

### Claude Code (plugin — recommandé)

Le repo est une marketplace de plugins Claude Code (`.claude-plugin/marketplace.json` pointe sur la racine de plugin `dist/`) :

```bash
claude plugin marketplace add amiel-35/ix-recipes
claude plugin install ix-recipes@ix-recipes
claude plugin marketplace add amiel-35/ix-skills     # requis : les atomes sur lesquels reposent les recettes
claude plugin install ix-skills@ix-skills
```

Pour récupérer les mises à jour ensuite :

```bash
claude plugin marketplace update ix-recipes
claude plugin update ix-recipes
```

Puis redémarrer Claude Code. Les releases sont résolues par la version du manifeste (`dist/.claude-plugin/plugin.json`), voir `CHANGELOG.md`. Dans l'app desktop Claude Code, les mêmes étapes passent par la commande `/plugin`.

**Alternative — le catalogue `amiel-35`.** [amiel-35/plugins](https://github.com/amiel-35/plugins) est une marketplace qui référence ix-skills, ix-recipes et ghost-council, chacun pointant sur le dossier `dist/` de son propre dépôt :

```bash
claude plugin marketplace add amiel-35/plugins
claude plugin install ix-recipes@amiel-35
claude plugin install ix-skills@amiel-35
```

Installer un plugin depuis une seule marketplace (`ix-recipes@ix-recipes` ou `ix-recipes@amiel-35`, pas les deux), sinon il apparaît en double ; les mises à jour passent alors par `claude plugin marketplace update amiel-35`. Testé dans Claude Code ; pas encore testé avec « Ajouter depuis un dépôt » de Cowork : pour Cowork, garder la marketplace propre à chaque dépôt, ci-dessous.

Les 11 recettes RH qui déclarent des références par famille de métier (`partials/metier_*.md`, voir [Structure](#structure) ; tous les skills RH sauf `contrat-emploi`, `lettre-cadrage-disciplinaire` et `org-design-brief`) reçoivent leur dossier `references/` avec le plugin : rien de plus à faire.

> Transition : jusqu'à ix-skills 4.0.0, ces skills étaient aussi livrés dans ix-skills. Mettre ix-skills à jour pour ne pas les voir en double. ix-recipes 2.0.0 retire `code-review` et `contract-review` (voir `CHANGELOG.md`).

**Fallback manuel** : symlinker ou copier `dist/skills` dans `~/.claude/skills/` — pas `skills/`, dont le frontmatter canonique n'est pas un `SKILL.md` valide.

### Claude Cowork / claude.ai

**Option A — plugin** : **« Ajouter depuis un dépôt »** avec `amiel-35/ix-recipes`, puis à nouveau avec `amiel-35/ix-skills` (les recettes s'appuient sur ses atomes). Les références sont incluses.

**Option B — un seul skill** : les dossiers `dist/skills/<id>/` sont des Agent Skills valides, à uploader tels quels dans **Cowork → Customize** (ou l'éditeur ChatGPT Skills). Pour les 11 skills RH qui déclarent des références (`fiche-poste`, `entretien-professionnel`, `analyse-entretien`…), uploader le dossier entier, sous-dossier `references/` compris ; sans lui, le skill demande le référentiel de compétences de l'organisation. Un skill uploadé seul n'embarque pas les atomes ix-skills.

### Codex CLI

Codex lit la même marketplace que Claude Code (testé avec codex-cli 0.155.1). Les recettes s'appuient sur les atomes d'ix-skills : ajouter les deux.

```bash
codex plugin marketplace add amiel-35/ix-recipes
codex plugin add ix-recipes@ix-recipes
codex plugin marketplace add amiel-35/ix-skills
codex plugin add ix-skills@ix-skills
```

Les plugins atterrissent dans `~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/skills/<id>/`, avec les dossiers `references/`. Pour mettre à jour, lancer `codex plugin marketplace upgrade` puis ré-ajouter le plugin au besoin (voir `codex plugin --help`). Pour retirer :

```bash
codex plugin remove ix-recipes@ix-recipes
codex plugin marketplace remove ix-recipes
```

**Nommer le skill dans la demande** (« utilise le skill fiche-poste du plugin ix-recipes pour… »). Codex lit alors `SKILL.md` puis seulement le fichier de référence utile. Sur une demande simple qui ne nomme pas le skill, Codex ne l'a pas utilisé lors de nos essais.

Le catalogue `amiel-35/plugins` utilise des sources `git-subdir` et n'est **pas testé avec Codex** : pour Codex, passer par les marketplaces des repos ci-dessus.

**Installateur historique** (copie dans `~/.codex/skills/`, non retesté sur Codex 0.155) :

```bash
git clone https://github.com/amiel-35/ix-recipes /tmp/ix-recipes
cd /tmp/ix-recipes
pip install -r requirements.txt
bash scripts/install-codex.sh                 # tous les skills
bash scripts/install-codex.sh fiche-poste     # un seul skill
bash scripts/install-codex.sh --dry-run       # aperçu sans installer
```

Les skills sont installés dans `~/.codex/skills/<id>/SKILL.md`, avec leur dossier `references/` quand ils en ont un. Redémarrer Codex pour activer. Installer aussi ix-skills, avec le `scripts/install-codex.sh` de son propre dépôt.

### Antigravity CLI (agy, Gemini)

`agy` importe un dossier de plugin au format Claude (testé avec agy 1.3.3). Importer ix-recipes et sa dépendance ix-skills :

```bash
git clone https://github.com/amiel-35/ix-recipes
git clone https://github.com/amiel-35/ix-skills
agy plugin import ix-recipes/dist
agy plugin import ix-skills/dist
```

Les skills sont importés avec leurs `references/` dans `~/.gemini/config/plugins/<plugin>/`. Utiliser `import` : `agy plugin validate` et `agy plugin install` attendent un `plugin.json` à la racine et n'acceptent pas ce format. Pour importer à la place les plugins déjà installés dans Claude Code (tous) : `agy plugin import claude`. Pour retirer : `agy plugin uninstall ix-recipes`.

Comme pour Codex, **nommer le skill dans la demande** : agy lit alors `SKILL.md` puis seulement le fichier de référence utile.

### mystaffy

```bash
python3 build.py --target mystaffy
python3 build.py --target ix-memory   # format ix-memory natif
```

Ces cibles ne contiennent que `skill.md` et `manifest.json`, pas les dossiers `references/` : les skills RH demandent alors le référentiel de compétences de l'organisation.

### GPT / Gemini / autre LLM (interfaces de chat)

Pour les interfaces de chat simples, sans CLI : copier-coller le contenu de `skills/<id>.md` comme system prompt. Le frontmatter YAML est ignoré sans effet de bord. Pour un skill qui déclare `references` dans son frontmatter (les skills RH), coller aussi le `partials/metier_<famille>.md` correspondant (`metier_tech`, `metier_rh`…), sinon le skill demandera le référentiel de compétences de l'organisation.

---

## Structure

```
ix-recipes/
├── skills/                 ← source canonique (un .md + .mystaffy.json par skill)
├── partials/               ← références par famille de métier (metier_*.md), copiées dans references/ des skills qui les déclarent
├── scripts/
│   └── install-codex.sh    ← installateur Codex CLI
├── dist/                   ← racine du plugin, commité
│   ├── .claude-plugin/plugin.json   ← manifeste du plugin (à la main, bump à chaque release)
│   └── skills/<id>/                 ← artefacts Agent Skills, générés par build.py
│       ├── SKILL.md
│       └── references/              ← seulement pour les skills qui déclarent des références
├── .claude-plugin/
│   └── marketplace.json    ← manifeste marketplace, pointe sur ./dist
├── mystaffy-dist/, codex-dist/  ← artefacts mystaffy / Codex (ignorés par git)
├── build.py                ← packager multi-cibles, copie de celui d'ix-skills
├── requirements.txt        ← jsonschema, pyyaml
├── docs/                   ← bannière et notes de travail
├── LICENSE                 ← MIT
├── LICENSES/               ← copies des licences des sources tierces (Apache-2.0)
├── CHANGELOG.md            ← releases, par date
├── THIRD_PARTY.md          ← sources tierces et licences
└── CLAUDE.md               ← guide de contribution
```

---

## Packager

```bash
pip install -r requirements.txt         # jsonschema, pyyaml
python3 build.py --validate
python3 build.py
python3 build.py fiche-poste
python3 build.py --target agentskills   # dist/skills/<id>/SKILL.md — à commiter
python3 build.py --target cowork        # valide dist/.claude-plugin/plugin.json
python3 build.py --target mystaffy --domain rh
python3 build.py --target codex
claude plugin validate dist
```

---

## Projets frères

- [**ix-skills**](https://github.com/amiel-35/ix-skills) — les ingrédients : gestes cognitifs atomiques (critique, decision, explorer, fact-check…) et postures de conseil (`dixieme-homme`, `red-team`, `contrarian`…). Prérequis d'ix-recipes.
- [**ghost-council**](https://github.com/amiel-35/ghost-council) — des méthodes de raisonnement de philosophes encodées comme skills (Popper, Kant, Pascal, Wittgenstein…), et `/council`, qui fait délibérer plusieurs angles indépendants sur une décision.
- [**plugins**](https://github.com/amiel-35/plugins) — la marketplace `amiel-35`, qui référence ix-skills, ix-recipes et ghost-council au même endroit.

---

## Contribuer

Fork, modifie, PR. Lire [`CLAUDE.md`](CLAUDE.md) pour le format canonique d'un skill, la règle de dépendance avec ix-skills et les checklists, et [`CHANGELOG.md`](CHANGELOG.md) pour les versions.

Un skill qui applique un geste de raisonnement à n'importe quel contenu appartient à ix-skills ; un skill qui demande un savoir de métier appartient ici.

---

## Crédits

Plusieurs skills s'inspirent de sources publiques. Chaque source reprise est listée dans [`THIRD_PARTY.md`](THIRD_PARTY.md), avec ce qui en est repris et sous quelle licence.

---

## Licence

MIT, voir [LICENSE](LICENSE).
