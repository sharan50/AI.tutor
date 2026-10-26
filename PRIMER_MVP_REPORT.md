# PRIMER_MVP_REPORT

What `PRIMER_MVP_BRIEF.md` changed, the checks it passed, and what the independent
review found. Written 25 October 2026.

## 1. Outcome

The Primer has a build guide for a demonstration. It is a web app for adults who
play a child of 8 to 13, and the owner can build it with Claude Code in four or five
days (OA-44). The guide is a Primer page, `primer-mvp.html`. The specification that
Claude Code builds from is published beside it at `/mvp/primer-demo-spec.md`, to be
saved as `CLAUDE.md` in the demo's own repository.

Three things did not happen:
- No counsel question was answered. Taking adults' voices settles nothing about
  OI-17.
- No Verified marker was added, and no existing marker was changed.
- Nothing says the demo shows how children engage or learn, or that its answers are
  accurate, and no model vendor is named for the Primer itself.

The Primer's design changes in one place only. Under D73 it explains with narrated
video as well as words, and a video is part of a reviewed explanation, made in
advance. The demo departs from D24 and D44 for itself only, and says so where it
does; D50 is untouched, because only adults use it.

The video model the design named had been withdrawn three days before (CV-16). The
guide uses Gemini Omni Flash instead, with the generally available Veo models on
Google Cloud as the fallback behind the same interface.

Counts after this work, computed by the build:

| | |
|---|---|
| Documents | 31 |
| Decisions | 79: 14 settled (two since amended by the owner), 65 taken |
| Counsel questions | 27, none answered |
| Assumptions | 44, of which 19 are resolvable by reading or asking |
| Tests specified | 32, none run |
| External claims | 42 registered, plus 23 candidates awaiting the owner's check |

## 2. The owner's decisions and the defaults

**The owner's decisions, 25 October 2026:**
- **D70.** The Primer is shown first by a demonstration for adult testers, built in
  four or five days.
- **D71.** It answers any question, with no list of topics, and labels everything it
  generates as not checked.
- **D72.** Testers can speak their question.
- **D73.** The Primer is meant to explain with narrated video; in the product a video
  is reviewed and made in advance.
- **D74.** In the demo, every block's video is generated live and starts as soon as
  the plan is ready and the safety check has passed.
- **D75.** No "I already know this" control, removed after the owner saw the
  mock-up.

**Taken while writing, for the owner to keep or reverse:**

| | Decision |
|---|---|
| D76 | The video rules: pictures only, one style, one eight-second clip per block, a cache by concept, a daily limit of sixty video generations with retries counted, one retry for a failed clip and none for a slow one, then a still picture, and the provider behind one interface |
| D77 | Safety in the demo: a safety check before anything is shown; replies written in advance for five kinds of message, the one about safety naming Childline and Samaritans in the UK and Childhelp and 988 in the US; adults only; a passcode on the site and every paid call; and spending capped at each provider and in the app |
| D78 | The tools: Claude Opus 5.5 for every word, with Anthropic's refusal fallback on; Gemini Omni Flash, Gemini 3.5 Transcribe and Gemini 3.8 Flash-Lite TTS on Google's Gemini API; Netlify for hosting. All on their standard terms, without D24's zero retention, for the demo alone |
| D79 | No record of who asked what: no accounts, recordings or conversation logs; only the cache by concept, each day's short answers until the day ends, and timings and counts without content |

## 3. What was added

- **The guide,** `src/content/primer-mvp.html`: what the demo is; one question from
  start to finish, with target times; the video rules; the tools and why; safety,
  privacy and the testers; the costs and the three caps; the accounts to open before
  day one; the five days; the role-play sessions; and what the demo cannot show.
- **The specification,** `mvp/primer-demo-spec.md`: the rules that never change; the
  stack and its settings; the look and the screens; the request flow; every model
  call with its system prompt and schema; the video jobs and their two paths; the
  replies written in advance, as drafts for the owner to approve; the functions; the
  failures; the build order day by day, with its checks; and the final checklist.
- **Design pages.** P2's session names the video in the factual part (D73). P3's
  explanation bank holds a narrated video as part of an entry, at a cost that is
  Unknown. P6's milestones place the demo beside PM1 (D70).
