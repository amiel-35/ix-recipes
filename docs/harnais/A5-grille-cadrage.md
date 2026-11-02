# A5 : grille fixe du cadrage

Neuf règles qui jugent un cadrage. Elles valent pour **tous les sujets**, quel que soit leur type. Elles reprennent, sans l'affaiblir, la « grille fixe du cadrage » de la procédure (`corpus/procedure-traitement-sujet.md`, étape 1) : chaque règle garde le sens du point d'origine, avec les critères qui permettent de la juger.

## En-tête

**Qui l'applique.**
- L'agent de l'évaluation (étape 1d) : il juge le cadrage avec cette grille.
- L'auteur de la clôture (étape 1e) : il écrit son cadrage clos pour tenir cette grille. Il la lit avant d'écrire.
- Un agent distinct de cet auteur, qui applique les neuf points au cadrage clos une fois celui-ci écrit.

**Avec quel skill.** `ix-skills:controle-qualite`, en mode `verdict`. Cette grille est le **référentiel** (`reference`) ; le cadrage est le **livrable** (`deliverable`) ; les neuf points sont les suspicions (`suspected`), identifiées G1 à G9. Chaque suspicion est une infraction présumée. Le verdict est rendu **par point**, jamais sur le cadrage dans son ensemble : `breach` (la règle est enfreinte), `compliant` (elle est tenue), `doubtful` (deux lectures du passage, toutes deux données), `not found`, `outside reference`.

**Comment former les suspicions.** Pour chaque point à juger, l'agent cite le passage exact du cadrage qui porte la règle. Si la règle exige un élément absent du cadrage, la suspicion cite le passage où il devrait figurer (le titre voisin) et le verdict dit ce qui manque.

**Quand.** Deux moments, et la grille dit pour chaque point s'il s'applique au premier.

| Moment | Quoi | Points jugés |
|---|---|---|
| **Avant la pause 1** (étape 1d) | Le cadrage est complet mais pas encore clos : des questions bloquantes attendent la réponse du pilote. | G1, G2, G4, G5, G6, G7, G8. **G3 et G9 ne s'appliquent pas** : ils échouent par construction tant que la pause n'a pas eu lieu (le cadrage a des questions bloquantes ouvertes, donc on ne peut pas encore en dériver un goal sans question). Leur verdict d'infraction littérale n'est pas un défaut du cadrage : le pilote les note « attente de la pause 1 », sans verdict, et ils ne sont pas dans la liste des suspicions. |
| **Après la pause 1** (étape 1e) | Le cadrage clos intègre les réponses du pilote comme des décisions. | Les neuf points, G1 à G9, sans exception. |

Le nombre de passes de l'évaluation avant la pause est borné par le plafond `passes_verification_max` des réglages (`partie-a/A4-reglages.yaml`). Avant la pause, une partie des verdicts `doubtful` ou des infractions tient à une réponse attendue du pilote, non à un défaut du document : le juge sépare dans chaque verdict ce qui est une **attente de la pause 1** de ce qui est un **défaut corrigeable** dès maintenant.

**Relecture de cette grille.** Elle est relue **une fois** par le modèle de contre-vérification des réglages (clé `modeles.contre_verification`), après l'accord du pilote. Pour cette version, la relecture a été faite par Fable le 18/10/2026 (`trace/05a-relecture-A5.md`). Le juge de l'étape 5 a vérifié sa fidélité à la procédure (`trace/05-jugement.md`, ligne 51).

**Version figée, hors du producteur.** Cette version (1.2, du 18/10/2026) a été corrigée par la session de pilotage, et non par le producteur. Elle sert de référentiel en lecture seule à la suite : le producteur ne la modifie pas. Une grille qui note les essais du producteur ne doit pas pouvoir être changée par lui.

