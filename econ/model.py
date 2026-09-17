# === SECTION: HEADER ===
"""
AI.tutor economic instrument.

This is not a forecast. It is an instrument for ranking levers under stated
ignorance. Every driver is sampled from a prior. No level in the output is
evidence of anything; only the ordering of the drivers is what a simulation on
priors is good for.

Seed: 20260916. Paths: 20000. Horizon: 60 months. Currency: USD.
Run date stamped into every output: see RUN_DATE.

Section markers below are load-bearing: harness.py splits this file on them and
executes the pieces, so that everything downstream runs this code rather than a
restatement of it.
"""

import csv
import io
import math
import os

import numpy as np
from scipy import special

SEED = 20260916
RUN_DATE = "2026-09-16"
N_PATHS = 20000
HORIZON = 60

# Auxiliary seeds. Anything a variant needs that the published base run does not
# draw must come from one of these, never from the published stream, or the two
# runs stop being comparable path by path.
SEED_AUX_FEEDBACK = 771020260916
SEED_AUX_DEPENDENCE = 771120260916
SEED_AUX_FX = 771220260916
SEED_AUX_APPSTORE = 771420260916
SEED_AUX_CREATOR = 771520260916
SEED_AUX_RESIDUAL = 771620260916

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# === SECTION: CONSTANTS ===
# ---------------------------------------------------------------------------
# Fixed FX. The owner's instruction is a USD model with fixed rates where an
# item was originally quoted in GBP or INR. FX_GBP_USD is therefore a decision,
# not a draw, and checklist item 4 is not clean by construction. The
# por_fx_sampled scenario in variants.py re-runs with the POUND rate sampled and
# the write-up publishes the delta rather than claiming the exposure away.
#
# FX_INR_USD is a DEAD CONSTANT and is kept only because out/constants.csv
# publishes it and the write-up's own description of the model refers to it. No
# line in this file reads it: Bengaluru salaries and support are drawn directly
# in dollars from their own priors, so the rupee exposure has no term at all
# rather than a fixed one. An earlier comment here claimed both rates were
# sampled in the scenario. Neither statement was true. See CHANGELOG 4.4.
# ---------------------------------------------------------------------------
FX_GBP_USD = 1.27          # USD per GBP
FX_INR_USD = 1.0 / 86.5    # USD per INR, read by nothing in this file

# ---------------------------------------------------------------------------
# Consumption tax. Quoted consumer prices are read as GROSS, i.e. tax-inclusive,
# which is what UK B2C law requires a consumer-facing price to be. Net revenue
# is price / (1 + rate). The write-up quantifies the other reading, in which the
# quoted price is net and roughly a sixth more revenue exists.
# ---------------------------------------------------------------------------
VAT_UK = 0.20              # UK VAT on B2C digital services
GST_IN = 0.18              # Indian GST on OIDAR services
# US has no federal rate and state treatment of SaaS varies; sampled driver.

# ---------------------------------------------------------------------------
# Calendar. t = 0 is the month the seed closes. Base plan sets t=0 to March 2027
# so that the go-to-market at t=6 lands in September, the start of the academic
# year. Launch month is a decision the owner owns; swept separately.
# ---------------------------------------------------------------------------
START_YEAR = 2027
START_MONTH_IDX = 2        # 0 = January, so 2 = March

def cal_month(t):
    """Calendar month index 0..11 for horizon month t."""
    return (START_MONTH_IDX + t) % 12

def cal_year(t):
    return START_YEAR + (START_MONTH_IDX + t) // 12

# ---------------------------------------------------------------------------
# Markets and segments.
#
# India consumer is present in the array at all times but carries zero
# acquisition budget in the published run. DPDP Rules 2025 s.9(3) prohibits
# tracking, behavioural monitoring and targeted advertising directed at anyone
# under 18 independent of consent, and a parent cannot waive it; children's-data
# obligations bite around May 2027, inside this horizon. The India pilot is
# therefore modelled through the institution channel. Keeping the market in the
# array with a zero budget means variant_india_d2c() switches it on without the
# random stream diverging (checklist item 11).
# ---------------------------------------------------------------------------
MARKETS = ["UK", "US", "IN", "ROW"]
SEGMENTS = ["PRE", "EXAM", "ALEVEL"]
NM = len(MARKETS)
NS = len(SEGMENTS)
MS = NM * NS
# Cohort-year slots in the stock and arrivals arrays. A sixty-month horizon
# reaches t // 12 == 4, so a sixth slot was allocated in every month of every
# path and was permanently zero: one sixth of two of the largest arrays in the
# model, standing for a cohort year the horizon cannot reach.
N_COHORT_YEARS = 5

M_UK, M_US, M_IN, M_ROW = 0, 1, 2, 3
S_PRE, S_EXAM, S_ALEVEL = 0, 1, 2

def ms(m, s):
    return m * NS + s

# Month of the calendar year in which the terminal examination sitting ends,
# per market. UK GCSE/A-level finish in June; US AP sittings are in May; Indian
# board examinations finish in March.
EXAM_CAL_MONTH = {M_UK: 5, M_US: 4, M_IN: 2, M_ROW: 5}

# Consumer market opening months in the plan of record.
# India's month is real, not infinity: the india_d2c switch is what closes it in
# the published run, so that turning the switch on actually opens the market.
CONSUMER_OPEN = {M_UK: 6, M_US: 15, M_IN: 15, M_ROW: 24}

# Institution (Route B) channel opening month. The institution channel is
# modelled as ONE United Kingdom-priced motion, not per market, so this carries
# the United Kingdom only. Entries for the other markets were dead constants:
# _school_open_month is never called with anything else, and the seat price has
# no market index.
SCHOOL_OPEN = {M_UK: 12}

# ---------------------------------------------------------------------------
# Content scope, in units. A unit is one (subject x level x board).
# At go-to-market: 5 subjects (Maths, English, Biology, Chemistry, Physics),
# GCSE only, one board. By month 18: 5 subjects x 2 levels x 4 UK boards = 40.
# The 600-item figure in docs/03 is one strand of one subject, so items per full
# unit is an extrapolation and is sampled wide rather than asserted.
# ---------------------------------------------------------------------------
GTM_MONTH = 6

UK_UNIT_SCHEDULE = [
    # (month, subjects, levels, boards) cumulative target
    (6,  5, 1, 1),
    (10, 5, 1, 2),
    (13, 5, 2, 2),
    (16, 5, 2, 3),
    (18, 5, 2, 4),
    (30, 7, 2, 4),
    (42, 9, 2, 4),
    (54, 11, 2, 4),
]
US_UNIT_SCHEDULE = [(15, 5, 1, 1), (24, 5, 2, 2), (40, 7, 2, 2)]
IN_UNIT_SCHEDULE = [(15, 5, 2, 1), (26, 5, 2, 2), (44, 7, 2, 2)]
ROW_UNIT_SCHEDULE = [(24, 5, 1, 1), (34, 5, 2, 2), (48, 7, 2, 3)]

UNIT_SCHEDULES = {
    M_UK: UK_UNIT_SCHEDULE,
    M_US: US_UNIT_SCHEDULE,
    M_IN: IN_UNIT_SCHEDULE,
    M_ROW: ROW_UNIT_SCHEDULE,
}

# The go-to-market minimum: the five subjects of the brief, GCSE only, one
# board, United Kingdom only, and never widened. This is the floor of the scope
# ladder. It is defined here rather than in the scripts because two of them use
# it and a second copy would be free to drift from the first. It is never read
# by the published run: base_config() leaves unit_schedules at None.
GTM_MINIMUM_SCHEDULES = {
    M_UK: [(GTM_MONTH, 5, 1, 1)],
    M_US: [],
    M_IN: [],
    M_ROW: [],
}

# ---------------------------------------------------------------------------
# Commercial decisions taken here, so that the revenue line matches a pricing
# decision rather than being users times price.
# ---------------------------------------------------------------------------
SESSION_ALLOWANCE = 16.0   # included sessions per active household per month
OVERAGE_CAP_MULT = 2.5     # billed overage capped at this multiple of allowance

# Acquisition budget rule. A cap is mandatory: uncapped spend through a
# saturating channel eventually buys customers for more than they are worth.
CAC_LTV_CAP = 0.75         # never spend so that effective CAC exceeds this x LTV

# How many times over the reachable pool may be worked across the whole horizon.
# A household that churns can be sold to again; it cannot be sold to without
# limit. Without this the standing-book cap left cumulative acquisitions
# unbounded and the best paths bought tens of millions of households in a market
# of a few million.
# It does two jobs, and both are load-bearing: it bounds cumulative acquisitions
# AND it is the denominator of the saturation term, so it sets how fast the
# effective cost of acquisition rises. A single number doing two jobs is worth
# being able to vary, so base_config() carries pool_reacq_multiple; None means
# this published value and the switched-off case reproduces the base run.
POOL_REACQUISITION_MULTIPLE = 3.0

# The launch acquisition subsidy is not revenue-linked, so it must switch off.
# It holds for a year after go-to-market and tapers to nothing over the second,
# after which acquisition is funded only from trailing revenue. A standing
# subsidy that never switches off is not a budget rule, and it was one until
# this was added.
ACQ_RAMP_HOLD_MONTHS = 12
ACQ_RAMP_TAPER_MONTHS = 12

# Signed creators, under D14, which requires named presets shipped from day one.
# The published run carries NO creator cost, because D5 describes a one-page
# name-and-likeness agreement and the vault has never tested whether a creator
# signs one for nothing. That is an assumption, not a finding, and
# variant_creator_fees() prices what it costs if they want money.
CREATOR_RAMP = [(6, 3.0), (18, 8.0), (30, 15.0), (48, 25.0)]

# Platform engineering above the floor: heads per additional live consumer
# market, and heads for running the institution channel at all.
PLATFORM_PER_EXTRA_MARKET = 1.5
PLATFORM_FOR_INSTITUTIONS = 2.0

# The reachable pool driver is defined for the five-subject go-to-market scope.
# A product covering one subject reaches fewer households than one covering
# eleven, sublinearly. Without this a narrow scope was credited the whole pool
# while being charged only its own content, which is the same like-for-like
# defect as the platform ramp, running the other way (see CHANGELOG.md 0.9).
POOL_BREADTH_REFERENCE_SUBJECTS = 5.0
POOL_BREADTH_EXPONENT = 0.6

# The app store commission applied by variant_appstore(). This is the small
# business rate; the headline rate is double it, and LIMITS.md says the scenario
# uses the lower one on every path including the large ones.
APPSTORE_FEE = 0.15

# The demand multiplier BELOW which a month counts toward a bad run. Strictly
# below: the test at the call site is `shock_mult < SHOCK_BAD_THRESHOLD`, and
# this comment said "at or below" until a review read the two together.
SHOCK_BAD_THRESHOLD = 0.80

# Safeguarding rota thresholds, in active consumer households.
ROTA_EXTENDED_AT = 3000
ROTA_24_7_AT = 25000

