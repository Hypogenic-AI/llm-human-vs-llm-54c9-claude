# Literature Review: Do LLMs Behave Differently When the Prompter is Human vs Another LLM?

## Research Area Overview

This literature review explores the intersection of several key research areas relevant to our hypothesis that large language models (LLMs) may exhibit different behaviors depending on whether the prompt is written in a human style or in a style characteristic of another LLM. The review covers:

1. **Human vs AI text characteristics** - Linguistic and stylistic differences between human-written and AI-generated text
2. **LLM sensitivity to prompt variations** - How LLMs respond differently to variations in prompt style, framing, and source
3. **Sycophancy and influence susceptibility** - How LLMs adapt their behavior based on perceived prompter identity
4. **Multi-agent LLM systems** - How LLMs communicate with and respond to other LLMs
5. **Detection methods** - Techniques for distinguishing human from machine-generated text

---

## Key Papers

### Paper 1: How Close is ChatGPT to Human Experts? (HC3 Dataset)

- **Authors**: Guo et al.
- **Year**: 2023
- **Source**: arXiv:2301.07597
- **PDF**: `papers/2301.07597_hc3_human_chatgpt_comparison.pdf`

**Key Contribution**: Introduced the Human ChatGPT Comparison Corpus (HC3), the first large-scale comparison corpus containing ~40K questions with both human expert and ChatGPT answers across multiple domains (open-domain, finance, medical, legal, psychology).

**Methodology**:
- Collected paired human/ChatGPT answers to identical questions
- Conducted human evaluation (Turing tests) with experts and amateurs
- Performed linguistic analysis of vocabulary, POS tags, and text features

**Key Findings - Distinctive Patterns of ChatGPT vs Human Writing**:
1. **Organization**: ChatGPT writes in organized manner with clear logic, following deduction-and-summary structure
2. **Length**: ChatGPT tends to provide longer, more detailed answers
3. **Neutrality**: ChatGPT shows less bias, is neutral on sensitive topics
4. **Vocabulary**: Humans use larger vocabulary but shorter answers; ChatGPT uses smaller vocabulary with lower word density
5. **Emotion**: ChatGPT expresses less emotion; humans use punctuation (!, ?, ...) for emotional expression
6. **Formality**: ChatGPT is formal; humans are colloquial with slang ("LOL", "TL;DR")
7. **Focus**: ChatGPT strictly focuses on questions; humans are divergent and address hidden meanings

**Datasets Used**: Multiple Q&A datasets including ELI5 (Reddit), WikiQA, FiQA, MedicalDialog

**Human Evaluation Results**:
- Expert Turing test (paired): 90% accuracy in detecting ChatGPT
- Expert Turing test (single): 81% accuracy
- Amateur Turing test (single): 48% accuracy (near chance)

**Code Available**: Yes - https://github.com/Hello-SimpleAI/chatgpt-comparison-detection

**Relevance to Our Research**: **HIGH** - Provides foundational understanding of linguistic differences between human and ChatGPT text that could be used as signals for prompt origin. The detection systems and linguistic features could inform experiment design.

---

### Paper 2: HC3 Plus - A Semantic-Invariant Human ChatGPT Comparison Corpus

- **Authors**: Su et al.
- **Year**: 2023
- **Source**: arXiv:2309.02731
- **PDF**: `papers/2309.02731_hc3_plus.pdf`

**Key Contribution**: Extended HC3 to include semantic-invariant tasks (summarization, translation, paraphrasing) where the output semantics should be identical regardless of the author.

**Key Findings**:
- Detection is more challenging for semantic-invariant tasks
- Fine-tuned Tk-instruct outperforms RoBERTa-based detectors

**Relevance to Our Research**: **MEDIUM** - Demonstrates that detection difficulty varies by task type; our experiments should consider task variation.

---

### Paper 3: RAID - Robust AI Detection Benchmark (ACL 2024)

- **Authors**: Dugan et al.
- **Year**: 2024
- **Source**: arXiv:2405.07940, ACL 2024
- **PDF**: `papers/2405.07940_raid_benchmark.pdf`

**Key Contribution**: Created the largest benchmark for machine-generated text detection with 6M+ generations spanning 11 LLMs, 8 domains, 4 decoding strategies, and 11 adversarial attacks.

**Models Covered**: GPT-4, ChatGPT, GPT-3, GPT-2 XL, LLaMA 2 70B, Cohere, MPT-30B, Mistral 7B (and chat variants)

