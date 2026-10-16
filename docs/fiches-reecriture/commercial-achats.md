# Analyse — famille commercial-achats (2026-10-16)

Skills : `analyse-cdc`, `offre-commerciale`, `negotiation-brief`, `rfp-draft`, `vendor-scorecard`, `total-cost-analysis`, `offer-comparison`. Versions lues : commit `cbe271c` (`skills/<id>.md` et `.mystaffy.json`). Aucun de ces skills n'a de `references:`. Grille : `docs/etat-de-l-art-skills.md` (G1–G10, R1–R10). Revue : `docs/revue-skills-metier.md`.

Les articles cités ont été lus le 2026-10-16 avec l'outil de normes (texte Légifrance / EUR-Lex, statut en vigueur à cette date). Deux textes ont changé il y a moins de deux mois et touchent cette famille : **C. com. L442-1**, modifié par la loi n° 2026-796 du 18/08/2026 (appels d'offres répétés, baisse substantielle des volumes) ; **CCP R2152-7**, version en vigueur depuis le 21/08/2026 (au moins un critère environnemental). Le rédacteur doit les reprendre tels quels.

## A. Tableau

| Skill (version) | Lignes · équivalent Anthropic | Pourquoi il a cette longueur | Justifié ou manque | Ce qui change | En attente (§3) |
|---|---|---|---|---|---|
| `analyse-cdc` (1.3.0) | 80 L · partiel : `small-business/grant-rfp-writer` (162 L + 605 L en `reference/`, droit américain) | Gabarit (rôle, règle, 6 verbes de méthode) et une liste de sections que la recette lit. 5 interdits. Aucun savoir sur la lecture d'un dossier de consultation. | **mixte** : la structure est bonne et la recette en dépend ; il manque la manière de lire (exigence éliminatoire ou notée, effet de la formule de prix, pièges du marché public). | Environ 30 lignes de savoir : éliminatoire / noté / informatif, ordre de priorité des pièces, effet de la formule de prix, variantes (R2151-8), critère environnemental (R2152-7), délai de paiement public (R2192-10/11), offre anormalement basse (L2152-5/6), délai des questions (R2132-6). 5 interdits à reformuler. Aucun champ renommé. | — |
| `offre-commerciale` (1.1.0) | 110 L · `small-business/proposal-builder` (168 L + 695 L en `reference/`) | Rôle et règle répétés (« tu rédiges, tu n'expliques pas » dit 4 fois). 8 négations. Aucun savoir propre à une offre. | **manque** : la longueur vient du cadrage et des interdits. Il manque ce qui fait perdre de l'argent ou le marché : exclusions, hypothèses avec leur conséquence, prix en lignes de décision, validité, délais de paiement légaux, effort réparti selon les points des critères. | Ajouter une section « non compris », les hypothèses avec leur conséquence, des lignes de prix, la validité et les conditions de paiement (L441-10, D441-5, R2192-10). Fusionner rôle et règle (R8). Reformuler 8 interdits. Un exemple d'hypothèse avec sa conséquence. | **Q3** : étapes 1, 2 et 4 de la méthode (nature de la réponse, ce qui engage, choix de la position) et réduction à la seule rédaction. |
| `negotiation-brief` (1.1.0) | 83 L · aucun (partiel : `legal/review-contract` L281–306, paliers de négociation) | Gabarit. Nomme BATNA, cible et ligne rouge sans dire comment les calculer. 5 interdits. | **manque** : le modèle connaît les mots, pas la méthode chiffrée (ligne rouge tirée de la BATNA, ZOPA), ni les limites du droit français côté acheteur. | Ajouter : prix de réservation égal au coût complet de la BATNA, ZOPA et plancher supposé du fournisseur, ouverture défendable, concessions échangées, paliers 1/2/3 (repris d'Anthropic). Droit : L441-10 et L441-16, L442-1 (I 1°, 2°, 6° et II), C. civ. 1112 et 1137. Reformuler 5 interdits. Exemple d'une ligne « levier, fait, hypothèse ». | — |
| `rfp-draft` (1.1.0) | 81 L · aucun | Gabarit et plan en 9 titres. 5 interdits. Rien qui rende les offres comparables. | **manque** : sans cadre de réponse ni bordereau de prix, les offres reçues ne se comparent pas (constat de la revue). | Ajouter : cadre de réponse imposé avec matrice de conformité ; bordereau de prix (unités, quantités, ponctuel ou récurrent, options à part, révision, validité) ; test de l'éliminatoire ; critères, pondérations et méthode de notation du prix annoncés ; pièces à demander (vigilance URSSAF, RGPD art. 28) ; reprise du personnel (ex. CCN propreté art. 7) ; préavis au titulaire sortant (L442-1 II). Accepter une grille existante en entrée. Reformuler 5 interdits. | — (si Q12 = oui, la même question se posera ici pour le marché public) |
| `vendor-scorecard` (1.1.0) | 77 L · `operations/vendor-review` (104 L, surtout gabarit) | Gabarit et méthode générique (« construire une grille pondérée »). 5 interdits. | **manque** : rien de ce qu'un acheteur sait et que le modèle rate : formules de notation du prix et leurs effets pervers, pondérations figées avant les offres, éliminatoires hors pondération, dimensions par type d'achat, échelle ancrée. | Ajouter ce savoir dans le corps (environ 45 lignes, propre à ce skill). Un exemple de critère avec échelle ancrée. Retirer le déclencheur « offres reçues » (annexe B). Reformuler 5 interdits. | **Q12** : règles du marché public non ajoutées (R2152-7, R2152-11, R2152-12, critère environnemental obligatoire depuis le 21/08/2026, jurisprudence du Conseil d'État sur les méthodes de notation). |
| `total-cost-analysis` (1.1.0) | 90 L · `operations/vendor-review`, partie coût (environ 20 L) | Gabarit et structure par poste (confirmé / estimé / non chiffré, sensibilité). 6 interdits, dont 3 qui disent la même chose. | **justifié** : déjà plus rigoureux que l'équivalent d'Anthropic ; il manque quelques pièges chiffrés. | Ajouter : HT ou TTC selon que la TVA est récupérée, révision de prix au plafond, fin des remises de première année, coûts internes, double run, réversibilité (RGPD art. 28.3.g), horizon aligné sur l'engagement, actualisation seulement si les calendriers de paiement diffèrent, seuil de bascule. Fusionner les 3 « must » en une consigne. Reformuler 6 interdits. | — |
| `offer-comparison` (1.1.0) | 90 L · `operations/vendor-review`, matrice (environ 5 L) | Gabarit et structure de tableau. 6 interdits. | **mixte** : la structure est bonne ; il manque la notation du prix, la règle contre la repondération après ouverture (annexe B) et la mesure de fragilité du classement. | Ajouter : formules de prix et leurs effets (dont la dépendance au moins-disant) ; une repondération après ouverture devient une sensibilité étiquetée, jamais la grille ; écart de score comparé à l'effet d'un point ; offre non comparable chiffrée avant d'être notée ; défaut quand aucune grille n'existe. Reformuler 6 interdits. Exemple de ligne de conclusion sur la fragilité. | — |

---

## B. Fiches de réécriture

Consignes communes aux sept fiches, pour le rédacteur :

- Corps en anglais, frontmatter canonique, id et périmètre inchangés, convention « RAS — » conservée. Pas de capitales, pas de « règle absolue » quand une raison suffit (G2).
- Le savoir juridique va dans un tableau « Point / Règle / Source » avec la date de vérification (modèle : `skills/nda-draft.md` 1.2.0, déjà réécrit). Ne citer que les articles de cette fiche ; un point marqué « non vérifié » s'écrit sans numéro d'article.
- Aucun partial nouveau : le savoir de chaque skill lui est propre, il reste dans le corps (G5, CLAUDE.md §3bis).
- Toute reprise d'Anthropic : crédit dans `THIRD_PARTY.md` (commit `33eeda1`, Apache-2.0) et commentaire HTML en fin de fichier, comme dans `nda-draft`.
- Le triptyque « observé / hypothèse / recommandation » ne s'écrit qu'une fois par skill, à l'endroit du format où il sert.

---

### B1. `analyse-cdc` (1.3.0 → 1.4.0)

**À ne pas toucher.** C'est l'étape 1 de `reponse-appel-offres`. La recette lit `requirements`, `imposed_items`, `evaluation_criteria`, `submission_rules`, `grey_zones`, `blocking_questions`, plus la fiche de contexte, et les fait correspondre aux sections du « Recommended structure » (le HANDOFF prime). Garder les sections et leur ordre, en particulier « imposed items, copied verbatim » (champ `verbatim` de la recette). On peut **ajouter de l'information à l'intérieur** des sections (une étiquette par exigence, l'effet de la formule de prix dans les critères), pas renommer, fusionner ou créer de section qui devrait être transmise.

**Savoir métier à ajouter.**

| Point | Règle (une phrase) | Source | Vérifié |
|---|---|---|---|
| Éliminatoire ou noté | Étiqueter chaque exigence : *éliminatoire* (« doit », « est exigé », pièce obligatoire), *notée* (« sera apprécié », relié à un critère), *informative*. Raison : l'évaluateur rejette sur un « doit » manqué et ne fait que baisser la note sur un « souhaité ». Confondre les deux tue une offre gagnable ou fait travailler sur une offre morte. | Pratique ; formulation reprise de KWP `grant-rfp-writer/reference/go_no_go.md` L30–45 | — |
| Offre irrégulière (marché public) | Une offre qui ne respecte pas les exigences des documents de la consultation, notamment incomplète, est irrégulière. | CCP art. L2152-2 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037703649/2019-04-01 | vérifié 2026-10-16 |
| Régularisation | L'acheteur *peut* autoriser la régularisation d'une offre irrégulière, sans en modifier les caractéristiques substantielles. Ne pas compter dessus. | CCP art. R2152-2 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037730501/2019-04-01 | vérifié 2026-10-16 |
| Variantes | En procédure formalisée, un pouvoir adjudicateur interdit les variantes sauf mention contraire ; une entité adjudicatrice les autorise sauf mention contraire ; en procédure adaptée, elles sont autorisées sauf mention contraire. Si le dossier se tait, dire ce que vaut ce silence avant que l'offre propose une alternative. | CCP art. R2151-8 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037730527/2019-04-01 | vérifié 2026-10-16 |
| Critère environnemental | Pour les consultations engagées depuis le 21/08/2026, au moins un critère prend en compte les caractéristiques environnementales de l'offre (ou le critère unique du coût les intègre). Un règlement de consultation récent sans critère environnemental est une zone grise à soulever : la correction peut décaler le calendrier. | CCP art. R2152-7, version en vigueur depuis le 21/08/2026 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045739587/2026-08-21 | vérifié 2026-10-16 |
| Questions à l'acheteur | En procédure formalisée, l'acheteur envoie les renseignements complémentaires au plus tard 6 jours avant la date limite des offres (4 en urgence), si la demande a été faite à temps. La date limite des questions du règlement prime ; la noter dans les règles de remise. | CCP art. R2132-6 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037730727/2019-04-01 | vérifié 2026-10-16 |
| Offre anormalement basse | L'acheteur doit demander des justifications à une offre qui semble anormalement basse et la rejeter si elles ne convainquent pas. Le risque prix existe donc dans les deux sens. | CCP art. L2152-5, L2152-6, R2152-3 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037703657/2019-04-01 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037703659/2019-04-01 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037730497/2019-04-01 | vérifié 2026-10-16 |
| Délai de paiement public | 30 jours pour les pouvoirs adjudicateurs ; 50 jours pour les établissements publics de santé ; 60 jours pour les entreprises publiques. Un CCAP qui prévoit plus est une contradiction à relever. | CCP art. R2192-10, R2192-11 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037729711/2019-04-01 ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037729709/2019-04-01 | vérifié 2026-10-16 |
| Pièces d'un dossier public | Règlement de consultation (critères, remise), CCAP (pénalités, paiement, révision des prix), CCTP (technique), bordereau de prix (BPU, DPGF, DQE), acte d'engagement. Chercher la clause d'ordre de priorité entre pièces : c'est elle qui tranche une contradiction. Un DQE « non contractuel » sert à comparer les prix ; un écart avec le CCTP fausse la comparaison. | Pratique (vocabulaire) | — |
| Formule de notation du prix | Si le dossier donne la formule, écrire dans les critères ce qu'elle produit. Linéaire entre l'offre la plus basse et la plus haute : l'offre la plus chère reçoit 0, quel que soit l'écart. Proportionnelle au moins-disant (`note max × Pmin / P`) : courbe, écarts tassés vers le haut, et une offre très basse fait baisser la note de toutes les autres. C'est une donnée de la stratégie de prix, pas un commentaire. | Calcul (voir B5) | — |
| Clauses contractuelles à risque | Pénalités sans plafond, prix fermes sur plusieurs années sans révision, délai de paiement, transfert de propriété intellectuelle, réversibilité. Ce sont les risques de la section « main risks ». | Pratique | — |

Le marché public s'ajoute ici sans trancher Q12 : Q12 porte sur `vendor-scorecard`, côté acheteur ; ce skill lit côté répondant.

**Reprises d'Anthropic.** `small-business/skills/grant-rfp-writer/reference/go_no_go.md` L30–45 (« must » ou « should ») et L49–60 (règles de remise : compter à rebours depuis la date limite, en incluant les signatures et pièces à réunir). Adapter : retirer SAM.gov, NAICS, bonding et toute référence au droit américain.

**Contraintes à reformuler.**

| Citation actuelle | Proposition |
|---|---|
| « You do not produce a summary of the spec — you produce a critical analysis. » | Positive avec raison : produire une lecture critique, parce que l'équipe décide sur cette analyse sans relire le dossier ; un résumé lui laisserait le jugement. |
| « Do not ignore contradictions — flag them explicitly. » | Citer les deux passages et la pièce qui prévaut si le dossier fixe un ordre de priorité. Raison : une contradiction lissée devient une erreur de prix. |
| « Do not present an inference as an explicit requirement. » | Étiqueter chaque exigence explicite ou déduite. Raison : en aval, le contrôle de conformité traite une exigence explicite comme obligatoire. |
| « Do not produce a response plan » | S'arrêter à la lecture, parce que la stratégie de réponse vient après les réponses de l'acheteur (étape 4 de la recette). |
| « never invent one » (pondération) | Écrire « non indiquée » quand la pondération manque. Raison : une pondération inventée fausse le go / no-go. |

Règle absolue, définition de fini et contraintes redisent la même chose : fusionner (R8).

**Défauts d'annexe B.** « Les main risks d'`analyse-cdc` ne sont transmis à aucune étape. » Le défaut est dans la recette, hors périmètre : ne pas le corriger dans le skill, le laisser en note pour le chantier recette.

**Exemple de forme.** Une seule exigence étiquetée, entre balises `<example>` : la phrase du dossier entre guillemets, la pièce et l'article, l'étiquette « éliminatoire », et une phrase qui dit pourquoi (le verbe « doit » et une pièce exigée à la remise). Pas d'extrait du cas de test.

**Cas de test.**

> On est un organisme de formation (12 formateurs, certifié Qualiopi). Analyse ce dossier avant qu'on décide d'y répondre.
> Acheteur : centre hospitalier de Valmont (établissement public de santé). Appel d'offres ouvert, lancé le 2 octobre 2026. Objet : formation au management de proximité pour 120 cadres de santé.
> RC art. 3 : le DQE est fourni à titre indicatif et n'est pas contractuel. RC art. 5 : prix 40 %, note = 40 × (Pmax − P) / (Pmax − Pmin), où Pmin et Pmax sont l'offre la plus basse et la plus haute reçues ; valeur technique 60 % (méthodologie 35, équipe 25). RC art. 7 : questions au plus tard le 26 octobre, remise le 6 novembre à 12 h, mémoire technique limité à 15 pages. Le RC ne dit rien des variantes.
> CCTP art. 2 : 12 sessions de 2 jours, groupes de 10. CCTP art. 4 : le titulaire doit être certifié Qualiopi ; une expérience en milieu hospitalier serait appréciée.
> BPU : prix par session. DQE : 10 sessions.
> CCAP art. 9 : pénalité de 500 € par jour de retard dans la remise des supports, sans plafond. CCAP art. 11 : paiement à 60 jours.

Une bonne sortie contient (« * » : échouerait probablement avec la version actuelle) :

1. La contradiction 12 sessions (CCTP) / 10 sessions (DQE), avec les deux passages, posée en question bloquante ; le constat que 120 cadres en groupes de 10 donnent bien 12 sessions.
2. Le rôle du DQE non contractuel : il sert à comparer les prix, donc l'écart change la note prix de tous les candidats.
3. \* L'effet de la formule : l'offre la plus chère reçoit 0 sur 40 quel que soit l'écart (illustration possible : 30 000, 32 000 et 36 000 € donnent 40 ; 26,7 ; 0).
4. \* L'absence de critère environnemental dans une procédure formalisée lancée après le 21/08/2026 (R2152-7), relevée comme zone grise ou question.
5. \* Le silence sur les variantes lu comme une interdiction (procédure formalisée, pouvoir adjudicateur, R2151-8).
6. \* Le paiement à 60 jours relevé comme contraire au délai de 50 jours d'un établissement public de santé (R2192-11).
7. Qualiopi étiqueté éliminatoire ; l'expérience hospitalière étiquetée notée (méthodologie ou équipe), pas éliminatoire.
8. La pénalité sans plafond dans les risques contractuels.
9. Les règles de remise complètes : 15 pages, 26 octobre pour les questions, 6 novembre à 12 h.
10. Les éléments imposés recopiés mot pour mot (12 sessions de 2 jours, groupes de 10, 120 cadres de santé).
11. Aucune pondération ni exigence inventée, aucun plan de réponse.

---

### B2. `offre-commerciale` (1.1.0 → 1.2.0)

**À ne pas toucher.** Étape 5 de `reponse-appel-offres`. Elle reçoit `context_sheet`, `strategie.response_brief`, `analyse-cdc.imposed_items`, `analyse-cdc.submission_rules` et transmet un seul champ, `offer` (`output_field: offer`). Garder les noms du format (`offre_commerciale`, `hypotheses`, `options`) : la recette fait correspondre. L'étape `mise-en-forme` retire ensuite les annotations internes : les marques d'hypothèse dans l'offre sont attendues.

**En attente Q3, ne pas réécrire** : les étapes 1, 2 et 4 de la méthode (identifier la nature de la réponse, ce qui est assez stable pour engager, retenir une position entre options) et toute réduction du skill à la seule rédaction. Les reformuler en surface seulement (raison ajoutée), sans changer ce qu'elles font.

**Savoir métier à ajouter** (indépendant de Q3).

| Point | Règle | Source | Vérifié |
|---|---|---|---|
| Ce qui n'est pas compris | Une section « non compris » liste tout ce qu'un client raisonnable pourrait croire inclus. Raison : les litiges de périmètre commencent par ce que personne n'a écrit. | KWP `proposal-builder/reference/proposal_structure.md` L23–38 | — |
| Hypothèse et conséquence | Chaque hypothèse de prix est écrite dans le document client avec ce qui se passe si elle tombe (« au-delà de 40 pages, [prix par page] »). Raison : une conséquence nommée transforme un litige en avenant prévu. Une hypothèse connue du seul vendeur ne le protège pas. | KWP `proposal_structure.md` L40–51 ; `gotchas.md` L43–58 | — |
| Lignes de prix | Découper le prix en lignes que le client reconnaît comme des décisions (lots, options), pas en « main-d'œuvre / matériel ». Un prix unique n'appelle qu'une objection. Ne pas inventer une ventilation absente des entrées : laisser la ligne en blanc et la signaler. | KWP `pricing_method.md` L74–94 | — |
| Options | Deux ou trois au plus, la recommandée nommée avec sa raison. Ne jamais proposer une option que le vendeur ne veut pas exécuter. | KWP `pricing_method.md` L98–104 | — |
| Validité | Une date de validité de l'offre ; à défaut d'instruction, un défaut signalé comme tel. | KWP `proposal_structure.md` L11 | — |
| Délai de paiement entre professionnels | Sans accord : 30 jours après réception ou exécution. Convenu : 60 jours au plus après la date de facture, ou 45 jours fin de mois si c'est écrit au contrat. Un délai plus long demandé par le client ne peut pas être accepté. Le dire dans la note interne, pas en leçon dans le document client. | C. com. L441-10 I (version du 01/09/2026 ; règle reprise à l'identique au 01/01/2027) — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053151445/2026-09-01 | vérifié 2026-10-16 |
| Mentions de paiement | Les conditions de règlement indiquent le taux des pénalités de retard (au moins 3 fois le taux d'intérêt légal ; à défaut, taux BCE + 10 points) et l'indemnité forfaitaire de recouvrement de 40 €. L'omission est sanctionnée (amende jusqu'à 2 M€ pour une personne morale). | C. com. L441-10 II ; D441-5 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043197457/2021-02-27 ; L441-16 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043750778/2021-11-01 | vérifié 2026-10-16 |
| Client public | Délai de paiement fixé par la loi (30 jours en général, 50 pour un établissement public de santé, 60 pour une entreprise publique) : ne pas en proposer un autre. | CCP R2192-10, R2192-11 (URL en B1) | vérifié 2026-10-16 |
| Prix bas en marché public | Un prix qui semble anormalement bas oblige l'acheteur à demander des justifications (mode de production, conditions favorables, originalité) et peut entraîner le rejet. Garder la justification prête. | CCP L2152-6, R2152-3 (URL en B1) | vérifié 2026-10-16 |
| Écrire au poids des critères | Répartir l'effort selon les points de chaque critère ; reprendre les mots de l'acheteur dans les titres, pour qu'un évaluateur pressé trouve la réponse. | KWP `grant-rfp-writer/reference/drafting.md` L34–47 | — |
| Références et preuves | Aucune référence client, certification, CV ou chiffre de résultat inventé : marque visible qui dit qui peut répondre et ce qu'il faut. Raison : ces éléments se vérifient, et une offre acceptée engage. | KWP `drafting.md` L59–89 | — |
| Document client et note interne | Deux sorties distinctes : l'offre, en termes neutres ; une note interne courte qui dit franchement ce qui inquiète (prix tendu, hypothèse fragile, demande non conforme du client). | KWP `gotchas.md` L120–130 | — |

**Reprises d'Anthropic** (savoir et gabarit, à créditer) : `small-business/skills/proposal-builder/reference/proposal_structure.md` L23–51 ; `pricing_method.md` L74–104 ; `gotchas.md` L43–58 et L120–130 ; `small-business/skills/grant-rfp-writer/reference/drafting.md` L34–47 et L77–89. Adapter : euros HT, pas de DocuSign ni de connecteur, retirer le False Claims Act, remplacer « net 15 / net 30 » par la règle L441-10.

**Contraintes à reformuler.**

| Citation actuelle | Proposition |
|---|---|
| « You do not limit yourself to explaining how to respond. You write the client response. » (dit aussi dans Role, Constraints et Definition of done) | Une seule phrase dans le rôle (R8). |
| « You never invent figures, timelines, scopes, or commitments without sourcing them… » | Laisser les faits inconnus en marques visibles (`[prix par page]`, `[référence client]`), parce qu'une offre acceptée engage et qu'un chiffre plausible survit à la relecture. |
| « You do not handle final formatting » | « Provide the content; formatting is done afterwards (`deliver`, or the user) ». |
| « Do not produce an abstract response strategy instead of the response. » | Supprimer : redit le rôle. |
| « Do not produce a simple CDC audit. » | Supprimer : la frontière est dans la description. |
| « Do not overwhelm the reader with only risks and open questions. » | Les risques pour le vendeur vont dans la note interne ; dans l'offre, ils deviennent des hypothèses avec leur conséquence. |
| « Do not transform the offer into a strategic note or stakeholder communication. » | Supprimer : redit le rôle. |
| « without meta-commentary on how to respond » | Garder, avec la raison : le client lit ce document. |

**Exemple de forme.** Une hypothèse écrite pour le client avec sa conséquence chiffrée ou en blanc, entre `<example>`, suivie d'une phrase qui dit pourquoi elle est juste (le client voit la condition avant de signer, l'avenant est prévu). Domaine différent du cas de test.

**Cas de test.**

> Rédige notre proposition pour la refonte du site vitrine de Dupont Industrie (SAS, 200 salariés). Ce qu'on a décidé : forfait 38 000 € HT ; 10 semaines ; 3 allers-retours sur les maquettes ; reprise de 40 pages de contenu existant au maximum ; hébergement et maintenance non compris (on peut faire une offre à part) ; échéancier 30 % à la commande, 40 % à la recette, 30 % à la mise en ligne. Leur acheteur demande un paiement à 90 jours. Leur site actuel compte environ 65 pages. Mets en avant notre projet pour la Brasserie Martin (je n'ai pas les chiffres sous la main).

Valeurs de référence : échéancier 11 400 € / 15 200 € / 11 400 € HT, total 38 000 € HT. Écart de pages : 65 − 40 = 25 pages hors forfait.

Une bonne sortie contient :

1. Une section « non compris » : hébergement, maintenance, pages au-delà de 40, et ce qu'un client croirait inclus (rédaction de contenus, photos, traductions), avec l'offre d'hébergement proposée à part.
2. \* L'écart de 25 pages relevé, écrit comme hypothèse avec sa conséquence, le prix par page laissé en blanc, jamais inventé.
3. Les 3 allers-retours sur maquettes, avec ce qui se passe au quatrième (en blanc ou à confirmer).
4. Le prix de 38 000 € HT et l'échéancier 11 400 / 15 200 / 11 400 € HT ; aucune ventilation inventée du forfait.
5. \* Le paiement à 90 jours écarté, avec un délai conforme (60 jours date de facture au plus, ou 45 jours fin de mois) et la raison (L441-10) dans la note interne.
6. \* Les conditions de règlement avec le taux des pénalités de retard et l'indemnité forfaitaire de 40 €.
7. Une date de validité de l'offre (donnée ou marquée à confirmer).
8. La référence Brasserie Martin sans chiffre inventé, avec une marque pour les résultats.
9. \* Une note interne séparée du document client (demande de 90 jours, pages en trop, choix à confirmer).
10. Un planning de 10 semaines avec ses dépendances (contenus fournis par le client, délais de validation).
11. Aucune explication sur « comment répondre » dans le document client.

---

### B3. `negotiation-brief` (1.1.0 → 1.2.0)

**Savoir métier à ajouter.**

| Point | Règle | Source | Vérifié |
|---|---|---|---|
| BATNA chiffrée | Chiffrer la meilleure solution de repli sur le même horizon et le même périmètre, coûts de changement compris (transition, double intervention, temps interne, risque de continuité). | R. Fisher, W. Ury, *Getting to Yes*, 1981 (ouvrage, non vérifié en ligne ce jour) | — |
| Prix de réservation et ligne rouge | La ligne rouge est le prix au-delà duquel la BATNA vaut mieux, ramené à la même unité (par an, par unité). Une prime pour le risque de changement est permise si elle est écrite et justifiée. Raison : une ligne rouge arbitraire se cède à la table ; une ligne tirée de la BATNA se défend. | Idem | — |
| ZOPA | Zone entre la ligne rouge de l'acheteur et le plancher supposé du fournisseur. Estimer ce plancher (dépendance du fournisseur envers le client, capacité inemployée, structure de coûts) et le marquer comme hypothèse. Sans ZOPA, le dire et préparer la sortie ou un autre montage. | H. Raiffa, *The Art and Science of Negotiation*, 1982 (ouvrage, non vérifié en ligne ce jour) | — |
| Ouverture | Ancrer avec une ouverture ambitieuse mais défendable par un fait (devis concurrent, indice, volume). Raison : une ouverture qu'on ne peut pas justifier coûte la crédibilité pour la suite. Ordre attendu : ouverture < cible < ligne rouge, dans la même unité. | Pratique | — |
| Concessions | Chaque concession est un échange (« si vous…, alors nous… »), de taille décroissante. Lister ce qui coûte peu à l'acheteur et vaut cher au fournisseur : durée d'engagement, visibilité sur les volumes, paiement plus rapide (dans la limite légale), référence. | Pratique | — |
| Paliers | Palier 1, indispensable (pas de concession sans escalade) ; palier 2, préférence forte ; palier 3, monnaie d'échange. Céder du palier 3 pour obtenir du palier 2. | KWP `legal/skills/review-contract/SKILL.md` L281–306 | — |
| Délai de paiement | Le délai convenu ne dépasse pas 60 jours après la date de facture, ou 45 jours fin de mois s'il est écrit au contrat. Amende jusqu'à 2 M€ pour une personne morale. Un délai plus long n'est pas un levier. | C. com. L441-10 I ; L441-16 (URL en B2) | vérifié 2026-10-16 |
| Avantage sans contrepartie, déséquilibre | Engage la responsabilité le fait d'obtenir ou tenter d'obtenir un avantage sans contrepartie ou manifestement disproportionné (1°), ou de soumettre l'autre partie à un déséquilibre significatif (2°). Une baisse de prix se demande donc en échange de quelque chose. | C. com. L442-1 I 1° et 2° — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000054716237/2026-08-20 | vérifié 2026-10-16 |
| Appels d'offres répétés | Nouveau (loi n° 2026-796 du 18/08/2026) : soumettre un partenaire à des mises en concurrence répétées dont la fréquence ou les modalités créent un déséquilibre significatif engage la responsabilité (6°). Brandir sans cesse une remise en concurrence comme levier a donc un coût juridique. | C. com. L442-1 I 6° (même URL) | vérifié 2026-10-16 |
| Rupture d'une relation établie | Rompre, même partiellement, une relation commerciale établie sans préavis écrit tenant compte de sa durée engage la responsabilité. Un préavis de 18 mois met à l'abri d'un reproche sur la durée. Nouveau en 2026 : une réduction substantielle des volumes pendant la négociation peut aussi l'engager. Toute menace de sortie se planifie avec son préavis. | C. com. L442-1 II (même URL) | vérifié 2026-10-16 |
| Bonne foi et bluff | Négociations libres mais de bonne foi. Ne pas révéler son estimation de la valeur n'est pas un dol ; mentir l'est (un faux devis concurrent, par exemple). Garder sa ligne rouge pour soi est permis ; inventer une offre concurrente ne l'est pas. | C. civ. 1112 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036829818/2018-10-01 ; 1112-1 al. 2 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032007138/2016-10-01 ; 1137 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036829827/2018-10-01 | vérifié 2026-10-16 |

Le rappel juridique tient en un tableau court de garde-fous : la frontière avec `contrat-fournisseur` (analyse des clauses) reste dans la description.

**Reprises d'Anthropic.** `legal/skills/review-contract/SKILL.md` L281–306 (paliers et règle d'échange). Adapter : les exemples de palier 1 (responsabilité non plafonnée, données personnelles) sont contractuels ; ajouter des exemples d'achat (continuité de service, prix plafond, réversibilité).

