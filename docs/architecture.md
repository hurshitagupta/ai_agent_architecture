# AI Agent Architecture

## Architecture Overview

The system is divided into focused components so that reasoning, execution,
memory, communication, and external actions remain separated.

```text
                    ┌──────────────────┐
                    │   User Request   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Brain       │
                    │ Understands task │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Planner      │
                    │ Creates steps    │
                    └────────┬─────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Control Loop     │
                  │ Limits / retries    │
                  └─────────┬───────────┘
                            │
                            ▼
                    ┌──────────────────┐
                    │     Executor     │
                    │ Executes steps   │
                    └───────┬──────────┘
                            │
                            ▼
                    ┌──────────────────┐
                    │      Tools       │
                    │ Controlled APIs  │
                    └──────────────────┘

          ┌─────────────────────────────────────┐
          │              State                  │
          │ Tracks plan, progress and results   │
          └─────────────────────────────────────┘

          ┌─────────────────────────────────────┐
          │              Memory                 │
          │ Stores validated reusable context   │
          └─────────────────────────────────────┘

                            │
                            ▼
                    ┌──────────────────┐
                    │ Communication    │
                    │ Structured output│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Final Response   │
                    └──────────────────┘


Persistence stores selected traces and reports.

Deployment provides runtime configuration and environment-based secrets.