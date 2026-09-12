# BUILD_BRIEF.md

**Repository:** CINE venture design and plan
**Owner:** Dhruv Sharan
**Origin:** IIM-A MBA submission, "Breaking Academic Barriers with Multi-Modal AI Tutoring" (2025), substantially revised September 2026
**Run with:** Claude Code, Fable or Opus, ultracode mode
**Commit this file to the repo root. It is the source instruction; the repo is the source of truth that follows from it.**

---

## 0. What you are doing

You are populating a repository that is the central design and planning record for a venture: an AI tutor for UK secondary students (GCSE and A-level), built from Bengaluru, whose distinguishing feature is that a student chooses **how** they are taught by picking a named educator whose style they already know.

You are not writing application code. You are writing the design, the plan, the evidence behind both, and the honest account of what is still unknown. A later phase turns this repo into a codebase; until then it is a vault that a lawyer, an investor, a co-founder or a curriculum specialist can each open and act on.

**Output format:** each document is a standalone HTML file under `/docs`, styled to be genuinely good to read, published via Netlify pulling from this repo. Visual quality is a requirement, not a nicety; these documents get sent to people whose first judgement of the venture is how the design reads. Use a single shared stylesheet. No build step, no framework, no external runtime dependencies. Legible on a phone.

---

## 1. The acceptance bar

These two statements are the stop condition. They are reproduced verbatim from the conversation that produced this brief. Do not paraphrase them, do not soften them, and check the finished repo against these exact words.

### The owner's bar

> You open the finished design without me and can do four things. Put the two routes side by side and choose between them, and defend that choice to an investor who prefers the other one. Hand the persona chapter to a UK media lawyer and to the first creator you want to sign, and both can act on it that day. Pick any accuracy claim and trace it to the test that proves it. Point at the line that says what happens to a child's data and be comfortable putting it on the marketing site.

### The technical bar

> The product runs with zero licensed personas and the design proves it. Age assurance specified at something the ICO would accept after Reddit, not a date-of-birth field. Every persona traces to a rights model covering scope, term, termination, what happens to the voice and style mapping when a licence ends, on-screen labelling, and a kill switch with a stated time to effect. Nothing reaches a learner that cannot be traced to a source in the item bank, with a stated accuracy floor and a stated behaviour below it. The OSA scoping decision written down with the trigger that changes it. Everywhere I have reasoned rather than verified is marked. And the brief, run cold in a fresh session, produces the repo it claims to.

---

## 2. Settled decisions: do not re-open these

Each of these was decided deliberately. If the design you write contradicts one, you have made an error, not an improvement.

| # | Decision | Why |
|---|---|---|
| D1 | **UK first.** Bengaluru is the build base; the UK is the market. | Higher willingness to pay and to experiment; Indian edtech is crowded and Indian child-data law is categorically hostile to adaptive tutoring sold direct. |
| D2 | **Two routes planned in parallel:** Route A direct to parents, Route B through schools. Route A is the owner's current preference. | The owner wants to choose on evidence, not on either of our priors. |
| D3 | **Shared core written once.** Roughly 80% of the design does not care who pays. Divergence is confined to pricing and unit economics, data and consent model, distribution motion, and compliance posture. | Avoids writing two full plans. |
| D4 | **Named-educator personas are the wedge**, retained against advice to substitute institutional teachers. | A student cannot articulate a pedagogy but can name someone who teaches the way they like. The name is the handle; the style is the substance. |
| D5 | **Personas pass a student usefulness test, not a fan's ear test**, at launch. The creator licenses name and likeness only. No creator material is ingested. | One-page agreement rather than a content-licence negotiation; a departing creator costs a text file; the kill switch is genuinely instant; zero-persona launch becomes real. |
| D6 | **Route to high-fidelity personas (exemplar conditioning on licensed creator material) must be designed for now, not bolted on later**, as a contingency if market feedback on D5 is weak. | Owner's instruction. The boundary must be built now or the fallback becomes a rewrite under time pressure. |
| D7 | **Style is represented as a structured parameter object**, with a written style card generated from it as the surface layer given to the model. | Prose alone drifts and captures register while losing structure. Parameters are auditable, composable, and legally inert. The object gains an exemplar field under D6 without rebuilding the conditioning path. |
| D8 | **No persona LoRAs or fine-tuned weights carrying creator style.** Retrieval and prompting only. | Weights cannot be cleanly revoked. A kill switch requiring retraining is not a kill switch. |
| D9 | **Voice cloning is off the launch path**, and becomes a separate opt-in limb of the creator licence. | Highest-risk signal on both the rights and the regulatory side; the specific thing Ofcom named when warning about virtual clones. |
| D10 | **Student-facing style control.** Picking a creator selects a preset; the student may then move individual dimensions. | Preserves the handle and lets them turn it. |
| D11 | **Zero-persona operation is a hard requirement**, not a contingency. The product launches and runs with no signed creators. | No single unsigned contract can block launch. |
| D12 | **Clean-room content.** Original items written to the published specification, examiner-validated. No exam board material enters the system. | See §4; AQA has published a policy that forbids it. |
| D13 | **No offshore litigation-evasion strategy.** The Indian operating company is retained for ordinary tax and capital reasons; the "fight it in India" rationale is dropped. | See §4.4. The theory runs the opposite way to how it was first read. |
| D14 | **Ship named presets and unnamed archetypes simultaneously from day one**, and instrument return rate rather than satisfaction score. | Distinguishes "the wedge is weak" from "the fidelity is short", which have opposite fixes. |

