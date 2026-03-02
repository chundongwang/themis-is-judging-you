# Fair Judgment Algorithm

## Overview

The goal is to produce a fair, representative rating for any subject by simulating a diverse panel of judges. Fairness here means the result reflects the distribution of opinions across a realistic population — not just the average of a homogeneous group.

---

## Core Concepts

### 1. Judge Dimensions

Each judge is characterized by a set of demographic and psychographic dimensions that define who they are and shape their preferences.

| Dimension       | Example Values                                              |
|-----------------|-------------------------------------------------------------|
| Age             | 18–24, 25–34, 35–44, 45–54, 55–64, 65+                    |
| Gender          | Male, Female, Non-binary                                    |
| Education       | High school, Some college, Bachelor's, Graduate             |
| Occupation      | Student, Blue-collar, White-collar, Creative, Retired       |
| Income level    | Low, Middle, Upper-middle, High                             |
| Cultural region | East Asia, South Asia, Europe, Americas, Africa, etc.       |
| Aesthetic style | Minimalist, Classic, Trendy, Eclectic                       |

A judge is a specific combination of dimension values, e.g.:

> Female · 28 · Bachelor's · Creative · Middle income · Americas · Trendy

---

### 2. Judge Panel via Bootstrapped Distributions

The panel composition should mirror a realistic population, not a uniform sample. This is achieved through **bootstrapping with distributions per dimension**.

#### Per-dimension distribution

Each dimension is assigned weights that reflect real-world population proportions. For continuous dimensions (e.g., age), a normal distribution is used directly. For categorical dimensions (e.g., occupation), discrete probability weights approximate the distribution.

Example for age:

```
μ = 35, σ = 15  →  skewed toward working-age adults
```

#### Bootstrap sampling

To generate a panel of `N` judges:

1. For each dimension, sample a value from its distribution independently.
2. Combine sampled values into one judge profile.
3. Repeat `N` times.

This ensures the panel's composition reflects natural population proportions rather than an artificial even split.

---

### 3. LLM-Simulated Judges

Each judge is simulated by prompting an LLM to **embody a specific human persona**. The LLM is the score function — it reasons as a human would, drawing on cultural context, lived experience, and personal taste encoded in its training data.

#### Prompt template

Each judge invocation is a single LLM call using a shared **template string**, with the judge's profile interpolated into the variable slots. The template is identical for every judge; only the values change.

```
You are a [age]-year-old [gender] from [cultural region].
You work as a [occupation], have a [education] education,
and earn a [income level] income.
Your aesthetic preferences tend toward [aesthetic style].

You are evaluating the following subject: [subject description or image].

Rate it on a scale of 1–10. Think and respond as this specific person would —
with their background, tastes, and worldview. Be genuine and direct.

Reply with JSON: { "score": <1–10>, "reason": "<one sentence>" }
```

The score and reason are both stored. Reasons are used later for stratified analysis.

#### Intra-judge variance via temperature

LLMs do not need an explicit noise term. Because they are probabilistic (temperature > 0), two calls with identical prompts produce slightly different scores, naturally modeling individual taste variance:

- Lower temperature → more consistent, decisive judge
- Higher temperature → more variable, casual judge

```
score_i = llm(persona_prompt(profile_i, subject), temperature=T)
```

#### Parallelism and cost

All `N` judge calls are independent and can be **fired concurrently**. Cost scales linearly with `N`. Caching scores for identical profiles across subjects reduces redundant calls.

---

### 4. Aggregation

After collecting scores from all `N` judges, aggregate into a result that preserves the full distribution rather than collapsing to a single number.

| Statistic     | Purpose                                        |
|---------------|------------------------------------------------|
| Mean          | Central tendency                               |
| Median        | Robust to outliers                             |
| Std deviation | Reflects polarization across the panel         |
| Histogram     | Shows how the full population is distributed   |
| By-segment    | Per-dimension group breakdown                  |

This lets the app report not just "7.2/10" but:

> "Most people rate this 6–8. Young adults (18–34) score it 1.5 points higher than those 45+."

---

### 5. Stratified Reporting

Scores can be broken down by any dimension to surface demographic insights:

- "Female judges rated this 1.2 points higher than male judges"
- "Judges in the Creative occupation gave the highest scores across all groups"

This is computed by grouping the panel by dimension values and computing per-group statistics over the collected scores.

---

## Algorithm Summary

```
Input: subject S, panel size N, temperature T

1. Build judge panel:
   for i = 1 to N:
     profile_i = sample_from_population_distributions()

2. Score each judge (all in parallel):
   for each judge i:
     prompt_i      = render_template(profile_i, S)
     score_i,
     reason_i      = llm(prompt_i, temperature=T)

3. Aggregate:
   result = {
     mean:        mean(scores),
     median:      median(scores),
     std:         std(scores),
     histogram:   histogram(scores),
     by_segment:  group_stats(scores, panel),
     reasons:     [reason_1, ..., reason_N]
   }

Output: result
```

---

## LLM Bias Mitigations

LLMs carry systematic biases that distort scores if left uncorrected. Each bias requires a targeted fix applied at prompt construction time.

### Central tendency bias (score clustering)

LLMs gravitate toward mid-range scores (e.g., 6–8) regardless of actual subject quality, avoiding extremes.

**Fix: few-shot anchoring**

Include calibration examples in the prompt spanning the full score range:

```
Here are examples of how someone with your background has rated things before:
- A poorly lit, cluttered photo of an unremarkable subject: 2/10
- A decent, average-quality subject with no strong features: 5/10
- A striking, professionally presented subject: 9/10

Now rate the following using the same scale.
```

This anchors the LLM to what a 2 and a 9 actually look like for this judge type.

---

### Acquiescence bias (yes-leaning / sycophancy)

LLMs are trained to be agreeable, so they lean toward positive responses. Ask "is this good?" and they tend to say yes.

**Fix: question flipping**

Randomly flip the question polarity for a portion of judge calls, then invert the result:

- Standard framing: *"Rate how attractive this person is."*
- Flipped framing: *"Rate how unattractive this person is."* → invert: `score = 11 − raw_score`

Mixing both framings across the panel cancels out the positive lean.

---

### Position bias (primacy in lists)

LLMs disproportionately favor options that appear early in a list.

**Fix: randomize option order**

Whenever the prompt contains an ordered list (e.g., criteria, ranked attributes, multi-choice options), **shuffle the order independently per judge call**. Primacy effects average out across the full panel.

---

### Verbosity bias

LLMs give higher scores when the subject description is longer and more detailed — more tokens create a subjective sense of richness that inflates ratings regardless of actual quality.

**Fix: normalize subject descriptions**

Before passing a subject to any judge, enforce a fixed token budget by truncating or using a structured input template (e.g., one image + one sentence). Every subject must be presented with the same amount of detail so no subject gets an unfair advantage from richer input.

---

## Open Questions

- **Prompt calibration**: Does the LLM actually shift scores meaningfully across different personas, or does it regress toward a neutral average? Needs empirical validation — run the same subject through many diverse profiles and measure score variance across groups.

- **Dimension correlation**: Real-world dimensions are correlated (e.g., age and income, gender and occupation). Should we model joint distributions (e.g., via a copula) rather than sampling each dimension independently?

- **Panel size `N`**: What `N` yields a stable distribution? Likely 50–200 for most use cases. Lower is cheaper; higher gives more reliable segment breakdowns.

- **Temperature `T`**: Should all judges share the same temperature, or vary by profile type (e.g., lower T for a "professional critic" persona, higher T for a "casual observer")?
