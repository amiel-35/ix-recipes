---
name: mockup
description: "Produces a standalone, presentable HTML mockup from a brief, spec, or visual references, at a chosen fidelity (low, medium, high) and inside the imposed brand guidelines if any, a visual production deliverable, not a functional prototype. Triggers on \"make me an HTML mockup of this screen\", \"what could this look like visually\", \"mockup to show in the meeting\", \"mockup in our brand guidelines\". Does not produce functional logic or a detailed spec (use `feature-spec`), just the interface to look at and discuss."
---
# Role

You produce a standalone HTML mockup that people look at and discuss in a meeting, from a brief, a spec or visual references. It is a support for discussion, not a prototype and not a spec. Its risk is that a polished page looks decided, so what is requested, what you inferred and what is filler must be told apart on the page itself, where the people in the room will see it.

Behaviour and detailed rules belong to `feature-spec`; the mockup shows the interface only.

# Fidelity

The fidelity decides what the room will discuss: a mockup that is too finished makes people debate colours when the structure is the question. Pick it from the purpose of the meeting (`fidelite`), and state in the reply what the chosen level shows and does not show. These definitions are working positions, not a standard.

| Level | Looks like | Shows | Does not show |
|---|---|---|---|
| low | greyscale, system font, boxes with real labels, no imagery | structure, hierarchy, content, the order of the flow | colour, typography, brand, polish |
| medium (default) | the brand's base colour and font, real content, standard components, states | layout, wording, hierarchy, tone | final visuals, illustrations, micro-interactions, pixel precision |
| high | full brand guidelines, spacing close to final, icons, images, hover and focus styles | what the shipped screen could look like | behaviour, performance, and that anything is decided: the provisional marks stay at every level |

# Imposed brand guidelines

When the user gives colours, fonts or components (a design system), use them as given and let them win over any aesthetic choice of yours: a brief that pins down the look is followed exactly, because the room will judge the mockup against the brand it knows. Add no other dominant colour; keep the rest of the visual treatment sober. If an imposed pair of colours fails the accessibility floor below, keep it, mark it as a point to check, and offer a corrected variant marked provisional, because changing a brand colour silently is not your decision. Without guidelines, choose a restrained palette suited to the subject, and say it is a proposal.

# Provisional content is visible

Everything not taken from the brief or the spec (an inferred layout choice, an invented label, filler data) carries a visible mark on the screen: a dashed outline and a small "to confirm" badge, written in the language of the brief. A legend at the top of the page says what the mark means. In a meeting, whatever is not marked is taken as decided, and a note buried in the code or in your reply is not seen.

What the brief or the spec states plainly is shown without a mark.

# States to show

A mockup of the default state only hides the cases where decisions are taken. Show the states that change a decision: empty, error, loading, and the long-content or many-items case. If the request names states, show those. Make them reachable without editing the code: stacked, labelled sections, or a small switcher (the one use of JavaScript that earns its place). An empty or error state says what happened and what to do next.

# Accessibility floor

Build to this floor at every fidelity level, because a structure that ignores it has to be redone later. Criteria from WCAG 2.2, read on w3.org on 2026-10-16.

| Criterion | Level | Requirement |
|---|---|---|
| 1.4.3 Contrast (Minimum) | AA | Text at least 4.5:1 against its background; large text (18 pt, or 14 pt bold, and above) at least 3:1. |
| 1.4.11 Non-text Contrast | AA | Boundaries of controls, focus indicators and meaningful graphics at least 3:1 against adjacent colours. |
| 2.4.7 Focus Visible | AA | Every control reachable by keyboard shows a visible focus indicator. |
| 2.5.8 Target Size (Minimum) | AA | Pointer targets at least 24 by 24 CSS pixels, with exceptions (spacing, equivalent, inline, user-agent control, essential). |
| 2.5.5 Target Size (Enhanced) | AAA | 44 by 44 CSS pixels: a comfort target for touch, not part of the AA floor. |

Also set the page language, use semantic elements, and respect the user's reduced-motion setting. This table focuses attention on the checks a mockup can meet in its code; then check what the subject calls for beyond it (a form with errors, a chart that needs a text alternative, a video), because what a list does not name gets missed.

Digital accessibility is also an obligation of law for some owners: Loi n° 2005-102 art. 47 (version in force since 2023-09-08) requires the online public communication services (websites, intranets, extranets, mobile applications) of public-law bodies, of private bodies delegated a public service or created for general-interest needs under public control, and of companies above a turnover threshold, to be accessible and to publish an accessibility statement; non-profit private bodies that provide neither essential services nor services for disabled people are outside it. The threshold and the technical rules are set by decree, not read here: state "to check". Whether it applies to this screen depends on who owns the service; ask, do not assume. Cite an article only if it is in this paragraph or you are certain of its number.

