# Essai pdf-25-pages

Pièces : annexe-25-pages.pdf  
Code de sortie : 0 ; coût : 0.1476 $

## Consigne

Le dossier courant contient la ou les pièces d'un dossier : annexe-25-pages.pdf. Lis-les avec l'outil Read. Si une lecture échoue, dis exactement ce que l'outil a répondu et n'invente rien. Quel est le délai de garantie des ouvrages, et à quelle page figure-t-il ? Dis combien de lectures il t'a fallu et ce que l'outil a répondu à chacune.

## Lectures (flux stream-json)

- `Read {"file_path": "/private/var/folders/fz/l9h9d2bx1kq0j9mt0fv9plfr0000gn/T/corpus-essai-e2o57c0o/annexe-25-pages.pdf", "pages": "1-20"}` → ok : 'PDF pages extracted: 20 page(s) from /private/var/folders/fz/l9h9d2bx1kq0j9mt0fv9plfr0000gn/T/corpus-essai-e2o57c0o/annexe-25-pages.pdf (10.1KB) [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image] [image]'
- `Read {"file_path": "/private/var/folders/fz/l9h9d2bx1kq0j9mt0fv9plfr0000gn/T/corpus-essai-e2o57c0o/annexe-25-pages.pdf", "pages": "21-25"}` → ok : 'PDF pages extracted: 5 page(s) from /private/var/folders/fz/l9h9d2bx1kq0j9mt0fv9plfr0000gn/T/corpus-essai-e2o57c0o/annexe-25-pages.pdf (10.1KB) [image] [image] [image] [image] [image]'

## Réponse

**Réponse :** le délai de garantie des ouvrages est de **36 mois à compter de la réception**. Il figure à la **page 23** (« Annexe technique - section 23 »). C'est la seule page qui contient cette phrase. Les 24 autres ne contiennent que le texte standard sur les tolérances d'usinage et d'humidité du bois.

**Lectures : 2.** Le PDF fait 25 pages et l'outil accepte au maximum 20 pages par requête, donc je l'ai lu en deux tranches.

1. Pages 1 à 20 : l'outil a répondu « PDF pages extracted: 20 page(s) from …/annexe-25-pages.pdf (10.1KB) » et m'a renvoyé les 20 pages sous forme d'images.
2. Pages 21 à 25 : l'outil a répondu « PDF pages extracted: 5 page(s) from …/annexe-25-pages.pdf (10.1KB) » et m'a renvoyé les 5 pages sous forme d'images.

Aucune des deux lectures n'a échoué.
