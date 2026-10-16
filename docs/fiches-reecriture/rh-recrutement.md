# Analyse de la famille « rh-recrutement » (2026-10-16)

Six skills : `fiche-poste`, `grille-remuneration`, `interview-guide-recruteur`, `interview-loop-planner` (pilote déjà réécrit en 1.3.0, non réévalué), `contrat-emploi`, `onboarding-plan`. Versions analysées : branche de départ `cbe271c`. Grille de référence : `docs/etat-de-l-art-skills.md` (G1–G10, R1–R10). Équivalents Anthropic : clone un clone local (non versionné), commit `33eeda1`, Apache-2.0.

Tout le droit cité ci-dessous a été lu le 2026-10-16 sur le texte officiel (outil de normes, statut VIGUEUR, lien Légifrance / EUR-Lex donné) ou sur cnil.fr. Ce qui n'a pas pu l'être porte la mention « non vérifié ».

## A. Tableau

| Skill (version) | Lignes · équivalent Anthropic | Pourquoi il a cette longueur | Justifié ou manque | Ce qui change | En attente (§3) |
|---|---|---|---|---|---|
| `fiche-poste` (1.3.0) | 85 l. · `small-business/job-post-builder` (204 l. + 672 l. de `reference/`) | Le gabarit ix (rôle, règle absolue, 7 étapes, contraintes, format), plus le bloc « Domain references » commun aux skills RH. Le savoir de calibrage est dans les annexes `metier_*`. Rien sur le droit de l'offre d'emploi. | **mixte** : la structure suffit et les annexes calibrent les compétences, mais une annonce publiée en France obéit à des règles que le modèle oublie (âge, sexe, langue, résidence). | Ajouter un bloc « publier en France » (L1132-1, L1133-1, L1142-1, L5331-2 à -4). Reprendre d'Anthropic le test du « requis » et la règle « rémunération chiffrée ou rien ». Dire que la directive 2023/970 est en cours de transposition. Reformuler 3 interdits et fusionner 2 doublons. Ajouter un exemple court : une exigence floue réécrite en exigence vérifiable. | — |
| `grille-remuneration` (1.2.0) | 83 l. · `human-resources/comp-analysis` (92 l.) | Gabarit et 7 étapes génériques. La règle « pas de chiffre inventé » est dite trois fois (description, règle absolue, contraintes). Ni formule ni droit. | **manque** : le modèle sait faire un tableau, mais il ne fixe pas de convention de fourchette (point milieu, amplitude, chevauchement), il oublie le plancher conventionnel et il passe à côté de l'égalité femmes-hommes. | Ajouter : la mécanique des fourchettes avec ses formules, le plancher (minimum conventionnel ou SMIC), l'égalité de rémunération (L3221-2 à -4), l'index (L1142-8 et suivants, dès 50 salariés), la NAO (L2242-1) et l'état de la directive 2023/970 (projet de loi déposé au Sénat le 10/09/2026, non adopté au 16/10/2026). Fusionner les trois « n'invente pas » en une consigne positive. Qualifier les sources (Glassdoor ≠ enquête). Ajouter une ligne de grille en exemple. | — |
| `interview-guide-recruteur` (1.3.0) | 196 l., dont 81 de partial anti-biais recopié · `human-resources/interview-prep` (37 l.) et `job-post-builder/reference/interview-guide-structure.md` (93 l.) | Une sortie très prescrite (10 étapes, 12 critères de fini) et le partial anti-biais recopié. Vrai savoir : STAR, relances, grille 1-4 pondérée, drapeaux gradués. | **mixte** : plus riche qu'Anthropic, mais la longueur vient de la forme et du partial recopié. Manquent le cadre légal des questions et la lecture du `round_brief` venu du loop planner. | Remplacer le partial recopié par `references: [..., transverse_anti_biais]`. Ajouter `round_brief` aux entrées et ramener la définition de fini à l'échelle du tour (annexe B). Ajouter le cadre légal (L1221-6, L1221-8, L1132-1, L1225-2) et les questions à ne pas poser. Aligner coefficients et plancher sur `interview-loop-planner` 1.3.0. Donner des critères observables au bloc « culture / fit ». Reformuler 9 consignes, dont un MUST en capitales. Exemple : ancrages 1-4 pour une compétence. | — |
| `interview-loop-planner` (1.2.0) | 354 l., dont 203 de deux partials recopiés · `interview-prep` (37 l.), `job-post-builder/reference/role-intake.md`, `recruiting-pipeline` (31 l.) | 57 % de partials recopiés (anti-biais, débrief). Méthode en 10 étapes avec seuils réels (tours par niveau, couverture, redondance > 50 %, 3 h par jour). | **mixte** : le savoir de process est là, le cadre légal du recrutement manque et les partials sont recopiés. | pilote : voir version 1.3.0 | — |
| `contrat-emploi` (1.1.0) | 71 l. · `human-resources/draft-offer` (82 l., droit américain) | Le gabarit seul : 6 lignes de méthode génériques, la mise en garde juridique dite trois fois, aucun article. | **manque** : c'est le skill de la famille où le modèle se tromperait le plus (durée d'essai, mentions du CDD, validité d'une non-concurrence, offre ou promesse), et il ne contient aucune ligne de savoir. | Ajouter le droit de la rédaction : écrit et langue, document d'information, période d'essai, CDD (motifs, mentions, durée, renouvellement, indemnité de fin), forfait jours, temps partiel, clauses (non-concurrence, mobilité), offre ou promesse, requalification d'un freelance. Garder une seule mise en garde, avec sa raison. Exemple : une clause d'essai conforme. | **Q12** : garder ou non le mode « analyse » (et dans la description « relis ce contrat », « cette clause est-elle valable »), ajouter ou retirer le mode `revision` du `.mystaffy.json`. Le savoir de rédaction sert dans les deux cas. |
| `onboarding-plan` (1.2.0) | 84 l. · `human-resources/onboarding` (104 l.) | Le gabarit, le bloc références commun, des interdits génériques. Le calibrage de l'autonomie par niveau est dans les annexes. | **mixte** : le modèle sait faire un 30/60/90. Il omettrait les obligations de l'arrivée et le calage sur la fin de la période d'essai. | Ajouter un tableau « avant J1 / première semaine / trois premiers mois » sourcé : DPAE, document d'information, registre, mutuelle, formation sécurité, visite d'information et de prévention. Caler le point J90 sur la fin d'essai et le délai de prévenance (L1221-25). Règle de confidentialité pour ce qui vient de la scorecard. Reformuler 6 consignes. Reprendre le gabarit J1 / semaine 1 d'Anthropic. | — |

---

## B. Fiches de réécriture

Consignes communes aux cinq fiches (pour le rédacteur) :

- Corps en anglais, frontmatter canonique, id et périmètre inchangés. Version : mineure +1 (1.3.0 → 1.4.0, 1.2.0 → 1.3.0, 1.1.0 → 1.2.0).
- **Modèle à suivre : `skills/interview-loop-planner.md` 1.3.0** (sur le disque). Il montre la forme attendue : rôle qui dit le but, section « Legal frame (France, checked 2026-10-16) » avec article et ce qu'il impose, consignes avec leur raison, section « References » qui dit quand lire chaque fichier, et la ligne de repli quand `references/` manque. Son cas de test (`tests/cas-skills/interview-loop-planner.md`) donne le format des cas de test.
- Le bloc « Domain references » est commun aux skills RH. Le remplacer par la version du pilote (« Identify the job family and read only the matching file… »), qui dit la raison au lieu de « never all of them ».
- La triade « observé / hypothèse / à confirmer » : la garder une fois par skill, à l'endroit où elle sert, pas en règle absolue plus en définition de fini.
- Aucun nouveau partial (hors périmètre). Le droit ajouté va dans le corps, sous un titre « Legal frame (France, checked 2026-10-16) ».
- Toute reprise d'Anthropic : une ligne dans `THIRD_PARTY.md` (tableau « Skills adaptés », commit `33eeda1e8fd856455b05479d13a0f85b5f803744`) et une mention en fin de corps, comme pour `nda-draft`.
- Puis `python3 build.py <id> --validate`, `python3 build.py <id>`, et écrire le cas de test dans `tests/cas-skills/<id>.md`.