Changements depuis la version jugée (étiquette `partie-a-jugee`) :
- **G2** : la conformité exige ce que la règle demande, et l'exception « question ouverte » ne vaut qu'avant la pause (TST-1) ;
- **G5** : la règle définit la contrainte par ce qu'elle fait, et distingue une raison d'une source (AMB-1, HYP-1) ;
- **G6** : une hypothèse acceptée par défaut, sans avoir été soulevée, n'est pas un risque accepté (décision d'Amiel du 18/10/2026), et la règle ne se contredit plus (AMB-2) ;
- **G8** : un test vrai entraîne le découpage, comme dans la procédure, sauf décision contraire du décideur, citée (ligne 51 du jugement) ;
- **G9** : la clause sur les autorisations est précisée (AMB-3).

Changements de la 1.2, après le rejugement du tour 1 (`trace/06-rejugement-tour1.md`, ligne 51) et sur décision d'Amiel du 18/10/2026 :
- **G6** : aucune hypothèse « à confirmer » ne reste dans un cadrage clos. Celles qui apparaissent après la pause vont dans un rappel, et le cadrage n'est clos qu'une fois le rappel répondu ou laissé passer. Toutes les hypothèses restantes sont donc des risques acceptés, comme le veut la procédure. La marque peut s'accorder ;
- **G5** : l'exception « imposée sans autre raison » est retirée. Une contrainte sans raison devient une question résiduelle ;
- **G8** : l'exception « le décideur refuse de découper » est retirée. Un test vrai entraîne le découpage.

## Les neuf points

### G1. L'intention est un but, pas un artefact

- **Règle.** L'intention dit ce qui doit être vrai une fois le sujet traité, pour des personnes ou une situation : un but. Elle n'est pas formulée comme la chose à produire (une application, un document, un module, un skill).
- **S'applique avant la pause 1 :** oui.
- **Conforme** si l'intention peut se vérifier sans nommer d'artefact, et si les artefacts évoqués apparaissent ailleurs comme moyens, contraintes ou hypothèses, avec leur place dite. **Infraction** si l'intention se réduit à « produire X » ou « faire X », où X est un artefact. **Douteux** si l'intention nomme un artefact tout en disant le but qu'il sert : le juge donne les deux lectures.

### G2. Le public et la situation d'usage sont décrits

