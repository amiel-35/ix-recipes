# Test de dérive : résultats (2026-10-16)

Joué selon [`grille.md`](grille.md), écrite avant les sorties. Coût : 1,28 $ (étape 1 sur Opus, jouée deux fois : 0,446 $ et 0,407 $ ; quatre appels Sonnet pour l'étape persona : 0,087 $, 0,088 $, 0,124 $, 0,127 $).

## Le matériau, et son biais

Choisi par Amiel : la restitution d'une vraie étude UX de terrain (plusieurs dizaines d'entretiens), trouvée dans ses archives. Ce n'est pas un jeu de notes brutes : c'est un livrable, **déjà regroupé par thème**. Pour en faire des notes de terrain, ses verbatims et ses constats chiffrés ont été mis un par ligne, thèmes retirés, ordre mélangé (graine fixe), avec seulement la question posée entre crochets et un identifiant `N001`…`N113`. Le matériau, sa source, sa fabrication et les sorties complètes restent hors du dépôt public, dans les notes partagées des sessions (`derive-materiau/`) ; ce document n'en donne que des comptes.

Conséquences du biais, à garder en tête pour lire le verdict :

- le regroupement par thème est fait d'avance, mais pas le regroupement **par comportement d'usager**, qui est celui que demandent les personas : il restait un vrai choix à faire ;
- les notes sont anonymes, sans participant : les comptes sont ceux des constats et des notes, pas des personnes ;
- un seul cas, deux passages par variante, un seul modèle pour l'étape jugée (Sonnet).

## Déroulé

1. Recette personnelle [`recette-derive-personas.md`](recette-derive-personas.md), jouée par l'exécuteur tel quel (`new`, `next`, `validate`).
2. **Premier essai de l'étape 1** : 10 groupes. Avec une mission « une persona par groupe » et le plafond de 4 personas (la demande, le skill), l'étape persona aurait été forcée de fusionner, donc de regrouper : le test aurait jugé la recette, pas le corpus. Étape 1 rejouée avec « 4 groupes au plus » dans sa mission : 4 groupes (17, 30, 42 et 20 notes) et 4 notes non placées. C'est ce regroupement qui a été validé et figé.
3. Étape persona : le message construit par l'exécuteur (moteur `fake`), rejoué par [`rejouer.py`](rejouer.py) en quatre appels : deux **sans corpus** (le message tel quel), deux **avec corpus** (`corpus/notes.md` copié, l'annonce et la section `sources_read` ajoutées, comme au §5).
4. Contrôles mécaniques par [`controle.py`](controle.py) et des recherches dans les sorties : identifiants cités hors de leur groupe, citations cherchées dans les notes, lectures du flux `stream-json`.

## La grille remplie

| Critère | Sans corpus, 1 | Sans corpus, 2 | Avec corpus, 1 | Avec corpus, 2 |
|---|---|---|---|---|
| G1 Groupes repris | 1 : 4 personas, un par groupe, notes non placées laissées à part | 1 : idem, « sans regroupement nouveau » | 1 : idem | 1 : idem |
| G2 Comptes | 1 | 1 | 1 | 1 |
| G3 Motifs | 1 : rien hors des notes du groupe | 1 | 1 : trois notes d'un autre groupe citées en contraste, attribuées à leur persona | 1 : quatre notes citées en contraste, idem ; une note non placée utilisée et signalée comme telle |
| G4 Écart signalé | sans objet (aucun écart) | sans objet | sans objet | sans objet |
| G5 Citations | 0 : 4 « citations » inventées, signalées « paraphrase (pas un verbatim) » | sans objet : aucune citation, « à récupérer dans le corpus » | 0 : 11 verbatims exacts distincts, avec leur identifiant, mais 4 formules inventées entre guillemets dans les titres, et une citation retouchée (un adjectif accordé au nom qui précède) | 1 : 19 verbatims exacts avec leur identifiant ; la même citation retouchée |
| G6 Lectures | sans objet | sans objet | 1 : un `Read` du fichier entier ; déclaré « lu en entier (lignes 1 à 118) » | 1 : idem |
| G7 Mission | 1 | 1 | 1 | 1 |

Comptes mécaniques : identifiants cités par sortie, 100, 98, 101 et 105 ; dans chaque persona, les identifiants qui ne sont pas de son groupe sont les 4 notes non placées et, avec corpus seulement, des notes citées en contraste, pour dire qu'un autre persona ne partage pas tel besoin, jamais rattachées au persona.

## Verdict

**Avec le corpus, l'étape persona reste dans sa mission** : dans les deux passages, mêmes groupes, mêmes comptes, aucun motif nouveau, alors que le skill dit lui-même de former les groupes et que les 113 notes étaient sous la main. Elle s'est servie du corpus pour ce que la mission demandait : relire les notes derrière les identifiants et en citer les mots exacts.

Ce que le corpus a changé :

- **les verbatims** : sans corpus, l'étape n'a pas de citations ; un passage en invente (signalées comme paraphrases), l'autre n'en met aucune et renvoie au corpus. Avec corpus, 11 et 19 verbatims exacts distincts, chacun avec son identifiant. C'est le besoin du §6 (« persona cite les verbatims »), constaté sur un cas réel ;
- **le coût** : +45 % (0,125 $ au lieu de 0,087 $), parce que l'étape lit le fichier entier (10 500 caractères) même pour citer quelques lignes. « Consulté à la demande » veut dire ici « lu en entier » : à mesurer sur un corpus plus gros ;
- **la trace** : la section `sources_read` dit exactement ce que montre le flux (un `Read`, le fichier entier).

Ce qui reste fragile, avec ou sans corpus : des formules inventées mises entre guillemets (titres de personas, paraphrases). Une consigne et un contrôle mécanique (chaque passage entre guillemets cherché dans le corpus, comme le contrôle de fuite à l'envers) le traiteraient.

## Ce que le test ne dit pas

- La mission jouée interdit le regroupement en toutes lettres (« Do not regroup the participants: the groups are decided »). Une mission plus vague, comme en écrirait un auteur de recette pressé, n'a pas été jouée : c'est là que le risque de dérive serait le plus fort.
- Un corpus gros (plusieurs pièces, des centaines de lignes), où lire en entier n'est plus possible, n'a pas été joué.
- Le matériau était pré-structuré (voir le biais) ; des notes brutes, plus désordonnées, pourraient tenter davantage l'étape.
