# Décision : la notion de corpus dans les recettes

Document de décision du 2026-10-16. Amiel a tranché les questions (§3, §7) ; **pas de code avant les vérifications du §8**. Il remplace l'approche du commit `a27a922` (format 3 : `items` et `mode`), retiré le même jour (gardé sur la branche locale `sauvegarde-format3-a27a922`) ; seule la vérification de calcul en a été conservée.

## 1. Le problème

Aujourd'hui le moteur ne connaît qu'une entrée, « la demande brute » (`input.md`), réservée à l'étape 1 et protégée par le contrôle de fuite. Or ce texte mélange deux choses :

- **la demande** : ce que l'utilisateur veut obtenir (« fais-moi les personas », « réponds à cet appel d'offres ») ;
- **le matériau** : ce sur quoi on travaille (verbatims, tableau budget / réel, contrat, cahier des charges, offres reçues).

La règle d'isolation vient d'ix-memory : les étapes aval qui relisaient le brief le réinterprétaient et refaisaient tout. Ce danger vient de la demande. En protégeant les deux ensemble, on prive les étapes aval du matériau dont elles ont besoin : c'est la cause commune des besoins relevés par la revue des skills métier (§1.1) — vérifier une absence dans un contrat, vérifier des chiffres contre un tableau, donner le détail d'un besoin à une étape 2, citer des verbatims sans les réécrire.

## 2. La notion de corpus

| | La demande | Le corpus |
|---|---|---|
| Ce que c'est | ce qu'on veut obtenir | les pièces sur lesquelles on travaille |
| Qui la sépare | l'humain, à la création du dossier (la demande tapée, les pièces jointes) | idem |
| Qui la voit | l'étape 1, et une étape qui vérifie et déclare `reads_source` (déjà sur main) | l'étape 1, et les étapes que la recette autorise, nommément |
| Comment | dans le message | **consulté** : les pièces sont copiées dans le dossier jetable de l'étape, qui lit ce dont elle a besoin |
| Protection | contrôle de fuite | aucune : c'est du matériau ; ce que l'étape produit reste contrôlé contre la demande |