**Contraintes à reformuler.**

| Citation actuelle | Proposition |
|---|---|
| « You must never invent figures, discounts, margins, or conditions… » | Marquer chaque chiffre « fait (source) » ou « hypothèse », parce que le brief sert en direct à la table, où un chiffre sans source devient un engagement ou un bluff. |
| « You must always distinguish facts, probable levers, and assumed negotiation positions. » | Garder comme format : chaque levier sur une ligne, avec son fait et son hypothèse. |
| « Do not present a hypothetical room for maneuver as a given. » | Fusionner avec la première ligne. |
| « Do not turn the brief into a legal memo or exhaustive contract analysis. » | Les points de droit tiennent en garde-fous d'une ligne, parce que le brief se lit en cinq minutes avant la réunion ; l'analyse des clauses relève de `contrat-fournisseur`. |
| « Do not forget relational, timeline, or supplier dependency risks. » | Positive : lister les risques d'échec (continuité, délai de transition, dépendance du fournisseur), en précisant que la dépendance est aussi une exposition juridique (L442-1). |

**Exemple de forme.** Une ligne de levier, entre `<example>` : le levier, le fait qui le fonde (avec sa source), l'hypothèse qu'il suppose, la contrepartie offerte, et une phrase qui dit pourquoi la ligne est juste (le fait se montre à la table, l'hypothèse ne se dit pas).

**Cas de test.**

> Je suis acheteur dans une ETI. Notre prestataire de maintenance des chariots élévateurs travaille avec nous depuis 8 ans, pour environ 120 k€ HT/an ; d'après son dernier bilan, on représente environ 25 % de son chiffre d'affaires. Il veut renouveler à 124,8 k€ (+4 %). J'ai un devis d'un concurrent à 98 k€ HT/an sur 3 ans, mais il faudrait compter 15 k€ de coûts de transition, une fois (inventaire, formation, un mois de double intervention). Ma direction veut −15 % et un paiement à 90 jours. Le contrat actuel se termine dans 4 mois. Prépare ma négo.

Valeurs de référence :

| Grandeur | Calcul | Valeur |
|---|---|---|
| Coût de la BATNA sur 3 ans | 98 × 3 + 15 | 309 k€ |
| BATNA ramenée à l'année | 309 / 3 | **103 k€/an** (prix de réservation avant prime de risque) |
| Cible « −15 % » | sur 120 → 102 ; sur 124,8 → 106,1 | base à faire préciser |
| Demande du fournisseur | 120 × 1,04 | 124,8 k€ |

Une bonne sortie contient :

1. \* Une ligne rouge tirée de la BATNA, environ 103 k€/an, avec le calcul ; toute prime de risque de transition écrite et justifiée.
2. \* Le paiement à 90 jours écarté comme illégal (L441-10 : 60 jours date de facture ou 45 jours fin de mois), remplacé par une concession ou un levier licite.
3. \* La sortie après 8 ans traitée comme rupture d'une relation établie : préavis écrit proportionné, contrat qui finit dans 4 mois (L442-1 II).
4. La base du −15 % (120 ou 124,8 k€) relevée comme ambiguïté ; une cible à 102 k€ notée juste sous la ligne rouge.
5. Une ouverture défendable appuyée sur le devis concurrent, plus basse que la cible, toutes trois en k€/an.
6. La dépendance du fournisseur (25 %) traitée à la fois comme levier et comme risque (contrepartie à offrir, L442-1 I 1°), avec son plancher marqué comme hypothèse.
7. Des concessions écrites en échanges (« si… alors… ») : durée, volume, paiement plus rapide dans la limite légale.
8. Aucun bluff mensonger proposé (pas de faux devis) ; la ligne rouge gardée pour soi.
9. Les risques de transition (un mois de double intervention, continuité) nommés.
10. Les questions ouvertes : performance passée du titulaire, solidité du concurrent, ce que couvre son devis.

---

### B4. `rfp-draft` (1.1.0 → 1.2.0)

**Savoir métier à ajouter.**

| Point | Règle | Source | Vérifié |
|---|---|---|---|
| Cadre de réponse imposé | Imposer le plan de la réponse (mêmes numéros que les exigences) et une matrice de conformité à remplir (exigence, conforme / partiel / non conforme, page de la réponse). Raison : sans cadre, chaque offre a sa structure et la comparaison devient une traduction. | Constat de la revue ; pratique | — |
| Bordereau de prix | Imposer un tableau : lignes, unité, quantité estimée, prix unitaire, total ; ponctuel séparé du récurrent ; options chiffrées à part ; HT ; formule de révision demandée ; durée de validité de l'offre. Les quantités pondèrent les prix unitaires. Raison : additionner des prix unitaires sans quantités donne trop de poids aux prestations rares. | Pratique ; même effet jugé irrégulier en marché public (CE, 13/11/2020, n° 439525, voir B5 en attente) | — |
| Test de l'éliminatoire | Une exigence n'est éliminatoire que si l'on rejetterait une très bonne offre qui ne la remplit pas ; sinon elle est notée. Raison : chaque éliminatoire en trop réduit la concurrence. | Adapté de KWP `small-business/skills/job-post-builder/reference/job-post-structure.md` L34–35 | — |
| Critères annoncés | Annoncer critères, pondérations et méthode de notation du prix avant l'envoi, et les garder. Raison : les fournisseurs construisent leur offre sur ces priorités ; les changer après réception fausse le choix (voir B5). Si une grille existe déjà (`vendor-scorecard`), la reprendre telle quelle. | Pratique | — |
| Besoin, pas marque | Écrire le besoin en résultats, fréquences, niveaux de service, pas en nom de produit. | Pratique | — |
| Obligation de vigilance | Pour tout contrat d'au moins 5 000 € HT, le donneur d'ordre se fait remettre, à la conclusion puis tous les 6 mois, une attestation URSSAF de moins de 6 mois et une preuve d'immatriculation (Kbis…). À demander dans les pièces. | C. trav. L8222-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000024197683/2011-06-18 ; R8222-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030422273/2015-05-01 ; D8222-5 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046078939/2023-01-01 | vérifié 2026-10-16 |
| Données personnelles | Si le prestataire traitera des données personnelles pour le compte de l'acheteur, n'en retenir qu'un qui présente des garanties suffisantes, avec un contrat art. 28 (instructions, sécurité, sous-traitants ultérieurs, retour ou suppression des données en fin de contrat, audits). À demander dans la réponse. | RGPD art. 28 — https://eur-lex.europa.eu/eli/reg/2016/679/oj | vérifié 2026-10-16 |
| Reprise du personnel | Dans certains services de main-d'œuvre, la convention collective impose au nouveau prestataire de reprendre le personnel du sortant. Exemple : en propreté, le nouveau prestataire garantit l'emploi de 100 % du personnel du marché qui remplit les conditions (notamment 6 mois d'affectation sur le marché), et le sortant transmet la liste du personnel. Le cahier des charges doit prévoir ces données, car elles changent les prix. Vérifier la convention du secteur avant d'écrire. | CCN des entreprises de propreté du 26/07/2011, art. 7.2 et 7.3 — https://www.legifrance.gouv.fr/codes/article_lc/KALIARTI000043930178/2020-09-29 | vérifié 2026-10-16 |
| Titulaire sortant | Remplacer un prestataire présent depuis longtemps est une rupture de relation établie : le calendrier doit laisser le préavis écrit au sortant. Des mises en concurrence répétées dont la fréquence crée un déséquilibre significatif engagent aussi la responsabilité (nouveau 6°, 2026). | C. com. L442-1 II et I 6° (URL en B3) | vérifié 2026-10-16 |
| Budget | Dire si le budget ou le prix actuel est communiqué aux fournisseurs, et l'effet de ce choix (il ancre les offres). | Pratique | — |
| Calendrier | Date limite des questions, réponses communiquées à tous les candidats, visite éventuelle, remise, décision, démarrage avec transition. | Pratique | — |

**Défaut relevé par la revue.** Le skill « ne prévoit pas de recevoir une grille existante » : ajouter aux entrées « evaluation grid from `vendor-scorecard`, if any, reused as is ».

**Contraintes à reformuler.**

| Citation actuelle | Proposition |
|---|---|
| « You must never invent figures, dates, volumes, or constraints… » | Volumes, dates et budgets inconnus restent `[à compléter]` et vont dans les points à clarifier, parce que les fournisseurs chiffrent ce qui est écrit : un volume inventé devient un prix. |
| « You must always distinguish confirmed scope, options, and areas to clarify… » | Garder comme format (trois statuts visibles). |
| « Do not produce a vague or purely narrative document. » | Écrire chaque exigence comme un énoncé auquel on répond « conforme / non conforme » ; le récit ne sert qu'au contexte. |
| « Do not present a hypothesis as a validated requirement. » | Fusionner avec la première ligne. |
| « Do not transform the RFP into a strategic note or supplier analysis. » | Le document part chez les fournisseurs : le raisonnement interne (budget plafond, fournisseur préféré) va dans une note interne. |

**Exemple de forme.** Trois lignes de bordereau de prix (une récurrente, une ponctuelle, une option) entre `<example>`, avec une phrase sur ce qui rend les offres comparables (unité, quantité, HT). Secteur différent du cas de test.

**Cas de test.**

> On veut changer de prestataire de nettoyage pour nos 3 sites : Lyon (2 500 m²), Villeurbanne (1 200 m²) et Grenoble (800 m²), passages 5 jours sur 7, contrat de 3 ans. Le titulaire actuel est là depuis 9 ans, son contrat finit le 30 juin et il nous coûte 96 k€ HT/an. On veut aussi la vitrerie deux fois par an. Rédige l'appel d'offres à envoyer à 4 prestataires.

Une bonne sortie contient :

1. \* Un cadre de réponse imposé : plan de la réponse et matrice de conformité à remplir.
2. \* Un bordereau de prix par site (surface, fréquence, prix mensuel), la vitrerie en prix unitaire par intervention avec 2 interventions par an, des totaux annuels comparables, HT, la formule de révision et la durée de validité demandées.
3. \* Critères, pondérations et méthode de notation du prix annoncés dans le document.
4. \* Les pièces obligatoires : attestation URSSAF de moins de 6 mois et Kbis (vigilance, contrat ≥ 5 000 € HT), assurance.
5. \* La reprise du personnel (CCN propreté art. 7) : liste du personnel du sortant fournie aux candidats, effet sur les prix signalé.
6. \* Le préavis au titulaire de 9 ans pris en compte dans le calendrier (L442-1 II).
7. Un calendrier complet : questions, réponses partagées, visite des sites, remise, décision, démarrage au 1er juillet avec transition.
8. Les éliminatoires distingués des exigences notées.
9. Le choix de communiquer ou non le budget de 96 k€ signalé avec son effet d'ancrage.
10. Les manques listés à compléter (horaires, zones et fréquences par type de local, consommables inclus ou non), sans valeur inventée.

---

### B5. `vendor-scorecard` (1.1.0 → 1.2.0)

**En attente Q12 (marché public), à lister sans traiter.** Si Amiel répond oui, ajouter :

- CCP R2152-7, critères liés à l'objet, au moins un critère environnemental pour les consultations engagées depuis le 21/08/2026 (URL en B1) ;
- R2152-11, critères et modalités de mise en œuvre indiqués dans les documents de la consultation — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037730473/2019-04-01 ;
- R2152-12, pondération obligatoire en procédure formalisée, ou à défaut ordre décroissant d'importance — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037730471/2019-04-01 ;
- jurisprudence sur les méthodes de notation : l'acheteur choisit librement sa méthode, mais elle est irrégulière si elle prive un critère de portée ou neutralise sa pondération. CE, 3/11/2014, *Commune de Belleville-sur-Loire*, n° 373362 (formule `10/3 × (7 − P/P0)`, qui neutralise les écarts de prix) — https://www.legifrance.gouv.fr/ceta/id/CETATEXT000029691320 ; CE, 24/05/2017, n° 405787 (linéaire entre extrêmes, 20 au moins-disant et 0 au plus cher, qui neutralise les autres critères avec un prix pondéré à 60 %) — https://www.legifrance.gouv.fr/ceta/id/CETATEXT000034808264 ; CE, 13/11/2020, n° 439525 (somme de prix unitaires sans quantités) — https://www.legifrance.gouv.fr/ceta/id/CETATEXT000042520648. Toutes lues le 2026-10-16.

Hors marché public, les mêmes effets s'écrivent comme des propriétés de calcul, sans citer ces arrêts.

**Savoir métier à ajouter** (dans le corps, environ 45 lignes).

1. **Éliminatoires hors pondération.** Les exigences réglementaires ou vitales sont des conditions « oui / non » vérifiées avant toute note. Raison : un poids laisse une bonne note ailleurs compenser un manque rédhibitoire. Exemples : contrat de sous-traitance RGPD art. 28 signable si des données personnelles sont traitées (URL en B4, vérifié 2026-10-16) ; attestation de vigilance pour un contrat ≥ 5 000 € HT (L8222-1, R8222-1, D8222-5, URL en B4, vérifié 2026-10-16) ; capacité à démarrer à la date ; exigence légale propre à l'objet (pour un logiciel de paie, produire la DSN : CSS L133-5-3 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051287164/2025-02-28, vérifié 2026-10-16).
2. **Dimensions par type d'achat** (défaut à adapter, pas une norme) :
   - **Logiciel, SaaS** : couverture fonctionnelle, intégration (API, SSO, outils en place), sécurité et données, réversibilité (export, formats, aide en fin de contrat), accompagnement au déploiement, support et engagements de service, solidité de l'éditeur, coût complet.
   - **Prestation intellectuelle** : compréhension du besoin, méthode, équipe nommée (et règle de remplacement), références comparables, planning, prix.
   - **Fournitures** : conformité technique, prix sur quantités, délais et fiabilité de livraison, qualité (non-conformités), garantie et SAV, sécurité d'approvisionnement (source unique), impact environnemental.
   - **Service récurrent de main-d'œuvre** (nettoyage, maintenance, infogérance) : moyens, niveaux de service et pénalités, plan de transition et de réversibilité, conditions sociales (vigilance, reprise du personnel), prix.
   - Risque de concentration et continuité d'activité, quand l'achat est critique (KWP `operations/skills/vendor-review/SKILL.md` L37, L39).
3. **Poids du prix** : un repère de praticien, à donner comme défaut ajustable et non comme norme. Achat banalisé : prix ≥ 50 %. Service standard : 30 à 40 %. Logiciel stratégique ou prestation intellectuelle : 20 à 30 %. Non sourcé : le présenter comme tel.
4. **Pondérations figées avant les offres.** Fixer critères, poids, échelle et formule de prix avant de recevoir les offres, les communiquer aux fournisseurs (avec `rfp-draft`), ne plus y toucher. Trois raisons : après lecture, les poids glissent vers l'offre déjà préférée ; les fournisseurs ont construit leur offre sur les priorités annoncées ; le choix doit pouvoir se justifier auprès des perdants et en interne. Un changement après ouverture ne se fait qu'en sensibilité étiquetée (voir `offer-comparison`).
5. **Échelle ancrée.** Échelle de 0 à 4 ou de 0 à 5 avec un descripteur observable par niveau et par critère (0 absent ou non conforme, 1 insuffisant, 2 partiel, 3 conforme, 4 au-delà avec preuve). Raison : sans ancrage, deux évaluateurs ne notent pas la même chose. Une échelle paire évite le refuge au milieu.
6. **Seuil technique** (facultatif) : écarter avant le prix les offres sous un minimum technique. Dire le seuil et sa raison.
7. **Formules de notation du prix**, avec leurs effets. Notes sur 10, P = prix de l'offre, calculé sur le coût complet et le même horizon :
   - *proportionnelle au moins-disant* : `N = 10 × Pmin / P`. Courbe, pas droite : un écart de 10 % coûte environ 0,9 point en haut de l'échelle, moins chez les offres chères. La note de chacun dépend de l'offre la plus basse : une offre très basse tasse toutes les autres et peut inverser le classement entre deux offres qui n'ont pas bougé.
   - *linéaire entre le minimum et le maximum reçus* : `N = 10 × (Pmax − P) / (Pmax − Pmin)`. La plus chère a 0 quel que soit l'écart, et un petit écart s'étire sur toute l'échelle. Avec un prix fortement pondéré, la plus chère est éliminée d'office.
   - *linéaire sur l'écart relatif au moins-disant* : `N = 10 × (1 − k × (P − Pmin) / Pmin)`, plancher 0. Chaque pourcentage au-dessus du moins-disant coûte k × 0,1 point. Ne dépend que du moins-disant ; k se choisit et se dit (k = 1 : 10 % plus cher = 1 point de moins).
   - Défaut proposé : la troisième, avec k annoncé, ou la première, en disant sa dépendance au moins-disant. La deuxième seulement si l'on assume ses effets.
8. **Taux de change entre critères.** Dire ce que chaque poids échange : avec un prix à 40 % et une notation proportionnelle, une offre 10 % plus chère perd environ 0,36 point sur 10, l'équivalent d'un point sur un critère pondéré à 35 %. Raison : c'est cette phrase que la direction valide, pas le pourcentage.

**Défaut d'annexe B.** Le déclencheur « comment on va scorer ces offres reçues » chevauche `offer-comparison`. Le remplacer par un déclencheur d'avant réception (« comment on notera les offres qu'on va recevoir », « grille à valider avant d'envoyer le cahier des charges ») et nommer `offer-comparison` comme frontière, en FR comme en EN. Rester sous 1 024 caractères.

**Contraintes à reformuler.**

| Citation actuelle | Proposition |
|---|---|
| « You must never invent weightings, thresholds, or scoring scales without justifying them… » | Donner chaque poids avec ce qu'il reflète du besoin, parce qu'un poids sans raison ne se défend ni devant le fournisseur écarté ni devant le métier. |
| « You must always make the scoring logic and the space reserved for qualitative comments visible. » | Garder comme format. |
| « Do not produce an overcomplicated grid if few criteria suffice. » | 5 à 8 critères par défaut. Un critère sous 5 % ne départage presque jamais (au plus 0,5 point sur 10) : le fusionner. |
| « Do not hide implicit trade-offs in the weighting. » | Écrire le taux de change entre critères (point 8). |
| « Do not present a scale as universal for all purchases. » | Partir du tableau des dimensions par type d'achat et l'adapter. |

**Exemple de forme.** Un critère complet entre `<example>` : dimension, critère, poids et sa raison, échelle 0 à 4 avec un descripteur par niveau, preuve attendue dans l'offre, plus une phrase qui dit pourquoi l'ancrage est juste (deux évaluateurs donneraient la même note). Pas le critère du cas de test.

**Cas de test.**

> On lance une consultation pour remplacer notre logiciel de paie (SaaS, 250 salariés, données RH sensibles). La DAF veut que le prix compte pour 40 %. Construis la grille avant qu'on envoie le cahier des charges. Pour qu'on voie comment se comporte la note prix, simule-la sur trois prix fictifs sur 3 ans : 100 k€, 110 k€ et 150 k€.

Valeurs de référence (notes sur 10 ; entre parenthèses, points sur 4 avec un prix à 40 %) :

| Formule | 100 k€ | 110 k€ | 150 k€ |
|---|---|---|---|
| Proportionnelle `10 × Pmin/P` | 10 (4,00) | 9,09 (3,64) | 6,67 (2,67) |
| Linéaire min–max `10 × (Pmax−P)/(Pmax−Pmin)` | 10 (4,00) | 8,00 (3,20) | 0 (0) |
| Écart relatif, k = 1 | 10 (4,00) | 9,00 (3,60) | 5,00 (2,00) |

Une bonne sortie contient :

1. \* Des éliminatoires « oui / non » séparés de la notation : production de la DSN, contrat RGPD art. 28. La raison est donnée (un poids compenserait).
2. Des dimensions propres à un logiciel de paie : couverture fonctionnelle et conventions collectives, mises à jour réglementaires incluses, intégration (SIRH, comptabilité), sécurité, réversibilité des historiques, reprise et déploiement, support, solidité de l'éditeur.
3. Le prix à 40 %, avec ce que ce poids implique, et des poids qui totalisent 100.
4. \* Une formule de prix choisie et justifiée, et les valeurs simulées exactes (tableau ci-dessus).
5. \* L'effet de la formule linéaire min–max (150 k€ obtient 0 quel que soit l'écart) et la dépendance de la proportionnelle au moins-disant.
6. \* La règle des pondérations figées avant l'envoi, avec sa raison ; tout changement après réception présenté comme une sensibilité.
7. \* Une échelle ancrée (descripteur par niveau) pour au moins un critère.
8. Le prix noté sur le coût complet à 3 ans, pas sur l'abonnement seul.
9. Les critères qui demandent une définition interne avant usage, signalés.
10. Aucun « bon poids » présenté comme une norme sans source.

---

### B6. `total-cost-analysis` (1.1.0 → 1.2.0)

**Savoir métier à ajouter** (court : le skill est déjà juste).

| Point | Règle | Source | Vérifié |
|---|---|---|---|
| HT ou TTC | Comparer HT quand l'acheteur récupère la TVA ; TTC quand il ne la récupère pas (association non assujettie, certaines activités exonérées, une partie du secteur public). Le dire en tête. | Principe de déduction de la TVA. Ne pas citer CGI art. 271 : abrogé au 01/01/2027 et recodifié dans le Code des impositions sur les biens et services (article de reprise non vérifié) | — |
| Révision de prix | Une clause de révision (indice Syntec, par exemple) se chiffre au plafond pour le pire cas et à 0 % pour le meilleur. Ne pas l'ignorer. | Pratique | — |
| Prix d'appel | Remise de première année, prix « de lancement » : chiffrer les années suivantes au prix normal. | Pratique | — |
| Coûts internes | Temps des équipes (administration, formation, recette), valorisé au coût chargé fourni ou marqué non chiffré. | Pratique ; KWP `operations/skills/vendor-review/SKILL.md` L27–32 | — |
| Double run | La période où l'ancien et le nouveau tournent ensemble est un coût. Commun à toutes les options, il ne change pas le classement : le dire. | Pratique | — |
| Sortie et réversibilité | Coût de récupération des données et de résiliation. Si des données personnelles sont traitées, leur retour ou leur suppression en fin de contrat relève du contrat RGPD : le demander, ne pas le supposer gratuit. | RGPD art. 28.3.g (URL en B4) | vérifié 2026-10-16 |
| Horizon | Aligner l'horizon sur la durée d'engagement ou la durée de vie de l'actif, identique pour toutes les options. Un engagement ferme plus long que le besoin est un coût de sortie. | Pratique | — |
| Volumes | Appliquer la croissance des volumes et les paliers de prix à toutes les options. | Pratique | — |
| Actualisation | Rester en euros courants par défaut. Actualiser seulement si les calendriers de paiement diffèrent beaucoup (achat comptant contre abonnement) ou si l'horizon dépasse 3 ans, au taux fourni par l'utilisateur, jamais inventé. | Pratique | — |
| Seuil de bascule | Pour chaque hypothèse qui peut inverser le classement, donner la valeur à partir de laquelle il s'inverse. | Pratique | — |
| Coût du cycle de vie | Définition utile des postes : acquisition, utilisation (énergie, ressources), maintenance, fin de vie, et le cas échéant les externalités environnementales chiffrables. | CCP R2152-9 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037730479/2019-04-01 (définition reprise comme grille de postes, sans changer le périmètre du skill) | vérifié 2026-10-16 |

**Contraintes à reformuler.**

| Citation actuelle | Proposition |
|---|---|
| Les trois « must » de la règle absolue (pas d'invention ; confirmé / estimé / non chiffré ; fait / hypothèse / inférence / risque) | Une consigne : étiqueter chaque ligne confirmé / estimé / non chiffré, parce que le lecteur décide sur le confirmé et négocie le reste. |
| « Do not reduce TCO to the purchase price alone. » | Supprimer : la méthode le fait déjà. |
| « Do not hide structuring hypotheses. » | Supprimer : le format les liste déjà. |
| « Do not present as certain a cost derived from a simple estimate. » | Supprimer : couvert par l'étiquette. |
| « Flag unquantified costs that could change the decision. » | Garder et ajouter : dire quel montant les ferait inverser le classement (seuil de bascule). |

**Exemple de forme.** Une ligne de coût avec sa nature, sa fourchette, son hypothèse de calcul et sa sensibilité, plus une ligne « seuil de bascule », entre `<example>`.

**Cas de test.**

> Deux offres pour notre outil de ticketing support (40 agents), horizon 3 ans, montants HT.
> Offre A (SaaS) : 55 €/agent/mois, mise en service 8 000 €, connecteur CRM inclus, révision annuelle des prix selon l'indice Syntec, plafonnée à 4 %.
> Offre B (SaaS) : 45 €/agent/mois, prix fermes et engagement ferme sur 3 ans, mise en service 20 000 €, connecteur CRM en option à 300 €/mois, reprise de l'historique « sur devis ».
> On passera de 40 à 50 agents au début de la 2e année. Le connecteur CRM nous semble nécessaire, à confirmer avec l'équipe. Notre outil actuel coûte 2 400 €/mois et il faudra le garder 2 mois de plus pendant la bascule. Compare le coût total.

Valeurs de référence :

| Poste | A | B |
|---|---|---|
| Mise en service | 8 000 | 20 000 |
| Année 1 (40 agents) | 26 400 | 21 600 |
| Année 2 (50 agents) | 33 000 sans révision ; 34 320 à +4 % | 27 000 |
| Année 3 | 33 000 ; 35 692,80 à +4 %/an | 27 000 |
| Connecteur CRM | inclus | 10 800 (300 × 36) |
| **Total** | **100 400 à 104 412,80** | **106 400 + reprise non chiffrée** |
| B sans connecteur | — | 95 600 |
| Double run (commun) | 4 800 | 4 800 |

Seuil de bascule : sans connecteur, B est moins cher que A de 4 800 € (A sans révision) à 8 812,80 € (A au plafond), tant que la reprise d'historique coûte moins que cet écart.

Une bonne sortie contient :

1. \* Le total de A en fourchette, de 100 400 à 104 412,80 € HT, avec la révision chiffrée au plafond à partir de l'année 2.
2. Le total de B : 106 400 € HT plus la reprise d'historique, marquée non chiffrée.
3. Le passage à 50 agents appliqué aux deux offres dès l'année 2.
4. \* Le connecteur CRM nommé comme l'hypothèse qui inverse le classement (B à 95 600 € sans lui).
5. \* Le seuil de bascule sur la reprise d'historique (4 800 à 8 813 €).
6. Le double run de 4 800 € compté, et dit neutre pour la comparaison.
7. L'engagement ferme de 3 ans de B signalé comme coût de sortie si l'effectif baisse.
8. La base HT dite, avec la condition (TVA récupérée).
9. Les coûts internes (administration, formation) listés, chiffrés ou marqués non chiffrés.
10. Le piège du prix affiché relevé : B est 18 % moins cher par agent mais plus cher au total avec le connecteur.
11. Pas de recommandation : le skill compare, c'est `offer-comparison` ou `decision` qui tranche.

---

### B7. `offer-comparison` (1.1.0 → 1.2.0)

**Savoir métier à ajouter.**

1. **Contrôle de comparabilité, avant de noter.** Même périmètre, même horizon, même base HT, mêmes quantités. Une offre avec un poste « sur devis » n'est pas comparable sur le prix : demander le chiffre, ou noter avec une fourchette et le dire. Raison : le prix d'une offre change la note prix des autres (point 2).
2. **Notation du prix.** Appliquer la formule de la grille. Si la grille n'en donne pas, appliquer l'écart relatif au moins-disant avec k = 1 et le dire. Connaître l'effet de chaque formule (mêmes trois formules qu'en B5, point 7) : avec la proportionnelle, un changement du moins-disant peut inverser le classement entre deux autres offres. Raison : c'est le piège que l'utilisateur ne voit pas.
3. **Pas de repondération après ouverture.** La grille validée avant réception reste la grille. Une autre pondération demandée après lecture des offres se calcule en sensibilité, étiquetée « pondération modifiée après ouverture des offres », à côté du résultat officiel, jamais à sa place. Trois raisons : les poids glissent vers l'offre déjà préférée ; les fournisseurs ont répondu aux priorités annoncées ; le choix doit se justifier. Défaut annexe B corrigé.
4. **Sans grille.** Quand aucune grille n'a été fixée avant les offres, reprendre les priorités écrites avant réception (cahier des charges, brief) ; sinon, proposer des poids marqués « fixés après ouverture, risque de biais », et montrer si le classement tient sur une plage de poids raisonnable. Défaut de la revue corrigé (« il fixe lui-même les pondérations »).
5. **Fragilité du classement.** Comparer l'écart entre les deux premiers à l'effet d'un point de note sur le critère le plus subjectif (poids × 1 point). Si l'écart est plus petit, le classement est à égalité de fait : confiance « faible », et dire ce qui départagerait (négociation, preuve demandée, démonstration).
6. **Offre anormalement basse.** Une offre très en dessous des autres se questionne (méthode, périmètre oublié) avant d'en tirer une note de 10. Repère de pratique, non sourcé ; en marché public, la règle L2152-6 relève de Q12.
7. **Conclure.** Une offre recommandée, la condition qui changerait la recommandation, et ce qu'il faut obtenir avant de signer.

**Contraintes à reformuler.**

| Citation actuelle | Proposition |
|---|---|
| Les trois « must » de la règle absolue | Une consigne : chaque chiffre est fourni (source), calculé (méthode) ou supposé (marqué), parce que la recommandation sera contestée sur ses chiffres. |
| « Do not parse or reconstruct non-normalized PDF offers. » | Raison et consigne : normaliser, c'est faire des choix (périmètre, horizon, HT) qui décident de la comparaison. Si les offres sont brutes, lister ce que chacune doit indiquer avant d'être notée et s'arrêter là, ou noter avec les manques marqués. |
| « Do not present a score as objective if the weightings are fragile or incomplete. » | Donner un niveau de confiance calculé (point 5). |
| « Do not drown the recommendation in soft neutrality. » | Conclure sur une offre et la condition qui changerait ce choix. |

**Exemple de forme.** Une ligne de conclusion sur la fragilité entre `<example>` : écart entre les deux premiers, effet d'un point sur le critère le plus subjectif, confiance qui en découle, ce qui départagerait. Plus une phrase qui dit pourquoi elle est juste (le lecteur voit que l'égalité est réelle et pas une prudence de style). Chiffres différents du cas de test.