- **Règle.** Le cadrage dit qui utilise ou reçoit le résultat, et dans quelle situation : ce qu'il en fait, quand, avec quels moyens. Le public et la situation sont décrits, pas seulement nommés.
- **S'applique avant la pause 1 :** oui, avec une réserve qui ne vaut **qu'avant la pause**. Un public dont l'identité dépend d'une question bloquante encore ouverte est décrit pour ce qui est connu et renvoyé à cette question : le juge classe le reste en **attente de la pause 1**. Il ne le compte pas comme infraction.
- **Conforme** si chaque public, y compris chaque destinataire ou validateur d'un livrable, est décrit : ce qu'il fait du résultat, quand, et avec quels moyens quand ils ne vont pas de soi (pour un validateur : ce qu'il valide, à quel moment, sur quel support). **Infraction** si un public ou la situation d'usage manque, ou n'est que nommé. Avant la pause, ce n'est pas une infraction quand cela tient à une question bloquante ouverte. Après la pause, l'exception ne s'applique plus : un public renvoyé à une question résiduelle est une infraction. **Douteux** si la description est présente mais qu'il lui manque l'un des trois éléments (ce qu'il fait, quand, moyens) dans une seule des deux lectures.

### G3. Aucune question bloquante n'est ouverte

- **Règle.** Aucune question bloquante n'est ouverte. Une question est bloquante quand, sans sa réponse, on ne peut pas dériver le goal ou les critères. Chaque question bloquante reçoit une décision, qui cite sa source. Une question qui reste sans réponse est écrite comme **question résiduelle** et dit pourquoi elle ne bloque ni le goal ni les critères.
- **S'applique avant la pause 1 :** **non.** Avant la pause, les questions bloquantes sont ouvertes par construction, et elles attendent la réponse du pilote.
- **Conforme** si chaque question bloquante a une décision et sa source, et si chaque question résiduelle dit pourquoi elle ne bloque rien. **Infraction** si une question bloquante est encore posée, ou si une question laissée ouverte conditionne le goal ou les critères. **Douteux** si la raison qui la dit non bloquante se lit de deux façons.

### G4. Le hors-périmètre est écrit

- **Règle.** Le cadrage liste ce qui est hors périmètre : ce qu'on ne fait pas dans ce sujet, ce qui est renvoyé à plus tard ou à un autre sujet. La liste est écrite, concrète, et ne se réduit pas à « le reste ».
- **S'applique avant la pause 1 :** oui. Qu'un hors-périmètre proposé soit confirmé relève de la pause 1.
- **Conforme** si une section nomme les exclusions, avec leur destination quand elle existe. **Infraction** si aucune exclusion n'est écrite. **Douteux** si la liste ne tient qu'en une phrase générale.

### G5. Chaque contrainte a sa raison

- **Règle.** Chaque contrainte est écrite avec sa **raison**. Une contrainte, c'est tout ce qui limite la réponse : ce qu'il faut faire, ne pas faire ou respecter. Elle reste une contrainte quelle que soit la section où le cadrage la range (« contraintes », « décisions », « interdits transmis au goal »), et renommer une contrainte ne la soustrait pas à la règle. La **raison** dit pourquoi la contrainte tient. La **source** dit d'où elle vient. Une citation de la demande ou d'un décideur qui redit la contrainte est une source, pas une raison. Une contrainte dont le décideur n'a pas donné la raison n'est pas encore tenue : le cadrage en fait une question résiduelle, posée au décideur.
- **S'applique avant la pause 1 :** oui.
- **Conforme** si chaque contrainte, où qu'elle soit rangée, a une raison qui dit pourquoi elle tient, et sa source quand elle existe. **Infraction** si une contrainte n'a pas de raison, si sa raison ne fait que la reformuler, ou si sa seule « raison » est une citation qui la redit. **Douteux** si la raison est présente mais ne justifie la contrainte que dans une lecture.

### G6. Les hypothèses restantes sont des risques acceptés

- **Règle.** Les hypothèses qui restent sont marquées comme **risques acceptés** : chacune dit le risque qu'on court si elle est fausse, et que ce risque est accepté. Une hypothèse sans risque écrit n'est pas tenue.
- **S'applique avant la pause 1 :** oui, avec une réserve. Avant la pause, chaque hypothèse restante doit avoir son risque écrit ; qu'il soit **accepté** relève de la pause 1 et se classe en attente. Le juge ne compte comme infraction qu'une hypothèse sans risque.
- **Conforme** si chaque hypothèse restante a un risque écrit et, après la pause, la marque **« risque accepté »** avec son origine. Une origine est l'une de ces trois sources :
  - une réponse du décideur, citée ;
  - un défaut proposé à la pause, ou une hypothèse que le cadrage soumis portait avec son risque, que le décideur a vu à la pause et laissé passer ;
  - une réponse au rappel, ou un rappel laissé passer, pour une hypothèse apparue après la pause.

  Le texte de la marque peut s'accorder (« risque accepté », « risques acceptés »).

  **Un cadrage clos ne contient aucune hypothèse « à confirmer ».** Une hypothèse apparue à la clôture, que la pause n'a pas pu voir, n'est pas acceptée à la place du décideur. Elle va dans un **rappel** au décideur, et le cadrage reste **non clos** tant que le rappel n'a pas reçu de réponse ou n'a pas été laissé passer. Le cadrage le dit en tête et sous « Prêt pour l'étape 2 ». Une hypothèse dite ouverte dans le texte a sa ligne dans le tableau.
- **Infraction** si une hypothèse reste sans risque, si elle n'a pas la marque « risque accepté » avec son origine, si elle porte cette marque sans origine valable, ou si un cadrage qui se déclare clos contient une hypothèse « à confirmer » ou un rappel sans réponse. **Douteux** si le risque est écrit mais que l'origine de l'acceptation se lit de deux façons.

### G7. Les livrables sont listés avec leur lecteur, doc comprise

- **Règle.** Chaque livrable est listé avec son **lecteur** (qui le reçoit ou l'utilise). La documentation fait partie des livrables : elle est listée aussi, avec son lecteur. Quand le sujet s'y prête (il construit un système, un outil, un logiciel), la liste comprend une **spec et une architecture**, avec leur lecteur. Quand il ne s'y prête pas, le cadrage dit pourquoi.
- **S'applique avant la pause 1 :** oui. Qu'un livrable soit inclus ou écarté peut dépendre de la pause 1 : le juge classe cet arbitrage en attente.
- **Conforme** si chaque livrable, documentation comprise, a un lecteur ; si le sujet s'y prête, une ligne spec et architecture est présente avec son lecteur ; sinon, la raison est écrite. **Infraction** si un livrable n'a pas de lecteur, si la documentation manque, ou si une spec et une architecture sont attendues et absentes sans raison. **Douteux** si le lecteur est désigné de façon trop large pour être le lecteur d'un document précis.

### G8. Les tests de découpage ont été appliqués

- **Règle.** Les **tests de découpage** de la procédure ont été appliqués, un par un, avec un verdict et sa raison. On découpe si l'un des quatre est vrai :
  1. des parties s'acceptent séparément, chacune avec ses propres utilisateurs ;
  2. une seule grille ne se rejoue plus en environ une heure de recette ;
  3. une partie dépend d'une décision qui n'est pas prise ;
  4. des parties prenantes ont des intérêts en conflit qu'il faut arbitrer séparément.
  Quand un test est vrai, le sujet est découpé : le cadrage nomme les parties et dit laquelle part maintenant.
- **S'applique avant la pause 1 :** oui. Les verdicts qui dépendent d'une décision à venir sont donnés comme conditionnels. Après la pause, ils sont rejoués.
- **Conforme** si les quatre tests ont chacun un verdict et une raison, et si le cadrage tire la conséquence du résultat. **Infraction** si un test manque, ou si un test vrai n'entraîne pas de découpage. **Douteux** si un verdict est donné sans raison, ou n'est pas rejoué après la pause alors qu'il était conditionnel.

### G9. On peut dériver un goal et des critères sans reposer de question

- **Règle.** À partir du cadrage seul, un rédacteur de goal et un rédacteur de critères peuvent travailler sans poser de nouvelle question : le cadrage donne l'intention, les livrables avec leur lecteur, les contraintes et les interdits, ce qui rend le travail fini, et il dit d'où viennent les autres éléments d'un goal (les skills de format et le plafond de tours ne sont pas décidés par le cadrage : ils viennent de la liste des skills de format et des réglages, et le cadrage le dit). Les limites et les modèles des sous-agents viennent aussi des réglages. Ce que le sujet permet ou interdit (ce qu'on peut construire, acheter, décider) reste dans le périmètre et les contraintes du cadrage. Ce n'est pas une rubrique « autorisations » à part, que deux rédacteurs rempliraient différemment. Ce qui reste incertain est écrit comme question résiduelle qui ne bloque pas.
- **S'applique avant la pause 1 :** **non.** Tant que des questions bloquantes sont ouvertes, ces éléments ne sont pas tous fixés.
- **Conforme** si chaque élément nécessaire à un goal et à des critères se lit dans le cadrage, ou est renvoyé à une question résiduelle qui ne bloque pas. **Infraction** si un élément manque et qu'un rédacteur devrait demander. **Douteux** si l'élément est présent mais ambigu au point que deux rédacteurs l'écriraient différemment.

## Lecture rapide

| Point | Règle en une ligne | Avant la pause 1 | Après la pause 1 |
|---|---|---|---|
| G1 | l'intention est un but, pas un artefact | oui | oui |
| G2 | public et situation d'usage décrits | oui, avec réserve | oui |
| G3 | aucune question bloquante ouverte | **non** | oui |
| G4 | hors-périmètre écrit | oui | oui |
| G5 | chaque contrainte a sa raison | oui | oui |
| G6 | hypothèses restantes marquées risques acceptés, avec leur origine ; rien « à confirmer » au cadrage clos | oui, avec réserve | oui |
| G7 | livrables avec lecteur, doc comprise, spec et architecture quand le sujet s'y prête | oui | oui |
| G8 | tests de découpage appliqués | oui | oui |
| G9 | un goal et des critères se dérivent sans reposer de question | **non** | oui |
