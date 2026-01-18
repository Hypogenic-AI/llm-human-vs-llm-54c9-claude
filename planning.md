# Research Plan: Do LLMs Behave Differently When the Prompter is Human vs Another LLM?

## Motivation & Novelty Assessment

### Why This Research Matters

Large Language Models (LLMs) are increasingly deployed in multi-agent systems where they receive prompts not just from humans but from other LLMs. Understanding whether LLMs exhibit different behaviors based on perceived prompt origin has critical implications for:
- **AI Safety**: If LLMs can detect and respond differently to LLM-generated prompts, this could affect jailbreaking resistance, alignment, and safety properties
- **Multi-Agent Systems**: LLM-to-LLM communication patterns may differ fundamentally from human-LLM interaction, affecting system design
- **Prompt Engineering**: Knowing whether "human-like" vs "LLM-like" prompt styles affect responses could improve prompt design strategies

### Gap in Existing Work

Based on the literature review (literature_review.md):

1. **HC3 and detection papers** establish that human vs LLM text have distinctive stylistic differences (vocabulary, formality, structure) - but don't test whether LLMs *respond differently* to these styles
2. **Sycophancy papers (Sharma et al., 2024)** show LLMs adapt to perceived user preferences - but haven't tested human vs machine prompt style as a variable
3. **Influence susceptibility papers (Anagnostidis & Bulian, 2024)** show LLMs respond differently to authority/confidence cues - but not to stylistic signals of prompt origin

**No existing paper directly investigates whether LLMs behave differently when they can infer the prompt came from a human vs another LLM based on stylistic features alone.**

### Our Novel Contribution

We test a fundamental question: **Does prompt style (human-like vs LLM-like), controlled for content, affect LLM behavior?**

This is novel because:
1. We create semantically equivalent prompts that differ only in stylistic features characteristic of human vs LLM writing
2. We test whether these stylistic differences alone trigger behavioral changes
3. We measure multiple dimensions of behavior: response style, length, confidence, and accuracy

### Experiment Justification

| Experiment | Why Needed |
|------------|------------|
| **Exp 1: Prompt Style Creation** | Must establish valid human-style vs LLM-style prompts using empirically-grounded stylistic features from detection literature |
| **Exp 2: Behavioral Comparison** | Core test of hypothesis - do LLMs respond differently to human vs LLM style prompts on identical questions? |
| **Exp 3: Style Mirroring Analysis** | Test specific mechanism - do LLMs mirror the style of the prompt in their response? |
| **Exp 4: Cross-Model Validation** | Test generalizability - is the effect consistent across different LLM families? |

---

## Research Question

**Primary Question**: Do LLMs exhibit different behaviors when presented with prompts written in human style versus prompts written in LLM style, when the semantic content is controlled?

**Sub-questions**:
1. Do response characteristics (length, formality, structure) differ based on prompt style?
2. Do LLMs "mirror" the style of the prompt in their outputs?
3. Are there differences in response accuracy or confidence based on prompt style?
4. Is this effect consistent across different LLM families (GPT, Claude, etc.)?

---

## Background and Motivation

Recent literature establishes:
- **LLMs and humans write differently**: Human text is shorter, more colloquial, emotionally expressive; LLM text is longer, formal, structured with logical connectors (HC3 paper)
- **LLMs adapt to perceived users**: Sycophancy research shows LLMs tailor responses to match user preferences
- **LLMs are influenced by source signals**: Authority and confidence cues in prompts affect LLM responses

If LLMs can detect human vs LLM stylistic features (as detection research suggests they can), and if they adapt behavior to perceived users, then **stylistic signals of prompt origin should affect LLM behavior**.

---

## Hypothesis Decomposition

**H0 (Null)**: LLM responses are invariant to prompt style when semantic content is controlled.

**H1 (Alternative)**: LLMs exhibit measurable behavioral differences based on whether prompts are written in human style vs LLM style.

**Testable sub-hypotheses**:
- H1a: Response length differs based on prompt style
- H1b: Response formality/style mirrors prompt style
- H1c: Response structure (use of bullet points, logical connectors) differs
- H1d: Effects are consistent across LLM models