# === SECTION: DRAWS ===
# ---------------------------------------------------------------------------
# The driver registry. Every entry is a prior. Not one of them is a measurement.
# The order of this list is the order of draws from the published stream and
# must not be reordered, because every variant depends on drawing the same
# numbers in the same order so that paths stay matched.
#
# note: what the range is anchored on. "prior" means nothing anchors it.
# ---------------------------------------------------------------------------
DRIVERS = [
    # --- price and the anchor regime (condition C1 in docs/09) -------------
    ("anchor_u", "u", (0.0, 1.0),
     "uniform used to draw the price-anchor regime; see P_TUTORING_ANCHOR"),
    ("price_uk_tut_gbp", "tri", (14.0, 22.0, 42.0),
     "gross monthly GBP if parents anchor on tutoring; docs/07 substitution table against verified 25-45 GBP/hr"),
    ("price_uk_sw_gbp", "tri", (3.5, 7.0, 13.0),
     "gross monthly GBP if parents anchor on software; prior, no anchor in the vault"),
    ("price_rel_us", "u", (0.85, 1.45), "US price relative to UK, prior"),
    ("price_rel_in", "u", (0.10, 0.32), "India price relative to UK, prior"),
    ("price_rel_row", "u", (0.55, 1.05), "rest-of-English-speaking price relative to UK, prior"),
    ("price_drift_yr", "n", (0.015, 0.030), "annual real price drift, prior"),
    ("overage_price_frac", "u", (0.55, 1.45),
     "overage price per session as a fraction of (plan price / allowance), prior"),

    # --- usage -------------------------------------------------------------
    ("sessions_per_hh_month", "u", (3.5, 18.0),
     "mean sessions per active household per month. docs/03's own arithmetic, three sessions a week for a Year 11 revising one strand, is about 13 a month; the top of this range is above that and the bottom well below it, because nothing measures this before M5"),
    ("sessions_cv", "u", (0.55, 1.60), "coefficient of variation of sessions across households, prior"),
    ("usage_season_amp", "u", (0.10, 0.55), "seasonal swing in sessions per household, prior"),

    # --- retention and the examination calendar ----------------------------
    ("churn_base", "u", (0.030, 0.180), "voluntary monthly churn in season, prior"),
    ("churn_m1_extra", "u", (0.04, 0.32), "additional churn in the first month, prior"),
    ("summer_lapse_pre", "u", (0.20, 0.85),
     "probability a pre-examination-year household lapses across July and August; this is OA-21, the assumption the Year 10 doubling rests on"),
    ("progress_continue", "u", (0.65, 0.98),
     "of pre-examination households that survive the summer, the share that continue into their examination year, prior"),
    ("alevel_continue", "u", (0.02, 0.22),
     "share of GCSE examination-year households continuing to A-level, prior"),
    ("alevel_exit_rate", "u", (0.35, 0.72), "share of A-level stock exiting at each A-level sitting, prior"),
    ("exam_carryover", "u", (0.00, 0.10),
     "share of examination-year households that do not leave at the sitting, prior"),

    # --- inference cost ----------------------------------------------------
    ("turns_per_session", "u", (8.0, 30.0), "turns per session, prior; docs/06 bounds context per turn but not turn count"),
    ("tok_in_per_turn", "u", (2500.0, 9000.0), "bounded input tokens per turn under D30, prior"),
    ("tok_out_per_turn", "u", (250.0, 900.0), "output tokens per turn, prior"),
    ("price_in_mtok_usd", "lu", (0.15, 3.00), "USD per million input tokens, prior; docs/06 deliberately declines to write vendor prices from memory"),
    ("price_out_mtok_usd", "lu", (0.60, 15.0), "USD per million output tokens, prior"),
    ("verify_overhead", "u", (0.12, 0.85), "verifier cost as a multiple of generation, prior"),
    ("gate_fire_rate", "u", (0.02, 0.28), "share of generations discarded by the gate, prior; docs/06 instruments this at M2"),
    ("infer_decline_yr", "u", (0.08, 0.55), "annual decline in unit inference price, prior"),

    # --- other variable cost ----------------------------------------------
    ("support_min_hh_month", "u", (0.4, 6.0), "human support minutes per active household per month, prior"),
    ("support_usd_hr", "u", (3.0, 9.5), "loaded Bengaluru support cost per hour, INR-quoted, stated as its USD equivalent at the fixed rate, prior"),
    ("pay_pct", "u", (0.019, 0.037), "payment processing percentage, prior"),
    ("pay_fixed_usd", "u", (0.18, 0.45), "payment processing fixed fee per charge, prior"),
    ("hosting_hh_usd", "u", (0.04, 0.60), "retrieval, storage and telemetry per active household per month, prior"),
    ("verif_cost_usd", "lu", (0.12, 7.00),
     "age assurance per verified adult; open item OI-5 and condition C2, deliberately spanning two orders of magnitude because nothing anchors it"),

    # --- content and examiner validation -----------------------------------
    ("minutes_per_item", "u", (4.0, 30.0), "examiner validation minutes per item; docs/03 names the 5-fold spread explicitly as unknown"),
    ("examiner_rate_gbp_hr", "u", (22.0, 78.0), "examiner contract rate per hour, GBP, prior"),
    ("writer_gbp_item", "u", (5.0, 36.0), "authoring cost per item, GBP, prior"),
    ("items_per_unit", "u", (1800.0, 6000.0),
     "items per subject x level x board; docs/03's 600 is one strand of one subject, so this is an extrapolation"),
    ("board_reuse", "u", (0.50, 0.92),
     "share of items reused when the same subject and level is taken to a second UK board; if this were near 1 the expansion case would be getting for free the thing it is asking to buy"),
    ("market_reuse", "u", (0.10, 0.60), "share of items reused when a subject crosses to a foreign curriculum, prior"),
    ("reval_frac_yr", "u", (0.04, 0.28), "share of the live bank revalidated each year, prior"),

    # --- people ------------------------------------------------------------
    ("eng_usd_yr", "u", (14000.0, 45000.0), "Bengaluru engineer base, INR-quoted, stated as its USD equivalent at the fixed rate, prior"),
    ("uk_gbp_yr", "u", (45000.0, 98000.0), "UK-based role base (safeguarding, sales, DPO) in GBP, prior"),
    ("overhead_mult", "u", (1.12, 1.48), "employer cost multiplier over base, prior"),
    ("units_per_content_head", "u", (0.5, 2.6), "content units one content head can build and maintain per year, prior"),
    ("eng_ramp_mult", "u", (0.7, 1.6), "multiplier on the engineering headcount ramp, prior"),

    # --- acquisition -------------------------------------------------------
    ("cac_anchor_usd", "lu", (8.0, 130.0),
     "UK cost per acquired household at low volume; this is an anchor, not an effective cost at scale"),
    ("cac_rel_us", "u", (0.9, 2.4), "US CAC anchor relative to UK, prior"),
    ("cac_rel_in", "u", (0.15, 0.8), "India CAC anchor relative to UK, prior"),
    ("cac_rel_row", "u", (0.6, 1.8), "rest-of-English-speaking CAC anchor relative to UK, prior"),
    ("sat_kappa", "u", (0.12, 0.80),
     "channel saturation exponent: effective CAC scales as (spend / reference spend) ** kappa"),
    ("cac_ref_spend_usd", "lu", (2500.0, 70000.0), "monthly spend at which the anchor CAC holds, prior"),
    ("pool_pressure_psi", "u", (0.25, 1.60), "how hard CAC rises as the reachable pool is penetrated, prior"),
    ("creator_share", "u", (0.0, 0.60), "share of acquisitions arriving through a signed creator's audience, prior"),
    ("creator_cac_rel", "u", (0.15, 0.95), "creator-led CAC relative to non-creator CAC, prior"),
    ("pool_uk", "lu", (40000.0, 1200000.0),
     "reachable UK households; this number does not exist anywhere, so it is taken as an input and the break-even is published instead of a guess"),
    ("pool_rel_us", "lu", (0.8, 9.0), "US reachable pool relative to UK, prior"),
    ("pool_rel_in", "lu", (0.5, 30.0), "India reachable pool relative to UK, prior"),
    ("pool_rel_row", "lu", (0.3, 4.0), "rest-of-English-speaking reachable pool relative to UK, prior"),
    ("acq_season_amp", "u", (0.15, 0.80), "seasonal swing in acquisition, prior"),
    ("seg_mix_exam", "u", (0.40, 0.85),
     "share of acquisitions landing in the examination year; docs/07 says the two cohorts must never be blended, so the mix is a driver"),
    ("seg_mix_alevel", "u", (0.03, 0.25), "share of acquisitions landing directly in A-level, prior"),
    ("acq_pct_of_rev", "u", (0.12, 0.65), "acquisition budget as a share of trailing net revenue once revenue exists, prior"),
    ("acq_launch_ramp", "lu", (6000.0, 120000.0),
     "monthly acquisition budget at launch, before there is revenue to fund it; tapered off over the second year after launch by ACQ_RAMP_* below, because a standing subsidy that never switches off is not a budget rule"),

    # --- persistent demand shock (checklist item 18) -----------------------
    ("shock_rho", "u", (0.45, 0.95), "AR(1) persistence of the demand shock, prior"),
    ("shock_sd", "u", (0.04, 0.32), "monthly innovation standard deviation of the demand shock, prior"),

    # --- Route B, institutions --------------------------------------------
    ("school_seats", "u", (40.0, 420.0), "seats per institution contract, prior"),
    ("school_gbp_seat_yr", "u", (3.5, 32.0), "annual price per seat, GBP, prior"),
    ("school_win_rate", "u", (0.03, 0.28), "share of qualified pipeline that closes, prior"),
    ("school_rep_pipeline_yr", "u", (12.0, 60.0), "qualified institutions worked per rep per year, prior"),
    ("school_renewal", "u", (0.45, 0.92), "annual renewal rate, prior"),
    ("school_cycle_m", "u", (6.0, 18.0), "months from first contact to purchase order, prior"),

    # --- tax ---------------------------------------------------------------
    ("us_sales_tax_eff", "u", (0.0, 0.085), "effective US state sales tax on the subscription, prior"),

    # --- step costs --------------------------------------------------------
    ("step_entity_setup_usd", "u", (9000.0, 48000.0), "foreign operating entity set-up, prior"),
    ("step_entity_annual_usd", "u", (7000.0, 34000.0), "per-entity annual compliance, audit and accounting, prior"),
    ("step_cert_setup_usd", "u", (18000.0, 70000.0), "information security certification, first award, prior"),
    ("step_cert_annual_usd", "u", (9000.0, 28000.0), "certification surveillance and renewal, prior"),
    ("step_uk_rep_usd_yr", "u", (3500.0, 16000.0), "UK Article 27 representative, prior"),
    ("step_counsel_initial_usd", "u", (25000.0, 130000.0), "the counsel items in docs/14, prior. The vault is not internally consistent about how many there are: docs/14 lists OI-1 to OI-12, its README and docs/11 both say eleven"),
    ("step_counsel_market_usd", "u", (12000.0, 70000.0), "counsel per additional jurisdiction, prior"),
    ("step_office_usd_head_yr", "u", (900.0, 3600.0), "premises per head per year once premises exist, prior"),
    ("step_dpia_audit_usd_yr", "u", (8000.0, 40000.0), "DPIA maintenance and ICO-facing audit readiness, prior"),
]

DRIVER_NAMES = [d[0] for d in DRIVERS]

# The probability that a path lands in the tutoring-anchored price regime.
# This is a decision about how to weight condition C1, not a measurement, and it
# is swept in the sensitivity because it is one of the few numbers whose value
# the owner chooses rather than discovers.
P_TUTORING_ANCHOR = 0.50


