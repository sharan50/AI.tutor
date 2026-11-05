# AI.tutor: the Primer MVP brief

Commit this file at the repository root as `PRIMER_MVP_BRIEF.md`. It records what
the owner decided on 25 October 2026 about a first build of the Primer, a
demonstration for adult testers, and turns it into instructions a fresh Claude Code
session can execute. Everything binding is in this file; nothing depends on
conversation history.

`BUILD_BRIEF.md` remains the source instruction for the vault's rules, and
`FACETS_BRIEF.md` for the Primer's design pages, P1 to P6. This brief governs the
Primer's MVP build guide (`src/content/primer-mvp.html`), the specification it
publishes for Claude Code (`mvp/primer-demo-spec.md`), and the register entries it
adds: decisions D70 to D79, assumptions OA-41 to OA-44 and candidate claims CV-16
to CV-23.

## 1. What the demo is

A web app at an unlisted address, behind a passcode, used only by adults who play a
child of 8 to 13 and ask the questions such a child would ask, out loud or typed. It
gives a short answer within seconds; explains it in three building blocks, each with
text, narration and a short video made for the question; and then asks the child
what they think, a few turns at a time, until they say it in their own words.
Sensitive and personal questions get replies written in advance and no video.

The owner builds it with Claude Code in four or five days. Its job is to support
conversations with teachers, parents and accelerators. It is not evidence about
children, it is not the built Primer of PM4, and it decides nothing about which idea
goes first.

The owner reviewed a mock-up of it on 25 October 2026, a design canvas at
<https://claude.ai/artifact/TFkTFz4RzJrM7UJsLJkZmP>, private until the owner shares
it, and removed one control from it (D75). On 26 October 2026 the owner asked for the
mock-up on the site. It is published at `/mockup/` from `mockup/index.html`, a
hand-maintained port of the canvas whose words follow the specification; where the
two differ, the specification governs.

## 2. The owner's decisions, 25 October 2026

- **Build a demonstration first:** a web demo at a private address, no accounts, used
  by adults who role-play children of 8 to 13; a wrapper around existing AI
  products; the chat answer first, and in parallel the question split into what the
  child must understand first; a prompt to think; buildable in four or five days
  with limited resources (D70).
- **Flexibility over accuracy:** no narrow topic or question list (D71).
- **Voice:** testers speak their question through a dictation model, "like Whisper"
  (D72).
- **Video explainers are a key part.** Prompts for a video model are drafted and
  sent at the same time as the short answer, one video per building block, "to show
  that this is a little bit more like what the real tool, the real product is going
  to look like", because children of that age do not read fast (D73, D74).
- **No "I already know this" control** (D75).
- **The guide** is written for the owner building with Claude Code, explicit enough
  for a hired developer, and lives in the vault as a Primer page. The owner said
  "build the guide" after these two defaults were proposed.

## 3. Defaults taken while writing

The owner did not specify these. Each is a decision the owner may keep or reverse:
the video rules (D76), safety in the demo (D77), the tools (D78) and what the demo
keeps (D79).

## 4. Decisions D70 to D79

Recorded in a new ledger section, `src/content/decision-ledger/050-mvp.html`,
`<h2 id="mvp">D70 to D79: the Primer's demonstration</h2>`, each as `<dt>` and
`<dd>` with Driven by, Rejected and Makes harder. The section of decisions not taken
moves from `050-unresolved.html` to `060-unresolved.html` so that it stays last. D70 to D75 are the owner's; D76 to
D79 were taken while writing. The last link in each entry names its owner.

- **D70.** The Primer is shown first by a demonstration, not built first: a web app
  at an unlisted address, behind a passcode, used only by adults who play a child of
  8 to 13, built by the owner with Claude Code in four or five days. It supports
  PM1's conversations; it is not PM4's built Primer, involves no child, and decides
  nothing about which idea goes first. Owner: the CEO, through P6's milestones.
- **D71.** The demo answers any question, with no topic list, and labels everything
  it generates as not checked. D44 is unchanged for the Primer itself.
- **D72.** Testers can speak their question; the recording is transcribed, shown as
  editable text and not kept by the demo. Adults only, so D50 is untouched; whether
  the Primer itself should take a child's voice is a separate decision that waits on
  OI-17.