- **Registers.**
  - Decisions D70 to D79 in a new ledger section; the section of decisions not taken
    moves from `050-unresolved.html` to `060-unresolved.html`, unchanged, so that it
    stays last.
  - Assumptions OA-41 to OA-44, with OA-42 and OA-43 resolvable by reading.
  - Candidates CV-16 to CV-23: the providers' models, prices and limits, and
    NotebookLM.
- **Shared pages.** The contents page's investor route names the guide, and the
  front page's Primer card links it.
- **Ownership.** The CTO owns the page and `mvp/`, the CFO the page's costs and
  counsel its safety section. The frames of the CTO, the CFO, counsel and the COO
  each gain a clause.
- **The build.** `PAGES` and `GROUPS` gain the page; `PUBLISHED` gains `mvp`; the
  headers serve `/mvp/*` as plain text, as the contracts are; CODEOWNERS covers
  `mvp/` as it does `contracts/`.
- **Root files.** README (counts and layout), CLAUDE.md (map and page ranges) and
  `netlify.toml` (comments).

The mock-up the owner reviewed is a design canvas, private until the owner shares it,
at <https://claude.ai/artifact/TFkTFz4RzJrM7UJsLJkZmP>. It is not in the repository.

## 4. What the research changed

- **The video model.** The design named Veo 3.1 Fast on the Gemini API, whose preview
  models Google shut down on 22 October 2026 (CV-16). The guide uses Gemini Omni
  Flash (CV-17), with Veo on Google Cloud as the fallback.
- **Speech to text.** The owner named Whisper. Gemini 3.5 Transcribe does the same
  job on the account the demo already needs (CV-19), so the demo has three accounts,
  not four. Whisper stays a drop-in alternative.
- **Spend caps.** The design said Google's budgets warn without stopping spend. The
  Gemini API now has project spend caps, which billing lag can overshoot (CV-20). The
  app's own daily limit is still the one that bites first.
- **What could not be opened.** The Gemini API's, Netlify's and OpenAI's
  documentation could not be reached from the build environment, so their claims
  were read through search summaries of those pages, and each candidate row says
  so. Google Cloud's pricing page and Anthropic's documentation were read directly,
  and Netlify's coding context for functions and Blobs through Netlify's connector.

## 5. Checks run, and what each returned

| Check | Result |
|---|---|
| `python3 src/build.py` | Exit 0 |
| `python3 tools/verify.py` | All checks pass: build fresh, 4,205 links in 42 files with none broken, map loci resolve (100 nodes, 191 edges), no view or ownership problems |
| Existing markers | Every marker in every edited source matches `main`; the work only adds markers |
| Verified markers added | None |
| Dashes and American spellings in anything new | None, apart from code (the `Authorization` header) |
| Line endings | Unchanged in every edited file |
| Page size | The guide is 2,984 words by the build's own counter, under the 3,000-word limit; the front page and the Tutor summary stay within their caps |
| Rendering | Every touched page fits at 390 px and 1280 px with no failed request |
| Deploy preview | Netlify's deploy preview, header rules and redirect rules passed on the first push |

## 6. The independent review

A fresh agent was given the rules and the change but none of the conversation, and
read everything the work touched. It found 2 blocking problems, 12 that should be
fixed and 11 nits. It also confirmed:
- every count is right wherever it appears;
- ownership resolves as the brief says;
- no Verified marker was added and no existing marker changed;
- no counsel question is resolved and no settled decision reopened;
- the Claude API usage matches the current reference;
- CV-18 and CV-19 match Google Cloud's pricing page, which it opened directly, and
  the arithmetic holds.

Every finding was checked against the files and, where it named an outside fact,
against the source. All were fixed.

