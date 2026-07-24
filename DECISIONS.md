# Design decisions

Deliberate trade-offs, recorded so they read as choices rather than gaps.

**Why a small gold set (9 conditions, 2 notes)?**
The assessment asks for a satisficing demonstrator, not a validation study.
The gold set is big enough to expose the one metric where the eras genuinely
separate (status accuracy, 89% vs 100%) and small enough to be fully auditable
by a reviewer in minutes. Real-note validation (below) covers what a curated
gold set cannot.

**Why also test on real de-identified notes?**
A gold set authored by the same person who wrote the notes flatters the
dictionary. Running the pipeline on public teaching notes (UHN, UCF,
MTSamples) surfaced what curation couldn't: the rules pass missing an actual
discharge diagnosis, and a live false positive on "no evidence of coronary
artery disease."

**Why claude-haiku-4-5 and not a bigger model?**
Extraction with an enforced JSON schema is a constrained task; the smallest,
cheapest model hit 100% status accuracy on the gold set. Escalating model size
before measurement says otherwise would be spend without evidence.

**Why no RAG / vector store?**
Nothing in the three-era comparison needs retrieval. The natural RAG extension
is nearest-valid-code suggestion over the 74,719 ICD-10-CM descriptions when
validation flags a code — noted as future work rather than bolted on.

**Why validate codes against the official CMS table instead of trusting the LLM?**
Because the failure mode is real: the vision model emitted R61.9 and R21.9 —
well-formed codes that do not exist. A deterministic check on a probabilistic
model is cheap, exact, and the same architecture the report recommends.

**Why an audit artifact per run?**
In payment integrity, output that cannot be audited cannot be defended. Every
run records note, model, prompt version, and each finding with its evidence —
the code-validity metrics in BENCHMARKS.md are computed from these artifacts.

**Why is the rule-based pass kept so simple?**
It is the historical baseline being measured, not a product. Making it
stronger (bigger dictionary, bidirectional negation) would blur the era
comparison the assessment topic asks for.

**Why offline simulation mode?**
The demo must run for a reviewer without an API key. Offline mode reuses the
rule-based pass and labels itself as a simulation rather than pretending to be
the LLM.
