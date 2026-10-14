# Cadrage — la suite d'ix-recipes

État au 2026-10-14, après la séparation ix-skills / ix-recipes, la récupération des références métier et la revue des 46 recettes.

## 1. Intention

Faire d'ix-recipes un vrai livre de recettes : des skills métier qui marchent seuls dans Claude, et des enchaînements d'atomes ix-skills qu'on peut suivre pas à pas — à la main dans une conversation, par script, ou depuis une petite interface — sans reconstruire le moteur lourd d'ix-memory (base, runs, composer, catalogue).

Le problème de fond à ne pas reproduire : dans ix-memory, chaque étape relisait le brief de départ, la livraison défaisait la décision et la décision corrigeait au lieu de trancher. `handoff.fields` devait l'empêcher et n'a jamais été appliqué.

## 2. Acquis (contraintes)

- **ix-recipes dépend d'ix-skills, jamais l'inverse.** Ids uniques entre les deux repos.
- **Le skill unique reste la règle.** Revue des 46 recettes : 39 restent des skills, 5 deviennent des workflows, 2 sont à fusionner. L'ancien composer avait choisi « skill unique » 14 fois sur 14.
- **Les annexes se lisent à la demande** (`partials/` → `references/`), éprouvé sur les recettes RH et sur `prioritize`.
- **Règles de chaîne héritées d'ix-memory** : chaîne la plus courte défendable, linéaire, une mission locale par étape, brief brut à l'étape 1 seulement, une étape ne refait pas le travail d'une autre, l'orchestrateur ne tranche jamais sur le fond, pas de requalification d'un champ reçu sans le signaler.
- **Clés JSON en anglais** (décision du 2026-10-06).
- **Repos publics, sources créditées** (`THIRD_PARTY.md`).

## 3. Chantiers

| # | Chantier | Dépend de | Taille |
|---|---|---|---|
| A | **Format de recette** : spec du SKILL.md de workflow | — | moyenne |
| B | **Prototype `brief-client`** : `cadrage` → `questioning` → réponses du client → [`explorer` → `decision`] → `brief`, plus un `mode: handoff` sur `cadrage`, `questioning`, `brief` | A | moyenne |
| C | **Sortie machine (JSON)** : schéma par skill (`skills/<id>.schema.json`), `output: json` remplace le Markdown, ids conservés, champ `nature` observé / déduit | A pour les clés de handoff | grande |
| D | **État d'un parcours** : un fichier JSON qui décrit les étapes, leur statut, leurs sorties, les questions en attente — indépendant de l'interface | C | moyenne |
| E | **Exécution et suivi** : script (`claude -p` par étape, ne transmet que les champs de handoff), puis interface | D | grande |
| F | **Les 5 workflows** : note-strategique, offer-comparison, business-case-draft, strategie-prix (à enrichir, sinon fusion), persona | A, B | moyenne |
| G | **Parcours métier documentés** : recrutement, achats (`vendor-scorecard` → `rfp-draft` → offres → `total-cost-analysis` → `decision`), réponse à appel d'offres, produit | A | petite par parcours |
| H | **Fusions** : `feature-spec` → `product-spec` ; `contrat-fournisseur` → `cgv-checker` (à discuter) | — | petite |
| I | **Recettes minces** : 13 signalées ; `feature-spec` et `ticket-triage` peuvent retrouver le savoir de leur source Anthropic | — | moyenne |

## 3bis. Décisions du 2026-10-14

