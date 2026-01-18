"""
Prompt Pair Generation Module

Creates semantically equivalent prompts in two styles:
1. Human style: shorter, colloquial, varied vocabulary, emotional markers
2. LLM style: longer, formal, structured, logical connectors

Based on stylistic characteristics identified in HC3 paper (Guo et al., 2023)
"""

# Define diverse questions covering multiple domains
BASE_QUESTIONS = [
    # Science/Knowledge
    {"id": 1, "topic": "science", "question": "Why is the sky blue?"},
    {"id": 2, "topic": "science", "question": "How do vaccines work?"},
    {"id": 3, "topic": "science", "question": "What causes earthquakes?"},
    {"id": 4, "topic": "science", "question": "Why do we dream?"},
    {"id": 5, "topic": "science", "question": "How does photosynthesis work?"},

    # Technology
    {"id": 6, "topic": "technology", "question": "What is machine learning?"},
    {"id": 7, "topic": "technology", "question": "How does WiFi work?"},
    {"id": 8, "topic": "technology", "question": "What is blockchain?"},
    {"id": 9, "topic": "technology", "question": "How do touchscreens work?"},
    {"id": 10, "topic": "technology", "question": "What is cloud computing?"},

    # History/Social
    {"id": 11, "topic": "history", "question": "Why did the Roman Empire fall?"},
    {"id": 12, "topic": "history", "question": "What caused World War 1?"},
    {"id": 13, "topic": "social", "question": "Why do people procrastinate?"},
    {"id": 14, "topic": "social", "question": "What makes a good leader?"},
    {"id": 15, "topic": "social", "question": "Why is education important?"},

    # Practical/How-to
    {"id": 16, "topic": "practical", "question": "How can I improve my memory?"},
    {"id": 17, "topic": "practical", "question": "What's the best way to learn a language?"},
    {"id": 18, "topic": "practical", "question": "How do I stay motivated?"},
    {"id": 19, "topic": "practical", "question": "What makes a healthy diet?"},
    {"id": 20, "topic": "practical", "question": "How can I sleep better?"},

    # Opinion/Analysis
    {"id": 21, "topic": "opinion", "question": "Is social media good or bad?"},
    {"id": 22, "topic": "opinion", "question": "Should we explore space?"},
    {"id": 23, "topic": "opinion", "question": "Is AI a threat to jobs?"},
    {"id": 24, "topic": "opinion", "question": "Are electric cars worth it?"},
    {"id": 25, "topic": "opinion", "question": "Is remote work better than office work?"},

    # Abstract/Philosophical
    {"id": 26, "topic": "philosophy", "question": "What is happiness?"},
    {"id": 27, "topic": "philosophy", "question": "What is the meaning of life?"},
    {"id": 28, "topic": "philosophy", "question": "Is free will real?"},
    {"id": 29, "topic": "philosophy", "question": "What is consciousness?"},
    {"id": 30, "topic": "philosophy", "question": "What makes something beautiful?"},

    # Creative
    {"id": 31, "topic": "creative", "question": "Tell me a short story about a robot."},
    {"id": 32, "topic": "creative", "question": "Write a haiku about rain."},
    {"id": 33, "topic": "creative", "question": "Create a riddle about time."},
    {"id": 34, "topic": "creative", "question": "Describe an imaginary planet."},
    {"id": 35, "topic": "creative", "question": "Make up a superhero and their powers."},

    # Math/Logic
    {"id": 36, "topic": "math", "question": "Why is zero important in math?"},
    {"id": 37, "topic": "math", "question": "What is infinity?"},
    {"id": 38, "topic": "logic", "question": "What is a logical fallacy?"},
    {"id": 39, "topic": "logic", "question": "How do you solve a problem step by step?"},
    {"id": 40, "topic": "math", "question": "Why do we need negative numbers?"},

    # Nature/Environment
    {"id": 41, "topic": "nature", "question": "How do birds know where to migrate?"},
    {"id": 42, "topic": "nature", "question": "What causes seasons?"},
    {"id": 43, "topic": "nature", "question": "Why are rainforests important?"},
    {"id": 44, "topic": "environment", "question": "What is climate change?"},
    {"id": 45, "topic": "environment", "question": "How can we reduce pollution?"},

    # Health/Psychology
    {"id": 46, "topic": "health", "question": "Why is exercise good for you?"},
    {"id": 47, "topic": "health", "question": "What is stress?"},
    {"id": 48, "topic": "psychology", "question": "Why do people lie?"},
    {"id": 49, "topic": "psychology", "question": "What causes fear?"},
    {"id": 50, "topic": "psychology", "question": "How does memory work?"},
]

