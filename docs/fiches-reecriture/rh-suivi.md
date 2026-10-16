# Analyse de la famille « rh-suivi » — 2026-10-16

Skills : `entretien-professionnel` (version 2.0.0 du commit `62afe4d`, non fusionnée, **pas réécrite ici**), `performance-review-helper`, `plan-developpement-competences`, `analyse-entretien`, `people-review`, `lettre-cadrage-disciplinaire`, `offboarding-structure`, `org-design-brief` (versions de `cbe271c`).

Référence : grille R1–R10 de `docs/etat-de-l-art-skills.md`. Équivalents Anthropic : clone `kwp`, commit `33eeda1`, Apache-2.0. Droit : chaque article a été lu le 2026-10-16 avec l'outil de normes (statut VIGUEUR, lien Légifrance ou EUR-Lex), sauf mention « non vérifié ».

Forme de référence pour le rédacteur : les pilotes déjà réécrits sur le disque (`skills/nda-draft.md` 1.2.0, `skills/interview-loop-planner.md` 1.3.0). Ils n'ont plus de section « Absolute rule » et portent une section `# Legal frame (France, checked 2026-10-16)`. Suivre ce modèle.

---

## A. Tableau

| Skill (version) | Lignes · équivalent Anthropic | Pourquoi il a cette longueur | Justifié ou manque | Ce qui change | En attente (§3) |
|---|---|---|---|---|---|
| `entretien-professionnel` (2.0.0, `62afe4d`) | 108 l. · aucun | Le droit en vigueur (L6315-1 depuis la loi 2025-989), environ 40 lignes de savoir légal sourcé, le gabarit commun et le bloc des annexes métier. | **justifié** : c'est le skill le plus riche de la famille, et le savoir est à jour. | Pas de réécriture ici. Il lui manque encore : qui mène l'entretien et quand (supérieur hiérarchique, pendant le temps de travail), l'arrêt de 2023 qui permet de tenir l'EPP le même jour que l'entretien annuel, la liste de ce qu'on n'écrit pas dans le compte rendu, un exemple de question qui explore et d'une question qui évalue, et 5 interdits à reformuler (« n'évalue pas » est écrit 4 fois). | Q7 (recette « entretien annuel ») |
| `performance-review-helper` (1.3.0) | 84 l. · `human-resources/performance-review` 149 l. (70 % de gabarits) | Le gabarit commun et le bloc des annexes métier. Aucune règle de droit, aucun gabarit de sortie. | **manque** : il ignore le cadre de l'évaluation (L1222-2/3, critères et méthode connus à l'avance, CSE, discrimination, forfait jours, quotas interdits), et le modèle laissé seul passerait à côté. | Ajouter un cadre légal de 8 à 10 lignes. Ajouter la liste de ce qu'on n'écrit pas (santé, grossesse, syndicat, absences protégées), une auto-évaluation facultative (gabarit Anthropic adapté) et un exemple d'objectif mesurable. Reformuler 6 interdits. Enlever « objectifs SMART pour l'an prochain » des déclencheurs (collision avec `okr`). | Q7 (frontière avec `plan-developpement-competences`, axes présumés / constatés) |
| `plan-developpement-competences` (1.2.0) | 83 l. · aucun (le tableau de `performance-review` L89–92 seulement) | Une méthode métier en 7 étapes : renforcer / acquérir / maintenir, formats, financement nommé (OPCO, CPF), et le bloc des annexes métier. | **mixte** : la méthode est bonne, mais les règles de financement et de temps de formation manquent, et le modèle les inventerait (OPCO pour tous, CPF imposé). | Ajouter 5 règles : OPCO seulement sous 50 salariés, CPF seulement avec l'accord exprès du salarié, formation = temps de travail sauf exception (30 h par an, 2 % du forfait), formations obligatoires à part, lien avec l'EPP et avis du CSE sur le plan. Ajouter un exemple d'indicateur observable. Reformuler 5 interdits. | Q7 (frontière avec `performance-review-helper`) |
| `analyse-entretien` (1.0.0) | 86 l. · aucun (gabarit de debrief de `interview-prep` seulement) | Le gabarit commun, une typologie de risques de 4 mots et le bloc des annexes métier. | **manque** : la contrainte « respecter la confidentialité » ne dit pas quoi ne pas écrire. Il ne dit rien du harcèlement ni de la surcharge (obligation d'agir de l'employeur), ni du droit du salarié à obtenir la copie. Sa description dit encore « obligation légale biennale ». | Ajouter ce qu'on ne consigne pas (art. 9 RGPD, CNIL, L1132-1), les signaux qui obligent à agir (L1152-1/-4, L4121-1, heures non déclarées) et leur escalade aux RH, et le droit d'accès (art. 15). Corriger « biennale ». Ajouter un exemple de reformulation neutre. Reformuler 4 interdits. | Q12 (notes de recrutement : périmètre et déclencheur) ; Q7 |
| `people-review` (1.2.0) | 87 l. · partiel : `performance-review` mode calibrage (L98–132), `people-report` | Le gabarit commun, la méthode (4 dimensions, 9-box, succession, 4 catégories d'actions) et le bloc des annexes métier. | **mixte** : le cœur métier est là, mais il manque le droit (discrimination dans l'évaluation, quotas illicites, accès du salarié à son « potentiel ») et la règle des petits effectifs, qui permettent de reconnaître quelqu'un. | Ajouter les critères qui ne jouent jamais sur le potentiel (âge, grossesse, congé, santé, mandat), la répartition indicative et non imposée (Cass. 2013), le seuil de réidentification et les horizons de succession par défaut. Ajouter un tableau de calibrage (repris d'Anthropic et adapté). Reformuler 6 interdits. | Q5 (pause de calibrage, nominatif, `category: decision`) ; Q2 |
| `lettre-cadrage-disciplinaire` (1.1.0) | 74 l. · aucun | Le gabarit commun, une procédure légale résumée en une ligne, et la règle des faits datés répétée 4 fois. | **manque** : le droit disciplinaire est fragile, et il en manque l'essentiel. Une lettre de « recadrage » qui reproche des fautes est souvent un avertissement (pouvoir disciplinaire épuisé). Il manque aussi l'entretien préalable dès que la sanction touche la paie ou le poste, les délais d'un mois et de 2 jours, la règle des 3 ans, le règlement intérieur et l'interdiction des amendes. | Ajouter un cadre légal (L1331-1 à L1333-2, R1332-1/2, 4 arrêts). Calculer les délais à partir des dates fournies. Signaler le piège de la « mise en demeure » (présomption de démission). Ramener à une seule fois les règles dites 3 ou 4 fois. Aligner le README (annexe B). | — (manque du catalogue : convocation à l'entretien préalable, ne pas la créer) |
| `offboarding-structure` (1.2.0) | 84 l. · aucun | Le gabarit commun, une checklist administrative d'une ligne, identique quel que soit le mode de départ, et le bloc des annexes métier. | **manque** : la checklist ne varie pas selon le mode de départ, alors que préavis, indemnités, délais et documents en dépendent. La renonciation à la non-concurrence, la portabilité et l'épargne salariale manquent. | Ajouter un tableau « mode de départ → préavis, indemnité, délais, documents » (démission, licenciement, rupture conventionnelle, fin de CDD, fin de période d'essai), avec ses articles. Ajouter la date limite de renonciation à la non-concurrence, les accès sensibles (banque, signatures) et un exemple chiffré d'indemnité minimale. Reformuler 5 interdits. | — |
| `org-design-brief` (1.1.0) | 80 l. · `human-resources/org-planning` 28 l. (repères chiffrés) | Le gabarit commun et 6 gestes, dont 4 sont ceux d'atomes. Aucun vocabulaire d'organisation, aucun droit. | **manque** : il prépare une annonce sans le CSE, ce qui expose à un délit d'entrave (annexe B). Il n'a ni seuils, ni délais, ni repères de taille d'équipe. | Ajouter le cadre CSE (L2312-8 et -14, délais R2312-6, expert, entrave L2317-1) et un séquencement par défaut « consulter avant d'annoncer ». Ajouter ce qui fait basculer vers une autre procédure (modification du contrat, L1222-6, 10 refus, PSE), les risques psychosociaux et le DUERP, et les repères d'encadrement d'Anthropic adaptés. Reformuler 6 interdits. | Q2 (même skill avant et après l'avis du CSE) ; manque du catalogue « dossier CSE » (ne pas le créer ici) |

---

## B. Fiches de réécriture

Règles communes à toutes les fiches (pour le rédacteur) :

- Ne pas changer l'id, le périmètre, la forme (skill simple), le corps en anglais, le frontmatter canonique, ni la convention « RAS — ». Version : passer en mineure (1.x → 1.(x+1).0) sauf `entretien-professionnel`, qui n'est pas touché ici.
- Toute règle de droit ajoutée va dans une section `# Legal frame (France, checked 2026-10-16)`, avec l'article et ce qu'il impose en une ligne. Dire « vérifier la version en vigueur avant de s'y fier ». Pas d'URL dans le corps si le pilote n'en met pas ; les URL ci-dessous servent à vérifier.
- Le bloc « Domain references » (8 lignes, identique dans 6 skills) reste tel quel : c'est le format du §3bis.
- La section « Absolute rule » disparaît. Ce qu'elle porte d'utile passe dans Role (une phrase) ou dans Method, avec sa raison. Le triple « observé / hypothèse / recommandation », recopié dans tout le corpus, est dit **une fois**, à l'endroit du livrable où il sert.
- La mise en garde « ne remplace pas un avis juridique » est dite **une fois** dans le corps, et une fois dans le livrable.
- Aucune reprise d'Anthropic n'est obligatoire. Toute reprise est créditée dans `THIRD_PARTY.md` (anthropics/knowledge-work-plugins, commit `33eeda1`, Apache-2.0, chemin et lignes).
- Créer un nouveau partial est hors périmètre. Le paragraphe « ce qu'on n'écrit pas sur une personne », utile à 4 skills de la famille, est donc écrit court (3 à 5 lignes) dans chacun. Le passer en partial est une idée à proposer à Amiel, pas à faire.

---

### B1. `entretien-professionnel` (2.0.0, commit `62afe4d`) — ce qui manque encore, sans réécriture

Lu dans `git show 62afe4d:skills/entretien-professionnel.md`. Le savoir légal de cette version a été recoupé avec L6315-1 en vigueur depuis le 2025-12-31 (lu le 2026-10-16) : périodicité, retour d'absence, mi-carrière, 60 ans, état des lieux à 8 ans et abondement sont exacts.

| Grille | Ce qui manque |
|---|---|
| R1 savoir | (a) **Qui et quand** : l'EPP est « organisé par l'employeur et réalisé par un supérieur hiérarchique ou un représentant de la direction », « pendant le temps de travail » (L6315-1 I, al. 7). Absent du skill. (b) **Même jour que l'entretien annuel** : possible si l'évaluation n'est pas évoquée pendant l'EPP (Cass. soc., 5 juillet 2023, n° 21-24.122, publié). C'est la question pratique la plus fréquente, et le skill dit seulement « ne pas confondre ». (c) **Ce qu'on n'écrit pas dans le compte rendu** : santé (art. 9 RGPD ; L6315-1 IV, l'employeur n'a pas accès aux données de santé, déjà dit pour la mi-carrière seulement), grossesse, appartenance syndicale ; le salarié peut en obtenir copie (art. 15 RGPD). (d) Lien aval : le plan de développement « peut tenir compte des conclusions » des EPP (L6321-1 dernier al., version du 2025-10-26), à citer pour la frontière avec `plan-developpement-competences`. (e) L'effectif de 50 salariés pour l'abondement s'apprécie selon L130-1 CSS (L6315-1 II) : une demi-ligne. |
| R2 interdits | 5 à reformuler. « Do not evaluate performance — it is outside the scope » est dit 4 fois (description, Absolute rule, Constraints, Definition of done) : n'en garder qu'une, avec la raison légale (« L6315-1 : il ne porte pas sur l'évaluation du travail ; un compte rendu qui évalue fragilise la preuve que l'EPP a eu lieu »). « Do not produce a pre-filled record with invented information » : remplacer par « laisse vides les champs que seul l'entretien peut remplir, entre crochets ». « Never state the former 2-year / 6-year rules as current » : garder, la raison est déjà là. « You never formulate value judgments… must never invent » : fusionner dans Role. |
| R3 liberté | Correct : le droit est prescrit, la trame est laissée au jugement. |
| R4 annexes | Le cadre légal (environ 25 lignes) ne sert qu'à ce skill et sert à chaque exécution : il reste dans le corps. |
| R5 exemple | Manque une paire `<example>` d'une ligne : une question qui explore (« Quelles compétences de votre poste voyez-vous évoluer d'ici 4 ans ? ») et la même tournée en évaluation (« Avez-vous atteint vos objectifs ? »), avec une phrase qui dit pourquoi la seconde sort de l'EPP. |
| R6 description | 789 / 862 caractères, sous 1 024. Rien à changer. |
| R7 cohérence | « EPP », « career path interview » et « professional development interview » (nom du champ de sortie) cohabitent. Garder le nom du champ, et dire une fois que c'est l'EPP. |
| R8 gabarit | « Absolute rule » redit la Definition of done : fusionner. |
| R9 §3 | Q7 : la recette « entretien annuel » le cite comme étape 1 possible. Rien à faire avant la réponse. |
| R10 test | Aucun. Cas proposé ci-dessous. |

**Cas de test (court).**

> Je dois préparer l'entretien de parcours professionnel de Nadia, technicienne de maintenance, embauchée le 1er mars 2018. On est 62 salariés. Elle a eu ses entretiens professionnels en mars 2020 et en mars 2022, plus rien depuis. Elle est revenue de congé parental le 1er septembre 2026. Depuis 2018 elle n'a suivi que l'habilitation électrique obligatoire. Son manager voudrait en profiter pour faire aussi son évaluation annuelle le même jour. Prépare l'entretien.

Une bonne sortie :
1. Dit qu'un EPP de retour de congé parental est dû (aucun EPP dans les 12 mois avant la reprise).
2. Signale que l'état des lieux des 8 ans est dû ou dépassé (8 ans d'ancienneté atteints en mars 2026), avec les 3 critères du II.
3. Signale le risque d'abondement correctif de 3 000 € (au moins 50 salariés, aucune formation autre qu'obligatoire), versé au plus tard le dernier jour du trimestre civil suivant l'état des lieux.
4. Ne compte pas l'habilitation obligatoire comme « formation autre que celle de L6321-2 ».
5. Accepte le même jour, à condition de tenir deux entretiens distincts, sans évaluation dans l'EPP (Cass. soc. 5 juillet 2023). *La version 2.0.0 échouerait probablement : elle dit seulement « ne pas confondre ».*
6. Rappelle que l'EPP se tient pendant le temps de travail, mené par un supérieur hiérarchique ou un représentant de la direction. *La version 2.0.0 échouerait probablement.*
7. Couvre les 5 thèmes légaux avec des questions ouvertes, et donne un compte rendu à remettre en copie à la salariée.
8. N'applique pas les anciennes règles (2 ans, 6 ans).
9. Ne prérédige aucune réponse de la salariée.

