# Analyse famille « finance » — 2026-10-16

Grille : `docs/etat-de-l-art-skills.md` (G1–G10, R1–R10). Versions analysées : `cbe271c`. Clone Anthropic : un clone local (non versionné), commit `33eeda1`, Apache-2.0 (abrégé « kwp » ci-dessous). Aucun fichier du dépôt n'a été modifié.

Constat transversal (vaut pour les 9 skills) :
- Les 8 skills non pilotes ont le même gabarit (rôle, règle absolue, entrées, méthode en 4–6 lignes, contraintes, format, définition de fini) et pèsent 76 à 84 lignes. Le savoir propre tient en 0 à 3 lignes par skill ; le reste est gabarit et interdits. La règle « distinguer observé / hypothèse / recommandation » est écrite 2 à 3 fois par skill (règle absolue, contraintes, définition de fini).
- **Paramètres `.mystaffy.json` jamais définis dans le corps** (hors pilote) : `niveau_granularite` et `inclure_hypotheses` (budget-variance), `horizon_analyse` et `inclure_options` (business-case), `audience` et `longueur` (financial-narrative), `modele_prix` et `inclure_tests` (strategie-prix), `destinataire`, `longueur` et `inclure_risques` (note-strategique), `methode_principale` (tam-sam-som), `destinataire`, `domaine` et `nb_kpis_max` (tableau-de-bord-kpi), `cadre_analyse` = five-forces / positionnement / benchmark-produit (analyse-concurrentielle). Le pilote `metriques-saas` 1.2.0 montre la forme : une ligne par paramètre (« If a depth level is given… », « If a focus is given… »). Même famille de défaut que l'annexe B (modes non définis).
- **Le défaut kwp relevé (« three-way », variance-analysis L31–36) n'est pas le seul.** La décomposition effectifs / rémunération (L70–71) a le même trou : effet effectif au salaire moyen budgété **et** effet taux à l'effectif budgété, donc l'interaction ΔHC × Δsalaire disparaît (ex. 10 → 12 personnes, 50 → 55 k€ : 100 + 50 = 150 k€ pour un écart de 160 k€). La décomposition rate / mix (L52–53) ne se réconcilie qu'avec un effet volume au prix moyen budgété, que la section ne donne pas. Ne reprendre de kwp que la décomposition deux termes (L19–29) et son exemple (L38–44), qui se réconcilient.

## A. Tableau