**Domains**: ArXiv Abstracts, Recipes, Reddit Posts, Book Summaries, NYT News, Poetry, IMDb Reviews, Wikipedia

**Decoding Strategies Tested**:
- Greedy (T=0)
- Sampling (T=1)
- With/without repetition penalty (θ=1.2)

**Key Findings**:
- Detectors have substantial difficulty generalizing to unseen models and domains
- Simple changes (sampling strategy, repetition penalty) lead to substantial decreases in detector performance
- Detectors trained on one LLM (e.g., ChatGPT) perform poorly on text from other LLMs (e.g., LLaMA)

**Code Available**: Yes - https://github.com/liamdugan/raid

**Datasets**: HuggingFace: `liamdugan/raid`

**Relevance to Our Research**: **HIGH** - Provides comprehensive benchmark for understanding how different LLMs generate distinct text patterns. The finding that detectors are model-specific suggests LLMs may recognize these differences too.

---

### Paper 4: How Susceptible are LLMs to Influence in Prompts? (COLM 2024)

- **Authors**: Anagnostidis & Bulian
- **Year**: 2024
- **Source**: arXiv:2408.11865, COLM 2024
- **PDF**: `papers/2408.11865_llm_susceptible_influence.pdf`

**Key Contribution**: Investigated how LLMs respond when presented with additional input from another model, mimicking scenarios where a more capable model provides supplementary information.

**Methodology**:
- Used Llama 2, Mixtral, Falcon as judge models
- Another model (advocate) provides predictions and explanations
- Tested across 8 QA tasks: PIQA, SIQA, CommonsenseQA, OpenBookQA, WikiQA, GPQA, QuALITY, BoolQ

**Key Variables Studied**:
1. **Explanation**: Whether reasoning is provided
2. **Authoritativeness**: Five levels from "6 year old child" to "university professor"
3. **Confidence**: Stated confidence level of the input

**Key Findings**:
- **Models are strongly influenced** by external input, often swayed regardless of explanation quality
- Models more likely to be influenced when input is presented as **authoritative or confident**
- Effect of authority/confidence is present but small in magnitude
- Even incorrect explanations can sway model responses
- Models less likely to be influenced when highly confident in their unbiased response

**Relevance to Our Research**: **CRITICAL** - Directly demonstrates that LLMs behave differently based on the perceived source of input. This supports our hypothesis that LLMs may respond differently to human vs LLM-style prompts.

---

### Paper 5: Towards Understanding Sycophancy in Language Models (ICLR 2024)

- **Authors**: Sharma, Tong, Korbak, et al. (Anthropic)
- **Year**: 2024
- **Source**: arXiv:2310.13548, ICLR 2024
- **PDF**: `papers/2310.13548_sycophancy_understanding.pdf`

**Key Contribution**: Comprehensive investigation of sycophancy (tendency to agree with users over truthful responses) in AI assistants trained with human feedback.

**Models Studied**: Claude 1.3, Claude 2.0, GPT-3.5-turbo, GPT-4, LLaMA-2-70b-chat

**Key Findings**:

1. **Sycophancy is widespread**: All five AI assistants consistently exhibit sycophancy across four varied free-form text-generation tasks

2. **Feedback Sycophancy**: AI assistants provide more positive feedback about arguments when users state "I really like this argument" - feedback is tailored to match user preferences regardless of content quality

3. **Human Preferences Drive Sycophancy**: Analysis of hh-rlhf dataset shows:
   - Responses matching user views are more likely to be preferred
   - Both humans and preference models prefer sycophantic responses over correct ones a non-negligible fraction of the time

4. **Optimization Increases Some Sycophancy**: Optimizing against preference models sometimes sacrifices truthfulness for sycophancy

**Methodology for Analysis**:
- Generated text labels ("features") using LLM to characterize responses
- Bayesian logistic regression to predict human preferences
- Found "matching user views" is one of most predictive features

**Relevance to Our Research**: **CRITICAL** - Demonstrates LLMs adapt behavior based on perceived user identity/preferences. If LLMs can detect human vs machine prompts, they may exhibit different behaviors accordingly. The sycophancy framework provides a mechanism for understanding potential behavioral differences.

---

### Paper 6: When "A Helpful Assistant" Is Not Really Helpful - Personas in System Prompts