Sans pièces séparées (tout collé d'un bloc), rien ne change : tout est « demande », protégée comme aujourd'hui.

## 3. Décisions d'Amiel (2026-10-16)

1. **Le corpus est lu à la demande**, pas poussé dans le message. Trace de lecture : **déclarative toujours** (c'est la base : l'étape dit ce qu'elle a lu et ce qu'elle n'a pas ouvert), **mécanique en plus quand le moteur le permet**.
2. **Une étape qui produit peut consulter le corpus**, mais seulement si la recette l'autorise sur cette étape. **C'est l'exécuteur qui donne le droit** : il copie les pièces dans le dossier de l'étape, ou non.
3. **`verbatim` est gardé** tel quel : il reste utile sans corpus séparé, pour une sélection validée à l'étape 1, et en conversation, où il n'y a pas de dossier.

## 4. Ce que les tests ont montré (2026-10-16)

Dossier jetable contenant une référence et une pièce ; à côté, un faux dossier de parcours avec sa demande.

| Moteur | Lit son dossier | Lit hors de son dossier | Trace mécanique |
|---|---|---|---|
| Claude (`claude -p --tools Read`, options de l'exécuteur) | oui | **non** : refusé par Claude, en chemin absolu comme en `../` ; le refus remonte dans `permission_denials` | **oui** en `--output-format stream-json --verbose` : chaque `Read` avec son chemin et son résultat. Le format `json` actuel ne donne que les refus |
| Codex, avant (`-s read-only`, testé par `codex sandbox`, sans appel au modèle) | oui | **oui** : son bac à sable interdit d'écrire, pas de lire ; il lit la demande d'un dossier, et tout le disque | — |
| Codex, depuis le plugin 2.13.0 (profil de permission `ixetape`, [exécuteur](executeur.md) §4 ; vrai appel `codex exec`, codex-cli 0.155.1) | oui | **non**, sauf `/tmp`, `/var/tmp` et des fichiers système : la demande à côté du dossier, celle d'un dossier de parcours et `~/.zshrc` sont refusées | **partielle** : `--json` donne les commandes lancées et leur sortie, pas les fichiers lus ; une commande refusée par le bac à sable n'y figure pas |
| Antigravity, Vibe | — | non testé | non testé : trace déclarative seule |

Conséquence pour Claude : « une étape ne voit que ce que l'exécuteur lui copie » est vrai, le droit se donne en copiant ou non. Conséquence pour Codex : **c'était un trou dans l'isolation**, corpus ou pas ; une étape Codex qui cherchait `input.md` sur le disque le trouvait. Refermé par le plugin 2.13.0 : un profil de permission limite ses lectures au dossier de l'étape, vérifié avant chaque appel ; le droit se donne alors en copiant ou non, comme pour Claude. Reste lisible `/tmp` (rien du parcours n'y est).

## 5. Ce que ça changerait (proposition)

- **Création du dossier** : la demande d'un côté, des pièces de l'autre (page : une zone « votre demande », une zone « vos pièces » ; ligne de commande : `new --input demande.md --corpus piece1.md piece2.xlsx`). Les pièces vont dans `./parcours/<slug>/corpus/`.
- **Recette** : une étape déclare `receives: [corpus]` pour consulter les pièces. Une nouvelle source dans `receives` : un exécuteur plus ancien ne saurait pas la jouer, donc **format 3** (le critère du §2bis de `format-recette.md`).
- **Exécuteur** : copie `corpus/` dans le dossier jetable des seules étapes autorisées ; annonce les pièces dans le message (comme les `references/`) ; demande une section `### sources_read` (lues / non ouvertes) ; avec Claude, passe en `stream-json` et enregistre les lectures réelles, signale les écarts avec la déclaration.
- **Citer** : Claude lit les fichiers avec leurs numéros de ligne ; une étape cite `entretiens.md:12`. Le regroupement donne des références, l'étape persona relit les lignes. Le handoff par identifiants du commit `a27a922` devient inutile.
- **`reads_source`** reste : il donne la **demande** à une étape qui vérifie (contrôler ce qui a été demandé, les mots du demandeur). Le corpus donne les **pièces**. Deux choses différentes.

## 6. Ce que ça règle

| Besoin | Avec le corpus |
|---|---|
| `persona` cite les verbatims | l'étape consulte le corpus et cite par fichier et ligne — **réglé** |
| vérifier des chiffres (`budget-variance-analysis`, `calc-check`) | la vérification consulte le tableau — **réglé** |
| vérifier une absence (`cgv-checker`, `contrat-fournisseur`) | la vérification relit tout le contrat — **réglé** |
| `rfp-draft`, `offer-comparison` ont besoin du détail | étapes qui produisent, autorisées nommément — **réglé, risque de dérive le plus fort** |
| `people-review` : ne rien inventer sur une personne | une vérification consulte les notes — **réglé** |
| `brief-client` (le mail est demande et matériau) | pas de pièces séparées : comme aujourd'hui |

Hors du sujet : les deux phases d'un même skill (décision 2) n'ont pas besoin du corpus ni d'un format ; assouplir la règle de `concepteur-recette` et dire le mode dans la mission suffit probablement.

## 7. Décidé le 2026-10-16

1. **Codex lit tout le disque** : on l'accepte et on le dit dans la page, au moment de choisir Codex comme moteur. En parallèle, une session cherche un réglage qui limite ses lectures au dossier de l'étape (note attendue : `codex-lecture.md` dans les notes partagées). **Suite (plugin 2.13.0)** : le réglage existe (profils de permission de Codex) et l'exécuteur l'utilise ; la page dit désormais, au choix de Codex, ce qui reste lisible (`/tmp`, `/var/tmp`, fichiers système).
2. **La page attendra** : le corpus arrive d'abord en ligne de commande (`new --input demande.md --corpus pièces…`), pour le tester sur un cas réel ; les deux zones « votre demande » et « vos pièces » viendront dans la page ensuite, si le test de dérive (§8) passe.

## 8. À vérifier avant de coder

- **La dérive** : sur un cas réel (notes de terrain → regroupement → personas), jouer l'étape persona avec et sans le corpus, et regarder si elle reste dans sa mission ou refait le regroupement. Quelques appels Sonnet, comme la preuve de `reads_source`.
- **Codex** : ~~lire ses évènements `--json` ; chercher un réglage qui restreint ses lectures~~ — fait (plugin 2.13.0, [exécuteur](executeur.md) §4) : le profil `ixetape` limite les lectures au dossier de l'étape ; `--json` est gardé comme trace, partielle (commandes lancées, pas les refus). Reste ouvert : `/tmp` lisible, profils en bêta (vérifiés avant chaque appel), sous-agents de Codex non testés.
- **Antigravity, Vibe** : lecture hors du dossier.
- **Les pièces non textuelles** (xlsx, pdf) : Claude lit les PDF ; un tableur demande une conversion à la création du dossier.
