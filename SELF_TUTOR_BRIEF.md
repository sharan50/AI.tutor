# SELF_TUTOR_BRIEF

The contract for adding the self-tutor to the Tutor. Written 23 October 2026 from
the owner's instructions of that day. It governs the work it describes; where it is
silent, `BUILD_BRIEF.md` and `CLAUDE.md` govern.

## 1. What the self-tutor is

A learner may choose to be taught by a tutor with their own face and voice. They
capture their face and voice once, live in the product; from then on the tutor can
appear and speak in their likeness, teaching in any style the product offers.
Nothing is trained on the learner: the teaching is the Tutor's own, gated as every
turn is, and the likeness is only how it is presented.

The owner's case for it: being taught by oneself may build confidence, a benefit
nobody has measured (OA-37). It is designed as a launch feature.

## 2. The owner's decisions, 23 October 2026

1. Voice, image and style are all included.
2. The Tutor launches with it. Every document is designed on that basis.
3. Counsel's advice is logged as needed. The feature proceeds unless counsel gives
   a categoric no.
4. The owner's view on Ofcom: its warning about virtual clones was made in a child
   protection and safety context, and where the company controls what can be
   generated it is not a concern. Record this as the owner's view (OA-38), never as
   fact. OI-4 stays open.

## 3. Defaults taken while writing

The owner did not specify these. Each is recorded as a decision the owner may keep
or reverse, and the report says so:

- **Image** means a head-and-shoulders face scan. No full-body image (D61).
- **Style:** every archetype; a named educator's preset only where that creator has
  opted in by a new licence term (D66).
- **Visibility:** the learner's alone (D60).
- **Route:** families buying directly (Route A) only, at launch (D67).
- **D9** is narrowed by the owner's amendment, as the direct consequence of launching
  with the learner's voice (section 5).

## 4. Decisions D59 to D69

Recorded in a new ledger section, `src/content/decision-ledger/049-self.html`,
`<h2 id="self">D59 to D69: the self-tutor</h2>`, each as `<dt>` and `<dd>` with
Driven by, Rejected and Makes harder, following `048-ideas.html`. D59 is the
owner's; D60 to D69 were taken while writing and are the owner's to keep or reverse.

- **D59.** The Tutor launches with a self-tutor: a learner may choose to be taught by a
  tutor with their own face and voice, in any style the product offers (D66). It is
  designed into every document as a launch feature and proceeds ahead of counsel's
  answers on OI-23 to OI-27. It is withdrawn in a market only if counsel advises in
  writing that no form of it the design allows may launch there; a conditional
  answer changes the design instead of stopping it.
- **D60.** The self-tutor is the learner's alone. No parent, school, creator or other
  user can see or hear it; nothing it renders can be shared, exported or downloaded;
  the parent report shows the same progress for self-tutor sessions as for any
  other, and never the likeness.
- **D61.** A self-tutor is made only from a live capture in the product: a
  head-and-shoulders face scan and a voice sample read from prompted sentences,
  with a liveness check. No uploaded photograph, video or recording is accepted,
  and no full-body image is taken.
- **D62.** Before capture, the verified adult and the learner each consent,
  separately and explicitly, after being told in plain words what is kept, that no
  one else can see or hear it, and how to delete it. Either can withdraw at any
  time, which deletes the self-tutor. It is off by default.
- **D63.** The learner or the adult can delete the self-tutor at any moment. A deletion
  flag is read at every turn under the kill switch's sixty-second cache ceiling, so
  rendering stops at the next turn; samples, anything derived from them and any
  rendered clip leave primary stores within seven days, and the vendor holds nothing
  under zero-retention terms (D24). A self-tutor is also deleted when the account
  closes, or after twelve months without a self-tutor session.
- **D64.** The self-tutor speaks only text that has passed the gate. Speech and
  animation are rendered after the verifier, from the text shown on screen, which is
  always shown; a blocked turn falls back as text does. Every clip carries a visible
  label that it is synthetic, and provenance metadata. The self-tutor never claims to
  be the learner, never comments on their face or voice, and offers no filter or
  alteration of the likeness.
- **D65.** No model weights are trained or fine-tuned on a learner's face or voice. The
  likeness is conditioned at render time from the stored samples or embeddings
  derived from them, so deleting those deletes the likeness. A vendor that can clone
  only by fine-tuning is excluded.
- **D66.** Every archetype is available in the self-tutor, with the learner's own
  adjustments (D10). A named educator's preset is available in it only where that
  creator has opted in by a new licence term, and the label says whose style it is
  without implying that the creator appears.
