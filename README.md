# Dependency Length Minimization (DLM)

This project is based on the paper:
"A Reappraisal of Dependency Length Minimization as a Linguistic Universal"

## Overview

The goal of this project was to understand how sentence structure in natural language is organized. Specifically, I explored whether real sentences are structured in a way that reduces complexity compared to random arrangements of words.

## What I Implemented

- Computed **Dependency Length (DL)** for sentences  
- Computed **Intervener Complexity (IC)**  
- Created a **random baseline** by shuffling word positions  
- Compared real sentences with randomized versions  
- Tested the results across multiple languages:
  - English  
  - Hindi  
  - German  
  - French  
- Ran the experiment multiple times and averaged the results  

## Method

For each sentence in the dataset:

1. Measured the dependency length (distance between words and their heads)
2. Measured intervener complexity (number of words between dependencies)
3. Generated a randomized version of the sentence
4. Recomputed the same metrics
5. Compared the real and randomized values

## Results

Across all languages, the results show a clear pattern:

- Real sentences consistently have **lower dependency length**
- Real sentences also have **lower intervener complexity**
- Randomized sentences show significantly higher values

This suggests that natural language is not random, but structured in a way that reduces complexity.

## Conclusion

The experiment supports the idea that languages tend to minimize structural complexity.  
While both dependency length and intervener complexity are reduced, intervener complexity may better capture how sentence structure is optimized.

## Files

- `main.py` → Implementation  
- `results.txt` → Output table  
- `graph.png` → Visualization of results  

## Note

The datasets used are from Universal Dependencies (UD) treebanks and are not included in this repository.