---

## 3. Verified findings

**This section is your factual base. You may not have web access. Do not supplement it from memory, and do not invent figures to fill gaps.** Every claim here was checked in September 2026 against the source named. Reproduce these with their dates and sources in `/docs/00-thesis.html` and `/evidence/sources.html`. Where a document needs a fact that is not in this section or §4, say that the fact is missing rather than supplying one.

### 3.1 The differentiation in the 2025 submission has been commoditised

- OpenAI launched **Study Mode** in ChatGPT on 29 July 2025; Google launched **Guided Learning** in Gemini roughly a week later, built on LearnLM; Claude has an equivalent Learning Mode. All are free toggles.
- Gemini's Guided Learning already produces scaffolded multimodal output including images, diagrams, videos and interactive quizzes, and can generate flashcards and study guides.
- Google offered students in the US, Japan, Indonesia, Korea and Brazil a free 12-month AI Pro subscription, and committed $1bn over three years to AI education in the US.
- Khanmigo is free to all US teachers; a consumer price point of $4/month has been reported.

**Implication for the design:** "an LLM that teaches Socratically with diagrams" is not a product. Sections 4.1 and 5.1 of the original submission describe features that three consumer apps now give away. The thesis document must confront this directly rather than restate the original claim.

### 3.2 The evidence base for AI tutoring strengthened

- Kestin, Miller, Klales et al., *Scientific Reports*, published 3 June 2025: a purpose-built AI tutor at Harvard produced median learning gains more than double those of an active-learning classroom group. The AI supplemented human teaching rather than replacing it; the correct comparison is AI-supported instruction versus conventional instruction.
- ASSISTments: effect sizes of 0.18 to 0.29 SD across two large RCTs, ESSA Tier 1 evidence rating, at under £100 per student.
- Carnegie Learning MATHia: 0.21 to 0.38 SD across more than 18,000 students in 147 schools.
- Reported caveats: accuracy gaps at subject edges; students who default to the AI rather than working a problem can develop surface fluency that does not hold under exam conditions.

### 3.3 UK market

Sutton Trust, *Private Tutoring 2026*, published February 2026:

- 29% of secondary pupils in England and Wales have had private tutoring at some point, up from 18% twenty years ago and 27% in 2019.
- Year 11 is the peak year at 25%, followed by Year 10 at 10%.
- London 45%, rest of England 27%, Wales 24%. Urban 33%, rural 19%.
- Worst-off households 23%, best-off 30%.
- By ethnicity: Black pupils 64%, Asian 50%, White 20%; in deprived areas, 65%, 43% and 10% respectively.
- 20% of pupils received one-to-one or small-group tutoring organised by their school, down from 22% in 2023; separate 2025 polling found 58% of schools had reduced their tutoring offer year on year.

