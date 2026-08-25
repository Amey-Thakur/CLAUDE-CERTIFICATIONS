# Official study resources

Everything here is published by Anthropic or its official partners. Third-party courseware is deliberately excluded; the [exam guides](official-sources.md) define what is on each exam, and these resources teach it.

## Courses

All 22 official courses, with descriptions, enrollment links, and exam relevance, are cataloged in [Anthropic courses](courses.md). The platforms that host them:

| Resource | What it is |
| --- | --- |
| [Anthropic Academy](https://anthropic.skilljar.com/) | The public academy: every course free, no partner account needed |
| [Anthropic Partner Academy](https://anthropic-partners.skilljar.com/) | The certification program's home: prep paths, registration, and partner-exclusive content. Requires a partner sign-in |
| [Anthropic on Coursera](https://www.coursera.org/partners/anthropic) | Core courses (Building with the Claude API, Claude Code in Action, MCP) delivered through Coursera |
| [Build with Claude](https://www.anthropic.com/learn/build-with-claude) | Anthropic's index of learning paths for API development |

## Documentation

The exams are written against the platform as documented. These are the canonical references:

| Resource | Covers | Most relevant to |
| --- | --- | --- |
| [Claude platform documentation](https://platform.claude.com/docs) | The API: messages, tools, streaming, vision, batches, caching, [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Developer, both Architect exams |
| [Claude Code documentation](https://code.claude.com/docs) | CLAUDE.md, skills, subagents, hooks, headless mode, and [best practices](https://code.claude.com/docs/en/best-practices) | Developer, Architect Foundations |
| [Model Context Protocol](https://modelcontextprotocol.io/) | The MCP specification, concepts, and SDK guides | Developer, both Architect exams |
| [Claude help center](https://support.claude.com/) | Projects, Artifacts, connectors, and product features | Associate |

## Engineering articles

Anthropic's engineering blog covers the exact judgment the scenario questions test. Worth reading in this order:

1. [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): the workflow-versus-agent decision framework that underpins the agent domains
2. [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): context windows, drift, and compaction
3. [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents): tool descriptions and interface design, the substance of the MCP domains
4. [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills): what Skills are for and when to use them over tools
5. [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp): efficiency patterns for production MCP use
6. [Building agents that reach production systems with MCP](https://claude.com/blog/building-agents-that-reach-production-systems-with-mcp): integration patterns at production scale

## Videos

Anthropic publishes a great deal on its [YouTube channel](https://www.youtube.com/@anthropic-ai), including the complete **AI Fluency** course. The [official videos](videos.md) page collects the ones that map to exam domains, arranged by exam and playable inline.

The [Academy courses](courses.md) are themselves video curricula; for structured watching, they are the primary official video resource.

## Code

| Resource | What it is |
| --- | --- |
| [anthropics/courses](https://github.com/anthropics/courses) | Anthropic's own course notebooks: API fundamentals, prompt engineering, evaluations, tool use |
| [anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook) | Runnable recipes for the patterns the exams describe: RAG, tool use, agents, vision |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | Claude Code itself: issues and releases are a current picture of the tool |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | Reference MCP servers to read before writing your own |

## Matching resources to your exam

- **Associate – Foundations:** the help center, Prompting 101, and the AI Fluency courses on the public academy.
- **Developer – Foundations:** platform documentation, the cookbook, the MCP specification, and the API and MCP courses.
- **Architect – Foundations:** Claude Code documentation and best practices, Building effective agents, Writing effective tools, and the reference MCP servers.
- **Architect – Professional:** the engineering articles end to end, plus evaluation and RAG material from the cookbook.

---

Facts last verified against the official sources on 2026-08-25. [Repository index](../README.md)