**Cas de test.**

> Trois offres normalisées pour notre logiciel de notes de frais (coût total sur 3 ans, HT, même périmètre sauf mention). Grille validée avant l'envoi du cahier des charges : prix 40 %, couverture fonctionnelle 35 %, support 15 %, sécurité et réversibilité 10 %. Note prix = 10 × prix le plus bas / prix de l'offre. Notes qualité (sur 10) de l'équipe projet :
> A : 180 k€ ; fonctionnel 8 ; support 7 ; sécurité 8.
> B : 210 k€ ; fonctionnel 9 ; support 9 ; sécurité 7.
> C : 150 k€ ; fonctionnel 6 ; support 5 ; sécurité 4. Reprise des données historiques non chiffrée (« sur devis »).
> Notre DG trouve que le support de B est un vrai plus et propose de passer le support à 25 %, en prenant 10 points au prix. Lequel on prend ?

Valeurs de référence :

| | Note prix | Score, grille validée | Score, grille du DG (30/35/25/10) | Score si C = 180 k€ |
|---|---|---|---|---|
| A | 8,33 | **7,98** | 7,85 | **8,65** (note prix 10) |
| B | 7,14 | **8,06** | 8,24 | **8,63** (note prix 8,57) |
| C | 10 | **7,25** | 6,75 | 7,25 (note prix 10) |