def _sample(rng, kind, params, n):
    if kind == "u":
        a, b = params
        return rng.uniform(a, b, n)
    if kind == "lu":
        a, b = params
        return np.exp(rng.uniform(math.log(a), math.log(b), n))
    if kind == "tri":
        a, m, b = params
        return rng.triangular(a, m, b, n)
    if kind == "n":
        mu, sd = params
        return rng.normal(mu, sd, n)
    raise ValueError(kind)


def draw_drivers(n_paths=N_PATHS, seed=SEED, horizon=HORIZON):
    """Draw the published random stream. Order is fixed by the registry."""
    rng = np.random.default_rng(seed)
    drv = {}
    for name, kind, params, _note in DRIVERS:
        drv[name] = _sample(rng, kind, params, n_paths).astype(np.float64)
    # Drawn last, and only once, so that adding a driver above would be caught
    # by the harness rather than silently shifting this block.
    drv["_shock_eps"] = rng.standard_normal((n_paths, horizon))
    return drv
# === SECTION: MECHANISM ===
# Blended consumption tax for the rest-of-English-speaking bucket. A prior, and
# a blend rather than a rate: Ireland 23, Canada 5 to 15, Australia 10,
# New Zealand 15, Singapore 9.
ROW_TAX = 0.13

# Seasonality shapes, January to December, before amplitude scaling.
_ACQ_SHAPE = np.array([1.25, 0.95, 0.90, 0.85, 0.60, 0.35, 0.25, 0.45, 1.50, 1.20, 1.00, 0.70])
_USE_SHAPE = np.array([1.05, 1.15, 1.30, 1.35, 1.40, 0.70, 0.30, 0.35, 0.85, 1.00, 1.05, 0.90])
_ACQ_SHAPE = _ACQ_SHAPE / _ACQ_SHAPE.mean()
_USE_SHAPE = _USE_SHAPE / _USE_SHAPE.mean()

# Phase shift in months applied to the seasonality of each market, because the
# examination calendar is what drives it and it does not sit in the same place.
SEASON_SHIFT = {M_UK: 0, M_US: 0, M_IN: -3, M_ROW: 0}


def season_factor(shape, m, t, amp):
    idx = (cal_month(t) + SEASON_SHIFT[m]) % 12
    return 1.0 + amp * (shape[idx] - 1.0)


# units_target() lived here and was never called. It read UNIT_SCHEDULES directly
# rather than the config's schedules, so any future caller would have silently
# ignored every narrow-scope scenario. Removed rather than fixed: dead code that
# would be wrong if used is worse than no code. units_cost_weight() below is the
# live function and it takes the schedules as an argument.


def units_cost_weight(m, t, schedules=None):
    """
    The catalogue reached by month t in market m, as (subjects, levels, boards).

    It returns the SCHEDULE, not a cost. content_full_equivalents() turns these
    three into full item-bank equivalents, applying board reuse and market reuse,
    and that is the quantity the content cost line is built on. An earlier
    docstring here described a four-value return beginning with full
    equivalents; three are returned and none of them is that, which would have
    misled a reader about the mechanism the largest cost line rests on.
    """
    subj = lev = boards = 0
    for month, s, l, b in (schedules or UNIT_SCHEDULES)[m]:
        if t >= month:
            subj, lev, boards = s, l, b
    return subj, lev, boards


def content_full_equivalents(drv, m, t, schedules=None):
    """Full item-bank equivalents of content built by month t in market m."""
    subj, lev, boards = units_cost_weight(m, t, schedules)
    if subj == 0:
        return np.zeros_like(drv["board_reuse"])
    first_board = subj * lev
    extra_boards = subj * lev * (boards - 1)
    fe = first_board + extra_boards * (1.0 - drv["board_reuse"])
    if m != M_UK:
        # A foreign curriculum reuses only part of the UK bank.
        fe = fe * (1.0 - drv["market_reuse"])
    return fe


def cost_per_item_usd(drv):
    """Examiner validation plus authoring, per item, in USD."""
    exam_cost_gbp = drv["minutes_per_item"] / 60.0 * drv["examiner_rate_gbp_hr"]
    # docs/03 sets a 10 per cent second-validation sample as a design choice.
    exam_cost_gbp = exam_cost_gbp * 1.10
    return (exam_cost_gbp + drv["writer_gbp_item"]) * FX_GBP_USD


def cost_per_session_usd(drv, t):
    """
    Built from the architecture, not assumed. Bounded context per turn (D30),
    a verifier pass on every turn, and generations discarded by the gate.
    """
    decline = (1.0 - drv["infer_decline_yr"]) ** (t / 12.0)
    per_turn = (drv["tok_in_per_turn"] * drv["price_in_mtok_usd"]
                + drv["tok_out_per_turn"] * drv["price_out_mtok_usd"]) / 1e6
    per_turn = per_turn * (1.0 + drv["verify_overhead"]) / (1.0 - drv["gate_fire_rate"])
    return drv["turns_per_session"] * per_turn * decline


def gross_price_usd(drv, m, t):
    base_gbp = np.where(drv["anchor_u"] < P_TUTORING_ANCHOR,
                        drv["price_uk_tut_gbp"], drv["price_uk_sw_gbp"])
    rel = {M_UK: 1.0, M_US: drv["price_rel_us"], M_IN: drv["price_rel_in"],
           M_ROW: drv["price_rel_row"]}[m]
    drift = (1.0 + drv["price_drift_yr"]) ** (t / 12.0)
    return base_gbp * rel * FX_GBP_USD * drift


def tax_rate(drv, m):
    if m == M_UK:
        return np.full_like(drv["anchor_u"], VAT_UK)
    if m == M_US:
        return drv["us_sales_tax_eff"]
    if m == M_IN:
        return np.full_like(drv["anchor_u"], GST_IN)
    return np.full_like(drv["anchor_u"], ROW_TAX)


def _gamma_tail(mu, cv, thresh):
    """
    For sessions per household distributed gamma with mean mu and coefficient of
    variation cv, return (P(X > thresh), E[max(0, X - thresh)]).
    """
    k = 1.0 / np.maximum(cv, 1e-6) ** 2
    theta = mu / k
    z = thresh / np.maximum(theta, 1e-12)
    # special.gammaincc is what stats.gamma.sf calls underneath; using it
    # directly is bit-identical and avoids the distribution-object overhead,
    # which was four fifths of the run time.
    sf_k = special.gammaincc(k, z)
    sf_k1 = special.gammaincc(k + 1.0, z)
    excess = mu * sf_k1 - thresh * sf_k
    return sf_k, np.maximum(excess, 0.0)


def overage_terms(drv, mu_sessions):
    """
    Billed overage sessions per household per month and the share of households
    over the allowance. The allowance is sold, not enforced: sessions above it
    are delivered and cost money, and are billed only up to the cap. The
    asymmetry is deliberate and its sign is therefore known rather than assumed
    away (checklist item 3).
    """
    a = SESSION_ALLOWANCE
    cap_at = OVERAGE_CAP_MULT * a
    share_over, exc_a = _gamma_tail(mu_sessions, drv["sessions_cv"], a)
    _, exc_cap = _gamma_tail(mu_sessions, drv["sessions_cv"], cap_at)
    billed = exc_a - exc_cap
    return share_over, billed


def headcount(drv, cfg, t, active_consumer, units_fe_total, units_fe_ahead, reps_live):
    """
    Returns (bengaluru_heads, uk_heads). Step-shaped where the business would
    actually step, not smoothed into a slope.
    """
    z = np.zeros_like(drv["eng_usd_yr"])

    # Platform engineering. A floor, because the product has to exist at all,
    # plus a component that scales with how many consumer markets are live and
    # whether the institution channel is running. A scenario that opens one
    # market must not be charged a platform team sized for four; charging it one
    # made every narrow scope look worse than it is, which is checklist item 10
    # (see CHANGELOG.md 0.8).
    floor_pts = [(0, 4.0), (6, 7.0), (12, 9.0), (24, 11.0), (36, 12.0), (48, 13.0)]
    base = floor_pts[0][1]
    for month, v in floor_pts:
        if t >= month:
            base = v
    extra_markets = max(sum(1 for mm in range(NM) if t >= _open_month(cfg, mm)) - 1, 0)
    schools_on = 1.0 if t >= _school_open_month(cfg, M_UK) else 0.0
    plat_heads = (base + PLATFORM_PER_EXTRA_MARKET * extra_markets
                  + PLATFORM_FOR_INSTITUTIONS * schools_on) * drv["eng_ramp_mult"]

    # Content: what is being built over the coming year, plus revalidation of
    # what is live. Both divided by what one content head sustains in a year.
    fe_now = units_fe_total
    build = np.maximum(units_fe_ahead - fe_now, 0.0)
    content = (build + fe_now * drv["reval_frac_yr"]) / drv["units_per_content_head"]
    content = np.maximum(content, 2.0)

    # General and administrative, a decided step schedule.
    ga = 1.0
    for month, v in [(0, 1.0), (12, 2.0), (30, 4.0), (48, 7.0)]:
        if t >= month:
            ga = v

    beng = plat_heads + content + ga

    # UK-based roles. Safeguarding is a rota, which is a step cost: docs/05
    # concedes next-business-day review is not adequate for an acute
    # disclosure. The step below adds three and a half further posts, which is
    # thin for genuine round-the-clock cover and is named as such in LIMITS.md.
    uk = np.zeros_like(z)
    if t >= 3:
        uk = uk + 0.5                      # data protection officer, part time
    if t >= 12:
        uk = uk + 0.5
    if t >= _open_month(cfg, M_UK):
        uk = uk + 1.0                      # business-hours safeguarding reviewer
    uk = uk + np.where(active_consumer > ROTA_EXTENDED_AT, 1.0, 0.0)
    uk = uk + np.where(active_consumer > ROTA_24_7_AT, 3.5, 0.0)

    # Route B field sales. A fixed cost that cannot be turned down quickly, and
    # one a scenario that does not open the institution channel must not carry.
    uk = uk + reps_live
    return beng, uk, plat_heads, content


