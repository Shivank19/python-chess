# Spell Chess — Unit Test Suite

**Group 5** — Prashant Rao, Shivank Sapra, Francis Aweenagua, Tarannum Perween

---

## Overview

This repository contains a requirements-based unit test suite for Spell Chess.

The tests in `test_spell_logic.py` verify the correctness of the game logic implemented in `spell_logic.py` against the rules defined in `SPELL_CHESS_RULES.md`.

---

## Files

| File                   | Description                                             |
| ---------------------- | ------------------------------------------------------- |
| `test_spell_logic.py`  | Unit test suite (this is the main deliverable)          |
| `spell_logic.py`       | Game logic implementation under test                    |
| `SPELL_CHESS_RULES.md` | Full game specification (source of truth for all tests) |

---

## Dependencies

Python 3.8 or later is required. Install the two required packages using `pip`:

```bash
pip install chess pytest
```

---

## How to Run the Tests

### Run all tests (recommended)

```bash
pytest test_spell_logic.py -v
```

### Run a specific test class

```bash
pytest test_spell_logic.py::TestFreezeCharges -v
```

### Run tests and show only failures

```bash
pytest test_spell_logic.py -v --tb=short
```
