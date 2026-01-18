# Do LLMs Behave Differently When the Prompter is Human vs Another LLM?

This research project investigates whether Large Language Models (LLMs) exhibit different behaviors when prompted with human-style versus LLM-style prompts, controlling for semantic content.

## Key Findings

**Yes, LLMs significantly alter their behavior based on prompt style:**

- **+66% longer responses** when given formal LLM-style prompts (Cohen's d = 2.07, p < 0.0001)
- **+120% more bullet points** and structured formatting in LLM-style response conditions
- **Lower readability** (Flesch Reading Ease drops from 38.8 to 6.4)
- **Effect is consistent** across GPT-4.1-mini and Claude Sonnet 4

This suggests LLMs engage in "style mirroring" - adapting their output style to match the formality and structure of the input prompt.

## Quick Results

| Metric | Human-Style Prompt | LLM-Style Prompt | Change |
|--------|-------------------|------------------|--------|
| Word Count | 195 words | 323 words | +66% |
| Bullet Points | 8.5 | 18.6 | +119% |
| Reading Level | Grade 13 | Grade 20 | +52% |
| Vocabulary Diversity | 0.72 TTR | 0.64 TTR | -11% |

## Practical Implications

1. **Prompt Engineering**: Style framing matters, not just semantic content
2. **Multi-Agent Systems**: LLM-to-LLM communication may naturally produce more formal outputs
3. **AI Safety**: Prompt style should be controlled in evaluations

## Repository Structure

```
.
├── REPORT.md              # Full research report with methodology and findings
├── README.md              # This file
├── planning.md            # Research plan and hypothesis decomposition
├── src/
│   ├── prompt_pairs.py    # Prompt generation with human/LLM style templates
│   ├── run_experiment.py  # Main experiment runner (API calls)
│   └── analyze_results.py # Statistical analysis and visualization
├── results/
│   ├── experiment_results.json    # Raw API responses
│   ├── statistical_analysis.csv   # Statistical test results
│   ├── features_extracted.csv     # Extracted linguistic features
│   └── plots/                     # Visualization figures
├── papers/                # Downloaded research papers
├── datasets/              # Downloaded datasets (not used directly)
├── code/                  # Cloned reference repositories
├── literature_review.md   # Pre-gathered literature review
└── resources.md           # Resource catalog
```

## How to Reproduce

### 1. Environment Setup

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install requests openai httpx numpy pandas scipy matplotlib seaborn tqdm textstat
```

### 2. Set API Key

```bash
export OPENROUTER_API_KEY="your-key-here"
```

### 3. Run Experiment

```bash
python src/run_experiment.py
```

### 4. Analyze Results

```bash
python src/analyze_results.py
```

## Models Tested

- **GPT-4.1-mini** (OpenAI via OpenRouter)
- **Claude Sonnet 4** (Anthropic via OpenRouter)

## Methodology

1. Created 50 diverse questions across 14 topic categories
2. Generated paired prompts: human-style (casual, short) and LLM-style (formal, comprehensive)
3. Queried each model with both prompt versions
4. Extracted 10 linguistic features from responses
5. Computed paired statistical tests with Bonferroni correction

## Citation

If you use this research, please cite:

```
@article{llm_human_vs_llm_2026,
  title={Do LLMs Behave Differently When the Prompter is Human vs Another LLM?},
  year={2026},
  note={Research project investigating LLM style sensitivity}
}
```

## License

Research code released under MIT License.

---

*See [REPORT.md](REPORT.md) for the full research report with detailed methodology, analysis, and discussion.*