---

### B2. `performance-review-helper` (1.3.0)

**Savoir métier à ajouter** (section `Legal frame`, vérifié 2026-10-16) :

| Règle | Ce qu'elle impose | Source |
|---|---|---|
| C. trav. L1222-2 | Les informations demandées au salarié n'ont pour finalité que d'apprécier ses aptitudes professionnelles, avec un lien direct et nécessaire. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900859 |
| C. trav. L1222-3 | Le salarié est informé **avant** des méthodes et techniques d'évaluation ; les résultats sont confidentiels ; les méthodes sont pertinentes au regard de la finalité. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900860 |
| C. trav. L1132-1 | Pas de mesure discriminatoire, notamment en matière d'« évaluation de la performance », en raison de l'âge, de la grossesse, de la situation de famille, de l'état de santé, des activités syndicales, etc. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045391841 |
| Cass. soc., 27 mars 2013, n° 11-26.539 (publié) | Un mode d'évaluation qui impose des groupes affectés de quotas préétablis est illicite ; une répartition indicative reste possible. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000027252089 |
| Cass. soc., 28 nov. 2007, n° 06-21.964 (publié) | Un projet d'entretiens annuels qui pèse sur la carrière et la rémunération, et peut créer une pression psychologique, doit être soumis à l'instance compétente (alors le CHSCT) avant sa mise en œuvre. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000017738045 |
| C. trav. L2312-8 II 3° et 4° | Le CSE (au moins 50 salariés) est informé et consulté sur les conditions de travail et sur tout aménagement important qui les modifie. Fonde, avec l'arrêt de 2007, la consultation sur un **dispositif** d'évaluation. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043975196 |
| C. trav. L2312-38 | Le CSE est informé et consulté avant la mise en œuvre des moyens ou techniques de contrôle de l'activité des salariés. Le texte ne nomme pas l'évaluation : ne pas lui faire dire plus. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035610275 |
| CNIL, « L'évaluation annuelle des salariés » (page du 25/01/2016) | Critères objectifs et transparents. Commentaires libres objectifs, sans propos subjectifs ou insultants. Le salarié accède aux données qui ont fondé une décision, comme un classement ou un potentiel. Conservation limitée à la durée de l'emploi. CSE informé et consulté sur les techniques d'évaluation. | https://www.cnil.fr/fr/levaluation-annuelle-des-salaries-droits-et-obligations-des-employeurs |
| C. trav. L3121-65 I 3° | Salarié au forfait jours sans stipulation conventionnelle : un entretien annuel porte sur la charge de travail, l'organisation, l'articulation vie professionnelle / personnelle et la rémunération. Des entretiens d'évaluation qui n'en parlent pas ne suffisent pas (Cass. soc., 27 mars 2024, n° 22-17.078, inédit). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036262800 |
| Cass. soc., 5 juillet 2023, n° 21-24.122 (publié) | L'entretien annuel et l'EPP peuvent avoir lieu le même jour, si l'évaluation n'est pas évoquée pendant l'EPP. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000047805228 |
| Art. 9 RGPD, et CNIL « Zones bloc-note et commentaires » (28/02/2019) | La santé est une donnée sensible : pas de pathologie sans consentement exprès ; termes neutres. | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:02016R0679-20160504 ; https://www.cnil.fr/fr/zones-bloc-note-et-commentaires-les-bons-reflexes-pour-ne-pas-deraper |

