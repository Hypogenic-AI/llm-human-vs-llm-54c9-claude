# Resources Catalog

## Summary

This document catalogs all resources gathered for the research project:
**"Do LLMs behave differently when the prompter is human vs another LLM?"**

Resources include academic papers, datasets, and code repositories related to:
- Human vs AI text detection and characterization
- LLM behavioral studies (sycophancy, influence susceptibility)
- Multi-agent LLM systems and communication
- Prompt sensitivity and style effects

---

## Papers

**Total papers downloaded: 9**

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| How Close is ChatGPT to Human Experts? (HC3) | Guo et al. | 2023 | papers/2301.07597_hc3_human_chatgpt_comparison.pdf | Foundation dataset for human vs ChatGPT comparison |
| HC3 Plus: Semantic-Invariant Comparison | Su et al. | 2023 | papers/2309.02731_hc3_plus.pdf | Extended HC3 with semantic-invariant tasks |
| Towards Understanding Sycophancy | Sharma et al. | 2024 | papers/2310.13548_sycophancy_understanding.pdf | **CRITICAL** - Shows LLMs adapt to user preferences |
| Personas in System Prompts | Multiple | 2023 | papers/2311.10054_personas_not_helpful.pdf | Persona prompting effects |
| LLM Multi-Agents Survey | Multiple | 2024 | papers/2402.01680_llm_multi_agents_survey.pdf | LLM-to-LLM communication patterns |
| Quantifying Persona Effect | Multiple | 2024 | papers/2402.10811_persona_effect_quantifying.pdf | Methodology for behavioral measurement |
| AI Text Detection via NLP/ML | Multiple | 2024 | papers/2404.10032_ai_text_detection_nlp_ml.pdf | Detection methods and features |
| RAID: Robust AI Detection | Dugan et al. | 2024 | papers/2405.07940_raid_benchmark.pdf | Largest detection benchmark |
| How Susceptible are LLMs to Influence? | Anagnostidis & Bulian | 2024 | papers/2408.11865_llm_susceptible_influence.pdf | **CRITICAL** - LLMs respond differently to source authority |

See `papers/README.md` for detailed descriptions.

---

## Datasets

**Total datasets downloaded: 3**

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| AI-Human-Text | HuggingFace: andythetechnerd03/AI-human-text | 462K samples | Binary classification | datasets/ai_human_text/ | Human vs AI text with labels |
| Anthropic HH-RLHF | HuggingFace: Anthropic/hh-rlhf | 160K samples | Preference modeling | datasets/hh_rlhf/ | Used for sycophancy analysis |
| AI Text Detection Pile | HuggingFace: artem9k/ai-text-detection-pile | 1.4M samples | Text detection | datasets/ai_text_pile/ | Large-scale essays |

See `datasets/README.md` for detailed descriptions and download instructions.

---

## Code Repositories

**Total repositories cloned: 3**

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| HC3 Detection | github.com/Hello-SimpleAI/chatgpt-comparison-detection | Human vs AI detection | code/hc3_detection/ | Linguistic feature extraction |
| RAID Benchmark | github.com/liamdugan/raid | Detection evaluation | code/raid_benchmark/ | Multiple detectors |
| Sycophancy Eval | github.com/meg-tong/sycophancy-eval | Behavioral evaluation | code/sycophancy_eval/ | Sycophancy measurement |

See `code/README.md` for detailed descriptions.

---

## Resource Gathering Notes

### Search Strategy

1. **Literature Search**: Started with paper-finder (unavailable), then used web search across:
   - arXiv for recent preprints
   - ACL Anthology for NLP papers
   - Semantic Scholar for citation networks
   - Papers with Code for implementations

2. **Dataset Search**: Searched HuggingFace Datasets for:
   - Human vs AI text comparison
   - Preference/RLHF training data
   - Text detection benchmarks

3. **Code Repository Search**: Targeted GitHub repos from:
   - Paper author pages
   - Papers with Code links
   - Direct arXiv citations

### Selection Criteria

**Papers selected based on:**
- Direct relevance to human vs AI text characterization
- Studies on LLM behavioral adaptation to user/source characteristics
- Multi-agent LLM communication patterns
- Recent publication (2023-2024 preferred)
- Availability of code/data

**Datasets selected based on:**
- Labeled human vs AI text with stylistic variety
- Preference data for understanding LLM adaptation
- Size sufficient for statistical analysis
- Easy programmatic access via HuggingFace