Prevailing 2026 rates: roughly £25 to £45 per hour at GCSE, £35 to £65 at A-level. An earlier Sutton Trust estimate put the UK private tuition market at up to £2bn.

**Implication:** the demand is concentrated in Year 11, in London and in urban areas, and the school-funded channel is shrinking. This is the strongest single argument for Route A and it must be stated as such in the route comparison.

UK competitors already in market: Third Space Learning's **Skye** (voice-based conversational maths tutoring), **Century Tech** (adaptive pathways), **Oak National Academy's Aila** (teacher lesson-planning assistant, reported to save teachers 3 to 4 hours per week; state-backed and free).

### 3.4 Exam board rights: the hardest constraint

- **AQA's published copyright and IP policy states that AQA does not permit the use of any AQA material, in any manner or for any purpose, in connection with the training of AI-powered tools or technologies; and that it will not allow the use of any AQA material in or on any edition of a third-party work where any part of that work is generated or produced using AI.** Read plainly, the second limb bars an AI tutoring product from containing AQA material at all, not merely from training on it.
- **Pearson/Edexcel** permits approved examination centres to reproduce past papers and mark schemes for practice, revision or teaching within the centre, on condition that students are not charged. A paid consumer product is outside that permission by construction.
- Both boards assert copyright over specifications, schemes of work, past papers and mark schemes.

**What this does and does not prohibit.** Copyright protects expression, not facts or curricula. Nobody owns the requirement that a student know Newton's second law, and GCSE and A-level subject content is set and published by the DfE. Teaching *to* a published specification with wholly original items and explanations is not an act a board has standing to stop. Reproducing its papers, mark schemes, or specification text is. The design must hold that line explicitly and visibly.

### 3.5 UK regulators