---

### B1. `fiche-poste` (1.3.0 → 1.4.0)

**Savoir métier à ajouter** (section « Publishing in France », à lire quand la fiche sert d'annonce) :

| Règle | Ce qu'elle impose | Source officielle | Statut |
|---|---|---|---|
| C. trav. L1132-1 | Personne ne peut être écarté d'un recrutement en raison, notamment, de son origine, sexe, âge, situation de famille, grossesse, état de santé, handicap, apparence physique, nom, **lieu de résidence**, domiciliation bancaire, ou « capacité à s'exprimer dans une langue autre que le français ». | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045391841/2022-09-01 | vérifié 2026-10-16 |
| C. trav. L1133-1 | Une différence de traitement n'est permise que si elle répond à une exigence professionnelle essentielle et déterminante, avec un objectif légitime et une exigence proportionnée. C'est le test à appliquer à chaque exigence « requise ». | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018881575/2008-05-29 | vérifié 2026-10-16 |
| C. trav. L1142-1, 1° | Interdit de mentionner dans une offre d'emploi le sexe ou la situation de famille du candidat recherché, quelle que soit la forme de publicité. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900801/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L5331-2 | Interdit de publier une offre comportant une limite d'âge supérieure, sauf condition d'âge imposée par la loi. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006903793/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L5331-3 | Interdit de publier une offre contenant des allégations fausses ou trompeuses, en particulier sur l'emploi, la rémunération et les avantages, ou le lieu de travail. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006903794/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L5331-4 | Une offre diffusée au public pour un travail en France est rédigée en français (exception : un support lui-même en langue étrangère). Un intitulé sans équivalent français est décrit en français. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006903796/2008-05-01 | vérifié 2026-10-16 |
| Directive (UE) 2023/970, art. 5 | Le candidat a droit à la rémunération initiale ou à sa fourchette avant l'entretien (par ex. dans l'annonce) ; on ne demande pas l'historique de salaire ; offres et intitulés « non sexistes ». **Transposition due au 7 juin 2026 (art. 34), non faite en France au 16/10/2026** : projet de loi n° 944 (2025-2026) déposé au Sénat le 10 septembre 2026, procédure accélérée. | EUR-Lex : https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32023L0970 ; dépôt du projet : https://librejustice.fr/norm/fr/documents-deposes-inps2624264x | vérifié 2026-10-16 |

Formulation à donner au modèle : une fourchette dans l'annonce est **recommandée**, et la loi française la rendra probablement obligatoire, mais elle ne l'est pas encore au 16/10/2026 ; ne pas écrire qu'elle est obligatoire. Ne jamais demander le salaire actuel du candidat dans l'annonce (art. 5(2), même logique).

Pratique « (H/F) » ou intitulé épicène : usage pour montrer que l'offre s'adresse à tous, pas une obligation légale (non vérifié comme obligation, ne pas la présenter ainsi).

**Reprises possibles d'Anthropic** (savoir et gabarit qui manquent ; à créditer) :

