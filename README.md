# Text-to-SQL: Deterministic vs Tool-Based Architectures (WIP)

This repository investigates a core systems question:

**Can a tool-based reasoning system outperform a deterministic Text-to-SQL engine in production?**

## Motivation

Most Text-to-SQL research optimizes for benchmark accuracy.
This project optimizes for:
- Safety
- Determinism
- Debuggability
- Production reliability

## Architectures Implemented

### 1. Deterministic Pipeline
- Schema grounding
- Rule-based SQL generation
- Static validation
- Direct execution

### 2. Tool-Based Reasoning System
- LLM-mediated reasoning
- Strict tool boundaries
- Bounded retries
- Deterministic execution guarantees

## Testing Philosophy

The system is evaluated using:
- Deterministic regression tests
- Semantic equivalence checks
- SQL invariant enforcement
- Failure injection

## Key Insight

LLMs do not replace deterministic systems.
They augment them — when strictly constrained.

## Paper

A full technical paper can be accessed [here](https://github.com/ZubinMehta27/text-to-sql/blob/main/T2S%20Research%20Paper.pdf).