- **D73.** The Primer is meant to explain with narrated video as well as words,
  because, in the owner's view, children of 8 to 13 do not read fast. In
  the product, D44 applies to a video as to text: it is part of a reviewed
  explanation, made in advance, never generated live for a child. Owner: the COO,
  through P3's explanation bank.
- **D74.** In the demo, each building block's video is generated live from a prompt
  drafted with the blocks, and all three start as soon as the plan is ready and the
  safety check has passed.
- **D75.** No "I already know this" control: every building block is offered in full.
- **D76.** The video rules: no words, numbers or people in the picture; the clip's own
  sound muted under the narration; one fixed style; one clip per block, eight
  seconds at 720p in 16:9, looped; a cache by concept; a daily limit of sixty video
  generations in the app, retries included; one retry for a failed clip and none for
  a slow one, then a still picture with the narration; the provider behind one
  interface.
- **D77.** Safety in the demo: a safety check before anything is shown; fixed replies
  for a tester's own life, a death or serious illness close to them, their safety and
  big subjects, with nothing sent to video; Childline and, for an adult, Samaritans in
  the UK, and Childhelp and 988 in the US, named in the reply about safety; adults
  only; a passcode on the site and on every paid call; spending capped at each
  provider and in the app. Owner: counsel.
- **D78.** The tools: Claude Opus 5.5 on Anthropic's API for every word, with
  Anthropic's refusal fallback turned on; Google's Gemini API for video (Gemini Omni
  Flash), transcription (Gemini 3.5 Transcribe) and narration (Gemini 3.8 Flash-Lite
  TTS); Netlify for hosting, functions and storage. All on their standard terms,
  without the zero retention D24 makes a gate for the Primer's vendors: a departure
  for the demo alone. The choice binds the demo only; the product's model vendor
  stays deliberately undecided.
- **D79.** The demo keeps no record of who asked what: no accounts, no recordings,
  no conversation logs; only generated material in its cache, by concept, each day's
  short answers until the day ends, and timings and counts without content. Owner:
  counsel.

## 5. Register entries

**Assumptions**, under "The Primer" in `14-open-items/020-assumptions.html`, each
marked new:

- **OA-41.** That a block's video arrives within the 40 to 90 seconds the design
  targets. Resolved on day one by generating clips.
- **OA-42.** That the owner's paid Gemini API project allows the demo's daily limit
  of video generations. Resolvable by reading the project's limits in AI Studio.
- **OA-43.** That audio sent to Google for transcription is held only as Google's
  paid-tier terms describe, so that the welcome page's account of a tester's voice
  stays true end to end. Resolvable by reading the terms.
- **OA-44.** That one person working with Claude Code can build the demo in four or
  five days. The owner's estimate and the guide's premise.

The lede gains the four; the pattern line becomes nineteen of the forty-four, with
OA-42 and OA-43 among the readings.

**Candidates**, in `sources/080-candidates.html`, found 25 October 2026:

- **CV-16.** Google shut down the Veo 3.1 preview models in the Gemini API on 22
  October 2026 and recommends Gemini Omni Flash, or the generally available Veo
  models on its Gemini Enterprise Agent Platform.
- **CV-17.** Gemini Omni Flash (`gemini-omni-1.1-flash`) is generally available on the
  Gemini API's paid tier: clips of 3 to 10 seconds with native audio, 360p to 4K,
  16:9 or 9:16, through the Interactions API.
- **CV-18.** Its video output is priced at $17.50 per million tokens, with 720p
  counted at 5,792 tokens a second, about $0.10 a second; Veo 3.1 Fast on Google
  Cloud, video without audio, is listed at $0.08 a second at 720p.
- **CV-19.** Gemini 3.5 Transcribe and Gemini 3.8 Flash-Lite TTS: availability, prices,
  and the TTS model's WAV output.
- **CV-20.** Gemini API billing: project spend caps that can be overshot; paid-tier
  data kept out of Google's product improvement; a prepayment to upgrade.
- **CV-21.** Claude Opus 5.5's prices, the Claude API's spend limits, and its refusal
  fallback.
- **CV-22.** Netlify's limits for functions, background functions and Blobs, Blobs'
  consistency, rate limits on functions, and how credits are counted and spent.
- **CV-23.** NotebookLM's Video Overviews have no public API.

No counsel question is added. No test identifier is added: the demo's checks are
build checks, not tests of the Primer.