**ICO** (Information Commissioner's Office; the UK data protection regulator; Information Commissioner John Edwards; fines to the higher of £17.5m or 4% of global annual turnover):

- Fined **Reddit £14.47m on 24 February 2026** for unlawfully processing children's personal data, specifically inadequate age assurance and profiling children without a lawful basis. MediaLab was fined earlier the same month. Prior actions: TikTok £12.7m, Snap £1.95m.
- **Open letter, 12 March 2026:** self-declared age is no longer adequate where a service is likely to be accessed by children; platforms should use modern age assurance technologies.
- The ICO has stated it will audit edtech providers, and publishes Children's code guidance with a sector-specific edtech FAQ.
- A joint ICO/Ofcom statement on age assurance was published in March 2026.
- Unlike India, the UK has **no categorical ban** on profiling children. Profiling is permissible with a lawful basis and Children's code compliant design: high privacy by default, profiling off unless justified, best interests of the child.

**Ofcom** (Online Safety Act 2023):

- Open letter of 8 November 2024 confirmed the OSA reaches generative AI. A service is user-to-user where users can share chatbot-generated content with other users, or where users can create chatbots made available to others. The trigger incidents included users building virtual clones of real people.
- Penalties: the higher of £18m or 10% of qualifying worldwide revenue.
- Where non-compliance continues, Ofcom may seek court-ordered business disruption and service restriction measures: UK ISPs blocking the service, app stores removing the app, payment providers ceasing to process.
- The Act reaches providers with links to the UK regardless of where they are established. Between 1 April 2025 and 30 June 2026 Ofcom imposed penalties totalling £6.1m on nine companies that were either not UK-based or did not state their jurisdiction. It has pursued business disruption measures, including a possible UK access block, against a non-compliant overseas provider fined £950,000.

### 3.6 India, for the operating entity and for Route C if it is ever revisited

- DPDP Rules 2025 notified November 2025. Anyone under 18 is a child. Verifiable parental consent is mandatory (Rule 10; identity verification including Aadhaar-linked DigiLocker virtual tokens; audit trails required).
- Section 9(3) prohibits tracking, behavioural monitoring and targeted advertising directed at children. **The prohibition stands independent of consent and cannot be waived by a parent.**
- Fourth Schedule, Part A, Entry 3 exempts educational institutions, defined as institutions of learning imparting education including vocational education, and fiduciaries engaged by them, where processing is limited to educational activity or child safety. Whether a digital-first edtech platform falls within that definition is **unresolved**.
- An edtech company that determines its own purposes, including building learning analytics or offering direct-to-student services, is an independent data fiduciary rather than a processor. At scale with children's data and behavioural analytics it is a candidate for Significant Data Fiduciary designation.
- Children's-data obligations take effect approximately 18 months from notification, so around May 2027.
- **IT (Intermediary Guidelines and Digital Media Ethics Code) Amendment Rules 2026**, G.S.R. 120(E), notified 10 February 2026, in force 20 February 2026: defines synthetically generated information, requires prominent labelling and permanent provenance metadata that cannot be stripped, compresses takedown for flagged unlawful content to three hours and for non-consensual sexual imagery to two.
- Indian personality-rights jurisprudence is currently the most aggressive in the world on AI likeness: Anil Kapoor (Del HC 2023), Jackie Shroff (2024), Arijit Singh (Bom HC 2024, AI voice cloning), Hrithik Roshan (CS(COMM) 1107/2025, Del HC, 72-hour takedowns and domain suspensions), and **Sonakshi Sinha v. Character Technologies Inc & Ors, Del HC, 20 March 2026, 2026 SCC OnLine Del 1177**, restraining misuse of identity through AI chatbots, deepfakes and voice cloning.
- **Section 44A, Code of Civil Procedure 1908:** the United Kingdom is a notified reciprocating territory and the English High Courts are notified superior courts (Notification F.34-I/52-L, 1 March 1953). A UK superior court money decree is executable in India as if passed by an Indian District Court, without a fresh suit, subject only to the Section 13 conclusiveness tests. The Delhi High Court has enforced an ex parte English Commercial Court judgment for USD 47m on this basis.

### 3.7 Competitive and infrastructure context

- PhysicsWallah raised $210m at a $2.8bn valuation in September 2024 and has since pursued an IPO. Co-founder Prateek Maheshwari told *Business Today* on 1 June 2026 that PW would ship its AI tutor that year, and that its edge over OpenAI, Google and Anthropic is access to millions of Indian students and the behavioural data they generate.
- IndiaAI Mission common compute passed 38,000 GPUs by late 2025, subsidised to roughly ₹65 per hour for startups, researchers and academia. Sarvam was selected to build India's sovereign LLM, open-weight, around 120B parameters, designed for reasoning, voice and Indian languages, with a ₹98.68 crore subsidy against 4,096 H100s for six months.

---

## 4. Reasoned but not verified

**Mark every one of these in the repo as an open assumption, not a finding.** They shape the plan and none of them has been confirmed.

1. Whether AQA's AI clause bites at inference (retrieval-grounded use at runtime) as well as at training. The wording is broad enough to cover both; this has not been tested.
2. Whether OCR, WJEC and Eduqas take the same position as AQA. Not checked.
3. That naming an exam board to describe what a product prepares a student for can be honest descriptive use under section 11(2) of the Trade Marks Act 1994, provided endorsement is not implied. Stated as counsel's likely starting point, not as settled advice.
4. That UK protection of a creator's persona runs through passing off for false endorsement (following *Irvine v Talksport*), trade marks, copyright in the underlying videos, performers' rights, and data protection insofar as a voice is personal data, there being no statutory UK personality right.
5. **That Save My Exams, Physics & Maths Tutor, Seneca, Cognito and Twinkl sell board-aligned commercial revision material without licensing past papers.** This is inference from their existence, not from their terms. Establishing exactly where each of them draws the line is a named research task, not a finding.
6. That a private one-to-one tutor with no sharing between users sits outside the OSA's user-to-user duties. Reasoned from Ofcom's published examples; needs counsel.
7. That UK GDPR Article 3(2) and the Article 27 UK representative requirement apply to an India-established controller serving UK children. Standard position, unconfirmed for this fact pattern.
8. The proportion-of-screen and proportion-of-audio requirements for synthetic content labelling under the Indian rules appeared in the October 2025 draft; the final notified text has not been checked.
9. That most creators the venture wants are US-resident, bringing US state right-of-publicity law into scope.

---

## 5. Open items for counsel: do not resolve these yourself

Write them as questions, with the decision each one unblocks and the cost of getting it wrong. Do not supply an answer, a likely answer, or a range.

- Does AQA's AI clause reach runtime retrieval, or only training?
- Do the other boards' positions differ, and does any board licence for AI use at any price?
- What exact wording may be used to state which specification a course follows, without implying endorsement?
- Is a one-to-one tutor with no inter-user sharing outside the OSA user-to-user duties, and precisely which feature changes that?
- What age assurance method would satisfy the ICO for a service whose entire user base is children, at a cost compatible with a consumer price point?
- What is the minimum viable creator licence for name and likeness only, and what does the exemplar-conditioning upgrade under D6 add to it?
- Which entity contracts with the parent, and what does that do to consumer jurisdiction, UK representative obligations and VAT?

---

## 6. Repository structure

```
/BUILD_BRIEF.md              this file, unchanged
/README.md                   what this repo is, how to read it, status, how to publish
/docs/
  index.html                 contents page and reading order
  00-thesis.html
  01-product.html
  02-style-engine.html
  03-curriculum-and-content.html
  04-rights-dossier.html
  05-safety-privacy-regulatory.html
  06-architecture.html
  07-route-a-direct-to-parents.html
  08-route-b-through-schools.html
  09-route-comparison.html
  10-economics.html
  11-roadmap.html
  12-risk-register.html
  13-open-items.html
  decision-ledger.html
  style.css
/evidence/
  sources.html               every external claim, with source and date checked
/contracts/
  creator-licence-term-sheet.md
  creator-licence-heads-of-terms.md
/netlify.toml
```

### Document specifications

**00 Thesis.** What is true, what changed between the 2025 submission and now, and what the venture is for. Must state plainly that the original differentiation has been commoditised (§3.1) and answer, in one page, why a parent pays when Gemini is free. That answer is the owner's: the free tools are general-purpose and know nothing about a specific board, a specific exam, or how this particular student wants to be taught. Argue it properly or say it does not hold.

**01 Product.** The learner, the session, what is promised. A worked session transcript for one real topic at GCSE level, showing the style engine visibly changing the teaching rather than the vocabulary. State what the product does not do.

**02 Style engine.** The parameter set: the dimensions along which teaching varies, each observable and owned by nobody. Start from, but do not treat as final: point of entry (concrete situation versus formal statement), lateness of formalism, one running example versus many varied, error response (direct correction versus predict-then-falsify), digression tolerance, visual density, pace of abstraction. Define each with its range and its observable signature. Then: how a style card is generated from the object; how a named preset maps a creator onto a point in the space; how a student adjusts individual dimensions from a preset (D10); how conformance is tested, because a style that cannot be verified is a claim; and the D6 boundary, namely the exact interface at which exemplar conditioning would attach, what changes when it does, and what does not.

**03 Curriculum and content.** The clean-room policy: what may enter the item bank and what may not, with provenance recorded per item. The examiner validation process and who performs it. The accuracy floor as a number, the harness that measures it, and the defined behaviour below floor. Scope at launch, which will be narrower than desirable: name the board, the subject and the tier, and say how many items get examiner validation at launch and what that costs.

**04 Rights dossier.** The chapter that must survive contact with a lawyer and a creator on the same day. Contains: the position on each exam board with the AQA policy quoted and dated; the copyright line between specification-shaped teaching and reproduction (§3.4); the creator licence covering scope, term, exclusivity, termination, what happens to the style mapping and any voice model when a licence ends, on-screen labelling, and the kill switch with a stated time to effect; the enforcement war-game, naming who can do what on what timeline, and covering payment processors and app stores as the real chokepoint rather than the courts; and why the offshore litigation strategy was considered and dropped (D13, §3.6 on Section 44A and §3.5 on business disruption measures).

**05 Safety, privacy and regulatory.** Age assurance specified concretely. The data model for a child user: what is held, for how long, who can see it, what is inferred and on what lawful basis, and the one-line statement that goes on the marketing site. Children's code compliance mapped point by point. The OSA scoping decision, with the trigger that changes it stated explicitly: user-created or shareable personas convert the service into a user-to-user platform with the full duties attached (§3.5). Content safety, escalation paths, and what the tutor does when a student raises something outside academic scope.

**06 Architecture.** Models, retrieval, data model, evaluation harness, kill-switch mechanics, cost per session. Buy the model, own the item bank and the verification layer; the moat is the examiner-validated content and the outcome evidence, not the model. Justify every choice against a constraint in §2 or §3, and state what each choice makes harder later.

**07 and 08 Routes.** Each covers pricing and unit economics, the data and consent model, the distribution motion, and the compliance posture. Route A must confront churn after exam season and the Year 11 concentration (§3.3). Route B must confront the 58% of schools that cut their tutoring offer, and say who in a school holds the budget.

**09 Route comparison.** The document the owner uses to choose. Side by side on: cost to run, time to first revenue, what breaks first and how you find out, what each forecloses, and what it costs to change your mind. Evidence attached to each cell. A recommendation with the condition under which it holds. It must be usable to defend the choice to an investor who prefers the other route, so state the strongest case for the one you do not recommend.

**10 Economics.** Cost per session built up from the architecture rather than assumed. Price points against the £25 to £45 GCSE tutoring rate (§3.3). Sensitivity to the one variable that dominates, which you should identify rather than assume. Examiner validation as a real line item.

**11 Roadmap.** Milestones defined by evidence obtained rather than features shipped. Include the D14 instrumentation and the D6 trigger: named presets go to exemplar conditioning only when they show a clear retention advantage over unnamed archetypes *and* qualitative feedback attributes the shortfall to fidelity rather than relevance.

**12 Risk register.** Ordered by the owner's ranking: a creator or board suing first, teaching something wrong before an exam second, nobody paying third, child harm or data breach fourth. Note in the document that the engineering standard for the fourth does not follow that ordering, and why.

**13 Open items.** §4 and §5, each with the decision it unblocks and the cost of being wrong.

**Decision ledger.** Every decision in §2, plus every decision you take while writing, in the form: what was chosen, which constraint drove it, what was rejected and what it would have cost, and what it makes harder later. Dated. This is the document that lets someone reconstruct the reasoning in six months.

---

## 7. House style

- **British English.**
- **No em-dashes.** Use commas and semicolons for clause separation.
- Conclusions before the reasoning that supports them.
- Conviction-forward and analytically grounded. Honest self-assessment over polished corporate framing. If something is weak, say it is weak.
- No invented figures. No plausible-sounding market numbers. If a number is needed and is not in §3, write that it is needed and unknown.
- Every external claim carries its source and the date it was checked, and appears in `/evidence/sources.html`.
- Unverified reasoning is visibly marked as such, in the text, not in a footnote.

---

## 8. Before you declare this done

Run these checks and report what each actually returned, not what you expect it to return.

1. **Owner's bar, item by item.** Can someone open `/docs/09-route-comparison.html` and choose? Can `/docs/04-rights-dossier.html` be sent to a lawyer and a creator today? Pick three accuracy claims at random from anywhere in the repo and trace each to its test. Find the single line about a child's data and read it as if it were on a marketing site.
2. **Technical bar, item by item.** Zero-persona operation proved, not asserted. Age assurance specified beyond a date-of-birth field. Kill switch with a stated time to effect. Accuracy floor with a stated below-floor behaviour. OSA trigger written down. Every unverified claim marked.
3. **Contradiction sweep.** Read the two route documents against the economics and the roadmap, and list anything that cannot be true at the same time.
4. **Adversarial read.** Take the finished repo into a fresh context with none of the reasoning that produced it, and brief that reader to find the thing that would embarrass the owner in front of a lawyer, a school, or a parent. Report what it found, including anything you disagree with.
5. State plainly which parts of the design are tested, which are reasoned but unproven, and which single part is most likely to break first and how it would be noticed.

If you reach the end without meeting the bar, say so and name the specific blocker. Do not redefine the bar downward to reach it.

