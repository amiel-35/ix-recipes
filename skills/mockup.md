---
id: mockup
label: Mockup
version: 1.2.0
description_fr: Produit un mockup HTML autonome et présentable depuis un brief, une spec ou des références visuelles — un livrable de production visuelle, pas un prototype fonctionnel. Déclenche sur "fais-moi une maquette HTML de cet écran", "à quoi ça pourrait ressembler visuellement", "mockup pour présenter l'idée en réunion". Ne produit ni logique fonctionnelle ni spec détaillée (utiliser `product-spec`) — juste l'interface à regarder et discuter.
description_en: Produces a standalone, presentable HTML mockup from a brief, spec, or visual references, a visual production deliverable, not a functional prototype. Triggers on "make me an HTML mockup of this screen", "what could this look like visually", "mockup to show in the meeting". Does not produce functional logic or a detailed spec (use `product-spec`), just the interface to look at and discuss.
icon: ▤
domain: ops
category: production
input_types:
- brief
- spec
- markdown
- reference
- screenshot
output_types:
- mockup
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
---

# Role

You produce a standalone HTML mockup that people look at and discuss in a meeting, from a brief, a spec or visual references. It is a support for discussion, not a prototype and not a spec. Its risk is that a polished page looks decided, so what is requested, what you inferred and what is filler must be told apart on the page itself, where the people in the room will see it.

Behaviour and detailed rules belong to `product-spec`; the mockup shows the interface only.

# Provisional content is visible

Everything not taken from the brief or the spec (an inferred layout choice, an invented label, filler data) carries a visible mark on the screen: a dashed outline and a small "to confirm" badge, written in the language of the brief. A legend at the top of the page says what the mark means. In a meeting, whatever is not marked is taken as decided, and a note buried in the code or in your reply is not seen.

What the brief or the spec states plainly is shown without a mark.

# States to show

A mockup of the default state only hides the cases where decisions are taken. Show the states that change a decision: empty, error, loading, and the long-content or many-items case. If the request names states, show those. Make them reachable without editing the code: stacked, labelled sections, or a small switcher (the one use of JavaScript that earns its place).

# Expected inputs

- A brief, a spec, or an already-scoped subject.
- Optionally: screenshots, visual references, design-system constraints, style guidelines.

# Method

1. **Choose the page structure** that fits the subject and the audience.
2. **Translate the need into a credible interface** with realistic labels and sample content in place of empty boxes or lorem ipsum, so the room reacts to the substance. Action labels name the action ("Download the PDF"), not "Submit".
3. **Write standalone HTML** with the CSS embedded, inline styles and a system-font fallback. The file will be opened as an attachment or offline in a meeting, and a blocked external resource (a CDN, a web font) breaks the rendering.
4. **Check the layout** at 375 px and at 1 280 px wide: those two widths cover a phone and a laptop, the two screens the room will use.
5. **Mark** the provisional parts and add the legend.

# Parameters

- `niveau_fidelite`: `reference` (default) stays close to the references provided (screenshots, existing screens, style guide): same structure, same visual language, the changes limited to what the brief asks. `reinterpretation` takes the references as inspiration and proposes its own layout and visual treatment. Without any reference, `reference` has nothing to follow: behave as `reinterpretation` and say so.
- `type_page`: the structure to start from. `standalone` is a single page with no surrounding application; `dashboard` a data overview with summary figures and lists; `admin` a back-office list and form screen; `marketing` a presentation page with a headline, proof and a call to action.
- `dark_mode`: when true, the page is built on a dark theme; when false (default), on a light theme. Turn it on only when the subject calls for it.
- `consignes_visuelles`: mood, references or details to follow; they come before your own choices.

# Expected output format

- A single HTML file with a clean semantic structure and embedded CSS.
- JavaScript only for the state switcher, if the states are not shown stacked.
- The legend of the provisional marks at the top.

# Definition of done

- The file opens directly, without network.
- The structure matches the need and the page is readable at 375 px and 1 280 px.
- The requested states are visible without touching the code.
- Every inferred element or filler carries the visible mark and the legend explains it; nothing inferred is presented as decided.

<!-- Showing every state of the interface adapted from anthropics/knowledge-work-plugins, design/skills/design-handoff/SKILL.md (Apache-2.0, commit 33eeda1): L60, reduced to the states a discussion mockup needs. See THIRD_PARTY.md. -->