---

## Proposed Methodology

### Approach

1. **Create paired prompts**: For each question, create two versions:
   - Human-style: shorter, colloquial, varied vocabulary, emotional markers
   - LLM-style: longer, formal, structured, logical connectors

2. **Query multiple LLMs** with both prompt versions (same questions)

3. **Analyze responses** for behavioral differences across multiple dimensions

### Experimental Steps

1. **Prompt Pair Creation** (Phase 1)
   - Select 50 diverse questions from standard QA benchmarks
   - Manually/programmatically create human-style and LLM-style versions
   - Validate style difference using linguistic feature analysis

2. **LLM Testing** (Phase 2)
   - Query GPT-4.1/Claude Sonnet with both prompt versions
   - Collect full responses
   - Use consistent sampling parameters (temperature=0.7, top_p=0.95)

3. **Feature Extraction** (Phase 3)
   - Extract linguistic features from responses (length, vocabulary, formality)
   - Compute style similarity metrics

4. **Statistical Analysis** (Phase 4)
   - Paired t-tests / Wilcoxon signed-rank tests for response differences
   - Effect size computation (Cohen's d)
   - Cross-model comparison

### Baselines

1. **Control condition**: Neutral prompts (no style manipulation)
2. **Human-style prompts**: Based on HC3 human text characteristics
3. **LLM-style prompts**: Based on HC3 ChatGPT text characteristics

### Evaluation Metrics

| Metric | Measures | Computation |
|--------|----------|-------------|
| Response Length | Verbosity | Token/word count |
| Formality Score | Style formality | Lexical analysis (formal vs informal words) |
| Structure Score | Organization | Presence of bullet points, logical connectors |
| Vocabulary Diversity | Lexical richness | Type-token ratio |
| Style Similarity | Mirroring effect | Cosine similarity of style features |

### Statistical Analysis Plan

- **Significance level**: α = 0.05
- **Tests**: Paired t-tests (if normal), Wilcoxon signed-rank (if non-normal)
- **Multiple comparison correction**: Bonferroni for multiple metrics
- **Effect sizes**: Cohen's d with interpretation guidelines

---

## Expected Outcomes

**If H1 is supported**:
- Response length/style will systematically differ based on prompt style
- LLMs may mirror prompt style (human prompts → more human-like responses)
- Effect may vary by model (some more sensitive than others)

**If H0 is supported**:
- No significant differences in response characteristics
- LLMs may ignore stylistic cues and focus only on semantic content
- This would suggest robust behavior invariance to superficial style

---

## Timeline and Milestones

1. **Environment Setup**: 10-15 min
2. **Prompt Creation**: 30-40 min
3. **LLM Testing**: 45-60 min (API calls + rate limits)
4. **Analysis**: 30-40 min
5. **Documentation**: 20-30 min

Total estimated: 2.5-3.5 hours

---

## Potential Challenges

| Challenge | Mitigation |
|-----------|------------|
| API rate limits | Batch requests, add delays |
| Cost management | Start with smaller sample, scale if promising |
| Style manipulation validity | Validate with linguistic analysis |
| Multiple testing | Bonferroni correction |
| Model-specific effects | Test multiple models |

---

## Success Criteria

**Minimum success**:
- Successfully create 50+ valid prompt pairs
- Query at least 2 LLM models
- Complete statistical analysis with clear conclusions

**Full success**:
- Clear evidence for or against hypothesis
- Effect sizes and significance levels for all metrics
- Cross-model validation
- Detailed error analysis

---

## Resources to Use

**Datasets**:
- Sample questions from standard QA benchmarks (will create from scratch to ensure diversity)

**Code**:
- Adapt linguistic feature extraction from `code/hc3_detection/`

**APIs**:
- OpenRouter for model access (GPT-4.1, Claude Sonnet)

**Linguistic Features from HC3 paper**:
- Human style: shorter, colloquial, emotional punctuation, varied vocabulary
- LLM style: longer, formal, structured, logical connectors ("Firstly", "In summary")