- **D67.** At launch the self-tutor is offered only to families buying directly
  (Route A). Through schools (Route B) it is off until counsel has answered OI-23
  for a school as controller.
- **D68.** In the experiment D14 sets up, the self-tutor is a second factor, not a third
  arm: learners are assigned to named or unnamed presets as D14 requires, and
  separately to being offered the self-tutor or not, so the wedge's measurement
  stays clean. T-SLF-01 measures the self-tutor's effect.
- **D69.** No style dimension reaches the self-tutor's voice. The learner's own voice
  speaks the gated text at one neutral delivery under every preset; speaking rate,
  pitch and intonation are set by the voice rendering, never by the preset. (Added
  while writing 02, for D17's reason and so T-STY-02 cannot be passed by sound.)

## 5. D9, amended by the owner

`BUILD_BRIEF.md` §2 and the ledger's settled group, recorded as D1's amendment was:
the old text kept, the new text, the date, and a plain statement that the change rests
on the owner's decision and an unverified view (OA-38), not on evidence, and
overrides the ledger's rule against re-opening on preference for D9 alone.

- **Old:** "Voice cloning is off the launch path, and becomes a separate opt-in limb of
  the creator licence."
- **New:** "Cloning a creator's voice, or anyone's voice but the learner's own, is off
  the launch path, and a creator's voice becomes a separate opt-in limb of the
  creator licence. A learner's own voice, in the self-tutor (D59), is on it."

## 6. Register entries

**Counsel questions** (`14-open-items#counsel`), all new, none answered:

- **OI-23.** UK data. Are a learner's face scan and voice sample, and anything derived
  from them, biometric or special category data under UK GDPR when used to present a
  tutor in their likeness rather than to identify them? What lawful basis applies?
  Can a learner of 14 to 17 give the consent, or must the verified adult, or both?
  What does the Children's code require of the feature? Does a school-controlled
  version change any of this? Unblocks D59, D62 and D67.
- **OI-24.** Ofcom. Does a self-tutor only its learner can see or hear engage the
  Online Safety Act, or the virtual-clone concern in Ofcom's letter of 8 November
  2024, given that the company controls what it says? With OI-4 and OA-38.
- **OI-25.** US. For a US launch (D1), which state laws on biometric identifiers and on
  minors' data apply to a learner's face and voice used this way, and what consent,
  notice, retention and deletion duties follow? With OI-21.
- **OI-26.** Labelling. What labelling and provenance duties apply to synthetic audio
  and video of a real person shown only to that person: under India's IT Rules 2026,
  the operating company being in India, and in the UK and the US?
- **OI-27.** The licence. What must the new opt-in term say so that a named preset
  delivered in a learner's likeness implies no endorsement by the creator, and may a
  creator's name label it at all?

**Assumptions** (`14-open-items#assumptions`), all new:

- **OA-37** (group: Product and style). That being taught by a tutor with one's own face
  and voice helps a learner, by more confidence, more persistence or better unaided
  performance, rather than distracting them or making them self-conscious. The
  owner's view and the case for D59. Adjacent research is registered as candidates
  CV-13 to CV-15; none tests the question directly. Settled only by T-SLF-01.
- **OA-38** (group: Regulatory). That Ofcom's concern with virtual clones of real people
  does not reach a self-tutor only its learner can access and whose output the
  company controls. The owner's view, and the basis of D59 and of D9 as amended.
  With OI-24 and OI-4.
- **OA-39** (group: Regulatory). That live capture with a liveness check stops a self-tutor
  being made of anyone but the learner often enough; a person physically present can
  still be captured in the learner's place. T-SLF-02 at M2.
- **OA-40** (group: Commercial). That parents will consent to their child's face and
  voice being used this way. **Resolvable by asking parents** (so it counts among
  the assumptions resolvable by asking).

**Tests**, defined in one table in `01-product#self` (rows
`<tr><td class="id">T-SLF-0N</td><td>...</td>...`), referenced elsewhere:

- **T-SLF-01.** The self-tutor's effect, as D14's second factor (D68): unaided
  performance on held-out items and stated confidence, compared between learners
  offered the self-tutor and learners not; pre-registered. M3 to M4. Not a release
  gate; it decides whether the feature stays and what may be claimed for it.
- **T-SLF-02.** Only a live person can be captured: replayed photographs, videos and
  recordings are refused, at a false-accept rate measured at M2 against a threshold
  written down before M2 begins. Release gate.
- **T-SLF-03.** Nothing is spoken or shown in the likeness that the gate did not pass:
  every clip's script equals the gated text on screen. Blocking, on every release.
- **T-SLF-04.** Deletion is complete: rendering stops at the next turn after deletion;
  samples, derived conditioning and clips leave primary stores within seven days;
  the vendor confirms deletion. Release gate.
- **T-SLF-05.** No path to anyone else: no surface lets anyone but the learner see or
  hear a self-tutor, or obtain anything it renders; checked against every surface,
  with T1, T2 and T9 in `05#trigger`. Release gate.
- **T-SLF-06.** Every rendered clip carries the synthetic label and provenance
  metadata. Release gate.

**Risks** (`12-risk-register`, second tier):

- **R12.** A self-tutor is made of someone other than the learner. Mitigation: D61,
  T-SLF-02; residual: a person present at the camera (OA-39).
- **R13.** A breach of children's face and voice data. Mitigation: D63, D65, a separate
  encrypted store, zero-retention vendor terms.
- **R14.** Harm to a learner from seeing and hearing themselves teach: self-image,
  distress, over-attachment. Mitigation: off by default, one tap back to the
  standard tutor, no filter, no comment on appearance (D64); signals to D26's route.
- **R15.** A categoric no, or a regulator's action after launch, removes a launch
  feature. Mitigation: D59's rule; the product launches and runs without it, as it
  runs without creators (D11).

**Candidates** (`sources.html`, section 8; found 23 October 2026 through search
summaries only, unchecked):

- **CV-13.** Video self-modelling: a meta-analysis of single-case studies (Mason and
  others, 2016, *Journal of Developmental and Physical Disabilities*) found effects
  strongest for autistic participants and small to none for learning disabilities;
  most studies involve young children, and evidence for secondary students is thin.
  Source: the ASHA evidence map summary.
- **CV-14.** Fox and Bailenson (2009), *Media Psychology* 12(1): adults who watched a
  photorealistic virtual likeness of themselves exercising exercised more afterwards,
  including 24 hours later, than those who watched a likeness of someone else or
  none. Source: Stanford Virtual Human Interaction Lab.
- **CV-15.** A 2024 study in *Frontiers in Education* with 133 university students:
  learner self-avatars did not significantly change performance beyond the AI
  teacher's presence, but changed learners' perception of it and their motivation.

Text relying on a candidate carries an Assumed marker naming it (D53).

## 7. Where each part goes

New sections are fragment files placed by filename. Each page's contents list in its
`000-head.html` gains the new entry. New sections inherit their page's owner.

| Page | New section | Also |
|---|---|---|
| 01 Product | `075-self.html`, `<h2 id="self">The self-tutor</h2>`: what the learner sees and does, consent and capture, the session, the controls, what it never does, the T-SLF table, a `data-key="01-product.self.1"` lede | `080-parent`: the report never shows the likeness. `090-not`: never makes a self-tutor of anyone but the learner; never shows one to anyone else |
| 02 Style engine | `055-self.html`, `<h2 id="self">Style in the learner's own likeness</h2>`: the likeness carries no style; what, if anything, of the style object reaches speech; named presets by opt-in (D66); D68 | the preset or adjust section, a pointer |
| 04 Rights dossier | `065-self.html`, `<h2 id="self">The learner's own likeness</h2>`: no third-party persona right; the misuse case (someone else's likeness); the opt-in term; labelling (OI-26) | `050-creator`: a licence row for the opt-in term. `060-killswitch`: a creator's kill switch reaches self-tutor presets. `070-india`: synthetic-content labelling |
| 05 Safety, privacy, regulatory | `085-self.html`, `<h2 id="self">The self-tutor: a child's face and voice</h2>`: the data, consent, the Children's code, Ofcom and the owner's view, the US, safeguarding | `030-data`: rows for samples, derived conditioning, clips, consents. `050-line`: one clause. `060-code`: the standards it engages. `080-trigger`: T9, "any way for anyone but the learner to see or hear a learner's self-tutor, or obtain anything it renders", and a note on T2. `100-gaps`: a DPIA before launch |
| 06 Architecture | `075-self.html`, `<h2 id="self">Rendering the self-tutor</h2>`: capture and liveness, the likeness store, render after the gate, streaming, the still-likeness fallback, deletion, provenance | `060-data`, `080-model` (vendor rules, D65), `090-cost` (render cost Unknown), `100-harder` |
| 07 Route A | short additions in pricing (whether it is priced separately is not decided), compliance (consent, the DPIA) and distribution (no benefit claim before T-SLF-01; no real child shown without written consent) | |
| 08 Route B | one paragraph: off at launch (D67) | |
| 10 Economics | the render cost per turn as an Unknown input; price not decided | |
| 11 Roadmap | M1: counsel on OI-23 to OI-27, parents on OA-40. M2: vendor selection, T-SLF-02 to T-SLF-06. M3 and M4: T-SLF-01 (D68), in the D14 section | |
| 12 Risk register | R12 to R15 in the second tier | |
| 14 Open items | split into a directory first (it is over 3,000 words), then OI-23 to OI-27 and OA-37 to OA-40, the ledes and the pattern line | |
| Decision ledger | `049-self.html`; D9's amendment in the settled group and its record; the head | |
| 00 Thesis | `for.1` and `brief.1`: one clause each. Stay under 3,000 words | |
| Which idea goes first | the Tutor's regulatory weight row | |
| Field research | OA-40 among the parents' questions, asked as past behaviour | |
| Evidence register | CV-13 to CV-15 | |
| Contracts | heads of terms: a new schedule for the opt-in term; term sheet: one line | |
| Dependency map | the nodes below, with their tests, decisions, open items and risks in the template's tables | |

**Map nodes** (`tools/depmap/graph.json`), using the existing vocabularies:

| id | st | label | locus |
|---|---|---|---|
| `ui.selfsetup` | surface | Self-tutor setup | `01-product#self` |
| `ui.selftutor` | surface | Self-tutor | `01-product#self` |
| `eng.liveness` | engine | Liveness check | `06-architecture#self` |
| `db.likeness` | data | Likeness store | `05-safety-privacy-regulatory#self` |
| `eng.voice` | engine | Voice rendering | `06-architecture#self` |
| `eng.face` | engine | Face animation | `06-architecture#self` |
| `svc.selfdelete` | orchestration | Self-tutor deletion | `06-architecture#self` |
| `gov.selfprivate` | obligation | Self-tutor stays private | `05-safety-privacy-regulatory#trigger` |
| `gov.labelling` | obligation | Synthetic media labelling | `04-rights-dossier#self` |
| `ext.mediavendor` | supply | Speech and animation vendor | `06-architecture#model` |

## 8. Rules for this work

- British English. No em-dashes or en-dashes. Conclusions before reasoning.
- No invented figures. Seven days, sixty seconds and twelve months are design
  choices stated here; every other number comes from the evidence register or is
  marked Unknown. The latency budget, the render cost and the false-accept threshold
  are Unknown.
- Never add a Verified marker; never change an existing marker.
- Never answer a counsel question or write as if one were answered. The self-tutor
  proceeds ahead of OI-23 to OI-27 under D59's rule, and says so where it is applied,
  as D34 does for OI-3.
- The owner's views are marked as the owner's: OA-37 and OA-38.
- No benefit is claimed for the self-tutor anywhere until T-SLF-01 reports.
- Edit `src/content/`, never `docs/`, `evidence/` or `viz/`. Build and verify must
  pass.

## 9. Changed after the independent review, 23 October 2026

The ledger's text governs where it differs from sections 4 and 6 above. The review led
to these changes:

- **D60** now puts the self-tutor behind a passcode the learner sets, because learners
  have no sign-in of their own and their sessions sit under the adult's account. Every
  page promises only what the product shows. Whether a parent's subject access request
  reaches the scan and sample is part of OI-23, including where the parent is the risk
  (D26).
- **D62**'s plain words say the product shows the self-tutor to no one else, not that
  no one can ever see it.
- **D63:** the deleting write clears the cached flag, so rendering stops at the next
  turn, and the sixty-second ceiling bounds it if the clearing fails. Rendered clips are
  never stored, so they are not in the seven-day list.
- **D64:** a safeguarding reply, and any turn the safety classifier flags, is shown as
  text from the standard tutor, never in the learner's likeness.
- **D68:** cohorts, not learners, are randomised, as D33 requires, and the interaction
  between the factors is pre-registered, because D66 offers only opted-in creators'
  presets inside the self-tutor. T-SLF-01 also reads the return rate.
- **D69:** the reason is that style is defined and tested on transcripts, not that a
  grader could hear it.
- **OI-27** also asks whether an archetype in a learner's own likeness engages anyone's
  rights but the learner's. The claim that it does not is marked as the vault's reading.
- **Online Safety Act:** the self-tutor makes the question arguable (OI-24), so under
  the trigger list's own rule it needs the duties assessment signed off before its work
  starts.
