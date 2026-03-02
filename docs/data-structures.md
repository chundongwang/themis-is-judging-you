# Data Structures

## Overview

A **Test** is a one-time judging run. It defines the criteria, the subjects to evaluate, and which population to draw judges from. At runtime, a panel of judges is bootstrapped from the population, each judge scores every subject, and the results are aggregated.

---

## Population

A named, reusable description of a demographic population. Tests reference a population by ID — they do not define distributions inline.

```ts
Population {
  id:          string           // e.g. "us-general", "cn-mainland"
  name:        string           // e.g. "United States General Public"
  description: string
  dimensions:  DimensionConfig[]
}

DimensionConfig {
  name:         string          // e.g. "age", "income_level"
  type:         "continuous"    // sampled via a distribution function
            | "categorical"     // sampled via discrete weights
  distribution: Distribution
}

// For continuous dimensions (e.g. age):
Distribution (continuous) {
  fn:    "normal" | "skewed_normal" | "uniform"
  mu:    number
  sigma: number
  min:   number                // clamp output to valid range
  max:   number
}

// For categorical dimensions (e.g. occupation):
Distribution (categorical) {
  fn:      "weighted"
  weights: { value: string, weight: number }[]
  // weights should sum to 1.0
}
```

> Future: a merge tool could combine two populations into a blended one (e.g. 50% US + 50% CN), producing a new `Population` object.

---

## Judge Profile

A concrete profile sampled from a population at test runtime. Profiles are stored in an index and referenced by ID everywhere else — result records never inline the full profile.

```ts
JudgeProfile {
  id:              string       // stable ID for this sampled profile
  population_id:   string       // which population this was sampled from
  dimensions:      { [key: string]: string | number }
  // e.g. { age: 34, gender: "Female", occupation: "Creative", ... }
}
```

Profiles are generated fresh for each test run. The index lives alongside the run log and is used to reconstruct full profiles during analysis.

---

## Test

The configuration for a judging run. Defines what to judge, how to judge it, and which population to sample judges from.

```ts
Test {
  id:             string
  name:           string
  created_at:     timestamp

  // Judging criteria
  prompt_template: string       // the shared prompt with {{variable}} slots
  scale:           ScaleConfig

  // Panel configuration
  population_id:   string       // references a Population
  panel_size:      number       // N judges to bootstrap

  // Subjects to evaluate
  subjects:        Subject[]
}

ScaleConfig {
  min:    number                // e.g. 1
  max:    number                // e.g. 10
  label:  string                // e.g. "attractiveness", "quality"
}

Subject {
  id:     string
  text:   string                // required — description of the subject
  image:  string | null         // optional — URL or base64
}
```

---

## Run

The output of executing a Test. Contains the aggregated result per subject, plus a reference to the debug log for raw per-judge scores.

```ts
Run {
  id:           string
  test_id:      string
  executed_at:  timestamp
  panel_size:   number          // actual N used (may differ if some calls failed)
  results:      SubjectResult[]
  log_id:       string | null   // reference to RunLog for debugging
}

SubjectResult {
  subject_id:   string
  mean:         number
  median:       number
  std:          number
  histogram:    { bucket: string, count: number }[]
}
```

---

## Run Log (debug)

Stores the raw per-judge scores for a run. Optional — generated when debug mode is enabled. Intended for post-hoc stratified analysis and bias investigation.

```ts
RunLog {
  id:           string
  run_id:       string
  entries:      LogEntry[]
}

LogEntry {
  subject_id:   string
  judge_id:     string          // references JudgeProfile by ID
  score:        number
  reason:       string          // one sentence from the LLM
  prompt:       string          // the exact prompt sent (for auditability)
}
```

> Future: `RunLog` entries are a natural fit for an OLAP store (e.g. Druid, ClickHouse). Each entry is an immutable fact row with subject, judge, and score dimensions — enabling arbitrary slice-and-dice aggregations without re-running.

---

## Entity Relationships

```
Population  ←──────────────  Test
    │                          │
    │ (sampled at runtime)     │
    ▼                          ▼
JudgeProfile ◄──── LogEntry ──► Subject
    │                │
    └── (indexed     └── aggregated into ──► SubjectResult
         by Run)                                  │
                                                  ▼
                                                 Run
```

---

## Data Flow

```
1. Load Test
     ├── fetch Population by population_id
     └── fetch Subjects[]

2. Bootstrap panel
     for i = 1 to panel_size:
       profile_i = sample(Population.dimensions)
       store profile_i in JudgeProfile index

3. Score subjects (all judge × subject pairs in parallel)
     for each (profile_i, subject_j):
       prompt    = render(test.prompt_template, profile_i, subject_j)
       score, reason = llm(prompt, temperature=T)
       append LogEntry { subject_j.id, profile_i.id, score, reason, prompt }

4. Aggregate per subject
     for each subject_j:
       scores = [entry.score for entry in log where entry.subject_id == subject_j.id]
       SubjectResult = { mean, median, std, histogram }

5. Write Run { results, log_id }
```