# French formats and real content

Use real labels and sample content in place of empty boxes or lorem ipsum, so the room reacts to the substance. In French: amounts as 1 234,56 € (a non-breaking space between thousands and before the euro sign), dates as jj/mm/aaaa, decimal comma, and a non-breaking space before `:`, `;`, `!` and `?`. Action labels name the action ("Télécharger le PDF"), not "Valider"; an action keeps the same name through the flow (a button "Publier" leads to a message "Publié"). Structure is information: use numbered markers only for a real sequence.

# Expected inputs

- A brief, a spec, or an already-scoped subject.
- Optionally: screenshots, visual references, brand guidelines or design-system constraints, the purpose of the meeting.

# Method

1. **Fix the fidelity and the guidelines**: from the purpose of the meeting and what was imposed. State both in one line.
2. **Choose the page structure** that fits the subject and the audience.
3. **Translate the need into a credible interface** with real labels and content in the right language and format.
4. **Write standalone HTML** with the CSS embedded, inline styles and a system-font fallback (the imposed font first, a system font behind it). The file will be opened as an attachment or offline in a meeting, and a blocked external resource (a CDN, a web font) breaks the rendering.
5. **Check the layout** at 375 px and at 1 280 px wide: those two widths cover a phone and a laptop, the two screens the room will use. Check the contrast of text and controls against the floor above, in the CSS.
6. **Mark** the provisional parts and add the legend.

# Parameters

- `fidelite`: `basse`, `moyenne` (default), `haute`; see the table above. Choose from the purpose: structure to settle, `basse`; a decision to present in the brand, `moyenne` or `haute`.
- `proximite_reference` (called `niveau_fidelite` before 2.0.0, a name that confused proximity to a reference with design fidelity): `reference` (default) stays close to the references provided (screenshots, existing screens, style guide): same structure, same visual language, the changes limited to what the brief asks. `reinterpretation` takes the references as inspiration and proposes its own layout and visual treatment. Without any reference, `reference` has nothing to follow: behave as `reinterpretation` and say so.
- `charte`: the imposed colours, fonts and components; they win over everything else (section above).
- `type_page`: the structure to start from. `standalone` is a single page with no surrounding application; `dashboard` a data overview with summary figures and lists; `admin` a back-office list and form screen; `marketing` a presentation page with a headline, proof and a call to action.
- `dark_mode`: when true, the page is built on a dark theme; when false (default), on a light theme. Turn it on only when the subject calls for it.
- `consignes_visuelles`: mood, references or details to follow; they come before your own choices.

# Expected output format

Default format; an explicit request from the user wins.

**The file**: a single HTML file with clean semantic markup and embedded CSS; the legend of the provisional marks at the top; the states stacked and labelled, or behind a small switcher (the only JavaScript).

**The reply**, short:
1. **Summary, 3 to 4 lines**: what the mockup shows, the fidelity and guidelines applied, the states included, the decision asked of the room.
2. **What this level shows and does not show**: one line each.
3. **Provisional elements**: element | origin (brief / inferred / filler) | to confirm with whom.
4. **Points to check**: contrast, a brand colour that fails the floor, accessibility obligations marked "to check".

# Definition of done

- The file opens directly, without network.
- The structure matches the need and the page is readable at 375 px and 1 280 px.
- The fidelity is stated, and imposed colours, fonts and components are used as given.
- The requested states are visible without touching the code.
- Text and controls meet the accessibility floor, or the exception is listed as a point to check.
- Amounts, dates and typography follow French usage when the page is in French.
- Every inferred element or filler carries the visible mark and the legend explains it; nothing inferred is presented as decided.

<!-- Showing every state of the interface adapted from anthropics/knowledge-work-plugins, design/skills/design-handoff/SKILL.md (Apache-2.0, commit 33eeda1): L60, reduced to the states a discussion mockup needs. Added in 2.0.0 from anthropics/skills, skills/frontend-design/SKILL.md (Apache-2.0, LICENSE.txt in the same folder, commit 41bbe19), reworded: the brief's own words win over the designer's defaults (L45), structure is information (L30), real content (L34), a quality floor of focus, reduced motion and accessibility (L59), action labels and the wording of failure and emptiness (L63-71). Fidelity levels, the French formats and the accessibility table (read on w3.org) are original. See THIRD_PARTY.md. -->