Savoir métier (non juridique) à écrire comme positions par défaut, sans source externe :
- Une période d'absence protégée (maternité, paternité, maladie, mandat) se traite par **prorata ou neutralisation** de l'objectif, jamais par une note plus basse. Raison : L1132-1, et c'est l'erreur que le modèle ferait seul (« objectif manqué »).
- Une échelle d'appréciation se définit par des comportements observables à chaque niveau. Si l'entreprise a sa propre échelle, on la reprend sans la remplacer.
- Biais à surveiller, une ligne chacun : récence, halo, indulgence ou sévérité centrale, comparaison entre collègues. Le partial `transverse_anti_biais` porte sur le recrutement : ne pas le lier.
- Pas plus de 3 à 5 objectifs, chacun avec un indicateur, une cible, une échéance et le point de départ mesuré. Si le point de départ manque, l'écrire « à mesurer » plutôt que l'inventer.

**Reprises d'Anthropic** :
- `human-resources/skills/performance-review/SKILL.md` L29–60 (gabarit d'auto-évaluation) : à proposer en sortie facultative « trame d'auto-évaluation à envoyer au salarié ». À adapter : retirer « Feedback for Manager » ou le rendre facultatif, et ajouter « conditions de travail et charge » pour le forfait jours.
- Ne **pas** reprendre la distribution cible 15-20 / 60-70 / 10-15 % (L109–114) comme cible : c'est une norme américaine de distribution forcée. Imposée, elle devient un quota illicite en France (Cass. 2013).
- Ne pas reprendre les « Tips » L144–149 : du remplissage.

**Contraintes à reformuler** :

| Texte actuel | Proposition |
|---|---|
| « You never formulate value judgments about a person » | Positif, dans Role : « describe work behaviours and results with their date or source; an adjective about the person is not evidence and is what the employee will contest ». |
| « must never invent individual data, results, or behaviors » | « Leave a bracketed field when a result is not given; the review is a record the employee can obtain a copy of (CNIL), so an invented figure becomes a liability. » |
| « You must remain factual, professional… » + la répétition du triple | Une seule fois, dans le format de sortie : trois colonnes « fait / lecture du manager / question à poser ». |
| « Do not analyze an already-completed grid. » | À sortir du corps : la frontière est dans la description (`analyse-entretien`). |
| « Do not turn perceptions into established facts. » | Fusionner avec la colonne « lecture du manager ». |
| « Do not produce vague or unmeasurable objectives. » | Remplacer par l'exemple R5 et la règle « indicator, target, deadline, baseline ». |

**Défauts d'annexe B à corriger** : la collision de déclencheur avec `okr` sur « objectifs SMART ». Retirer « objectifs SMART pour l'an prochain » / « SMART objectives for next year » des déclencheurs, et ajouter « prépare l'entretien d'évaluation de… ». La frontière avec `plan-developpement-competences` (§5 de la méthode actuelle) dépend de Q7 : la lister sans la trancher, et garder pour l'instant « development axes » sans plan détaillé.

**Exemple de forme à ajouter** : une ligne d'objectif dans un `<example>`. Un objectif flou (« améliorer la relation client »), puis sa version avec indicateur, valeur de départ, cible et échéance (« NPS interne de 46 en sept. 2026 à 50 au 30/06/2027, mesuré par l'enquête semestrielle »). Une phrase dit pourquoi : chaque terme peut être vérifié au prochain entretien.

**Cas de test**

