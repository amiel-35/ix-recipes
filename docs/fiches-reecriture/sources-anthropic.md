# Anthropic guidance on writing Skills and prompts — sourced notes

Read on 2026-10-16. All sources fetched live (raw markdown via `curl`, `gh api`), not from memory.
Quotes are verbatim and under 25 words. "Paraphrase" lines are mine.
Raw copies of the pages were kept locally during the session (not versioned).

## 0. Sources

| # | Title | URL (current) | Published / updated | Notes |
|---|---|---|---|---|
| S1 | Skill authoring best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | No date shown on page | MOVED: `docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices` now redirects (HTTP 200 after redirect) to `platform.claude.com/docs/en/...`. Append `.md` to get raw markdown. |
| S2 | Agent Skills (overview) | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | No date shown | Same move. |
| S3 | skill-creator `SKILL.md` (anthropics/skills) | https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator/SKILL.md | Repo `main` HEAD = `dbd4588f9e1033efb41dad4bef2f7947c8993d44` (2026-10-09). The file itself last changed in commit `b0cbd3df1533b396d281a6886d5132f623393a9c` (2026-03-06). `references/schemas.md` last changed `3d59511518591fa82e6cfcf0438d68dd5dad3e76` (2026-02-25). | 485 lines. Ships `agents/{grader,comparator,analyzer}.md`, `references/schemas.md`, `scripts/`, `eval-viewer/`, `assets/`. No separate "writing style" reference file: the style rules are inside SKILL.md. |
| S4 | Prompting best practices (general) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | No date shown | Covers Fable 5.1, Mythos 5.1, Fable 5, Opus 5.5, Opus 5, Opus 4.8, Sonnet 5.5, Sonnet 5, Haiku 5.5 etc. (lists models up to Fable 5.1). |
| S5 | Prompting Claude Fable 5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 | No date shown | Most relevant for "skills too prescriptive". |
| S6 | Prompting Claude Sonnet 5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 | No date shown | Literal instruction following. |
| S7 | Prompting Claude Sonnet 5.5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5 | No date shown | Scope / initiative. |
| S8 | Prompting Claude Opus 5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | No date shown | Literal "be conservative", over-verification. |
| S9 | Prompting Claude Fable 5.1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | No date shown | Example with rationale. |
| S10 | Equipping agents for the real world with Agent Skills (Anthropic Engineering) | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | Published Oct 16, 2025; update line: Agent Skills published as an open standard (Dec 18, 2025) | Short post; principles only. |

Also checked, not needed: Opus 5.5, Haiku 5.5 pages (nothing on emphasis/skills beyond what is below).

---

## a. Conciseness / "Claude is already smart" / token budget / SKILL.md size

**S1 — Core principle**
- "The context window is a public good." / "Default assumption: Claude is already very smart"
- Rule: "Only add context Claude doesn't already have." Challenge each paragraph with three questions: does Claude need this explanation, can I assume it, does it justify its token cost.
- Worked example: 50-token version (just the pdfplumber snippet) = good; 150-token version explaining what a PDF is = bad.
- Nuance: only metadata is preloaded, but "once Claude loads it, every token competes with conversation history and other context."

**S1 — Size limit**
- "Keep SKILL.md body under 500 lines for optimal performance" (appears under Progressive disclosure AND under Token budgets AND in the final checklist).
- When near the limit, split into separate files.

**S2 — Token budget by level** (table)
- Level 1 metadata: "~100 tokens per Skill", always loaded.
- Level 2 SKILL.md body: "Under 5k tokens", loaded when triggered.
- Level 3+ resources: "None until accessed"; scripts run through bash and only their output enters context.

**S3 (skill-creator)**
- "Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy" with clear pointers on where to go next.
- Metadata "~100 words", body "<500 lines ideal"; "These word counts are approximate and you can feel free to go longer if needed."
- "Keep the prompt lean. Remove things that aren't pulling their weight." Read transcripts, not only outputs, to spot parts that make the model waste time.