| Skill (version) | Lignes · équivalent Anthropic | Pourquoi il a cette longueur | Justifié ou manque | Ce qui change | En attente (§3) |
|---|---|---|---|---|---|
| `budget-variance-analysis` (1.1.0) | 84 · `finance/variance-analysis` 266 | Gabarit. Il nomme « volume, prix, mix, calendrier » sans formule ni seuil. La règle absolue dit trois fois la même chose. | **manque** : sans formule ni seuil de matérialité, « significatif » et « effet prix » sont laissés au hasard. | Ajouter : décomposition volume / mix / prix qui se réconcilie (vérifiée par calcul), budget flexible pour les charges variables, seuils de matérialité avec leur raison, convention de signe, priorité d'investigation, mauvais commentaires d'écart. Ajouter le pont avec contrôle de bouclage et un exemple d'une ligne. 5 interdits à reformuler (2 en double). Définir `niveau_granularite` et `inclure_hypotheses`. | Q8 : vérification isolée hors réécriture (l'auto-contrôle interne reste permis) |
| `business-case-draft` (1.1.0) | 84 · aucun (`sales/close-plan` L56–70, partiel, côté client) | Gabarit et interdits. Aucun outil de calcul : ni VAN, ni TRI, ni payback, ni scénarios, ni scénario de référence « on ne fait rien ». | **manque** : le modèle sort un « ROI » sans définition, souvent sur les gains bruts, et mélange gains encaissés et temps libéré. | Ajouter : flux incrémentaux par rapport au statu quo, VAN / TRI / payback simple et actualisé avec leurs pièges, gains encaissés ou non (hard / soft), point mort, au moins 3 scénarios, taux d'actualisation donné ou supposé, avant ou après IS (25 %, art. 219 CGI). Un exemple de tableau de scénarios. 5 interdits à reformuler. Définir `horizon_analyse` et `inclure_options`. | Q9 : pas de pause de validation des hypothèses ; seuls les garde-fous internes (scénarios et point mort calculés avant la recommandation) |
| `financial-narrative` (1.1.1) | 81 · `finance/variance-analysis` L125–159 (récit) ; `finance/financial-statements` L97–176 | Gabarit. La méthode en 6 lignes est juste mais générique ; ni marges en points, ni éléments non récurrents, ni lien résultat / trésorerie. | **mixte** : la structure tient ; il manque les pièges de lecture qu'un DAF repère et que le modèle commet. | Ajouter : écarts de taux en points, pas en %, non récurrent présenté à part (publié et retraité, chacun nommé), message principal d'abord sur l'écart au budget s'il domine, écart résultat / trésorerie signalé, anti-modèles de commentaire (kwp L152–159), comparaison budget / prévision / N-1 (kwp L233–239). Un exemple « mauvais / bon » message. 4 interdits à reformuler. Définir `audience` et `longueur`. | Q8 (idem) |
| `strategie-prix` (1.1.0) | 77 · aucun | Gabarit d'`explorer` → `decision` titré « prix ». Seul savoir : « ne pas mélanger prix, packaging et go-to-market ». | **manque** : aucun modèle tarifaire décrit, aucune métrique de valeur, aucune méthode de consentement à payer, aucun calcul de volume d'équilibre. | **Maintenant** : reformuler les 4 interdits (2 en double) et dire ce que fait `modele_prix`, sans toucher au périmètre. **Si Q10 = enrichir** : catalogue de modèles avec conditions, critères de la métrique de valeur, méthodes de consentement à payer, volume d'équilibre d'un changement de prix (vérifié par calcul), règles françaises d'annonce de réduction et de prix abusivement bas (vérifiées), exemple d'une ligne. | **Q10** : tout enrichissement attend ; le savoir prévu porte sur la partie « valeur, segments, modèles candidats », qui resterait dans un skill allégé |
| `note-strategique` (1.1.0) | 76 · aucun | Gabarit et 7 consignes de forme. Le savoir (pyramide de Minto, conclusion d'abord), le modèle l'a. | **justifié** : peu de choses que le modèle ferait mal ; deux manques de forme seulement. | Reformuler les interdits (« conclusion d'abord » écrit deux fois, « 2 pages » sans raison). Ajouter : la décision demandée (qui, quoi, pour quand) en tête, l'option « ne rien faire » parmi les options, ce qui ferait changer la recommandation. Définir `destinataire`, `longueur` et `inclure_risques`. | — |
| `tam-sam-som` (1.1.0) | 80 · aucun | Gabarit plus le bloc « modes » copié de `research` sans les modes. Aucune définition opérationnelle de TAM / SAM / SOM. | **manque** : les définitions et les contrôles de cohérence sont ce que le modèle rate (TAM tiré d'un rapport plus large, SOM = « 1 % du marché »). | Ajouter : définitions opérationnelles, bottom-up calculé **avant** le top-down (contre l'ancrage relevé par la revue), SOM par capacité commerciale, unités (€/an), contrôles SOM ≤ SAM ≤ TAM, écart top-down / bottom-up expliqué, sources publiques françaises. Définir flash / standard / deep (annexe B), comme le pilote. 3 interdits à reformuler (1 en double). Définir `methode_principale`. | Q8 (idem) |
| `metriques-saas` (1.1.0) | 79 · aucun (`product-management/metrics-review` partiel) | Gabarit ; promettait « toujours donner les formules » sans en contenir une. | **manque** (corrigé par le pilote) | — pilote : voir version 1.2.0 | Q8 (idem) |
| `tableau-de-bord-kpi` (1.1.0) | 83 · `product-management/metrics-review` L268–273, L319–375 | Gabarit avec un vrai savoir (avancé / résultat, fiche par KPI, 5–10 KPI, KPI sans action exclu). | **mixte** : le savoir est juste, mais la règle « refuse un KPI sans cible » pousse à inventer une cible quand il n'y a pas de mesure de départ. | Ajouter : définition exacte (numérateur, dénominateur, filtre, période), mesure de départ avant cible (sinon « cible à fixer après N périodes »), cible engagée et cible haute, indicateur de contrepoids (Grove ; loi de Goodhart), responsable par KPI, seuil d'alerte, même période sur une vue, anti-modèles (kwp L355–362). Un exemple de fiche KPI. 3 consignes à reformuler. Définir `destinataire`, `domaine` et `nb_kpis_max`. | — |
| `analyse-concurrentielle` (1.1.0) | 79 · `product-management/competitive-brief` 302 ; `marketing/competitive-brief` 331 | Gabarit plus le bloc « modes » non défini. Seul savoir : direct / indirect / substitut. | **manque** : aucun cadre, aucune règle de preuve ; le modèle comble par mémoire non datée. | Ajouter : quatre niveaux de concurrents plus la non-consommation (kwp PM L99–118), axes de carte choisis sur les critères d'achat (L120–130), échelle de notation (L149–163), prix comparés avec leurs réserves, chaque fait avec source et date, forces des concurrents dites, quand Porter sert. Définir flash / standard / deep (annexe B) et `cadre_analyse`. 4 interdits à reformuler (1 en double). | — |

---

## B. Fiches de réécriture

Consignes communes aux 8 fiches (pour le rédacteur) :
- Prendre `skills/metriques-saas.md` 1.2.0 comme modèle de forme : rôle qui dit qui lit et pourquoi l'erreur coûte, section « What makes this hard », table de formules, méthode avec étape « recompute », exemple balisé `<example>` avec une phrase « Why this is right », définition de fini vérifiable. Ne pas recopier son contenu.
- Fusionner « Absolute rule » et « Constraints » quand elles se répètent (R8). Une seule phrase sur observé / hypothèse / recommandation, avec sa raison, au lieu de trois.
- Toute formule écrite dans un skill est vérifiée par calcul sur un exemple **différent** du cas de test.
- Reprise kwp : créditer dans `THIRD_PARTY.md` (tableau « Skills adaptés », commit `33eeda1`), en disant ce qui est repris. Les définitions générales (VAN, TRI, TAM) ne sont pas des reprises.
- Le cas de test va dans `tests/cas-skills/<id>.md`, au format de `tests/cas-skills/metriques-saas.md`.

---

### 1. `budget-variance-analysis` (1.1.0 → 1.2.0)

**Savoir métier à ajouter**

1. **Décomposition prix / volume, un produit** (kwp `finance/skills/variance-analysis/SKILL.md` L19–29, exemple L38–44) :
   - effet volume = (volume réel − volume budget) × prix budget ;
   - effet prix = (prix réel − prix budget) × volume réel ;
   - la somme égale l'écart total, exactement. L'interaction ΔP × ΔV est rangée dans l'effet prix : le dire, car l'autre convention (prix × volume budget + terme d'interaction séparé) existe et change les chiffres.
   - Vérifié par calcul sur l'exemple kwp : 1 000 × 50 + (−2) × 11 000 = 28 000 = 528 000 − 500 000.
2. **Décomposition volume / mix / prix, plusieurs produits** (à écrire nous-mêmes ; vérifiée par calcul le 2026-10-16) :
   - effet volume = (volume total réel − volume total budget) × prix moyen budget ;
   - effet mix = Σ prix budgetᵢ × (volume réelᵢ − volume total réel × part budgetᵢ) ;
   - effet prix = Σ volume réelᵢ × (prix réelᵢ − prix budgetᵢ) ;
   - volume + mix + prix = réel − budget, exactement.
   - **Ne pas reprendre** kwp L31–36 (« three-way ») : sur un seul produit il oublie ΔP × ΔV (1 000 × 50 + (−2) × 10 000 = 30 000 au lieu de 28 000). Ni L70–71 (effectifs / salaires), même défaut.
   - Raison à écrire dans le skill : sans effet mix, une hausse du volume total peut cacher un glissement vers les produits bon marché ; c'est la lecture que le contrôleur attend.
3. **Budget flexible pour les charges variables** (comptabilité de gestion, budget flexible : p. ex. Horngren, *Cost Accounting*, chapitre « flexible budgets » ; chapitre non vérifié). Une charge variable se compare au budget recalculé au volume réel ; sinon un écart de volume passe pour une dérive de coût. Écart total = écart de volume (budget flexible − budget initial) + écart de dépense (réel − budget flexible).
4. **Convention de signe** : favorable / défavorable, pas « + / − » seul ; un dépassement de charge est défavorable. La dire en tête du livrable.
5. **Seuils de matérialité** (kwp L93–113) : en relatif, 10 % sur budget, 15 % sur N-1, 5 % sur prévision, 20 % d'un mois sur l'autre ; en absolu, 0,5 à 1 % du chiffre d'affaires de la période pour les lignes du compte de résultat. Position par défaut à écrire, et sa raison :
   - si l'utilisateur donne un seuil, le prendre ;
   - sinon, annoncer le seuil retenu en tête (par défaut : 10 % **et** 1 % du CA de la période) et pourquoi (le but est d'expliquer ce qui change une décision, pas chaque ligne) ;
   - lister en une ligne les écarts qui dépassent un seul des deux seuils, sans analyse de cause.
   - Le choix « et » plutôt que « ou » (kwp dit « ou ») est une **position proposée, non sourcée** : la signaler à Amiel à la relecture.
6. **Priorité d'investigation** (kwp L115–123) : montant absolu, puis %, sens inattendu, écart nouveau, écart qui grossit. Et un écart d'un mois se lit avec le cumul de l'année : un écart de calendrier se compense sur le cumul (raison qui remplace « do not overinterpret an isolated variance »).
7. **Calendrier** : un écart de calendrier dit ce qui est en avance ou en retard et quand il se résorbe (kwp L156).
8. **Mauvais commentaires d'écart** (kwp L152–159) : circulaire (« le CA est au-dessus parce que le CA a augmenté »), vague, « calendrier » ou « exceptionnel » sans dire quoi, « divers » sur un écart significatif, cause principale seule en oubliant ce qui compense.
9. **Pont budget → réel** (kwp L169–175, L198–212) : budget + Σ effets = réel ; contrôle de bouclage écrit. 5 à 8 effets au plus, le reste en « autres ».

**Reprises kwp** (Apache-2.0, `33eeda1`) : L19–29 et L38–44 (prix / volume), L104–113 (seuils), L115–123 (priorité), L127–139 (gabarit de commentaire, en français), L152–159 (anti-modèles), L169–175 et L198–212 (pont et bouclage). Adapter : euros, vocabulaire du contrôle de gestion français (« écart sur volume », « écart sur prix », « favorable / défavorable »). À créditer dans `THIRD_PARTY.md`.

**Contraintes à reformuler**
- L33 « You must never invent a figure, cause, or saving — and you must explicitly mark any quantified hypothesis » → « Chaque chiffre vient du tableau ou d'un calcul montré ; une cause absente de la source est écrite comme hypothèse, avec ce qui la confirmerait. Raison : le commentaire part aux responsables budgétaires, qui le prendront pour un constat. »
- L34 et L35 (deux fois « distinguish observations / hypotheses / recommendations ») → une seule phrase, avec la raison : le contrôleur traite un constat, une piste et une action de trois façons différentes.
- L54 « Do not present a quantified hypothesis as verified data » → supprimer (doublon de L33).
- L55 « Do not overinterpret an isolated variance without context » → remplacé par le seuil de matérialité et la lecture avec le cumul (savoir 5–6).
- L56 « Do not hide data limits or lack of granularity » → « Dis quelle décomposition la granularité permet : sans volumes, pas de prix / volume ; sans détail par produit, pas de mix. »

**Défauts à corriger** : règle absolue redondante (R8) ; paramètres `niveau_granularite` (flash / standard / detaille) et `inclure_hypotheses` non définis dans le corps.

**Exemple à ajouter** : une ligne d'écart avec formule, données, montant, sens, nature (« Ventes produit X : effet prix = (52 − 50) × 4 000 = 8 000 € favorable ») et une phrase « Why this is right » (formule et entrées visibles, convention dite). Puis un pont de 4 lignes avec la ligne de bouclage. Données différentes du cas de test.

**Cas de test**

Demande :
> Clôture de septembre, on a un écart sur le trimestre. Analyse-moi ça pour le comité de lundi.
>
> Chiffre d'affaires T3 :
> - Produit Pro : budget 1 000 unités à 200 € ; réel 900 unités à 210 €
> - Produit Lite : budget 2 000 unités à 50 € ; réel 2 600 unités à 48 €
>
> Charges T3 (budget / réel) :
> - Marketing : 40 000 / 52 000 € (l'acompte de 10 000 € du salon de novembre a été payé en septembre)
> - Hébergement : 20 000 / 21 500 €
> - Salaires : 150 000 / 147 000 €
> - Déplacements : 5 000 / 7 500 €

Valeurs de référence (calculées le 2026-10-16) :

| Élément | Valeur |
|---|---|
| CA budget / réel / écart | 300 000 / 313 800 / **+13 800 € favorable** |
| Effet volume (total au prix moyen budget 100 €) | (3 500 − 3 000) × 100 = **+50 000** |
| Effet mix | Pro : (900 − 1 166,7) × 200 = −53 333 ; Lite : (2 600 − 2 333,3) × 50 = +13 333 ; **−40 000** |
| Effet prix | 900 × 10 + 2 600 × (−2) = **+3 800** |
| Bouclage | 50 000 − 40 000 + 3 800 = 13 800 |
| Par produit (deux termes) | Pro : volume −20 000, prix +9 000 (−11 000) ; Lite : volume +30 000, prix −5 200 (+24 800) |
| Seuil absolu à 1 % du CA réel | ≈ 3 138 € |
| Marketing | +12 000 (+30 %), défavorable, significatif ; dont 10 000 de calendrier (salon de novembre), 2 000 non expliqués |
| Hébergement | +1 500 (+7,5 %), sous les deux seuils |
| Salaires | −3 000 (−2 %), favorable, sous le seuil relatif |
| Déplacements | +2 500 (+50 %) : au-dessus du seuil relatif, sous l'absolu ; traitement selon la règle annoncée |

Une bonne sortie contient :
1. Un écart de CA de +13 800 € décomposé en volume, mix et prix dont la somme boucle, avec les formules.
2. L'effet mix nommé (≈ −40 000 €) : le volume total monte mais se déplace vers Lite, moins cher. *(échoue probablement avec 1.1.0 : pas de formule de mix)*
3. La convention retenue pour l'interaction (rangée dans l'effet prix, ou séparée et nommée).
4. Le seuil de matérialité annoncé avec sa raison, et le traitement des déplacements cohérent avec ce seuil. *(échoue probablement avec 1.1.0 : aucun seuil)*
5. Le marketing ventilé : 10 000 € de calendrier (le salon, qui se compensera en novembre) et 2 000 € non expliqués, marqués à vérifier.
6. Les sens favorable / défavorable corrects sur les charges (dépassement = défavorable).
7. Aucune cause inventée à la baisse de volume de Pro ni à la baisse de prix de Lite : hypothèses marquées, ou questions aux responsables.
8. Un pont budget → réel qui boucle, contrôle écrit.
9. Aucun commentaire circulaire ou « divers » sur un écart significatif.
10. Les actions reliées chacune à un écart.

---

### 2. `business-case-draft` (1.1.0 → 1.2.0)

**Savoir métier à ajouter** (définitions de manuel, p. ex. Brealey, Myers et Allen, *Principles of Corporate Finance* ; formules vérifiées par calcul le 2026-10-16)
1. **Flux incrémentaux par rapport au statu quo** : on compare au scénario « on ne fait rien », qui a ses propres coûts. Coûts déjà engagés exclus (coûts irrécupérables). Raison : c'est la première erreur des dossiers d'investissement.
2. **VAN** = Σ flux_t / (1 + r)^t, t = 0 à N. Décider sur la VAN ; le TRI ne départage pas deux projets exclusifs (taille, calendrier différents).
3. **TRI** : taux qui annule la VAN. Pièges : plusieurs TRI si les flux changent de signe plus d'une fois ; pas de TRI si la somme des flux est négative et n'en change pas ; il suppose un réinvestissement au TRI.
4. **Payback** simple et actualisé ; tous deux ignorent les flux après le retour, donc ne départagent pas seuls.
5. **ROI** : nom ambigu ; écrire la formule utilisée ((gains nets cumulés − investissement) / investissement, sur N ans, après coûts de fonctionnement).
6. **Taux d'actualisation** : celui de l'entreprise (coût du capital ou taux plancher fourni par la finance). Sinon l'écrire comme hypothèse et montrer la sensibilité. Flux et taux tous deux nominaux, ou tous deux réels.
7. **Avant ou après impôt** : le dire. En France, IS au taux normal de 25 %, et 15 % jusqu'à 42 500 € de bénéfice pour les sociétés au CA ≤ 10 M€ dont le capital remplit les conditions de détention (art. 219 I CGI, al. 2 et b ; https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053542939/2026-02-21 ; en vigueur, vérifié 2026-10-16). L'amortissement n'est pas un flux de trésorerie mais réduit l'impôt.
8. **Gains encaissés ou non** (« hard » / « soft ») : du temps libéré n'est un gain de trésorerie que si une dépense disparaît (départ, embauche évitée, intérim arrêté). Calculer la VAN avec les seuls gains encaissés, puis avec tous, et dire l'écart. Pratique courante des dossiers d'investissement, pas de source unique : le présenter comme position par défaut.
9. **Scénarios et point mort** : au moins trois scénarios (bas, central, haut), chacun avec l'hypothèse qui bouge ; le point mort (la valeur de l'hypothèse clé qui annule la VAN) dit au décideur de combien on peut se tromper. Raison : c'est la défense interne contre des chiffres construits pour la recommandation, sans trancher Q9.

**Reprises kwp** : aucune utile (`sales/close-plan` L56–70 est un dossier côté client).

**Contraintes à reformuler**
- L33 « must never invent a number, ROI… » → « Chaque estimation porte sa source ou son hypothèse, sur la même ligne. Raison : un décideur conteste une hypothèse, il ne peut pas contester un chiffre nu. »
- L34–35 (deux « must distinguish ») → une phrase : coûts engagés, estimations, scénarios, recommandation.
- L58 « Do not present a ROI or payback as certain if the assumptions are fragile » → « Montre les scénarios et le point mort à côté du chiffre central. »
- L59 « Do not bury risks in the argument » → « Chaque risque dit son effet sur la VAN ou le scénario qui le traduit. »
- L55–57 (renvoi à `note-strategique` si pas de chiffres) : garder, c'est une frontière utile ; ôter le « Do not block », redondant.
- Description FR / EN : « Ne présente jamais un ROI comme certain » → « présente le ROI avec ses scénarios et son point mort ».

**Défauts à corriger** : `horizon_analyse` (12–60 mois, défaut 36) et `inclure_options` non définis dans le corps. Rien ne dit quelle période d'analyse prendre sans ce paramètre.

**En attente (Q9)** : ne pas ajouter de pause « fais valider les hypothèses avant de recommander », ni sortir la recommandation vers `decision`. La recommandation reste (§6bis). Permis : calculer scénarios et point mort **avant** d'écrire la recommandation, et faire dépendre celle-ci du point mort.

**Exemple à ajouter** : un tableau de scénarios de trois lignes (hypothèse qui bouge, flux net annuel, VAN, TRI) et la phrase du point mort (« la VAN s'annule si le gain annuel tombe à X, soit Y % du scénario central »), avec « Why this is right ». Données différentes du cas de test.

**Cas de test**

Demande :
> Mon DG veut un business case pour automatiser la saisie des commandes. Il me demande « le ROI ». Voilà ce que j'ai :
> - Investissement : 120 000 € la première année (licences + intégration)
> - Coût de fonctionnement : 10 000 €/an
> - Gains attendus par an : 18 000 € d'intérim qu'on arrête au service commandes, 12 000 € de pénalités de retard évitées, et environ 0,4 ETP libéré (≈ 20 000 €/an), mais personne ne part
> - Horizon 5 ans, taux d'actualisation 8 % (donné par le DAF), on raisonne avant impôt pour l'instant.

Valeurs de référence (calculées le 2026-10-16 ; facteur d'annuité 8 %, 5 ans = 3,9927) :

| Cas | Flux net annuel | VAN à 8 % | TRI | Payback |
|---|---|---|---|---|
| Tous gains (encaissés + temps libéré) | 40 000 € | **+39 708 €** | **19,9 %** | 3 ans simple ; 3,58 ans actualisé |
| Gains encaissés seuls | 20 000 € | **−40 146 €** | ≈ −5,8 % | jamais sur 5 ans (100 000 € cumulés < 120 000 €) |
| Point mort | **30 055 €/an** de flux net | 0 | 8 % | — il faut qu'environ la moitié (≈ 10 055 €) du temps libéré devienne un gain encaissé |
| Exemple bas (encaissés −20 %, moitié du temps libéré) | 24 000 € | −24 175 € | 0 % | — |
| Exemple haut (encaissés +10 %, temps libéré entier) | 43 000 € | +51 687 € | 23,2 % | — |
| « ROI » naïf sans coût de fonctionnement | — | (5 × 50 000 − 120 000) / 120 000 = 108 % | — | — à refuser |
| ROI sur 5 ans avec coût de fonctionnement | — | (5 × 40 000 − 120 000) / 120 000 = 66,7 % (non actualisé) | — | — |

Les scénarios bas et haut sont libres ; les critères portent sur leur présence et leur cohérence.

Une bonne sortie contient :
1. Le coût de fonctionnement de 10 000 €/an déduit de chaque année ; aucun ROI à 108 %.
2. La distinction entre gains encaissés (30 000 €) et temps libéré (20 000 €), avec la VAN dans les deux cas (+39,7 k€ et −40,1 k€). *(échoue probablement avec 1.1.0)*
3. Une VAN à 8 % de ≈ +39 700 € sur l'ensemble des gains, et un TRI ≈ 19,9 %.
4. Le payback simple de 3 ans, avec le payback actualisé (≈ 3,6 ans) ou la limite du payback dite.
5. Le point mort calculé (≈ 30 000 €/an de flux net, soit la moitié environ du temps libéré à convertir en gain encaissé). *(échoue probablement avec 1.1.0)*
6. Au moins trois scénarios, chacun nommant l'hypothèse qui bouge.
7. Le « ROI » demandé défini par sa formule.
8. La comparaison au statu quo explicite (les pénalités et l'intérim continuent si on ne fait rien).
9. Une recommandation qui dépend de la condition clé (que fait-on des 0,4 ETP ?), pas un oui sans condition.
10. Le calcul dit avant impôt, conformément à la demande.

---

### 3. `financial-narrative` (1.1.1 → 1.2.0)

**Savoir métier à ajouter**
1. **Taux et marges en points** : un écart de marge s'écrit en points (ou en points de base), pas en % d'un % (42 % → 40 % = −2 points, pas −4,8 %). Raison : un board compare des marges entre elles ; un % de % est lu à tort comme un écart de chiffre d'affaires (kwp `financial-statements` L104–106).
2. **Comparaison de référence** (kwp `variance-analysis` L233–239) : budget pour la performance, prévision pour le pilotage, N-1 pour la tendance. Le récit dit lesquelles il utilise. Quand elles divergent (au-dessus de N-1, sous le budget), les deux vont dans le message principal.
3. **Non récurrent** : publié et retraité côte à côte, l'élément retiré nommé et chiffré, le retraité étiqueté comme tel. Ne pas ouvrir sur le retraité seul. Raison : le board sait que l'exceptionnel revient souvent.
4. **Résultat et trésorerie** : quand l'EBITDA et la variation de trésorerie divergent, chiffrer l'écart et dire ce qui l'explique (BFR, investissements, impôt, dette) ou que la source ne l'explique pas.
5. **Ordre des messages** : le message principal est l'écart qui change une décision. Si c'est une dégradation, elle ouvre le récit, chiffrée.
6. **Gabarit de commentaire d'écart** (kwp L127–139) et **anti-modèles** (kwp L152–159), comme pour `budget-variance-analysis` (même texte, partagé en esprit, pas en partial : hors périmètre de créer un partial nouveau).
7. **Décomposer un écart de marge** en effet volume (écart de CA × taux budget) et effet taux (écart de taux × CA réel) quand les données le permettent ; la somme boucle.

**Reprises kwp** : `finance/skills/variance-analysis/SKILL.md` L127–139, L152–159, L233–239 ; `finance/skills/financial-statements/SKILL.md` L104–106 (points de base). À créditer.

**Contraintes à reformuler**
- L33–35 (trois « must ») → une phrase : chaque message dit le chiffre source, la comparaison, la lecture proposée et son niveau de confiance ; raison : le board répète le message, pas le tableau.
- L55 « Do not simply copy a table into prose » → « Le lecteur a le tableau ; le récit apporte l'ordre d'importance et le pourquoi. Trois messages au plus en tête. »
- L56 « Do not overinterpret undocumented variations » → « Une variation sans cause dans la source s'écrit "cause non documentée", avec la question à poser et à qui. »
- L57 « Do not hide a deterioration behind an overly diplomatic tone » → « Si l'écart principal est défavorable, il ouvre le récit, chiffré. Raison : un board qui découvre seul un écart caché cesse de croire le reste. »

**Défauts à corriger** : `audience` (direction / board / codir / managerial) et `longueur` (flash / standard / detaillee) non définis dans le corps.

**Exemple à ajouter** : un message clé en deux versions, `<example>` : la mauvaise (« Le CA progresse de 10 % ») et la bonne (CA au-dessus de N-1 mais sous le budget, chiffré, avec le niveau de confiance), et « Why this is right ». Données différentes du cas de test.

**Cas de test**

Demande :
> Prépare le narratif financier du T3 pour le conseil d'administration de jeudi. Chiffres en M€ :
>
> | | T3 2026 réel | T3 2026 budget | T3 2025 |
> |---|---|---|---|
> | Chiffre d'affaires | 4,20 | 4,50 | 3,80 |
> | Marge brute | 1,68 | 1,89 | 1,596 |
> | Charges opérationnelles | 1,45 | 1,40 | 1,30 |
> | EBITDA | 0,23 | 0,49 | 0,296 |
>
> Les charges du T3 incluent 0,15 M€ d'indemnité transactionnelle sur un litige client, non récurrente. Trésorerie : 2,6 M€ au 1er juillet, 2,1 M€ au 30 septembre.

Valeurs de référence (calculées le 2026-10-16) :

| Élément | Valeur |
|---|---|
| CA vs budget / vs N-1 | −0,30 M€ (−6,7 %) / +0,40 M€ (+10,5 %) |
| Taux de marge brute | 40,0 % réel ; 42,0 % budget et N-1 → **−2,0 points** |
| Écart de marge brute vs budget | −0,21 M€ = effet volume (4,2 − 4,5) × 42 % = −0,126 + effet taux (−2 pts) × 4,2 = −0,084 |
| EBITDA vs budget | −0,26 M€ (−53 %) ; vs N-1 −0,066 M€ (−22 %) |
| EBITDA hors indemnité | 0,38 M€ : −0,11 M€ vs budget, +0,084 M€ vs N-1 (+28 %) |
| Charges hors indemnité | 1,30 M€ : 0,10 M€ sous le budget |
| Marge d'EBITDA | 5,5 % publiée ; 9,0 % retraitée ; budget 10,9 % ; N-1 7,8 % |
| Trésorerie | −0,50 M€ sur le trimestre pour un EBITDA de +0,23 M€ → écart de 0,73 M€ non expliqué par les données |

Une bonne sortie contient :
1. Un message principal qui ouvre sur l'écart au budget (EBITDA −0,26 M€, CA −6,7 %), pas sur la croissance vs N-1 seule.
2. La croissance vs N-1 (+10,5 %) donnée aussi, les deux comparaisons nommées.
3. La baisse de marge brute exprimée en points (−2 points), pas en « −4,8 % ». *(échoue probablement avec 1.1.0)*
4. L'indemnité de 0,15 M€ présentée à part : EBITDA publié 0,23 et retraité 0,38, chacun étiqueté. *(échoue probablement avec 1.1.0)*
5. L'écart de marge brute (−0,21 M€) ventilé entre volume (≈ −0,13) et taux (≈ −0,08), ou la limite des données dite.
6. Aucune cause inventée à la baisse du taux de marge : hypothèse marquée ou question posée.
7. L'écart EBITDA / trésorerie (≈ 0,73 M€) signalé comme non expliqué, avec les postes à demander (BFR, investissements, impôt, dette).
8. Les charges hors indemnité sous le budget (−0,10 M€) mentionnées : sinon le lecteur croit à une dérive des coûts.
9. Pour chaque message, chiffre source, comparaison, lecture et niveau de confiance distinguables.
10. Un texte prêt pour le conseil, messages avant détails.

---

### 4. `strategie-prix` (1.1.0) — en attente partielle de Q10

**Ce qui peut se faire maintenant** (ne tranche pas Q10, vaut que le skill reste, devienne mélange ou soit retiré entre-temps) :
- Reformuler les 4 contraintes (ci-dessous), sans changer le périmètre ni la recommandation finale.
- Dire dans le corps ce que fait `modele_prix` (auto / freemium / tiers / usage / enterprise) et `inclure_tests`.
- Version de patch (1.1.1), pas de savoir ajouté.

**Ce qui attend Q10** : tout le savoir ci-dessous. Enrichir maintenant reviendrait à répondre « enrichir » à la place d'Amiel (travail perdu si « retirer »). Le savoir choisi porte sur la partie qui resterait dans un `strategie-prix` allégé (valeur, segments, modèles candidats). L'arbitrage (étapes 3–4) passerait à `decision` : ne rien investir là.

**Savoir métier prêt pour Q10 = enrichir**
1. **Trois décisions séparées** : le modèle (abonnement, usage, par siège, par résultat, licence, freemium, hybride), la métrique de valeur (ce qui est compté), le niveau de prix et le packaging (paliers, options). Raison : elles se testent différemment et relèvent souvent de personnes différentes. Cela remplace « do not mix price, packaging and go-to-market ».
2. **Critères d'une bonne métrique de valeur** : elle croît avec la valeur reçue par le client, le client la comprend et la prévoit, elle se mesure sans litige, elle croît avec le compte. Source : Ramanujam et Tacke, *Monetizing Innovation* (Wiley, 2016) ; chapitre non vérifié.
3. **Consentement à payer**, méthodes et limites :
   - Van Westendorp (4 questions ; donne une plage acceptable, pas un prix optimal) ;
   - Gabor-Granger (achat à des prix donnés ; surestime le consentement déclaré) ;
   - analyse conjointe (arbitrages entre attributs ; coûteuse) ;
   - test réel (A/B ou nouvelle cohorte), seule mesure du comportement.
   - Sans aucune de ces données : une plage ou des prix à tester, pas un prix.
4. **Volume d'équilibre d'un changement de prix** (Nagle, Müller et Gruyaert, *The Strategy and Tactics of Pricing*, 6e éd., Routledge 2018 ; chapitre non vérifié ; formule vérifiée par calcul le 2026-10-16) : variation de volume tolérée = −Δp / (m + Δp), où Δp est la variation de prix en fraction du prix initial et m le taux de marge sur coût variable. Hausse de 10 % à 60 % de marge : −0,10 / 0,70 = 14,3 % de volume perdable. Baisse de 10 % à 80 % de marge : il faut +14,3 % de volume.
5. **Hausse sur une base installée** : conditions contractuelles de révision (date de renouvellement, préavis), maintien de l'ancien prix pour les clients existants (« grandfathering ») ou migration, communication. Ne pas citer d'article : la règle est dans le contrat B2B.
6. **Règles françaises** (vérifiées le 2026-10-16), pour les prix aux consommateurs :
   - **C. conso. art. L112-1-1** : toute annonce de réduction de prix indique le prix antérieur, c'est-à-dire le prix le plus bas pratiqué sur les 30 jours précédents ; en vigueur depuis le 28/05/2022. https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044549592/2022-05-28
   - **C. com. art. L420-5** : interdit les prix de vente aux consommateurs abusivement bas par rapport aux coûts de production, de transformation et de commercialisation, s'ils visent ou peuvent avoir pour effet d'éliminer une entreprise d'un marché ou de l'empêcher d'y entrer. Ne s'applique pas à la revente en l'état. Version en vigueur depuis le 01/01/2026. https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000052094370/2026-01-01 (concerne un prix de pénétration très bas vendu à des consommateurs)
   - **C. com. art. L442-5** : interdit de revendre en l'état sous le prix d'achat effectif (revente à perte), avec des exceptions (soldes, fin de saison, alignement en petit magasin…). Version en vigueur depuis le 15/04/2025. https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051467834/2025-04-15 (concerne la revente de produits, pas un service ou un logiciel)
7. **Ancrage et paliers** : l'offre « bon / mieux / meilleur » oriente vers le palier du milieu ; l'option haute sert d'ancre. Connu du modèle : une ligne suffit.

**Reprises kwp** : aucune (seule une mention du modèle de prix dans `product-management/competitive-brief`).

**Contraintes à reformuler (maintenant)**
- L34 « You must always propose a pricing recommendation with clear trade-offs » → « Termine par une option recommandée et ce qu'elle sacrifie : une liste d'options laisse le décideur là où il était. » (Si Q10 = mélange, cette ligne part avec la recommandation.)
- L53 « Do not recommend a pricing without stating its assumptions » → « Écris à côté du prix recommandé les hypothèses de volume, de conversion et de consentement à payer qui le portent. »
- L54 « Do not mix price, packaging, and go-to-market » → garder, avec sa raison (savoir 1).
- L55 « Do not oversell a precision that the data does not support » → « Sans mesure du consentement à payer, donne une plage ou des prix à tester. »
- L56 « Always surface the trade-offs » → supprimer (doublon de L34).

**Défauts à corriger** : `modele_prix` et `inclure_tests` non définis (maintenant). Domaine `fondateur` : laisser.

**Exemple à ajouter (si enrichi)** : une ligne « volume d'équilibre » (prix, marge, variation de prix, volume perdable) avec « Why this is right ». Données différentes du cas de test.

**Cas de test** (pour la version enrichie ; à jouer aussi sur 1.1.0 pour la référence)

Demande :
> On vend notre outil à 49 €/mois par utilisateur, marge brute 80 %, 1 200 utilisateurs payants (PME françaises, contrats mensuels). On pense passer à 59 €. Combien d'utilisateurs on peut perdre avant d'y perdre ? Et est-ce que le « par utilisateur » est le bon modèle, nos clients se plaignent de payer pour des gens qui se connectent une fois par mois ?

Valeurs de référence (calculées le 2026-10-16) :

| Élément | Valeur |
|---|---|
| Δp | 10 / 49 = 20,4 % |
| Coût variable par utilisateur | 49 × 20 % = 9,80 € |
| Contribution mensuelle actuelle | 1 200 × 39,20 = **47 040 €** |
| Utilisateurs pour la même contribution à 59 € | 47 040 / 49,20 = **956** |
| Perte tolérée | **244 utilisateurs, soit 20,3 %** = 0,204 / (0,80 + 0,204) |

Une bonne sortie contient :
1. La perte tolérée ≈ 20 % (≈ 244 utilisateurs), formule et entrées montrées. *(échoue probablement avec 1.1.0 : pas de calcul d'équilibre)*
2. Le raisonnement sur la marge sur coût variable, pas sur le chiffre d'affaires.
3. Le niveau de prix (49 → 59) séparé de la question du modèle (par siège ou autre).
4. Au moins deux métriques de valeur de rechange (utilisateurs actifs, volume traité, palier par compte), jugées sur les critères de la bonne métrique. *(échoue probablement avec 1.1.0)*
5. La plainte des clients reliée à une métrique de valeur qui ne suit pas la valeur reçue.
6. Une méthode pour mesurer le consentement à payer ou un test proposé (nouvelle cohorte à 59 €, par exemple), sans prix « optimal » affirmé sans données.
7. Le traitement des clients existants (préavis, maintien temporaire de l'ancien prix) mentionné.
8. Une recommandation avec ce qu'elle sacrifie et les hypothèses qui la feraient changer.
9. Aucune règle de droit de la consommation plaquée sur une vente B2B (L112-1-1 ne concerne que les consommateurs).

---

### 5. `note-strategique` (1.1.0 → 1.1.1)

**Savoir à ajouter** (peu ; le modèle connaît la pyramide de Minto) :
1. **En tête, la décision demandée** : qui décide, quoi, pour quand, et ce qui se passe sans décision. Raison : le destinataire lit les premières lignes pour savoir ce qu'on attend de lui.
2. **L'option « ne rien faire » parmi les options**, avec son coût. Raison : sans elle, toute option paraît meilleure que rien.
3. **Ce qui ferait changer la recommandation** (1 à 3 conditions) dans « risques et hypothèses ». Raison : le décideur sait quoi surveiller après sa décision.
4. **Réversibilité** de chaque option (coût d'un retour en arrière), une ligne : elle règle souvent le niveau de preuve demandé.

**Reprises kwp** : aucune.

**Contraintes à reformuler**
- L32 « You do not produce a repurposed internal report » → « Le destinataire décide ; tout ce qui ne sert pas sa décision va en annexe ou disparaît. »
- L33 et L53 (« begins with the conclusion », deux fois) → une fois, avec la raison ci-dessus.
- L34 « You do not hide risks or assumptions to appear more solid » → savoir 3.
- L54 « Do not produce more than 2 equivalent pages without justification » → « Deux pages par défaut, parce qu'un comité les lit en séance ; le détail en annexe ; la longueur suit `longueur` si elle est donnée. »
- L55 « Do not drown the recommendation in nuances » → « Une phrase de recommandation ; les nuances vont dans les risques. »
- L56 « Each section must bring new information » → garder, sans « must ».

**Défauts à corriger** : `destinataire`, `longueur` (flash / standard / detaillee) et `inclure_risques` non définis dans le corps.

**Exemple à ajouter** : non nécessaire. Au plus, le gabarit des 4 lignes de tête (décision demandée, recommandation, raison principale, coût ou risque majeur).

**Cas de test**

Demande :
> Il me faut une note pour le CODIR de mardi. Notre outil de ticketing interne arrive en fin de support en juin 2027. Trois pistes : migrer vers un SaaS du marché (≈ 45 k€/an, 4 mois de projet), redévelopper en interne (2 développeurs pendant 6 mois, la DSI dit qu'elle n'a personne avant mars), ou prolonger avec un support tiers (18 k€/an, sans évolutions). L'équipe support veut le SaaS. Je penche aussi pour le SaaS.

Une bonne sortie contient :
1. Dans les 5 premières lignes : la décision demandée, qui la prend et pour quand (avant la date qui rend juin 2027 tenable).
2. Une recommandation en une phrase dans le résumé.
3. Le statu quo (prolonger sans rien changer) traité comme une option, avec son coût et son risque. *(échoue probablement avec 1.1.0)*
4. La contrainte de calendrier chiffrée : le redéveloppement interne (début en mars + 6 mois = septembre 2027) dépasse juin 2027.
5. Les trois options comparées sur les mêmes critères (coût, délai, risque, réversibilité).
6. Une ou plusieurs conditions qui feraient changer la recommandation. *(échoue probablement avec 1.1.0)*
7. Faits (montants, dates donnés) et hypothèses (durée de projet SaaS, coût de migration non donné) distinguables.
8. Deux pages au plus ; aucun historique de l'outil avant la conclusion.

---

### 6. `tam-sam-som` (1.1.0 → 1.2.0)

**Savoir métier à ajouter** (pratique courante du capital-risque, pas de source normative ; présenter comme positions par défaut)
1. **Définitions opérationnelles** :
   - TAM : dépense annuelle totale pour le besoin dans le périmètre géographique, si 100 % des clients possibles achetaient ;
   - SAM : la part que le modèle de l'entreprise peut servir (segments, géographie, canal, contraintes techniques ou réglementaires) ;
   - SOM : ce qui est réaliste de capter à un horizon daté, compte tenu de la concurrence et de la capacité commerciale.
   - Toujours en €/an (récurrent) avec l'année de référence, pas en cumul.
2. **Bottom-up d'abord** : nombre de clients cibles × prix annuel (ou panier × fréquence), chaque facteur sourcé. Raison : la revue a relevé qu'en un seul passage le bottom-up s'ancre sur le top-down calculé juste avant ; le calculer en premier réduit cet ancrage.
3. **Top-down ensuite** : chiffre de marché publié × filtres de périmètre, chaque filtre justifié. Piège : le rapport couvre un périmètre plus large (toutes catégories de logiciels, Europe entière, matériel compris).
4. **Comparer** : si top-down et bottom-up diffèrent de plus d'un facteur 2 environ, expliquer l'écart par le périmètre ou par une hypothèse, sans faire de moyenne. (Le facteur 2 est un repère proposé, non sourcé : à valider.)
5. **SOM par la capacité, pas par un pourcentage** : vendeurs × signatures par vendeur × prix × durée, attrition comprise, ou une part de marché comparée à des acteurs observés. Un « 1 % du TAM » sans raisonnement est le signal d'un SOM non défendable.
6. **Contrôles** : SOM ≤ SAM ≤ TAM ; unités et année identiques ; le SOM est cohérent avec le plan commercial ; une fourchette basse / haute pour chaque niveau.
7. **Sources publiques françaises** à proposer : INSEE (répertoire Sirene, statistiques d'entreprises par taille et secteur), Eurostat (statistiques structurelles d'entreprises), statistiques d'ordres et de ministères selon le secteur (p. ex. DREES pour les professions de santé). Donner l'année de chaque donnée.

**Modes** (annexe B), sur le modèle du pilote :
- `flash` : chiffres de marché de mémoire autorisés, avertissement en tête ;
- `standard` : chiffres de marché sourcés avec un outil de recherche (URL, date) ;
- `deep` : plusieurs sources par chiffre clé, divergences dites.
- Les chiffres fournis par l'utilisateur ne demandent jamais de recherche et ne déclenchent pas l'avertissement.
- Écrire « a search tool », pas `web_search` (le nom change selon l'environnement).
- Défaut si rien n'est dit : `standard` si un outil de recherche existe, sinon `flash` avec l'avertissement.
- `.mystaffy.json` n'a pas de paramètre de profondeur : proposer d'ajouter `niveau_profondeur` (flash / standard / deep), comme `metriques-saas`, à confirmer par Amiel (ce n'est pas un changement de forme).

**Reprises kwp** : aucune (pas d'équivalent).

**Contraintes à reformuler**
- L34 « must always state the calculation method and hypotheses before announcing… figures » → « Montre la méthode et les facteurs avant chaque chiffre : un investisseur conteste un facteur, pas un total. »
- L36–37 (« must be sourced via web_search », « memory is not a valid source ») → définition des modes ci-dessus.
- L56 « Do not give figures without an explicit method » → supprimer (doublon de L34).
- L57 « Do not hide the uncertainty of hypotheses » → « Donne une fourchette basse / haute pour chaque niveau, en nommant le facteur qui la fait bouger. »
- L58 « Do not confuse total, addressable, capturable market » → remplacé par les définitions (savoir 1).

**Défauts à corriger** : modes non définis (annexe B) ; `methode_principale` (mixte / top-down / bottom-up) non défini dans le corps (dire : il change l'ordre et le poids, mais le contrôle croisé reste fait si les données le permettent).

**En attente** : Q8 seulement (vérification isolée). L'isolement des deux estimations est un besoin de moteur (revue §1.2), pas une question : on ne le traite pas.

**Exemple à ajouter** : une ligne de bottom-up (« établissements cibles × prix annuel = €/an », chaque facteur avec source et année) et « Why this is right ». Données différentes du cas de test.

**Cas de test**

Demande (mode flash) :
> Mode flash, j'ai besoin d'un ordre de grandeur pour le pitch de vendredi. On vend un logiciel de gestion des plannings pour cabinets dentaires en France, 150 €/mois par cabinet. Mes données : environ 38 000 chirurgiens-dentistes libéraux, 1,6 praticien par cabinet en moyenne ; à peu près 40 % des cabinets ont un logiciel de gestion avec agenda intégré et ne changeront pas. Un rapport dit que le marché européen des logiciels dentaires pèse 1,2 Md€. Côté équipe : 3 commerciaux, environ 8 signatures par mois chacun. Horizon 3 ans.

Valeurs de référence (calculées le 2026-10-16 ; données fictives fournies par l'utilisateur) :

| Élément | Valeur |
|---|---|
| Cabinets | 38 000 / 1,6 = **23 750** |
| TAM (bottom-up) | 23 750 × 150 × 12 = **42,75 M€/an** |
| SAM (60 % non équipés) | **25,65 M€/an** |
| SOM à 3 ans (capacité, sans attrition) | 3 × 8 × 36 = 864 cabinets × 1 800 € = **1,56 M€ d'ARR** ≈ 6 % du SAM |
| Top-down naïf | 1,2 Md€ × part France (≈ 15 % si supposée) ≈ 180 M€ : **tous logiciels dentaires**, pas les plannings seuls |

Une bonne sortie contient :
1. TAM ≈ 42,75 M€/an, calculé bottom-up, facteurs et unités (€/an) visibles.
2. SAM ≈ 25,65 M€/an avec le filtre des 40 % justifié.
3. SOM tiré de la capacité commerciale (≈ 864 cabinets, ≈ 1,56 M€ d'ARR à 3 ans), pas d'un pourcentage du marché. *(échoue probablement avec 1.1.0)*
4. Le chiffre de 1,2 Md€ jamais retenu comme TAM : son périmètre (Europe, toutes catégories de logiciels) est dit plus large, et l'écart au bottom-up expliqué. *(échoue probablement avec 1.1.0)*
5. Toute part France supposée (≈ 15 % par exemple) marquée comme hypothèse.
6. SOM ≤ SAM ≤ TAM respecté.
7. L'attrition et le temps de montée en charge des commerciaux signalés comme facteurs qui réduisent le SOM.
8. Avertissement « mode flash » limité aux chiffres de mémoire ; les données de l'utilisateur ne sont pas présentées comme « potentiellement périmées ».
9. Une fourchette ou les facteurs les plus sensibles nommés (praticiens par cabinet, taux d'équipement).
10. Les données à vérifier avant le pitch, avec une source publique proposée pour chacune.

---

### 7. `metriques-saas` (1.1.0) — pilote

Pilote déjà réécrit (1.2.0 sur le disque) et cas de test existant (`tests/cas-skills/metriques-saas.md`). Non réévalué. Seul point en attente : Q8 (vérification isolée).

---

### 8. `tableau-de-bord-kpi` (1.1.0 → 1.2.0)

**Savoir métier à ajouter**
1. **Définition exacte** de chaque KPI : numérateur, dénominateur, filtre, période, règle de date. Raison : « taux de conversion » ou « délai de réponse » (moyenne ou médiane, heures ouvrées ou calendaires) cachent des calculs différents d'une équipe à l'autre.
2. **Mesure de départ avant cible** (kwp `product-management/skills/metrics-review/SKILL.md` L268–273 : niveau de départ, comparaison externe, tendance, effort, confiance ; cible engagée et cible haute). Sans mesure de départ, la cible s'écrit « à fixer après N périodes de mesure (date) » et le KPI passe dans « sous hypothèse ». Cela corrige la règle actuelle, qui pousse à inventer une cible.
3. **Indicateur de contrepoids** : chaque KPI qu'on pousse est apparié à un indicateur qui révèle sa manipulation ou son effet pervers (délai de résolution ↔ taux de réouverture). Sources : Andy Grove, *High Output Management* (1983), indicateurs appariés ; loi de Goodhart (C. Goodhart, 1975, dans la formulation de M. Strathern, 1997 : une mesure qui devient un objectif cesse d'être une bonne mesure). Chapitres non vérifiés.
4. **Un responsable par KPI** (qui agit quand il bouge), distinct du destinataire.
5. **Seuil d'alerte** et action déclenchée pour les KPI opérationnels ; alerte sans action = bruit (kwp L363–375).
6. **Même période sur une vue** ; avancé et résultat sur la même ligne de lecture (kwp L334, principe 5).
7. **Anti-modèles** (kwp L355–362) : métrique de vanité (total cumulé qui ne baisse jamais), chiffre sans comparaison, tableau d'activité de l'équipe au lieu de résultats, un seul tableau pour tous les publics.

**Reprises kwp** : `product-management/skills/metrics-review/SKILL.md` L268–273, L319–334 (principes), L355–362 (anti-modèles), L363–375 (alertes). Adapter : vocabulaire français (cible engagée / cible haute). À créditer.

**Contraintes à reformuler**
- L33–34 « A KPI without a measurement metric and without a target is not a KPI — it is a wish. You refuse to validate non-measurable or non-actionable indicators » → « Un KPI a une définition mesurable et une cible ; sans mesure de départ, la cible est datée "à fixer", et le KPI reste sous hypothèse : une cible inventée serait pire que pas de cible. » Adapter la fin de la description (« Refuse un KPI sans cible mesurable »).
- L35 « You must distinguish directly measurable / estimable / problematic » → garder, avec la raison : le lecteur sait ce qu'il faut construire avant que le tableau marche.
- L55 « Each KPI must have an identifiable data source » → « … une source nommée (outil, table, champ) ; sinon il va dans les KPI problématiques avec ce qu'il faudrait collecter. »
- L56 « Do not create non-actionable KPIs — if nothing can be done with it, it pilots nothing » : bon modèle (la raison est là), garder.

**Défauts à corriger** : `destinataire`, `domaine` (saas / ecommerce / service / rh / marketing / support) et `nb_kpis_max` (5–20) non définis dans le corps ; `nb_kpis_max` à 15–20 contredit « 5 à 10 » : dire que le paramètre l'emporte, et que l'excédent va en vue de détail.

**Exemple à ajouter** : une fiche KPI d'une ligne (définition avec numérateur / dénominateur, mesure de départ, cible ou « à fixer », contrepoids, responsable, seuil d'alerte) et « Why this is right ». Domaine différent du cas de test (pas du support).

**Cas de test**

Demande :
> Je dirige le support client d'un SaaS B2B, 8 personnes, on est sur Zendesk. La direction a fixé deux objectifs 2027 : réduire le churn causé par un mauvais support et tenir nos SLA contractuels (première réponse en 4 h ouvrées pour les clients Premium). Aujourd'hui je sais que le délai médian de première réponse est de 6 h et que le CSAT est à 82 %. On ne mesure pas les réouvertures, et les motifs de résiliation ne sont pas renseignés dans le CRM. Fais-moi le tableau de bord.

Une bonne sortie contient :
1. Entre 5 et 10 KPI, séparés en vue direction et vue équipe.
2. Chaque KPI défini avec numérateur, dénominateur, période et règle (médiane ou moyenne, heures ouvrées).
3. Des cibles seulement là où une mesure de départ existe (délai de première réponse, CSAT) ; « à fixer après N semaines de mesure » pour le taux de réouverture. *(échoue probablement avec 1.1.0 : la règle pousse à inventer une cible)*
4. Le KPI « churn causé par le support » classé problématique, avec la donnée à collecter (motif de résiliation obligatoire dans le CRM).
5. Au moins un couple KPI / contrepoids (délai de première réponse avec CSAT ou réouvertures). *(échoue probablement avec 1.1.0)*
6. Le SLA Premium (4 h ouvrées) suivi en % de tickets dans le délai, avec un seuil d'alerte et un responsable.
7. Indicateurs avancés et de résultat distingués.
8. Un responsable nommé par KPI (un rôle, pas « l'équipe »).
9. Aucune métrique de vanité (total des tickets traités depuis l'origine) ou d'activité seule.
10. Une décision ou une action rattachée à chaque KPI.

---

### 9. `analyse-concurrentielle` (1.1.0 → 1.2.0)

**Savoir métier à ajouter**
1. **Quatre niveaux de concurrents et la non-consommation** (kwp `product-management/skills/competitive-brief/SKILL.md` L99–118) :
   - direct : même problème, mêmes utilisateurs, même manière ;
   - indirect : même problème, autre manière ;
   - adjacent : pas concurrent aujourd'hui, peut le devenir ;
   - substitut : tableur, embauche, sous-traitance, ne rien faire.
   - Cela remplace « do not confuse direct / indirect / substitute ».
2. **Axes de la carte de positionnement** choisis sur les critères d'achat du client cible, pas sur les fonctions du produit (kwp PM L120–130 ; marketing L233–244). Deux axes qui montrent un espace libre ou encombré.
3. **Échelle de notation** fort / correct / faible / absent, notée sur des preuves (essai, avis clients, documentation), pas sur la communication du concurrent (kwp PM L149–163, L176–182).
4. **Prix comparés avec leurs réserves** : unité facturée, paliers, seuil de gratuité, prix public ou négocié, date du relevé (kwp PM L298).
5. **Preuve et date** : chaque fait sur un concurrent porte sa source et sa date, ou « mémoire, non vérifié ». Raison : un paysage concurrentiel se périme en mois.
6. **Forces des concurrents dites franchement** (kwp PM L296) : une analyse où l'on gagne partout n'est pas crue.
7. **Quand Porter sert** : les cinq forces jugent l'attrait d'un secteur (entrer ou non), pas la différenciation d'un produit. Le dire pour `cadre_analyse = five-forces`. Source : M. Porter, *Competitive Strategy* (1980), connu du modèle ; une ligne suffit.
8. **Pièges du positionnement** (kwp marketing L252–257) : se positionner contre un concurrent plutôt que pour un besoin, trop de différenciateurs, différenciation par fonctions plutôt que par résultat.

**Modes** (annexe B) : même définition que pour `tam-sam-som`. En `deep`, une fiche par concurrent puis la comparaison (le parallèle est un besoin de moteur, hors réécriture). Les faits fournis par l'utilisateur ne déclenchent pas l'avertissement.

**Paramètre `cadre_analyse`** : définir les quatre valeurs.
- `mixte` : défaut ;
- `five-forces` : attrait du secteur ;
- `positionnement` : carte à deux axes et espaces libres ;
- `benchmark-produit` : matrice de capacités notées.

**Reprises kwp** : PM `competitive-brief` L99–130, L149–163, L176–182, L296–298 ; marketing `competitive-brief` L233–244, L252–257. À créditer.

**Contraintes à reformuler**
- L34 « You must always surface the differentiation logic » → « Termine sur la logique de différenciation : un inventaire d'acteurs ne dit pas où se placer. »
- L36–37 (modes) → définition ci-dessus.
- L56 « Do not confuse direct competitor, indirect competitor, and substitute » → remplacé par le savoir 1.
- L57 « Do not produce a descriptive inventory without strategic reading » → supprimer (doublon de L34).
- L59 « Do not present market hypotheses as established facts » → savoir 5.

**Défauts à corriger** : modes non définis (annexe B) ; `cadre_analyse` non défini dans le corps.

**Exemple à ajouter** : une ligne de matrice (capacité, note par acteur, source et date de la note) et « Why this is right ». Concurrents fictifs différents de ceux du cas de test.

**Cas de test**

Demande :
> Mode flash. On lance Notafrais, une appli de notes de frais pour TPE (1 à 10 salariés), à 6 € par utilisateur et par mois. Nos prospects nous comparent à : Fraizo (9 € par utilisateur et par mois, intégré aux logiciels comptables), Kipnote (gratuit jusqu'à 3 utilisateurs, puis 12 € par mois et par entreprise), le tableur Excel que l'expert-comptable leur fournit, et l'expert-comptable qui ressaisit les tickets lui-même. Fais-moi l'analyse concurrentielle, je dois choisir notre angle de différenciation.

(Fraizo et Kipnote sont fictifs : le modèle ne doit rien « savoir » d'eux.)

Une bonne sortie contient :
1. Les acteurs classés : Fraizo et Kipnote directs ; le tableur Excel substitut ou non-consommation ; l'expert-comptable qui ressaisit, substitut sous forme de service. *(échoue probablement avec 1.1.0 : pas de niveau substitut de service ni de non-consommation)*
2. La comparaison de prix rapportée à une même unité, pour une TPE de 3 et de 8 salariés : Notafrais 18 / 48 €, Fraizo 27 / 72 €, Kipnote 0 / 12 € par mois, avec la réserve des paliers.
3. Le constat que Kipnote est moins cher que Notafrais à toutes les tailles de TPE (gratuit jusqu'à 3, puis forfait par entreprise) : le prix ne peut pas être l'angle face à lui. *(échoue probablement avec 1.1.0)*
4. Aucune information inventée sur Fraizo ou Kipnote au-delà de la demande ; ce qui est supposé (fonctions, intégrations) est marqué « à vérifier ».
5. Avertissement « mode flash » en tête pour ce qui viendrait de mémoire, sans l'appliquer aux faits donnés par l'utilisateur.
6. Des axes de comparaison tirés des critères d'achat d'une TPE (temps de saisie, lien avec l'expert-comptable, prix), pas une liste de fonctions.
7. Les forces des concurrents dites (intégration comptable de Fraizo, gratuité de Kipnote).
8. Le rôle de l'expert-comptable traité aussi comme prescripteur ou canal, pas seulement comme concurrent.
9. Une conclusion sur la logique de différenciation, avec ses hypothèses à vérifier, sans plan d'action détaillé.
