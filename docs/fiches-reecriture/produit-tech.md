# Analyse de la famille « produit-tech » (2026-10-16)

Onze skills : `prd`, `product-spec`, `feature-spec`, `reformulation-us`, `okr`, `persona`, `journey-map`, `mockup`, `system-design`, `tech-debt`, `ticket-triage`. Version analysée : branche de départ `cbe271c`. Grille : `docs/etat-de-l-art-skills.md` (G1–G10, R1–R10). Rien n'a été modifié dans le dépôt.

Sources Anthropic citées :
- **kwp** = anthropics/knowledge-work-plugins, clone un clone local (non versionné), commit `33eeda1e8fd856455b05479d13a0f85b5f803744` (2026-10-15), Apache-2.0, pas de NOTICE. Les quatre fichiers déjà crédités (write-spec, system-design, tech-debt, ticket-triage) n'ont pas changé depuis `7b2ea8e`.
- **frontend-design** = anthropics/skills, `skills/frontend-design/SKILL.md`, lu sur `main` au commit `dbd4588f9e1033efb41dad4bef2f7947c8993d44` (2026-10-09) ; dernier commit touchant le fichier : `41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f` (2026-09-03, « avoid generic design defaults »). 71 lignes. Licence : Apache-2.0, `skills/frontend-design/LICENSE.txt` (177 lignes, texte standard). C'est un **autre dépôt** que kwp : une reprise demanderait une nouvelle section dans `THIRD_PARTY.md`.

Droit vérifié le 2026-10-16 avec l'outil de normes (statut VIGUEUR pour chacun) : RGPD art. 5, 9, 25, 33, 34, 44 ; loi n° 2005-102 art. 47 ; CSP art. L1111-8.

## A. Tableau