**S1 — Review step when Claude drafts the skill**
- Suggested prompt: "Remove the explanation about what win rate means - Claude already knows that."

**S10** — no numeric limit; says to split a unwieldy SKILL.md into files, and that mutually exclusive contexts kept in separate paths "reduce the token usage".

**S5 (Fable 5)** — "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality." Advice: review and consider removing older instructions if default performance is better.

---

## b. Degrees of freedom (high / medium / low)

**S1 — "Set appropriate degrees of freedom"**
- "Match the level of specificity to the task's fragility and variability."
- High freedom (text instructions): use when "Multiple approaches are valid", decisions depend on context, heuristics guide. Example: code review steps.
- Medium freedom (pseudocode / script with parameters): "A preferred pattern exists", some variation acceptable.
- Low freedom (exact script, few or no parameters): "Operations are fragile and error-prone", "Consistency is critical", "A specific sequence must be followed". Example: `python scripts/migrate.py --verify --backup` then "Do not modify the command or add additional flags."
- Analogy: narrow bridge with cliffs = exact guardrails; open field = general direction, trust Claude.

**S1 — Template strictness follows the same logic**
- Strict (API responses, data formats): "ALWAYS use this exact template structure".
- Flexible: "Here is a sensible default format, but use your best judgment based on the analysis".

**S4 (general prompting, thinking section)**
- "Prefer general instructions over prescriptive steps." Claude's reasoning "frequently exceeds what a human would prescribe."

**S5 (Fable 5)** — "you can steer most behaviors with a brief instruction rather than enumerating each behavior by name." A two-sentence brevity instruction works as well as listing each unwanted pattern.

**S1 — Test across models**
- Haiku: "Does the Skill provide enough guidance?" Sonnet: "clear and efficient?" Opus: "avoid over-explaining?" Aim for instructions that work with all of them.

---

## c. Explaining the why vs rigid MUST / ALWAYS / NEVER; tone

**S3 (skill-creator) — strongest statements**
- "Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs."
- "If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag"
- Reframe so the model understands why. Also: "Use theory of mind and try to make the skill general and not super-narrow to specific examples."
- "Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs" — try different metaphors or working patterns.
- "Today's LLMs are smart. They have good theory of mind" (paraphrase of the "Explain the why" item, written with italics in the original).
- "Prefer using the imperative form in instructions."
- Note: skill-creator itself still contains one "ALWAYS use this exact template" example and an all-caps "GENERATE THE EVAL VIEWER *BEFORE*..." line (Cowork section). So it applies the yellow-flag rule loosely.

**S4 (general prompting)**
- "Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can help"
- Example pair: less effective "NEVER use ellipses"; more effective: "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them."
- "Claude is smart enough to generalize from the explanation."
- Over-emphasis makes recent models over-trigger: "these models may now overtrigger. The fix is to dial back any aggressive language." Replace "CRITICAL: You MUST use this tool when..." by "Use this tool when...".
- Also: instructions such as "If in doubt, use [tool]" "will cause overtriggering". Migration step 6: "dial back that guidance. Claude 4.6 models are more proactive and may overtrigger".
- Golden rule: show the prompt to a colleague with minimal context; "If they'd be confused, Claude will be too." Framing: Claude is "a brilliant but new employee who lacks context on your norms and workflows."

**S5 (Fable 5)** — section titled "Give the reason, not only the request": "tends to perform better when it understands the intent behind a request". Suggested template: who it is for, what the output enables, then the request.

**S9 (Fable 5.1)** — mannered prose / flourish criticism is about *outputs*, not instructions; not relevant to skill bodies except as style guidance for generated text.

**S4 — Literalism cuts the other way (important for skill rules)**
- S6 (Sonnet 5): "interprets prompts literally and explicitly... does not silently generalize an instruction from one item to another". Fix: "state the scope explicitly" (e.g. apply to every section, not just the first).
- S8 (Opus 5): if told "only report high-severity issues" or "be conservative", "the model may follow that instruction literally and report less"; ask for everything and filter in a second pass.