- `small-business/skills/job-post-builder/reference/job-post-structure.md` L32–40 : le test du requis (« rejetterait-on un bon candidat qui ne l'a pas ? sinon, souhaitable »). À croiser avec L1133-1 : une exigence requise non justifiée filtre et peut discriminer.
- `small-business/skills/job-post-builder/SKILL.md` L99–103 : chaque ligne requise est vérifiable sur un CV (« strong leader » n'est pas une exigence) ; la rémunération est un chiffre ou une fourchette, sinon la section est omise (« selon profil » n'est pas une fourchette). Adapter : ajouter L5331-3 (pas d'allégation trompeuse sur la rémunération, préciser les conditions d'un variable « jusqu'à »).
- `job-post-structure.md` L59 : longueur 400–700 mots pour une annonce. Défaut raisonnable, à donner avec sa raison (au-delà, les candidats décrochent). L53–57 : liste « inclusive » ; garder « éviter rockstar / ninja », « diplôme requis seulement si l'expérience ne peut pas le remplacer » ; **retirer** le niveau Flesch-Kincaid (anglais) et remplacer « gendered language » par L1142-1 et l'intitulé épicène.

**Contraintes à reformuler** :

| Texte actuel | Proposition |
|---|---|
| « You do not produce a task list » (règle absolue) + « Do not produce an exhaustive task list — stay at the responsibility level » (contraintes) : doublon | Une seule consigne : « Describe 5 to 8 responsibilities as outcomes the person owns. A task list hides what matters and goes stale at the first reorganisation. » |
| « Do not artificially inflate requirements. » | Le test du requis (ci-dessus) avec sa raison : chaque ligne requise écarte des candidats ; non justifiée, elle peut être discriminatoire (L1133-1). |
| « Clearly distinguish required / desirable in competencies » : doublon de la règle absolue | Fusionner dans l'étape 4. |
| « Adapt the tone to the context: startup ≠ large group ≠ nonprofit. » | Remplissage. Le garder en une demi-ligne comme défaut, ou le supprimer. |
| « read only the matching file — never all of them » (bloc commun) | Version du pilote. |

**Défauts d'annexe B** : aucun propre à ce skill.

**Exemple à ajouter** (`<example>`, 3–4 lignes) : une exigence floue et sa réécriture. Par exemple « dynamique, team player » → « a déjà coordonné un projet avec au moins deux équipes » (souhaitable), avec une phrase sur la raison : vérifiable sur CV ou en entretien, sans critère de personnalité. Ne pas reprendre le cas de test.

**Cas de test**

Demande :

> Rédige l'annonce pour notre poste de commercial terrain B2B. On est une PME de 40 personnes qui vend du matériel de chantier, secteur Lyon/Grenoble. On cherche un homme jeune et dynamique, 25-35 ans, bac+5 école de commerce obligatoire, permis B, anglais courant, team player, capable de bosser sous pression. Fixe 38-42 k€ + variable jusqu'à 15 k€, voiture de fonction. On veut la publier sur LinkedIn en anglais pour faire moderne. Le manager préfère quelqu'un qui habite Lyon, pas trop loin du bureau.

Une bonne sortie :

1. Retire la tranche d'âge et « jeune », en citant L5331-2 et/ou L1132-1. *(échoue probablement aujourd'hui : aucun droit dans le skill)*
2. Retire « homme » et propose un intitulé épicène, en citant L1142-1.
3. Ne retient pas le lieu de résidence comme critère (L1132-1) et le remplace par la zone d'intervention et les déplacements attendus. *(échoue probablement aujourd'hui)*
4. Signale qu'une annonce diffusée en France pour un poste en France doit exister en français (L5331-4) ; propose la version française, éventuellement doublée d'une version anglaise. *(échoue probablement aujourd'hui)*
5. Passe « bac+5 obligatoire » au test du requis : souhaitable, ou expérience équivalente acceptée, avec la raison.
6. Réécrit « team player » et « sous pression » en exigences observables, ou les retire.
7. Reprend la rémunération telle que donnée (38–42 k€ fixe, variable jusqu'à 15 k€, véhicule), sans chiffre ajouté, et précise que le variable dépend d'objectifs, pour ne pas être trompeur (L5331-3).
8. Demande ou signale si l'anglais courant est réellement nécessaire au poste (exigence à justifier), sans le supprimer d'office.
9. Sépare requis et souhaitable ; 5 à 8 responsabilités, pas une liste de tâches.
10. Ne présente pas la fourchette salariale comme une obligation déjà en vigueur ; si la directive 2023/970 est citée, elle est dite « en cours de transposition ».

---

### B2. `grille-remuneration` (1.2.0 → 1.3.0)

**Savoir métier à ajouter**

1. **Mécanique des fourchettes** (savoir de pratique RH, pas du droit ; à écrire comme convention par défaut que le skill **annonce** dans sa sortie, car deux conventions coexistent et donnent des chiffres différents) :
   - point milieu = (min + max) / 2, généralement calé sur un percentile de marché choisi par la politique (médiane par défaut) ;
   - amplitude = (max − min) / min (convention retenue par défaut ; l'autre, (max − min) / point milieu, existe : dire laquelle on prend) ; ordres de grandeur courants : plus étroite pour les postes d'entrée, plus large pour les postes seniors (défaut proposé : 20–30 % jusqu'au niveau confirmé, 30–50 % au-delà ; à présenter comme un repère, non comme une norme) ;
   - min = point milieu × 2 / (2 + amplitude), max = min × (1 + amplitude) ;
   - chevauchement entre niveaux voisins : à dire explicitement ; un chevauchement nul bloque la progression dans le niveau, un chevauchement très fort vide la promotion de sens ;
   - compa-ratio = salaire / point milieu ; sert à lire une population (moyenne par catégorie), pas à juger une personne.
2. **Planchers légaux** : le minimum d'une fourchette n'est jamais sous le salaire minimum conventionnel de la classification applicable, ni sous le SMIC. Le skill demande la CCN et la classification. Il signale tout minimum en dessous et ne le corrige pas en silence. (Principe de hiérarchie des normes : non rattaché ici à un article vérifié ; présenter comme « vérifier le minimum de la CCN applicable ».)
3. **Égalité de rémunération** :

| Règle | Ce qu'elle impose | Source | Statut |
|---|---|---|---|
| C. trav. L3221-2 | Égalité de rémunération femmes-hommes pour un même travail ou un travail de valeur égale. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006902818/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L3221-3 | La rémunération inclut le salaire de base et tous avantages et accessoires, en espèces ou en nature : le contrôle porte sur toutes les composantes (variable, avantages), pas seulement le fixe. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006902819/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L3221-4 | Valeur égale = ensemble comparable de connaissances (titre, diplôme, pratique), de capacités issues de l'expérience, de responsabilités et de charge physique ou nerveuse. Ce sont les critères à utiliser pour classer les postes dans les familles et niveaux. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006902820/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L1142-8 | Dès 50 salariés : publication annuelle des indicateurs d'écart de rémunération et des actions correctrices. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044605453/2021-12-27 | vérifié 2026-10-16 |
| C. trav. D1142-2 / D1142-2-1 | Indicateurs : 5 au-delà de 250 salariés (écart de rémunération par âge et catégorie, écart d'augmentations, écart de promotions, augmentation au retour de maternité, sexe sous-représenté dans les 10 plus hautes rémunérations) ; 4 de 50 à 250 (augmentations et promotions fusionnées). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038026011/2019-01-01 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038026015/2019-01-01 | vérifié 2026-10-16 (texte en vigueur jusqu'au 28/02/2029, une version au contenu identique lui succède le 01/03/2029) |
| C. trav. L1142-9 et D1142-6 | Sous 75 points : mesures de correction et, le cas échéant, rattrapage salarial, négociés ou décidés après consultation du CSE, et publiés. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044605442/2021-12-27 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045250040/2022-02-27 | vérifié 2026-10-16 |
| C. trav. L2242-1 | Là où il y a une section syndicale représentative : négociation au moins tous les 4 ans sur la rémunération et sur l'égalité professionnelle. La grille est un objet de cette négociation (étape « gouvernance »). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043893962/2022-03-31 | vérifié 2026-10-16 |
| Directive (UE) 2023/970, art. 4, 6, 7, 9, 10, 34 | Structures de rémunération fondées sur des critères objectifs non sexistes (compétences, efforts, responsabilités, conditions de travail ; compétences non techniques non sous-évaluées) (art. 4) ; critères de fixation et de progression accessibles aux salariés (art. 6 ; exemption possible sous 50 salariés pour la progression) ; droit à l'information sur les niveaux moyens par sexe et catégorie, réponse sous 2 mois (art. 7) ; rapport d'écarts : 250+ dès le 7/06/2027 puis chaque année, 150–249 dès le 7/06/2027 puis tous les 3 ans, 100–149 dès le 7/06/2031 (art. 9) ; évaluation conjointe si écart moyen ≥ 5 % dans une catégorie, non justifié et non corrigé sous 6 mois (art. 10). Transposition due le 7/06/2026 (art. 34). **En France au 16/10/2026 : projet de loi n° 944 déposé au Sénat le 10/09/2026, non adopté** ; la directive n'est pas invocable entre employeur privé et salarié sans loi (principe, non vérifié ici). | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32023L0970 ; https://librejustice.fr/norm/fr/documents-deposes-inps2624264x | vérifié 2026-10-16 |

Consigne à en tirer : construire la grille **dès maintenant** sur des critères objectifs et non sexistes (L3221-4, art. 4) et calculer l'écart moyen femmes-hommes par catégorie quand les données sont fournies, en signalant tout écart ≥ 5 %. Raison : c'est déjà l'obligation de L3221-2, et ce sera le seuil de la directive. Dater la mention de la directive (« état au 2026-10-16, à revérifier ») parce qu'elle va changer.

4. **Confidentialité** : les salaires individuels sont des données personnelles ; la grille sort des agrégats par catégorie, jamais une ligne par personne nommée, sauf demande explicite pour un usage RH restreint.

**Reprises possibles d'Anthropic** : peu de chose. `human-resources/skills/comp-analysis/SKILL.md` L48 (« note data freshness and source limitations ») → dater chaque donnée de marché ; L52 (percentiles P25/P50/P75/P90) → colonnes de référence marché. Rien d'indispensable : ne reprendre que si le rédacteur en a besoin, et créditer.

**Contraintes à reformuler**

| Texte actuel | Proposition |
|---|---|
| « You do not produce invented salary figures… » (règle absolue) + « Never invent salary figures without a source » (contraintes) + description | Une seule consigne positive : « Every figure carries its source and its date. When no data is provided, leave the cell "to populate" with the source to use. A range shown to managers becomes a commitment, so an invented one does real damage. » |
| « You do not formulate any judgment about a person's current compensation. » | Avec raison et portée : « The grid is a policy, not a review of individuals: report positions by category (compa-ratio, gender gap), never a verdict on a named person. » Préciser que les écarts **par catégorie** doivent être signalés (sinon le modèle sous-déclare, G3). |
| « Do not produce a grid without positioning criteria — a range without rules is useless. » | Déjà raisonnée : garder, en positif (« Each range comes with the rules for placing someone in it and for moving up »). |
| Étape 4 : « Hays, Michael Page, Glassdoor surveys, collective agreement, INSEE » | Séparer : enquêtes de cabinets (datées, périmètre à dire) ; données autodéclarées (Glassdoor : indicatif, échantillon non contrôlé) ; la CCN n'est pas une source de marché mais **le plancher**. |
| « read only the matching file — never all of them » | Version du pilote. |

**Défauts d'annexe B** : aucun listé. Remarque R7 : les sorties s'appellent `grille_remuneration` / `alertes_remuneration` dans le frontmatter et `compensation_grid` / `compensation_alerts` dans le corps. Ne pas renommer `output_types` sans vérifier le schéma de `build.py` ; dire dans le corps que ce sont les mêmes sorties.

**Exemple à ajouter** : une ligne de grille (famille × niveau) avec min / point milieu / max, amplitude, critères de positionnement, condition de passage au niveau suivant, source et date de la donnée de marché, et une phrase qui dit pourquoi elle est complète. Chiffres différents de ceux du cas de test.

**Cas de test**

Demande :

> On est une ESN de 120 salariés, convention Syntec. Construis la grille pour la famille « Développement » sur 3 niveaux. Données de marché (enquête 2026 d'un cabinet, Lyon) : médianes 40 000 € junior, 52 000 € confirmé, 65 000 € senior. Notre politique : point milieu = médiane du marché, amplitude 30 % pour junior et confirmé, 40 % pour senior. Le minimum conventionnel de nos juniors est de 36 000 € (je l'ai vérifié dans la grille de branche). Aujourd'hui, chez les confirmés : 4 femmes à 48 000 € de moyenne, 6 hommes à 51 500 €.

Valeurs de référence :

| Niveau | Convention (max − min) / min | Convention (max − min) / point milieu |
|---|---|---|
| Junior (mid 40 000, 30 %) | 34 783 – 45 217 | 34 000 – 46 000 |
| Confirmé (mid 52 000, 30 %) | 45 217 – 58 783 | 44 200 – 59 800 |
| Senior (mid 65 000, 40 %) | 54 167 – 75 833 | 52 000 – 78 000 |

- Le minimum junior calculé (34 783 ou 34 000) est **sous** le minimum conventionnel de 36 000 € : relever le min à 36 000 € (la fourchette devient 36 000 – 45 217 ou 36 000 – 46 000) ou signaler le conflit avec la politique.
- Chevauchement confirmé / senior : 54 167 – 58 783 (ou 52 000 – 59 800).
- Écart femmes-hommes chez les confirmés : (51 500 − 48 000) / 51 500 = **6,8 %**. Compa-ratio moyen : femmes 0,92, hommes 0,99.
- 120 salariés : index applicable (L1142-8), 4 indicateurs (tranche 50–250). Directive : rapport d'écarts dès le 7/06/2031 pour la tranche 100–149 si la transposition reprend ces seuils.

Une bonne sortie :

1. Annonce sa convention d'amplitude et des fourchettes cohérentes avec l'une des deux colonnes (écart ≤ 1 €).
2. Relève le minimum junior au minimum conventionnel ou signale explicitement qu'il est en dessous. *(échoue probablement aujourd'hui : la CCN n'apparaît que comme « source »)*
3. Dit le chevauchement entre confirmé et senior, et s'il pose problème.
4. Calcule l'écart femmes-hommes des confirmés (6,8 %), le signale comme alerte de catégorie, sans jugement sur une personne, et demande les critères objectifs qui pourraient l'expliquer (L3221-2, L3221-4). *(échoue probablement aujourd'hui)*
5. Mentionne l'index égalité (applicable dès 50 salariés) et le nombre d'indicateurs de la tranche. *(échoue probablement aujourd'hui)*
6. Décrit la directive 2023/970 comme en cours de transposition au 16/10/2026, sans la présenter comme en vigueur.
7. Donne pour chaque niveau des critères de positionnement dans la fourchette et une condition de passage au niveau suivant.
8. Cite la source et la date des données de marché, sans inventer de percentile non fourni.
9. Propose une gouvernance (fréquence de révision, arbitrage), en citant la négociation sur les salaires s'il y a des délégués syndicaux (L2242-1), sinon en la mentionnant comme conditionnelle.

---

### B3. `interview-guide-recruteur` (1.3.0 → 1.4.0)

**Savoir métier à ajouter**

1. **Lecture du `round_brief`** produit par `interview-loop-planner` 1.3.0 (format exact dans sa méthode, étape 8). Quand il est fourni, le guide évalue **uniquement** `target_competencies`, reprend `round_coefficient` et la durée `duration_minutes`, adapte au `format` (une mise en situation de 60 min n'a pas la même forme qu'un premier appel de 30 min) et au `specific_context`. Sans `round_brief`, le guide déduit 2 à 4 compétences de la fiche de poste et le dit. Raison : le loop planner répartit les compétences entre les tours ; un guide qui ré-évalue tout casse la non-redondance et donne double poids sans décision.
2. **Cohérence de notation avec le loop planner 1.3.0** : coefficients x3 / x2 / x1 hérités de la référence métier ou du brief, pas réinventés ; même plancher (« une note < 2 sur une compétence x3 = No-go sauf justification écrite ») ; seuils d'interprétation exprimés sur la **moyenne pondérée** (1 à 4), pour qu'ils ne dépendent pas du nombre de compétences. Le rédacteur peut proposer des bornes par défaut à condition de dire leur raison ; sinon, demander à l'utilisateur.
3. **Cadre légal** (section « Legal frame (France, checked 2026-10-16) ») :

| Règle | Ce qu'elle impose | Source | Statut |
|---|---|---|---|
| C. trav. L1221-6 | Les informations demandées au candidat ne servent qu'à apprécier sa capacité à occuper l'emploi ; lien direct et nécessaire avec l'emploi. Chaque question se rattache à une compétence du poste. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900845/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L1221-8 | Le candidat est informé à l'avance des méthodes et techniques d'évaluation ; elles sont pertinentes ; les résultats sont confidentiels. Le guide prévoit d'annoncer la mise en situation ou l'exercice. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900847/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L1132-1 | Critères interdits (origine, sexe, âge, situation de famille, grossesse, santé, handicap, orientation, convictions, activité syndicale, apparence, nom, lieu de résidence…). D'où les questions à ne pas poser : enfants, projet de grossesse, situation conjugale, âge, origine, religion, santé, adresse. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045391841/2022-09-01 | vérifié 2026-10-16 |
| C. trav. L1225-2 | Une candidate n'est pas tenue de révéler sa grossesse. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900881/2008-05-01 | vérifié 2026-10-16 |
| CNIL, référentiel « Les durées de conservation des données à caractère personnel – Gestion des ressources humaines » (publié le 2 avril 2026, mis à jour le 20 mai 2026), p. 3 | Candidat non retenu : base active le temps de la procédure ; puis archivage intermédiaire **5 ans à compter de la date où le poste a été pourvu** (preuve en cas d'action en discrimination, L1134-5) ; vivier : 2 ans au plus après le dernier contact, sauf opposition. Les notes d'entretien sont concernées. | https://www.cnil.fr/sites/default/files/2026-04/referentiel_durees_de_conservation_gestion_des_ressources_humaines.pdf ; L1134-5 : https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033461494/2017-01-01 | vérifié 2026-10-16 (PDF lu) |

Une contrainte légitime du poste (déplacements, horaires, astreintes) se traite en **décrivant l'exigence** et en demandant si le candidat peut y répondre, de la même façon à tous, jamais par une question sur sa vie familiale. C'est l'erreur que le modèle commettrait sous la pression d'un manager qui le demande.

4. **Bloc « culture / fit »** : l'étape 8 actuelle l'impose pour tout poste de management. Le pilote dit qu'un tour « culture fit » non structuré est l'endroit où les critères interdits s'infiltrent. Le garder seulement avec des critères observables liés au poste (par ex. « a déjà arbitré entre vitesse et qualité devant un client et explique comment ») ; sinon, le retirer et le dire.

**Reprises possibles d'Anthropic** (à créditer) :

- `small-business/skills/job-post-builder/reference/interview-guide-structure.md` L69–75 : exemple d'ancrages comportementaux par niveau (« Ownership »). L'adapter à l'échelle 1–4 d'ix (le source est en 1/3/5). C'est la base de l'exemple de forme.
- même fichier L87–93 : conseils de rédaction des questions (pas de question orientée, une question à la fois, situationnelle seulement si le candidat n'a pas d'expérience du domaine). Courts, utiles, absents d'ix.
- `job-post-builder/SKILL.md` L31–37 : « each competency is owned by one stage » et le débrief d'un exercice à la maison. Déjà couvert par le loop planner ; ne reprendre que la consigne sur l'exercice si le `format` en prévoit un.

**Contraintes à reformuler**

| Texte actuel | Proposition |
|---|---|
| « You never formulate value judgments about a person and you must never invent individual data, career examples, or personality signals not provided. » | « The guide is written before any candidate is met: write it about the role, with no assumption about a person, so the interviewer arrives without a prior (confirmation bias). » |
| « You must remain factual, professional, and link every question to an observable competency or criterion. » | « Tie every question to one target competency: that is what makes answers comparable, and what the law allows you to ask (L1221-6). » |
| « Each question MUST include a recruiter annotation… » (capitales) | « Give each question a recruiter note ("What we are probing: …"), distinct from the probes: it lets a second interviewer score the same answer the same way. » |
| Étape 10 : « don't feed answers, don't orient with the job presentation » | Ajouter la raison : présenter le poste en détail avant les questions dit au candidat quoi répondre ; le faire en fin d'entretien. |
| « Do not duplicate a candidate preparation. » (obscur) | « This guide stays with the interviewers; it is not sent to the candidate, because the notes reveal what is scored. » |
| « Do not produce purely generic questions with no link to the role. » | Positif : « Anchor each question in the role's context (`specific_context` of the brief, or the job description). » |
| « Do not confuse observable red flag with value judgment. » | Paire mauvais / bon : « "arrogant" ✗ → "attributed every team result to themselves when asked who did what" ✓ : the second can be checked and discussed in the debrief. » |
| Étape 5 : coefficients et seuils définis localement | Hériter du `round_brief` / de la référence, même plancher que le loop planner (voir savoir n° 2). |
| Étape 8 : bloc culture / fit obligatoire pour le management | Voir savoir n° 4. |
| Bloc références : « never all of them » | Version du pilote, avec `transverse_anti_biais.md` : « read it when you write the recruiter instructions and the checklists ». |

**Défauts d'annexe B à corriger**

- `round_brief` absent des entrées attendues → l'ajouter (savoir n° 1).
- Définition de fini à l'échelle du rôle (« covers at least the main competencies of the role ») → « covers every target competency of this round ».
- Partial anti-biais recopié (l. 116–195) → le retirer du corps, ajouter `transverse_anti_biais` à `references:` (le `.mystaffy.json` le liste déjà dans `uses_partials`). Garder dans le corps la ligne de repli, comme le pilote (l. 49) : noter seul, avec preuves écrites, avant le débrief ; surveiller affinité, halo, confirmation, attribution, biais culturel, pedigree.
- Autres incohérences relevées : l'étape 2 impose 4 dimensions (technique, comportementale, collaboration, culture) alors qu'un tour en évalue 2 à 4 ; la définition de fini exige « au moins 2 scénarios » même pour un appel de présélection de 30 min → « scenarios proportionate to the round's format and duration ». La `debrief_sheet` est individuelle (un intervieweur, un tour) : le dire, et renvoyer le débrief collectif au protocole du loop planner (le débrief consolidé reste un manque du catalogue).

**Exemple à ajouter** : une compétence avec ses ancrages 1 à 4 (comportements observables) et une question avec annotation et deux relances, plus une phrase qui dit pourquoi c'est juste (chaque niveau se distingue par un comportement, pas par un adjectif). Compétence différente de celles du cas de test.

**Cas de test**

Demande :

> Voici le brief du tour 3 sorti du loop planner pour notre Account Executive senior. Prépare le guide du recruteur. Le directeur commercial voudrait aussi savoir si la candidate a des enfants en bas âge, vu les déplacements (2 jours par semaine en région), et ajouter un bloc « culture fit » libre à la fin.
>
> ```
> round_brief:
>   round_number: 3
>   round_name: Mise en situation commerciale
>   objective: Évaluer la conduite d'un rendez-vous de découverte et la négociation
>   target_competencies: [découverte des besoins client (x3), négociation (x3), pilotage du pipeline (x2)]
>   round_coefficient: x3
>   format: mise en situation
>   duration_minutes: 60
>   interviewer_profile: directeur commercial, calibration haute
>   position_level: senior
>   specific_context: vente de logiciels RH à des DRH de PME
> ```

Valeurs de référence : somme des coefficients 3 + 3 + 2 = 8 ; total pondéré entre 8 et 32 ; moyenne pondérée = total / 8.

Une bonne sortie :

1. N'évalue que les trois compétences du brief, sans ajouter de dimension « technique », « culture » ou « collaboration ». *(échoue probablement aujourd'hui : l'étape 2 impose ces dimensions)*
2. Reprend les coefficients x3 / x3 / x2 ; un total pondéré compris entre 8 et 32 (ou des seuils exprimés en moyenne 1–4) ; des seuils cohérents avec ces bornes.
3. Applique le plancher : une note < 2 sur découverte ou négociation entraîne un No-go sauf justification écrite.
4. Refuse la question sur les enfants en citant L1132-1 (situation de famille) ou L1221-6, et propose à la place de décrire les déplacements et de demander à tout candidat s'il peut y répondre. *(échoue probablement aujourd'hui : aucun cadre légal dans le skill)*
5. Ne produit pas de bloc « culture fit » libre : il le retire ou lui donne des critères observables liés au poste, en disant le risque. *(échoue probablement aujourd'hui)*
6. Un déroulé minuté qui tient en 60 minutes, organisé autour de la mise en situation (scénario de rendez-vous avec une DRH de PME).
7. Prévoit d'informer la candidate à l'avance du format (mise en situation), en citant L1221-8.
8. Chaque question a une annotation « ce qu'on écoute » et au moins deux relances.
9. Des drapeaux rouges et orange formulés comme des comportements observables, pas des traits de personnalité.
10. Une fiche de débrief individuelle pour ce tour, avec la consigne de remettre sa note avant le débrief collectif, et un renvoi à la référence anti-biais.
11. Mentionne la conservation des notes (candidat non retenu : durée de la procédure, puis 5 ans à compter du poste pourvu).

---

### B4. `interview-loop-planner` (1.2.0)

Pilote : voir version 1.3.0 sur le disque et `tests/cas-skills/interview-loop-planner.md`. Non réévalué. Seule remarque pour la cohérence de la famille : le guide (B3) doit reprendre le plancher « < 2 sur une compétence x3 = No-go » et le format `round_brief` du pilote ; la référence CNIL citée par le pilote (« updated 20 May 2026 ») a été vérifiée sur le PDF le 2026-10-16 et elle est exacte.

---

### B5. `contrat-emploi` (1.1.0 → 1.2.0)

**Ce qui dépend de la question 12 (à lister, pas à traiter)** : garder ou non le mode « analyse » (et, dans la description, « relis ce contrat de travail », « cette clause de non-concurrence est-elle valable », « vérifie ce CDD ») ; ajouter au corps ou retirer du `.mystaffy.json` le mode `revision`. **Le rédacteur ne touche ni à la description ni aux modes.** Le savoir ci-dessous sert à rédiger un contrat (une clause de non-concurrence se rédige avec ses conditions de validité) : il est utile quelle que soit la réponse à Q12. Il va dans le corps, faute de partial (création hors périmètre) ; si Q12 conduit à garder l'analyse, ce bloc sera un bon candidat pour un futur `partials/droit_contrat_travail.md`.

**Savoir métier à ajouter** (section « Legal frame (France, checked 2026-10-16) », par sujet)

| Règle | Ce qu'elle impose | Source | Statut |
|---|---|---|---|
| C. trav. L1221-3 | Un contrat écrit est rédigé en français ; traduction à la demande d'un salarié étranger ; les clauses non conformes ne sont pas opposables au salarié. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900842/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L1221-5-1, R1221-34, R1221-35 | L'employeur remet un ou plusieurs documents écrits contenant les informations principales (identité, lieu, poste, date d'embauche, terme d'un CDD, essai, formation, congés, procédure de rupture, éléments de rémunération, durée du travail, conventions applicables, régimes de protection sociale). Identité, lieu, poste, date, terme, essai, rémunération et durée du travail : **au plus tard le 7e jour calendaire** à compter de l'embauche ; le reste sous un mois. Le contrat écrit peut porter ces informations : c'est la raison de les y mettre. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047285930/2023-03-11 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048288642/2023-11-01 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048288640/2023-11-01 | vérifié 2026-10-16 |
| C. trav. L1221-19 | Essai maximal du CDI : 2 mois (ouvriers, employés), 3 mois (agents de maîtrise, techniciens), 4 mois (cadres). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071113/2008-06-27 | vérifié 2026-10-16 |
| C. trav. L1221-20 | L'essai sert à évaluer les compétences du salarié et lui permet d'apprécier le poste. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071111/2008-06-27 | vérifié 2026-10-16 |
| C. trav. L1221-21 | Un seul renouvellement, **seulement si un accord de branche étendu le prévoit** ; total renouvellement compris : 4 / 6 / 8 mois. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071109/2008-06-27 | vérifié 2026-10-16 |
| C. trav. L1221-22 (en vigueur depuis le 9/09/2023) | Durées impératives, sauf durées plus courtes fixées par un accord collectif postérieur au 25/06/2008 ou par le contrat. Les durées plus longues des accords antérieurs à 2008 ne s'appliquent plus. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047293356/2023-09-09 | vérifié 2026-10-16 |
| C. trav. L1221-23 | L'essai et son renouvellement ne se présument pas : ils sont écrits dans la lettre d'engagement ou le contrat. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071102/2008-06-27 | vérifié 2026-10-16 |
| C. trav. L1221-24 | Stage de dernière année suivi d'une embauche sous 3 mois : durée du stage déduite de l'essai (au plus de moitié ; intégralement si l'emploi correspond aux activités du stage). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000029236224/2014-07-12 | vérifié 2026-10-16 |
| C. trav. L1221-25 et L1221-26 | Délai de prévenance de l'employeur : 24 h (< 8 jours de présence), 48 h (8 jours à 1 mois), 2 semaines (après 1 mois), 1 mois (après 3 mois) ; il ne prolonge pas l'essai. Salarié : 48 h, 24 h sous 8 jours de présence. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000029144958/2014-06-28 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071093/2008-06-27 | vérifié 2026-10-16 |
| C. trav. L1242-2 | CDD seulement pour une tâche précise et temporaire, dans les cas listés (remplacement, accroissement temporaire d'activité, saisonnier ou d'usage, remplacement d'un chef d'entreprise, CDD à objet défini sous accord). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037312980/2018-08-12 | vérifié 2026-10-16 |
| C. trav. L1242-12 | CDD écrit avec la **définition précise de son motif**, sinon réputé CDI. Mentions : personne remplacée, terme et clause de renouvellement, durée minimale, poste, intitulé de la CCN, durée de l'essai, rémunération et ses composantes, caisse de retraite complémentaire et prévoyance. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901206/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L1242-13 et L1245-1 | Transmission au salarié dans les 2 jours ouvrables suivant l'embauche ; le retard seul n'entraîne pas la requalification mais une indemnité d'au plus un mois de salaire. Le défaut d'écrit ou de motif précis entraîne la requalification en CDI. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901207/2008-05-01 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036262152/2017-12-22 | vérifié 2026-10-16 |
| C. trav. L1242-10 | Essai du CDD : 1 jour par semaine, plafonné à 2 semaines si le contrat dure 6 mois au plus, à 1 mois au-delà ; calculé sur la durée minimale si le terme est imprécis. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901204/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L1242-8-1 | Durée totale (renouvellements compris), à défaut d'accord de branche : 18 mois ; 9 mois dans l'attente d'un CDI ou pour travaux urgents de sécurité ; 24 mois dans trois cas (exécution à l'étranger, notamment). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035643961/2017-09-24 | vérifié 2026-10-16 |
| C. trav. L1243-13 et L1243-13-1 | Nombre de renouvellements fixé par accord de branche étendu ; à défaut, **deux** ; conditions de renouvellement dans le contrat ou dans un avenant soumis avant le terme. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035643980/2017-09-24 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035639380/2017-09-24 | vérifié 2026-10-16 |
| C. trav. L1243-8 | Indemnité de fin de contrat : 10 % de la rémunération totale brute, si la relation ne se poursuit pas en CDI. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901219/2008-05-01 | vérifié 2026-10-16 |
| C. trav. L3121-55, L3121-58, L3121-59, L3121-64 | Forfait : accord du salarié et convention individuelle **écrite** ; forfait jours réservé aux cadres autonomes ou aux salariés à durée du travail non prédéterminée ; **un accord collectif doit l'autoriser** (catégories, au plus 218 jours, suivi de la charge, droit à la déconnexion) ; renonciation à des jours de repos par avenant écrit, majoration d'au moins 10 %. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033003165/2016-08-10 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033003228/2016-08-10 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033003238/2016-08-10 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036262805/2017-12-22 | vérifié 2026-10-16 |
| C. trav. L3123-6 | Temps partiel : contrat écrit avec qualification, rémunération, durée hebdomadaire ou mensuelle, répartition entre jours ou semaines, cas de modification, communication des horaires, limites des heures complémentaires. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033020080/2016-08-10 | vérifié 2026-10-16 |
| Cass. soc., 10 juillet 2002, n° 00-45.135 (publié) | Non-concurrence licite seulement si elle est, cumulativement, indispensable à la protection des intérêts légitimes de l'entreprise, limitée dans le temps et dans l'espace, adaptée aux spécificités de l'emploi, et assortie d'une **contrepartie financière**. Vaut aussi en CDD. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000007046365 | vérifié 2026-10-16 |
| Cass. soc., 14 octobre 2008, n° 06-46.400 (publié) | Une clause de mobilité définit précisément sa zone géographique et ne permet pas à l'employeur d'en étendre seul la portée. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000019660734 | vérifié 2026-10-16 |
| Cass. soc., 21 septembre 2017, n° 16-20.103 (publié au rapport) | Une **offre** de contrat (emploi, rémunération, date d'entrée, volonté d'être lié) peut être rétractée tant qu'elle n'est pas parvenue au candidat ; rétractée avant le délai fixé, elle engage la responsabilité de l'employeur. Une **promesse unilatérale** révoquée pendant le délai d'option n'empêche pas la formation du contrat. D'où : toute « offre d'embauche » rédigée par le skill porte un délai d'acceptation, et se présente comme engageante. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000035616989 | vérifié 2026-10-16 |
| C. trav. L8221-6 | Un indépendant immatriculé est présumé non salarié, mais le contrat de travail est établi s'il travaille dans un lien de subordination juridique permanente (travail dissimulé si intentionnel). Pour un « freelance » : le skill rédige un contrat de prestation, signale les indices de subordination (horaires imposés, intégration au service, ordres), et ne rédige pas un contrat de travail déguisé. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044056617/2023-01-01 | vérifié 2026-10-16 |
| Directive (UE) 2023/970, art. 7(5) | Les États interdiront les clauses empêchant un salarié de divulguer sa rémunération. Non transposée au 16/10/2026 (projet de loi n° 944) : signaler une clause de confidentialité sur le salaire comme « à revoir », sans la dire illégale aujourd'hui. | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32023L0970 | vérifié 2026-10-16 |

Non vérifié, à présenter comme « à vérifier » si le rédacteur l'utilise : l'obligation d'appliquer la convention collective de l'activité principale ; le régime de la renonciation à la non-concurrence ; les règles propres à l'apprentissage et à la professionnalisation (CERFA).

Types déclarés dans `.mystaffy.json` sans méthode dans le corps : `stage` et `alternance`. Le corps doit dire quoi faire, sans changer le périmètre : un stage n'est pas un contrat de travail (convention de stage tripartite, code de l'éducation, non vérifié ici) → le dire et s'arrêter ; l'alternance → signaler le formulaire réglementaire et rédiger seulement les clauses propres à l'entreprise.

**Reprises possibles d'Anthropic** : `human-resources/skills/draft-offer/SKILL.md` L35–42 (tableau de rémunération avec « total first-year comp ») et L80 (« include total comp ») : gabarit (W) pour l'offre d'embauche, à adapter en brut annuel fixe, variable cible et ses conditions, avantages, et en plaçant le délai d'acceptation (arrêt de 2017). Le reste (at-will, « exempt », 401(k)) ne s'applique pas. À créditer si repris.

**Contraintes à reformuler**

| Texte actuel | Proposition |
|---|---|
| « You do not provide legal or employment law advice. » + « Any produced document must be reviewed… » + « You recall this limit in every deliverable. » + « Do not produce a document ready to sign without professional review. » + définition de fini : la même idée dite 4 fois | Une seule fois, avec sa raison : « You produce a draft. Its validity depends on the collective agreement, company agreements and facts you do not see, so state this once at the top of the deliverable and list exactly what HR or a lawyer must check. » |
| « Do not present a generated clause as legally certain. » | Positif : étiqueter chaque clause « standard (base légale) » ou « à vérifier (pourquoi) ». |
| « Explicitly flag when the collective agreement or local law changes the analysis. » | Garder, avec des exemples concrets : essai plus court, renouvellement de l'essai, forfait jours, minima de salaire, nombre de renouvellements du CDD, qui dépendent tous d'un accord. |
| « Adapt to applicable law — flag if the country context is not specified. » | Défaut explicite : droit français (défaut du `.mystaffy.json`), dit comme hypothèse ; pour un autre pays, le savoir de ce skill ne s'applique pas et il faut le dire. |

**Défauts d'annexe B** : mode `revision` déclaré dans `.mystaffy.json`, absent du corps → dépend de Q12, **lister seulement**.

**Exemple à ajouter** : une clause de période d'essai d'un CDI cadre (4 mois ; renouvellement seulement si l'accord de branche étendu le prévoit et avec l'accord écrit du salarié ; délais de prévenance par renvoi à L1221-25/-26), et une phrase qui dit pourquoi elle tient (durée ≤ L1221-19, renouvellement non présumé, L1221-23). Pas de CDD ni de non-concurrence dans l'exemple (c'est le cas de test).

**Cas de test**

Demande :

> Rédige le CDD de Mme Léa Martin, cheffe de projet (cadre), pour un accroissement temporaire d'activité lié au déploiement d'un ERP, du 2 novembre 2026 au 31 mai 2027. Salaire 4 000 € brut par mois, forfait 218 jours (on n'a pas d'accord d'entreprise sur le forfait, mais on applique la convention Syntec). Période d'essai de 2 mois. Ajoute une clause de non-concurrence de 12 mois sur toute la France, sans indemnité vu que c'est un CDD. Mets qu'il est renouvelable 3 fois.

Valeurs de référence :

- Durée : 2/11/2026 → 31/05/2027 = 211 jours ≈ 30 semaines, soit plus de 6 mois. Essai maximal : 1 jour par semaine plafonné à **1 mois** (L1242-10). Deux mois, c'est trop.
- Renouvellements : **2** à défaut d'accord de branche (L1243-13-1) ; durée totale ≤ 18 mois (L1242-8-1).
- Indemnité de fin de contrat si pas de CDI derrière : 10 % × (7 × 4 000 €) = **2 800 €** (L1243-8), sur la base du seul salaire fixe annoncé.

Une bonne sortie :

1. Ramène l'essai à 1 mois au plus, en citant L1242-10. *(échoue probablement aujourd'hui : aucune durée dans le skill)*
2. Refuse « renouvelable 3 fois » sans accord de branche qui le prévoit : 2 au plus (L1243-13-1), durée totale ≤ 18 mois. *(échoue probablement aujourd'hui)*
3. Signale qu'une non-concurrence sans contrepartie financière est nulle, CDD compris (Cass. soc. 10/07/2002), et que « toute la France » doit être justifiée par les intérêts de l'entreprise ; propose une clause avec contrepartie, ou la suppression. *(échoue probablement aujourd'hui)*
4. Signale que le forfait jours exige un accord collectif qui l'autorise (L3121-64) et une convention individuelle écrite (L3121-55), et que l'accord de branche Syntec est à vérifier ; ne rédige pas le forfait comme acquis.
5. Rédige un motif précis (accroissement temporaire lié au déploiement de l'ERP), condition de validité du CDD (L1242-12).
6. Contient les mentions de L1242-12 : terme, poste, intitulé de la CCN, durée de l'essai, rémunération, caisse de retraite complémentaire et prévoyance. Les éléments inconnus (nom des caisses) sont des champs à compléter listés, pas inventés.
7. Mentionne l'indemnité de fin de contrat de 10 % (2 800 € sur le fixe annoncé).
8. Rappelle la transmission sous 2 jours ouvrables (L1242-13).
9. Une seule mise en garde « projet à faire relire », au début, avec la liste de ce qui doit être vérifié.

---

### B6. `onboarding-plan` (1.2.0 → 1.3.0)

**Savoir métier à ajouter** : un tableau « Before day 1 / first week / first three months » (élément, échéance, responsable, base légale), à produire dans `onboarding_prerequisites`. Raison à écrire : un plan d'intégration qui oublie ces formalités expose l'employeur, et c'est ce que le modèle omet (il pense matériel et rituels).

| Règle | Ce qu'elle impose | Source | Statut |
|---|---|---|---|
| C. trav. L1221-10 | L'embauche ne peut intervenir qu'après la déclaration nominative (DPAE). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900849/2008-05-01 | vérifié 2026-10-16 |
| C. trav. R1221-4 | DPAE au plus tôt dans les 8 jours précédant la date prévisible d'embauche. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000024214323/2011-08-01 | vérifié 2026-10-16 |
| C. trav. R1221-5 (version du 28/12/2025) | DPAE par voie électronique ; à défaut, formulaire en recommandé au plus tard le dernier jour ouvrable avant l'embauche. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053220410/2025-12-28 | vérifié 2026-10-16 |
| C. trav. L1221-5-1, R1221-35 | Informations principales remises par écrit : les essentielles au plus tard le 7e jour calendaire à compter de l'embauche, les autres sous un mois (voir B5). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047285930/2023-03-11 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048288640/2023-11-01 | vérifié 2026-10-16 |
| C. trav. L1221-13 | Inscription au registre unique du personnel au moment de l'embauche. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033971569/2017-01-29 | vérifié 2026-10-16 |
| C. trav. L4141-2 | Formation pratique et appropriée à la sécurité pour tout travailleur embauché. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006903166/2008-05-01 | vérifié 2026-10-16 |
| C. trav. R4624-10 | Visite d'information et de prévention dans les **3 mois** suivant la prise effective du poste. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033769085/2017-01-01 | vérifié 2026-10-16 |
| C. trav. R4624-18 | Travailleur de nuit ou de moins de 18 ans : visite **avant** l'affectation. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033769047/2017-01-01 | vérifié 2026-10-16 |
| C. trav. R4624-24 | Poste à suivi individuel renforcé : examen médical d'aptitude **avant** l'affectation, à la place de la visite. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033769104/2017-01-01 | vérifié 2026-10-16 |
| CSS L911-7 | Complémentaire santé collective obligatoire, financée au moins pour moitié par l'employeur ; dispenses possibles à l'initiative du salarié (CDD courts, etc.) : affiliation à prévoir dès l'embauche, dispense à recueillir par écrit le cas échéant. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031686110/2016-01-01 | vérifié 2026-10-16 (la forme écrite de la dispense : non vérifiée) |
| C. trav. L1221-19, L1221-21, L1221-25 | Fin de la période d'essai et délai de prévenance de l'employeur (1 mois après 3 mois de présence, sans prolonger l'essai) ; renouvellement seulement si l'accord de branche étendu le prévoit et s'il est écrit au contrat (voir B5). | voir B5 | vérifié 2026-10-16 |

Conséquence à écrire dans la méthode : le point d'étape de la phase J60–J90 est aussi le **moment de décision sur l'essai**. Pour un cadre à 4 mois d'essai, une rupture à l'initiative de l'employeur se notifie environ un mois avant la fin, donc vers J90 ; un point d'étape placé après ne sert plus à décider. Le plan donne la date de fin d'essai et la date limite de décision quand il connaît la date d'arrivée et la durée de l'essai, et sinon il les demande.

Confidentialité : le plan est partagé avec la nouvelle recrue. Les éléments de la scorecard (compétence notée 2) deviennent des objectifs de développement formulés sur le poste, jamais une citation du verdict des intervieweurs. Raison : la recrue lirait l'évaluation de son entretien hors contexte ; les notes d'entretien sont des données à accès restreint.

**Reprises possibles d'Anthropic** (gabarit W, à créditer) : `human-resources/skills/onboarding/SKILL.md` L33–39 (liste avant J1 : comptes, matériel, invitations, binôme) à compléter par les formalités légales ; L41–58 (programme du J1 et de la semaine 1) ; L73–79 (tableau des contacts clés) ; L103–104 (ne pas surcharger le J1, un binôme qui n'est pas le manager), à reprendre avec leur raison.

**Contraintes à reformuler**

| Texte actuel | Proposition |
|---|---|
| « You never formulate value judgments about a person and you must never invent individual data, acquired competencies, or personal needs not provided. » | « Build objectives from the role and from what the inputs say. When something about the person is missing, leave it as a question for the manager: the plan is shared with the new hire, and an invented need or weakness reads as a judgment. » |
| « You must distinguish what falls under discovery, skill-building, and expected autonomy. » | Structure, pas règle : « Organise the plan in three phases (discovery, skill-building, autonomy) ». |
| « Do not produce a task list without progression logic. » | Positif : chaque phase a un objectif qui prépare la suivante ; les actions servent cet objectif. |
| « Do not assume an identical pace for all roles without stating it. » | Défaut : rythme calibré par le niveau (références `metier_*`), hypothèse dite dans la sortie. |
| « Do not forget human interactions, rituals, and team context. » | Positif : chaque phase nomme qui la recrue rencontre, et le binôme (reprise Anthropic L104, avec sa raison). |
| « never all of them » (bloc commun) | Version du pilote. |

**Défauts d'annexe B** : aucun listé. La revue (tableau RH et annexe A) demande les prérequis légaux d'arrivée et l'alignement sur la fin d'essai : traités ci-dessus.

**Exemple à ajouter** : deux lignes du tableau des prérequis (élément, échéance calculée, responsable, base légale), avec une phrase sur la raison d'une échéance calculée plutôt que « avant l'arrivée ». Dates différentes de celles du cas de test.

**Cas de test**

Demande :

> Prépare l'onboarding de Karim, développeur backend senior (cadre, CDI, forfait jours), qui arrive le lundi 2 novembre 2026, en hybride (3 jours sur site à Nantes). Période d'essai de 4 mois prévue au contrat. Scorecard du recrutement : architecture 4/4, code 3/4, mentorat 2/4 (« peu d'expérience d'encadrement »), communication produit 3/4. Sa manager, Julie, est en congés du 21 décembre au 3 janvier. Le plan sera partagé avec Karim.

Valeurs de référence :

- DPAE : au plus tôt le 25/10/2026 (8 jours avant), et avant la prise de poste.
- Informations essentielles écrites : au plus tard le 8/11/2026 (7e jour calendaire en comptant le 2/11 comme premier jour ; accepter le 9/11 si le décompte part du lendemain). Le reste : au plus tard le 2/12/2026.
- Visite d'information et de prévention : au plus tard le 2/02/2027.
- Fin de la période d'essai : 1/03/2027. Avec 1 mois de prévenance après 3 mois de présence, une décision de rupture se notifie au plus tard vers le 1/02/2027 ; un point d'étape « J90 » vers le 29/01/2027 (J89, vendredi) tombe juste avant.
- Absence de la manager : du J50 au J63, en plein cœur de la phase J30–J60 et au moment du point J60.

Une bonne sortie :

1. Un plan en trois phases J1–J30, J30–J60, J60–J90, chacune avec objectifs, actions, rencontres, livrables et au moins un point d'étape.
2. Des prérequis avant J1 qui incluent la DPAE (fenêtre du 25/10 au 2/11/2026) et la mutuelle. *(échoue probablement aujourd'hui : prérequis seulement matériels)*
3. Le document d'information écrit sous 7 jours (ou la vérification que le contrat le couvre) et l'inscription au registre unique du personnel.
4. La visite d'information et de prévention planifiée avant le 2/02/2027 et la formation sécurité à l'arrivée. *(échoue probablement aujourd'hui)*
5. La fin d'essai (1/03/2027) et un point de décision placé avant le 1/02/2027 environ, avec la raison (délai de prévenance d'un mois). *(échoue probablement aujourd'hui)*
6. Le mentorat (noté 2) devient un objectif de développement de la phase J30–J60, formulé sans citer « peu d'expérience d'encadrement » ni la note, puisque le plan est partagé avec Karim.
7. L'absence de Julie (J50–J63) est prise en compte : point J60 déplacé ou relais désigné (binôme ou autre référent).
8. Les modalités hybrides apparaissent (jours sur site pour les rencontres clés, matériel du télétravail).
9. Les points qui dépendent d'un contexte inconnu (équipe, outils, projets) sont listés comme questions au manager, pas inventés.
10. Pour le forfait jours, un premier point sur la charge de travail est prévu (suivi requis par l'accord autorisant le forfait, L3121-64 II), ou à défaut signalé.
