# Contrary-case and quotation checks — 2026-11-11

*Checkpoint: the fixed manual sample check is complete. Full automatic quotation checks,
S24 B failures and the complete rebuilt-chunk comparison are pending below.*

This is an analysis audit by Codex, without subagents or new coders. It preserves every coder
record. It checks whether the published interpretation survives contrary passages and fixed
sensitivities; it is not a recoding of the seasons or independent verification of the
underlying allegations.

## Fixed selection and scope

D7 was committed in `f49ef02` before the first headline calculation. The reproducible
[quotation_sample.json](quotation_sample.json) selects the first eligible agreed positive,
agreed negative and disagreement for each prediction in each reporting group, in season/ID
order. Repeated selections across groups are retained in the manifest but not counted twice
in the audit totals. Relevant coded quotations were read alongside the cited transcript
context; contact sequences and coder notes were consulted where one quotation could not
establish the whole outcome. This sample does not substitute for the coders’ full-season
reading.

The sample contains **12 coded records (six matched stories) for each of full protection,
adverse responses, decisive work and never reaching**; **36 unique coded records overall**,
because these checks overlap. A quotation found by the script establishes wording, not that
the code follows from it. The sample is deliberately selected to include contrary cases,
not a random estimate of coding error.

The original identity matches, unmatched dispositions and repeats were validated before
calculation. No identity decision was changed after seeing codes. All recorded reading
endpoints match the committed original chunk counts (502 entries across 68 coder files).
The complete rebuilt-transcript comparison is pending; the original reading-log check is complete.

## What would count against the findings, and what was found

| Question | Disconfirming check | Observation from the fixed sample |
|---|---|---|
| Full protection [W1] | Find final protection in updates; look for a helpful contact wrongly equated with no protection; compare both own-coder figures and fixed exclusions | Daniel’s social-services custody outcome and Danielle’s later full-custody update are clear contrary cases. Sarah’s bank refunds and therapy show helpful action even though her family arranged her exit. Amy’s ten-year order and continuing-abuse statement sustain the full/partial disagreement. Hadas’s later prosecution cannot protect her from a harm that killed her. |
| Adverse response [W2] | Check that ordinary inaction has not been counted as disbelief/blame; inspect both a negative and disputed case; compare families and roles | Sarah’s contacts and Hadas’s temporary police interventions do not enter the specified indicator. Kelly’s counseling and church suppression do. The Jim S4 disagreement turns on authorities being used against him without a report of coercion to them. Mia’s S10 church/college teachings are present in the transcript, but classification as contacts about disclosed harm differs between coders. |
| Decisive work [W3] | Find proactive institutional work; check whether reporting or gathering evidence is being treated automatically as decisive; narrow to full protection | Jez’s restaurant staff and Kenji’s employer are institutional-action counterexamples. J.E.’s family recordings and FBI identification both matter. Jessa’s coders emphasize different protections, and the surrender passage also credits pressure from a relative. Natalia’s preparation and refusal to leave no record go beyond a bare report, alongside active legal aid and court work. |
| Never reaching | Look for actual contact; distinguish failed access, private support and suspected harm from a report; do not recode unknown as no | The first fiancée threatens a future order; that is not a filing. CJ’s family-wide police contact and Zara’s private investigation expose the boundary of acting on behalf of a particular person. Daisy’s observers state that they lacked proof and chose not to report. Amy’s early concealment does not negate her later contacts. |

The arithmetic checks are in `ARITHMETIC.md`. Repeat removal retains the earliest story
before eligibility or agreement. Contradictions, quotation exclusions and S17 substitution
are shown beside unchanged records. Each coder’s own figures, central survivors only and
full-protection-only attribution remain visible. No sample observation was used to alter a
code, reselect a person or move a threshold.

## Exact sample record locators

Claude A/B records below are **unblinded**. Codex CA/CB records are **blinded**. Source slugs
and timestamps for the outcome, contacts and decisive-worker quotations remain in the
original JSON records and the sample manifest. These observations do not name any uncharged
person.

