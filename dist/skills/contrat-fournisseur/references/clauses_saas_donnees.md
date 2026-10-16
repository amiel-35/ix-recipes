# Clause set: SaaS, cloud and hosting conditions (data, exit, processors)

Read this file when the service is software as a service, cloud or hosting, whether the conditions are standard terms or a negotiated contract (French and EU law, checked 2026-10-16). Used by `contrat-fournisseur` for `type_document` = `saas_cloud`. These are the points a clause-by-clause grid on general terms most often misses: read them even when the document never mentions data.

## Switching and exit (Data Act)

| Point | What the text imposes | Source |
|---|---|---|
| Cloud / SaaS exit | The written contract states: a notice to start switching ≤ 2 months; a transition period ≤ 30 days with assistance and continuity; the exhaustive list of exportable data; a data-retrieval period ≥ 30 days, then erasure. Applicable since 12 Sept 2025 (art. 50). | Reg. (EU) 2023/2854 (Data Act), art. 25, 50 |
| Switching fees | Until 12 Jan 2027, only fees reduced to the supplier's direct cost; from 12 Jan 2027, none. Early-termination penalties must be disclosed before signing. | Data Act, art. 29 |
| Data Act exceptions | Custom-built services not sold at scale from the supplier's catalogue escape the fee rules (art. 29) and some other switching obligations; trial versions escape the whole chapter. The supplier must say so before signing. | Data Act, art. 31 |
| Connected products | Data-access design for connected products placed on the market after 12 Sept 2026. | Data Act |

Read the exit clause against these: a notice period longer than 2 months, exit fees after 12 Jan 2027, no export list or no retrieval period are findings (read as the customer) or exposures (read as the supplier). Do not raise them for a custom-built service or a trial without saying which exception you assume.

## Personal data: the processor contract (GDPR art. 28)

If the supplier processes personal data for the customer, it is a processor and a written contract is required (art. 28(3), (9)). It sets out the subject-matter, duration, nature and purpose of the processing, the types of data and categories of data subjects, and carries these clauses: processing on documented instructions only, including for transfers; confidentiality of staff; art. 32 security measures; sub-processors only with the controller's prior written authorisation, specific or general (under a general one the controller is told of every change and may object, art. 28(2)) and with the same obligations passed down (art. 28(4)); help with data-subject rights and with arts. 32 to 36; deletion or return at the end unless law requires retention; information and audits; immediate warning when an instruction seems unlawful. For the whole GDPR checklist, refer to `conformite-rgpd` instead of redoing it.

Check also:
- **Roles.** A supplier that decides the purposes and means of a processing (its own analytics, model training on customer data) becomes a controller for it (art. 28(10)): the standard terms must say so and the customer needs a legal basis for the disclosure.
- **Transfers outside the EEA** (arts. 44-49): name every non-EEA recipient, including sub-processors and support teams. For the United States, adequacy covers only recipients certified under the EU-US Data Privacy Framework: check each certification and that the decision is still in force on the date of analysis. Otherwise standard contractual clauses and a transfer impact assessment.
- **Breach notice.** The processor alerts the controller without undue delay (art. 33(2)): a contractual delay of days or weeks leaves the customer unable to meet its 72 hours.
- **Health data.** Data collected in prevention, diagnosis, care or medico-social follow-up and hosted for others need a certified host (art. L. 1111-8 CSP; whether it applies is to confirm).

## Other points to read in the conditions

- **Liability and service levels**: the cap, the availability target in hours per month, credits as the sole remedy (see `clauses_contrat_fournisseur` for the thresholds; between businesses, `clauses_cgv` for the L442-1 test and the default positions).
- **Unilateral changes** to the service, the price or the terms, and the notice given; suspension of the account without notice.
- **Customer content and licence**: who owns the data and outputs, what licence the supplier takes over the content.
- **Security and audit**: certifications claimed, the customer's audit rights, incident reporting.

Cite an article only if it is in this table or you are certain of it; otherwise state the rule without a number and mark it "to check".

## Keep the grid open

This is a list to focus attention, not the limit of the review. After it, check what the service's subject calls for beyond it: sector rules (health, finance, public bodies), AI features and the use of customer data to train models, the specific product. What a list does not name gets missed.