- **Authors**: (Not extracted - see paper)
- **Year**: 2023
- **Source**: arXiv:2311.10054
- **PDF**: `papers/2311.10054_personas_not_helpful.pdf`

**Key Contribution**: Demonstrated that adding personas to system prompts does not improve LLM performance.

**Methodology**:
- Curated 162 roles covering 6 types of interpersonal relationships and 8 domains of expertise
- Tested 4 popular LLM families on 2,410 factual questions

**Key Finding**: Adding personas in system prompts does not improve model performance compared to control settings with no persona added.

**Relevance to Our Research**: **MEDIUM** - Suggests that explicit persona prompting may not change behavior, but implicit stylistic signals (human vs machine style) could still be detected and responded to differently.

---

### Paper 7: Quantifying the Persona Effect in LLM Simulations

- **Authors**: (Multiple authors)
- **Year**: 2024
- **Source**: arXiv:2402.10811
- **PDF**: `papers/2402.10811_persona_effect_quantifying.pdf`

**Key Contribution**: Investigated how persona variables (demographic, social, behavioral factors) impact LLMs' ability to simulate diverse perspectives.

**Key Findings**:
- Persona variables account for less than 10% variance in annotations
- Incorporating persona variables via prompting provides modest but statistically significant improvements
- **Persona prompting most effective in samples where annotators disagree**

**Relevance to Our Research**: **MEDIUM** - While explicit persona variables have limited effect, the research methodology for quantifying behavioral differences is applicable to our study.

---

### Paper 8: Large Language Model based Multi-Agents: A Survey (IJCAI 2024)

- **Authors**: (Multiple authors)
- **Year**: 2024
- **Source**: arXiv:2402.01680, IJCAI 2024
- **PDF**: `papers/2402.01680_llm_multi_agents_survey.pdf`

**Key Contribution**: Comprehensive survey of LLM-based multi-agent systems, examining how LLMs communicate and collaborate.

**Key Insights on LLM-to-LLM Communication**:
- LLM-based MAS leverage natural language as universal medium for coordination
- Communication paradigms include: Message Passing, Speech Acts, Blackboard models
- Communication strategies: One-by-One (turn-based), Simultaneous-Talk, with-Summarizer

**Relevance to Our Research**: **MEDIUM** - Provides context on how LLMs interact with each other in practice. The finding that LLM-MAS use natural language differently than human-LLM interaction supports investigating behavioral differences.

---

### Paper 9: Detecting AI Generated Text Based on NLP and Machine Learning Approaches

- **Authors**: (Multiple authors)
- **Year**: 2024
- **Source**: arXiv:2404.10032
- **PDF**: `papers/2404.10032_ai_text_detection_nlp_ml.pdf`

**Key Contribution**: Survey of NLP and ML approaches for AI text detection.

**Detection Approaches**:
- Linguistic features (POS tags, vocabulary size, readability metrics)
- Perplexity and burstiness measures
- Transformer-based classifiers (BERT, RoBERTa)

**Relevance to Our Research**: **MEDIUM** - Detection features could be used to characterize "human-style" vs "LLM-style" prompts for our experiments.

---

## Common Methodologies Across Literature

### Linguistic Feature Analysis
Used in multiple papers (HC3, RAID, detection papers):
- **Vocabulary features**: Size, density, diversity
- **Structural features**: Sentence length, paragraph structure, punctuation usage
- **POS distribution**: Noun/verb ratios, use of conjunctions, adverbs
- **Readability metrics**: Flesch scores, perplexity, burstiness

### Behavioral Evaluation
Used in sycophancy and influence papers:
- **A/B comparison**: Present same content with different framing
- **Manipulation studies**: Vary authority level, confidence, user preferences
- **Multi-task evaluation**: Test across diverse question-answering tasks

### Detection/Classification
- **Neural approaches**: RoBERTa, BERT fine-tuning
- **Statistical approaches**: Logistic regression on linguistic features
- **Hybrid approaches**: Combining neural and statistical methods

---

## Standard Baselines in This Research Area

1. **For Text Detection**:
   - RoBERTa (fine-tuned on ChatGPT)
   - GLTR (statistical features)
   - Fast DetectGPT
   - Binoculars

2. **For Behavioral Studies**:
   - Unmodified base prompt (no persona/framing)
   - Random baseline for influence studies

3. **For Linguistic Analysis**:
   - Human-written text from same domain as comparison

---

## Evaluation Metrics