Écart B − A avec la grille validée : 0,07. Effet d'un point de support : 0,15. Effet d'un point de fonctionnel : 0,35.

Une bonne sortie contient :

1. Les notes prix et les scores de la grille validée (A 7,98, B 8,06, C 7,25) avec la méthode.
2. \* La pondération du DG non appliquée comme grille, présentée en sensibilité étiquetée « après ouverture » (A 7,85, B 8,24, C 6,75), avec la raison.
3. C déclarée non comparable sur le prix tant que la reprise n'est pas chiffrée ; prix ferme demandé.
4. \* L'effet de la formule : si la reprise porte C à 180 k€, A passe devant B (8,65 contre 8,63) sans qu'A ni B n'aient changé.
5. \* Un classement A / B jugé fragile : 0,07 d'écart, moins qu'un point de support (0,15) ; confiance faible.
6. Une recommandation nette malgré tout, avec sa condition (par exemple : B, sous réserve du chiffre de C et d'une négociation ; ou un départage nommé).
7. La note sécurité de C (4/10) signalée comme point de vigilance, voire seuil à poser.
8. La distinction entre données fournies, calculs, hypothèses et recommandation.

---

## Annexe — sources lues pour cette famille

- Skills à `cbe271c` : `skills/{analyse-cdc,offre-commerciale,negotiation-brief,rfp-draft,vendor-scorecard,total-cost-analysis,offer-comparison}.md` et `.mystaffy.json`.
- `skills/reponse-appel-offres.md` 1.6.0 : champs lus aux étapes 1 et 5.
- KWP, commit `33eeda1` : `operations/skills/vendor-review/SKILL.md` ; `small-business/skills/proposal-builder/reference/{proposal_structure,pricing_method,gotchas}.md` ; `small-business/skills/grant-rfp-writer/reference/{go_no_go,drafting}.md` ; `legal/skills/review-contract/SKILL.md` L276–306 ; `small-business/skills/job-post-builder/reference/job-post-structure.md` L30–35.
- Textes officiels lus le 2026-10-16 (URL dans les fiches) : C. com. L441-1, L441-10 (versions du 01/09/2026 et du 01/01/2027), L441-16, L442-1, D441-5 ; C. civ. 1112, 1112-1, 1137 ; CCP L2152-2, L2152-5, L2152-6, R2132-6, R2151-8, R2152-2, R2152-3, R2152-7, R2152-9, R2152-11, R2152-12, R2192-10, R2192-11 ; C. trav. L8222-1, R8222-1, D8222-5 ; CSS L133-5-3 ; RGPD art. 28 ; CCN propreté art. 7.2 ; CE n° 373362, 405787, 439525. CGI art. 271 lu et écarté (abrogation au 01/01/2027).
