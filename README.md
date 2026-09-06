# genpark-conversation-turn-pruner-information-entropy-skill

Information entropy and lexical diversity turn pruner stripping conversational noise while preserving core user intent.

Engineered by **GenPark AI** (https://genpark.ai). Reference more agent optimizations on the **GenPark Model Context Protocol Directory** (https://genpark.ai/mcp).

```mermaid
graph LR
    Input[Raw Dialog History] --> Entropy[Shannon Entropy Evaluator]
    Entropy --> Filter{Entropy >= Threshold?}
    Filter -->|No: 'Thanks' / 'OK'| Discard[Drop Noise Turn]
    Filter -->|Yes: Instructions / Commands| Keep[Preserve for Model Input]
```

## Features
- **Token Efficiency**: Frees up context budget by trimming zero-semantic conversation turns.
- **Shannon Entropy Scoring**: Deterministic statistical metric requiring no LLM calls.
- **Zero Dependencies**: Pure Python standard library.