def step_costs_usd(drv, cfg, t, heads_total):
    """
    One-off and recurring step costs, each named. Absence is not conservatism,
    so anything believed to be zero is written down as zero here rather than
    left out.
    """
    z = np.zeros_like(drv["eng_usd_yr"])
    c = z.copy()

    # The counsel items in docs/14, spread over the first four months. The vault
    # is not internally consistent about how many there are: docs/14 lists
    # OI-1 to OI-12, while its README and docs/11 both say eleven. The cost here
    # does not depend on which is right.
    if 0 <= t < 4:
        c = c + drv["step_counsel_initial_usd"] / 4.0

    # Entity set-up, two months ahead of each market opening, then annual
    # compliance, audit and accounting for every live entity.
    # An entity exists only where the scenario actually opens a market. A
    # scenario that does not open the United States must not be charged for a
    # United States entity, and a scenario that does open one must not get it
    # free (checklist items 9 and 10).
    entity_months = {}
    if cfg["scope"] != "ukonly":
        entity_months[M_US] = 13 + cfg["launch_shift"]
        entity_months[M_ROW] = 22 + cfg["launch_shift"]
        if cfg["india_d2c"]:
            entity_months[M_IN] = 13 + cfg["launch_shift"]
    for m, month in entity_months.items():
        if t == month:
            c = c + drv["step_entity_setup_usd"]
        if t == month + 1:
            c = c + drv["step_counsel_market_usd"]
    live_entities = 1.0                     # the Bengaluru operating company
    if t >= 4:
        live_entities += 1.0                # the UK contracting entity
    for m, month in entity_months.items():
        if t >= month:
            live_entities += 1.0
    c = c + live_entities * drv["step_entity_annual_usd"] / 12.0

    # UK Article 27 representative, from the month the UK entity stands up.
    if t >= 4:
        c = c + drv["step_uk_rep_usd_yr"] / 12.0

    # DPIA maintenance and audit readiness, from UK consumer launch.
    if t >= _open_month(cfg, M_UK):
        c = c + drv["step_dpia_audit_usd_yr"] / 12.0

    # Information security certification, required before an institution will
    # complete a security review. Awarded two months before the school channel,
    # and not charged at all to a scenario that never opens it.
    school_m = _school_open_month(cfg, M_UK)
    if school_m < 10 ** 9:
        if t == school_m - 2:
            c = c + drv["step_cert_setup_usd"]
        if t >= school_m:
            c = c + drv["step_cert_annual_usd"] / 12.0

    # Premises, once there are enough heads to need them.
    c = c + np.where(heads_total > 8.0, heads_total * drv["step_office_usd_head_yr"] / 12.0, 0.0)
    return c


def expected_contrib_pm(drv, m, t, cps, billed=None):
    """
    The contribution per active household per month that the company would
    forecast for a market at month t, from its own drivers rather than from the
    book it has not yet written. Used only to set the acquisition budget cap;
    before the first customer exists there is no realised figure to use and a
    cap driven off the realised one deadlocks the budget at zero.
    """
    price_g = gross_price_usd(drv, m, t)
    trate = tax_rate(drv, m)
    mu = drv["sessions_per_hh_month"]
    if billed is None:
        _share, billed = overage_terms(drv, mu)
    gross = price_g + billed * price_g / SESSION_ALLOWANCE * drv["overage_price_frac"]
    net = gross / (1.0 + trate)
    var = (mu * cps
           + drv["support_min_hh_month"] / 60.0 * drv["support_usd_hr"]
           + gross * drv["pay_pct"] + drv["pay_fixed_usd"]
           + drv["hosting_hh_usd"])
    return net - var


def verification_cost(drv, m):
    """
    Age assurance per acquired account. India is charged double because verifiable
    parental consent under the DPDP Rules is a heavier process than United Kingdom
    age assurance, not the same one.

    This exists as a function because the acquisition loop and the lifetime value
    estimate used to disagree: the loop charged India twice and the estimate
    credited it nothing, so the India budget cap was set on a lifetime value that
    omitted the largest India-specific unit cost.
    """
    return drv["verif_cost_usd"] * (2.0 if m == M_IN else 1.0)


def normalise_segment_mix(mix_e, mix_a):
    """
    The three segment shares, guaranteed to sum to one.

    seg_mix_exam is U(0.40, 0.85) and seg_mix_alevel is U(0.03, 0.25), drawn
    independently, so their sum exceeds one on about a twentieth of paths and
    reaches 1.097. The old arithmetic floored the pre-examination share at zero
    and left the other two alone, so on those paths the loop put MORE households
    into stock than acquisitions bought. They were billed, they consumed
    inference, and no acquisition cost and no age-assurance check was paid for
    any of them. The clamp made the discrepancy invisible rather than absent:
    it is exactly the np.maximum that hides a defect instead of reporting it.

    Rescaling preserves the ratio between the two drawn shares, which is what
    the priors are about, and gives up nothing the model was using. It is
    applied here and at the acquisition site so the budget cap and the loop
    cannot disagree about what a cohort is made of. See CHANGELOG 6.2.
    """
    mix_p = np.maximum(1.0 - mix_e - mix_a, 0.0)
    total = mix_p + mix_e + mix_a
    return mix_p / total, mix_e / total, mix_a / total


def ltv_estimate(drv, contrib_pm, m, t):
    """
    The company's own running estimate of what a household is worth, used only
    to cap the acquisition budget. Gross of every fixed cost, and the write-up
    publishes the all-in contribution beside it rather than passing this off as
    a net figure.

    It must agree with the survival the month loop actually applies, because it
    is the only restraint on acquisition spend anywhere in the model and the cap
    it sets scales as roughly the square of it. It did not. Two things were
    missing and between them they made the estimate about two and a half times the
    retention the same model delivers. Round five found a third, and all three
    are listed here because the function is the only restraint on acquisition
    spend anywhere in the model and the cap it sets scales as roughly its
    square:

      1. First-month attrition. An acquisition enters as `add * keep` and is
         then hit by `churn` in the same month, before it is ever billed. About
         a quarter of every acquisition is gone before the first invoice. The
         estimate credited all of it.
      2. The examination calendar. An examination-year household is wiped at
         the sitting whatever its churn rate. A geometric life capped at a
         constant seven months credited it up to seven months wherever in the
         year it was acquired, including the month before a sitting.

      3. The pre-examination cap. The loop moves a pre-examination household on
         at the PROGRESSION month, two months after the sitting; this function
         capped its life at the sitting plus ten. Those are different
         quantities and not congruent, and the post-progression term counted
         the months to THIS year's sitting rather than to the household's own.

    All three are now taken from the loop's own quantities rather than from a
    constant. The gap is smaller and is not closed; cohorts.py publishes what
    remains. See CHANGELOG 4.3 and 5.4.
    """
    keep_first, months = ltv_billed_months(drv, m, t)
    # Verification is paid on every acquisition whether or not it survives, so
    # it is not scaled by keep_first.
    return np.maximum(keep_first * contrib_pm * months - verification_cost(drv, m), 0.0)


def ltv_billed_months(drv, m, t):
    """
    The survival the budget cap believes in, split out of ltv_estimate so that
    the retained months it assumes can be read without inverting a clamped cash
    figure. cohorts.py publishes the gap between this and what the loop
    delivers, and until round 6 it did so from its own COPY of this arithmetic,
    which still carried the form CHANGELOG 5.4 removed. One implementation is
    the only way that cannot drift again. See CHANGELOG 6.5.

    Returns (keep_first, months): the share of an acquisition that survives to
    be billed at all, and the months the survivors are credited with.
    """
    ch = np.clip(drv["churn_base"], 1e-3, 0.95)
    # What survives to be billed at all.
    keep_first = (1.0 - drv["churn_m1_extra"]) * (1.0 - ch)
    # Months from here to the next sitting in this market, which is the hard
    # ceiling on an examination-year household however slowly it churns.
    # A household acquired IN the sitting month is exempt from that month's
    # sitting exit (the loop skips this month's arrivals), so its ceiling is the
    # NEXT sitting, twelve months out, not zero. The bare modulus gave it zero
    # billed months and, through budget_cap_from_ltv, collapsed the acquisition
    # budget in one month of every twelve. See CHANGELOG 6.3.
    to_sitting = float((EXAM_CAL_MONTH[m] - cal_month(t)) % 12) or 12.0
    # A pre-examination household leaves that segment at the PROGRESSION month,
    # which the loop puts two months after the sitting, not at the sitting plus
    # ten. Those are different quantities and not congruent: for a household
    # acquired in the sitting month the true figure is two and the code used
    # ten. After progressing it has a full run to its OWN sitting, ten months
    # later, not to this year's. Round 4 rewrote this function to take the
    # calendar from the loop and then used arithmetic the loop does not.
    # See CHANGELOG 5.4.
    to_progress = float((EXAM_CAL_MONTH[m] + 2 - cal_month(t)) % 12) or 12.0
    m_exam = np.minimum(1.0 / ch, to_sitting)
    m_pre_first = np.minimum(1.0 / ch, to_progress)
    m_pre = (m_pre_first + (1.0 - drv["summer_lapse_pre"]) * drv["progress_continue"]
             * np.minimum(1.0 / ch, 10.0))
    m_al = np.minimum(1.0 / ch, to_sitting + 12.0)
    mix_e = drv["seg_mix_exam"]
    mix_a = drv["seg_mix_alevel"]
    mix_p, mix_e, mix_a = normalise_segment_mix(mix_e, mix_a)
    months = mix_e * m_exam + mix_p * m_pre + mix_a * m_al
    return keep_first, months


def effective_cac(drv, m, spend, penetration):
    """
    Effective cost per acquired household at the spend actually being made, not
    the low-volume anchor. Saturation in spend and pressure from exhausting the
    reachable pool, then the creator-led blend.
    """
    rel = {M_UK: 1.0, M_US: drv["cac_rel_us"], M_IN: drv["cac_rel_in"],
           M_ROW: drv["cac_rel_row"]}[m]
    sat = (np.maximum(spend, 1.0) / drv["cac_ref_spend_usd"]) ** drv["sat_kappa"]
    pool_term = (1.0 / np.maximum(1.0 - np.clip(penetration, 0.0, 0.97), 0.03)) ** drv["pool_pressure_psi"]
    non_creator = drv["cac_anchor_usd"] * rel * sat * pool_term
    blend = 1.0 - drv["creator_share"] * (1.0 - drv["creator_cac_rel"])
    return non_creator * blend, non_creator


def budget_cap_from_ltv(drv, m, ltv, penetration):
    """
    Invert the saturation curve for the spend at which effective CAC reaches the
    cap. Without this the budget is a rule with no cap and a saturating channel
    eventually buys households for more than they are worth.
    """
    rel = {M_UK: 1.0, M_US: drv["cac_rel_us"], M_IN: drv["cac_rel_in"],
           M_ROW: drv["cac_rel_row"]}[m]
    pool_term = (1.0 / np.maximum(1.0 - np.clip(penetration, 0.0, 0.97), 0.03)) ** drv["pool_pressure_psi"]
    blend = 1.0 - drv["creator_share"] * (1.0 - drv["creator_cac_rel"])
    target = CAC_LTV_CAP * ltv
    denom = drv["cac_anchor_usd"] * rel * pool_term * blend
    ratio = np.maximum(target, 0.0) / np.maximum(denom, 1e-9)
    return drv["cac_ref_spend_usd"] * ratio ** (1.0 / drv["sat_kappa"])
# === SECTION: LOOP ===
# Decisions inside the loop, stated here so they are arguable rather than buried.
SEG_USAGE_REL = {S_PRE: 0.85, S_EXAM: 1.15, S_ALEVEL: 1.00}
MARKET_BUDGET_WEIGHT = {M_UK: 1.00, M_US: 0.70, M_IN: 0.40, M_ROW: 0.50}
SCHOOL_USAGE_REL = 0.35          # a seat in a school is used less than a paying household
SCHOOL_ONBOARD_WEEKS = 0.75      # UK person-weeks per institution: DPA, security review, onboarding
SCHOOL_REP_RAMP = [(12, 1.0), (24, 3.0), (40, 6.0)]
CONTENT_BUILD_WINDOW = 6         # months spent building a content step before it is delivered


