#!/bin/bash
# Prépare le dossier `dist/skills` d'ix-skills que lit l'exécuteur (IX_SKILLS_PATH) pour jouer l'amont d'un sujet.
#
# Les trois skills de l'amont qui ne sont pas encore dans `main` d'ix-skills se lisent sur leur branche, sans extraction
# dans le dépôt : `git archive` d'une référence, vers un dossier à vous. Rien n'est écrit dans ix-skills.
#
#   harnais/preparer-skills.sh DOSSIER            puis   export IX_SKILLS_PATH=DOSSIER/dist/skills
#
# Variables : IXS (le dépôt ix-skills, défaut ~/Projets/ix-skills) ; IX_SKILLS_REFS (les références, défaut ci-dessous :
# `cadrage` en mode close et `goal-writing` sur 645a599, `criteres-reussite` sur sa branche). Une fois ces branches
# fusionnées dans ix-skills, ce script ne sert plus : IX_SKILLS_PATH peut désigner `dist/skills` d'ix-skills lui-même.
set -eu
cible=${1:?usage : preparer-skills.sh DOSSIER}
ixs=${IXS:-$HOME/Projets/ix-skills}
refs=${IX_SKILLS_REFS:-"645a599 claude/skill-cahier-de-recette-30edc2"}
mkdir -p "$cible"
[ -z "$(ls -A "$cible")" ] || { echo "$cible n'est pas vide : choisissez un dossier neuf" >&2; exit 1; }
premiere=1
for ref in $refs; do
  if [ $premiere = 1 ]; then
    git -C "$ixs" archive "$ref" dist/skills skills | tar -x -C "$cible"
    premiere=0
  else   # les références suivantes ne complètent que ce qui manque (un skill d'une autre branche)
    tmp=$(mktemp -d)
    git -C "$ixs" archive "$ref" dist/skills | tar -x -C "$tmp"
    for d in "$tmp"/dist/skills/*/; do
      d=${d%/}
      [ -d "$cible/dist/skills/$(basename "$d")" ] || cp -R "$d" "$cible/dist/skills/"
    done
    rm -rf "$tmp"
  fi
done
echo "Prêt : export IX_SKILLS_PATH=$cible/dist/skills"
