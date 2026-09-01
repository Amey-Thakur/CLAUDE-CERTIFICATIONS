# Things that get mixed up

Every one of these four exams tests a distinction rather than a fact. You are
rarely asked what something is. You are asked which of two similar things fits
the situation in front of you.

This page holds the pairs worth being certain about, with the question that
separates each one.

---

## Agent or workflow

| | Workflow | Agent |
| --- | --- | --- |
| Who decides the path | You did, in advance | The model, at run time |
| Testable | Yes, it is deterministic | Only in aggregate |
| Cost | Predictable | Depends on the run |
| Fails by | Doing the wrong thing you specified | Not stopping |

**The question:** can you write down the steps?

If you can, write them down. Most problems people reach for an agent to solve
are workflows that were never finished being specified.

---

## Tool, Skill, or MCP server

| | Use it when |
| --- | --- |
| **Built-in tool** | Anthropic already ships the capability |
| **Custom tool** | Only your system can do it, and only your application needs it |
| **Skill** | A reusable procedure, no new data access |
| **MCP server** | The same integration is needed by more than one client |

**The question:** how many applications need this?

One application means a custom tool. More than one means a server, because that
is the entire reason the protocol exists.

---

## Streaming or batching

Neither is about cost, although cost is the usual reason people choose.

**The question:** is anyone waiting?

Somebody waiting means the Messages API, and streaming if the wait is long
enough to feel. Nobody waiting means the Message Batches API, at 50% cost,
returned within a 24-hour window. Multi-turn tool calling rules batching out
regardless.

---

## Context editing or compaction

Both manage a conversation that has grown too long, and they do opposite things.

**Context editing clears.** Old tool results or thinking blocks are removed
before the model sees them. What was there is gone.

**Compaction summarizes.** Earlier context is replaced by a summary of itself,
so the substance survives in less space.

**The question:** is the old content still needed, or only the fact of it?

Tool results you have already acted on can be cleared. A conversation whose
earlier decisions still matter should be compacted.

---

## Prompt caching or context editing

Both reduce what you pay for a long conversation, at different ends.

Caching makes the **repeated prefix** cheap to resend. Context editing makes the
conversation **shorter**. Caching is free to try; editing changes what the model
can see.

Reach for caching first. It costs nothing to be wrong about.

---

## end_turn, tool_use, or max_tokens

`stop_reason` is the field, and treating all three as "I have a response now" is
the most common API mistake there is.

| Value | Meaning | What your code should do |
| --- | --- | --- |
| `end_turn` | Claude finished | Return the content |
| `tool_use` | Claude wants a tool run | Execute it, append the result as a **user** turn, call again |
| `max_tokens` | Output was truncated | Raise the limit or split the task. Do not use the fragment |
| `pause_turn` | A long-running server tool paused | Send the response back to continue |
| `refusal` | A safety classifier declined | Check `stop_details`; do not read `content` as an answer |

The dangerous one is `max_tokens`. Nothing throws, the string looks like an
answer, and if you were parsing JSON the error you log will be a JSON error.

---

## Certification or course certificate

The distinction this repository is most careful about, because getting it wrong
in public is expensive.

| | Course certificate | Certification |
| --- | --- | --- |
| How you get it | Complete a free course on Claude Academy | Pass a proctored exam |
| Where | Online, at your own pace | Pearson VUE, online or a test center |
| Costs | Nothing | 99 to 175 USD |
| Proves | You watched the material | You passed an assessment against a published blueprint |
| Expires | No | 12 months, with a free renewal |

Never describe a course certificate as a certification, and never write "Claude
Certified" unless you hold the credential.

---

## Scaled score or percentage

720 is a scaled score on a range of 100 to 1,000. It is not 72%.

A scaled score places your result on a standard range so that different versions
of the paper, which may differ slightly in difficulty, can be compared. There is
no published mapping from questions answered to scaled score, so any "you can
afford to miss N" figure you have been told was invented.

**The question:** am I treating this as a fraction of questions?

If so, stop. Use the per-domain breakdown on the score report instead, which is
the half that tells you what to do next.

---

## Retake wait or appeal window

Two different clocks, and people confuse them at the worst moment.

**Retake waits** grow per attempt: 14 days, then 30, then 90. Full fee each
time, and both the wait and the attempt count reset on a new exam version.

**The appeal window** is 14 calendar days from an invalidated result. The
content of individual items is never appealable; the process around them is.

They share a number, which is exactly why they get muddled.

---

## Where to go next

- The blueprint for your exam, in its [study guide](../README.md#the-certifications)
- [Study strategy](study-strategy.md), for the order to work in
- [Policies](policies.md), for the rules in full
- [Glossary](glossary.md), for terms rather than distinctions

---

Facts last verified against the official sources on 2026-09-01. [Repository index](../README.md)