def base_config():
    return dict(
        scope="por",              # "por" plan of record, or "ukonly"
        india_d2c=False,
        schools=True,
        feedback=None,            # dict of feedback parameters, drawn outside the published stream
        fx=None,                  # dict of sampled FX arrays, drawn outside the published stream
        appstore=None,            # dict with share and fee, drawn outside the published stream
        enforce_allowance=False,
        launch_shift=0,           # months added to every market opening
        unit_schedules=None,      # None means the published schedules in CONSTANTS
        creator=None,             # None means no creator licence cost, which is the published run
        onshore_share=None,       # None or 0.0 means all engineering stays in Bengaluru
        residual=None,            # None means the horizon writes everything to zero, which is the published run
        pool_reacq_multiple=None, # None means the published POOL_REACQUISITION_MULTIPLE
        stop_acquisition_after=None,  # None means acquire to the end, which is the published run
    )


def _open_month(cfg, m):
    base = CONSUMER_OPEN[m]
    if cfg["scope"] == "ukonly" and m != M_UK:
        return 10 ** 9
    if m == M_IN and not cfg["india_d2c"]:
        return 10 ** 9
    if base >= 10 ** 9:
        return base
    return base + cfg["launch_shift"]


def _school_open_month(cfg, m):
    if not cfg["schools"] or cfg["scope"] == "ukonly" or m not in SCHOOL_OPEN:
        return 10 ** 9
    return SCHOOL_OPEN[m] + cfg["launch_shift"]


def content_build_plan(drv, cfg):
    """
    Full item-bank equivalents built in each month. A content step is built over
    the six months before it is delivered, not charged in the month it lands.
    """
    P = drv["anchor_u"].shape[0]
    schedules = cfg.get("unit_schedules") or UNIT_SCHEDULES
    plan = [np.zeros(P) for _ in range(HORIZON)]
    live = [np.zeros(P) for _ in range(HORIZON)]
    for m in range(NM):
        if cfg["scope"] == "ukonly" and m != M_UK:
            continue
        # India content is built only if India actually trades. The institution
        # channel is modelled as a single United Kingdom motion (see LIMITS.md),
        # so tying the India bank to it charged the base run for a bank nothing
        # bills and made por_no_schools differ in two things rather than one.
        if m == M_IN and not cfg["india_d2c"]:
            continue
        prev = np.zeros(P)
        for month, _s, _l, _b in schedules[m]:
            month = month + cfg["launch_shift"]
            if month >= HORIZON:
                continue
            fe = content_full_equivalents(drv, m, month - cfg["launch_shift"], schedules)
            delta = np.maximum(fe - prev, 0.0)
            start = max(month - CONTENT_BUILD_WINDOW, 0)
            span = max(month - start, 1)
            for tt in range(start, month):
                plan[tt] = plan[tt] + delta / span
            for tt in range(month, HORIZON):
                live[tt] = live[tt] + delta
            prev = fe
    return plan, live


