# Parallel Text Preprocessing with Multiprocessing

A Python script designed to practice and master the `multiprocessing` module (via `concurrent.futures`) in the context of Machine Learning / NLP pipelines. It parallelizes the preprocessing of the **IMDB 50K Movie Review Dataset**.

## 🚀 Overview

The pipeline splits a large Pandas DataFrame into equal, isolated chunks based on the CPU core count, distributes them across multiple processes, applies heavy text cleaning, and concatenates the results back into a single clean dataset.

### Preprocessing Steps Applied:
* **Lowercasing**: Standardizing text format.
* **HTML Stripping**: Removing raw `<br />` tags using Regex.
* **Noise Reduction**: Stripping numbers, punctuation, and special characters.
* **Stop-words Filtering**: Dropping uninformative words (`the`, `is`, `at`, etc.) to reduce feature space.

## 📊 Benchmarks & Insights

* **Dataset Size**: 50,000 rows (IMDB Dataset)
* **CPU Cores**: 4 Cores
* **Parallel Processing Time**: ~4.05 sec
* **Sequential Execution Time**: ~3.58 sec

### Key Takeaway
For 50K rows on 4 cores, single-threaded execution slightly outperforms multiprocessing due to IPC (Inter-Process Communication) and `pickle` serialization overhead. Multiprocessing will scale dynamically and show massive speedups when handling millions of rows (e.g., 500K+ rows) or when switching to computationally heavy steps like **Lemmatization** or **Named Entity Recognition (NER)**.

## 🛠️ Requirements & Usage

1. Place your `IMDB Dataset.csv` in the same directory as the script.
2. Run the script:
   ```bash
   python conc.py
   ```
3. The cleaned dataset will be exported to the same directory as `IMDB Dataset Cleaned.csv`.