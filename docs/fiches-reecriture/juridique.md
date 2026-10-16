# Analyse de la famille « juridique » : longueur, manques, fiches de réécriture

Analyse du 2026-10-16, faite selon le brief commun (grille G1–G10 et R1–R10 de `docs/etat-de-l-art-skills.md`, revue `docs/revue-skills-metier.md`). Versions analysées : branche de départ `cbe271c`. Rien n'a été modifié dans le dépôt.

Équivalents Anthropic : clone un clone local (non versionné), commit `33eeda1` (2026-10-15), Apache-2.0, pas de NOTICE. Toute reprise doit être créditée dans `THIRD_PARTY.md`, dans le même commit.

Droit : chaque article cité dans les fiches a été lu le 2026-10-16 dans sa version en vigueur, avec l'outil de normes (texte Légifrance / EUR-Lex). Ce qui n'a pas pu être lu est marqué **non vérifié**.

---

## A. Tableau de la famille

| Skill (version) | Lignes · équivalent Anthropic | Pourquoi il a cette longueur | Justifié ou manque | Ce qui change | En attente (§3) |
|---|---|---|---|---|---|
| `cgv-checker` (1.2.1) | 71 · `legal/review-contract` 358 | Le gabarit ix seul : une méthode de 5 lignes, 4 « Do not », la mise en garde juridique écrite deux fois. Aucun article de loi, aucune grille. | **manque** : il promet de trouver les « clauses abusives » sans aucune des grilles qui les définissent, et c'est précisément là que le modèle se trompe (liste noire ou grise, 1171 ou L442-1). | Ajouter : la qualification B2B / B2C / non-professionnel ; les listes R212-1 (noire) et R212-2 (grise), une ligne par clause ; les mentions et délais B2B (L441-1, L441-10, D441-5) ; L442-1 avec ses ajouts du 18/08/2026, et sa priorité sur l'art. 1171 (Cass. com. 13/05/2026) ; 1119, 1170, 1190, CPC 48 ; la rétractation et la fonction de rétractation obligatoire depuis le 19/06/2026. Des positions vert / orange / rouge chiffrées et un format « constat + repli ». Reformuler 4 interdits, ramener la mise en garde à une ligne, dire comment lire `niveau_detail`. Un exemple de constat. | Q11 (fusion avec `contrat-fournisseur`, la position « fournisseur » doublant l'autre skill) ; Q8 (vérification séparée des clauses absentes) |
| `contrat-fournisseur` (1.2.1) | 69 · `legal/review-contract` 358 | Même gabarit que `cgv-checker`, avec la liste de clauses de l'acheteur. Il promet la rédaction dans sa description, et rien dans le corps n'en traite. | **manque** : il ne contient ni position par défaut (plafond, SLA, reconduction, réversibilité), ni aucune des obligations propres à l'acheteur français (délais de paiement maximaux, vigilance URSSAF, Data Act). « Classés par impact » n'est défini nulle part. | Aligner la description (FR, EN, README, README-fr) sur ce que fait le corps, l'analyse côté acheteur. Ajouter la règle « RAS » (annexe B) ; les positions chiffrées adaptées d'Anthropic ; les trois niveaux de priorité, chacun avec son repli ; les obligations de l'acheteur (L441-10 et L441-16, L442-1 I 6° et II al. 2 du 18/08/2026, L8222-1 à partir de 5 000 € HT, Data Act art. 25 et 29) ; le renvoi à `conformite-rgpd` pour l'art. 28. Le corps doit utiliser le paramètre `type_fournisseur`. Reformuler 3 interdits. | Q11 : la fusion, et le sort du mode rédaction (le garder ou en faire un manque du catalogue). La fiche propose seulement de retirer la promesse de la description, ce qui est compatible avec les deux issues ; elle n'ajoute aucune méthode de rédaction. Q8 |
| `legal-risk-flag` (1.2.1) | 87 · `legal/legal-risk-assessment` 265 | Le gabarit, plus un format de signal en 6 champs. Deux échelles haut / moyen / bas qui se superposent (risque et certitude), et aucune ancre. 5 phrases en « must / never ». | **mixte** : la brièveté est voulue (un tri rapide) et le format est bon. En revanche, sans ancre, le seuil « RAS sous moyen » est arbitraire et fait sous-déclarer (G3). Il n'a ni déclencheur d'escalade ni repère de délai. | Ancrer les trois niveaux (montant en jeu en % de la valeur, délai qui éteint un droit, exposition pénale ou réglementaire), en adaptant Anthropic (L18-36). Remplacer l'échelle de certitude par « texte clair / interprétation / dépend de faits absents ». Ajouter les déclencheurs d'avocat obligatoire (L230-239, adaptés) et une table courte des signaux français fréquents (1170, 1171 / L442-1, 1225, 1231-3, 1231-5, CPC 48, L441-10, 1344, 2224). Dire pourquoi le seuil RAS existe, plafonner le nombre de signaux, définir `type_document` et `niveau_detail`. | Q12 (si l'analyse de `contrat-emploi` lui revient, il faudra des déclencheurs de droit du travail) |
| `nda-draft` (1.1.1) | 67 · `legal/triage-nda` 262 | Le gabarit seul : il nomme les rubriques de clauses et ajoute la mise en garde. Aucun contenu métier (voir notes KWP §2.3). | **manque** (en cbe271c) : ni durée par défaut, ni exclusions, ni ce qui dépend de la relation, ni droit français. Pilote : voir version 1.2.0. | Pilote : voir version 1.2.0. Rien de plus ici. | — |
| `compliance-checklist` (1.1.1) | 69 · `legal/compliance-check` 274 | Le gabarit seul. L'étape 1 « identifier les domaines » ne nomme aucun domaine. | **manque** : le modèle ne connaît pas l'état du droit au 2026-10-16. Le calendrier de l'AI Act a été modifié le 08/07/2026, NIS2 n'est toujours pas transposée en France, la facturation électronique a commencé le 01/09/2026, et plusieurs textes exonèrent les micro et petites entreprises (accessibilité, DSA). Le skill n'a aucune règle de date. | Ajouter une table domaine → fait déclencheur → texte → date d'application → exemption de taille (12 lignes environ), une règle de date (« état du droit au … »), la qualification de taille avant tout, une échelle de statut et de priorité définie, et la frontière avec `conformite-rgpd` (une ligne puis un renvoi). Retirer la valeur `rgpd` de `contexte_reglementaire`, qui contredit cette frontière. Gabarit de verdict d'Anthropic (L29-63). Reformuler 3 interdits. | Q8 (`compliance-checklist` → pause sur les domaines → `conformite-rgpd`) |
| `conformite-rgpd` (1.3.0) | 89 lignes / 2 012 mots · `legal/compliance-check` 274 (partie RGPD L66-240) | Du savoir, article par article : 9 étapes denses, plus dense que KWP sur le RGPD. Plus la mise en garde, écrite 4 fois. | **justifié** : la longueur est du savoir. Il reste deux mises à jour de date et des répétitions à retirer. | Reformuler les interdits et ne garder qu'une mise en garde. Ajouter le démarchage téléphonique sur consentement préalable (C. conso. L223-1, en vigueur depuis le 11/08/2026), comme point séparé à côté de L34-5 et des cookies. Dater le paragraphe « omnibus » : au 2026-10-16, les art. 30 et 33 sont inchangés. Définir `niveau_detail` (rapide / standard / approfondi). Ne rien reprendre de KWP, qui donne d'ailleurs un délai de 30 jours erroné pour les demandes de droits. | Q8 (point d'arrivée de `compliance-checklist`) ; Q2 (le rejouer avec les réponses de l'équipe produit) |

---

## B. Fiches de réécriture

Conventions pour le rédacteur (modèle sans contexte) :
- Corps en anglais, frontmatter canonique inchangé (id, domaine, `compatible`). On ne change ni la forme ni le périmètre. Bump de version mineure.
- La forme à imiter est le pilote `skills/nda-draft.md` 1.2.0 : un paragraphe « pourquoi un générique ne suffit pas », une table « Legal points to get right (French law, checked 2026-10-16) » (point | règle | source), des positions par défaut annoncées comme telles, un exemple court entre balises `<example>` avec une phrase qui dit pourquoi il est juste, et une seule ligne de mise en garde à la fin du livrable.
- Pas de nouveau partial : le savoir va dans le corps. La revue a relevé que les « jeux de clauses par type de contrat » manquent au catalogue ; leur place naturelle viendra avec la décision Q11.
- `dist/` est régénéré par `python3 build.py <id>`, et `THIRD_PARTY.md` est complété pour toute reprise.

### URL de référence (vérifiées le 2026-10-16)

Les URL Légifrance sont les liens permanents d'article (`https://www.legifrance.gouv.fr/codes/article_lc/<LEGIARTI>`). Pour l'UE, le CELEX consolidé lu ce jour est indiqué.

---

### B1. `cgv-checker` (1.2.1 → 1.3.0)

**Savoir à ajouter**

*Étape 0, qualifier avant de lire : la grille applicable en dépend.*

| Point | Ce que le texte impose (une phrase) | Source | URL | Statut |
|---|---|---|---|---|
| Contrat d'adhésion | Un contrat d'adhésion comporte des clauses non négociables déterminées à l'avance par une partie, ce qui est le cas typique des CG. | C. civ. 1110 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036829815 | vérifié 2026-10-16 |
| B2C : clauses abusives | Est abusive la clause qui crée, au détriment du consommateur, un déséquilibre significatif ; l'appréciation ne porte ni sur l'objet principal ni sur le prix si la clause est claire. | C. conso. L212-1 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032890812 | vérifié 2026-10-16 |
| Non-professionnels | L212-1 s'applique aussi aux non-professionnels (associations, SCI…). | C. conso. L212-2 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032227000 | vérifié 2026-10-16 |
| Liste noire (12 clauses) | Ces clauses sont abusives de manière irréfragable et donc interdites : adhésion à des clauses non portées à connaissance (1°), modification unilatérale de la durée, des caractéristiques ou du prix (3°), droit exclusif de juger la conformité ou d'interpréter (4°), suppression ou réduction du droit à réparation (6°), interdiction de résoudre en cas d'inexécution du pro (7°), résiliation discrétionnaire réservée au pro (8°), préavis plus long pour le consommateur en CDI (10°), indemnité de résiliation en CDI (11°), renversement de la charge de la preuve (12°), etc. | C. conso. R212-1 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032807196 | vérifié 2026-10-16 |
| Liste grise (10 clauses) | Ces clauses sont présumées abusives, et le professionnel peut prouver le contraire : indemnité manifestement disproportionnée (3°), résiliation par le pro sans préavis raisonnable (4°), cession du contrat sans accord (5°), modification unilatérale d'autres clauses (6°), date d'exécution indicative (7°), conditions de résiliation plus rigoureuses pour le consommateur (8°), limitation des preuves (9°), entrave aux actions en justice ou MARD imposé (10°), etc. | C. conso. R212-2 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032807198 | vérifié 2026-10-16 |
| Sanction | Les clauses abusives sont réputées non écrites, et le contrat subsiste sans elles (ordre public). | C. conso. L241-1 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032226417 | vérifié 2026-10-16 |
| B2C : rétractation | 14 jours, sans motif et sans autres coûts que ceux de L221-23 à L221-25, à compter de la conclusion (services) ou de la réception (biens). | C. conso. L221-18 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032226842 | vérifié 2026-10-16 |
| Fonction de rétractation | Pour un contrat conclu via une interface en ligne, le pro met à disposition, gratuitement, une fonctionnalité de rétractation. **En vigueur depuis le 19/06/2026** (ord. 2026-2 du 05/01/2026), le modèle l'ignore. | C. conso. L221-21 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053310520 | vérifié 2026-10-16 |
| Exceptions à la rétractation | Biens descellés non renvoyables pour hygiène (5°), biens personnalisés (3°), services pleinement exécutés avec accord exprès (1°), etc. | C. conso. L221-28 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044563170 | vérifié 2026-10-16 |
| Délai de livraison | À défaut de date convenue, livraison sans retard injustifié et au plus tard 30 jours après la conclusion. | C. conso. L216-1 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044142498 | vérifié 2026-10-16 |
| Garantie légale de conformité | Le vendeur répond des défauts existant à la délivrance qui apparaissent dans les 2 ans. | C. conso. L217-3 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044142579 | vérifié 2026-10-16 |
| Tacite reconduction (services, B2C) | Le pro informe par écrit, 3 mois à 1 mois avant le terme, de la faculté de ne pas reconduire ; à défaut, le consommateur résilie gratuitement à tout moment. | C. conso. L215-1 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046194176 | vérifié 2026-10-16 |
| Résiliation en ligne | Si le contrat se conclut en ligne, il doit pouvoir se résilier en ligne par une fonctionnalité gratuite. | C. conso. L215-1-1 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046190107 | vérifié 2026-10-16 |
| Médiateur | Le pro communique les coordonnées du médiateur de la consommation dont il relève. | C. conso. L616-1 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032224762 | vérifié 2026-10-16 |
| B2B : contenu et communication des CGV | Les CGV comprennent les conditions de règlement et les éléments de prix ; elles sont communiquées à tout acheteur professionnel qui le demande et forment le « socle unique de la négociation ». Le manquement est puni d'une amende de 15 000 / 75 000 €. | C. com. L441-1 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038414469 | vérifié 2026-10-16 |
| B2B : délais de paiement et pénalités | Le délai convenu ne dépasse pas 60 jours après la facture, ou 45 jours fin de mois si c'est expressément stipulé. À défaut de délai convenu : 30 jours. Les CGV mentionnent le taux des pénalités (par défaut BCE + 10 points, au minimum 3 fois le taux d'intérêt légal), exigibles sans rappel, et l'indemnité forfaitaire de recouvrement. La procédure d'acceptation ne dépasse pas 30 jours. | C. com. L441-10, version en vigueur du 01/09/2026 au 31/12/2026 ; la version du 01/01/2027 ne change que le renvoi au CIBS | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053151445 | vérifié 2026-10-16 |
| Indemnité forfaitaire | 40 €. | C. com. D441-5 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043197457 | vérifié 2026-10-16 |
| Sanction des délais | Amende administrative jusqu'à 75 000 € (personne physique) ou 2 M€ (personne morale) en cas de non-respect des délais, des mentions ou du taux. | C. com. L441-16 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043750778 | vérifié 2026-10-16 |
| B2B : déséquilibre significatif et autres pratiques | Engage la responsabilité de son auteur : obtenir un avantage sans contrepartie (I 1°) ; soumettre à un déséquilibre significatif (I 2°) ; **depuis le 20/08/2026**, imposer des mises en concurrence ou appels d'offres répétés créant un tel déséquilibre (I 6°) ; rompre brutalement une relation commerciale établie sans préavis écrit suffisant, 18 mois de préavis mettant à l'abri (II) ; **depuis le 20/08/2026**, réduire substantiellement les volumes de commande (II al. 2). | C. com. L442-1, modifié par la loi 2026-796 du 18/08/2026, art. 54 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000054716237 | vérifié 2026-10-16 (ajouts confirmés par comparaison avec la version au 01/08/2026) |
| Articulation 1171 / L442-1 | L'art. 1171 C. civ. ne s'applique pas aux contrats conclus par une personne exerçant des activités de production, de distribution ou de services, sauf si L442-1 est écarté par un autre texte (ex. location financière par un établissement de crédit). Le juge doit rechercher d'office si L442-1 s'applique. | Cass. com. 26/01/2022 n° 20-16.782 ; Cass. com. 13/05/2026 n° 24-17.137 ; Cass. com. 23/09/2026 n° 24-20.775 (publiés au Bulletin) | https://www.legifrance.gouv.fr/juri/id/JURITEXT000045097530 · https://www.legifrance.gouv.fr/juri/id/JURITEXT000054167043 · https://www.courdecassation.fr/decision/6ab38331c27382d099072e9e | vérifié 2026-10-16 (résumés et extraits lus, pas le texte intégral) |
| Art. 1171 (hors commerçants et hors consommateurs) | Dans un contrat d'adhésion, la clause non négociable qui crée un déséquilibre significatif est réputée non écrite (hors objet principal et prix). | C. civ. 1171 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036829836 | vérifié 2026-10-16 |
| Obligation essentielle | La clause qui prive de sa substance l'obligation essentielle du débiteur est réputée non écrite. | C. civ. 1170 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041115 | vérifié 2026-10-16 |
| Bataille des CG | Les CG ne valent que portées à connaissance et acceptées ; si les CG des deux parties se contredisent, les clauses incompatibles sont sans effet ; les conditions particulières l'emportent sur les CG. | C. civ. 1119 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032040866 | vérifié 2026-10-16 |
| Interprétation | Dans le doute, le contrat d'adhésion s'interprète contre celui qui l'a proposé. | C. civ. 1190 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041260 | vérifié 2026-10-16 |
| Limitation de responsabilité | Seul le dommage prévisible est réparé, sauf faute lourde ou dolosive. | C. civ. 1231-3 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032010127 | vérifié 2026-10-16 |
| Clause pénale | Le juge peut la modérer ou l'augmenter si elle est manifestement excessive ou dérisoire ; elle n'est encourue qu'après mise en demeure, sauf inexécution définitive. | C. civ. 1231-5 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032010131 | vérifié 2026-10-16 |
| Clause résolutoire | Elle précise les engagements visés, et la mise en demeure doit la mentionner expressément. | C. civ. 1225 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041477 | vérifié 2026-10-16 |
| Clause attributive de juridiction | Elle est réputée non écrite sauf entre commerçants et si elle est très apparente. Elle ne vaut donc pas contre un consommateur ni contre un non-commerçant. | CPC 48 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006410147 | vérifié 2026-10-16 |
| CGU de service en ligne | Tout fournisseur de service intermédiaire décrit dans ses CG les restrictions d'usage et la modération (y compris algorithmique), en langage clair, et informe de toute modification importante. | Règlement (UE) 2022/2065 (DSA), art. 14 | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32022R2065 | vérifié 2026-10-16 |
| Plateformes vis-à-vis des professionnels | Une plateforme d'intermédiation qui ne respecte pas le règlement P2B engage sa responsabilité. | C. com. L442-1 III ; règlement (UE) 2019/1150 | (voir L442-1) | renvoi vérifié ; contenu du règlement **non vérifié** |

**Consigne de forme pour le rédacteur.** Les listes R212-1 et R212-2 tiennent en une ligne par clause, comme ci-dessus. Le modèle doit pouvoir dire « noire, 3° » ou « grise, 7° » : c'est la différence entre « réputée non écrite » et « présumée abusive, preuve contraire possible ». La raison à écrire dans le skill : le modèle mélange spontanément les deux listes et cite l'art. 1171 entre commerçants.

**Positions par défaut** (B2B, quand l'utilisateur n'a pas de politique interne ; à présenter comme des positions de marché, pas comme du droit) :
- Plafond de responsabilité : vert ≥ 12 mois de prix ; orange entre 6 et 12 mois ; rouge en dessous de 6 mois, s'il n'y a aucun plafond pour l'autre partie, ou s'il est asymétrique.
- Préavis de non-reconduction : vert ≤ 3 mois pour une période annuelle ; orange 3 à 6 mois ; rouge au-delà, ou pour une reconduction pluriannuelle.
- Données personnelles : rouge si aucun accord de sous-traitance (art. 28 RGPD) alors que des données sont traitées ; renvoyer à `conformite-rgpd`.

**Reprises possibles d'Anthropic** (`legal/skills/review-contract/SKILL.md`, commit `33eeda1`, Apache-2.0) :
- L71-86, table des 12 catégories de clauses : à reprendre comme liste de contrôle des clauses absentes, sans les entrées propres au droit américain (jury waiver, class action, L178-186).
- L198-240, vert / orange / rouge avec exemples chiffrés (plafond de 6 contre 12 mois, préavis de 60 contre 90 jours) : adapter les seuils comme ci-dessus, et ajouter les rouges de droit français (clause de la liste noire, délai de paiement au-delà de L441-10, CPC 48 contre un non-commerçant).
- L263-271, format « clause / texte actuel / proposition / raison / priorité / repli » : à reprendre pour `negotiation_points`.
- Crédit à ajouter dans `THIRD_PARTY.md` : la ligne `cgv-checker` (depuis 1.3.0), avec la catégorisation des clauses, les seuils vert / orange / rouge et le format de redline, adaptés au droit français.

**Contraintes à reformuler**

| Texte actuel | Reformulation proposée |
|---|---|
| « You never replace professional legal advice. » + « You must always recall this limit… » (règle absolue) + la même chose en Definition of done | Une seule ligne de livrable : « This review orients a lawyer's review and is not legal advice. » La raison, pour le corps : l'utilisateur pourrait signer ou publier sur cette seule base. |
| « never affirm that a clause is valid or invalid with certainty without reservation » | « State the rule and the fact it depends on: "réputée non écrite if the customer is a consumer (R212-1 3°)". Validity turns on facts the text does not show (who the parties are, whether the clause was negotiated), so name the fact rather than hedge. » |
| « Do not produce a generic analysis outside the provided text. » | « Anchor every finding on a quoted clause and its number; a finding about something absent goes in a separate "missing clauses" list. A finding that cites no clause cannot be negotiated. » |
| « Do not present a negotiation point as settled. » | « Give each point a fallback position: the other side may refuse, and the user needs to know what to accept instead. » |
| « Do not forget liability limitation, termination, and applicable law clauses. » | « Always check, present or absent: liability, termination and renewal, payment and late penalties (B2B), withdrawal and legal guarantees (B2C), jurisdiction and law, data, amendment of the terms. » |

**Défauts à corriger**
- `niveau_detail` (flash / standard / complet) est déclaré dans `.mystaffy.json` sans être défini dans le corps. À définir : flash = les 5 constats les plus graves sans repli ; standard = tous les constats avec repli ; complet = ajouter les clauses absentes et l'article cité par ligne.
- La règle « RAS » doit dire pourquoi elle existe (des CG équilibrées sont un résultat) et rester compatible avec la liste noire : une clause de la liste noire n'est jamais « RAS ».

**Exemple de forme à ajouter.** Un seul constat B2C, sur une clause qui n'est pas dans le cas de test (par exemple une clause « le vendeur seul apprécie la conformité du produit livré », R212-1 4°). Il contient : la clause citée avec son numéro, la qualification « liste noire, 4° → réputée non écrite (L241-1) », la conséquence pratique, la reformulation proposée, et une phrase qui dit pourquoi le constat est utile (il nomme la liste et le numéro, et ne se contente pas de « déséquilibré »).

**Cas de test**

> Je lance ma boutique en ligne de cosmétiques bio (SAS, 3 salariés, vente aux particuliers uniquement). Voici mes CGV, relis-les côté vendeur avant publication lundi. Dis-moi ce qui ne passera pas et comment corriger.
>
> Art. 3 Prix — Les prix peuvent être modifiés à tout moment par le Vendeur, y compris pour les commandes déjà validées en cas de hausse du coût des matières premières.
> Art. 5 Livraison — Les délais de livraison sont donnés à titre indicatif. Aucun retard ne peut donner lieu à annulation de la commande ni à indemnité.
> Art. 6 Rétractation — Le client dispose de 7 jours à compter de sa commande pour se rétracter, par courrier recommandé. Les frais de retour et des frais de dossier de 5 € restent à sa charge.
> Art. 8 Responsabilité — La responsabilité du Vendeur est exclue pour tout dommage, direct ou indirect, lié à l'utilisation des produits.
> Art. 9 Force majeure — Aucune partie n'est responsable d'un manquement dû à un cas de force majeure au sens de l'article 1218 du Code civil.
> Art. 11 Litiges — Tout litige relève de la compétence exclusive du Tribunal de commerce de Lyon. Le droit français est applicable.

Une bonne sortie :
1. Qualifie le contrat en B2C et applique L212-1 / R212-1 / R212-2, pas l'art. 1171.
2. Art. 3 : liste noire, R212-1 3° (modification unilatérale du prix), donc réputée non écrite (L241-1).
3. Art. 5 : la clause qui interdit l'annulation et l'indemnité relève de la liste noire (R212-1 6° et 7°) ; la date indicative relève de la liste grise (R212-2 7°) ; elle rappelle le délai supplétif de 30 jours (L216-1).
4. Art. 6 : 14 jours (L221-18), courant à la réception pour des biens ; pas de frais de dossier ; aucun formalisme imposé (recommandé). **La fonctionnalité de rétractation en ligne est obligatoire depuis le 19/06/2026 (L221-21).**
5. Art. 6 : elle signale l'exception des produits descellés non renvoyables pour hygiène (L221-28 5°) comme une option légitime à rédiger.
6. Art. 8 : liste noire, R212-1 6°.
7. Art. 9 : **aucun constat** (clause conforme à 1218).
8. Art. 11 : la clause attributive est réputée non écrite contre un consommateur (CPC 48), et le tribunal de commerce n'est pas le juge du consommateur ; elle propose de supprimer ou de réécrire la clause.
9. Clauses absentes : le médiateur de la consommation (L616-1) et la garantie légale de conformité de 2 ans (L217-3).
10. Elle distingue la liste noire (irréfragable) de la liste grise (preuve contraire possible), et propose pour chaque constat une rédaction corrigée.
11. La mise en garde juridique n'apparaît qu'une fois.

Échoueraient probablement avec 1.2.1 : 4 (fonction de rétractation 2026), 7 (constat sur une clause conforme), 10 (noire / grise avec numéros), 9 (médiateur absent).

---

### B2. `contrat-fournisseur` (1.2.1 → 1.3.0)

**Ce qui ne tranche pas Q11.** La fusion avec `cgv-checker` et le sort du mode rédaction restent ouverts. La fiche propose une seule chose : **aligner la description sur le corps**, c'est-à-dire l'analyse d'un contrat côté acheteur, en retirant « ou rédige » et le déclencheur « rédige un contrat fournisseur pour ce sous-traitant » (FR, EN, README.md, README-fr.md). Ce retrait est compatible avec les deux issues de la revue (retirer la promesse, ou en faire un manque du catalogue). On n'ajoute **aucune méthode de rédaction** au corps. Si Amiel décide plus tard de garder le mode rédaction, il faudra l'écrire.

**Savoir à ajouter** (ce que l'acheteur français doit savoir et que le modèle omet)

| Point | Ce que le texte impose | Source | URL | Statut |
|---|---|---|---|---|
| Ce que l'acheteur ne peut pas négocier | Délai de paiement ≤ 60 jours après la facture, ou 45 jours fin de mois si c'est expressément stipulé. Procédure d'acceptation ≤ 30 jours, sans décaler le point de départ du délai sauf stipulation expresse non abusive. **Ne jamais proposer plus long** : l'amende va jusqu'à 2 M€ pour une personne morale. | C. com. L441-10 ; L441-16 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053151445 · https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043750778 | vérifié 2026-10-16 |
| L'acheteur aussi peut être l'auteur | Déséquilibre significatif imposé au fournisseur (I 2°), appels d'offres répétés (I 6°, **depuis le 20/08/2026**), rupture brutale (II), réduction substantielle des volumes (II al. 2, **depuis le 20/08/2026**). Les contre-propositions de l'acheteur ne doivent pas tomber dans ces cas. | C. com. L442-1 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000054716237 | vérifié 2026-10-16 |
| Pas d'art. 1171 entre professionnels | Le déséquilibre se plaide sous L442-1, pas sous 1171 (voir la jurisprudence de B1). | Cass. com. 13/05/2026 n° 24-17.137 | https://www.legifrance.gouv.fr/juri/id/JURITEXT000054167043 | vérifié 2026-10-16 (résumé) |
| Obligation de vigilance | Pour tout contrat d'au moins 5 000 € HT : se faire remettre, à la signature puis tous les 6 mois, l'attestation URSSAF de moins de 6 mois (dont on vérifie l'authenticité) et un extrait Kbis ou équivalent. Sans ces pièces, l'acheteur est solidaire des impôts, cotisations et salaires dus en cas de travail dissimulé. | C. trav. L8222-1, R8222-1, D8222-5, L8222-2 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000024197683 · https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030422273 · https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046078939 | vérifié 2026-10-16 |
| Vigilance sur les sous-traitants acceptés (à venir) | **À partir du 26/12/2026**, le maître de l'ouvrage vérifie aussi périodiquement les sous-traitants qu'il accepte (loi 1975-1334, art. 3), et la solidarité s'étend à ce cas. | C. trav. L8222-1-1 et L8222-2, issus de la loi 2026-534 du 25/06/2026, art. 95 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000054335512 | vérifié 2026-10-16 (version à venir) |
| Plafond et faute lourde | La limitation ne joue pas en cas de faute lourde ou dolosive ; une clause qui vide l'obligation essentielle est réputée non écrite (le cas d'un crédit de service dérisoire comme « seule réparation » d'une indisponibilité est à confirmer avec un avocat). | C. civ. 1231-3, 1170 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032010127 · https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041115 | vérifié 2026-10-16 ; application au cas SaaS : **interprétation** |
| Pénalités | Le juge peut modérer une pénalité manifestement excessive ou dérisoire, ce qui vaut aussi pour la pénalité qui protège l'acheteur. | C. civ. 1231-5 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032010131 | vérifié 2026-10-16 |
| Durée ferme | Un CDD s'exécute jusqu'à son terme et nul ne peut exiger le renouvellement : une durée ferme longue sans sortie anticipée bloque l'acheteur. | C. civ. 1212 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041402 | vérifié 2026-10-16 |
| Imprévision | Le mécanisme de renégociation peut être écarté par contrat ; vérifier si la clause l'écarte et qui porte le risque. | C. civ. 1195 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041302 | vérifié 2026-10-16 |
| SaaS / cloud : changement de fournisseur | Le contrat prévoit par écrit : un préavis de lancement du changement ≤ 2 mois, une période transitoire ≤ 30 jours avec assistance et continuité, la liste exhaustive des données exportables, une période de récupération ≥ 30 jours, puis l'effacement. | Règlement (UE) 2023/2854 (Data Act), art. 25 | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32023R2854 | vérifié 2026-10-16 (texte d'origine ; aucune modification adoptée trouvée, **non vérifié** au-delà) |
| SaaS / cloud : frais de changement | Jusqu'au 12/01/2027, seuls des frais réduits au coût direct sont permis ; **à compter du 12/01/2027, aucun frais**. Les pénalités de résiliation anticipée doivent être annoncées avant la signature. | Data Act, art. 29 ; application depuis le 12/09/2025 (art. 50) | idem | vérifié 2026-10-16 ; exception des services sur mesure (art. 31) **non vérifiée** |
| Données personnelles | Si le fournisseur traite des données pour l'acheteur, un contrat art. 28 RGPD est exigé : renvoyer à `conformite-rgpd` (étape 6) plutôt que le refaire. | RGPD art. 28 | (déjà sourcé dans `conformite-rgpd`) | — |

**Positions par défaut côté acheteur** (positions de marché, présentées comme telles) :
- Plafond de responsabilité ≥ 12 mois de prix. Hors plafond ou sous un plafond supérieur : violation de données, confidentialité, contrefaçon, et la faute lourde ou dolosive (déjà exclue par la loi).
- SLA : une disponibilité mesurée sur un mois, avec un équivalent en heures (99,5 % = 3 h 36 min sur 30 jours). Les crédits de service ne sont pas la « seule réparation ». Droit de résilier après N mois sous l'objectif.
- Durée : la reconduction par périodes d'un an, avec un préavis ≤ 3 mois ; refuser la reconduction pluriannuelle tacite.
- Prix : une révision indexée (indice nommé) et plafonnée, plutôt qu'une hausse unilatérale libre.
- Sortie : la réversibilité dans un format structuré et couramment utilisé, avec l'assistance (Data Act pour un SaaS).

**Priorités** (remplacent « classés par impact », non défini) : niveau 1 = indispensable, on ne signe pas sans ; niveau 2 = forte préférence ; niveau 3 = monnaie d'échange. Règle : céder du niveau 3 pour obtenir du niveau 2, et ne pas céder de niveau 1 sans arbitrage interne. Chaque point a un repli.

**Reprises possibles d'Anthropic** (`legal/skills/review-contract/SKILL.md`, `33eeda1`) :
- L90-192, points à revoir et problèmes fréquents par clause (responsabilité, garanties, PI, données, durée et résiliation) : lire côté acheteur ; retirer jury waiver, class action et attorney's fees (US) ; remplacer « 72 h for GDPR » par le renvoi à `conformite-rgpd`.
- L198-240, exemples chiffrés vert / orange / rouge : seuils repris ci-dessus.
- L263-271, format de redline avec Priority et **Fallback**.
- L281-306, trois niveaux de priorité et la règle d'échange.
- Crédit `THIRD_PARTY.md` : ligne `contrat-fournisseur` (depuis 1.3.0).
- À ne pas reprendre : `legal/compliance-check` L118-172 (art. 28), déjà couvert par `conformite-rgpd`.

**Contraintes à reformuler**

| Texte actuel | Reformulation |
|---|---|
| Mise en garde ×2 (règle absolue et DoD) | Une ligne de livrable, comme en B1. |
| « never present a clause as acceptable or unacceptable with certainty without reservation » | Même reformulation qu'en B1 : la règle, puis le fait dont elle dépend. |
| « Do not duplicate a generic multi-party analysis. » | Phrase de périmètre : « Read only from the buyer's side; the seller's reading of its own terms is `cgv-checker`. » Sans interdit. |
| « Do not forget exit, liability, and performance clauses. » | Une liste de contrôle positive : SLA et pénalités, responsabilité, durée, reconduction et sortie, réversibilité, prix et révision, sous-traitance, données, vigilance URSSAF, exclusivité. |
| « Do not present a negotiation point as legally settled. » | « Each point gets a fallback », comme en B1. |

**Défauts à corriger**
- Annexe B : la description promet la rédaction (voir plus haut) ; **pas de règle « RAS »**. À ajouter : « RAS — no clause unfavourable to the buyer at the negotiated level. » avec la raison (un contrat équilibré est un résultat). Une obligation légale de l'acheteur (vigilance, délais) reste à rappeler même dans ce cas, sur une ligne.
- `.mystaffy.json` déclare `type_fournisseur` (prestation / logiciel / maintenance / outsourcing / autre), que le corps n'utilise pas. Écrire une ligne par type : logiciel → réversibilité, Data Act, licence ; maintenance → délais d'intervention et de rétablissement ; outsourcing → transfert de personnel (**non vérifié** : art. L1224-1 C. trav., à confirmer avant d'écrire), audit, vigilance ; prestation → livrables, recette ≤ 30 jours (L441-10 III).
- `niveau_detail` non défini, comme en B1.

**Exemple de forme.** Une ligne de renégociation, sur une clause hors cas de test (par exemple une clause d'exclusivité d'achat sur 3 ans) : clause citée, risque acheteur, proposition, repli, niveau de priorité, et une phrase sur ce qui rend la ligne exploitable en réunion (le repli est déjà prêt).

**Cas de test**

> On s'apprête à signer avec un éditeur (SAS française, 12 salariés) un contrat pour un logiciel SaaS de gestion de stock + une prestation d'intégration. Relis-le côté acheteur et dis-moi ce qu'on renégocie, par ordre de priorité. Signature prévue le 1er novembre 2026.
> - Abonnement : 48 000 € HT/an, durée ferme 3 ans, puis reconduction tacite par périodes de 3 ans sauf dénonciation 6 mois avant l'échéance.
> - Intégration : forfait 15 000 € HT.
> - Paiement à 60 jours date de facture.
> - SLA : disponibilité 99,5 % mesurée par mois ; crédit de service de 5 % de la redevance mensuelle par tranche de 0,5 point sous l'objectif, plafonné à 10 % de la redevance mensuelle. « Les crédits de service constituent la seule et unique réparation du Client en cas d'indisponibilité. »
> - Responsabilité : « plafonnée aux sommes effectivement payées par le Client au cours des trois mois précédant le fait générateur ».
> - Prix : « révisable chaque année par le Prestataire ».
> - Hébergement : « par un sous-traitant choisi par le Prestataire, pouvant être situé hors de l'Union européenne ». Le logiciel contiendra les fiches de nos clients (particuliers). Pas d'annexe données personnelles.
> - Fin de contrat : « les données sont restituées sur demande, dans un format choisi par le Prestataire, moyennant facturation au temps passé (1 200 € HT par jour) ».

Valeurs de référence : redevance mensuelle 4 000 € HT ; plafond de responsabilité = 12 000 € HT, soit 25 % de l'annuel et environ 7,5 % de l'engagement total (144 000 + 15 000 = 159 000 € HT) ; 99,5 % sur 30 jours = 3 h 36 min d'indisponibilité tolérée ; crédit maximal 400 €/mois, 4 800 €/an ; si le contrat court du 01/11/2026 au 31/10/2029, la dénonciation doit partir au plus tard le 30/04/2029.

Une bonne sortie :
1. Calcule le plafond (12 000 € HT) et le rapporte à l'annuel et à l'engagement total ; propose ≥ 12 mois avec des exclusions (données, confidentialité), et rappelle que la faute lourde ou dolosive n'est pas plafonnable (1231-3), sans en dire plus que le texte.
2. Traduit 99,5 % en environ 3 h 36 min par mois et le crédit maximal en 400 €/mois ; signale la clause de « seule réparation », avec l'art. 1170 présenté comme **interprétation à confirmer**.
3. Signale l'enfermement de la reconduction triennale avec un préavis de 6 mois, donne la date limite de dénonciation (30/04/2029) et propose une reconduction annuelle avec un préavis ≤ 3 mois.
4. **Fin de contrat : applique le Data Act (préavis ≤ 2 mois, transition ≤ 30 jours, récupération ≥ 30 jours, aucun frais de changement à compter du 12/01/2027) et demande un format structuré.**
5. Données clients : absence de contrat art. 28 et hébergement hors UE non nommé = niveau 1 ; renvoie à `conformite-rgpd` sans refaire l'analyse RGPD.
6. **Vigilance : l'intégration (15 000 € HT) et l'abonnement dépassent 5 000 € HT, donc il faut l'attestation URSSAF et le Kbis à la signature puis tous les 6 mois (L8222-1, R8222-1, D8222-5).**
7. Ne fait aucun constat sur le paiement à 60 jours et ne propose pas de délai plus long (L441-10).
8. Propose une révision de prix indexée et plafonnée.
9. Classe chaque point en niveau 1 / 2 / 3, avec un repli pour chacun.
10. Cite pour chaque constat le texte du contrat, le risque pour l'acheteur et la proposition, séparément.
11. Une seule ligne de mise en garde.

Échoueraient probablement avec 1.2.1 : 4 (Data Act), 6 (vigilance URSSAF), 9 (niveaux et repli), sans doute 2 (conversion en heures).

---

### B3. `legal-risk-flag` (1.2.1 → 1.3.0)

**Pourquoi il garde un format court.** C'est un tri en un passage, revendiqué (revue : « une chaîne trahirait sa raison d'être »). On ne l'allonge pas avec des modèles de mémo ou de registre (KWP L155-228, à ne pas reprendre). On lui donne ce qui rend le tri fiable : des ancres, des déclencheurs et des repères de délai.

**Ancres de niveau** (adaptées de `legal/skills/legal-risk-assessment/SKILL.md` L18-36, `33eeda1` : les 5 niveaux de gravité KWP sont ramenés aux 3 niveaux ix ; KWP 1-2 → bas, 3 → moyen, 4-5 → haut ; la probabilité abaisse d'un cran seulement si elle est « remote »).
- **Haut** : un montant en jeu > 25 % de la valeur du contrat ou de l'enjeu, ou illimité ; ou un délai dans le document qui éteint un droit ou déclenche une résiliation sous 30 jours ; ou une exposition pénale ou réglementaire (sanction administrative, notification obligatoire) ; ou une clause dont l'utilisateur dépend et que la loi répute non écrite.
- **Moyen** : 5 à 25 % de la valeur ; un écart négociable par rapport au marché ; une ambiguïté sur une obligation essentielle.
- **Bas** : < 5 % ; un écart de forme ; un point facile à corriger.

La raison à écrire : sans ancre, « moyen » se décide au hasard et le seuil RAS fait sous-déclarer (G3, S8). Les pourcentages de KWP sont plus fins (1 / 5 / 25 %) ; ix les regroupe parce qu'un tri rapide n'a besoin que de trois niveaux.

**Une seule échelle de certitude, en mots, pas en haut / moyen / bas** : « texte clair » / « interprétation » / « dépend de faits absents du document ». Elle remplace le champ « certainty level: high / medium / low », qui doublait le niveau de risque (R7).

**Déclencheurs d'avocat sans délai** (adaptés de KWP L230-239) : assignation ou procédure en cours ; contrôle ou enquête d'une autorité (CNIL, DGCCRF, URSSAF, inspection du travail, AMF) ; exposition pénale de la société ou d'un dirigeant ; information privilégiée d'une société cotée (MAR) ; décision qui relève de l'organe de direction ou de l'assemblée. Retirer « securities filings » et « board » au sens américain.

**Signaux français fréquents** (table courte dans le corps, une ligne chacun ; les sources sont détaillées en B1 et B2) :

| Signal | Règle | Source | Statut |
|---|---|---|---|
| Clause qui vide l'obligation essentielle | Réputée non écrite | C. civ. 1170 | vérifié 2026-10-16 |
| Déséquilibre significatif | Entre professionnels : L442-1 I 2°, pas 1171 (Cass. com. 13/05/2026) ; consommateur : L212-1 et listes R212-1/-2 ; autres contrats d'adhésion : 1171 | voir B1 | vérifié 2026-10-16 |
| Exclusion de responsabilité | Inefficace en cas de faute lourde ou dolosive | C. civ. 1231-3 | vérifié 2026-10-16 |
| Clause pénale | Modérable par le juge, encourue après mise en demeure | C. civ. 1231-5 | vérifié 2026-10-16 |
| Clause résolutoire / mise en demeure | La clause précise les engagements visés ; la mise en demeure la mentionne expressément | C. civ. 1225 | vérifié 2026-10-16 |
| Mise en demeure de payer | Sommation ou acte valant interpellation suffisante | C. civ. 1344 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032042162 · vérifié 2026-10-16 |
| Suspension de ses propres prestations | Possible seulement si l'inexécution de l'autre est suffisamment grave | C. civ. 1219 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041509 · vérifié 2026-10-16 |
| Juridiction choisie contre un non-commerçant | Réputée non écrite | CPC 48 | vérifié 2026-10-16 |
| Délais de paiement B2B | ≤ 60 jours ou 45 jours fin de mois ; pénalités ≥ 3 × taux légal ; 40 € par retard | C. com. L441-10, D441-5 | vérifié 2026-10-16 |
| Engagement sans terme | Résiliable à tout moment avec préavis | C. civ. 1210 (vérifié dans le pilote `nda-draft`) | vérifié 2026-10-16 (pilote) |
| Prescription | 5 ans à compter du jour où l'on a connu ou dû connaître les faits | C. civ. 2224 | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019017112 · vérifié 2026-10-16 |

Règle de délai à écrire : toute date ou tout délai du document est calculé en jours calendaires, avec la date d'échéance. Si le point de départ est ambigu (envoi ou réception), on donne les deux dates et on prend la plus proche pour fixer le niveau. La raison : un délai manqué est la perte la plus fréquente, et elle est irréversible.

**Contraintes à reformuler**

| Texte actuel | Reformulation |
|---|---|
| « You never replace… » + « You must always explicitly recall… » + DoD | Une ligne de livrable. |
| « you must say so explicitly and not overplay certainty » + « You must explicitly distinguish… » | Elles fusionnent dans le champ « fiabilité de la lecture » (3 valeurs), qui oblige à dire d'où vient le signal. |
| « RAS … do not pad with low-level generalities » | « Output RAS when nothing reaches medium on the anchors above. The reader is deciding in minutes whether to escalate, and a list of low items hides the one that matters. A deadline under 30 days is never low. » |
| « Do not produce an exhaustive clause-by-clause redline analysis. » | « Keep to the 7 most important signals at most; a full clause review is `cgv-checker` or `contrat-fournisseur`. » |
| « Do not ignore uncertainties or grey areas. » | Couvert par la fiabilité de la lecture. |
| « Do not use an alarmist tone if the risk simply needs confirmation. » | « When the signal depends on a missing fact, say which fact and set the action to "verify", not "submit to counsel". » |

**Défauts à corriger**
- `.mystaffy.json` : `type_document` (auto / contrat / cgv_cgu / courrier / accord / politique) et `niveau_detail` ne sont pas définis dans le corps. Écrire une ligne par type de document. Pour un **courrier**, chercher d'abord les délais, les montants réclamés, la clause invoquée et la menace d'action ; pour une **politique**, chercher les écarts avec la loi applicable. Écrire aussi : flash = 3 signaux au plus ; standard = 7 ; complet = 7 plus les questions à l'avocat.
- Le corps dit « read the full document before flagging risks » sans la raison. Ajouter : les clauses interagissent, un plafond pouvant neutraliser une indemnisation (raison donnée par KWP review-contract L67).

**Reprises possibles d'Anthropic** (`legal/skills/legal-risk-assessment/SKILL.md`, `33eeda1`) : L18-26 (gravité), L28-36 (probabilité), L78-81 / L98-102 / L120-125 / L145-151 (un exemple par niveau, à franciser : « indemnisation illimitée » → « garantie sans plafond ni durée »), L230-239 (déclencheurs). À ne pas reprendre : les actions recommandées par couleur (L72-76, L90-96, L111-118, L134-143), qui sont du conseil de gestion générique, ni « selecting outside counsel » (L256-265). Crédit `THIRD_PARTY.md` : ligne `legal-risk-flag` (depuis 1.3.0).

**Exemple de forme.** Un signal complet sur un document autre que le cas de test (par exemple une clause de non-concurrence d'un contrat d'agent), avec : sujet, niveau (justifié par l'ancre), pourquoi, conséquence probable, fiabilité de la lecture, action. Plus une phrase qui dit pourquoi le niveau est défendable (l'ancre est nommée).

**Cas de test**

> Scan rapide, j'ai 10 minutes avant un call. Courrier reçu le 14 octobre 2026 de notre éditeur de logiciel (abonnement 38 400 € TTC/an), daté du 2 octobre 2026 :
> « Malgré nos relances, les factures F-101 (4 800 € TTC), F-102 (6 400 € TTC), F-103 (3 600 € TTC) et F-104 (3 600 € TTC) restent impayées, soit 18 400 € TTC. Nous vous mettons en demeure de les régler sous 8 jours à compter de la présente, majorées des pénalités de retard au taux de 15 % l'an et de l'indemnité forfaitaire de 40 € par facture. À défaut, nous résilierons le contrat de plein droit en application de son article 12 et suspendrons immédiatement votre accès à la plateforme, sans préjudice de la saisine du tribunal. »
> Article 12 du contrat : « En cas de manquement à l'une quelconque de ses obligations, le contrat pourra être résilié de plein droit huit jours après une mise en demeure restée sans effet. »
> Contexte : on conteste F-103 et F-104 (maintenance de septembre jamais réalisée). F-101 et F-102 ne sont pas contestées, on les a oubliées.

Valeurs de référence : montant contesté 7 200 € TTC ; montant non contesté 11 200 € TTC ; le montant réclamé représente 47,9 % de la valeur annuelle (18 400 / 38 400) ; délai de « 8 jours à compter de la présente » : 10/10/2026 si l'on part de la date du courrier (déjà échu à la réception), 22/10/2026 si l'on part de la réception ; indemnité forfaitaire réclamée 4 × 40 = 160 €.

Une bonne sortie :
1. Met au niveau **haut** le risque de résiliation et de coupure, avec les deux dates possibles (10/10 et 22/10/2026) et la lecture la plus prudente (déjà échu).
2. Recommande de payer sans délai le non contesté (11 200 € TTC) et de contester par écrit, motifs à l'appui, F-103 et F-104 (7 200 € TTC).
3. Note que la mise en demeure vise expressément l'art. 12 (condition de 1225 remplie), et que l'art. 12 vise « l'une quelconque » des obligations : point d'**interprétation** à soumettre à un avocat, sans l'affirmer nul.
4. Ne signale pas l'indemnité de 40 € comme abusive (D441-5), ou au plus comme un point bas.
5. Sur le taux de 15 % : rappelle le plancher (3 × taux légal) et le défaut légal (BCE + 10 points) sans affirmer de chiffre pour le taux légal du second semestre 2026.
6. Mentionne que la suspension de l'accès n'est légitime que si l'inexécution est suffisamment grave (1219), comme argument pour la réponse.
7. Déclenche l'avocat parce qu'une action en justice est annoncée.
8. Reste sous 7 signaux, avec un niveau ancré, une fiabilité de lecture et une action pour chacun.
9. Une seule ligne de mise en garde.

Échoueraient probablement avec 1.2.1 : 1 (calcul des deux échéances), 4 (le 40 € signalé à tort), 7 (pas de déclencheur), 2 (séparation chiffrée contesté / non contesté).

---

### B4. `nda-draft` (1.1.1 → pilote 1.2.0)

Pilote : voir la version 1.2.0 sur le disque, non réévaluée. Cas de test existant : `tests/cas-skills/nda-draft.md` (14 critères). Rien à ajouter ici.

Une seule observation de cohérence de famille, pour le jour où la description de `contrat-fournisseur` changera (B2) : la description du pilote dit encore « N'analyse pas un contrat existant — voir `contrat-fournisseur` ». Pour relire un NDA reçu, le bon renvoi serait plutôt `legal-risk-flag`. Le texte du pilote n'a pas été touché.

---

### B5. `compliance-checklist` (1.1.1 → 1.2.0)

**Règle de date** (à écrire en tête) : « Every obligation is stated as in force on the date of analysis, given at the top of the deliverable. For each text with an application date after that date, give the date. A text that is pending or not transposed is listed as such, never applied. » La raison : plusieurs calendriers ont bougé en 2026 (AI Act, NIS2, facturation électronique), et le modèle ne le sait pas.

**Qualifier la taille d'abord** : effectif, chiffre d'affaires et bilan ; micro (< 10 personnes et ≤ 2 M€), petite, moyenne. La raison : l'accessibilité et le DSA exonèrent les micro et petites entreprises, et NIS2 vise les moyennes et grandes.

**Table domaine → déclencheur** (dans le corps, une ligne par domaine)

| Domaine | Fait déclencheur | Texte et ce qu'il impose | Application / exemption | URL | Statut |
|---|---|---|---|---|---|
| Mentions légales | Tout site ou appli édité à titre professionnel | LCEN art. 1-1 (issu de la loi SREN 2024-449) : identité, immatriculation, directeur de la publication, hébergeur | En vigueur | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049568614 | vérifié 2026-10-16 |
| Cookies et traceurs | Lecture ou écriture sur le terminal | Loi 78-17 art. 82 : information et consentement préalables, sauf traceurs strictement nécessaires. Lignes directrices et recommandation CNIL n° 2020-091 / 2020-092 du 17/09/2020 ; retirer son consentement doit être aussi simple que le donner (délib. 2020-092, art. 3) ; modifiées par la délib. 2025-131 du 18/12/2025 (consentement multi-terminaux) | En vigueur | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037813978 ; délibérations : https://librejustice.fr/norm/fr/deliberation-n-2020-092-du-17-septembre-2020-portant-adoption-d-une/3 , https://librejustice.fr/norm/fr/deliberation-n-2025-131-du-18-decembre-2025-proposant-des-modalites-pratiques-de/1 | art. 82 vérifié ; délibérations vérifiées par extrait ; « refuser aussi simple qu'accepter » **non vérifié mot à mot** |
| Données personnelles | Toute donnée relative à une personne | Une ligne, puis le renvoi à `conformite-rgpd` | — | — | frontière |
| Consommation (vente à distance) | Clients particuliers | Information précontractuelle (L221-5), rétractation 14 jours (L221-18), **fonctionnalité de rétractation en ligne depuis le 19/06/2026 (L221-21)**, médiateur (L616-1), résiliation en ligne (L215-1-1), garantie légale (L217-3) | En vigueur | voir B1 | vérifié 2026-10-16 (L221-5 lu par extrait seulement) |
| Démarchage téléphonique | Appels de prospection vers des consommateurs | **Consentement préalable obligatoire depuis le 11/08/2026** ; exception pour un contrat en cours et un objet lié ; contrat conclu en violation = nul | En vigueur depuis le 11/08/2026 (loi 2025-594) | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051830285 | vérifié 2026-10-16 |
| Accessibilité (privé) | Commerce électronique, banque, télécoms, transport, livres numériques… | C. conso. L412-13 et D412-50 (transposition de la directive (UE) 2019/882) : produits et services conformes aux exigences d'accessibilité | Services fournis après le **28/06/2025** ; **exemption des entreprises de services de moins de 10 personnes avec CA ou bilan ≤ 2 M€** ; charge disproportionnée possible | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047284913 · https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048180184 | vérifié 2026-10-16 |
| Accessibilité (public et grandes entreprises) | Organismes publics ou délégataires ; entreprises au-delà du seuil | Loi 2005-102 art. 47 : déclaration d'accessibilité, schéma pluriannuel, mention en page d'accueil ; seuil privé : CA > 250 M€ (décret 2019-768 art. 2) | En vigueur | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048050213 | art. 47 vérifié ; seuil vérifié par extrait |
| Services numériques (DSA) | Hébergement, plateforme, place de marché | Règlement (UE) 2022/2065 : obligations de tous les intermédiaires (art. 11-15, dont CG art. 14) ; hébergeurs (art. 16-18) ; plateformes (section 3) ; places de marché B2C (section 4) | Applicable depuis le 17/02/2024 (art. 93) ; **sections 3 et 4 non applicables aux micro et petites entreprises** (art. 19, 29), sauf art. 24(3) | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32022R2065 | vérifié 2026-10-16 |
| Plateformes vis-à-vis des pros | Intermédiation pour des entreprises utilisatrices | Règlement P2B (UE) 2019/1150 ; sanction par C. com. L442-1 III | En vigueur | voir B1 | renvoi vérifié ; contenu **non vérifié** |
| Plateformes : information fiscale | Mise en relation en vue de vente ou de service | CGI 242 bis : information sur les obligations fiscales et sociales à chaque transaction, avec lien vers les administrations | En vigueur | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044981558 | vérifié ; déclaration annuelle DAC7 (CGI 1649 ter A) **non vérifiée** |
| IA | Système d'IA mis sur le marché ou utilisé | Règlement (UE) 2024/1689, consolidé au 27/07/2026 après le règlement (UE) 2026/1744 du 08/07/2026 (omnibus IA) : interdictions et maîtrise de l'IA (art. 4) depuis le 02/02/2025, nouvelles interdictions art. 5(1) b bis / b ter le **02/12/2026** ; modèles à usage général depuis le 02/08/2025 ; transparence art. 50 depuis le **02/08/2026** (systèmes génératifs déjà sur le marché : art. 50(2) au plus tard le 02/12/2026, art. 111(4)) ; haut risque annexe III **le 02/12/2027**, annexe I **le 02/08/2028** | voir colonne précédente | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:02024R1689-20260727 | vérifié 2026-10-16 (art. 4, 50, 111, 113) |
| Cybersécurité (NIS2) | Entité moyenne ou grande d'un secteur des annexes I-II | Directive (UE) 2022/2555. **France : pas de loi de transposition trouvée au 2026-10-16** ; le projet de loi « résilience des infrastructures critiques et renforcement de la cybersécurité » a été adopté par le Sénat et examiné en commission spéciale à l'AN en septembre 2025 | À lister comme « en attente », jamais appliqué | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32022L2555 | vérifié négativement (recherche Légifrance des lois 2026, sans résultat) ; état parlementaire **non vérifié** sur source officielle (presse spécialisée seulement) |
| Produits numériques (CRA) | Produit comportant des éléments numériques mis sur le marché de l'UE | Règlement (UE) 2024/2847 : **déclaration des vulnérabilités activement exploitées depuis le 11/09/2026** (art. 14) ; le reste le 11/12/2027 | voir colonne précédente | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:02024R2847-20241120 | vérifié 2026-10-16 (art. 71) |
| Données des objets connectés et cloud | Produit connecté, service de traitement de données | Règlement (UE) 2023/2854 (Data Act) : applicable depuis le 12/09/2025 ; conception de l'accès aux données pour les produits mis sur le marché après le **12/09/2026** ; changement de fournisseur cloud (art. 25, 29 : plus aucun frais à compter du 12/01/2027) | voir colonne précédente | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32023R2854 | vérifié 2026-10-16 (art. 25, 29, 50) |
| LCB-FT | Activité de la liste (banque, paiement, crypto, assurance, immobilier, art, métaux précieux, experts-comptables, avocats, domiciliation, agents sportifs…) | CMF L561-2 : liste des assujettis. Cette version prend fin le 09/07/2027, avec l'application du règlement (UE) 2024/1624 (AMLR) | En vigueur | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000054616568 | vérifié 2026-10-16 ; contenu AMLR **non vérifié** |
| Facturation électronique | Ventes entre assujettis à la TVA établis en France | Loi 2022-1157 art. 26 III (modifiée par la LF 2026-103) : émission électronique pour les factures émises **à partir du 01/09/2026** (grandes entreprises et ETI) et **du 01/09/2027** (PME et micro), report possible par décret jusqu'au 01/12/2026 et au 01/12/2027 ; réception obligatoire pour tous dès le 01/09/2026 | voir colonne précédente | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053546715 | dates d'émission vérifiées 2026-10-16 ; réception pour tous au 01/09/2026 **non vérifiée article par article** ; publication d'un décret de report **non vérifiée** |
| Vigilance sous-traitants | Achat de prestation ≥ 5 000 € HT | C. trav. L8222-1 et suivants (voir B2) | En vigueur ; extension au 26/12/2026 | voir B2 | vérifié 2026-10-16 |
| Sectoriel | Santé, paiement, assurance, jeux, énergie, transport… | Pointer le régulateur (ARS / HAS, ACPR, AMF, ANJ, CRE…) et marquer « à confirmer » ; ne pas énumérer d'articles non vérifiés | — | — | pointeurs seulement |

**Échelle de statut** (la règle absolue actuelle dit « probable / certain / hypothèse » sans les définir) : « applicable » (le fait déclencheur est dans la demande) / « probable » (le fait est vraisemblable mais absent) / « à confirmer » (dépend d'une information manquante, qu'on nomme) / « hors champ » (exemption ou seuil, avec la raison). **Priorité** : P1 = due avant le lancement ou déjà en vigueur et sanctionnée ; P2 = date d'application dans les 12 mois ; P3 = bonne pratique ou exemption à surveiller (passage d'un seuil).

**Reprises possibles d'Anthropic** (`legal/skills/compliance-check/SKILL.md`, `33eeda1`) : L29-63, le gabarit de sortie (verdict « Proceed / Proceed with conditions / Requires further review », table des exigences avec statut, risques, actions, **validations nécessaires** : qui doit signer). Le contenu réglementaire (CCPA, HIPAA, L88-116) est américain et ne se reprend pas. Crédit `THIRD_PARTY.md` : ligne `compliance-checklist` (depuis 1.2.0), gabarit de sortie.

**Contraintes à reformuler**

| Texte actuel | Reformulation |
|---|---|
| Mise en garde ×2 | Une ligne de livrable. |
| « distinguish what must be verified from what appears already compliant » + « probable obligations, certain obligations… » | L'échelle de statut ci-dessus, qui les définit. |
| « Do not reduce compliance to GDPR if the context is broader. » | « Personal data get one line and a pointer to `conformite-rgpd`; spend the checklist on the other domains, which no other skill covers. » |
| « Do not present a generic checklist as exhaustive for all sectors. » | « End with "Not examined": the sectors and countries the input did not let you assess. » |
| « Do not turn contextual hypotheses into certain obligations without reservation. » | Couvert par l'échelle : chaque item « probable » ou « à confirmer » nomme le fait manquant. |

**Défauts à corriger**
- L'étape 1 ne nomme aucun domaine (revue) : elle est remplacée par la table.
- `.mystaffy.json` : `contexte_reglementaire` propose `rgpd`, ce qui contredit la frontière de la description ; proposer de retirer cette valeur, ou de la faire router vers `conformite-rgpd`. La valeur `travail` n'a aucun contenu dans le corps : la garder comme « à confirmer, droit du travail non couvert ici » ou la retirer. `niveau_priorisation` (essentiel / standard / approfondi) est à définir : essentiel = P1 seulement ; standard = P1-P2 ; approfondi = tout, avec les textes en attente.
- La règle « RAS » ne s'applique pas telle quelle : un projet a toujours au moins les mentions légales. Écrire à la place : « if the input does not say what is launched, to whom and where, ask those three questions instead of producing a checklist ».

**Exemple de forme.** Une ligne de checklist, sur un domaine absent du cas de test (par exemple le CRA pour un objet connecté) : domaine, fait déclencheur relevé dans la demande, texte et article, date d'application, statut, priorité, action. Plus une phrase sur ce qui la rend juste (la date est donnée, et le fait déclencheur est cité).

**Cas de test**

> On lance en janvier 2027 une plateforme web + appli mobile de cours particuliers : des parents (particuliers) réservent et paient en ligne des cours donnés par des profs indépendants (auto-entrepreneurs). On prend une commission de 15 % qu'on facture aux profs. Paiement via Stripe. Un chatbot basé sur un modèle d'IA tiers recommande un prof selon le besoin de l'enfant. Nous : SAS, 8 salariés, CA 2025 de 1,2 M€, total de bilan 0,9 M€. Fais-moi la checklist conformité avant lancement.

Une bonne sortie :
1. Pose la date de référence et la taille : micro-entreprise (8 personnes, ≤ 2 M€).
2. **Accessibilité : l'exemption de L412-13 s'applique** (services, < 10 personnes, CA ≤ 2 M€). L'art. 47 de la loi 2005 ne s'applique pas (seuil de 250 M€). Statut « hors champ », avec la raison et le seuil à surveiller.
3. **DSA : plateforme en ligne et place de marché B2C ; les art. 11-18 s'appliquent (CG art. 14, signalement art. 16) ; les sections 3 et 4 sont écartées pour une micro ou petite entreprise (art. 19, 29), sauf art. 24(3).**
4. Information fiscale et sociale des profs à chaque transaction (CGI 242 bis) ; P2B vis-à-vis des profs.
5. Consommation : CGV/CGU B2C, rétractation (14 jours, exception des services pleinement exécutés avec accord exprès, L221-28 1°), **fonctionnalité de rétractation en ligne (L221-21, depuis le 19/06/2026)**, médiateur ; il signale que la qualité de vendeur (plateforme ou prof) est à préciser.
6. LCEN art. 1-1 et cookies (art. 82 + CNIL).
7. Données personnelles, dont celles d'enfants : une ligne et le renvoi à `conformite-rgpd`, sans analyse RGPD détaillée.
8. **IA : transparence art. 50(1) applicable depuis le 02/08/2026 (le chatbot doit annoncer qu'il est une IA) ; maîtrise de l'IA (art. 4) ; pas de haut risque a priori (annexe III, éducation : à confirmer) ; rôle de fournisseur ou de déployeur à confirmer.**
9. **Facturation électronique : les factures de commission aux profs entrent dans le champ si ces derniers sont assujettis ; réception à partir du 01/09/2026 et émission obligatoire pour une micro-entreprise à partir du 01/09/2027.**
10. Encaissement pour le compte des profs : service de paiement réglementé, sauf montage avec un prestataire agréé, statut « à confirmer », sans article inventé.
11. **NIS2 : hors champ (taille) et non transposée en France au 2026-10-16.**
12. Chaque item a un statut et une priorité définis, et la sortie finit par « non examiné ».

Échoueraient probablement avec 1.1.1 : 2 (exemption d'accessibilité), 3 (exemptions DSA), 8 (calendrier AI Act 2026), 9 (dates de facturation électronique), 11 (état de NIS2).

---

### B6. `conformite-rgpd` (1.3.0 → 1.3.1)

**Verdict.** La longueur est du savoir (G1) ; la réécriture est légère. Ne rien reprendre de KWP : `legal/compliance-check` L208-216 donne « 30 jours » pour les demandes de droits, alors que l'art. 12(3) prévoit un mois prorogeable de deux. Le skill est déjà juste sur ce point.

**Savoir à ajouter ou à dater**

| Point | Règle | Source | URL | Statut |
|---|---|---|---|---|
| Démarchage téléphonique | **Depuis le 11/08/2026**, il est interdit de démarcher par téléphone un consommateur sans son consentement préalable (acte positif, preuve à la charge du pro) ; exception pour un contrat en cours et un objet lié ; contrat conclu en violation = nul. À traiter comme un point séparé, comme L34-5 CPCE et les cookies (les données collectées restent soumises au RGPD). | C. conso. L223-1 (loi 2025-594, art. 13) | https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051830285 | vérifié 2026-10-16 |
| Paragraphe « omnibus » | Au 2026-10-16, les art. 30 et 33 RGPD sont inchangés dans le texte consolidé ; aucune modification adoptée n'a été trouvée. Garder la règle « une proposition ne s'applique pas » et dater la phrase (« as checked on 2026-10-16 »). | RGPD art. 30, 33 | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:02016R0679-20160504 | articles vérifiés 2026-10-16 ; état d'adoption des propositions **non vérifié** |
| Cookies multi-terminaux | La recommandation CNIL 2020-092 a été modifiée par la délib. 2025-131 du 18/12/2025 (consentement multi-terminaux). Une phrase dans le point séparé « cookies ». | CNIL | https://librejustice.fr/norm/fr/deliberation-n-2025-131-du-18-decembre-2025-proposant-des-modalites-pratiques-de/1 | existence vérifiée 2026-10-16 ; contenu **non vérifié** |
| DPF | Le skill dit « adéquation limitée aux destinataires certifiés DPF » : c'est juste. Le sort du recours contre la décision d'adéquation (affaire Latombe, T-553/23) au 2026-10-16 **n'a pas été vérifié** ; ajouter « vérifier que la décision d'adéquation est toujours en vigueur à la date d'analyse ». | — | — | non vérifié |

**Contraintes à reformuler**

| Texte actuel | Reformulation |
|---|---|
| « Any checklist must be reviewed by a DPO… » + « You always state this limit » + « Always recall the legal limit of the analysis » + DoD (4 occurrences) | Une ligne dans le livrable (« legal disclaimer and reference date » existe déjà dans la structure recommandée). Retirer les trois autres. |
| « Do not present an inference as a legal certainty. » | Déjà couvert par « observed / inferred / to confirm » ; supprimer. |
| « put them in the controller's column, never in the processor's to-do list » | Garder, sans « never » : « …in the controller's column: the processor cannot act on them, and listing them there hides who must. » |
| « never tell a team it is exempt on headcount alone » | Garder (la raison est présente), en minuscules et en forme positive : « state that the record is required ». |
| « Cite articles of the GDPR, not paraphrases from memory » | Ajouter la raison : « the reviewer checks each point against the text in force ». |
| « Never apply a proposal as if it were in force » | « A proposal can change or fail; state it as pending, with the date checked. » |

**Défauts à corriger**
- `.mystaffy.json` : `niveau_detail` (rapide / standard / approfondi) et `contexte_org` (dont `sante` et `public`) ne sont pas lus par le corps. Écrire : rapide = traitements, rôles, bases légales, et les 5 obligations dues dès la première personne (base, information, registre, sécurité, contrat art. 28), avec les priorités ; approfondi = ajoute l'analyse art. 35 et les transferts détaillés. `public` : art. 6(1) dernière phrase (pas d'intérêt légitime pour les missions) et DPO obligatoire (art. 37(1)(a)), déjà dans le corps : y renvoyer. `sante` : art. 9 et AIPD ; l'hébergement de données de santé (HDS, CSP L1111-8) est **non vérifié**, à ne pas écrire sans vérification.
- Rien dans l'annexe B.

**Exemple de forme.** Non nécessaire : la structure de sortie est déjà décrite, et le livrable est une liste.

**Cas de test**

> Check RGPD de notre nouvelle version avant mise en prod le 1er novembre 2026. Appli B2C de coaching sportif (SAS, 25 salariés, France). Inscription dès 13 ans. On collecte : e-mail, téléphone, date de naissance, poids, fréquence cardiaque et sommeil via la montre connectée de l'utilisateur. Nouveauté : un plan d'entraînement généré par IA à partir de ces données. Hébergement AWS (région Francfort), support client sur Zendesk (société américaine), Google Analytics sur le site et dans l'appli. Le marketing veut appeler à partir du 1er novembre les anciens abonnés qui ont résilié pour leur proposer -50 % ; les numéros viennent du formulaire d'inscription, sans case de consentement à la prospection.

Une bonne sortie :
1. Qualifie poids, fréquence cardiaque et sommeil en données de santé (art. 9) et exige une exception art. 9(2), vraisemblablement le consentement explicite (a).
2. Registre requis malgré moins de 250 salariés (art. 30(5) : données art. 9).
3. AIPD : à mener ou à justifier (art. 35, liste CNIL), présentée comme « à confirmer », avec la raison.
4. Utilisateurs de 13-14 ans : art. 8 et art. 45 LIL (15 ans), consentement conjoint avec le titulaire de l'autorité parentale.
5. **Appels aux anciens abonnés : depuis le 11/08/2026, un consentement préalable est obligatoire (C. conso. L223-1) ; l'exception du contrat en cours ne joue pas pour des abonnés qui ont résilié ; le projet n'est pas conforme en l'état ; c'est un point séparé, comme les cookies.**
6. **N'invoque pas Bloctel ou l'opposition comme régime applicable aux appels vers des consommateurs.**
7. Google Analytics : point séparé, art. 82 LIL et CNIL.
8. Zendesk : transfert hors EEE (certification DPF à vérifier, sinon CCT et analyse d'impact) ; AWS Francfort : contrat art. 28 ; chaque sous-traitant est nommé.
9. Procédure de violation de données sous 72 heures (art. 33).
10. Date de référence ; chaque point cite son article ; statut en place / à faire / à confirmer.
11. Une seule mention de la limite juridique.

Échoueraient probablement avec 1.3.0 : 5 et 6 (le skill ne connaît que L34-5, qui vise les appels automatisés, et le modèle ramène les appels humains au régime d'opposition), 11 (mise en garde répétée).

---

## Points listés, non traités (§3 de la revue)

- **Q11 (fusion `contrat-fournisseur` / `cgv-checker`)** : non tranchée. B1 et B2 gardent deux skills, avec une frontière par la position (vendeur ou utilisateur des CG d'un côté, acheteur de l'autre). Le savoir commun (L442-1, 1170, 1231-3, CPC 48) est écrit deux fois en attendant ; si la fusion se fait, il partira dans le partial « jeux de clauses par type de contrat », que la revue a relevé comme manque du catalogue. Le mode rédaction de `contrat-fournisseur` est seulement retiré de la description.
- **Q8 (vérification séparée)** : non tranchée. Les cas de test B1 et B2 contiennent des critères de « clause absente » (médiateur, art. 28, réversibilité), qui sont exactement ce qu'une vérification isolée contrôlerait.
- **Q12** : si l'analyse de `contrat-emploi` passe à `legal-risk-flag`, il faudra une ligne « contrat de travail » dans `type_document` et des déclencheurs de droit du travail (non écrits ici).
- **Q2** : rejouer `conformite-rgpd` avec les réponses de l'équipe produit ; rien à faire dans le skill.