> Je prépare l'entretien annuel de Karim, chef de projet confirmé, 4 ans d'ancienneté, au forfait jours (notre accord de branche ne dit rien sur l'entretien). Ses objectifs 2026 : 1) livrer la migration CRM avant le 30 juin (livrée le 15 septembre, le prestataire a quitté le projet en avril) ; 2) former deux juniors à l'outil de ticketing (fait) ; 3) NPS interne ≥ 40 (mesuré 46 en septembre). Il a pris 4 semaines de congé paternité en mars et a été en arrêt 3 semaines en mai (« burn-out léger » d'après son N+1, aucun document). La DRH demande qu'au maximum 20 % de l'équipe soit noté « dépasse les attentes ». Prépare la trame de l'entretien et ses objectifs 2027.

Une bonne sortie :
1. Fait le bilan objectif par objectif avec le fait chiffré : retard d'environ 2,5 mois avec sa cause externe, 2 juniors sur 2, 46 pour une cible de 40.
2. N'écrit ni « burn-out » ni aucun diagnostic dans la trame, et dit pourquoi (donnée de santé, art. 9 RGPD, document accessible au salarié). *La version 1.3.0 échouerait probablement.*
3. Ne retient pas le congé paternité ni l'arrêt contre l'atteinte des objectifs : prorata ou neutralisation, en citant le risque de discrimination (L1132-1). *Échouerait probablement.*
4. Ajoute le volet forfait jours : charge de travail, organisation, articulation vie professionnelle / personnelle, rémunération (L3121-65). *Échouerait probablement.*
5. Traite les 20 % comme un repère indicatif. Signale qu'un quota imposé est illicite (Cass. soc. 27 mars 2013) et que la note de Karim se fonde sur ses résultats. *Échouerait probablement.*
6. Propose au plus 5 objectifs 2027, chacun avec indicateur, valeur de départ, cible et échéance.
7. Sépare les faits, la lecture du manager et les questions à poser à Karim.
8. Propose des questions ouvertes ou une trame d'auto-évaluation pour Karim.
9. Demande si les critères et la méthode d'évaluation ont été communiqués au salarié avant l'entretien (L1222-3), au lieu de le supposer.
10. Renvoie vers `entretien-professionnel` pour les souhaits d'évolution, sans les traiter dans la trame d'évaluation.

---

### B3. `plan-developpement-competences` (1.2.0)

**Savoir métier à ajouter** (vérifié 2026-10-16) :

| Règle | Ce qu'elle impose | Source |
|---|---|---|
| C. trav. L6321-1 (version du 2025-10-26, loi 2025-989) | L'employeur assure l'adaptation au poste et veille au maintien de la capacité à occuper un emploi. Les actions sont prévues par le plan de développement des compétences, qui « peut tenir compte des conclusions » des EPP (L6315-1). Elles peuvent viser un bloc de compétences du RNCP. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000052437104 |
| C. trav. L6321-2 | Une formation qui conditionne l'exercice d'une activité (obligation légale ou réglementaire) est du temps de travail effectif, rémunération maintenue. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037385739 |
| C. trav. L6321-6 | Les autres formations sont aussi du temps de travail effectif, sauf (1) accord collectif qui fixe une limite hors temps de travail, ou (2) sans accord, avec l'accord formalisé du salarié, dans la limite de **30 h par an** (2 % du forfait pour un forfait jours ou heures). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049049406 |
| C. trav. L6323-2 | Le CPF n'est mobilisé qu'avec l'**accord exprès** du titulaire. Son refus n'est pas une faute. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037385087 |
| C. trav. L6332-1-3 I 1° | L'OPCO finance les actions de développement des compétences au bénéfice des entreprises de **moins de 50 salariés**. Au-delà, le plan est à la charge de l'entreprise, sauf accord de branche ou dispositif particulier. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048700911 |
| C. trav. L2312-24 | Le CSE est consulté chaque année sur les orientations stratégiques, dont le plan de développement des compétences. Pour un plan collectif, le signaler. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037385809 |
| C. trav. L6315-1 II | L'état des lieux à 8 ans vérifie qu'au moins une formation non obligatoire a été suivie. Dans les entreprises d'au moins 50 salariés, sans elle et sans les entretiens, l'abondement correctif s'applique. Un plan qui ne contient que des formations obligatoires n'y répond pas. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053279288 |

Non vérifié ici, à ne pas écrire sans vérification : les taux et plafonds de prise en charge des OPCO (ils varient par branche et par an), et le montant du « reste à charge » CPF.

Positions par défaut (sans source externe) :
- Un indicateur de progrès est un comportement observable, daté, constatable par un tiers (« produit seul la consolidation trimestrielle de 2 filiales à T3 »). « A suivi la formation » est un indicateur d'activité, pas de progrès.
- La règle 70 / 20 / 10 n'est pas une norme. Ne pas la citer comme telle ; préférer la pratique en situation à la formation formelle quand l'écart porte sur un savoir-faire.
- Les coûts sont donnés en estimation, marqués comme tels, jamais comme des prix.

**Reprises d'Anthropic** : aucune. Le seul matériau est le tableau « Skill / Current / Target / Actions » de `performance-review` (L89–92), que le skill dépasse déjà.

**Contraintes à reformuler** :

| Texte actuel | Proposition |
|---|---|
| « never formulate value judgments… must never invent gaps or needs not documented » | « Every gap cites where it comes from (review, assessment, job change); a gap without a source goes to "to confirm", because the plan commits a budget. » |
| « Do not produce a list of training programs with no link to identified competencies » | Déjà couvert par la Definition of done (« each action linked to a competency ») : supprimer le doublon. |
| « Do not confuse the employee's wishes with the identified need — both are useful but must be distinguished » | Positif : « keep the employee's wishes in their own column; they can be funded differently (CPF only with their express agreement, L6323-2) ». |
| « Do not propose unrealistic actions relative to the context » | « Size the plan to the budget and hours given; when none is given, state the assumption (e.g. hours per quarter) so the manager can correct it. » |

**Défauts d'annexe B** : aucun propre. La frontière avec `performance-review-helper` dépend de Q7 : la lister.

**Exemple de forme à ajouter** : une ligne du plan dans un `<example>` (compétence, type renforcer / acquérir / maintenir, action, format, trimestre, indicateur observable, coût estimé, financement), avec une phrase sur ce qui la rend vérifiable.

**Cas de test**

> On est un cabinet d'expertise comptable de 35 salariés, pas d'accord sur la formation. Léa est comptable junior depuis 2 ans. Son entretien annuel conclut qu'elle doit gagner en autonomie sur les révisions de dossiers et apprendre la consolidation pour passer comptable confirmée d'ici 12 mois. Elle voudrait aussi progresser en anglais (pour elle, pas pour le poste) et préférerait se former le samedi pour ne pas laisser ses dossiers. Budget : 3 000 € sur l'année. Fais-lui un plan de développement.

Une bonne sortie :
1. Classe la révision en « renforcer », la consolidation en « acquérir », et met l'anglais à part comme souhait personnel.
2. Propose pour l'anglais le CPF, seulement avec l'accord exprès de Léa, en disant que son refus n'est pas une faute (L6323-2). *La version 1.2.0 échouerait probablement : elle cite le CPF comme une source de financement parmi d'autres.*
3. Dit que la formation sur le samedi, hors temps de travail, demande l'accord écrit de Léa et reste limitée à 30 h par an sans accord collectif (L6321-6). Sinon, c'est du temps de travail payé. *Échouerait probablement.*
4. Mentionne la prise en charge possible par l'OPCO, puisque le cabinet a moins de 50 salariés (L6332-1-3), sans inventer de taux. *La version actuelle cite l'OPCO sans condition d'effectif.*
5. Donne un calendrier par trimestre, sur 12 mois.
6. Donne au moins un indicateur observable par compétence, et pas seulement « formation suivie ».
7. Tient dans les 3 000 €, avec des coûts marqués comme estimations.
8. Mêle formation formelle et mise en situation (révision de dossiers en autonomie croissante, tutorat).
9. Liste les prérequis : validation du manager, dossier support pour la consolidation.
10. Ne réévalue pas Léa et n'invente pas d'écart que l'entretien n'a pas relevé.

---

### B4. `analyse-entretien` (1.0.0)

**Savoir métier à ajouter** (vérifié 2026-10-16) :

| Règle | Ce qu'elle impose | Source |
|---|---|---|
| Art. 9 RGPD | Le traitement des données de santé, d'appartenance syndicale, d'opinions politiques ou religieuses, ou d'orientation sexuelle est interdit sauf exception (par ex. consentement explicite, obligation de droit du travail encadrée). | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:02016R0679-20160504 |
| Art. 15 RGPD | Le salarié obtient copie des données qui le concernent, donc de la synthèse. | même URL |
| CNIL, « Zones bloc-note et commentaires » (28/02/2019) | À ne jamais inscrire : commentaires subjectifs ou insultants, situation personnelle non pertinente (divorce…), pathologie précise sans consentement exprès, infractions. Termes génériques recommandés (« arrêt maladie », « hospitalisation »). | https://www.cnil.fr/fr/zones-bloc-note-et-commentaires-les-bons-reflexes-pour-ne-pas-deraper |
| CNIL, « L'évaluation annuelle des salariés » (25/01/2016) | Seules les informations ayant un lien direct et nécessaire avec l'emploi. Conservation limitée à la durée de l'emploi. | https://www.cnil.fr/fr/levaluation-annuelle-des-salaries-droits-et-obligations-des-employeurs |
| C. trav. L1222-2 | Les informations demandées n'ont pour finalité que d'apprécier les aptitudes professionnelles. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900859 |
| C. trav. L1132-1 | Grossesse, situation de famille, santé et activité syndicale ne peuvent fonder aucune mesure, évaluation comprise. Les sortir de la synthèse évite qu'ils pèsent sur une décision. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045391841 |
| C. trav. L4121-1 | L'employeur prend les mesures pour protéger la santé physique **et mentale** (prévention, information, organisation). Un signal de surcharge ou d'épuisement appelle une action, pas seulement une note. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035640828 |
| C. trav. L1152-1 et L1152-4 ; L1153-5 | Le harcèlement moral est défini par des agissements répétés. L'employeur prend toutes dispositions pour le prévenir (et, pour le harcèlement sexuel, pour y mettre un terme et le sanctionner). Un propos rapporté de cet ordre déclenche une escalade aux RH, pas une qualification par le skill. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900818 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000029144897 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037389712 |

Positions par défaut :
- Trois destinations distinctes : (1) la synthèse pour le manager ; (2) ce qui va **aux RH seulement** (allégation de harcèlement, situation de santé évoquée par le salarié, demande de protection) ; (3) ce qui **n'est pas écrit du tout** (diagnostic, traitement, grossesse non annoncée, appartenance syndicale). Raison : la synthèse circule, elle est accessible au salarié, et ces données ne peuvent fonder aucune décision.
- Signaux qui imposent une action datée, au-dessus de tout le reste : propos rapportés de dénigrement ou d'humiliation répétés, propos ou gestes à caractère sexuel, heures non déclarées ou charge incompatible avec les repos, idées noires. Le skill ne qualifie pas juridiquement : il écrit « faits rapportés, à instruire par les RH ».
- Cette liste dit **ce qui doit être signalé**, pas un seuil sous lequel on se tait (G3).

**Reprises d'Anthropic** : aucune utile. `interview-prep` porte sur le recrutement.

**Contraintes à reformuler** :

| Texte actuel | Proposition |
|---|---|
| « You pass no value judgment on the person » + « Do not pass judgment on the person » (en double) | Une fois, dans Role, avec la raison : « the synthesis is read by the manager and can be obtained by the employee ». |
| « Do not turn an inference into a certainty. » | Déjà porté par la colonne certain / probable / à confirmer : supprimer. |
| « Respect the implicit confidentiality of HR data — do not overexpose personal details. » | Remplacer par les trois destinations ci-dessus et l'exemple R5. |
| « Flag the areas too vague… » | Garder : c'est positif. |

**Défauts d'annexe B** :
- La description dit « `entretien-professionnel` pour l'obligation légale **biennale** » (FR) et « biennial » (EN). C'est périmé depuis la loi 2025-989 : écrire « l'entretien de parcours professionnel ». Le commit `62afe4d` ne l'a pas corrigé.
- Déclencheur « notes d'entretien » qui capte aussi le recrutement : dépend de Q12. Lister, ne pas toucher.

**Exemple de forme à ajouter** : un `<example>` de trois lignes. Une phrase de notes brutes (« sous antidépresseurs depuis janvier, dort mal ») et ce que devient chaque destination : synthèse manager « a fait part d'une fatigue importante ; charge de travail à revoir », note RH « situation de santé évoquée, proposer la médecine du travail », rien sur le traitement. Une phrase dit pourquoi.

**Cas de test**

> Voici mes notes brutes de l'entretien annuel de Sophie, assistante commerciale, 3 ans d'ancienneté. Fais-moi la synthèse pour moi (manager) et pour la RH.
> « Objectifs atteints sauf taux de relance clients : 60 % pour 80 % visés. Dit qu'elle fait des heures sup non déclarées depuis le départ de Marc en juin, dort mal, est sous antidépresseurs depuis janvier. Se plaint que Paul (N+2) lui a crié dessus devant l'équipe en réunion, trois fois depuis juillet. Veut évoluer vers chargée de clientèle. Enceinte, elle l'annoncera à l'équipe en novembre. S'est syndiquée récemment. Demande une formation Salesforce. »

Une bonne sortie :
1. N'écrit ni le traitement, ni la grossesse, ni l'appartenance syndicale dans la synthèse du manager, et dit pourquoi (art. 9 RGPD, CNIL, L1132-1). *La version 1.0.0 échouerait probablement : elle ne dit que « confidentialité implicite ».*
2. Signale les propos rapportés sur le N+2 (répétés, devant l'équipe) comme des faits à instruire par les RH sans délai, en lien avec l'obligation de prévention (L1152-1, L1152-4). Ne les range pas comme un simple « conflict ». *Échouerait probablement.*
3. Signale les heures non déclarées comme un risque de santé (L4121-1) et de rémunération, avec une action datée sur la charge.
4. Sépare l'explicite (« dort mal ») de l'inféré (épuisement, à confirmer).
5. Donne le chiffre de l'écart (60 % pour 80 %) sans jugement.
6. Liste les besoins exprimés : mobilité vers chargée de clientèle, formation Salesforce.
7. Range les actions par destinataire (manager / RH) et par urgence, l'allégation en premier.
8. Rappelle que la salariée peut obtenir copie de ce qui est écrit (art. 15 RGPD), et en tire la règle d'écriture. *Échouerait probablement.*
9. Liste les points à confirmer.
10. Ne porte aucun jugement sur Sophie ni sur Paul.

---

### B5. `people-review` (1.2.0)

**Savoir métier à ajouter** (vérifié 2026-10-16) :

| Règle | Ce qu'elle impose | Source |
|---|---|---|
| C. trav. L1132-1 | Pas de mesure discriminatoire en matière d'évaluation, de promotion ou de formation en raison de l'âge, de la grossesse, de la situation de famille, de la santé, de l'activité syndicale… Ces critères ne réduisent jamais un « potentiel ». | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045391841 |
| Cass. soc., 27 mars 2013, n° 11-26.539 | Les quotas préétablis imposés aux évaluateurs sont illicites ; une répartition indicative est admise. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000027252089 |
| C. trav. L1222-3 | Méthodes d'évaluation portées à la connaissance des salariés avant leur mise en œuvre ; résultats confidentiels ; méthodes pertinentes. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900860 |
| CNIL, « L'évaluation annuelle des salariés » (25/01/2016) | Le salarié peut accéder aux données qui ont servi à prendre une décision le concernant, « par exemple un classement ou un potentiel de carrière ». | https://www.cnil.fr/fr/levaluation-annuelle-des-salaries-droits-et-obligations-des-employeurs |
| Art. 15 RGPD | Droit d'accès et copie. | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:02016R0679-20160504 |

Non vérifié : un seuil chiffré officiel de réidentification. Écrire la règle comme une position par défaut, pas comme une norme : « ne publier aucun agrégat sur un groupe de moins de 5 personnes, ni un croisement qui isole une personne (seule femme cadre du service, seul senior de l'équipe) ; fusionner ou supprimer la ligne ».

Positions par défaut :
- La performance et le potentiel sont deux axes notés séparément, sur des preuves séparées : résultats pour l'une, comportements observés dans des situations nouvelles pour l'autre. Un « fort performeur » placé d'office en haut potentiel est l'erreur à éviter.
- Préparation à la succession : prêt maintenant / prêt sous 1-2 ans / plus de 2 ans. Un poste clé sans successeur « prêt sous 1-2 ans » est un risque.
- Le placement 9-box n'est rempli que si les deux axes ont des données. Sinon la case reste vide et la donnée manquante est listée.

**Reprises d'Anthropic** :
- `human-resources/skills/performance-review/SKILL.md` L98–132 (tableau « Calibration Prep »), à adapter : retirer « Compensation Actions » (hors périmètre) ; renommer « Company Target » en « repère indicatif (non imposé) » ; garder « Calibration Discussion Points » (cas limites, premier cycle à ce niveau, changement de poste récent), qui est le vrai savoir. Ce tableau va dans le **dossier nominatif**, jamais dans la synthèse collective.
- Ne pas reprendre la distribution cible 15-20 / 60-70 / 10-15 % comme cible (quota, Cass. 2013).
- `people-report` : rien à reprendre (indicateurs génériques).

**Contraintes à reformuler** :

| Texte actuel | Proposition |
|---|---|
| « You never formulate value judgments about an individual person in a collective document » + « Respect confidentiality: individual signals are inputs, not outputs » + « No individual data is exposed… » (trois fois la même règle) | Une fois, avec la raison : « the collective summary circulates to the executive committee; individual placements belong in a separate confidential file, which each employee can access for their own data (CNIL) ». |
| « Do not produce a nominative ranking in the collective summary without the sponsor's validation. » | **Ne pas toucher au fond** (Q5). Garder le texte, sans capitales. |
| « Do not confuse potential and performance — a high performer is not automatically high potential. » | La raison est là : passer en positif (« rate them on separate evidence »). |
| « Do not turn trends into certainties — flag the confidence level. » | Positif : « give each trend its confidence level and the size of the group behind it ». |

**Défauts d'annexe B** : aucun propre. `category: decision` jugé trompeur : dépend de Q5, ne pas le changer.

**Exemple de forme à ajouter** : une ligne de la synthèse collective (agrégat avec effectif et confiance : « Équipe Ops (12) : 3 départs à risque sur postes clés, confiance moyenne ») et la même ligne mal faite (« Julie, seule cheffe d'équipe Ops, risque de départ »), avec une phrase sur la réidentification.

**Cas de test**

> Prépare la people review du comité de direction pour le pôle Finance (11 personnes) : 6 en comptabilité, 3 en contrôle de gestion, 2 au juridique. Données : notes de performance 2026 pour 10 personnes (Inès, contrôleuse de gestion, en congé maternité depuis avril, n'a pas de note). Le manager du contrôle de gestion écrit « Inès : potentiel à revoir, absente 6 mois ». Le DAF écrit « Bernard, 58 ans, potentiel limité, proche de la retraite ». Postes clés : DAF, responsable comptable, juriste senior. La DRH veut 20 % de hauts potentiels, 70 % de standards et 10 % à surveiller. Fais la synthèse pour le comité et le plan d'actions.

Une bonne sortie :
1. Refuse de baisser le potentiel d'Inès à cause du congé maternité et celui de Bernard à cause de son âge. Signale ces deux mentions comme des critères discriminatoires (L1132-1) à retirer du dossier. *La version 1.2.0 échouerait probablement.*
2. Traite la répartition 20 / 70 / 10 comme un repère indicatif, et signale qu'un quota imposé est illicite (Cass. 2013). *Échouerait probablement.*
3. Ne publie dans la synthèse collective aucun agrégat sur le juridique (2 personnes) ni sur le contrôle de gestion (3) qui permette de reconnaître quelqu'un : fusion ou suppression, en le disant. *Échouerait probablement.*
4. Sépare les axes performance et potentiel, et laisse la case vide pour Inès (pas de note) en listant la donnée manquante.
5. Donne une succession par poste clé, avec l'horizon (prêt maintenant / 1-2 ans / plus de 2 ans) ou « aucun successeur identifié ».
6. Classe les actions par catégorie (fidélisation, développement, correction, recrutement) et donne les 5 décisions les plus urgentes.
7. Met les noms seulement dans un dossier nominatif séparé, soumis à la validation du commanditaire.
8. Rappelle que chacun peut accéder aux données qui fondent son classement ou son potentiel (CNIL), et rédige en conséquence.
9. Liste les angles morts : effectif réduit, note manquante, un seul évaluateur par personne.
10. Distingue les faits documentés des hypothèses.

---

### B6. `lettre-cadrage-disciplinaire` (1.1.0)

**Savoir métier à ajouter** (vérifié 2026-10-16) :

| Règle | Ce qu'elle impose | Source |
|---|---|---|
| C. trav. L1331-1 | Est une sanction toute mesure **autre que les observations verbales** prise après un agissement jugé fautif, qu'elle affecte ou non la présence, la fonction, la carrière ou la rémunération. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901445 |
| Cass. soc., 18 mars 2015, n° 13-28.481 ; 30 nov. 2010, n° 09-42.542 | Une lettre qui reproche un manquement précis et prévient qu'il ne sera plus toléré, ou prévoit une sanction s'il se répète, **est un avertissement**. Les mêmes faits ne peuvent plus fonder une autre sanction. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000030386498 ; https://www.legifrance.gouv.fr/juri/id/JURITEXT000023170323 |
| Cass. soc., 25 sept. 2013, n° 12-12.976 ; 23 juin 2021, n° 19-24.020 (publiés) | L'employeur qui connaît plusieurs faits fautifs et n'en sanctionne que certains ne peut plus sanctionner les autres, antérieurs. L'« employeur » inclut le supérieur hiérarchique. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000028004592 ; https://www.legifrance.gouv.fr/juri/id/JURITEXT000043711119 |
| C. trav. L1332-1 | Aucune sanction sans que le salarié soit informé, en même temps et par écrit, des griefs retenus. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901447 |
| C. trav. L1332-2 | Entretien préalable obligatoire, **sauf** pour un avertissement ou une sanction de même nature sans incidence sur la présence, la fonction, la carrière ou la rémunération. Assistance par un membre du personnel. Sanction **ni moins de 2 jours ouvrables, ni plus d'1 mois** après le jour fixé pour l'entretien ; motivée et notifiée. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000025560074 |
| C. trav. R1332-1 | Convocation : objet, date, heure, lieu, droit d'être assisté ; remise contre récépissé ou lettre recommandée, dans le délai de 2 mois. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018536889 |
| C. trav. R1332-2 | Décision écrite et motivée, notifiée par lettre remise contre récépissé ou recommandée, dans le délai d'un mois. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000018536887 |
| C. trav. L1332-3 | Après une mise à pied conservatoire, aucune sanction définitive sans la procédure de L1332-2. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901449 |
| C. trav. L1332-4 | Aucune poursuite disciplinaire pour un fait connu de l'employeur depuis plus de **2 mois**, sauf poursuites pénales dans le même délai. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901450 |
| Cass. soc., 18 janv. 2023, n° 21-20.645 ; 17 janv. 2024, n° 22-13.673 (inédits) | Pour la prescription de 2 mois, l'« employeur » inclut le **supérieur hiérarchique**, même sans pouvoir disciplinaire : sa connaissance des faits fait courir le délai. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000047023599 ; https://www.legifrance.gouv.fr/juri/id/JURITEXT000048990904 |
| C. trav. L1332-5 | Aucune sanction de plus de **3 ans** avant l'engagement des poursuites ne peut être invoquée à l'appui d'une nouvelle sanction. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901451 |
| C. trav. L1331-2 | Amendes et sanctions pécuniaires interdites. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901446 |
| C. trav. L1311-2 et L1321-1 3° ; Cass. soc., 26 oct. 2010, n° 09-42.740 (publié) | Règlement intérieur obligatoire à partir de 50 salariés (après 12 mois au seuil). Il fixe la nature et l'échelle des sanctions. Une sanction autre que le licenciement n'est possible que si elle y est prévue ; une mise à pied n'est licite que si sa durée maximale y est fixée. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038610176 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901432 ; https://www.legifrance.gouv.fr/juri/id/JURITEXT000022977598 |
| C. trav. L1333-2 | Le conseil de prud'hommes peut annuler une sanction irrégulière en la forme, injustifiée ou disproportionnée. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901454 |
| C. trav. L1237-1-1 et R1237-13 | Une **mise en demeure** de justifier une absence et de reprendre le poste (délai d'au moins 15 jours) déclenche la présomption de démission en cas d'abandon de poste. Ce n'est pas un courrier disciplinaire. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046773104 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047456645 |

Non vérifié ici : la jurisprudence qui permet d'invoquer un fait de plus de 2 mois quand le comportement fautif s'est poursuivi ou répété dans le délai. La signaler comme « à faire confirmer par l'avocat », sans l'affirmer.

Positions par défaut :
- **Avant de rédiger**, le skill dit quelle sanction est visée et la procédure qu'elle déclenche : avertissement → pas d'entretien (sauf convention collective ou règlement intérieur) ; mise à pied disciplinaire, mutation, rétrogradation → convocation à l'entretien préalable, et la lettre de sanction ne part qu'après l'entretien.
- Le skill **calcule** les dates à partir de celles qu'on lui donne : date limite de convocation (connaissance + 2 mois), fenêtre de notification (entretien + 2 jours ouvrables, au plus entretien + 1 mois), sanctions antérieures encore invocables (moins de 3 ans).
- Une « lettre de recadrage pour garder une trace », suivie d'une sanction plus lourde pour les mêmes faits, est la double sanction typique. Il faut choisir **avant** d'écrire.
- Rédiger la convocation à l'entretien préalable reste hors périmètre (manque du catalogue). Le skill dit seulement qu'elle est nécessaire et ce qu'elle doit contenir (R1332-1).

**Reprises d'Anthropic** : aucune (pas d'équivalent).

**Contraintes à reformuler** (la règle des faits datés est dite 4 fois, la mention BROUILLON 3 fois, l'avocat 3 fois) :

| Texte actuel | Proposition |
|---|---|
| « You never produce a disciplinary document without precise, dated, and documented facts » (Absolute rule) + Method 1 + Constraints 1 + Definition of done | Une fois, dans Method 1, avec la raison : « the letter must state the grievances (L1332-1) and the labour court checks them (L1333-2); a vague grievance makes the sanction void ». Garder le refus et la « RAS » de la description. |
| « Never qualify a behavior in moral terms (…) » | Garder, avec la raison : un qualificatif moral n'est pas un grief vérifiable et sert l'annulation. |
| « Always include the "DRAFT" mention… » + Absolute rule + Definition of done | Une fois dans le format de sortie. |
| « Do not presume the applicable collective agreement — request it or flag its absence » | Positif : « ask for the collective agreement and the internal rules; they can add a procedure (e.g. an interview before a warning) or limit the sanctions available ». |
| « You do not substitute for a lawyer… You systematically recall this limit » | Une fois dans le corps. |
| « Adapt the formality level… (reprimand < warning < suspension) » | Remplacer par l'échelle réelle : celle du règlement intérieur, ou à défaut observation écrite / avertissement / mise à pied / mutation / rétrogradation / licenciement, avec la procédure de chaque niveau. |

**Défauts d'annexe B à corriger** :
- Le README (FR et EN) présente le skill comme un écrit **avant** procédure, pour « créer une trace écrite », et dit qu'il « ne produit pas une lettre de sanction formelle ». C'est faux en droit (L1331-1, Cass. 2015) et dangereux. Aligner le README sur le corps : le skill rédige un projet de courrier disciplinaire, et tout écrit qui reproche une faute est, en principe, une sanction.
- `.mystaffy.json`, `type_sanction` : la valeur `mise_en_demeure` mélange deux régimes (présomption de démission, L1237-1-1). La signaler dans la fiche ; la retirer ou la renommer est une décision de paramètre (proposée, pas imposée).

**Exemple de forme à ajouter** : le paragraphe « exposé des faits » d'une lettre (date, heure, durée, conséquence observée, source), dans un `<example>`. En regard, la version à proscrire (« votre manque de sérieux répété »), avec une phrase sur ce que le juge vérifie.

**Cas de test** (date du jour donnée dans la demande)

> Nous sommes le 16 octobre 2026. PME de 80 salariés, notre règlement intérieur prévoit : observation écrite, avertissement, mise à pied disciplinaire de 1 à 5 jours, licenciement. Thomas, technicien, est arrivé en retard sans prévenir le 8 septembre (45 min), le 15 septembre (1 h 10) et le 2 octobre (50 min). Le 2 octobre, un client l'a attendu et s'est plaint par mail. Son chef ne m'a prévenue que le 3 octobre pour les trois retards. Thomas a eu un avertissement en juin 2022 pour des retards. Je veux d'abord lui envoyer une lettre de recadrage pour garder une trace, puis lui mettre 3 jours de mise à pied s'il recommence. Rédige.

Une bonne sortie :
1. Signale que la « lettre de recadrage » qui reproche ces retards serait un avertissement : ces faits ne pourraient plus fonder la mise à pied (L1331-1, Cass. 2015). Demande de choisir maintenant. *La version 1.1.0 échouerait probablement.*
2. Pour la mise à pied de 3 jours, impose la convocation à l'entretien préalable avant toute lettre de sanction, et donne la fenêtre de notification : au moins 2 jours ouvrables, au plus 1 mois après l'entretien (L1332-2). *La version actuelle dit « if necessary ».*
3. Calcule la prescription à partir de la connaissance du **chef**, pas de la RH (Cass. 2023 et 2024). S'il a constaté chaque retard le jour même, les dates limites d'engagement sont le 8 novembre 2026 (retard du 8 septembre), le 15 novembre (retard du 15 septembre) et le 2 décembre (retard du 2 octobre). Pour garder les trois faits, la convocation doit donc partir avant le **8 novembre 2026**. Prendre le 3 octobre (la date où la RH a été prévenue) comme point de départ est l'erreur attendue.
4. Écarte l'avertissement de juin 2022 : plus de 3 ans avant l'engagement des poursuites (octobre 2026), il ne peut pas être invoqué (L1332-5). *Échouerait probablement.*
5. Vérifie que la mise à pied est prévue au règlement intérieur, avec une durée maximale (5 jours), et que 3 jours y entrent.
6. Rédige un projet qui expose des faits datés et chiffrés et leur conséquence (plainte du client), sans qualificatif moral.
7. Prévoit la notification par lettre recommandée ou remise contre récépissé (R1332-2), avec une décision motivée.
8. Ne prévoit aucune retenue autre que le salaire des jours de mise à pied (L1331-2).
9. Discute la proportionnalité (3 retards, 1 conséquence client) et cite l'avertissement comme alternative.
10. Porte une seule mention « PROJET — à faire relire par un avocat ou juriste » dans le livrable.

---

### B7. `offboarding-structure` (1.2.0)

**Savoir métier à ajouter** (vérifié 2026-10-16). À mettre sous forme d'un tableau « mode de départ → préavis / indemnités / délais / points propres » dans le corps (environ 15 lignes : il sert à chaque exécution et à ce seul skill, donc pas en `references/`).

| Règle | Ce qu'elle impose | Source |
|---|---|---|
| C. trav. L1234-19 et D1234-6 | À l'expiration du contrat, l'employeur remet un certificat de travail, qui contient **exclusivement** les dates d'entrée et de sortie et la nature des emplois tenus, avec leurs périodes. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901138 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000029544357 |
| CSS L911-8 | Portabilité gratuite de la mutuelle et de la prévoyance collectives si la rupture ouvre droit à l'assurance chômage (pas en cas de faute lourde), pendant la durée d'indemnisation, dans la limite de la durée du dernier contrat, **12 mois au plus**. L'employeur **signale ce maintien dans le certificat de travail** et informe l'assureur. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000027549338 |
| C. trav. L1234-20 | Le solde de tout compte fait l'inventaire des sommes versées. Le reçu est dénonçable dans les **6 mois** suivant la signature, puis il devient libératoire pour ces sommes. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071122 |
| C. trav. R1234-9 | L'attestation d'assurance chômage est remise au salarié et transmise sans délai à France Travail, par voie électronique à partir de 11 salariés. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049816309 |
| C. trav. L3341-7 | Tout bénéficiaire qui quitte l'entreprise reçoit un état récapitulatif de son épargne salariale (PEE, PERCO / PER d'entreprise…). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043197156 |
| C. trav. L3141-28 | Les congés non pris donnent lieu à une indemnité compensatrice, quel que soit l'auteur de la rupture. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033020681 |
| C. trav. L1237-1 | Démission : le préavis dépend de la loi, de la convention collective ou, à défaut, des usages. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901174 |
| C. trav. L1234-1 | Licenciement (hors faute grave) : préavis légal d'1 mois de 6 mois à 2 ans d'ancienneté, de 2 mois au-delà, sauf disposition plus favorable. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901112 |
| C. trav. L1234-9, R1234-2, R1234-4 | Indemnité de licenciement à partir de 8 mois d'ancienneté (sauf faute grave), au moins 1/4 de mois de salaire par année jusqu'à 10 ans, 1/3 au-delà. Salaire de référence : la plus favorable entre la moyenne des 12 derniers mois et le tiers des 3 derniers mois (primes annuelles au prorata). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035644154 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035644692 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035644695 |
| C. trav. L1237-11 à L1237-14 | Rupture conventionnelle : un ou plusieurs entretiens, avec assistance possible (L1237-12) ; indemnité au moins égale à l'indemnité légale de licenciement ; **15 jours calendaires** de rétractation à partir de la signature ; puis demande d'homologation ; **15 jours ouvrables** d'instruction (homologation tacite) ; rupture au plus tôt le lendemain de l'homologation ; recours dans les 12 mois. Pas de préavis : la date de rupture est fixée par la convention. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071187 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071185 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071182 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019071180 |
| C. trav. L1237-15 | Salarié protégé : rupture conventionnelle soumise à l'autorisation de l'inspecteur du travail, et rupture au plus tôt le lendemain de l'autorisation. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000024396475 |
| C. trav. L1243-8 | Fin de CDD non suivie d'un CDI : indemnité de fin de contrat de 10 % de la rémunération brute totale, versée avec le dernier salaire. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901219 |
| Cass. soc., 26 janv. 2022, n° 20-15.755 (publié) ; Cass. soc., 1er juil. 2026, n° 25-10.960 (publié) | Clause de non-concurrence : en rupture conventionnelle, l'employeur qui veut y renoncer doit le faire **au plus tard à la date de rupture fixée par la convention**, quelle que soit la clause. En cas de démission, dans le délai contractuel ou conventionnel et au plus tard au **départ effectif**. Sinon, la contrepartie est due. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000045097537 ; https://www.legifrance.gouv.fr/juri/id/JURITEXT000054392399 |

Non vérifié ici : la règle de prorogation d'un délai qui expire un samedi, un dimanche ou un jour férié (pour la rétractation et l'homologation). Donner les dates comme repères, à confirmer avec la DREETS ou le conseil.

Positions par défaut :
- Les **accès à fort enjeu** passent en tête de la checklist, avec une date : pouvoirs bancaires et de signature, tokens, délégations de pouvoir, comptes administrateurs, mandats auprès des tiers (banque, administration fiscale, URSSAF). Raison : un pouvoir oublié engage encore l'entreprise après le départ.
- L'entretien de sortie est facultatif. Ses réponses ne sont pas reportées nominativement dans un document partagé ; elles sont agrégées.
- La date de départ fixe le budget de passation : si elle tombe avant une échéance que la personne porte seule (clôture, renouvellement de contrat), c'est un risque de continuité à signaler en premier.

**Reprises d'Anthropic** : aucune (pas d'équivalent ; l'`onboarding` d'Anthropic ne couvre pas le départ).

**Contraintes à reformuler** :

| Texte actuel | Proposition |
|---|---|
| « You never formulate value judgments about the person or the reasons for their departure » + « do not presuppose the reason » | Une fois, avec la raison : « the reason changes the legal checklist, so take it from the user or ask; never infer it ». |
| « Do not turn the offboarding into an interrogation about the reasons for departure. » | Positif : « mark the exit interview optional and confidential; ask about the experience, and let the person decide what they say about why they leave ». |
| « Do not forget the human dimension: a well-managed departure protects the employer brand. » | La raison est là : passer en positif (« plan a farewell and a clear last-day schedule »). |
| « Do not assume that everything is documentable — some handovers require time in tandem. » | La raison est là : passer en positif (« for tacit knowledge, plan shadowing time, not only documentation »). |

**Défauts d'annexe B** : la checklist ne varie pas selon le mode de départ (revue, tableau RH). C'est corrigé par le tableau. Le paramètre mystaffy `motif_depart` existe déjà : le corps doit s'y référer.

**Exemple de forme à ajouter** : le calcul de l'indemnité légale minimale en une ligne, dans un `<example>` (ancienneté en années et mois, salaire de référence retenu et pourquoi, résultat). Une phrase dit pourquoi le salaire de référence est le plus favorable des deux.

**Cas de test**

> Claire, responsable comptable en CDI depuis le 1er juillet 2020, part par rupture conventionnelle. On signe la convention le lundi 2 novembre 2026 et on vise une rupture au 31 décembre 2026. Salaire brut mensuel moyen des 12 derniers mois : 3 600 € (les 3 derniers mois sont plus bas). Son contrat contient une clause de non-concurrence de 12 mois payée 30 % du salaire : on ne veut pas la payer. Elle gère seule la clôture annuelle (exercice au 31 décembre) et a la signature bancaire et les tokens. Mutuelle et prévoyance collectives, PEE. On est 40 salariés. Prépare son offboarding.

Une bonne sortie :
1. Calcule l'indemnité minimale : 6 ans et 6 mois × 1/4 × 3 600 € = **5 850 €**, sur le salaire de référence le plus favorable (moyenne des 12 mois), et dit que c'est un plancher (la convention collective peut prévoir mieux).
2. Donne le calendrier : rétractation jusqu'au 17 novembre 2026 inclus, puis demande d'homologation et 15 jours ouvrables d'instruction. Si la demande est reçue le 19 novembre, l'homologation tacite tombe vers le 7 décembre 2026, à confirmer. Le 31 décembre est donc tenable. Pas de préavis.
3. Dit que l'employeur doit renoncer à la non-concurrence **au plus tard le 31 décembre 2026** (date de rupture de la convention), quelle que soit la clause (Cass. 2022). *La version 1.2.0 échouerait probablement.*
4. Mentionne la portabilité mutuelle et prévoyance, pour 12 mois au plus, et son **inscription dans le certificat de travail** (L911-8 CSS). *Échouerait probablement : la version actuelle dit seulement « portability ».*
5. Liste les documents de fin de contrat : certificat de travail, reçu pour solde de tout compte (dénonçable 6 mois), attestation France Travail transmise en ligne (40 salariés, donc au moins 11), état récapitulatif d'épargne salariale (L3341-7). *Le dernier manquerait probablement.*
6. Met en tête le retrait de la signature bancaire, des tokens et des délégations, à une date précise.
7. Signale le risque principal : la clôture annuelle tombe après son départ et elle la porte seule. Il propose une passation en binôme dès novembre ou un relais externe.
8. Demande si Claire est salariée protégée (autorisation de l'inspecteur du travail, L1237-15), au lieu de le supposer.
9. Propose un entretien de sortie facultatif et confidentiel, et une dernière semaine planifiée.
10. Ne présume ni n'interprète les raisons du départ.

---

### B8. `org-design-brief` (1.1.0)

**Savoir métier à ajouter** (vérifié 2026-10-16) :

| Règle | Ce qu'elle impose | Source |
|---|---|---|
| C. trav. L2312-1 | Les attributions du CSE dépendent de l'effectif : section 2 sous 50 salariés, section 3 à partir de 50. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036262407 |
| C. trav. L2312-8 (section 3, au moins 50 salariés) | Le CSE est informé et consulté sur l'organisation, la gestion et la marche générale de l'entreprise, notamment sur les mesures qui affectent le volume ou la structure des effectifs (1°), les conditions d'emploi et de travail, dont la durée du travail (3°), et tout aménagement important des conditions de travail (4°). | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043975196 |
| C. trav. L2312-14 | Les décisions de l'employeur sont **précédées** de la consultation du CSE. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036262404 |
| C. trav. L2312-15 | Le CSE dispose d'informations précises et écrites, d'un délai d'examen suffisant et de la réponse motivée de l'employeur ; l'employeur rend compte de la suite donnée à l'avis. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038791194 |
| C. trav. R2312-6 | Sans accord, le CSE est réputé avoir rendu un avis négatif au bout d'**1 mois**, **2 mois** avec un expert, 3 mois s'il y a des expertises au niveau central et dans les établissements. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036411558 |
| C. trav. L2315-94 2° | Le CSE peut recourir à un expert pour un projet important modifiant les conditions de santé, de sécurité ou de travail. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043975185 |
| C. trav. L2317-1 | L'entrave au fonctionnement régulier du CSE est punie de 7 500 € d'amende. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035634273 |
| Cass. crim., 27 juin 2000, n° 99-85.312 ; 19 sept. 2006, n° 05-86.668 (publié) | L'entrave est constituée quand le dirigeant arrête une restructuration sans consulter le comité, ou avance le calendrier d'un plan sans nouvelle consultation. | https://www.legifrance.gouv.fr/juri/id/JURITEXT000007597156 ; https://www.legifrance.gouv.fr/juri/id/JURITEXT000007075010 |
| C. trav. L1222-6 | Modification d'un élément essentiel du contrat pour motif économique : proposition par lettre recommandée, **1 mois** pour refuser, le silence vaut acceptation. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000028724382 |
| C. trav. L1233-3 | La réorganisation nécessaire à la sauvegarde de la compétitivité est un motif économique, comme la suppression ou la transformation d'emploi. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036762081 |
| C. trav. L1233-25 | Quand au moins 10 salariés refusent une modification de contrat pour motif économique et que leur licenciement est envisagé, la procédure de licenciement collectif s'applique. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901037 |
| C. trav. L1233-61 | À partir de 50 salariés, un projet de licenciement d'au moins 10 salariés sur 30 jours impose un PSE. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036261733 |
| C. trav. L2312-39 | Le CSE est saisi en temps utile des projets de restructuration et de compression des effectifs. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035610279 |
| C. trav. L4121-1 et L4121-3 | L'employeur protège la santé physique et mentale. Il évalue les risques, y compris dans l'organisation du travail et la définition des postes. Le CSE est consulté sur le DUERP et ses mises à jour. | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035640828 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043893923 |

Non vérifié : le détail des attributions du CSE de moins de 50 salariés (article L2312-5) et la frontière jurisprudentielle entre « modification du contrat » et « changement des conditions de travail » (perte d'encadrement, nouveaux horaires). Écrire : « à faire qualifier par un juriste ; le brief liste le point ».

Positions par défaut :
- **Séquencement par défaut** à partir de 50 salariés : (1) le brief est un **projet** ; (2) remise au CSE des informations écrites ; (3) avis du CSE (délai d'un ou deux mois) ; (4) décision ; (5) annonce, puis mise en œuvre. Une présentation aux salariés **avant** l'avis est présentée comme un projet soumis à consultation, jamais comme une décision. Raison : le délit d'entrave, et un avis rendu après coup ne régularise rien.
- Sous 50 salariés : pas de consultation générale. L'écrire, et garder l'information individuelle des personnes touchées.
- Signaux de bascule à mettre en tête du brief s'ils sont présents : un poste supprimé ou transformé (motif économique), une modification de rémunération, de qualification ou de responsabilités, de nouveaux horaires, et plus de 10 personnes concernées par une modification de contrat.
- Les risques psychosociaux de la réorganisation (charge, perte de repères, conflits d'interface) se traitent dans le brief et dans la mise à jour du DUERP, pas seulement dans « human risks ».

**Reprises d'Anthropic** : `human-resources/skills/org-planning/SKILL.md` L17–24 (« Healthy Org Benchmarks » : 5 à 8 subordonnés directs, alerte sous 3 ou au-dessus de 12 ; équipe de 5 à 9). Les reprendre comme **repères indicatifs**, en disant que ce sont des normes d'entreprises technologiques américaines et que l'organisation peut les remplacer. Ne pas reprendre « Management layers 4-6 for 500 people » sans contexte. Créditer dans `THIRD_PARTY.md`.

**Contraintes à reformuler** :

| Texte actuel | Proposition |
|---|---|
| « You never formulate value judgments about a person and you must never invent individual data, attributed responsibilities, or personal performance » | Positif : « name roles, not people, unless the user names them; who goes where is a decision the brief leaves open ». |
| « You must clearly distinguish the current diagnosis, the organizational target, and implementation risks. » | Déjà porté par la structure de sortie : supprimer. |
| « Do not transform the brief into an imaginary org chart without factual basis. » | Fusionner avec la phrase précédente. |
| « Do not present a target as final if decisions remain open. » | Garder, avec la raison légale : « until the works council has given its opinion, the target is a project (L2312-14) ». |
| « Do not overlook interfaces, overlapping zones… » | Déjà dans la structure recommandée : supprimer. |

**Défauts d'annexe B** : il se déclenche « avant toute annonce » sans parler de la consultation du CSE (risque de délit d'entrave). Corrigé par le cadre légal et le séquencement. Dans la description, ajouter « avant la consultation du CSE et l'annonce » sans changer le périmètre. La forme cible (pause `answers` pour l'avis du CSE, même skill avant et après) dépend de **Q2** : ne pas y toucher. Le « dossier d'information-consultation du CSE » est un manque du catalogue : le brief **liste** les informations à remettre au CSE, sans rédiger le dossier.

**Exemple de forme à ajouter** : un `<example>` de séquencement en 5 lignes datées (remise au CSE J, avis réputé rendu à J + 1 mois, J + 2 mois avec un expert, puis décision et annonce), avec une phrase sur pourquoi l'annonce vient après.

**Cas de test**

> SAS de 120 salariés, CSE en place. Je veux fusionner les équipes Support (14 personnes) et Customer Success (9) sous une seule responsable, supprimer 2 postes de managers (ils deviendraient experts, même salaire, sans équipe) et passer le support en horaires décalés 8 h–20 h par roulement. Je veux l'annoncer à l'all-hands du jeudi 5 novembre 2026 et que ce soit effectif au 1er janvier 2027. Prépare le brief de réorganisation.

Une bonne sortie :
1. Dit que le projet doit passer en information-consultation du CSE **avant** la décision : effectifs, conditions et durée du travail, aménagement important (L2312-8, L2312-14). Une annonce présentée comme décidée le 5 novembre expose au délit d'entrave (L2317-1). *La version 1.1.0 échouerait probablement.*
2. Donne un calendrier chiffré. Si le CSE reçoit le dossier complet le 22 octobre 2026, l'avis est réputé rendu le 22 novembre 2026, ou le 22 décembre 2026 avec un expert (R2312-6, L2315-94). Le 1er janvier n'est tenable qu'en commençant tout de suite. *Échouerait probablement.*
3. Présente l'all-hands du 5 novembre au mieux comme la présentation d'un projet soumis à consultation, ou propose de la décaler.
4. Signale que retirer l'encadrement aux 2 managers peut modifier leur contrat (responsabilités) : leur accord est à obtenir, ou la procédure de L1222-6 si le motif est économique. Point à faire qualifier par un juriste.
5. Signale que les horaires décalés touchent la durée et l'organisation du travail : consultation du CSE, évaluation des risques et mise à jour du DUERP (L4121-3), et possible modification de contrat selon les contrats.
6. Dit qu'aucun PSE n'est en jeu (aucun licenciement envisagé), et donne les seuils qui le déclencheraient (10 refus, L1233-25 ; 10 licenciements sur 30 jours, L1233-61).
7. Signale une responsable pour 23 personnes, au-dessus du repère d'alerte (plus de 12 subordonnés directs), et propose des relais (chefs d'équipe), en le présentant comme un repère indicatif.
8. Décrit la cible en rôles, responsabilités et interfaces Support / Customer Success, sans nommer de personnes non citées.
9. Sépare l'existant, la cible, la justification, les risques et le séquencement.
10. Liste les décisions encore ouvertes : qui dirige, sort des 2 managers, roulement, date d'effet.

---

## Points en attente (récapitulatif, aucun traité)

| Question | Skills | Point |
|---|---|---|
| §3 Q2 | `org-design-brief`, `people-review` | Rejouer le même skill avant et après une pause (avis du CSE, calibrage). |
| §3 Q5 | `people-review` | Calibrage, nominatif, `category: decision`. |
| §3 Q7 | `performance-review-helper`, `plan-developpement-competences`, `analyse-entretien`, `entretien-professionnel` | Recette « entretien annuel », frontière des axes présumés / constatés, frontière entre préparation et plan. |
| §3 Q12 | `analyse-entretien` | Notes de recrutement : périmètre et déclencheur. |
| Manques du catalogue | `lettre-cadrage-disciplinaire`, `org-design-brief` | Convocation à l'entretien préalable, dossier CSE : ne pas les créer. |
| Hors périmètre, à proposer | 4 skills de la famille | Un partial « ce qu'on n'écrit pas sur une personne » (art. 9 RGPD, CNIL, L1132-1), aujourd'hui à écrire court dans chaque skill. |