def run(drv, cfg=None):
    """The month loop. Returns monthly (paths x horizon) arrays and per-path summaries."""
    cfg = cfg or base_config()
    P = drv["anchor_u"].shape[0]
    T = HORIZON
    Z = lambda: np.zeros((P, T))

    fx_gbp = cfg["fx"]["gbp"] if cfg["fx"] else np.full(P, FX_GBP_USD)
    fx_scale = fx_gbp / FX_GBP_USD          # 1.0 exactly when FX is fixed

    fb = cfg["feedback"]

    out = {k: Z() for k in [
        "active_hh", "active_uk", "active_us", "active_in", "active_row",
        "acquisitions", "gross_rev_consumer", "net_rev_consumer", "tax_collected",
        "net_rev_schools", "school_contracts", "inference_cost", "support_cost",
        "payment_cost", "hosting_cost", "verif_cost", "cac_spend", "content_cost",
        "people_beng_cost", "people_uk_cost", "step_cost", "school_onboard_cost",
        "appstore_fee", "people_beng_content_cost", "school_inference_cost",
        "school_sessions_delivered", "sessions_delivered", "share_over_allowance",
        "arrivals_removed_same_month",
        "cac_effective_blended", "cac_effective_noncreator", "net_cash", "demand_shock",
        "terminal_value",
    ]}

    stock = np.zeros((P, MS, N_COHORT_YEARS))
    # Households acquired THIS month, tracked alongside the standing book. The
    # examination-calendar exits below must not fire on them: billing starts the
    # month after acquisition, so an arrival deleted in the month it arrives has
    # been charged its acquisition cost and its age-assurance check and billed
    # for nothing at all. Round 4 fixed the same ordering error on the
    # progression path and left it on the acquisition path, where it is twice
    # the size. See CHANGELOG 5.1.
    arrivals = np.zeros((P, MS, N_COHORT_YEARS))
    # acq_cum, cac_cum, contrib_cum and months_cum lived here. They were
    # populated every month, returned in the summary, and read by nothing in the
    # directory. contrib_cum in particular accumulated the WHOLE-BOOK blended
    # contribution against each cohort, so anything that had ever computed a
    # cohort payback from it would have credited an Indian pre-examination
    # cohort the United Kingdom examination-year average; and months_cum counted
    # the acquisition month while active_hh does not, so two household-month
    # counts differing by about a quarter sat in the same dict. Removed rather
    # than fixed. See CHANGELOG 4.6.

    build_plan, build_live = content_build_plan(drv, cfg)
    item_cost = cost_per_item_usd(drv)
    items_per_unit = drv["items_per_unit"]

    # The unseasoned overage terms do not depend on the month or the market, so
    # they are computed once rather than per market per month.
    _share_flat, billed_flat = overage_terms(drv, drv["sessions_per_hh_month"])

    shock_state = np.zeros(P)
    # The stationary variance of the AR(1) state. It is the right correction
    # only once the process HAS reached stationarity: shock_state starts at
    # exactly zero, so for the first several months its true variance is
    # smaller and subtracting the stationary half-variance made the
    # "mean-one" multiplier mean LESS than one. Measured on the published
    # draws it was 0.969 at month zero and 0.995 at the United Kingdom
    # go-to-market month, so the launch ran into a demand headwind that is an
    # artefact of the initial condition rather than a modelled shock. The
    # per-month variance below is the correct one at every t and converges to
    # this. See CHANGELOG 6.4.
    shock_var_stationary = drv["shock_sd"] ** 2 / np.maximum(1.0 - drv["shock_rho"] ** 2, 1e-3)

    school_live = np.zeros(P)
    school_pending = np.zeros((P, T + 24))
    trailing_net = np.zeros(P)
    cum_acq = [np.zeros(P) for _ in range(NM)]
    bad_run_current = np.zeros(P)
    bad_run_longest = np.zeros(P)

    for t in range(T):
        arrivals[:] = 0.0
        cps = cost_per_session_usd(drv, t)

        # --- persistent demand shock; independent monthly noise would remove
        # --- exactly the sustained bad run that ends companies.
        shock_state = drv["shock_rho"] * shock_state + drv["shock_sd"] * drv["_shock_eps"][:, t]
        shock_var = shock_var_stationary * (1.0 - drv["shock_rho"] ** (2 * (t + 1)))
        shock_mult = np.exp(shock_state - 0.5 * shock_var)
        # Tracked here so that the sustained-bad-run figures are re-derivable
        # from a published file. The innovations themselves are not published,
        # so a claim to have reconstructed the run lengths from them was not
        # checkable by a reader.
        is_bad = shock_mult < SHOCK_BAD_THRESHOLD
        bad_run_current = np.where(is_bad, bad_run_current + 1.0, 0.0)
        bad_run_longest = np.maximum(bad_run_longest, bad_run_current)
        out["demand_shock"][:, t] = shock_mult

        # --- content spend this month ------------------------------------
        built = build_plan[t]
        live_fe = build_live[t]
        # Content is wholly pound-denominated: examiner contract rates in pounds
        # per hour and authoring in pounds per item. It is the largest pound
        # cost in the model and it used to sit OUTSIDE the foreign-exchange
        # exposure while the much smaller United Kingdom people line sat inside
        # it, so the sampled-rate scenario priced the exposure without its
        # largest natural hedge. fx_scale is 1.0 exactly when the rate is fixed,
        # which is the published run. See CHANGELOG 4.4.
        content_c = built * items_per_unit * item_cost * fx_scale
        content_c = content_c + live_fe * items_per_unit * (
            drv["minutes_per_item"] / 60.0 * drv["examiner_rate_gbp_hr"] * FX_GBP_USD * fx_scale
        ) * drv["reval_frac_yr"] / 12.0
        out["content_cost"][:, t] = content_c

        # --- revenue and variable cost on the standing book ---------------
        gross_c = np.zeros(P)
        net_c = np.zeros(P)
        sess_total = np.zeros(P)
        over_weighted = np.zeros(P)
        charges = np.zeros(P)
        active_total = np.zeros(P)
        active_by_market = [np.zeros(P) for _ in range(NM)]

        # Markets that share a seasonal phase share their usage distribution, so
        # the overage integral is computed once per (phase, segment) per month.
        over_cache = {}
        for m in range(NM):
            price_g = gross_price_usd(drv, m, t) * (fx_scale if m != M_US else 1.0)
            trate = tax_rate(drv, m)
            over_price = price_g / SESSION_ALLOWANCE * drv["overage_price_frac"]
            use_season = season_factor(_USE_SHAPE, m, t, drv["usage_season_amp"])
            for s in range(NS):
                st = stock[:, ms(m, s), :].sum(axis=1)
                if not np.any(st > 0):
                    continue
                mu = drv["sessions_per_hh_month"] * use_season * SEG_USAGE_REL[s]
                key = (SEASON_SHIFT[m], s)
                if key not in over_cache:
                    over_cache[key] = overage_terms(drv, mu)
                share_over, billed = over_cache[key]
                if cfg["enforce_allowance"]:
                    # Enforce the ALLOWANCE. This used to truncate delivery at
                    # OVERAGE_CAP_MULT * SESSION_ALLOWANCE, which is the billing
                    # cap, so it cut off sessions almost nobody reaches and left
                    # the overage revenue in place: it answered a different
                    # question from the one the scenario is named for.
                    _, exc_allow = _gamma_tail(mu, drv["sessions_cv"], SESSION_ALLOWANCE)
                    delivered = mu - exc_allow
                    billed_here = np.zeros_like(billed)     # nothing to bill above a hard cap
                else:
                    delivered = mu
                    billed_here = billed
                g = price_g + billed_here * over_price
                gross_c = gross_c + st * g
                net_c = net_c + st * g / (1.0 + trate)
                sess_total = sess_total + st * delivered
                over_weighted = over_weighted + st * share_over
                charges = charges + st
                active_total = active_total + st
                active_by_market[m] = active_by_market[m] + st

        out["gross_rev_consumer"][:, t] = gross_c
        out["net_rev_consumer"][:, t] = net_c
        out["tax_collected"][:, t] = gross_c - net_c
        out["sessions_delivered"][:, t] = sess_total
        out["share_over_allowance"][:, t] = np.where(active_total > 0, over_weighted / np.maximum(active_total, 1e-9), 0.0)
        out["inference_cost"][:, t] = sess_total * cps
        out["support_cost"][:, t] = active_total * drv["support_min_hh_month"] / 60.0 * drv["support_usd_hr"] * (
            fb["support_mult"] if fb else 1.0)
        out["payment_cost"][:, t] = gross_c * drv["pay_pct"] + charges * drv["pay_fixed_usd"]
        out["hosting_cost"][:, t] = active_total * drv["hosting_hh_usd"]
        if cfg["appstore"]:
            out["appstore_fee"][:, t] = gross_c * cfg["appstore"]["share"] * cfg["appstore"]["fee"]
        out["active_hh"][:, t] = active_total
        for m, key in enumerate(["active_uk", "active_us", "active_in", "active_row"]):
            out[key][:, t] = active_by_market[m]

        # --- acquisition budget, then acquisition -------------------------
        contrib_pm = np.where(active_total > 0,
                              (net_c - out["inference_cost"][:, t] - out["support_cost"][:, t]
                               - out["payment_cost"][:, t] - out["hosting_cost"][:, t]
                               - out["appstore_fee"][:, t]) / np.maximum(active_total, 1e-9),
                              0.0)

        first_open = min((_open_month(cfg, m) for m in range(NM)), default=10 ** 9)
        if t >= first_open:
            since = t - first_open
            if since < ACQ_RAMP_HOLD_MONTHS:
                ramp_on = 1.0
            else:
                ramp_on = max(0.0, 1.0 - (since - ACQ_RAMP_HOLD_MONTHS) / ACQ_RAMP_TAPER_MONTHS)
            envelope = drv["acq_launch_ramp"] * ramp_on + drv["acq_pct_of_rev"] * trailing_net
        else:
            envelope = np.zeros(P)

        # Retained months are computed over the whole horizon, and acquisitions
        # are still ramping in its last months, so most of them have their
        # retention cut off by the window rather than by churn. Switching
        # acquisition off partway through leaves every remaining acquisition a
        # long run to churn out in, which is how the size of that censoring is
        # measured. None in the published run. See CHANGELOG 5.8.
        _stop = cfg.get("stop_acquisition_after")
        if _stop is not None and t >= _stop:
            open_markets = []
        else:
            open_markets = [m for m in range(NM) if t >= _open_month(cfg, m)]
        pool_reacq = cfg.get("pool_reacq_multiple") or POOL_REACQUISITION_MULTIPLE
        wsum = sum(MARKET_BUDGET_WEIGHT[m] for m in open_markets) or 1.0
        spend_total = np.zeros(P)
        acq_total = np.zeros(P)
        verif_total = np.zeros(P)
        cac_blend_num = np.zeros(P)
        cac_nc_num = np.zeros(P)

        schedules_live = cfg.get("unit_schedules") or UNIT_SCHEDULES
        for m in open_markets:
            # The catalogue the reachable pool is credited for must be the one
            # that has actually been BUILT, which under a launch delay is not
            # the one the raw schedule names at t. content_build_plan delivers
            # every step at month + launch_shift; this read the schedule at t,
            # so a delayed launch was credited breadth -- and therefore pool,
            # saturation denominator, budget cap and standing-book room -- for
            # item banks it had not paid for yet.
            #
            # launch_shift is zero in the published run and in every scenario
            # except the two launch delays, which is why this survived seven
            # rounds. It bit exactly where it mattered: it flattered delay, in
            # the same direction as the two contaminations section 9 already
            # names, and it was large enough to invert a sign. See CHANGELOG 7.9.
            subj_live, _lev_live, _b_live = units_cost_weight(
                m, t - cfg["launch_shift"], schedules_live)
            breadth = (max(subj_live, 1) / POOL_BREADTH_REFERENCE_SUBJECTS) ** POOL_BREADTH_EXPONENT
            pool = drv["pool_uk"] * breadth * {M_UK: 1.0, M_US: drv["pool_rel_us"],
                                               M_IN: drv["pool_rel_in"], M_ROW: drv["pool_rel_row"]}[m]
            # Pressure rises with CUMULATIVE reach, not with the standing book.
            # Measured on the standing book, a path that churned and reacquired
            # could sell to its whole market three times over while the
            # saturation term never rose above a fifth, which made the effective
            # cost curve in section 4 of the write-up describe something the
            # model was not doing.
            reach = cum_acq[m] / np.maximum(pool * pool_reacq, 1.0)
            pen = np.clip(reach, 0.0, 0.97)
            ltv_m = ltv_estimate(drv, expected_contrib_pm(drv, m, t, cps, billed_flat), m, t)
            cap = budget_cap_from_ltv(drv, m, ltv_m, pen)
            season = season_factor(_ACQ_SHAPE, m, t, drv["acq_season_amp"])
            want = envelope * MARKET_BUDGET_WEIGHT[m] / wsum * season
            spend = np.minimum(want, cap)
            cac_b, cac_nc = effective_cac(drv, m, spend, pen)
            acq_wanted = spend / np.maximum(cac_b, 1e-6) * shock_mult
            # The pool caps the standing book. It does not cap the cumulative
            # flow, so without the second term a path could churn and reacquire
            # its way to tens of millions of households in a market of a few
            # million. A household can be worked more than once, not endlessly.
            room = np.maximum(pool - active_by_market[m], 0.0)
            room_cum = np.maximum(pool * pool_reacq - cum_acq[m], 0.0)
            acq = np.minimum(acq_wanted, np.minimum(room, room_cum))
            # Spend is committed in advance, so a demand shock buys fewer
            # households for the same money. Only running out of market stops the
            # spend. Recomputing spend from realised acquisitions, which is what
            # this did before, made the shock cost nothing at all.
            served = np.where(acq_wanted > 1e-12, np.minimum(acq / np.maximum(acq_wanted, 1e-12), 1.0), 0.0)
            realised_spend = spend * served
            cum_acq[m] = cum_acq[m] + acq
            v = verification_cost(drv, m)
            verif_total = verif_total + acq * v
            spend_total = spend_total + realised_spend
            acq_total = acq_total + acq
            cac_blend_num = cac_blend_num + acq * cac_b
            cac_nc_num = cac_nc_num + acq * cac_nc

            cy = min(t // 12, N_COHORT_YEARS - 1)
            mix_e = drv["seg_mix_exam"]
            mix_a = drv["seg_mix_alevel"]
            mix_p, mix_e, mix_a = normalise_segment_mix(mix_e, mix_a)
            keep = 1.0 - drv["churn_m1_extra"]
            for s, mix in ((S_PRE, mix_p), (S_EXAM, mix_e), (S_ALEVEL, mix_a)):
                add = acq * mix
                stock[:, ms(m, s), cy] += add * keep
                arrivals[:, ms(m, s), cy] += add * keep

        out["cac_spend"][:, t] = spend_total
        out["verif_cost"][:, t] = verif_total
        out["acquisitions"][:, t] = acq_total
        out["cac_effective_blended"][:, t] = np.where(acq_total > 0, cac_blend_num / np.maximum(acq_total, 1e-9), 0.0)
        out["cac_effective_noncreator"][:, t] = np.where(acq_total > 0, cac_nc_num / np.maximum(acq_total, 1e-9), 0.0)

        # --- Route B ------------------------------------------------------
        reps_live = 0.0
        school_open = _school_open_month(cfg, M_UK)
        if school_open < 10 ** 9:
            for month, v in SCHOOL_REP_RAMP:
                if t >= month + cfg["launch_shift"]:
                    reps_live = v
        if reps_live > 0:
            qualified = reps_live * drv["school_rep_pipeline_yr"] / 12.0
            land = (t + np.round(drv["school_cycle_m"]).astype(int))
            wins = qualified * drv["school_win_rate"]
            idx = np.clip(land, 0, T + 23)
            np.add.at(school_pending, (np.arange(P), idx), wins)
        if cal_month(t) == 8:
            school_live = school_live * drv["school_renewal"] + school_pending[:, max(t - 11, 0):t + 1].sum(axis=1)
        seat_price_usd = drv["school_gbp_seat_yr"] * FX_GBP_USD * fx_scale
        school_rev = school_live * drv["school_seats"] * seat_price_usd / 12.0
        out["net_rev_schools"][:, t] = school_rev
        out["school_contracts"][:, t] = school_live
        school_sessions = school_live * drv["school_seats"] * drv["sessions_per_hh_month"] * SCHOOL_USAGE_REL * \
            season_factor(_USE_SHAPE, M_UK, t, drv["usage_season_amp"])
        # School seats consume inference and it lands in the same series as the
        # consumer book's. That is right for a cost total and wrong for every
        # ratio built against CONSUMER revenue or consumer household months,
        # because the cost of an institution seat then sits in a numerator whose
        # denominator excludes the institution's revenue. The school share is
        # emitted separately so those ratios can be built consistently. It is a
        # DECOMPOSITION of inference_cost, never a thirteenth cost line. See
        # CHANGELOG 5.2.
        out["school_inference_cost"][:, t] = school_sessions * cps
        out["inference_cost"][:, t] += school_sessions * cps
        # Same treatment for the session count, and for the same reason: a
        # sessions-per-household figure built from the combined series over
        # consumer households is not a per-household figure at all. Found by
        # invariants.py on its first run. See CHANGELOG 5.15.
        out["school_sessions_delivered"][:, t] = school_sessions
        out["sessions_delivered"][:, t] += school_sessions
        new_schools = school_pending[:, t] if reps_live > 0 else np.zeros(P)
        # Carries overhead_mult like every other people cost. It did not, which
        # made an onboarding person-week cheaper than the same person-week
        # anywhere else in the model. See CHANGELOG 4.5.
        out["school_onboard_cost"][:, t] = (new_schools * drv["uk_gbp_yr"] * FX_GBP_USD * fx_scale
                                            * drv["overhead_mult"] / 52.0 * SCHOOL_ONBOARD_WEEKS)

        # --- people and steps --------------------------------------------
        live_fe_ahead = build_live[min(t + 12, HORIZON - 1)]
        beng, uk, plat_heads, content_heads = headcount(drv, cfg, t, active_total, live_fe, live_fe_ahead, reps_live)
        if fb:
            beng = beng + fb["eng_heads_extra"]
        # docs/05 flags the restricted transfer of United Kingdom children's data
        # to an Indian controller as a standard position not confirmed for this
        # fact pattern. If a DPIA or counsel forces the learner-content path
        # onshore, the Bengaluru cost advantage goes with it. onshore_share moves
        # that fraction of engineering onto United Kingdom cost. Zero in the
        # published run, so this changes nothing there.
        # Onshoring moves the people who touch learner data: the platform
        # engineers who build and operate the learner path, and support, who read
        # learner conversations. It does NOT move content authoring, which works
        # from published DfE subject content and sees no learner, nor general and
        # administrative. An earlier version moved content and administration and
        # left support in Bengaluru, which is close to the opposite of what a
        # transfer restriction would do.
        onshore = cfg["onshore_share"] or 0.0
        moved = plat_heads * onshore
        out["people_beng_cost"][:, t] = (beng - moved) * drv["eng_usd_yr"] * drv["overhead_mult"] / 12.0
        # The content heads inside that line, published separately. They are
        # salaried people whose whole job is the content schedule, so they are a
        # content cost wearing a people label, and the cost-split table read as
        # though content were only the contracted authoring and validation. A
        # round-four review found the write-up understating content-driven cost
        # by this amount. It is NOT added to content_cost, because that would
        # double it in every total; it is published beside it. See CHANGELOG 4.8.
        out["people_beng_content_cost"][:, t] = (content_heads * drv["eng_usd_yr"]
                                                 * drv["overhead_mult"] / 12.0)
        out["people_uk_cost"][:, t] = ((uk + moved) * drv["uk_gbp_yr"] * FX_GBP_USD
                                       * fx_scale * drv["overhead_mult"] / 12.0)
        if onshore > 0.0:
            # Support moves with them, from a Bengaluru hourly rate to a United
            # Kingdom one, pro rata.
            uk_support_hr = drv["uk_gbp_yr"] * FX_GBP_USD * fx_scale / 2000.0
            out["support_cost"][:, t] = (active_total * drv["support_min_hh_month"] / 60.0
                                         * ((1.0 - onshore) * drv["support_usd_hr"] + onshore * uk_support_hr)
                                         * (fb["support_mult"] if fb else 1.0))
        out["step_cost"][:, t] = step_costs_usd(drv, cfg, t, beng + uk)

        # The creator licence, which the published run costs at zero. Both limbs
        # of a name-and-likeness deal: a fixed minimum per signed creator, and a
        # share of the revenue from households their audience brought.
        if cfg["creator"]:
            n_creators = 0.0
            for month, v in CREATOR_RAMP:
                if t >= month + cfg["launch_shift"]:
                    n_creators = v
            out["step_cost"][:, t] += (n_creators * cfg["creator"]["fee_per_creator_yr"] / 12.0
                                       + gross_c * drv["creator_share"] * cfg["creator"]["rev_share"])

        # The horizon writes everything to zero. A large share of the content
        # spend falls in the last two years and is charged against a truncated
        # revenue window, while the item bank it buys and the standing book are
        # both worth something on the day the window closes. Crediting nothing is
        # a choice, not a neutral default, and it is the choice that makes
        # content look as expensive as it does. residual prices the other
        # reading. Zero in the published run.
        if cfg["residual"] and t == T - 1:
            r = cfg["residual"]
            content_to_date = sum(out["content_cost"][:, tt] for tt in range(T))
            out["terminal_value"][:, t] = (content_to_date * r["content_retained"]
                                           + active_total * contrib_pm * r["book_months"])

        cost_t = sum(out[k][:, t] for k in [
            "inference_cost", "support_cost", "payment_cost", "hosting_cost", "verif_cost",
            "cac_spend", "content_cost", "people_beng_cost", "people_uk_cost", "step_cost",
            "school_onboard_cost", "appstore_fee"])
        rev_t = out["net_rev_consumer"][:, t] + out["net_rev_schools"][:, t]
        out["net_cash"][:, t] = rev_t - cost_t + out["terminal_value"][:, t]
        trailing_net = 0.5 * trailing_net + 0.5 * rev_t

        # A nested loop whose whole body bound a view of stock and discarded it
        # stood here. It was the remains of the cohort accumulators removed in
        # round 4 and did nothing. See CHANGELOG 5.5.

        # --- survival and the examination calendar ------------------------
        churn = drv["churn_base"]
        if fb:
            churn = np.clip(churn * fb["churn_price_mult"] * fb["churn_quality_mult"][:, t], 1e-4, 0.95)
        stock *= (1.0 - churn)[:, None, None]
        # This month's arrivals are a subset of stock and must take the same
        # churn, or the two are on different bases and "stock less arrivals"
        # stops being the standing book. The round 5 fix clamped that difference
        # at zero, which hid the mismatch and made the exemption slightly too
        # generous on paths with a small standing book. See CHANGELOG 5.15.
        arrivals *= (1.0 - churn)[:, None, None]

        for m in range(NM):
            em = EXAM_CAL_MONTH[m]
            cm = cal_month(t)
            if cm == em:
                # Both sitting-month exits fire on the STANDING book only:
                # households already on it before this month, not those acquired
                # into it this month. Two separate orderings were wrong here.
                # Round 4 fixed the A-level one against the PROGRESSION path,
                # which used to subject a household that had just moved up from
                # GCSE to the A-level sitting exit two years before its own
                # sitting; that was worth 1,049,552 of terminal cash. Round 5
                # found the same error against the ACQUISITION path, on both
                # segments, worth about twice as much again. See CHANGELOG 5.1.
                std_exam = stock[:, ms(m, S_EXAM), :] - arrivals[:, ms(m, S_EXAM), :]
                leaving = std_exam * (1.0 - drv["exam_carryover"])[:, None]
                stock[:, ms(m, S_EXAM), :] -= leaving
                std_al = stock[:, ms(m, S_ALEVEL), :] - arrivals[:, ms(m, S_ALEVEL), :]
                stock[:, ms(m, S_ALEVEL), :] -= std_al * drv["alevel_exit_rate"][:, None]
                stock[:, ms(m, S_ALEVEL), :] += leaving * drv["alevel_continue"][:, None]
            # The summer lapse and the progression are examination-calendar
            # exits exactly as the two above are, and until round 6 they were
            # the two that still fired on this month's arrivals. A pre-exam
            # household acquired in the month after the sitting lost the lapse
            # before its first invoice; one acquired two months after lost the
            # lapse AND was moved into the examination segment or deleted, about
            # 44 per cent of it gone in its arrival month having paid its
            # acquisition cost and its age-assurance check and billed nothing.
            # Round 5 fixed this on the sitting exits and left it here. The
            # arrivals stay in the pre-exam segment and take next year's
            # calendar, which is the year their own sitting falls in.
            # See CHANGELOG 6.1.
            if cm in ((em + 1) % 12, (em + 2) % 12):
                per_month = 1.0 - np.sqrt(1.0 - drv["summer_lapse_pre"])
                std_pre = stock[:, ms(m, S_PRE), :] - arrivals[:, ms(m, S_PRE), :]
                lapsed = std_pre * per_month[:, None]
                stock[:, ms(m, S_PRE), :] -= lapsed
            if cm == (em + 2) % 12:
                std_pre = stock[:, ms(m, S_PRE), :] - arrivals[:, ms(m, S_PRE), :]
                moving = std_pre * drv["progress_continue"][:, None]
                stock[:, ms(m, S_PRE), :] -= std_pre
                stock[:, ms(m, S_EXAM), :] += moving

            # Every household acquired this month must still be standing after
            # the calendar block, in whichever segment it was acquired into.
            # This replaces a diagnostic that compared what the two SITTING
            # exits removed against what they ought to have removed, which was
            # algebraically zero whatever the rest of the block did: it could
            # only ever fire if someone edited the one line it was written
            # against, and the summer lapse and the progression were wrong for
            # five rounds underneath it while it read zero in all sixty months.
            # This form is written against the arrivals array rather than
            # against any one exit, so it bites on all four. See CHANGELOG 6.1.
            for _s in (S_PRE, S_EXAM, S_ALEVEL):
                out["arrivals_removed_same_month"][:, t] += np.maximum(
                    arrivals[:, ms(m, _s), :] - stock[:, ms(m, _s), :], 0.0).sum(axis=1)

    summary = dict(stock=stock,
                   bad_run_longest=bad_run_longest, cum_acq=cum_acq)
    return out, summary
# === SECTION: AGGREGATE ===
# Band definitions. A band is a set of whole paths ranked on terminal cumulative
# cash, averaged within the band. It is not a percentile of anything, and the
# percentile it actually sits at is measured rather than assumed.
BANDS = {"low": (0.10, 0.30), "central": (0.40, 0.60), "high": (0.70, 0.90)}

# Column suffix discipline, enforced by check_suffix_discipline():
#   _mean  a mean over all paths
#   _p10 _p50 _p90  a percentile of the per-path distribution at that month
#   _bandlow _bandcentral _bandhigh  a within-band average of whole paths
# A _mean and a _band figure must never be divided by one another.
MEAN_SUFFIX = "_mean"
BAND_SUFFIXES = ("_bandlow", "_bandcentral", "_bandhigh")


def cumulative_cash(out):
    return np.cumsum(out["net_cash"], axis=1)


def band_indices(cum, band):
    P = cum.shape[0]
    order = np.argsort(cum[:, -1], kind="stable")
    lo, hi = BANDS[band]
    return order[int(round(lo * P)):int(round(hi * P))]


def band_line(series, cum, band):
    return series[band_indices(cum, band), :].mean(axis=0)


def band_percentile_placement(series, cum, band):
    """
    Where the band line actually sits in the real per-path distribution, month by
    month. It is not the percentile a reader assumes from the band's rank range,
    and it moves across MONTHS within a single run by several percentile points,
    which is what makes comparing a band line at one month against a band line at
    another invalid.

    It moves very little BETWEEN scenarios at the terminal month -- measured
    across every scenario in section 6 of the write-up. An earlier version of
    this docstring had the two axes the wrong way round and asserted exactly the
    conclusion the write-up went on to retract, so a reader sent to the code got
    the superseded claim. See CHANGELOG 8.2.
    """
    line = band_line(series, cum, band)
    P = series.shape[0]
    placement = np.empty(series.shape[1])
    for t in range(series.shape[1]):
        col = np.sort(series[:, t])
        placement[t] = np.searchsorted(col, line[t], side="left") / P
    return placement


def trough_stats(cum):
    per_path_min = cum.min(axis=1)
    per_path_argmin = cum.argmin(axis=1)
    mean_line = cum.mean(axis=0)
    return dict(
        min_of_mean=float(mean_line.min()),
        min_of_mean_month=int(mean_line.argmin()),
        mean_of_min=float(per_path_min.mean()),
        p10_of_min=float(np.percentile(per_path_min, 10)),
        p50_of_min=float(np.percentile(per_path_min, 50)),
        p90_of_min=float(np.percentile(per_path_min, 90)),
        mean_trough_month=float(per_path_argmin.mean()),
        understatement_abs=float(mean_line.min() - per_path_min.mean()),
        understatement_ratio=float(mean_line.min() / per_path_min.mean()) if per_path_min.mean() != 0 else float("nan"),
    )


def first_true_month(mask):
    """First month index where mask is True, or -1."""
    any_true = mask.any(axis=1)
    idx = np.argmax(mask, axis=1)
    return np.where(any_true, idx, -1)


def sustained_mask(x, k=3):
    """True from the first month of a run of k consecutive positive months."""
    pos = x > 0
    run = pos.copy()
    for i in range(1, k):
        run[:, :-i] &= pos[:, i:]
        run[:, -i:] = False
    return run


def path_outcomes(out, summary=None):
    cum = cumulative_cash(out)
    rev = out["net_rev_consumer"] + out["net_rev_schools"]
    cost = rev - out["net_cash"]
    sustained = sustained_mask(out["net_cash"], 3)
    per_path_min = cum.min(axis=1)
    o = dict(
        terminal_cash=cum[:, -1],
        trough=per_path_min,
        trough_month=cum.argmin(axis=1).astype(float),
        peak_funding_requirement=np.maximum(-per_path_min, 0.0),
        month_rev_passes_cost=first_true_month(sustained).astype(float),
        ever_month_positive=first_true_month(out["net_cash"] > 0).astype(float),
        cum_positive_month=first_true_month(cum > 0).astype(float),
        terminal_active_hh=out["active_hh"][:, -1],
        terminal_net_rev_month=rev[:, -1],
        terminal_cost_month=cost[:, -1],
        total_acquisitions=out["acquisitions"].sum(axis=1),
        total_cac_spend=out["cac_spend"].sum(axis=1) + out["verif_cost"].sum(axis=1),
        total_content_cost=out["content_cost"].sum(axis=1),
        total_people_cost=out["people_beng_cost"].sum(axis=1) + out["people_uk_cost"].sum(axis=1),
        total_step_cost=out["step_cost"].sum(axis=1),
        total_tax_collected=out["tax_collected"].sum(axis=1),
        total_sessions=out["sessions_delivered"].sum(axis=1),
    )
    o["effective_cac_all_in"] = np.where(o["total_acquisitions"] > 0,
                                         o["total_cac_spend"] / np.maximum(o["total_acquisitions"], 1e-9), 0.0)
    fy = slice(HORIZON - 12, HORIZON)
    fy_acq = out["acquisitions"][:, fy].sum(axis=1)
    fy_spend = out["cac_spend"][:, fy].sum(axis=1) + out["verif_cost"][:, fy].sum(axis=1)
    o["final_year_effective_cac"] = np.where(fy_acq > 0, fy_spend / np.maximum(fy_acq, 1e-9), 0.0)
    fy_active = out["active_hh"][:, fy].sum(axis=1)
    # CONSUMER contribution per consumer household month. It used to carry the
    # institution channel's revenue AND the institution channel's inference in a
    # numerator whose denominator is consumer household months only, which is
    # not the quantity the write-up describes ("net revenue less inference,
    # support, payment, hosting and store fees" per household month) and is not
    # a quantity anyone wants. The institution channel is priced on its own in
    # the no-schools scenario. See CHANGELOG 5.2.
    fy_contrib = (out["net_rev_consumer"][:, fy]
                  - (out["inference_cost"][:, fy] - out["school_inference_cost"][:, fy])
                  - out["support_cost"][:, fy]
                  - out["payment_cost"][:, fy] - out["hosting_cost"][:, fy]
                  - out["appstore_fee"][:, fy]).sum(axis=1)
    o["final_year_contrib_per_hh_month"] = np.where(fy_active > 0, fy_contrib / np.maximum(fy_active, 1e-9), 0.0)
    fy_allin = (out["net_rev_consumer"][:, fy] + out["net_rev_schools"][:, fy]
                - (out["net_rev_consumer"][:, fy] + out["net_rev_schools"][:, fy] - out["net_cash"][:, fy])
                + out["cac_spend"][:, fy] + out["verif_cost"][:, fy]).sum(axis=1)
    o["final_year_allin_contrib_per_hh_month"] = np.where(fy_active > 0, fy_allin / np.maximum(fy_active, 1e-9), 0.0)
    fyh = out["active_hh"][:, fy].sum(axis=1)
    o["final_year_hh_months"] = fyh
    o["total_demand_shock_months_below_threshold"] = (out["demand_shock"] < 0.80).sum(axis=1).astype(float)
    o["longest_demand_shock_bad_run"] = (summary["bad_run_longest"] if summary is not None
                                         else np.zeros(fyh.shape[0]))
    o["mean_share_over_allowance"] = np.where(
        out["active_hh"].sum(axis=1) > 0,
        (out["share_over_allowance"] * out["active_hh"]).sum(axis=1) / np.maximum(out["active_hh"].sum(axis=1), 1e-9),
        0.0)
    return o, cum


PERCENTILE_SUFFIXES = ("_p10", "_p50", "_p90")
PLACEMENT_SUFFIX = "_placement"
BASIS_SUFFIXES = (MEAN_SUFFIX,) + PERCENTILE_SUFFIXES + BAND_SUFFIXES + (PLACEMENT_SUFFIX,)
MONTHLY_META = ("run", "seed", "run_date", "t", "cal_year", "cal_month")

# One column is exempt and is named here rather than pattern-matched. It is the
# percentile position of the central band line, so it legitimately carries a band
# marker that is not its own basis. Everything else in the monthly file must end
# in exactly one basis and carry no other basis marker anywhere.
MONTHLY_EXEMPT = ("cum_cash_bandcentral_placement",)


def check_suffix_discipline(header, kind):
    """
    Refuse a header in which a reader could not tell what basis a column is on.

    An earlier version of this tested whether a name ended in both a mean suffix
    and a band suffix, which no string can do, so it could never fire. This one
    can, and suffix_discipline_selftest() shows it firing.

    kind is "monthly", where every column carries a basis, or "paths", where no
    column may carry one because nothing in that file is aggregated across paths.
    """
    problems = []
    for h in header:
        if h in MONTHLY_EXEMPT:
            continue
        ends = [s for s in BASIS_SUFFIXES if h.endswith(s)]
        inside = [s for s in BASIS_SUFFIXES if s in h and not h.endswith(s)]
        if inside:
            problems.append("%s carries the basis marker %s somewhere other than its suffix"
                            % (h, ", ".join(inside)))
        if kind == "monthly":
            if h in MONTHLY_META:
                continue
            if not ends:
                problems.append("%s carries no basis suffix, in a file where every column has one" % h)
            elif len(ends) > 1:
                problems.append("%s ends in more than one basis: %s" % (h, ", ".join(ends)))
        elif kind == "paths":
            if ends:
                problems.append("%s ends in %s, which is an aggregate basis, in a per-path file"
                                % (h, ", ".join(ends)))
        else:
            raise ValueError(kind)
    if problems:
        raise AssertionError("suffix discipline: %s" % "; ".join(problems))
    return True


def suffix_discipline_selftest():
    """Show the gate refusing. A check that has never failed is not a check."""
    cases = [
        (["active_hh_mean_bandlow"], "monthly", "a name carrying two bases"),
        (["active_hh"], "monthly", "a monthly column with no basis at all"),
        (["terminal_cash_mean"], "paths", "an aggregate basis in a per-path file"),
        (["sessions_mean_usd"], "paths", "a basis marker buried inside a name"),
    ]
    lines = ["suffix discipline self-test"]
    ok = True
    for header, kind, why in cases:
        try:
            check_suffix_discipline(header, kind)
            lines.append("FAILED to refuse %-34s (%s)" % (header[0], why))
            ok = False
        except AssertionError as exc:
            lines.append("refused %-34s %s" % (header[0], str(exc).split(": ", 1)[1]))
    return ok, "\n".join(lines) + "\n"

# === SECTION: EMIT ===
MONTHLY_SERIES = [
    "active_hh", "active_uk", "active_us", "active_in", "active_row", "acquisitions",
    "gross_rev_consumer", "net_rev_consumer", "tax_collected", "net_rev_schools",
    "school_contracts", "inference_cost", "support_cost", "payment_cost", "hosting_cost",
    "verif_cost", "cac_spend", "content_cost", "people_beng_cost", "people_uk_cost",
    "step_cost", "school_onboard_cost", "appstore_fee", "people_beng_content_cost",
    "school_inference_cost", "school_sessions_delivered", "sessions_delivered",
    "arrivals_removed_same_month",
    "share_over_allowance", "cac_effective_blended", "cac_effective_noncreator", "net_cash",
    "demand_shock", "terminal_value",
]

PATH_FIELDS = [
    "terminal_cash", "trough", "trough_month", "peak_funding_requirement",
    "month_rev_passes_cost", "ever_month_positive", "cum_positive_month",
    "terminal_active_hh", "terminal_net_rev_month", "terminal_cost_month",
    "total_acquisitions", "total_cac_spend", "total_content_cost", "total_people_cost",
    "total_step_cost", "total_tax_collected", "total_sessions", "effective_cac_all_in",
    "final_year_effective_cac", "final_year_contrib_per_hh_month",
    "final_year_allin_contrib_per_hh_month", "mean_share_over_allowance",
    "final_year_hh_months", "total_demand_shock_months_below_threshold",
    "longest_demand_shock_bad_run",
]

FMT = "%.6f"


def monthly_csv_text(out, cum, run_label):
    header = ["run", "seed", "run_date", "t", "cal_year", "cal_month"]
    for s in MONTHLY_SERIES:
        header += [s + "_mean", s + "_p10", s + "_p50", s + "_p90",
                   s + "_bandlow", s + "_bandcentral", s + "_bandhigh"]
    header += ["cum_cash_mean", "cum_cash_p10", "cum_cash_p50", "cum_cash_p90",
               "cum_cash_bandlow", "cum_cash_bandcentral", "cum_cash_bandhigh",
               "cum_cash_bandcentral_placement"]
    check_suffix_discipline(header, "monthly")

    prepared = {}
    for s in MONTHLY_SERIES + ["cum_cash"]:
        arr = cum if s == "cum_cash" else out[s]
        prepared[s] = dict(
            mean=arr.mean(axis=0),
            p10=np.percentile(arr, 10, axis=0),
            p50=np.percentile(arr, 50, axis=0),
            p90=np.percentile(arr, 90, axis=0),
            bandlow=band_line(arr, cum, "low"),
            bandcentral=band_line(arr, cum, "central"),
            bandhigh=band_line(arr, cum, "high"),
        )
    placement = band_percentile_placement(cum, cum, "central")

    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    for t in range(HORIZON):
        row = [run_label, SEED, RUN_DATE, t, cal_year(t), cal_month(t) + 1]
        for s in MONTHLY_SERIES:
            d = prepared[s]
            row += [FMT % d[k][t] for k in ("mean", "p10", "p50", "p90", "bandlow", "bandcentral", "bandhigh")]
        d = prepared["cum_cash"]
        row += [FMT % d[k][t] for k in ("mean", "p10", "p50", "p90", "bandlow", "bandcentral", "bandhigh")]
        row += [FMT % placement[t]]
        w.writerow(row)
    return buf.getvalue()


def paths_csv_text(o, drv, run_label):
    header = ["run", "seed", "run_date", "path"] + PATH_FIELDS + DRIVER_NAMES
    check_suffix_discipline(header, "paths")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    P = o["terminal_cash"].shape[0]
    cols = [o[f] for f in PATH_FIELDS] + [drv[n] for n in DRIVER_NAMES]
    for i in range(P):
        w.writerow([run_label, SEED, RUN_DATE, i] + [FMT % c[i] for c in cols])
    return buf.getvalue()


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as fh:
        fh.write(text)
    return path

# === SECTION: MAIN ===
def build_base():
    """The published base run: the plan of record."""
    drv = draw_drivers()
    out, summary = run(drv, base_config())
    o, cum = path_outcomes(out, summary)
    return drv, out, o, cum


def main():
    ok, text = suffix_discipline_selftest()
    write_text(os.path.join(OUT, "suffix_selftest.txt"), text)
    print(text, end="")
    if not ok:
        raise AssertionError("the suffix discipline check failed to refuse a header it must refuse")
    drv, out, o, cum = build_base()
    mtext = monthly_csv_text(out, cum, "por")
    ptext = paths_csv_text(o, drv, "por")
    write_text(os.path.join(OUT, "por_monthly.csv"), mtext)
    write_text(os.path.join(OUT, "por_paths.csv"), ptext)
    ts = trough_stats(cum)
    print("seed", SEED, "date", RUN_DATE, "paths", N_PATHS, "horizon", HORIZON)
    print("share of paths with 3 consecutive cash-positive months: %.4f"
          % float((o["month_rev_passes_cost"] >= 0).mean()))
    print("mean peak funding requirement USD: %.0f" % float(o["peak_funding_requirement"].mean()))
    print("min of the mean cash line USD: %.0f (month %d)" % (ts["min_of_mean"], ts["min_of_mean_month"]))
    print("mean of the per-path minimum USD: %.0f" % ts["mean_of_min"])
    print("understatement ratio: %.4f" % ts["understatement_ratio"])


if __name__ == "__main__":
    main()