| # | Finding | What was done |
|---|---|---|
| B1 | Text relying on candidates had no Assumed marker: D70, D76, D77 and D78 in the ledger, OA-42, and the two figures in the guide's caps box worked out from a candidate price | Each now carries an Assumed marker naming its candidate, as the ledger's earlier sections do |
| B2 | The specification could show the plan and start the videos before the safety check passed, whenever the plan returned first | The plan waits for whichever comes later, itself or the check; D74 now says the videos start once both hold |
| S3 | The ledger and the brief said the demo departs from D50, which D72 and the guide call untouched; nothing said the providers are not held to D24's zero retention | The demo departs from D24 and D44 for itself only, and says so in D78, the guide and the brief; D50 is untouched |
| S4 | The refusal fallback contradicted "one model for every word", and a refusal mid-stream left shown text in place | The fallback stays, as Anthropic's documentation recommends, and D78, the guide and CV-21 now say so. A refusal replaces everything shown for the question |
| S5 | Narration was both made in advance and made only when Listen was first pressed | The browser requests each narration as its block arrives |
| S6 | Testers were told their recording is deleted, which OA-43 leaves open; no card said where typed words go; "no audio" sat beside stored audio and short answers with no expiry | The Ask screen says the demo does not keep the recording; a welcome card says where words go; the rule is "no recordings"; short answers are deleted at the end of each day, as D79 now says |
| S7 | The pattern paragraph said the field research guide covers all nineteen readings, and that all of them are in M1 and PM1 | OA-42 and OA-43 are named as the demonstration's tasks before its first day |
| S8 | Retries were not counted against the daily video limit, and a day of six sessions needs more than sixty videos | Every request counts, a slow clip is never retried, and the guide holds at most four sessions a day at the default limit |
| S9 | Nothing kept `/api/ask` inside Netlify's 60-second limit; Blobs is eventually consistent by default; the demo would share this site's Netlify credits | A 50-second deadline with the SDK's retries off; strong consistency for jobs and slots; the demo on a team of its own if the account allows, or auto recharge, and one production deploy a day. CV-22 records the limits, the rates and the team-wide pause |
| S10 | The speech model is a preview, which the guide did not say | Said, with the browser's own voice as the fallback |
| S11 | The UK safety reply suited only a child, though every tester is an adult | Samaritans, which 05 names beside Childline, is added for an adult (D77) |
| S12 | The passcode could be guessed | Four or more random words, compared in constant time, behind Netlify's rate limit of ten attempts a minute per address |
| S13 | "Children of 8 to 13 read slowly" was stated as fact | Attributed to the owner, in D73 and the guide |
| S14 | Structured output cannot hold an array to exactly three items | The plan's three blocks and two replies are named fields |

The nits were fixed:
- the system prompts are too short to cache, so the spec no longer asks for caching;
- the guide and D77 now name serious illness and pets, as the safety check does;
- the thinking turns ask for the child's own words after three exchanges, so the
  four-turn check holds;
- CV-12, CV-19 and CV-21 list where they are used, and the text claims no more than
  its candidates record;
- this report exists, and the guide's "reviewed once independently" is now true;
- narration is fetched with the token and played from an object URL;
- the short answer's target is "a few seconds";
- the owner checks every number in the replies, not only the US ones;
- `mvp/` is owned by the CTO, with a CODEOWNERS line;
- `#limits` and D77 say that nothing checks what Claude writes beyond its
  instructions and the labels;
- tickets sign the plan's thinking part and the conversation so far.

Two more problems came to light while fixing these, from Netlify's own coding
context:
- **Blobs has no concurrency control,** so a daily count kept on one key undercounts
  when three videos start at once. The daily limits are now slots, each a key created
  only if new.
- **Netlify retries a failed background function twice by itself,** which would make
  videos that no slot counted. The background function now records every error and
  never throws.

## 7. What is left for the owner

- **Keep or reverse D76 to D79.**
- **Approve the replies written in advance** in the specification's section 8, and
  check every number in them, before any tester uses the demo. The UK numbers come
  from 05; the US numbers are CV-12.
- **Check candidates CV-16 to CV-23** and promote those that hold. The Gemini API's
  and Netlify's pages were read through search summaries, not opened.
- **Read the Gemini project's video limit** in AI Studio (OA-42), and Google's terms
  on audio sent for transcription (OA-43).
- **Decide where the demo is hosted on Netlify.** Netlify's API lists one team on the
  account, of type Personal, and it hosts this site. Credits are counted by team, and
  a team that runs out pauses every project on it (CV-22). Give the demo a team of its
  own if the account allows, or turn on auto recharge with a limit while it is in use.
- **Share the mock-up or export its screens,** so that Claude Code can match it from
  day 2.
- **Day one answers OA-41,** how long a video takes, and decides which path the video
  jobs use.
