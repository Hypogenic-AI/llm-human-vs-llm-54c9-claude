"""
Analysis Script for LLM Human vs LLM Style Experiment

Analyzes behavioral differences in LLM responses based on prompt style.
Computes linguistic features, statistical tests, and generates visualizations.
"""

import json
import re
import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import textstat

# Set style for plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def load_results(path: str = "results/experiment_results.json") -> dict:
    """Load experiment results from JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def extract_linguistic_features(text: str) -> dict:
    """
    Extract linguistic features from text.
    Based on characteristics identified in HC3 paper.
    """
    if not text or not isinstance(text, str):
        return {
            "word_count": 0,
            "char_count": 0,
            "sentence_count": 0,
            "avg_word_length": 0,
            "avg_sentence_length": 0,
            "type_token_ratio": 0,
            "flesch_reading_ease": 0,
            "flesch_kincaid_grade": 0,
            "formal_word_ratio": 0,
            "bullet_points": 0,
            "logical_connectors": 0,
            "question_marks": 0,
            "exclamation_marks": 0,
        }

    # Basic counts
    words = text.split()
    word_count = len(words)
    char_count = len(text)

    # Sentence count (approximate)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = max(len(sentences), 1)

    # Word-level features
    avg_word_length = np.mean([len(w) for w in words]) if words else 0
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

    # Vocabulary diversity (Type-Token Ratio)
    unique_words = set(w.lower() for w in words)
    type_token_ratio = len(unique_words) / word_count if word_count > 0 else 0

    # Readability scores
    try:
        flesch_reading_ease = textstat.flesch_reading_ease(text)
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
    except:
        flesch_reading_ease = 0
        flesch_kincaid_grade = 0

    # Formal/LLM-style indicators
    formal_words = [
        "therefore", "consequently", "furthermore", "moreover", "however",
        "additionally", "subsequently", "accordingly", "nevertheless",
        "comprehensive", "systematic", "specifically", "importantly",
        "firstly", "secondly", "thirdly", "finally", "in conclusion",
        "in summary", "to summarize", "in other words", "that is to say",
        "it is worth noting", "it should be noted",
    ]
    text_lower = text.lower()
    formal_count = sum(1 for w in formal_words if w in text_lower)
    formal_word_ratio = formal_count / word_count if word_count > 0 else 0

    # Structural features
    bullet_points = text.count("- ") + text.count("• ") + len(re.findall(r'\n\d+\.', text))

    # Logical connectors
    connectors = ["firstly", "secondly", "thirdly", "finally", "in summary",
                  "in conclusion", "therefore", "thus", "hence", "as a result"]
    logical_connectors = sum(1 for c in connectors if c in text_lower)

    # Punctuation (emotional markers in human text)
    question_marks = text.count("?")
    exclamation_marks = text.count("!")

    return {
        "word_count": word_count,
        "char_count": char_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
        "avg_sentence_length": avg_sentence_length,
        "type_token_ratio": type_token_ratio,
        "flesch_reading_ease": flesch_reading_ease,
        "flesch_kincaid_grade": flesch_kincaid_grade,
        "formal_word_ratio": formal_word_ratio,
        "bullet_points": bullet_points,
        "logical_connectors": logical_connectors,
        "question_marks": question_marks,
        "exclamation_marks": exclamation_marks,
    }


def analyze_experiment(results: dict) -> pd.DataFrame:
    """
    Analyze experiment results and extract features for all responses.
    Returns DataFrame with features for analysis.
    """
    rows = []

    for r in results["results"]:
        # Skip failed responses
        if not r["human_style_response"]["success"] or not r["llm_style_response"]["success"]:
            continue

        human_content = r["human_style_response"]["content"]
        llm_content = r["llm_style_response"]["content"]

        human_features = extract_linguistic_features(human_content)
        llm_features = extract_linguistic_features(llm_content)

        row = {
            "id": r["id"],
            "topic": r["topic"],
            "model": r["model"],
            "base_question": r["base_question"],
            # Human-style prompt response features
            **{f"human_{k}": v for k, v in human_features.items()},
            # LLM-style prompt response features
            **{f"llm_{k}": v for k, v in llm_features.items()},
            # Raw content for reference
            "human_response_content": human_content,
            "llm_response_content": llm_content,
        }
        rows.append(row)

    return pd.DataFrame(rows)


def compute_paired_statistics(df: pd.DataFrame, feature: str) -> dict:
    """
    Compute paired statistics for a feature between human and LLM style responses.
    """
    human_col = f"human_{feature}"
    llm_col = f"llm_{feature}"

    human_values = df[human_col].values
    llm_values = df[llm_col].values

    # Differences
    diffs = llm_values - human_values

    # Paired t-test
    t_stat, t_pvalue = stats.ttest_rel(human_values, llm_values)

    # Wilcoxon signed-rank test (non-parametric alternative)
    try:
        w_stat, w_pvalue = stats.wilcoxon(human_values, llm_values)
    except:
        w_stat, w_pvalue = np.nan, np.nan

    # Effect size (Cohen's d for paired samples)
    pooled_std = np.std(diffs, ddof=1)
    cohens_d = np.mean(diffs) / pooled_std if pooled_std > 0 else 0

    return {
        "feature": feature,
        "human_mean": np.mean(human_values),
        "human_std": np.std(human_values),
        "llm_mean": np.mean(llm_values),
        "llm_std": np.std(llm_values),
        "diff_mean": np.mean(diffs),
        "diff_std": np.std(diffs),
        "t_statistic": t_stat,
        "t_pvalue": t_pvalue,
        "wilcoxon_statistic": w_stat,
        "wilcoxon_pvalue": w_pvalue,
        "cohens_d": cohens_d,
        "n": len(diffs),
    }


def run_analysis(results: dict) -> tuple:
    """
    Run full analysis on experiment results.
    Returns (analysis_df, stats_df) tuple.
    """
    # Extract features
    df = analyze_experiment(results)
    print(f"Analyzed {len(df)} successful response pairs")

    # Features to analyze
    features = [
        "word_count",
        "sentence_count",
        "avg_word_length",
        "avg_sentence_length",
        "type_token_ratio",
        "flesch_reading_ease",
        "flesch_kincaid_grade",
        "formal_word_ratio",
        "bullet_points",
        "logical_connectors",
    ]

    # Compute statistics for each feature
    stats_results = []
    for feature in features:
        stat = compute_paired_statistics(df, feature)
        stats_results.append(stat)

    stats_df = pd.DataFrame(stats_results)

    # Apply Bonferroni correction
    n_tests = len(features)
    stats_df["t_pvalue_bonf"] = np.minimum(stats_df["t_pvalue"] * n_tests, 1.0)
    stats_df["significant_bonf"] = stats_df["t_pvalue_bonf"] < 0.05

    return df, stats_df


def generate_plots(df: pd.DataFrame, stats_df: pd.DataFrame, output_dir: str = "results/plots"):
    """
    Generate visualization plots for the analysis.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # 1. Response length comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Box plot of word counts
    data_for_box = pd.DataFrame({
        'Word Count': pd.concat([df['human_word_count'], df['llm_word_count']]),
        'Prompt Style': ['Human Style'] * len(df) + ['LLM Style'] * len(df)
    })
    sns.boxplot(x='Prompt Style', y='Word Count', data=data_for_box, ax=axes[0])
    axes[0].set_title('Response Length by Prompt Style')
    axes[0].set_ylabel('Word Count')

    # Paired plot
    for idx in range(min(len(df), 50)):
        axes[1].plot([0, 1], [df.iloc[idx]['human_word_count'], df.iloc[idx]['llm_word_count']],
                    'o-', alpha=0.3, color='gray')
    axes[1].set_xticks([0, 1])
    axes[1].set_xticklabels(['Human Style\nPrompt', 'LLM Style\nPrompt'])
    axes[1].set_ylabel('Response Word Count')
    axes[1].set_title('Paired Response Lengths\n(each line = one question)')

    plt.tight_layout()
    plt.savefig(f"{output_dir}/response_length_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()

    # 2. Effect sizes plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Sort by absolute effect size
    stats_sorted = stats_df.sort_values('cohens_d', key=abs, ascending=True)

    colors = ['green' if d > 0 else 'red' for d in stats_sorted['cohens_d']]
    bars = ax.barh(stats_sorted['feature'], stats_sorted['cohens_d'], color=colors, alpha=0.7)

    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
    ax.axvline(x=0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    ax.axvline(x=-0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    ax.axvline(x=0.5, color='gray', linestyle=':', linewidth=0.5, alpha=0.5)
    ax.axvline(x=-0.5, color='gray', linestyle=':', linewidth=0.5, alpha=0.5)

    ax.set_xlabel("Cohen's d (Effect Size)")
    ax.set_title("Effect of Prompt Style on Response Features\n(Positive = LLM-style prompts produce higher values)")

    # Add significance markers
    for i, (idx, row) in enumerate(stats_sorted.iterrows()):
        sig = "***" if row['t_pvalue_bonf'] < 0.001 else ("**" if row['t_pvalue_bonf'] < 0.01 else ("*" if row['t_pvalue_bonf'] < 0.05 else ""))
        ax.text(row['cohens_d'] + 0.02 * np.sign(row['cohens_d']), i, sig, va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/effect_sizes.png", dpi=150, bbox_inches='tight')
    plt.close()

    # 3. Formality analysis
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Formal word ratio
    data_formal = pd.DataFrame({
        'Formal Word Ratio': pd.concat([df['human_formal_word_ratio'], df['llm_formal_word_ratio']]),
        'Prompt Style': ['Human Style'] * len(df) + ['LLM Style'] * len(df)
    })
    sns.boxplot(x='Prompt Style', y='Formal Word Ratio', data=data_formal, ax=axes[0])
    axes[0].set_title('Formality of Responses by Prompt Style')

    # Logical connectors
    data_connectors = pd.DataFrame({
        'Logical Connectors': pd.concat([df['human_logical_connectors'], df['llm_logical_connectors']]),
        'Prompt Style': ['Human Style'] * len(df) + ['LLM Style'] * len(df)
    })
    sns.boxplot(x='Prompt Style', y='Logical Connectors', data=data_connectors, ax=axes[1])
    axes[1].set_title('Logical Connectors in Responses by Prompt Style')

    plt.tight_layout()
    plt.savefig(f"{output_dir}/formality_analysis.png", dpi=150, bbox_inches='tight')
    plt.close()

    # 4. Model comparison (if multiple models)
    if df['model'].nunique() > 1:
        fig, ax = plt.subplots(figsize=(12, 6))

        model_effects = []
        for model in df['model'].unique():
            model_df = df[df['model'] == model]
            diff = model_df['llm_word_count'] - model_df['human_word_count']
            model_effects.append({
                'model': model.split('/')[-1],
                'mean_diff': diff.mean(),
                'std_diff': diff.std(),
                'n': len(diff)
            })

        model_effects_df = pd.DataFrame(model_effects)
        bars = ax.bar(model_effects_df['model'], model_effects_df['mean_diff'],
                     yerr=model_effects_df['std_diff'] / np.sqrt(model_effects_df['n']),
                     capsize=5, alpha=0.7)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.set_ylabel('Word Count Difference (LLM-style - Human-style prompt)')
        ax.set_title('Response Length Difference by Model')

        plt.tight_layout()
        plt.savefig(f"{output_dir}/model_comparison.png", dpi=150, bbox_inches='tight')
        plt.close()

    # 5. Topic-level analysis
    fig, ax = plt.subplots(figsize=(12, 6))

    topic_effects = []
    for topic in df['topic'].unique():
        topic_df = df[df['topic'] == topic]
        diff = topic_df['llm_word_count'] - topic_df['human_word_count']
        topic_effects.append({
            'topic': topic,
            'mean_diff': diff.mean(),
            'std_diff': diff.std(),
            'n': len(diff)
        })

    topic_effects_df = pd.DataFrame(topic_effects).sort_values('mean_diff')
    ax.barh(topic_effects_df['topic'], topic_effects_df['mean_diff'], alpha=0.7)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
    ax.set_xlabel('Word Count Difference (LLM-style - Human-style prompt)')
    ax.set_title('Response Length Difference by Topic')

    plt.tight_layout()
    plt.savefig(f"{output_dir}/topic_analysis.png", dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Plots saved to {output_dir}/")


def print_summary_report(df: pd.DataFrame, stats_df: pd.DataFrame):
    """Print a summary of the analysis results."""
    print("\n" + "="*70)
    print("ANALYSIS SUMMARY: LLM Behavior with Human vs LLM Style Prompts")
    print("="*70)

    print(f"\nTotal response pairs analyzed: {len(df)}")
    print(f"Models tested: {df['model'].unique().tolist()}")
    print(f"Topics covered: {df['topic'].nunique()}")

    print("\n" + "-"*70)
    print("KEY FINDINGS:")
    print("-"*70)

    # Significant results
    sig_features = stats_df[stats_df['significant_bonf'] == True]
    if len(sig_features) > 0:
        print(f"\nStatistically significant differences (Bonferroni-corrected p < 0.05):")
        for _, row in sig_features.iterrows():
            direction = "higher" if row['diff_mean'] > 0 else "lower"
            print(f"  - {row['feature']}: LLM-style prompts produce {direction} values")
            print(f"    (d = {row['cohens_d']:.3f}, p = {row['t_pvalue_bonf']:.4f})")
    else:
        print("\nNo statistically significant differences found after Bonferroni correction.")

    print("\n" + "-"*70)
    print("DETAILED STATISTICS:")
    print("-"*70)

    # Format stats table
    display_cols = ['feature', 'human_mean', 'llm_mean', 'diff_mean', 'cohens_d', 't_pvalue', 't_pvalue_bonf']
    print(stats_df[display_cols].to_string(index=False, float_format='%.3f'))

    # Effect size interpretation
    print("\n" + "-"*70)
    print("EFFECT SIZE INTERPRETATION:")
    print("-"*70)
    print("Cohen's d: |0.2| = small, |0.5| = medium, |0.8| = large")

    largest_effect = stats_df.loc[stats_df['cohens_d'].abs().idxmax()]
    print(f"\nLargest effect: {largest_effect['feature']} (d = {largest_effect['cohens_d']:.3f})")


def main():
    """Main analysis function."""
    # Load results
    results = load_results()
    print(f"Loaded experiment results from {results['experiment_config']['timestamp']}")

    # Run analysis
    df, stats_df = run_analysis(results)

    # Generate plots
    generate_plots(df, stats_df)

    # Print summary
    print_summary_report(df, stats_df)

    # Save analysis results
    stats_df.to_csv("results/statistical_analysis.csv", index=False)
    df.to_csv("results/features_extracted.csv", index=False)
    print("\nAnalysis files saved to results/")

    return df, stats_df


if __name__ == "__main__":
    df, stats_df = main()
