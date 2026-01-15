# Production-Grade Text-to-SQL Agent with Deterministic Execution and Intelligent Recovery 

This repository implements a **production-grade Text-to-SQL agent** that combines **deterministic execution guarantees** with **controlled LLM-based reasoning** for ambiguity handling, query repair, and result interpretation.

The system is designed for **real-world deployment**, prioritizing correctness, safety, observability, and extensibility over benchmark-only accuracy.

## Problem Statement

Most Text-to-SQL systems optimize for:
- Benchmark accuracy
- Single-shot SQL generation
- End-to-end LLM reasoning

These approaches often fail in production due to:
- Unbounded retries
- Hallucinated SQL
- Poor debuggability
- Unsafe execution paths

This project addresses a different question:

> **How do we build a Text-to-SQL system that behaves predictably under failure, ambiguity, and partial correctness—without sacrificing usability?**

## Design Philosophy

### Determinism First
- SQL generation, validation, and execution follow strict, auditable rules.
- All retries are bounded.
- All termination paths are explicit.

### LLMs at the Edges
- LLMs are used **only where reasoning is required**, never where correctness is mandatory.
- Non-deterministic components cannot influence SQL execution.
- Deterministic and non-deterministic paths are cleanly separated.

### Fail-Safe by Default
- Ambiguous queries do not fail silently.
- Invalid SQL is repaired when possible or escalated safely.
- Every recovery action is observable.

## Core Capabilities

### Deterministic SQL Pipeline
- Schema introspection and grounding
- Schema-aware SQL generation
- Static SQL validation
- Safe execution with result limits
- Guaranteed non-destructive behavior

### Intelligent Query Recovery
- Automatic repair of invalid SQL (syntax, structure, schema issues)
- Repair attempts are bounded and transparent
- Repair metadata records what changed and why

### Human-in-the-Loop (HITL)
- Ambiguous or non-SQL queries trigger clarification instead of failure
- Structured clarification responses enable multi-turn interactions
- HITL context is preserved for downstream handling

### Post-Execution Reasoning
- Query results can be summarized in natural language
- Summaries are generated **after execution**
- Data correctness is never affected by explanation logic

### Observability & Debugging
- Full execution metadata: retries, repairs, tool usage
- Clear separation between deterministic and LLM-driven behavior
- Designed for auditability and production monitoring

## Architecture Overview

The system is implemented as a **graph-based execution engine** with explicit states and transitions:

- Routing (SQL vs Non-SQL)
- SQL generation
- Validation
- Optional repair
- Execution
- Final response or clarification

Each node has a single responsibility, and all transitions are governed by explicit policies.

![text_to_sql_agent_architecture](https://github.com/user-attachments/assets/dc9aa7c2-2a51-4e11-9a6c-97bac0a9e06e)

## Evaluation & Testing Philosophy

The system is validated using:
- Deterministic regression tests
- SQL invariant enforcement
- Failure injection (invalid SQL, ambiguity, schema mismatch)
- Behavioral guarantees (no infinite loops, no unsafe execution)

The goal is **predictable behavior**, not just correct answers.

## Key Insight

> **LLMs do not replace deterministic systems.  
> They enhance them—when strictly constrained.**

This repository demonstrates how to combine both safely.

## Research Paper

A full technical paper detailing the motivation, design decisions, and architectural trade-offs is available here:

📄 **Text-to-SQL Research Paper**  
https://github.com/ZubinMehta27/text-to-sql/blob/main/publications/T2S%20Research%20Paper.pdf