**Repositories selected based on:**
- Implementation of methods from key papers
- Reusable code for feature extraction
- Evaluation frameworks

### Challenges Encountered

1. **HC3 Dataset**: Uses deprecated HuggingFace loading script; workaround is to use GitHub repo
2. **RAID Dataset**: Very large (6M+ samples), ran out of disk space; recommend using subsets
3. **Some datasets gated**: NicolaiSivesind/human-vs-machine requires authentication
4. **Paper-finder service**: Unavailable during search; relied on manual web search

### Gaps and Workarounds

**Gap 1**: No existing paper directly tests if LLMs behave differently when prompter is human vs LLM
- **Workaround**: The sycophancy and influence papers provide framework; our experiment will be novel

**Gap 2**: Need controlled prompts with only style differences
- **Workaround**: Use HC3 linguistic features to create human-style vs LLM-style prompt pairs

**Gap 3**: No standardized evaluation metrics for our specific research question
- **Workaround**: Adapt sycophancy evaluation metrics + create new metrics for style mirroring

---

## Recommendations for Experiment Design

Based on gathered resources, we recommend:

### 1. Primary Dataset(s)

**Use AI-Human-Text dataset** (andythetechnerd03/AI-human-text)
- Contains labeled human vs AI text
- Can extract stylistic features to define "human-style" vs "LLM-style"
- Sample size sufficient for statistical power

**Supplementary: HH-RLHF** (Anthropic/hh-rlhf)
- Provides human-AI dialogue patterns
- Useful for understanding natural interaction styles

### 2. Baseline Methods

1. **Control condition**: Neutral prompts with standard formatting
2. **Human-style prompts**: Based on human text characteristics from HC3
   - Shorter sentences
   - Varied vocabulary (higher density)
   - Colloquial language
   - Emotional markers

3. **LLM-style prompts**: Based on ChatGPT characteristics from HC3
   - Longer, structured sentences
   - Lower vocabulary density
   - Formal language
   - Logical connectors

### 3. Evaluation Metrics

From sycophancy research (Sharma et al., 2024):
- Response consistency across prompt variants
- Agreement tendency changes
- Confidence marker analysis

Novel metrics for our research:
- **Style mirroring**: Does output style match input style?
- **Detail level variation**: Response length changes
- **Formality adaptation**: POS and vocabulary analysis of outputs

### 4. Code to Adapt/Reuse

1. **hc3_detection**: Feature extraction for prompt style characterization
2. **sycophancy_eval**: Behavioral evaluation methodology
3. **raid_benchmark**: Detector features for validation

### 5. Experimental Design Recommendations

**Phase 1: Prompt Pair Creation**
1. Select 100-200 questions from standard QA benchmarks (e.g., CommonsenseQA, PIQA)
2. For each question, create two versions:
   - Human-style: rewrite with human linguistic features
   - LLM-style: rewrite with LLM linguistic features
3. Validate style difference using HC3 detection model

**Phase 2: LLM Testing**
1. Query multiple LLMs (GPT-4, Claude, LLaMA, Mistral) with both prompt versions
2. Collect full responses for analysis
3. Run each prompt 3-5 times to assess consistency

**Phase 3: Analysis**
1. Compare response characteristics across prompt styles
2. Statistical tests for significant differences
3. Analyze which behavioral dimensions show most variation

**Phase 4: Interpretation**
1. If differences found: investigate mechanism (style detection? sycophancy? other?)
2. If no differences: document null result, discuss why hypothesis may be incorrect

---

## Quick Reference Links

### HuggingFace Datasets
- AI-Human-Text: https://huggingface.co/datasets/andythetechnerd03/AI-human-text
- HH-RLHF: https://huggingface.co/datasets/Anthropic/hh-rlhf
- HC3: https://huggingface.co/datasets/Hello-SimpleAI/HC3
- RAID: https://huggingface.co/datasets/liamdugan/raid

### GitHub Repositories
- HC3 Detection: https://github.com/Hello-SimpleAI/chatgpt-comparison-detection
- RAID Benchmark: https://github.com/liamdugan/raid
- Sycophancy Eval: https://github.com/meg-tong/sycophancy-eval

### Key arXiv Papers
- HC3: https://arxiv.org/abs/2301.07597
- Sycophancy: https://arxiv.org/abs/2310.13548
- LLM Influence: https://arxiv.org/abs/2408.11865
- RAID: https://arxiv.org/abs/2405.07940
