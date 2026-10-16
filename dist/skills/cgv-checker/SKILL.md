---
name: cgv-checker
description: "Merged into contrat-fournisseur \u2014 use contrat-fournisseur. Kept the triggers \"are these ToS balanced\", \"review these terms from the seller's side before we publish\", \"any unfair clauses in these terms of service\", \"check these ToS before we publish them\", \"what should we renegotiate in this supplier's GTC\" (reading GTC / ToS under French law from the client, supplier or user position) \u2014 these requests are now handled with `contrat-fournisseur`, reading position and document type \"GTC / ToS\"."
---
# Merged into `contrat-fournisseur`

This skill no longer carries its own method. Follow `contrat-fournisseur` with the reading position the user gave (`client`, `fournisseur` or `utilisateur`, default `client`) and the document type `cgv_cgu` ("CGV / CGU"); for SaaS or cloud conditions, the type `saas_cloud`.

Why: reading standard terms and reading a negotiated contract are the same gesture (liability, term, price, data, ranked points with a wording and a fallback) over a shared body of knowledge. Keeping two skills made the clause sets drift apart, and the terms-only grid missed what the contract skill knew (Data Act, art. 28 GDPR on SaaS conditions). The standard-terms clause set (qualification of the parties, black and grey lists, withdrawal, B2B payment) is now `references/clauses_cgv.md` in `contrat-fournisseur`.

This redirect stays for one version so requests that name `cgv-checker` still arrive. Do not analyse the document from this page.