1. **Isolation des étapes : oui.** Chaque étape tourne dans un contexte neuf (sous-agent sous Claude Code, appel `-p` neuf dans l'exécuteur) et ne reçoit que sa mission locale, la fiche de contexte et les champs de handoff de l'amont. Les consignes ne sont qu'un repli là où rien ne permet d'isoler. Raison : dans ix-memory, ce qui empêchait la dérive des étapes profondes était de ne *pas* leur donner le brief (note du 2026-04-28), jamais une consigne.
2. **Brief brut : jamais après l'étape 1.** L'étape 1 produit en plus une **fiche de contexte** — entités, contraintes, objectifs, destinataire, format, échéances, sans demande d'action — validée par l'humain à la première pause, puis transmise à toutes les étapes ; c'est elle qui donne destinataire et format à la dernière. Reprend l'idée `entities_constraints_objectives_only` d'ix-memory (jamais construite), sans planificateur LLM.
3. **Utilisateurs : d'abord la personne qui utilise les skills** (Amiel ou un autre), avec une interface locale installable depuis le repo, sans chemin propre à une machine ; **partage dans un second temps** (export, ou page claude.ai en lecture seule).
4. **Deux parcours, dans cet ordre.** `brief-client` (`cadrage` → `questioning` → réponses du client → `brief`, 4 étapes, 1 pause) sert à valider le format : c'est le plus petit cas qui teste isolation, fiche de contexte, pause et reprise. Puis **réponse à appel d'offres**, premier parcours outillé (état, exécuteur, interface), qui réutilise `brief-client` en sous-parcours (étapes 3–4 du §3ter). Matériau de test : un vrai brief client pour le premier, un vrai cahier des charges déjà utilisé pour les tests de skills pour le second.
5. **Fusion `contrat-fournisseur` / `cgv-checker`** : discussion à part.

## 3ter. Esquisse du parcours « réponse à appel d'offres »

| # | Étape | Skill | Reçoit | Transmet | Pause |
|---|---|---|---|---|---|
| 1 | Lire le cahier des charges | `analyse-cdc` (recette) | le DCE / CDC brut | exigences (explicites, implicites), critères d'évaluation, zones floues, questions bloquantes **+ fiche de contexte** | **oui** : valider la fiche de contexte et la lecture |
| 2 | Go / no-go | `decision` (atome) | exigences, critères, fiche de contexte | décision motivée, conditions | **oui** : l'humain tranche |
| 3 | Questions à l'acheteur | `questioning` (atome) | zones floues, questions bloquantes | questions à envoyer, par ordre d'importance | **oui** : envoi, puis réponses de l'acheteur |
| 4 | Stratégie de réponse | `brief` (atome) | exigences, critères, réponses de l'acheteur, fiche de contexte | brief de réponse : angle, preuves à fournir, risques | non |
| 5 | Rédiger l'offre | `offre-commerciale` (recette) | brief de réponse, fiche de contexte | contenu de l'offre | non |
| 6 | Contrôle de conformité | `controle-qualite` (atome) | l'offre + exigences et critères de l'étape 1 comme référentiel | verdict par exigence | **oui** : corrections |
| 7 | Mise en forme | `deliver` (atome) | offre corrigée, destinataire et format de la fiche de contexte | livrable final | non |

À vérifier en concevant : la granularité (le go/no-go peut-il précéder les questions ?), ce que l'étape 6 doit recevoir pour contrôler sans relire tout le DCE, et les champs exacts de la fiche de contexte.

## 4. Options pour le suivi des parcours (chantier E)

| | Script local | Interface locale | Page claude.ai (Artifact) |
|---|---|---|---|
| Ce que c'est | `claude -p` par étape, état en JSON sur disque | une page servie depuis le Mac, qui lit l'état et lance le script | une page hébergée, état partagé dans sa base |
| Qui exécute les étapes | le script | le script, déclenché depuis la page | Claude, dans la conversation ou via la page (capacité « demander à Claude » à vérifier) |
| Isolation entre étapes | **réelle** : le script choisit ce qu'il transmet | réelle | dépend de l'exécution |
| Partage | non | non | **oui** (lien privé, partageable) |
| Installation | aucune | un petit serveur | aucune |
| Pour qui | toi | toi | toi et d'autres (client, collègue) |

**Décision (2026-10-14) : architecture indépendante du moteur**, pour fonctionner avec Claude Code, Codex, agy (Gemini) et Vibe (Mistral) :

1. **Le cœur** — un fichier JSON d'état par parcours (étapes, statut, sorties, fiche de contexte, questions en attente, réponses) ; la définition des étapes vient de la recette.
2. **Un exécuteur en script** — chaque étape dans un appel neuf (`claude -p`, `codex exec --json`, `agy -p --output-format stream-json`, `vibe -p --output json`), moteur choisi par étape ; affiche le nombre d'appels avant de lancer (petits abonnements Codex et agy).
3. **Un serveur MCP « parcours »** — pour piloter un parcours en conversation depuis tout agent qui parle MCP (`claude mcp`, `codex mcp`, `agy mcp` ; Vibe à vérifier) ; le serveur tient l'état et ne rend à l'agent que ce dont l'étape a besoin.
4. **Une page locale de suivi** sur le même état : étapes, questions en attente, « lancer l'étape suivante avec tel moteur ».

La page claude.ai reste une option de partage en lecture seule, plus tard. Bonus : faire tourner une même étape sur deux moteurs donne un banc de comparaison sur de vrais parcours.

## 5. Hypothèses à valider

1. Sous Claude Code, un SKILL.md de workflow peut faire tourner chaque étape dans un sous-agent qui ne reçoit que le handoff ; le comportement sous Cowork n'est pas connu.
2. Une page claude.ai peut faire exécuter une étape par Claude depuis la page elle-même (à vérifier dans les capacités des Artifacts).
3. Cowork accepte les sources `git-subdir` du catalogue `amiel-35/plugins` (à tester avec « Ajouter depuis un dépôt »).
4. Un `mode: handoff` en Markdown compact suffit quand un modèle lit l'étape suivante ; le JSON n'est nécessaire que quand un script filtre.

## 6. Questions ouvertes (à trancher par Amiel)

*Les questions 1 à 4 ont été tranchées le 2026-10-14 (§3bis) ; la 5 se discute à part.*


1. **Isolation** : sous-agent par étape sous Claude Code (consignes en repli ailleurs), ou consignes partout pour un comportement identique sur toutes les plateformes ?
2. **Brief brut à la dernière étape** : le redonner pour le destinataire et le format, ou jamais après l'étape 1 ?
3. **Pour qui sont les parcours suivis** : toi seul (script + interface locale suffisent), ou aussi des clients ou collègues (page claude.ai partageable) ?
4. **Premier parcours outillé** : recrutement (le plus riche, références métier prêtes) ou réponse à appel d'offres (le plus fréquent en conseil) ?
5. **Fusion `contrat-fournisseur` / `cgv-checker`** : on fusionne, ou on garde les deux ?

## 7. Ordre proposé

1. **Lot 1** — A + B : spec du format de recette (isolation, fiche de contexte, pauses, sous-parcours), prototypée sur **`brief-client`**, joué sous Claude Code avec sous-agents sur un vrai brief ; puis le parcours **réponse à appel d'offres** (§3ter) écrit dans le même format, en réutilisant `brief-client`.
2. **Lot 2** — C + D + E : sortie JSON des skills du parcours, fichier d'état, exécuteur multi-moteur en script.
3. **Lot 3** — serveur MCP « parcours » et page locale de suivi, sur ce même parcours ; partage plus tard.
4. **Lot 4** — F, G, H, I au fil de l'eau, chaque recette convertie selon le format validé au lot 1.

## 8. Prochain pas

Écrire la spec du format (A) en partant de la synthèse des workflows d'ix-memory et des décisions du §3bis, prototyper `brief-client` sur un vrai brief, puis écrire et jouer le parcours appel d'offres (§3ter) sur le cahier des charges de test.
