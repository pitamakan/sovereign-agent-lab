"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No venues found — search_venues returned 0 matches for 300 guests with vegan options."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
After setting The Albanach's status to 'full' in mcp_venue_server.py, it
disappeared from search results — Query 1 returned only The Haymarket Vaults
instead of two venues. No agent code was touched. This demonstrates the core
MCP value: data lives in one place, and all consumers see the update
automatically without any changes to their own code.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 307   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 1   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP means the agent discovers tools at runtime rather than having them hardcoded
at import time. Any client — LangGraph, Rasa, a future agent — connects to the
same server and gets the same tools automatically. When the tool list or data
changes, only the server is updated; no client code changes.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- Planner: a strong-reasoning model that takes raw message and
  breaks it into an ordered list of subgoals (find venue, check weather, book,
  confirm). Lives upstream of the ReAct loop in the autonomous-loop half.

- Executor (research_agent.py grown): the ReAct loop that works through the
  planner's subgoals by calling tools. When it needs a human conversation it
  calls handoff_to_structured instead of improvising. Lives in the autonomous
  loop half.

- Shared MCP Tool Server (mcp_venue_server.py grown): the single source of
  truth for all capabilities — venue search, web search, calendar, email. Both
  halves discover tools from here; neither hardcodes them. Lives in the shared
  layer between the two halves.

- Structured Agent / Handoff target (exercise3_rasa grown): the Rasa CALM
  agent that handles the pub-manager call with deterministic business rules.
  Receives control from the executor via the handoff bridge when a real human
  conversation is required. Lives in the structured-agent half.

- Memory store (filesystem + vector): the autonomous loop writes research
  results to a persistent store so the structured agent can look up what was
  agreed without re-running the research. Sits in the shared layer.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph handles the research: in Exercise 2 it autonomously called four tools
in the right order, pivoted when The Bow Bar was full, and admitted failure
honestly when no venue could fit 300 guests — all without being told the
steps in advance. That open-ended reasoning is impossible to script.

Rasa CALM handles the confirmation call: in Exercise 3 it enforced the
£300 deposit limit exactly, refused the parking question without improvising,
and redirected the conversation back to the booking flow. Every decision was
auditable and guaranteed by Python, not by a prompt.

Swapping them feels wrong because the research problem has no fixed path —
a deterministic CALM flow would break the moment a venue is full. The
confirmation call has strict financial constraints — a LangGraph agent might
reason its way around a £300 limit if the manager argues persuasively enough.
Each architecture is brittle in exactly the place the other is strong.
"""