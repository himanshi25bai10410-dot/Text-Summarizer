#!/usr/bin/env python3
"""
summarizer.py — A lightweight CLI text summarizer using sumy + nltk.

Usage:
  python summarizer.py --text "Your text here..."
  echo "Your text..." | python summarizer.py
  python summarizer.py --text "..." --sentences 5 --algo lexrank
"""

import argparse
import sys

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"

ALGORITHMS = {
    "lsa": LsaSummarizer,
    "lexrank": LexRankSummarizer,
    "luhn": LuhnSummarizer,
}


def summarize(text: str, num_sentences: int = 3, algo: str = "lsa") -> str:
    """
    Summarize the given text.

    Args:
        text:          Input text to summarize.
        num_sentences: Number of sentences in the summary.
        algo:          Summarization algorithm ('lsa', 'lexrank', 'luhn').

    Returns:
        Summary as a single string.
    """
    if algo not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm '{algo}'. Choose from: {', '.join(ALGORITHMS)}")

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer_class = ALGORITHMS[algo]
    summarizer = summarizer_class(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sentences = summarizer(parser.document, num_sentences)
    return " ".join(str(s) for s in sentences)


def main():
    parser = argparse.ArgumentParser(
        description="Lightweight CLI text summarizer (extractive, offline)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python summarizer.py --text "Your long text here..."
  echo "Your long text..." | python summarizer.py
  python summarizer.py --text "..." --sentences 5 --algo lexrank
  python summarizer.py --text "..." --algo luhn --verbose
        """,
    )
    parser.add_argument(
        "--text", "-t",
        type=str,
        default=None,
        help="Text to summarize. If omitted, reads from stdin.",
    )
    parser.add_argument(
        "--sentences", "-s",
        type=int,
        default=3,
        help="Number of sentences in the summary (default: 3).",
    )
    parser.add_argument(
        "--algo", "-a",
        type=str,
        default="lsa",
        choices=ALGORITHMS.keys(),
        help="Summarization algorithm: lsa (default), lexrank, luhn.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show input word count and algorithm used.",
    )

    args = parser.parse_args()

    # Read text from --text flag or stdin
    if args.text:
        text = args.text.strip()
    elif not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        parser.print_help()
        sys.exit(1)

    if not text:
        print("Error: No input text provided.", file=sys.stderr)
        sys.exit(1)

    word_count = len(text.split())
    sentence_count_approx = text.count(".") + text.count("!") + text.count("?")

    if sentence_count_approx < args.sentences:
        print(
            f"Warning: Text appears to have ~{sentence_count_approx} sentence(s), "
            f"but you requested {args.sentences}. Adjusting to fit.",
            file=sys.stderr,
        )

    if args.verbose:
        print(f"── Input  : ~{word_count} words | Algorithm: {args.algo.upper()} | Summary sentences: {args.sentences}")
        print("── Summary ──────────────────────────────────────")

    try:
        summary = summarize(text, num_sentences=args.sentences, algo=args.algo)
        print(summary)
    except Exception as e:
        print(f"Error during summarization: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()