# How LLMs work

A compact reference for the chapter. Each lesson has the explanation; this page has the terms, the pipeline and the checks.

## Lessons

1. [From ML to transformers](01-from-ml-to-transformers.md)
2. [Tokens, embeddings and context windows](02-tokens-embeddings-and-context-windows.md)
3. [Training, fine-tuning and RLHF](03-training-fine-tuning-and-rlhf.md)
4. [Sampling and hallucinations](04-sampling-and-hallucinations.md)
5. [Choosing a model](05-choosing-a-model.md)

## The pipeline

```text
text -> tokens -> embeddings -> transformer layers -> next-token probabilities -> pick one -> repeat
```

Training pipeline: pretraining -> fine-tuning (instruction tuning) -> RLHF or RLAIF -> deployment.

## Key terms

| Term | Meaning |
|---|---|
| Token | Chunk of text from a fixed vocabulary, the unit of reading, writing, billing and limits |
| Embedding | Vector representing a token or text, similar meaning gives similar direction |
| Parameter | One learned number in the model, changed by training |
| Attention | Each token weighs the other tokens in the input to decide what matters |
| Inference | Using fixed parameters to answer a prompt, nothing is learned |
| Context window | Maximum tokens per request: input, history, tool results and output |
| Pretraining | Next-token prediction on a huge corpus |
| Instruction tuning | Fine-tuning on instruction and response pairs |
| RLHF, RLAIF | Training from human or AI preference judgements via a reward model |
| Knowledge cutoff | Date after which the training data has little or nothing |
| Logits, softmax | Raw scores per token, and the function that turns them into probabilities |
| Temperature, top-p | Settings that sharpen or flatten the distribution, and cut its tail |
| Hallucination | Fluent, confident output that is false or unsupported |

## Formulas

| Name | Formula |
|---|---|
| Cosine similarity | $\frac{a \cdot b}{\lvert a \rvert \, \lvert b \rvert}$ |
| Softmax with temperature | $p_i = e^{z_i / T} / \sum_j e^{z_j / T}$ |
| Preference probability | $P(A \succ B) = 1 / (1 + e^{-(r_A - r_B)})$ |
| Cost per call | input tokens $\times$ input price + output tokens $\times$ output price |

## Rules of thumb

- English prose is roughly 4 characters per token; code, JSON, digits and other languages cost more. Measure with the provider's counter.
- The whole history is re-sent every turn, so long chats cost more per turn.
- Weights are fixed at inference. Memory, search and documents must arrive in the prompt.
- Low temperature gives repeatable output, not correct output.
- Cheapest tier that passes your own tests wins. Benchmarks only shortlist.

## Reducing hallucinations

1. Ground the answer in text you supply.
2. Require quotes, then check them.
3. Use tools for facts and arithmetic.
4. Allow "not stated".
5. Verify: run, open, search, recompute.

## Claude models (as of 2026)

| Model ID | Role |
|---|---|
| `claude-fable-5-1` | Demanding reasoning, long-horizon agentic work |
| `claude-opus-5-5` | Long-running agentic coding and knowledge work |
| `claude-sonnet-5-5` | Speed and intelligence balance |
| `claude-haiku-5-5` | High-volume, latency-sensitive tasks |

Source: [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview).