**S4 — Positive framing**
- "Tell Claude what to do instead of what not to do": instead of "Do not use markdown in your response", try "Your response should be composed of smoothly flowing prose paragraphs."
- S6 and S8: "Positive examples ... tend to be more effective than negative examples or instructions that tell the model what not to do." (S8 wording: "Positive examples of the communication style you want tend to be more effective than instructions about what not to do.")
- S4 also notes prompt style bleeds into output style (match prompt style to desired output; removing markdown from prompt reduces markdown in output).

**S1 — contradiction to flag**
- In the iterating section, S1 suggests Claude A may recommend "using stronger language such as 'MUST filter' instead of 'always filter'" when Claude B misses a rule. That is the opposite direction from S3/S4. See "Tensions" at the end.

**S7 (Sonnet 5.5) / scope**
- "Don't add features, tests, files, docs or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it." (example of a scope instruction written as a positive procedure + escape hatch.)
- S4 has similar overengineering prompt for Opus 4.5/4.6 ("Avoid over-engineering...") — it uses "Don't" lists, but each bullet carries its reason/limit ("A bug fix doesn't need surrounding code cleaned up").

---

## d. Progressive disclosure: references, depth, splitting, tables of contents

**S2 / S10 — the model**
- Three levels: metadata (always), SKILL.md body (on trigger), bundled files (on demand). S10: "Progressive disclosure is the core design principle that makes Agent Skills flexible and scalable."
- S2: "A Skill can include dozens of reference files, but if your task only needs the sales schema, that's the one file Claude loads."
- S2/S1: scripts are executed, not read; "only their output ... consumes tokens".

**S1 — patterns**
- SKILL.md "serves as an overview that points Claude to detailed materials as needed, like a table of contents in an onboarding guide."
- Pattern 1: high-level guide with references (quick start inline; FORMS.md / REFERENCE.md / EXAMPLES.md by link).
- Pattern 2: domain-specific organisation (`reference/finance.md`, `sales.md`...): Claude reads only the relevant file. Direct fit for ix-recipes `partials/metier_*.md`.
- Pattern 3: conditional details (basic inline, advanced in linked file).
- Splitting trigger: approaching 500 lines, or "If workflows become large or complicated with many steps, consider pushing them into separate files and tell Claude to read the appropriate file based on the task at hand."

**S1 — one level deep**
- "Keep references one level deep from SKILL.md." Reason given: with nested references Claude "might use commands like head -100 to preview content rather than reading entire files, resulting in incomplete information."

**S1 — table of contents**
- "For reference files longer than 100 lines, include a table of contents at the top." (S1 threshold = 100 lines.)
- S3 threshold differs: "For large reference files (>300 lines), include a table of contents".

**S1 — file naming**
- Descriptive names (`form_validation_rules.md`, not `doc2.md`); organise by domain; forward slashes.
- Make intent explicit: "Run `analyze_form.py`" (execute) vs "See `analyze_form.py` for the extraction algorithm" (read).
- Observe navigation: if Claude never opens a bundled file it may be unnecessary or badly signalled; if it re-reads the same file repeatedly, move content into SKILL.md.

**S3** — "Reference files clearly from SKILL.md with guidance on when to read them". Domain organisation example `references/aws.md|gcp.md|azure.md`.

---

## e. Examples, templates, input/output pairs; over-copying risk

**S1 — Template pattern + Examples pattern**
- Templates: match strictness to need (strict vs "sensible default").
- Examples: "For Skills where output quality depends on seeing examples, provide input/output pairs just like in regular prompting". Three commit-message examples, then the rule stated in one sentence.
- "Examples convey the desired style and level of detail to Claude more clearly than descriptions alone."
- Checklist: "Examples are concrete, not abstract".

