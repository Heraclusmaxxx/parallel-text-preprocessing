import os
import pandas as pd
import re
from concurrent.futures import ProcessPoolExecutor
import time

# CONFIGURATION
INPUT_FILE_NAME = "IMDB Dataset.csv"
OUTPUT_FILE_NAME_PARALLEL = "IMDB Dataset Cleaned by par.csv"
OUTPUT_FILE_NAME_SEQUENTIAL = "IMDB Dataset Cleaned by seq.csv"
TARGET_COLUMN = "review"


def clean_func(text, stop_words):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"<[^>]+>", "", text, count=0)
    text = re.sub(r"[^a-z\s]", "", text)
    final_text = " ".join([word for word in text.split() if word not in stop_words])
    return final_text


def proc_func(chunk):
    stop_words = set(
        [
            "a",
            "an",
            "the",
            "in",
            "on",
            "at",
            "to",
            "with",
            "by",
            "and",
            "but",
            "or",
            "because",
            "so",
            "is",
            "am",
            "are",
            "was",
            "were",
            "do",
            "does",
            "did",
            "can",
            "will",
            "i",
            "he",
            "she",
            "it",
            "they",
            "my",
            "your",
        ]
    )
    chunk[TARGET_COLUMN] = chunk[TARGET_COLUMN].apply(clean_func, stop_words)
    return chunk


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, INPUT_FILE_NAME)
    raw_dset = pd.read_csv(file_path)
    n_cpu = os.cpu_count()
    total_rows = len(raw_dset)
    chunk_size = (total_rows + n_cpu - 1) // n_cpu
    chunks = [
        raw_dset[i : i + chunk_size].copy() for i in range(0, total_rows, chunk_size)
    ]
    time_start = time.time()
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = [executor.submit(proc_func, chunk) for chunk in chunks]
        processed_chunks = [fut.result() for fut in results]
    result_dset = pd.concat(processed_chunks)
    print(f"parallel processing time: {time.time() - time_start:.2f}sec")
    output_path = os.path.join(script_dir, OUTPUT_FILE_NAME_PARALLEL)
    result_dset.to_csv(output_path, index=False)
    # one process execution
    time_start1 = time.time()
    result = proc_func(raw_dset.copy())
    print(f"time for sequential execution: {time.time() - time_start1:.2f}sec")
    output_path = os.path.join(script_dir, OUTPUT_FILE_NAME_SEQUENTIAL)
    result.to_csv(output_path, index=False)
