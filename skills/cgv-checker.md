---
id: cgv-checker
label: Analyse CGV / CGU
version: 2.0.0
description_fr: Fusionné dans contrat-fournisseur — utiliser contrat-fournisseur. Gardait les déclencheurs "ces CGU sont-elles équilibrées", "relis ces CGV côté vendeur avant publication", "y a-t-il des clauses abusives dans ces conditions générales", "check ces CGU avant publication", "quels points négocier sur ces CGV fournisseur" (lecture des CGV / CGU en droit français selon la position client, fournisseur ou utilisateur) — ces demandes se traitent désormais avec `contrat-fournisseur`, position et type de document « CGV / CGU ».
description_en: Merged into contrat-fournisseur — use contrat-fournisseur. Kept the triggers "are these ToS balanced", "review these terms from the seller's side before we publish", "any unfair clauses in these terms of service", "check these ToS before we publish them", "what should we renegotiate in this supplier's GTC" (reading GTC / ToS under French law from the client, supplier or user position) — these requests are now handled with `contrat-fournisseur`, reading position and document type "GTC / ToS".
icon: ⊞
domain: legal
category: critique
input_types:
- markdown
- reference
- brief
output_types:
- analyse_cgv_cgu
- points_negociation
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Merged into `contrat-fournisseur`

This skill no longer carries its own method. Follow `contrat-fournisseur` with the reading position the user gave (`client`, `fournisseur` or `utilisateur`, default `client`) and the document type `cgv_cgu` ("CGV / CGU"); for SaaS or cloud conditions, the type `saas_cloud`.

Why: reading standard terms and reading a negotiated contract are the same gesture (liability, term, price, data, ranked points with a wording and a fallback) over a shared body of knowledge. Keeping two skills made the clause sets drift apart, and the terms-only grid missed what the contract skill knew (Data Act, art. 28 GDPR on SaaS conditions). The standard-terms clause set (qualification of the parties, black and grey lists, withdrawal, B2B payment) is now `references/clauses_cgv.md` in `contrat-fournisseur`.

This redirect stays for one version so requests that name `cgv-checker` still arrive. Do not analyse the document from this page.