## 6. What the research changed

- The design named Veo 3.1 Fast on the Gemini API. Google had shut down the Veo 3.1
  preview models there three days earlier (CV-16), which the research behind the
  design missed. The guide uses Gemini Omni Flash, with Veo on Google Cloud as the
  fallback behind the same interface.
- The owner named Whisper. Google's Gemini 3.5 Transcribe does the same job on the
  account the demo already needs (CV-19); Whisper stays a drop-in alternative.
- The design said Google's budgets warn without stopping spend. The Gemini API now
  has project spend caps, which can be overshot by billing lag (CV-20); the app's own
  daily limit is still the one that bites first.
- Netlify's own coding context, read through its connector, showed that Blobs has no
  concurrency control and that a failed background function is retried twice; the
  daily limits are therefore kept as slots, and the background function never throws.
- The Gemini API, Netlify and OpenAI documentation pages could not be opened from the
  build environment; their claims were read through search summaries of those pages.
  Google Cloud's pricing page and Anthropic's documentation were opened directly, and
  Netlify's coding context through its connector.

## 7. Where each part goes

- **The page,** `src/content/primer-mvp.html`, unnumbered, in the Primer group, under
  3,000 words: `#what`, `#flow`, `#video`, `#stack`, `#safety`, `#costs`, `#before`,
  `#days`, `#testing`, `#limits`. Owned by the CTO, except `#safety` (counsel) and
  `#costs` (the CFO).
- **The specification,** `mvp/primer-demo-spec.md`, hand-maintained, published at
  `/mvp/` as text, as the contracts are. The owner saves it as `CLAUDE.md` in the
  demo's own repository.
- **The mock-up,** `mockup/index.html`, hand-maintained, published at `/mockup/`.
  It runs one script, which its own policy names by hash, as the map's does, and
  loads nothing but its fonts. It is owned by the CTO, and linked from the guide and
  the front page's Primer card. Nothing on it may suggest that anything is built,
  generated or checked.
- **The build:** `PAGES` and `GROUPS` gain the page; `PUBLISHED` gains `mvp`; the
  headers serve `/mvp/*` as text.
- **Design pages:** P2 `#session` and P3 `#bank` gain D73's video; P6 `#milestones`
  gains a sentence placing the demo beside PM1.
- **Registers:** the ledger section and its head; the open items; the candidates and
  their note.
- **Shared pages:** the contents page's investor route names the guide; the front
  page's Primer card links it.
- **Ownership:** `roles.json` gives the page to the CTO with the two sections above,
  and the frames of the CTO, the CFO, counsel and the COO each gain a clause.
- **Root files:** README (counts and layout), CLAUDE.md (map and page ranges),
  netlify.toml (comments), and `PRIMER_MVP_REPORT.md` when the work is done.

## 8. Rules for this work

1. D1 to D69 stand. The demo departs from D24 and D44 for itself only and says so
   wherever it does; D50 is untouched, because only adults use it; the Primer's
   design changes only by D73.
2. Counsel questions OI-1 to OI-27 stay open and none is written as answered. Taking
   adults' voices settles nothing about OI-17.
3. House style is `BUILD_BRIEF.md` section 7: British English, no em-dashes or
   en-dashes, conclusions before reasoning, and weak things called weak.
4. Every number on the page is from the evidence register, a stated design choice,
   or marked Unknown. A provider's price, latency or limit is a candidate (D53) and
   carries an Assumed marker naming it. No Verified marker is added; no existing
   marker is changed.
5. Edit `src/`, `roles.json`, root files and `mvp/`; never `docs/`, `evidence/` or
   `viz/` by hand. Python 3 standard library only.
6. Nothing may suggest the demo shows how children engage or learn, or that its
   answers are accurate. No real child is shown, and no child is invited to use it.
7. Nothing may name a model vendor for the Primer itself.

## 9. Acceptance bar

1. `python3 src/build.py` and `python3 tools/verify.py` pass.
2. Every existing marker in every edited file is unchanged, in order.
3. No dashes and no American spellings in anything new, apart from code and URLs.
4. The page is under 3,000 words; the front page and the Tutor summary stay within
   their caps.
5. Every touched page fits at 390 px and 1280 px.
6. An independent review, given the rules and the change but not the conversation,
   finds nothing blocking, or every finding is fixed and recorded in the report.