**S4 — Use examples effectively**
- Make them "Relevant", "Diverse: Cover edge cases and vary enough that Claude doesn't pick up unintended patterns", "Structured: Wrap examples in `<example>` tags".
- "Include 3–5 examples for best results."
- (No sentence in the current page says outright "models copy example details"; the over-copy risk is carried by the "Diverse ... unintended patterns" line. Older Claude 4 guidance that said this explicitly is no longer on the page.)
- S4 thinking section: "Multishot examples work with thinking"; present each as problem, method, expected answer.
- Replace placeholders so the model does not emit them literally (S9: "Replace the two `[web_search: ...]` lines with your own tool's name, so the model reads them as templated tool output rather than literal text to emit.").

**S9 (Fable 5.1)** — fixing a bad habit (unmarked quoting): "add one complete example of a correct response ... the user's request, the response, and a sentence explaining why the response is correct." Example is wrapped in `<example>` with a `<rationale>` explaining why it is correct = example + why combined.

**S3** — "Use theory of mind and try to make the skill general and not super-narrow to specific examples." Warns that iterating on 2-3 test cases can yield "fiddly overfitty changes" that fail on the million other prompts.
- Example format hint: "if 'Input' and 'Output' are in the examples you might want to deviate a little."

**S6/S8** — positive examples beat prohibitions (see section c).

---

## f. Descriptions and triggering

**S1 — Writing effective descriptions**
- Field enables discovery: "should include both what the Skill does and when to use it."
- "Always write in third person." Reason: "The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems." Good: "Processes Excel files and generates reports"; avoid "I can help you..." and "You can use this to...".
- "Be specific and include key terms"; add triggers/contexts. Claude picks among "potentially 100+ available Skills".
- Bad: "Helps with documents", "Processes data", "Does stuff with files".
- Limits: `name` max 64 chars, lowercase letters/digits/hyphens, no XML tags, no reserved words "anthropic" / "claude"; `description` non-empty, max 1,024 chars, no XML tags (S1 + S2).
- Naming: prefer gerund (`processing-pdfs`); acceptable noun phrases or action-oriented; avoid vague (`helper`, `utils`), overly generic (`documents`, `data`), reserved words, and inconsistent patterns within a collection.

**S3 — triggering mechanics**
- "All 'when to use' info goes here, not in the body." (the description is the primary trigger mechanism.)
- "currently Claude has a tendency to 'undertrigger' skills" so make descriptions "a little bit 'pushy'", e.g. add "Make sure to use this skill whenever the user mentions dashboards, ... even if they don't explicitly ask for a 'dashboard.'"
- "Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries ... may not trigger a skill even if the description matches perfectly". So trigger tests need substantive prompts.
- Description optimisation: 20 queries, ~half should-trigger, ~half should-not (near-misses, not obviously irrelevant); 60/40 train/test split, each query run 3 times, up to 5 iterations, best description picked by held-out test score.
- Good trigger queries are realistic: file paths, backstory, casual phrasing, typos. Bad: "Format this data", "Create a chart".

**S10** — "Pay special attention to the name and description of your skill. Claude will use these when deciding whether to trigger the skill".

**S4 tension on pushiness** — S4 warns that aggressive language ("CRITICAL: You MUST use this tool when...") now over-triggers on Opus 4.5/4.6 and later. S3's "pushy" advice was written for undertriggering. Pushy = broader list of trigger contexts, not shouted capitals.

---

## g. Evaluation: evals first, test on target models, iterate

**S1 — "Build evaluations first"**
- "Create evaluations BEFORE writing extensive documentation." Reason: "ensures your Skill solves real problems rather than documenting imagined ones."
- Loop: (1) run Claude on representative tasks without the skill, document failures; (2) create three scenarios testing those gaps; (3) baseline without skill; (4) "Write minimal instructions" to close the gaps; (5) iterate against baseline.
- Test case structure (S1 JSON): `skills`, `query`, `files`, `expected_behavior` (list of observable behaviours, e.g. "Extracts text content from all pages in the document without missing any pages").
- Caveat: "There is not currently a built-in way to run these evaluations." Evaluations are "your source of truth".
- Checklist (Testing): "At least three evaluations created"; "Tested with Haiku, Sonnet, and Opus"; "Tested with real usage scenarios"; team feedback.