| Files / person IDs | Questions checked | Checked observation |
|---|---|---|
| s01_A P01 / s01_B P01 | Full protection; adverse response; reaching | Bank refunds within 24 hours, airline information and counseling were helpful; family organized departure. Bank card cancellation failed to stop later charges. One outcome quote refers to her father, not an institution; the fuller contact sequence is essential. |
| s01_A P02 / s01_B P02 | Never reaching | A threatened future restraining-order application is not an application. Delayed discovery of account intrusion supports that narrow reason; it does not prove every kind of abuse went unrecognized. Couples counseling appears in notes, but abuse disclosure there is not established. |
| s03_A P02 / s03_B P02 | Reaching disagreement | Transcript says the family notified police and followed the detective’s no-contact recommendation. Whether that was a contact for CJ’s particular harm is the disputed step. |
| s04_A P02 / s04_B P02 | Adverse-response disagreement | County responsibility for stolen food and Temple leverage are described. One coder treats this as institutional counter-accusation; the other requires the coercion to have been brought to those authorities. Positive action by the congressional delegation and later delays remain visible. |
| s05_A P02 / s05_B P02 | Adverse response | Counseling minimized her sexual-abuse account and pressed an arrangement under a threat; church leadership suppressed discussion. These are more specific than simple inaction. Legal terms in a survivor’s quotation are not treated as adjudicated violations. |
| s05_A P05 / s05_B P06 | Full protection | Social services obtained a custody transfer to a sister; both code protection. Earlier social-work interviews with parents present and delays are also described, so protection does not erase earlier failures. |
| s06_A P03 / s06_B P04 | Institutional decisive work | Restaurant workers warned and assisted Jez; she expressly thanks them. Police declined action. Calling restaurant staff an institution is a design boundary disclosed by a coder, not resolved after seeing the result. |
| s06_A P10 / s06_B P09 | Attribution disagreement | Both the mother’s recorded calls and FBI identification are in the updates. The coders choose different decisive contributors despite agreeing on protection. |
| s07_CA P01 / s07_CB P01 | Full protection disagreement; adverse response; outside work; reaching | The prison’s letter rejecting a threat and the muting of Amy at the parole hearing are in the transcripts. The later ten-year order and her gratitude are also present, alongside her statement that abuse continues. “I gave him everything” is short; surrounding text specifies evidence and escalation to the prosecutor. |
| s07_CA P02 / s07_CB P02 | No full protection; no specified adverse response | Temporary detentions, later arrest and prosecution are present. None stopped the harm before Hadas’s death. A no-protection outcome does not make every contact disbelieving or blaming. |
| s08_CA P05 / s08_CB P07 | Never reaching | Observers explain lack of proof and concern about disproportionate consequences. The passage does not establish a clinical injury or that all concerns were true. |
| s09_CA P01 / s09_CB P01 | Full protection | The update reports full custody and zero visits, plus additional court terms not requested by Danielle. Earlier disbelief and delay remain in the record. No conviction is inferred. |
| s09_CA P03 / s09_CB P03 | Institutional decisive work | The employer investigated the retaliatory complaint, found no evidence and cleared Kenji; other harassment persisted. This is partial protection and institutional work. |
| s09_CA P14 / s09_CB P17 | Reaching disagreement | The later happy ending is reported. Private investigation and the family/survivor intervention are distinct from a protective institutional order; coders disagree over reaching. |
| s10_CA P37 / s10_CB P36 | Adverse-response disagreement | Harmful teachings and unsuccessful couples counseling are in the passage. No disclosure to church/college authorities is established there. The first coder counts teaching as institutional contact; the second codes only counseling. |
| s11_CA P53 / s11_CB P53 | Attribution disagreement | Academic accommodation and the fugitive’s later surrender are described. The surrender quotation states that a relative was about to disclose his whereabouts; that is not clean evidence of institutional initiative. The account intercuts speakers, making short quotations an especially limited basis for credit. |
| s13_A P02 / s13_B P02 | Full/partial disagreement | The son was returned by his father; later court orders constrained access. The later passage also describes improved parenting after monitored contact. Both outcome interpretations require the sequence, not just a court action. |
| s13_A P05 / s13_B P05 | Outside decisive work | Natalia located information, organized evidence and refused an agreement leaving no court record. Legal aid, service and a court order were also protective. The transcript supports the work but does not make a unique causal attribution certain. |