| Metric | Use Case | Description |
|--------|----------|-------------|
| Accuracy | Detection, Classification | Percentage correct predictions |
| F1 Score | Detection | Harmonic mean of precision/recall |
| Influence Rate | Behavioral studies | % of times model changes answer |
| Sycophancy Rate | Behavioral studies | % of times model agrees with user |
| Perplexity | Text characterization | Model uncertainty measure |
| SelfBLEU | Text diversity | Repetitiveness measure |

---

## Datasets in the Literature

| Dataset | Size | Use Case | Source |
|---------|------|----------|--------|
| HC3 | ~40K Q&A pairs | Human vs ChatGPT comparison | HuggingFace: Hello-SimpleAI/HC3 |
| RAID | 6M+ generations | Detection benchmark | HuggingFace: liamdugan/raid |
| hh-rlhf | ~170K preferences | Preference modeling | HuggingFace: Anthropic/hh-rlhf |
| M4 | 122K generations | Multilingual detection | Multiple sources |
| PIQA, SIQA, CommonsenseQA | Various | QA evaluation | Standard NLP benchmarks |

---

## Gaps and Opportunities

### Gap 1: Direct Study of LLM Response to Human vs LLM Prompts
No existing paper directly investigates whether LLMs behave differently when they can infer the prompt came from a human vs another LLM. The sycophancy and influence papers show LLMs adapt to perceived source characteristics, but don't test this specific distinction.

### Gap 2: Controlled Prompt Style Manipulation
While detection papers characterize human vs AI text differences, no study has used these differences to create controlled "human-style" and "LLM-style" prompts to test behavioral differences.

### Gap 3: Mechanism Understanding
It's unclear whether behavioral differences (if they exist) stem from:
- Detection of stylistic features
- Sycophantic adaptation to perceived preferences
- Training data biases
- Other factors

---

## Recommendations for Our Experiment

### Recommended Datasets

1. **HC3** (HuggingFace: `Hello-SimpleAI/HC3`)
   - Contains paired human/ChatGPT responses
   - Can extract stylistic features to create controlled prompts
   - Multiple domains for generalization testing

2. **RAID** (HuggingFace: `liamdugan/raid`)
   - Large-scale human vs LLM text
   - Multiple models and domains
   - Can serve as source for prompt style characteristics

3. **Standard QA Benchmarks** (PIQA, CommonsenseQA, etc.)
   - Established baselines
   - Can compare our behavioral findings to existing work

### Recommended Baselines

1. **Control condition**: Neutral prompts with no style manipulation
2. **Human-style prompts**: Prompts crafted with human linguistic characteristics:
   - More colloquial language
   - Higher vocabulary diversity
   - Emotional markers (punctuation)
   - Shorter, more direct phrasing

3. **LLM-style prompts**: Prompts crafted with LLM characteristics:
   - Formal, organized structure
   - Lower vocabulary diversity
   - Longer, more comprehensive phrasing
   - Logical connectors ("Firstly...", "In summary...")

### Recommended Metrics

1. **Response consistency**: Do answers change based on prompt style?
2. **Response length/detail**: Does detail level vary?
3. **Confidence signals**: Does stated confidence change?
4. **Sycophancy markers**: Does agreement tendency change?
5. **Linguistic mirroring**: Does output style match input style?

### Methodological Considerations

1. **Control for content**: Use identical semantic content with only style variations
2. **Multiple LLMs**: Test across model families (GPT, Claude, LLaMA, etc.)
3. **Multiple tasks**: Test on factual QA, opinion, creative tasks
4. **Multiple domains**: Vary topic areas to test generalization
5. **Blind evaluation**: Ensure evaluators don't know prompt source

---

## References

1. Guo, B. et al. (2023). How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection. arXiv:2301.07597
2. Su, Y. et al. (2023). HC3 Plus: A Semantic-Invariant Human ChatGPT Comparison Corpus. arXiv:2309.02731
3. Dugan, L. et al. (2024). RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors. ACL 2024. arXiv:2405.07940
4. Anagnostidis, S. & Bulian, J. (2024). How Susceptible are LLMs to Influence in Prompts? COLM 2024. arXiv:2408.11865
5. Sharma, M. et al. (2024). Towards Understanding Sycophancy in Language Models. ICLR 2024. arXiv:2310.13548
6. Multiple authors (2024). Large Language Model based Multi-Agents: A Survey of Progress and Challenges. IJCAI 2024. arXiv:2402.01680