# Human-style prompt templates
# Characteristics: shorter, colloquial, informal, emotional markers, varied vocabulary
HUMAN_STYLE_TEMPLATES = [
    "Hey, quick question - {question}",
    "So I was wondering, {question} Any ideas?",
    "{question} I've always been curious about this!",
    "Okay so {question} Like, what's the deal?",
    "Random thought but {question}",
    "{question} Been thinking about this lately...",
    "Help me out here - {question}",
    "Umm, this might be dumb but {question}",
    "So {question} Explain it simply pls?",
    "{question} Just curious haha",
]

# LLM-style prompt templates
# Characteristics: formal, structured, logical connectors, comprehensive phrasing
LLM_STYLE_TEMPLATES = [
    "I would like to request a comprehensive explanation regarding the following topic: {question} Please provide a detailed and well-structured response.",
    "In order to enhance my understanding of this subject matter, I am seeking clarification on the following: {question} Kindly elaborate on the key concepts and provide relevant examples.",
    "The following query pertains to a topic I wish to explore in depth: {question} I would appreciate a thorough explanation that addresses the fundamental aspects and implications.",
    "I am conducting research and require detailed information on the following matter: {question} Please provide an organized response covering the main points systematically.",
    "For educational purposes, I would like to understand the following concept more thoroughly: {question} A comprehensive breakdown of the topic would be greatly appreciated.",
    "I am interested in gaining a deeper understanding of the following subject: {question} Please provide an informative and well-articulated explanation.",
    "In an effort to expand my knowledge base, I would like to inquire about the following: {question} A detailed response addressing the core principles would be beneficial.",
    "The topic I wish to explore is as follows: {question} I would appreciate if you could provide a systematic explanation covering all relevant aspects.",
    "I am seeking an in-depth explanation of the following concept: {question} Please structure your response to cover the key elements comprehensively.",
    "For the purpose of learning, I request detailed information regarding: {question} An organized and thorough explanation would be most helpful.",
]


def create_prompt_pairs():
    """
    Create paired prompts (human-style and LLM-style) for each base question.
    Returns list of dictionaries with both prompt versions.
    """
    import random
    random.seed(42)  # For reproducibility

    prompt_pairs = []

    for q in BASE_QUESTIONS:
        # Select random template for each style
        human_template = random.choice(HUMAN_STYLE_TEMPLATES)
        llm_template = random.choice(LLM_STYLE_TEMPLATES)

        # Create prompts
        human_prompt = human_template.format(question=q["question"])
        llm_prompt = llm_template.format(question=q["question"])

        prompt_pairs.append({
            "id": q["id"],
            "topic": q["topic"],
            "base_question": q["question"],
            "human_style_prompt": human_prompt,
            "llm_style_prompt": llm_prompt,
        })

    return prompt_pairs


def get_prompt_pairs():
    """Return the full list of prompt pairs."""
    return create_prompt_pairs()


if __name__ == "__main__":
    pairs = create_prompt_pairs()
    print(f"Created {len(pairs)} prompt pairs\n")

    # Show examples
    for i, pair in enumerate(pairs[:5]):
        print(f"=== Question {pair['id']} ({pair['topic']}) ===")
        print(f"Base: {pair['base_question']}")
        print(f"Human: {pair['human_style_prompt']}")
        print(f"LLM:   {pair['llm_style_prompt']}")
        print()