| Skill (version) | Lignes · équivalent Anthropic | Pourquoi il a cette longueur | Justifié ou manque | Ce qui change | En attente (§3) |
|---|---|---|---|---|---|
| `prd` (1.1.0) | 85 · kwp `write-spec` 250 | Gabarit ix (rôle, règle absolue, méthode en 9 étapes, structure en 11 rubriques). Aucune règle de métier au-delà de « le quoi, pas le comment ». | **manque** : il ne dit ni comment fixer une cible, ni comment tenir le périmètre, ni quoi faire d'une solution déjà nommée dans le brief. | Ajouter 5 savoirs tirés de write-spec : test du P0, non-objectifs avec leur raison, règles de cible, signes de dérive du périmètre, questions marquées avec un responsable. Ajouter 2 contraintes RGPD à signaler. Corriger l'entrée « feature spec » (annexe B). Donner une raison aux 4 interdits et fusionner les doublons. | 4 — recette « PRD depuis une demande de sponsor » : le skill y reste la dernière étape, rien à préparer. |
| `product-spec` (1.1.0) | 104 · kwp `write-spec` 250 ; en partie `design-handoff` 131 | Presque tout est de la forme : 6 artefacts compagnons et la règle qui dit quand produire chacun, répétée deux fois. Pas de savoir produit. | **manque** : il ne sait pas ce qu'une spec d'écran oublie d'habitude (états, contenus limites, droits, cycle de vie des objets). | Supprimer l'entrée morte `spec_plan` (annexe B). Ajouter une liste d'états et de cas limites (d'après design-handoff). Dire une fois pourquoi `spec` est le document de référence. Reformuler 5 interdits. | 11 — fusion avec `feature-spec` : le savoir commun (critères d'acceptation, P0) n'est pas ajouté ici. |
| `feature-spec` (1.1.1) | 91 · kwp `write-spec` 250 (source déjà créditée) | Gabarit avec un peu de discipline métier (MoSCoW, « si tout est Must… », Given/When/Then). Le reste de write-spec a été coupé. | **mixte** : il a la structure, il lui manque les règles qui rendent une spec vérifiable. | Reprendre de write-spec : test du P0, P2 « assurance d'architecture », erreurs de user stories, conseils pour les critères d'acceptation (cas négatifs, mots vagues), règles de cible. Produire critères et métriques par défaut. Ajouter un court exemple US + critères. | 11 — fusion avec `product-spec` (l'enrichir ne préjuge pas de l'id gardé). |
| `reformulation-us` (1.1.0) | 75 · kwp `write-spec` (US L137–152, critères L194–220) | Gabarit court. La règle absolue et les contraintes se répètent (intention gardée, US irrécupérable signalée). | **mixte** : le geste est clair, mais il ne nomme pas les défauts qu'il doit reconnaître. | Ajouter les 5 erreurs de user stories (write-spec L147–152) comme grille de diagnostic, dont « tâche technique déguisée en US ». Ajouter la règle « ne pas réécrire une US déjà correcte ». Ajouter les conseils de critères d'acceptation. Fusionner les doublons. | — |
| `okr` (2.1.0) | 162 · kwp `metrics-review` 388 (partie OKR L235–273) | Du contenu : formule, trois profils de calibrage, sortie et résultat, deux modes. 15 négations, presque toutes avec leur raison. | **justifié** : c'est le skill le plus abouti de la famille. | Ajouter le test de trajectoire contre les KR trop faciles, la norme « atteinte d'environ 0,7 », la norme « 2–4 KR par objectif » (metrics-review). Donner une raison à 4 interdits. La notation de fin de période n'est **pas** reprise : ce serait un troisième mode. | 2 (phases autour d'une séance) : sans effet sur la réécriture. |
| `persona` (1.1.0) | 76 · kwp `synthesize-research` (personas L225–274) 312 | Gabarit, plus une structure de sortie qui commence par l'âge. | **manque** : la sortie pousse vers des personas démographiques, sans seuil de preuve. | Ajouter : comportement plutôt que démographie, variables qui distinguent les groupes, nombre de participants par motif, « dire ≠ faire », verbatims pseudonymisés (RGPD art. 5). Corriger la structure de sortie. Reformuler 2 interdits. | 6 + décision §6bis non reportée : le skill allégé qui reçoit les groupes d'`affinity-mapping` change sa forme, donc il est **listé, pas proposé**. |
| `journey-map` (1.1.0) | 78 · aucun (kwp `user-research` en dit une ligne) | Gabarit. La consigne « observé ou hypothèse » est écrite 4 fois, « pas un flux technique » 3 fois. | **mixte** : sans équivalent, le modèle connaît la méthode. Ce qui lui manque, ce sont 3 règles de cadrage et des défauts chiffrés. | Ajouter : un acteur et un scénario par carte, une carte qui commence avant le produit et finit après, 5 à 8 étapes, chaque émotion reliée à une preuve. Retirer les répétitions. | — |
| `mockup` (1.1.0) | 70 · aucun chez kwp ; `frontend-design` (anthropics/skills) 71 | 5 étapes génériques, aucun savoir de design. | **manque**, mais l'avenir du skill n'est pas tranché. frontend-design couvre l'esthétique et un socle de qualité ; il ne couvre pas la fidélité, les états, le marquage du provisoire ni la charte imposée. | Si on le garde : ajouter les états à montrer, le marquage visible du provisoire, le respect de la charte, un socle d'accessibilité chiffré, du contenu réaliste (voir fiche). Clarifier le paramètre `niveau_fidelite`. | 12 — enrichir ou retirer. La comparaison est faite et éclaire la question sans la trancher. |
| `system-design` (1.1.1) | 75 · kwp `system-design` 42 (crédité) | Gabarit plus les 5 étapes de la source. ix en dit déjà plus que la source. | **mixte** : il est complet en méthode. Il lui manque les contraintes réglementaires européennes, et les noms des sorties ne correspondent pas à `output_types`. | Ajouter les contraintes à poser dès les exigences : RGPD art. 25, transferts hors UE (art. 44), données de santé (art. 9, CSP L1111-8). Ajouter « faciliter / compliquer / à revoir » pour chaque décision (kwp `architecture`). Exiger une estimation de charge chiffrée. Aligner les clés de sortie. | 8 — `questioning` → answers → `system-design` quand le brief est flou : sans effet sur le texte. |
| `tech-debt` (1.2.1) | 76 · kwp `tech-debt` 32 (crédité) | Formule, seuils, règle RAS, et une des rares raisons données (« sans justification métier, l'item est déprogrammé »). | **mixte** : il est plus riche que la source, mais sa formule est cassée par la double inversion de l'effort. | Corriger la double inversion (annexe B). Donner des repères pour chaque échelle et la raison des seuils 28 / 15. Rendre la colonne catégorie → risque de la source. Aligner les clés de sortie. Retirer les doublons. | — |
| `ticket-triage` (1.1.2) | 80 · kwp `ticket-triage` 275 (crédité) | Il ne garde de la source que les 4 définitions P1–P4 et la règle « dans le doute, monter ». Les délais, les déclencheurs, le routage et les réponses types ont été coupés. | **manque** : la source porte justement le savoir qui a été coupé, et il manque la règle RGPD de la violation de données. | Reprendre les délais par priorité comme défauts, les déclencheurs de montée, les conseils de catégorie, la table de routage et 2 réponses types (Bug, Sécurité). Ajouter les 72 h (RGPD art. 33) et le cas du sous-traitant. Corriger la recherche de doublons sans base (annexe B). | — |

---

## B. Fiches de réécriture

Pour toutes les fiches : le corps reste en anglais ; on ne change ni l'id, ni la forme, ni le périmètre ; on garde « RAS — » là où il existe. Une reprise de kwp ajoute une ligne à la table kwp de `THIRD_PARTY.md`, ou complète la colonne « Ce qui en est repris », en citant le commit `33eeda1`. La triade « distinguer faits / hypothèses / … », recopiée dans presque tous ces skills, s'écrit **une fois** par skill, au point où elle sert, avec ce qu'on fait concrètement (une étiquette sur chaque ligne).

---

### 1. `prd` (1.1.0 → 1.2.0)

**Savoir métier à ajouter**
- Test du P0 : « si on retire cette exigence, le produit résout-il encore le problème central ? Non → P0 ». Source kwp `product-management/skills/write-spec/SKILL.md` L115.
- P2 = « assurance d'architecture » : ce qu'on ne construit pas mais qui doit rester possible. On l'écrit pour que l'équipe technique ne ferme pas la porte. Source write-spec L119, L166.
- Non-objectifs : 3 à 5, **chacun avec sa raison** (impact trop faible, trop complexe, autre chantier, prématuré). Source write-spec L91–95.
- Règles de cible pour chaque métrique : un seuil de succès **et** une cible haute, la méthode de mesure (outil, requête, fenêtre), la date d'évaluation (1 semaine, 1 mois, 1 trimestre après lancement). Une cible sans base mesurée s'écrit « base à mesurer » (même règle que `okr`). Source write-spec L187–192.
- Dérive du périmètre : toute exigence ajoutée en retire une autre ou décale la date ; prévoir un « parking » pour les bonnes idées hors périmètre. Source write-spec L232–238.
- Questions ouvertes : chacune marquée **bloquante ou non**, avec **qui répond** (tech, design, juridique, données, sponsor). Une question à laquelle le contexte répond déjà n'est pas une question ouverte. Source write-spec L127–130, L250.
- Solution nommée dans la demande (« une appli React Native », « avec Firebase ») : elle devient une contrainte si elle est justifiée (qui l'impose, pourquoi), sinon une hypothèse à valider. Elle n'entre jamais dans les exigences. Raison : c'est la règle d'ix-skills `cadrage` / `brief`. Le PRD reste valable si l'implémentation change.
- Exigences non fonctionnelles à poser quand elles s'appliquent (le modèle les oublie souvent) :
  - Données personnelles : protection dès la conception et par défaut, seules les données nécessaires à chaque finalité, y compris pour la durée de conservation. RGPD art. 25, https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:02016R0679-20160504 (source_url renvoyée : http://publications.europa.eu/resource/celex/02016R0679-20160504), vérifié 2026-10-16.
  - Accessibilité numérique : obligatoire pour les services en ligne des personnes publiques, de leurs délégataires et des entreprises au-dessus d'un seuil de chiffre d'affaires fixé par décret ; déclaration d'accessibilité et mention en page d'accueil. Loi n° 2005-102 art. 47 (version du 2023-09-08), https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048050213/2023-09-08, vérifié 2026-10-16. Le montant du seuil (décret) est **non vérifié** : ne pas l'écrire dans le skill.

**Reprises d'Anthropic** : write-spec L91–95, L115, L119, L127–130, L166, L187–192, L232–238, L250 (savoir K). Pas de gabarit à reprendre : celui d'ix suffit. À créditer dans la ligne `feature-spec`/`prd` de `THIRD_PARTY.md`. Il faudra créer la ligne `prd`, qui n'existe pas encore.

**Contraintes à reformuler**
- « You describe the what and the why — never the how. » → garder et donner la raison : un « comment » fige un choix avant que l'équipe en ait étudié les compromis. Renvoyer à la règle de la solution nommée.
- « You never present as validated what is still a hypothesis to test. » + « You explicitly distinguish context facts, critical hypotheses, and retained requirements. » + « Explicitly flag unvalidated hypotheses. » (trois fois) → une seule consigne positive : chaque exigence porte une étiquette, soit « validé (source) », soit « hypothèse (comment la tester) ».
- « Do not go down to the design or implementation level. » + « Maintain a level of abstraction that allows changing the implementation… » → fusionner. La seconde est la raison de la première.
- « Do not produce a backlog of user stories » → retirer du corps : la frontière est déjà dans la description (G7). Garder une ligne qui dit que `feature-spec` prend la suite.

**Défauts d'annexe B**
- Les entrées attendues citent « feature spec », qui vient en aval. Remplacer par : brief (ou sortie de `cadrage` / `brief`), OKR, recherche utilisateur, vision. Retirer `spec` de `input_types` si aucun cas d'usage ne le justifie (à confirmer).

**Autres constats**
- Les paramètres mystaffy `niveau_detail` (lean / standard / complet), `inclure_metriques` et `inclure_hypotheses` ne sont pas lus par le corps. Une ligne peut dire ce que « lean » retire (par exemple : pas d'exigences non fonctionnelles détaillées, métriques réduites à une seule).

**Exemple de forme** : pas nécessaire.

**Cas de test**
> « Notre directeur des opérations veut "une appli mobile en React Native avec Firebase pour que les techniciens saisissent leurs rapports d'intervention, avec mode hors ligne". Contexte : 120 techniciens, les rapports sont faits sur papier et ressaisis au bureau en moyenne 2 jours plus tard ; 8 % des factures d'intervention sont contestées par les clients parce que le rapport est illisible ou incomplet. Les rapports contiennent le nom du client, son adresse, et parfois une signature. Objectif de la direction : lancer avant l'été. Fais-moi le PRD. »

Une bonne sortie contient :
1. Un problème qui chiffre ce que coûte le statu quo (délai de 2 jours, 8 % de factures contestées).
2. Des objectifs en résultats, avec un seuil, une cible haute, une méthode de mesure et une date. Exemple : contestations de 8 % vers un seuil et une cible, mesurées sur les factures du trimestre suivant.
3. React Native et Firebase sortis des exigences et rangés en contrainte (si justifiée) ou en hypothèse, avec la question « qui l'impose ? ». *(échoue probablement avec 1.1.0)*
4. Le mode hors ligne traité comme une exigence (besoin : saisir sans réseau), pas comme une technologie.
5. Des non-objectifs, chacun avec sa raison.
6. Une exigence non fonctionnelle sur les données personnelles : minimisation, durée de conservation des rapports et des signatures. *(échoue probablement)*
7. Des hypothèses étiquetées et séparées des exigences (exemple : « chaque technicien a un smartphone professionnel »).
8. Des questions ouvertes marquées bloquantes ou non, avec qui répond. *(échoue probablement)*
9. Aucune user story ni aucun backlog ; une mention de `feature-spec` comme étape suivante.
10. « Avant l'été » traité comme une échéance, avec ce qui en dépend.

---

### 2. `product-spec` (1.1.0 → 1.2.0)

**Savoir métier à ajouter** (propre à une spec d'écran ou de parcours, distinct de `feature-spec`)
- États à spécifier pour chaque vue : par défaut, chargement, vide (premier usage et filtre sans résultat), erreur (récupérable ou non), partiel, sans droit d'accès, désactivé. Source kwp `design/skills/design-handoff/SKILL.md` L37–43, L60.
- Cas limites de contenu : texte très long ou très court, traduction plus longue, beaucoup d'éléments (pagination ou chargement progressif, avec un nombre), connexion lente, donnée manquante. Source design-handoff L44–48.
- Modèle de données (pas dans la source, savoir courant que le modèle omet) : pour chaque objet, son identifiant, son cycle de vie (états et transitions, qui les déclenche), qui le possède et le voit, ce qui se passe à la suppression. Une règle métier dérivée (par exemple un statut « en retard ») a sa règle de calcul écrite, avec le fuseau horaire et la date de référence.
- Pas de nouveau partial : la liste tient en une dizaine de lignes dans le corps.

**Reprises d'Anthropic** : design-handoff L37–48 et L60 (savoir K). Nouveau fichier source à créditer : nouvelle ligne `product-spec` dans la table kwp.

**Contraintes à reformuler**
- « You must always produce a main artifact of type `spec`. », écrit deux fois (règle absolue et règle multi-sorties) → une seule fois, avec la raison : c'est le document que la suite lit en premier, les annexes ne servent qu'à le délester.
- « You never invent a document type outside the manifest. » → « Companion artefacts are limited to the types listed in `output_types`. » Ajouter la raison si elle existe (mystaffy route les sorties par type). Sinon, **à confirmer par Amiel**, et retirer la phrase si aucun lecteur ne dépend des types.
- « Do not drown the main spec in unnecessary appendices. » → doublon de la règle multi-sorties, qui dit déjà quand produire chaque annexe : supprimer.
- « Do not produce multiple separate specs without clearly stating the decomposition chosen. » → positif : « if you split, open with the split and its reason ».
- « Never present as decided what is only a hypothesis. » → étiquette, comme pour `prd`.
- « Mermaid diagrams should clarify, not decorate. » → défaut : un diagramme par parcours qui a au moins une branche ; aucun pour un écran seul.

**Défauts d'annexe B**
- Entrée `spec_plan` morte : l'atome `ix-skills:analysis` produit aujourd'hui `analysis_plan`. Deux options : renommer en `analysis_plan` (le découpage vient alors de `analysis`), ou supprimer l'entrée. Corriger aussi le rôle (« or a decomposition plan ») et la puce des entrées. La première option garde le cas du tableau « Une spec par lot » de la revue (§1.2).

**En attente (§3 n° 11)** : conseils de critères d'acceptation, test du P0, user stories. Ce savoir est dans `feature-spec`. Si les deux skills fusionnent, il arrive tout seul ; sinon, le recopier ici serait un doublon à décider après la question 11.

**Exemple de forme** : une ligne de tableau d'états (vue × état × ce qu'on montre × action possible), balisée `<example>`.

**Cas de test**
> « Écris la spec de l'écran "Mes factures" de notre espace client B2B : liste des factures, filtre par période, téléchargement du PDF, statut payé / en attente / en retard. Certains clients ont plus de 2 000 factures. Seuls les utilisateurs avec le rôle "Facturation" voient les montants. »

Une bonne sortie contient :
1. Une `spec` principale lisible seule, ouverte par le découpage choisi et la liste des annexes avec leur raison.
2. Les états de la liste : chargement, vide (aucune facture ; filtre sans résultat, avec deux messages distincts), erreur, sans droit sur les montants. *(échoue probablement)*
3. Les 2 000 factures traitées : pagination ou chargement progressif, avec un nombre par page.
4. La règle de calcul de « en retard » (échéance dépassée et non payée), avec la date et le fuseau de référence. *(échoue probablement)*
5. Le comportement pour le rôle sans « Facturation » (montants masqués ou écran refusé), posé en question s'il n'est pas tranché.
6. Un modèle de données de la facture : identifiant, numéro, dates, montant, statut et ses transitions.
7. Des critères d'acceptation vérifiables, dont au moins un cas négatif (PDF indisponible).
8. Aucune mention de `spec_plan`, et aucune annexe produite sans raison.

---

### 3. `feature-spec` (1.1.1 → 1.2.0)

**Savoir métier à ajouter** (tout vient de kwp `write-spec`, source déjà créditée)
- Test du P0 (L115) ; P1 = ce qu'on est sûr de construire bientôt, pas une liste de souhaits (L165) ; P2 = assurance d'architecture (L119, L166).
- Erreurs de user stories : trop vague, solution imposée (« un menu déroulant »), sans bénéfice, trop grande, centrée sur l'équipe interne (L147–152). Chacune avec ce qui ne va pas, à la manière de la source.
- Critères d'acceptation : chemin nominal, erreurs et cas limites ; au moins un cas négatif (ce qui ne doit pas se produire) ; chaque critère testable seul ; pas de mots vagues (« rapide », « intuitif ») sans chiffre (L215–220).
- Règles de cible des métriques (L187–192), comme pour `prd`.
- Non-objectifs avec leur raison (L91–95) ; une exigence ajoutée en retire une autre (L234).

**Reprises d'Anthropic** : les passages ci-dessus ; compléter la colonne « Ce qui en est repris » de la ligne `feature-spec` dans `THIRD_PARTY.md` et y indiquer le commit `33eeda1`. Ne pas reprendre INVEST, MoSCoW ni la définition de Given/When/Then : le modèle les connaît (G1).

**Contraintes à reformuler**
- « You must always produce a main artifact of type `feature_spec`. » → garder sans « must » : « The main document is `feature_spec`; the others are optional splits of it. »
- « You never present as decided what is still a hypothesis. » + « flag areas of uncertainty rather than masking them » + « distinguish the product need… » (trois fois) → une étiquette par exigence.
- « Do not present a choice as Must if the team has not agreed. » → raison : un Must bloque la livraison ; un Must non validé bloque donc sur une hypothèse. Positif : « mark it "Must (proposed, to confirm)" ».
- Étapes 6 et 7 « if requested » → produire les critères et les métriques **par défaut**, comme le promet la description et comme le règlent les paramètres mystaffy (par défaut `true`). Les omettre seulement sur demande.

**Défauts d'annexe B** : aucun.

**Autres constats**
- Le paramètre mystaffy `format_spec` a une valeur `prd`, qui se télescope avec le skill `prd`. À signaler à Amiel, sans le corriger ici (changement de périmètre).

**Exemple de forme** : une user story et ses trois critères (nominal, erreur, cas négatif), sur un sujet différent des cas de test. Exemple de sujet : réinitialiser un mot de passe. Une phrase dit pourquoi il est juste.

**En attente (§3 n° 11)** : fusion avec `product-spec`. Les ajouts ci-dessus restent valables dans les deux issues.

**Cas de test**
> « Spec fonctionnelle : export CSV des factures depuis l'espace client, pour nos clients PME qui l'envoient à leur expert-comptable. Sur 1 200 tickets "facturation" par trimestre, 30 % demandent un export. Il faut livrer avant le 15 janvier (clôtures annuelles). L'équipe voudrait aussi l'export PDF groupé et une API, et le PO considère que tout est Must. »

Une bonne sortie contient (valeur de référence : 30 % × 1 200 = **360 tickets d'export par trimestre**) :
1. Le problème en 2–3 phrases, avec la base de 360 tickets par trimestre.
2. Une métrique de succès avec un seuil et une cible haute sous cette base, une méthode de mesure (catégorie de ticket, fenêtre) et une date d'évaluation. *(échoue probablement)*
3. Le « tout est Must » contesté : CSV en Must par le test du P0 ; PDF et API en Should, Could ou Won't, chacun avec sa raison. *(échoue probablement)*
4. L'API classée en P2 / assurance d'architecture, ou en non-objectif avec sa raison.
5. Des user stories avec un utilisateur précis (gérant de PME, comptable) et une capacité sans élément d'interface.
6. Des critères Given/When/Then, dont un cas négatif (période sans facture, utilisateur sans droit).
7. Aucun mot vague sans chiffre (par exemple « export rapide » sans durée maximale).
8. Le format du fichier (séparateur, encodage, format des montants) posé en exigence ou en question bloquante.
9. Des questions ouvertes marquées bloquantes ou non, avec qui répond ; l'échéance du 15 janvier reprise.

---

### 4. `reformulation-us` (1.1.0 → 1.2.0)

**Savoir métier à ajouter**
- Grille de diagnostic : les 5 erreurs de write-spec L147–152 (trop vague, solution imposée, sans bénéfice, trop grande, centrée sur l'interne). Chaque US réécrite dit quelle erreur elle corrige.
- Une « US » technique (« en tant que développeur, je veux migrer la base ») est une tâche : la classer comme telle dans `us_problematiques`, sans lui inventer un utilisateur. Raison : un faux bénéfice utilisateur fausse la priorisation. Source write-spec L152.
- Une US déjà correcte ne se réécrit pas ; on lui ajoute seulement ses critères. Raison : réécrire sans motif fait perdre au lecteur ce qui a changé.
- Découpage d'une US trop grande : par étape du parcours, par règle métier, par variante de données, par chemin nominal ou d'erreur. C'est une méthode publique courante (R. Lawrence, « story splitting »), **non relue le 2026-10-16** : la citer comme défaut sans la sourcer précisément, ou la retirer.
- Conseils de critères d'acceptation (write-spec L215–220), comme pour `feature-spec`.

**Reprises d'Anthropic** : write-spec L147–152, L215–220 (K). Nouvelle ligne `reformulation-us` dans la table kwp.

**Contraintes à reformuler**
- « You rewrite — you do not rebuild from scratch. » + « Do not change the original intent of the US. » + « You remain faithful to the original intent » → une seule phrase, avec sa raison : l'auteur doit reconnaître sa demande, sinon la réécriture rouvre la discussion.
- « Do not describe a technical solution in the capability. » → raison : une solution dans la capacité ferme les options de design. Positif : « if the author named a UI, keep it as a note "suggested solution" ».
- « Flag unrecoverable US (too vague, contradictory) rather than inventing them. » (doublon de l'étape 6 et de la règle absolue) → garder une fois, avec ce qu'on produit à la place : la question qui débloquerait l'US.

**Défauts d'annexe B** : aucun.

**Exemple de forme** : un trio « US d'origine → erreur diagnostiquée → US réécrite », sur un sujet hors cas de test.

**Cas de test**
> « Reformule ces US de notre backlog congés :
> 1. En tant qu'utilisateur, je veux que l'appli soit plus rapide.
> 2. En tant qu'admin, je veux un menu déroulant pour choisir le rôle d'un membre.
> 3. En tant que développeur, je veux migrer la base vers Postgres 16.
> 4. En tant que manager, je veux voir les congés de l'équipe, les valider et exporter le planning.
> 5. En tant que salarié, je veux poser une demi-journée de congé afin de ne pas consommer une journée entière. »

Une bonne sortie contient :
1. L'US 1 placée dans `us_problematiques` (trop vague), avec la question qui la débloquerait (quel écran, quelle durée, mesurée comment), sans capacité inventée.
2. L'US 2 réécrite sur la capacité (« attribuer un rôle »), le menu déroulant gardé en note de solution suggérée.
3. L'US 3 classée comme tâche technique, sans faux utilisateur. *(échoue probablement)*
4. L'US 4 découpée en 3 (consulter, valider, exporter), chacune avec ses critères.
5. L'US 5 gardée presque telle quelle, avec seulement ses critères ajoutés. *(échoue probablement)*
6. Pour l'US 5, au moins un cas négatif dans les critères (solde insuffisant, demi-journée déjà posée).
7. L'erreur corrigée nommée pour chaque US réécrite.
8. Aucun critère avec un mot vague (« rapide ») sans seuil.

---

### 5. `okr` (2.1.0 → 2.2.0)

**Savoir métier à ajouter** (kwp `product-management/skills/metrics-review/SKILL.md`)
- Test de trajectoire contre les KR trop faciles : si la métrique progresse déjà de 5 % par mois, une cible de 6 % n'est pas ambitieuse. Il outille le profil « sandbagged », que le skill nomme sans test. Source L271.
- Repère de calibrage : pour un OKR ambitieux, on vise environ 70 % d'atteinte. Il donne la raison du profil « stretch » : un OKR toujours atteint à 100 % était trop facile. Source L261, L264.
- Nombre : 2 ou 3 objectifs, 2 à 4 KR chacun. En mode 1, signaler un ensemble plus chargé. Source L263.
- Entrées d'une cible : base, référence externe, trajectoire, effort engagé, confiance (« commit » et « stretch »). Le couple commit / stretch recoupe le « minimum acceptable / cible » du skill : garder le vocabulaire du skill (G9, un seul terme). Source L268–273.
- **Non repris** : la notation de fin de période (0–0,3 / 0,4–0,6 / 0,7–1, L266). Noter un OKR échu serait un troisième travail, alors que le skill dit « deux, jamais un troisième ». C'est un changement de périmètre, **à soumettre à Amiel**.

**Reprises d'Anthropic** : metrics-review L261, L263–264, L268–273 (K). Nouveau fichier source : nouvelle ligne `okr` dans la table kwp.

**Contraintes à reformuler**
- « You do one of two jobs, never a third » / « The two modes never merge. Reviewing is not drafting. » → donner la raison réelle : une relecture qui réécrit prend la main sur l'auteur, et l'objectif cesse d'être le sien (la raison est déjà en règle 3, il suffit d'y renvoyer).
- « Name the profile out loud with the person — never settle it silently. » → raison : le profil est un choix d'ambition qui appartient à l'équipe.
- « a concrete forcing mechanism (never a time budget) » → raison manquante : un budget de temps mesure l'effort, pas l'effet. Il est le cas typique de l'output pris pour un mécanisme.
- « Never hand back a finished OKR from a brief » : raison présente, garder.
- Les capitales en gras (« **Never invent an X.** ») peuvent rester : elles portent leur raison.

**Défauts d'annexe B**
- Le déclencheur « objectifs SMART » se dispute avec `performance-review-helper` : ajouter une frontière dans la description (« objectifs individuels d'entretien annuel : voir `performance-review-helper` »), sans changer le périmètre.

**Autres constats**
- Le paramètre mystaffy `horizon` (mois à année) n'est pas lu par le corps : une ligne peut dire que l'échéance d'un KR suit l'horizon choisi.

**Exemple de forme** : non (le format de verdict est déjà décrit).

**Cas de test**
> « Relis nos OKR du T1 (janvier–mars) :
> O : Améliorer l'onboarding.
> KR1 : Passer le taux d'activation à J7 de 32 % à 34 % d'ici fin mars. (Pour info, l'activation gagne 1 point par mois depuis 6 mois.)
> KR2 : Publier 4 tutoriels vidéo.
> KR3 : Réduire le temps de création du premier projet à 10 minutes d'ici fin mars.
> KR4 : NPS onboarding à 70.
> KR5 : Faire passer les tickets support liés à l'onboarding de 450 à 150 par mois d'ici fin mars. »

Une bonne sortie contient (valeur de référence : 32 % + 3 mois × 1 point = **35 % attendus par la seule tendance**) :
1. L'objectif signalé comme incomplet : il manque l'impact visé.
2. KR1 signalé comme trop facile, parce que 34 % est sous la tendance (35 %). *(échoue probablement)*
3. KR2 classé comme tâche déguisée (output).
4. KR3 : base absente, déclarée « base manquante — à mesurer », sans chiffre inventé.
5. KR4 : base et échéance absentes, chacune nommée.
6. KR5 : une division par 3 en 3 mois, signalée comme possiblement aspirationnelle, avec la question du mécanisme qui la rend possible.
7. 5 KR pour un objectif signalés au-dessus de la norme de 2 à 4. *(échoue probablement)*
8. Aucune ligne réécrite à la place de l'auteur (mode 1) ; chaque verdict porte sa question.
9. Aucune note de fin de période (0–1) attribuée.

---

### 6. `persona` (1.1.0 → 1.2.0)

**Savoir métier à ajouter** (kwp `product-management/skills/synthesize-research/SKILL.md`)
- Comportement plutôt que démographie : un persona défini par l'âge ou le lieu prédit mal les besoins. Source L270. Conséquence : la structure de sortie remplace « name and profile (age, context — indicative) » par « contexte : rôle, situation, fréquence et façon d'utiliser » ; l'âge n'apparaît que s'il est sourcé.
- Variables qui distinguent les groupes (taille d'entreprise, compétence, fréquence, cas d'usage principal) : les nommer pour montrer pourquoi deux personas sont distincts. Source L231.
- Seuil de preuve : chaque motif dit combien de participants le portent (« 3 sur 6 »). Un motif porté par 1 ou 2 entretiens est une hypothèse. Source L309.
- Dire et faire : ce que les gens déclarent pèse moins que ce qu'ils font. Étiqueter chaque élément « déclaré », « observé » ou « supposé ». Source L307.
- Moins de personas si les données n'en portent pas plus, même si on en demande davantage. Raison : un persona sans groupe réel derrière est une fiction de marketing, ce que la règle absolue refuse.
- Verbatims attribués par type de participant, jamais par nom (synthesize-research L308). Raison légale : les notes d'entretien sont des données personnelles, et seules les données nécessaires à la finalité doivent être traitées (minimisation). RGPD art. 5 § 1 c), http://publications.europa.eu/resource/celex/02016R0679-20160504, vérifié 2026-10-16.
- Le plafond ix de 4 profils reste ; kwp dit 3 à 5 (L271). Garder 4 avec sa raison actuelle : un seul seuil (G9).

**Reprises d'Anthropic** : synthesize-research L231, L269–274, L307–309 (K). Nouveau fichier source : nouvelle ligne `persona`.

**Contraintes à reformuler**
- « Do not invent precise demographic data without a source. » → positif, avec la raison ci-dessus (le comportement prédit les besoins ; un âge inventé oriente le design sur du faux).
- « Each persona must have a distinct primary need — no duplicates. » → garder, avec la raison de la Definition of done (sinon deux personas mènent aux mêmes décisions) ; supprimer le doublon de la DoD.
- « You always distinguish what is grounded in data from what is assumed. » + « Explicitly flag hypotheses vs observed facts. » + étapes 5–6 (quatre fois) → une seule consigne d'étiquetage.

**Défauts d'annexe B — listé, pas proposé**
- Décision §6bis (cadrage-suite.md, 2026-10-15) : « Personas : `affinity-mapping` → pause → `persona` reste juste ». La reporter veut dire que `persona` reçoit des groupes déjà validés au lieu de les former lui-même (étapes 1–2 retirées quand des groupes sont fournis), avec un double point d'entrée (corpus brut ou groupes). **C'est un changement de forme** (skill allégé, mélange), lié à la question 6 et au besoin de moteur §1.1 (citer sans réécrire). Le rédacteur n'y touche pas. Ce qui reste sans effet sur la forme : rien de plus que les ajouts ci-dessus.
- Constat : `affinity-mapping` n'existe pas encore sur `main` d'ix-skills. Dans le clone local `~/Projets/ix-skills`, `skills/affinity-mapping.md` est un fichier **non suivi par git**, et le dépôt public n'en a pas. La recette décidée au §6bis s'appuie donc sur un atome non publié.

**En attente (§3 n° 6)** : forme du skill (mélange avec données terrain).

**Exemple de forme** : une ligne de motif avec sa preuve (« Saisit ses frais le soir, en lot — observé, 3/6 — verbatim d'un commercial terrain »).

**Cas de test**
> « Fais-nous 3 personas à partir de ces 6 entretiens sur notre appli de notes de frais :
> – Karim B., commercial terrain : "Je prends les tickets en photo dans la voiture, sinon je les perds." Saisit tout le vendredi soir.
> – Sophie L., commerciale terrain : "Je fais mes notes une fois par mois, c'est l'enfer." A 3 semaines de retard en moyenne.
> – Hugo T., commercial terrain : photographie les tickets, oublie de les catégoriser.
> – Nadia R., comptable : "Je relance 15 personnes chaque fin de mois." Contrôle les justificatifs un par un.
> – Marc D., comptable : exporte tout dans Excel pour vérifier les plafonds.
> – Claire V., manager : valide depuis son téléphone "entre deux réunions", sans ouvrir les justificatifs. »

Une bonne sortie contient :
1. Des personas définis par leur comportement, sans âge, salaire ni situation familiale inventés. *(échoue probablement)*
2. Pour chaque motif, le nombre de participants qui le portent (3/6, 2/6, 1/6).
3. Le persona manager signalé comme hypothèse, parce qu'il repose sur un seul entretien ; ou bien deux personas seulement, avec la raison. *(échoue probablement)*
4. Des verbatims attribués par rôle, sans les noms des participants. *(échoue probablement)*
5. Un besoin principal distinct par persona.
6. La différence entre déclaré et observé (« saisit le vendredi » est déclaré ; le retard de 3 semaines est un fait rapporté).
7. Des implications produit pour chaque persona.
8. Au plus 4 personas.

---

### 7. `journey-map` (1.1.0 → 1.2.0)

**Savoir métier à ajouter** (pas d'équivalent kwp ; source publique : Sarah Gibbons, NN/g, « Journey Mapping 101 », 2018-12-09, revu par l'éditeur le 2026-07-15, https://www.nngroup.com/articles/journey-mapping-101/, lu le 2026-10-16. Méthode publique : aucune reprise de texte, rien à créditer dans `THIRD_PARTY.md`.)
- Un acteur et un scénario par carte. Deux publics donnent deux cartes. Raison : une carte qui mélange les points de vue moyenne des émotions qui n'existent chez personne.
- La carte commence avant le contact avec le produit (le déclencheur, la recherche) et finit après la dernière interaction (suivi, retour, résiliation). Raison : les frictions les plus coûteuses sont souvent hors produit. Position par défaut à écrire ; elle ne vient pas de la source.
- 5 à 8 étapes par défaut, chacune avec au moins une action de l'utilisateur. C'est le défaut chiffré qui remplace « neither too macro nor too micro ».
- Chaque émotion et chaque friction renvoie à sa preuve (verbatim, donnée d'usage) ou porte l'étiquette « hypothèse ».
- Chaque opportunité dit à quelle friction elle répond, avec un responsable et un indicateur possibles (NN/g : « opportunities », avec responsabilité et mesure).
- Frontière : les étapes internes de l'entreprise relèvent du *service blueprint*, pas de la journey map. Les mettre hors carte, ou en note.

**Reprises d'Anthropic** : aucune.

**Contraintes à reformuler**
- « observé / hypothèse » apparaît 4 fois (règle absolue × 2, étape 6, contrainte 3) → une seule consigne : la colonne « statut de preuve » de chaque étape.
- « A journey map is not a technical flow diagram » + « Do not confuse user stages with technical steps » + « Place yourself from the user's point of view » (3 fois) → une phrase, avec la frontière blueprint.
- « Keep a usable level of granularity — neither too macro nor too micro » → le défaut de 5 à 8 étapes.

**Défauts d'annexe B** : aucun.

**Exemple de forme** : une étape complète (nom, actions, pensées, émotion avec sa preuve, friction, opportunité), sur un sujet hors cas de test.

**Cas de test**
> « Fais la journey map d'un particulier qui résilie son abonnement box internet chez nous. Ce qu'on sait : 40 verbatims du service client. Les plus fréquents : "je n'ai pas trouvé où résilier sur le site" (18), "on m'a dit d'envoyer un courrier" (9), "j'ai dû rappeler 3 fois pour l'étiquette de retour de la box" (7), "j'ai été facturé un mois de plus" (6). Pas de données d'usage du site. »

Une bonne sortie contient :
1. Un seul acteur (le particulier qui résilie) et un seul scénario.
2. Une première étape avant le contact (décision de partir, recherche de la marche à suivre) et une dernière après la demande (retour de la box, dernière facture). *(échoue probablement)*
3. Entre 5 et 8 étapes, chacune avec au moins une action de l'utilisateur.
4. Chaque friction rattachée à son verbatim et à son effectif (18, 9, 7, 6). *(échoue probablement)*
5. Les émotions sans verbatim étiquetées « hypothèse ».
6. Des opportunités, chacune liée à une friction, avec un indicateur possible.
7. Aucune étape interne (traitement en back-office, système de facturation) dans la carte ; si elles apparaissent, c'est hors carte ou en note blueprint.
8. L'absence de données d'usage signalée, avec ce qui la comblerait.

---

### 8. `mockup` (1.1.0) — en attente de la question 12

**Comparaison avec `frontend-design`** (anthropics/skills, `41bbe19`, Apache-2.0), pour éclairer la question 12 sans la trancher :

| | `frontend-design` | `mockup` |
|---|---|---|
| But | une interface finale au **parti pris visuel** fort (« take aesthetic risk », L9) | un support de **discussion** en réunion |
| Ce qu'il apporte | la liste des tics visuels des pages générées (L38–45) ; plan de design puis relecture avant le code (L47–53) ; un socle de qualité implicite : responsive, focus clavier visible, mouvement réduit respecté, accessibilité (L59) ; la structure visuelle est de l'information, pas de numéros 01/02/03 hors séquence (L30) ; contenu réel plutôt qu'emplacements vides, libellés d'action (« Save changes », pas « Submit »), états vides et erreurs qui disent quoi faire (L63–71) | rien de cela |
| Ce qu'il n'a pas | fidélité à choisir ; états à montrer pour décider ; marquage visible du provisoire et de ce qui est déduit ; respect d'une charte ou d'un design system imposés (il dit seulement que « the brief's own words always win », L45) ; fichier unique sans dépendance | il a l'intention (provisoire marqué, fichier autonome), pas le savoir |

Lecture pour la question 12 : les deux skills se recoupent sur la moitié « faire une page propre », que frontend-design traite mieux et qui est installée par défaut dans plusieurs produits Claude (**non vérifié** pour claude.ai et Cowork). La moitié propre à `mockup`, maquette de discussion, existe mais tient en une vingtaine de lignes. Son parti pris « oser » va à l'inverse d'une maquette qu'on veut faire discuter sur la structure. Les deux issues sont défendables ; à Amiel de trancher.

**Si `mockup` est gardé, savoir métier à ajouter**
- Fidélité : basse (structure, gris), moyenne (charte de base, contenu réel), haute (charte complète). Par défaut, moyenne pour une réunion. Raison : une maquette trop finie fait discuter des couleurs au lieu de la structure. Position par défaut à écrire, sans source.
- États : montrer les états qui changent une décision (vide, erreur, chargement, cas long), par exemple avec des onglets ou des sections visibles. Source kwp design-handoff L60.
- Provisoire visible : tout ce qui est déduit ou de remplissage porte une marque visible à l'écran (bordure en pointillés, badge « à confirmer »), et une légende le dit. Raison : en réunion, ce qui n'est pas marqué est pris pour décidé.
- Charte : couleurs et police imposées respectées telles quelles ; le reste du parti pris visuel reste sobre.
- Contenu réel et localisé : vrais libellés, montants au format français (1 234,56 €), dates au format jj/mm/aaaa ; pas de lorem ipsum. Source frontend-design L34, L63–71 (sans le format français, qui est à écrire).
- Socle d'accessibilité chiffré :
  - contraste du texte d'au moins 4,5:1 (3:1 pour le gros texte), WCAG 2.1 critère 1.4.3 (cité par kwp accessibility-review L26) ;
  - focus visible (2.4.7) ;
  - cibles d'au moins 24 × 24 px CSS, WCAG 2.2 critère 2.5.8, niveau AA : https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html, lu le 2026-10-16.
  - Attention : kwp accessibility-review L33 classe « 2.5.5 Touch target ≥ 44x44 » parmi les critères AA, alors que 2.5.5 est un critère AAA (niveau et taille de 44 px **non relus** sur la page W3C ; à vérifier avant d'écrire). Ne pas reprendre cette ligne.
- Obligation légale (une ligne, seulement si l'écran est un service en ligne d'un organisme visé) : loi n° 2005-102 art. 47, vérifiée (voir `prd`).

**Reprises possibles** : design-handoff L60 (kwp) ; frontend-design L30, L34, L59, L63–71 (anthropics/skills). La seconde reprise demande une nouvelle section `anthropics/skills` dans `THIRD_PARTY.md`, avec commit et licence.

**Contraintes à reformuler** (si gardé)
- « The deliverable must be standalone and previewable as-is. » + « Avoid unnecessary external dependencies. » → raison : le fichier s'ouvre en pièce jointe ou hors ligne en réunion, et un CDN bloqué casse le rendu. Positif : CSS en ligne, polices système en repli.
- « Do not deliver a raw assembly of placeholders without intent. » → positif : du contenu réel (voir plus haut).
- « The render must remain presentable on desktop and mobile. » → défaut chiffré : vérifier à 375 px et à 1 280 px de large.

**Autres constats**
- Le paramètre mystaffy `niveau_fidelite` (`reference` / `reinterpretation`) parle de proximité avec une référence, pas de fidélité au sens design. À renommer ou à documenter si le skill est gardé.

**Cas de test** (à jouer seulement si la question 12 garde le skill)
> « Maquette HTML de la page "Mes factures" de notre espace client, pour la réunion de jeudi. Charte : bleu #1A3A5C, police Inter. Montre la liste normale (une dizaine de factures), le cas "aucune facture" et le cas "erreur de chargement". »

Une bonne sortie contient :
1. Un seul fichier HTML, CSS en ligne, lisible sans réseau (Inter avec une police système en repli).
2. Le bleu #1A3A5C et Inter appliqués ; aucune autre couleur dominante ajoutée.
3. Les 3 états visibles et accessibles sans modifier le code. *(échoue probablement)*
4. Des éléments déduits marqués visiblement à l'écran, avec une légende. *(échoue probablement)*
5. Des factures réalistes au format français (numéro, date jj/mm/aaaa, montant 1 234,56 €).
6. Un contraste du texte courant d'au moins 4,5:1, vérifiable dans le CSS.
7. Un focus clavier visible sur les liens et boutons.
8. Des boutons nommés par leur action (« Télécharger le PDF »).
9. Un message d'erreur qui dit ce qui s'est passé et quoi faire.
10. Une mise en page lisible à 375 px de large.

---

### 9. `system-design` (1.1.1 → 1.2.0)

**Savoir métier à ajouter**
- Estimation de charge chiffrée et visible (nombre d'utilisateurs × actions ÷ secondes, facteur de pic écrit) avant tout choix d'architecture. Raison : c'est elle qui décide si une architecture distribuée se justifie. Source kwp system-design L31 (« Load estimation »), à rendre obligatoire.
- Contraintes réglementaires à poser dès les exigences, quand des données personnelles passent dans le système :
  - protection dès la conception et par défaut ; minimisation, conservation et accessibilité limitées à la finalité. RGPD art. 25, http://publications.europa.eu/resource/celex/02016R0679-20160504, vérifié 2026-10-16 ;
  - transfert hors UE/EEE (hébergeur, sous-traitant SaaS, sauvegarde) soumis au chapitre V. RGPD art. 44, même URL, vérifié 2026-10-16 ;
  - données de santé : catégorie particulière, traitement interdit sauf exceptions (dont la prise en charge sanitaire). RGPD art. 9, même URL, vérifié 2026-10-16 ;
  - hébergement de données de santé recueillies lors d'activités de prévention, de diagnostic ou de soins : hébergeur titulaire d'un certificat de conformité (HDS) ; depuis le 2025-07-01, un décret fixe aussi les obligations de stockage dans l'UE/EEE. CSP art. L1111-8 (version du 2025-07-01), https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049577902/2025-07-01, vérifié 2026-10-16. Qu'une simple prise de rendez-vous relève de L1111-8 est **à qualifier** : le skill pose la question, il ne la tranche pas.
- Pour chaque décision structurante, une ligne « ce qui devient plus facile / plus difficile / à revoir quand le système grandit ». Source kwp `engineering/skills/architecture/SKILL.md` L61–64 (gabarit W, fichier non crédité à ce jour).

**Reprises d'Anthropic** : architecture L61–64 ; system-design L31 (déjà crédité). Ajouter `architecture` dans la ligne `system-design` de `THIRD_PARTY.md`.

**Contraintes à reformuler**
- « Do not over-architect for a current problem that does not justify it. » + « Do not propose a distributed architecture without explicit justification. » → une phrase avec sa raison : une architecture distribuée coûte en exploitation ce qu'une petite équipe ne peut pas payer ; l'estimation de charge en décide.
- « Mermaid diagrams must clarify, not decorate. » → défaut : un diagramme de composants et un de flux pour le cas principal ; pas plus sans raison.
- « Flag assumptions made about scale or constraints. » est un doublon de la règle absolue et de l'étape 6 : supprimer.

**Défauts (pas dans l'annexe B, relevés ici)**
- Les noms des sorties ne correspondent pas : le corps annonce `data_model`, `open_questions` et `trade_offs`, alors que `output_types` déclare `modele_donnees`, `api_contracts`, `questions_ouvertes` (et pas `trade_offs`). Aligner le corps sur `output_types`, puis mettre les compromis dans `system_design` ou ajouter le type (à confirmer).

**Exemple de forme** : non.

**Cas de test**
> « Conçois l'architecture d'un service de prise de rendez-vous en ligne pour un réseau de 40 cabinets de kinésithérapie (600 praticiens, en moyenne 20 rendez-vous par praticien et par jour ouvré, 21 jours ouvrés par mois, 60 % des rendez-vous pris en ligne, réservations ouvertes de 8 h à 20 h). Rappel SMS la veille pour chaque rendez-vous ; notre fournisseur SMS facture 0,045 € HT le SMS. Équipe : 3 développeurs Python. Budget d'hébergement : 500 € par mois. Lancement dans 4 mois. »

Valeurs de référence :
- 600 × 20 = **12 000 rendez-vous par jour** ; × 21 = **252 000 par mois**.
- Réservations en ligne : 12 000 × 0,6 = **7 200 par jour** ; sur 12 h (43 200 s) = **0,17 écriture par seconde** en moyenne, environ 0,8 par seconde avec un pic × 5.
- SMS : 252 000 × 0,045 € = **11 340 € HT par mois**.

Une bonne sortie contient :
1. Une estimation de charge chiffrée, cohérente avec les valeurs ci-dessus.
2. Une conclusion tirée de cette charge : un monolithe et une base relationnelle suffisent, sans microservices. *(échoue probablement)*
3. Le coût des SMS (environ 11 340 € HT par mois) relevé comme sans commune mesure avec le budget d'hébergement. *(échoue probablement)*
4. La double réservation d'un même créneau empêchée par une contrainte en base ou une transaction, avec le compromis choisi.
5. Des rappels SMS envoyés en lot, avec reprise sur erreur et sans double envoi (idempotence).
6. La question des données de santé et de l'hébergement HDS (RGPD art. 9, CSP L1111-8) posée comme contrainte à qualifier avant de choisir l'hébergeur. *(échoue probablement)*
7. Pour chaque décision : ce qui devient plus facile, plus difficile, et à revoir avec la croissance.
8. Des choix techniques adaptés à 3 développeurs Python (familiarité de l'équipe dans les compromis).
9. Des questions ouvertes bloquantes listées (qui paie les SMS, fuseau horaire, annulations).

---

### 10. `tech-debt` (1.2.1 → 1.3.0)

**Savoir métier à ajouter**
- Échelles avec repères (défauts à remplacer par ceux de l'équipe) :
  - Impact : de combien l'item ralentit l'équipe (1 = gêne rare, 5 = touche chaque sprint) ;
  - Risque : ce qui arrive si on ne fait rien (1 = rien de visible, 5 = incident en production ou faille de sécurité probable) ;
  - Effort : 1 = moins d'une journée, 5 = plusieurs sprints.
  Sources : kwp tech-debt L24–26 pour les questions ; les repères chiffrés sont à écrire, sans source.
- Raison des seuils (G9, pas de nombre sans raison). Le score maximal est (5 + 5) × 5 = 50. **28** demande un fort enjeu (Impact + Risque ≥ 7) pour un effort ≤ 2, ou un enjeu maximal (10) pour un effort moyen (3). **15** correspond à un enjeu moyen (Impact + Risque ≥ 5) pour un effort moyen (3).
- Colonne « catégorie → risque type » de la source (code → bugs et lenteur ; architecture → limites de montée en charge ; tests → régressions livrées ; dépendances → failles ; documentation → arrivées lentes ; infrastructure → incidents et reprise lente). Elle aide à noter le Risque. Source kwp tech-debt L12–19.

**Reprises d'Anthropic** : tech-debt L12–19 (déjà crédité ; compléter « Ce qui en est repris »).

**Contraintes à reformuler**
- « Each item must have a business justification, not just a technical one. » répète la règle absolue : supprimer et garder la règle, qui porte déjà sa raison.
- « Do not produce an exhaustive unprioritized list. » → raison : la planification ne lit que le haut de la liste. Positif : « rank by score; group items under 15 in one backlog line ».
- « Do not recommend a full rewrite without solid justification. » → raison : une réécriture gèle les fonctionnalités, ce que le plan entrelacé exclut. Positif : dire ce qui la justifierait (par exemple un coût de maintien qui dépasse un coût de remplacement chiffré).
- « Explicitly flag if the audit is partial. » : garder, avec ce que veut dire partiel (périmètre non lu).

**Défauts d'annexe B**
- Effort inversé deux fois : l'étape 2 dit « effort (inverted) », puis l'étape 3 applique « 6 − Effort ». Correction : l'étape 2 note l'effort brut (1 = facile, 5 = lourd) et dit que la formule fait l'inversion. Sinon, les items faciles tombent sous le seuil et les chantiers lourds remontent.

**Autres défauts (relevés ici)**
- Les noms des sorties ne correspondent pas : le corps dit `remediation_plan` et `open_questions`, alors que `output_types` déclare `plan_remediation` et `questions_ouvertes`. Aligner.

**Exemple de forme** : une ligne d'inventaire (item, catégorie, I, R, E, score calculé, horizon, justification métier chiffrée), hors cas de test.

**Cas de test**
> « Audit de dette pour le prochain planning. L'équipe a déjà noté chaque item (Impact, Risque, Effort de 1 à 5, Effort 1 = facile, 5 = très lourd) :
> 1. Module facturation sans tests automatisés, 2 régressions en prod ce trimestre — I4 R4 E2.
> 2. Déploiement manuel, 2 h chaque mardi, une erreur de configuration en juin — I3 R3 E1.
> 3. Django 3.2, plus maintenu depuis avril 2024 — I2 R5 E3.
> 4. README d'installation obsolète, il faut 3 jours pour installer le poste d'un nouveau développeur — I2 R1 E1.
> 5. Découper le monolithe en microservices — I3 R2 E5.
> 6. Logs non structurés — I2 R2 E2. »

Valeurs de référence avec (I + R) × (6 − E) :

| Item | Score | Horizon |
|---|---|---|
| 1 | 8 × 4 = **32** | sprint |
| 2 | 6 × 5 = **30** | sprint |
| 3 | 7 × 3 = **21** | trimestre |
| 4 | 3 × 5 = **15** | trimestre |
| 5 | 5 × 1 = **5** | backlog |
| 6 | 4 × 4 = **16** | trimestre |

Avec la double inversion, on trouverait : item 2 = 6 (backlog), item 5 = 25 (trimestre).

Une bonne sortie contient :
1. Les 6 scores ci-dessus, avec leurs horizons.
2. L'item 2 au prochain sprint, avec 30. *(échoue probablement)*
3. L'item 5 au backlog, avec 5 ; la réécriture en microservices n'est pas recommandée sans justification chiffrée. *(échoue probablement)*
4. Une justification métier pour chaque item retenu (par exemple 2 h par semaine ≈ 100 h par an pour l'item 2 ; les régressions de facturation exposent le chiffre d'affaires).
5. Un plan entrelacé avec les fonctionnalités (part de capacité par sprint), sans gel.
6. Pas de « RAS », puisque des items dépassent 15.
7. Les notes fragiles signalées (exemple : l'impact de l'item 4 dépend du rythme des recrutements, non fourni).
8. Les sorties nommées `tech_debt_audit`, `plan_remediation` et `questions_ouvertes`.

---

### 11. `ticket-triage` (1.1.2 → 1.2.0)

**Savoir métier à ajouter** (kwp `customer-support/skills/ticket-triage/SKILL.md`, source déjà créditée)
- Délais par priorité, donnés comme **défauts à remplacer par ceux de l'organisation** : P1 réponse en 1 h, mises à jour toutes les 1–2 h ; P2 en 4 h ; P3 en 1 jour ouvré ; P4 en 2 jours ouvrés. Source L138, L148, L158, L168.
- Déclencheurs de montée en priorité : délai dépassé, plusieurs clients sur le même problème, escalade explicite ou direction mentionnée, contournement qui cesse de marcher, périmètre qui s'étend. Source L170–177.
- Conseils de catégorie : un bug et une demande dans le même ticket → le bug est principal ; une connexion impossible à cause d'un bug → Bug ; « ça marchait avant » → Bug. Source L119–126.
- Table de routage par niveau (N1, N2, ingénierie, produit, sécurité, facturation). Source L179–190.
- Violation de données personnelles (pas dans la source) :
  - le responsable du traitement la notifie à l'autorité de contrôle (la CNIL en France) dans les meilleurs délais et si possible dans les 72 h après en avoir pris connaissance, sauf absence de risque. RGPD art. 33 § 1 ;
  - un sous-traitant prévient le responsable du traitement dans les meilleurs délais. RGPD art. 33 § 2 ;
  - toute violation est documentée. RGPD art. 33 § 5 ;
  - si le risque est élevé, les personnes concernées sont informées. RGPD art. 34.
  URL : http://publications.europa.eu/resource/celex/02016R0679-20160504, vérifié 2026-10-16. Conséquence pour le triage : un ticket qui signale des données visibles par un tiers est P1 sécurité, routé aussi vers le DPO ou le juridique, et l'heure de prise de connaissance est notée. Raison : elle fait partir le délai de 72 h. La qualification (données personnelles ou non, rôle de responsable ou de sous-traitant) revient au DPO ; le triage ne la tranche pas.

**Reprises d'Anthropic** : L119–126, L138–168, L170–177, L179–190 (K) ; deux réponses types, Bug et Sécurité (L209–219, L255–265), à adapter : vouvoiement, pas de « Great question! », aucune admission de responsabilité ni hypothèse sur la cause dans la réponse au client. Compléter la ligne `ticket-triage` de `THIRD_PARTY.md`.

**Contraintes à reformuler**
- « When in doubt: raise the priority, do not lower it. » est un doublon de la règle absolue, qui porte déjà la raison : supprimer.
- La liste P1–P4 est rangée sous « Constraints » : la déplacer en « Priority definitions », ce sont des définitions.

**Défauts d'annexe B**
- L'étape 4 vérifie les doublons sans recevoir de base. Correction : ajouter en entrée facultative « recent tickets or known-issues list ». Si elle manque, écrire « doublon non vérifiable — aucune base fournie » et donner les termes de recherche à utiliser (symptôme, client, zone produit ; source L196–199).

**Autres constats**
- `ticket-triage.mystaffy.json` : `enabled: false`, `visibility: internal`, à la différence du reste de la famille. À signaler, sans y toucher.

**Exemple de forme** : non ; les réponses types reprises jouent ce rôle.

**Cas de test**
> « Triage ce ticket, reçu vendredi à 17 h 40 : "Bonjour, depuis la mise à jour de ce matin, quand je me connecte à notre espace client, je vois les factures d'une autre société (raison sociale, adresse, nom du contact, IBAN partiel). Deux collègues voient la même chose. Nous sommes client Premium. Merci de régler ça vite. — Julie, DAF." »

Une bonne sortie contient :
1. Priorité P1, justifiée (données exposées à un tiers, plusieurs utilisateurs, depuis une mise à jour).
2. Catégorie Sécurité en principal, Bug (régression probable) en secondaire, la cause étant étiquetée hypothèse.
3. Un routage vers la sécurité et l'ingénierie, plus le DPO ou le juridique.
4. La possible violation de données personnelles signalée (nom du contact), avec le délai de 72 h à partir de la prise de connaissance, l'heure de réception notée, et la qualification renvoyée au DPO (responsable ou sous-traitant). *(échoue probablement)*
5. Le délai de première réponse P1 (1 h) donné comme défaut à remplacer par celui de l'organisation. *(échoue probablement)*
6. Aucun doublon affirmé ; la mention « aucune base fournie » ; la remarque que d'autres clients sont probablement touchés depuis la mise à jour, ce qui déclenche une montée. *(échoue probablement)*
7. Une réponse au client qui accuse réception, annonce l'escalade et un délai de retour, sans hypothèse sur la cause ni admission de responsabilité.
8. Aucune demande de captures d'écran des factures de l'autre société, qui propageraient la fuite. Au besoin, demander de ne pas diffuser ni télécharger ces documents.
9. Une note interne qui propose d'envisager un retour arrière de la mise à jour.
