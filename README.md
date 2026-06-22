🛰️ Orbit Autonomous Agent

An autonomous, multi-agent codebase optimization framework that interfaces with the GitLab Orbit Knowledge Graph to detect structural repository decay, validate code usage viability via static AST analysis, and automatically generate remediation merge requests.
📋 Hackathon Compliance & Disclosures

    Agent Type: Hybrid Multi-Agent System (Dual-layer deterministic Planner + asynchronous stateless Executor).

    UiPath Integration Layer: This system functions as an advanced external agent framework. It runs natively on your edge infrastructure or Cloud Run, with orchestration, conditional gating, and human-in-the-loop exception handling driven by UiPath Maestro (Track 1 / Track 2).

    AI-Assisted Development Bonus: Built and optimized utilizing AI coding agents (Gemini CLI / Claude Code). Session traces and verifiable prompt telemetry are documented in the project logs.

📐 Architecture Overview

The system is split into two core layers to guarantee deterministic execution pathways and clear fault isolation:

  [ CLI / Inbound Goal ]
            │
            ▼
   ┌─────────────────┐
   │  Planner Agent  │ ──► Breaks down Goal into atomic, prioritized Task graph
   └─────────────────┘
            │
            ▼
   ┌─────────────────┐
   │ Executor Agent  │ ──► Asynchronously dispatches tasks to specific engines
   └─────────────────┘
      │     │     │
      │     │     └─► [ Analysis Engine ] ──► Local AST & Semantic Trace
      │     └───────► [ Orbit API Client ] ──► Queries Orbit Graph Network
      └─────────────► [ Action Layer ]    ──► Generates Git Patches / MRs

    The Planner Agent (src/planner/): Consumes a high-level operational objective (Goal), selects the optimal strategy (e.g., DeadCodePlanner), and breaks it into an ordered list of atomic Task blocks sorted by strict priority matrix thresholds.

    The Executor Agent (src/executor/): Consumes the plan, evaluates task prefixes, maps them to targeted execution strategies (DeadCodeExecutor), and coordinates async network communication with the Orbit API and local static analysis loops.

🗂️ Directory Structure
Plaintext

orbit-autonomous-agent/
├── src/
│   ├── __init__.py
│   ├── planner/
│   │   ├── __init__.py
│   │   └── agent.py          # Planner agent (goal → prioritized tasks)
│   ├── executor/
│   │   ├── __init__.py
│   │   └── agent.py          # Executor agent (task evaluation & scheduling)
│   ├── orbit/
│   │   ├── __init__.py
│   │   └── client.py         # Async GitLab Orbit Knowledge Graph client
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── static.py         # AST-based static source validation
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py           # Command Line Interface (Click)
│   ├── config/
│   │   ├── __init__.py
│   │   └── loader.py         # Config ecosystem manager (Pydantic Settings)
│   └── utils/
│       ├── __init__.py
│       └── logging.py        # Loguru structured contextual logging
├── config/
│   └── orbit-agent.yaml      # Non-sensitive configuration layout
├── docker/
│   └── Dockerfile            # Containerized execution environment
├── scripts/
│   └── demo.sh               # Local evaluation pipeline runner
├── main.py                   # Production environment application hook
├── pyproject.toml            # Package metadata and build system setup
├── requirements.txt          # Absolute pinned dependencies
└── LICENSE                   # Apache 2.0 Open Source License

⚙️ Configuration Matrix

System constraints are controlled via config/orbit-agent.yaml and loaded dynamically via structural validation rules mapping back to Pydantic models.
YAML

orbit:
  api_url: "https://gitlab.com/api/v4/orbit"
  token: "YOUR_ORBIT_GRAPH_TOKEN"
gitlab:
  api_url: "https://gitlab.com/api/v4"
  token: "YOUR_GITLAB_PAT"
agent:
  max_concurrent_tasks: 5
  auto_create_mrs: true
  risk_threshold: "medium"

    ⚠️ Security Policy: Never commit secrets to source control. Sensitive values can be overridden at runtime using environment variables (e.g., ORBIT__TOKEN).

🚀 Installation & Setup
Prerequisites

    Python 3.11 or higher

    Git

Local Environment Deployment

    Clone the repository:
    Bash

    git clone https://github.com/your-user/orbit-autonomous-agent.git
    cd orbit-autonomous-agent

    Establish localized virtual containment sandbox:
    Bash

    python3 -m venv .venv
    source .venv/bin/activate

    Install dependencies and editable project package layout:
    Bash

    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -e .

💻 CLI Usage Guide

The system exposes a highly responsive command line interface built on Click with localized async event execution context mapping loops.
Run a Full Repository System Optimization Sweep

Scans target infrastructure dependencies, matches unreferenced file footprints, and evaluates AST structural viability.
Bash

orbit-agent audit --repo "gitlab-org/architecture-swarm" --auto-fix

Targeted Dead Code Isolation Sweep

Runs targeted analysis execution paths to isolate code paths requiring automatic patch compilation.
Bash

orbit-agent dead-code --repo "gitlab-org/legacy-utility-pipeline"

🦾 Multi-Agent Execution Lifecycle

    Goal Ingestion: The runtime receives target parameters from the interface layer.

    Deterministic Plan Generation: The DeadCodePlanner generates an array of critical tasks (e.g., Graph Queries → AST Validation → Patch Gen → MR Emit).

    State Management Validation: The Executor steps through the dependency tree, calling the async OrbitClient to interact with edge nodes.

    Context Cascading Fail-safe: If any middle validation layer marks code as actively referenced, downstream mutations (e.g., file removal MRs) are aborted.

📄 Open Source Licensing Compliance

This original solution code is distributed entirely under the Apache License 2.0.

    Licensing Exclusion Notice: The open-source license parameters defined herein apply solely to the participant's original solution codebase framework. It does not extend to, wrap, modify, or supersede any underlying proprietary UiPath platform packages, SDK extensions, or software components utilized during workflow orchestration layer tasks. All proprietary references remain strictly bound to their respective enterprise vendor EULA constraints.
