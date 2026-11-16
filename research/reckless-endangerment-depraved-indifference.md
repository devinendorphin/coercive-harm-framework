# Research: Reckless Endangerment, Depraved Indifference and Entity Liability (New York), for S-9

*Compiled 2026-11-16 at Endorphin's direction, on branch `claude/ai-researcher-interview-uqimk2`.
Companion to `research/foreseeability-and-risk-assessment.md` and doc 03's endangerment reframing.
Cross-repo origin: veriticide-general-ledger,
`docs/depraved-indifference-test-palisade-interview-2026-11-16.md`.*

## Why this matters for S-9

S-9 makes the **foreseeability nexus** the keystone: the offense drops proof of actual harm and
keeps the speech-tether and non-weaponizability. Doc 03 already cites "reckless endangerment" as the
constitutionally ordinary precedent, but only in passing. New York's Article 120 is a worked,
litigated example of that structure. It shows both that the structure works and how it fails.

## Finding 1: criminal law already punishes grave-risk creation without completed harm `[ESTABLISHED]`

| Tier | Statute | Mental state | Risk element | Grade |
|---|---|---|---|---|
| Base | **PL § 120.20**, second-degree reckless endangerment | recklessly (aware of the risk, consciously disregards it) | conduct creating a **substantial risk of serious physical injury** | class A misdemeanor |
| Aggravated | **PL § 120.25**, first-degree reckless endangerment | recklessly, **under circumstances evincing a depraved indifference to human life** | conduct creating a **grave risk of death** | class D felony |

**Neither tier requires injury or death.** The risk element is objective: it turns on the risk the
conduct actually created, not on the actor's state of mind (*People v Davis*, 72 N.Y.2d 32,
following *Register*).

**Mapping to the framework:**
- **§ 120.20** has the shape of doc 03's criminal tier after the steelman (S-13): subjective
  recklessness plus an objectively risky course of conduct, with actual harm as an aggravator rather
  than an element.
- **§ 120.25** is the analogue of the "aggravated tier".
- This supports S-9's move as **ordinary**, not novel. `[SUPPORTED]` as an analogy: the statutes
  are about physical danger, and the framework's harm is psychological (OBJ-019).

## Finding 2: the cautionary history, an objective-circumstances test that prosecutors stretched `[ESTABLISHED]`

- ***People v Register* (1983)** read "circumstances evincing depraved indifference" as an
  **objective** assessment of how dangerous the conduct was.
- Prosecutors then charged depraved indifference in one-on-one intentional killings, where intent
  was harder to prove.
- The Court of Appeals pulled it back:
  - ***Hafeez* (2003)**, ***Gonzalez* (2004)**;
  - ***Payne* (2004)**: depraved indifference "may not be properly charged in the overwhelming
    majority of homicides", and a one-on-one shooting or knifing "can almost never qualify";
  - ***Suarez* (2005)**;
  - ***Feingold* (2006)**: overruled *Register*. Depraved indifference is a **culpable mental
    state**: "an utter disregard for the value of human life."
- *Feingold* itself arose under § 120.25. *(Analyst's prior knowledge: a gas-explosion suicide
  attempt endangering neighbors. A citator lists Feingold as the leading Article 120 case. Verify
  the facts before quoting.)*

**Lesson for this framework.** When an aggravated risk offense rests on an *objective* "circumstances"
test, it becomes a prosecutorial tool for cases that do not fit it, here as a way around proving
intent. New York needed about twenty years of litigation to fix that by moving the test into the
actor's mind. **This is a live risk for S-9.** The framework's foreseeability nexus is deliberately
objective (doc 04 §0). It is safe only for as long as the criminal tier keeps **subjective
recklessness** as a separate gate (S-13). That is how § 120.20 survived while Register's § 120.25
reading did not. Recorded as **OBJ-033**. `[SUPPORTED]`

## Finding 3: words-only conduct is outside Article 120 `[SUPPORTED]`

Both tiers require *conduct* that creates a risk of *physical* injury or death. Coerced-suicide
prosecutions (Carter) were brought as involuntary manslaughter, not as reckless endangerment
(`research/coerced-suicide-prosecutions.md`). This search found no case applying § 120.25 to
words-only coercion. Article 120 therefore **confirms S-10**: it reaches the mixed-conduct pattern,
and the pure-words paradigm stays with civil orders, doc 05, and doc 06.

## Finding 4: entity liability, NY PL § 20.20(2)(b), and the apex gap `[ESTABLISHED]` statute / `[HYPOTHESIS]` application

A corporation is guilty of an offense when the conduct constituting it is "engaged in, authorized,
solicited, requested, commanded, or recklessly tolerated by the board of directors or by a high
managerial agent acting within the scope of his employment and in behalf of the corporation." A
*high managerial agent* is an officer, or an agent of comparable authority over policy or over the
supervision of subordinates. Applied in *People v Harco Constr.* (1st Dep't 2018). PG&E's 84
involuntary-manslaughter pleas (Camp Fire, 2020) show entity liability on a recklessness theory, after
deaths.

**Why it matters here.**
- OBJ-027 and S-17 (the apex-power gap) say the framework reaches subordinate-scale coercion and is
  silent at the apex. § 20.20(2)(b) is an existing doorway from individual conduct to the institution
  that **recklessly tolerates** it.
- That is the criminal-law cousin of S-15's civil lever (negligent retention or supervision for
  ignoring documented conduct).
- Candidate: an organization whose high managerial agents recklessly tolerate a documented course of
  coercive endangerment by a manager carries entity liability for it. `[HYPOTHESIS]` `[NORMATIVE]`

**Limits, named:**
1. § 20.20 attributes *conduct*. Whether an entity can carry an aggravated mental state (a
   *Feingold*-type state) through "recklessly tolerated" is untested as far as this search found.
   `[OPEN]`
2. The doorway is also a weaponization surface: an employer facing exposure for "tolerating" an
   *alleged* pattern has an incentive to over-react against the accused. That is exactly the
   liability-driven over-reaction that the S-15 safeguard (doc 05 §4) gates.
3. **Not liberty-reviewed.** Do not mark stable before `/liberty-review` (agreement 4).

## Cross-repo note (veriticide ledger)

In the ledger memo, the same doctrine was tested against an AI-lab insider's public testimony. The
individual-level *Feingold* test **failed**: the speaker's on-record concern defeats "utter
disregard". The enterprise-level recklessness skeleton **held** on his testimony. § 20.20's
high-managerial-agent prong was **not reached** by his testimony. That is the same three-way split
this note predicts: individual mental state hard, conduct skeleton easy, entity attribution dependent
on leadership-level records.

## Sources (verified by search 2026-11-16)

- NY PL § 120.20 and § 120.25 (nysenate.gov; CJI 2d § 120.25)
- NY PL § 20.20 (nysenate.gov)
- *People v Feingold*, 7 N.Y.3d 288 (2006)
- *People v Payne* (2004)
- *People v Taylor* (2010)
- *People v Galatro* (Davis/Register objective-risk discussion)
- *People v Harco Constr.* (1st Dep't 2018)
- PG&E Camp Fire plea (NBC News, 2020)
