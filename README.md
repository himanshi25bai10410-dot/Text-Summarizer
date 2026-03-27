# 📝 Text Summarizer CLI

A simple, lightweight, **offline** text summarizer built with Python and `sumy`.
No API keys. No internet required. Just fast, extractive summarization.

---

## ⚙️ Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Download NLTK tokenizer data** (one-time, ~1 MB)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

---

## 🚀 Usage

### Basic — paste text directly
```bash
python summarizer.py --text "Your long article or paragraph here..."
```

### Pipe text from stdin
```bash
echo "Your long text here..." | python summarizer.py
cat myfile.txt | python summarizer.py
```

### Control summary length
```bash
python summarizer.py --text "..." --sentences 5
```

### Choose summarization algorithm
```bash
python summarizer.py --text "..." --algo lexrank
python summarizer.py --text "..." --algo luhn
python summarizer.py --text "..." --algo lsa      # default
```

### Verbose mode (shows word count + algorithm)
```bash
python summarizer.py --text "..." --verbose
```

---

## 🔬 Algorithms

| Algorithm | Best for |
|-----------|----------|
| `lsa` (default) | General purpose, balanced |
| `lexrank` | News articles, longer documents |
| `luhn` | Short-to-medium texts |

---

## 📋 All Options

```
--text,      -t   Text to summarize (or pipe via stdin)
--sentences, -s   Number of output sentences (default: 3)
--algo,      -a   Algorithm: lsa, lexrank, luhn (default: lsa)
--verbose,   -v   Show stats and algorithm info
```

---

## 💡 Tips

- Works best on **100+ word** inputs.
- For very short texts, use `--sentences 1` or `2`.
- Pipe from a `.txt` file: `cat article.txt | python summarizer.py -s 4 -a lexrank`

# Author
Himanshi Saxena
25BAI10410
