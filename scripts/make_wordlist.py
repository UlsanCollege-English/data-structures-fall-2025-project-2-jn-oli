"""
Generates the data/words.csv snapshot file.

This script is for setup only and is not part of the
runtime application. It requires the 'wordfreq' library.

Install with:
pip install wordfreq
"""

import wordfreq
from pathlib import Path
import csv
import sys

# Define the target path
# This script should be run from the project root directory
OUT_PATH = Path(__file__).resolve().parents[1] / 'data' / 'words.csv'
COUNT = 50_000

def generate_wordlist():
    """Fetches top words and saves them to CSV."""
    print(f"Generating word list with {COUNT} words...")
    
    # Get top 50k words from 'en' (English) wordlist
    # 'wordlist=best' gives a good quality, clean list
    top_words = wordfreq.top_n_list('en', COUNT, wordlist='best')

    # Ensure the 'data' directory exists
    OUT_PATH.parent.mkdir(exist_ok=True)

    try:
        with open(OUT_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for word in top_words:
                # Get a frequency score (a float between 0 and 1)
                freq = wordfreq.zipf_frequency(word, 'en')
                writer.writerow([word, freq])
        
        print(f"\nSuccessfully created {OUT_PATH}")
        print(f"Total words written: {len(top_words)}")

    except IOError as e:
        print(f"\nERROR: Could not write to file {OUT_PATH}. {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        import wordfreq
    except ImportError:
        print("Error: 'wordfreq' library not found.")
        print("Please install it by running: pip install wordfreq")
        sys.exit(1)
        
    generate_wordlist()
