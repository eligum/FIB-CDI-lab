#!/usr/bin/env python

import argparse
import pathlib
from unidecode import unidecode


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", action="store", help="path of file to process")

    args = parser.parse_args()

    path = pathlib.Path(args.file)
    new_path = path.parent / (path.stem + "_clean" + path.suffix)

    with open(path, mode="r", encoding="utf-8") as f_in:
        text = f_in.read()              # Read entire file into a string
        text = text.replace("\n", " ")  # Replace newlines for spaces
        text = " ".join(text.split())   # Normalize whitespace
        text = unidecode(text)          # Map letters to ascii characters
        text = text.lower()             # Make all text lowercase
        with open(new_path, mode="w") as f_out:
            # Filter out punctuation marks
            for c in text:
                if c == " " or c.isalpha():
                    f_out.write(c)