## Reasons checked before quoting examples

The first quoted example for each of nine recorded reasons was inspected. These are
checks of the recorded reason, not new scores:

| Reason | File / person ID and source | Observation |
|---|---|---|
| Did not recognize abuse | s01_A P02; S1 E9 around 25:11 | Delayed recognition of account intrusion; broader lack of abuse recognition is a coder inference. |
| Other | s01_A P02; S1 E9 around 17:55 | Threatened future order and private cutoff, not an actual filing. |
| Not stated | s01_A P03; S1 E12 around 8:13 | Blocking contact is described; no reason for not contacting an institution is stated. |
| Earlier disbelief | s01_A P09; Sacramento live episode around 68:42 | A mother’s blame is described; it is family disbelief and does not by itself prove the cause of non-reporting. |
| Institution was the abuser’s | s05_A P01; S5 E2 around 4:16 | Church leadership shamed a pregnancy disclosure. The coder treats the church as the source of harm and reserves reaching for an outside body; compare the different contact boundary in Mia’s S10 records. |
| Cost or access | s10_CA P10; S10 E3 around 27:47 | An attempted police call went unanswered; “never reached” does not mean unwillingness to seek help. |
| Fear | s10_CA P13; S10 E4 around 44:23 | Explicit fear of exposing the person and of what would happen. |
| Protecting others | s11_CA P22; S11 E7 around 33:56 | Fear of harming the group and its prospects, alongside uncertainty what to do. |
| Status or connections | s18_A P24; S18 E11 around 27:46 | A larger platform and fear of career destruction are explicit. |

## Previously flagged quotations

**S04 NEG:** the four below-bar quotations reproduce as 52/56 found. P01 and P09 each have
a contact quotation scoring 0.753 and a never-reached quotation scoring 0.765. The source
passages were read by hand: S4 E4 around 11:57–12:34 describes the plan to reach the US
consulate, then capture; around 16:46–17:43 describes treatment, intervention by the leader’s
family and cutting off shackles. The coder joins separated passages with ellipses and
replaces names with role descriptions. The underlying words/actions are present, but the
automatic failures remain failures in the pre-fixed exclusion sensitivity. Medical treatment
and removal of shackles do not by themselves establish safety from the subsequent forced labor.

**S24 B:** pending the complete S24 transcript retrieval and recheck. The six known failures are not waived.

## Other limitations encountered

The seven deceased-with-protection flags were inspected as records. Several concern a
different, earlier harm: survival after a collision before death from cancer; adoption before
a later fatal abuse; shelter during a relationship before a later partner’s alleged violence.
The broad exclusion is therefore deliberately conservative. S16’s conviction-based protection
call does not show a repaired financial loss; the code stays unchanged and is not defended
merely because a court acted.

The 21 reached/outcome contradictions stay listed by file and ID in `flags.csv`, with no
names in that report. Excluding these records does not repair or recode them. The automatically
checked wording is not a validation of all contact boundaries, causal credit, speakers or
outcomes. D5’s broken Claude blinding remains unrepaired. Why only S24 POS disclosed the
harness exposure is still an open question; this analysis supplies no explanation for the
other coders’ silence.

## Reproduction

The final reproduction commands will be recorded when retrieval and the all-file check finish. The sample selection is reproducible with `tools/analyze_whole_story.py`; the fixed inputs and sample manifest are committed.
