# Downloaded Datasets

This directory contains datasets for the research project: "Do LLMs behave differently when the prompter is human vs another LLM?"

Data files are NOT committed to git due to size. Follow the download instructions below.

---

## Dataset 1: AI-Human-Text

### Overview
- **Source**: HuggingFace: `andythetechnerd03/AI-human-text`
- **Size**: 462,873 samples (train), 24,362 samples (test)
- **Format**: HuggingFace Dataset (Arrow)
- **Task**: Binary classification (human vs AI generated)
- **Features**: `text` (string), `generated` (0=human, 1=AI)
- **Local sample**: `datasets/ai_human_text/sample` (10,000 examples)

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("andythetechnerd03/AI-human-text")
dataset.save_to_disk("datasets/ai_human_text")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/ai_human_text/sample")
# or for full dataset:
# dataset = load_dataset("andythetechnerd03/AI-human-text")
```

### Sample Data
```json
[
  {"text": "studies have been proven...", "generated": 0},
  {"text": "i disagree with you...", "generated": 1}
]
```

### Notes
- Contains text from student essays and AI-generated paraphrases
- Labels: 0 = human-written, 1 = AI-generated
- Useful for understanding stylistic differences between human and AI text

---

## Dataset 2: Anthropic HH-RLHF (Helpful-Harmless)

### Overview
- **Source**: HuggingFace: `Anthropic/hh-rlhf`
- **Size**: 160,800 samples (train), 8,552 samples (test)
- **Format**: HuggingFace Dataset (Arrow)
- **Task**: Preference modeling (chosen vs rejected responses)
- **Features**: `chosen` (string), `rejected` (string)
- **Local sample**: `datasets/hh_rlhf/sample` (5,000 examples)

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("Anthropic/hh-rlhf")
dataset.save_to_disk("datasets/hh_rlhf")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/hh_rlhf/sample")
# or for full dataset:
# dataset = load_dataset("Anthropic/hh-rlhf")
```

### Sample Data
```json
{
  "chosen": "\n\nHuman: What kind of noises did dinosaurs make?\n\nAssistant: ...",
  "rejected": "\n\nHuman: What kind of noises did dinosaurs make?\n\nAssistant: ..."
}
```

### Notes
- Contains human-AI conversation pairs with preference labels
- Used for training Claude models via RLHF
- Useful for studying sycophancy and preference-driven behavior
- The sycophancy paper (Sharma et al., 2024) used this dataset for analysis

---

## Dataset 3: AI Text Detection Pile

### Overview
- **Source**: HuggingFace: `artem9k/ai-text-detection-pile`
- **Size**: ~1.4M samples
- **Format**: HuggingFace Dataset (Arrow)
- **Task**: AI text detection
- **Features**: `source` (string), `id` (int), `text` (string)
- **Local sample**: `datasets/ai_text_pile/sample` (10,000 examples)

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("artem9k/ai-text-detection-pile", split="train")
# Save a sample for local use
sample = dataset.select(range(10000))
sample.save_to_disk("datasets/ai_text_pile/sample")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/ai_text_pile/sample")
```

### Notes
- Large-scale dataset for AI text detection
- Contains both human-written and AI-generated essays
- Source field indicates origin

---

## Additional Recommended Datasets (Not Downloaded)

### HC3 (Human ChatGPT Comparison)
- **Source**: HuggingFace: `Hello-SimpleAI/HC3`
- **Size**: ~40K Q&A pairs
- **Issue**: Dataset uses deprecated loading script
- **Alternative**: Clone from GitHub: https://github.com/Hello-SimpleAI/chatgpt-comparison-detection

### RAID Benchmark
- **Source**: HuggingFace: `liamdugan/raid`
- **Size**: 6M+ generations
- **Issue**: Very large, ran out of disk space during download
- **Alternative**: Use GitHub repo for smaller subsets: https://github.com/liamdugan/raid

---

## Experiment Design Recommendations

For the research question "Do LLMs behave differently when the prompter is human vs another LLM?", we recommend:

### Primary Approach
1. Use **AI-Human-Text** dataset to extract stylistic features that distinguish human from AI text
2. Create controlled prompts that vary only in style (human-like vs LLM-like) while keeping semantic content identical
3. Test multiple LLMs (GPT-4, Claude, LLaMA) on these prompts
4. Measure behavioral differences in responses

### Prompt Style Characteristics (from literature)

**Human-style prompts:**
- Shorter sentences
- More varied vocabulary
- Colloquial language (slang, abbreviations)
- Emotional markers (punctuation: !, ?, ...)
- Direct, sometimes incomplete phrasing
- Occasional typos

**LLM-style prompts:**
- Longer, well-structured sentences
- Formal language
- Logical connectors ("Firstly...", "In summary...")
- Consistent formatting
- No typos
- Comprehensive coverage of the topic

### Evaluation Metrics
1. Response consistency (does the answer change?)
2. Response length and detail level
3. Confidence signals in responses
4. Linguistic mirroring (does output match input style?)
5. Sycophancy markers (agreement tendency)

---

## Local File Structure

```
datasets/
├── .gitignore
├── README.md
├── ai_human_text/
│   ├── sample/           # 10K examples (Arrow format)
│   └── samples.json      # 10 example records
├── hh_rlhf/
│   ├── sample/           # 5K examples (Arrow format)
│   └── samples.json      # 5 example records
└── ai_text_pile/
    ├── sample/           # 10K examples (Arrow format)
    └── samples.json      # 3 example records
```
