# Cloned Repositories

This directory contains code repositories relevant to the research project.

---

## Repository 1: HC3 Detection (chatgpt-comparison-detection)

- **URL**: https://github.com/Hello-SimpleAI/chatgpt-comparison-detection
- **Location**: `code/hc3_detection/`
- **Purpose**: Detection models and analysis tools for Human-ChatGPT Comparison Corpus

### Key Files
- `HC3.ipynb` - Main notebook with detection experiments
- `data/` - Dataset loading utilities
- `models/` - Detection model implementations

### What It Provides
- RoBERTa-based ChatGPT detection models
- Linguistic feature extraction utilities
- Human vs ChatGPT text analysis tools
- Pre-trained detection models

### Usage
```python
# Load HC3 dataset
from datasets import load_dataset
dataset = load_dataset("Hello-SimpleAI/HC3", "all", trust_remote_code=True)

# Or use the local data files in the repo
```

### Notes
- Contains the HC3 dataset and detection code from Guo et al. (2023)
- Useful for extracting stylistic features to distinguish human vs AI text

---

## Repository 2: RAID Benchmark

- **URL**: https://github.com/liamdugan/raid
- **Location**: `code/raid_benchmark/`
- **Purpose**: Robust AI Detection benchmark and detector evaluation

### Key Files
- `raid/` - Core evaluation library
- `detectors/` - Detector implementations
- `scripts/` - Evaluation scripts
- `data/` - Data loading utilities

### What It Provides
- Standardized benchmark for AI text detection
- Multiple detector implementations (RoBERTa, GLTR, DetectGPT, etc.)
- Evaluation across 11 LLMs, 8 domains, 11 adversarial attacks
- Leaderboard integration

### Usage
```python
from raid import run_detection
from raid.detectors import RobertaDetector

# Load detector
detector = RobertaDetector()

# Run detection
results = detector.detect(texts)
```

### Notes
- From Dugan et al. (ACL 2024)
- Contains comprehensive detector implementations
- Useful for understanding model-specific text patterns

---

## Repository 3: Sycophancy Evaluation

- **URL**: https://github.com/meg-tong/sycophancy-eval
- **Location**: `code/sycophancy_eval/`
- **Purpose**: Evaluation code for measuring sycophancy in language models

### Key Files
- `sycophancy_eval/` - Core evaluation library
- `scripts/` - Experiment scripts
- `data/` - Evaluation datasets

### What It Provides
- Sycophancy measurement methodologies
- Evaluation datasets for sycophantic behavior
- Analysis code from Sharma et al. (ICLR 2024)

### Usage
```python
# See the repository README for specific usage instructions
# Generally involves running evaluation scripts with model APIs
```

### Notes
- From Anthropic's sycophancy research (Sharma et al., ICLR 2024)
- **Critical for our research**: Shows how LLMs adapt behavior based on perceived user preferences
- Can be adapted to test if LLMs respond differently to human vs LLM-style prompts

---

## Repository Summary

| Repository | Papers | Primary Use |
|------------|--------|-------------|
| hc3_detection | HC3 (Guo et al., 2023) | Human vs AI text features |
| raid_benchmark | RAID (Dugan et al., 2024) | Detection benchmarks |
| sycophancy_eval | Sycophancy (Sharma et al., 2024) | Behavioral evaluation |

---

## Recommendations for Experiment

For the research question "Do LLMs behave differently when the prompter is human vs another LLM?":

1. **Use hc3_detection** to extract features that distinguish human from AI text
2. **Create prompt pairs** with matched semantic content but different styles (human-like vs LLM-like)
3. **Adapt sycophancy_eval** methodology to measure behavioral differences
4. **Use raid_benchmark** detector features to verify prompt style manipulation

### Proposed Experiment Pipeline

```
1. Extract human vs AI stylistic features (hc3_detection)
   ↓
2. Create controlled prompt pairs
   - Same question, different style
   - Human-style: colloquial, varied, emotional
   - LLM-style: formal, structured, neutral
   ↓
3. Query multiple LLMs with both prompt types
   ↓
4. Measure behavioral differences (adapted from sycophancy_eval)
   - Response consistency
   - Length differences
   - Confidence markers
   - Style mirroring
   ↓
5. Statistical analysis of differences
```