**S1 — Claude A / Claude B**
- Claude A (author) writes the skill, Claude B (fresh instance with the skill) does real tasks; observe, return with specifics, repeat. "Give Claude B ... actual tasks, not test scenarios".
- Gather team feedback: does it activate when expected, are instructions clear, what is missing.
- Watch for unexpected exploration paths, missed links, over-reliance on one section, ignored bundled files.

**S3 — test case contents** (`evals/evals.json`, `references/schemas.md`)
- Fields: `skill_name`; per eval `id`, `prompt` (realistic user task), `expected_output` (human-readable success description), `files` (optional inputs), `expectations` (list of verifiable statements; assertions added after first runs).
- 2-3 realistic test prompts "the kind of thing a real user would actually say". Save prompts first, draft assertions while runs execute.
- Per test case: spawn with-skill AND baseline in the same turn (baseline = no skill for a new skill, snapshot of old version when improving). Record tokens and duration. Grade with assertions, aggregate benchmark (pass rate, time, tokens, mean ± stddev), analyst pass, then human review in the viewer.
- "Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often don't need them."
- Assertions: "objectively verifiable and have descriptive names"; subjective skills "better evaluated qualitatively — don't force assertions onto things that need human judgment."
- Grader (S3 `agents/grader.md`): "A passing grade on a weak assertion is worse than useless — it creates false confidence." Flag non-discriminating assertions (e.g. checks filename but not content) and outcomes no assertion covers. Analyzer looks for assertions that always pass regardless of the skill and high-variance (flaky) evals.
- Iteration: generalize from feedback; stop when the user is happy, feedback is empty, or no progress. Repeated helper scripts across runs = bundle them in `scripts/`.
- Blind A/B comparison is optional: independent agent judges two outputs without knowing which is which.

**S10** — "Start with evaluation: Identify specific gaps in your agents' capabilities by running them on representative tasks". "Iterate with Claude": ask Claude to capture successful approaches and mistakes into the skill, "instead of trying to anticipate it upfront."

**S4 / S5 — re-test when models change**
- "Where a technique names a specific model, treat it as measured on that model and re-check it against your own evals".
- S5: skills built for prior models can be too prescriptive; S8: verification instructions written for earlier models cause over-verification on Opus 5.

---

## h. Anti-patterns listed (S1 unless noted)

- Time-sensitive information: do not write "before August 2025 use the old API". Put legacy in a collapsed "Old patterns" section (`<details>`), current method in the main text.
- Inconsistent terminology: pick one term (always "API endpoint", "field", "extract"). "Consistency helps Claude parse and follow instructions."
- Too many options: don't list pypdf or pdfplumber or PyMuPDF...; give a default plus one escape hatch ("For scanned PDFs requiring OCR, use pdf2image with pytesseract instead").
- Windows-style paths: "Always use forward slashes in file paths, even on Windows".
- Deeply nested references (SKILL.md -> advanced.md -> details.md).
- Vague names/descriptions; first or second person in descriptions; reserved words in names.
- Verbose explanation of things Claude knows (PDF primer example).
- Assuming tools/packages are installed: say which package to install; API has no network, claude.ai can install.
- MCP tools without server prefix: use `ServerName:tool_name`.
- Scripts that "Just fail and let Claude figure it out"; "voodoo constants" (unexplained magic numbers like `TIMEOUT = 47`); justify each value.
- Opaque file names (`doc2.md`, `file1.md`).
- S3: skills must not surprise the user ("Principle of Lack of Surprise"); no malware/exfiltration; roleplay skills are fine.
- S5/S8/S4: instructions that make the model echo its reasoning in the answer ("reasoning_extraction" refusals on Fable 5 / Opus 5 / Sonnet 5.5); over-verification instructions on Opus 5; "If in doubt, use [tool]" blanket defaults.
- S2 security: audit all files in a skill; skills that fetch external URLs are riskier.

---

## i. Domain knowledge, checklists, feedback loops, validation

**S2** — Skills "give Claude domain-specific expertise: workflows, context, and best practices that turn a general-purpose agent into a specialist." Resources section is "for factual lookup" (schemas, API docs, templates); code is "for reliability"; instructions "for flexible guidance".

**S1 — What to put in (knowledge Claude lacks)**
- Example of captured domain knowledge: table names, field definitions, filtering rules ("always exclude test accounts"), common query patterns. Test-driven discovery: add what Claude B demonstrably missed (e.g. forgot the Q4 date filter).
- S10: skills package "procedural knowledge and organizational context" that Claude cannot guess.
- Nothing in S1 says "write only knowledge Claude would get wrong" in those words; the equivalent is "Only add context Claude doesn't already have" plus eval-gap-first development.

**S1 — Workflows and checklists**
- "Break complex operations into clear, sequential steps." For complex workflows give a copyable checklist (`- [ ] Step 1: ...`); works for non-code skills too (research synthesis example with "Verify citations").
- "Clear steps prevent Claude from skipping critical validation."
- Conditional workflow pattern: decide "Creating new content?" vs "Editing existing content?" then branch.

**S1 — Feedback loops**
- "Common pattern: Run validator → fix errors → repeat". "This pattern greatly improves output quality."
- Without code, the validator can be a document: STYLE_GUIDE.md checklist; "Only proceed when all requirements are met".
- With code: validate immediately, fix, re-run, "Only proceed when validation passes".

**S1 — Plan-validate-execute (verifiable intermediate outputs)**
- Analyze -> create plan file (`changes.json`) -> validate plan with script -> execute -> verify. Use for "Batch operations, destructive changes, complex validation rules, high-stakes operations."
- Make validators verbose with specific errors ("Field 'signature_date' not found. Available fields: ...").
- Prefer scripts for deterministic work: more reliable, save tokens, consistent.

**S4 — self-check**
- "Before you finish, verify your answer against [test criteria]." catches errors "especially for coding and math"; but Opus 5 verifies on its own, so remove such instructions there (S8).
- S4 hallucination/grounding and research sections exist (long pages; not mined here beyond headings: "Research and information gathering", "Minimizing hallucinations in agentic coding").
- S5: separate fresh-context verifier subagents "tend to outperform self-critique" for long runs.

---

## Tensions and surprises (for the grid)

1. "Be concise" vs "explain the why": not contradictory in the sources. S1 says cut what Claude already knows; S3/S4 say add the reason behind each non-obvious rule. The test that reconciles them: a sentence earns its tokens if it carries information Claude lacks (a domain fact, or why this rule exists), not if it restates general competence.
2. S1's iteration advice ("stronger language such as 'MUST filter'") contradicts S3's "yellow flag" and S4's "dial back any aggressive language"; S1 is older-style advice, S3 and S4 are more recent and model-specific (4.5/4.6+). Treat caps as a last resort and prefer a reason or a rewording.
3. Literalism cuts both ways: S6/S8 say recent models follow instructions literally (so scope must be stated, and "be conservative" under-reports), while S4 says over-emphasis causes over-triggering. Net: precise scope + reason, no shouting.
4. TOC threshold differs: S1 says >100 lines, S3 says >300 lines. Pick the stricter (100) or cite both.
5. S5 (Fable 5) says older skills "are often too prescriptive" and may degrade output; S1 still recommends low freedom for fragile operations. Prescriptiveness should be reserved for fragile or deterministic steps and justified.
6. The old explicit "models copy example details" warning is not on the current prompting page; only "Diverse ... unintended patterns" and "Positive examples" remain. Do not attribute the stronger claim to Anthropic without the older source.
7. S1 has no publication date; S10 is dated Oct 16, 2025 (with a Dec 18, 2025 update note). Treat S1 and S4 as living pages read on 2026-10-16.
