# Asana RL Environment - Enterprise Seed Dataset

This repository contains a research-grade synthetic dataset and generation pipeline for simulating an enterprise Asana workspace.
The dataset is designed to serve as high-fidelity seed data for reinforcement learning environments used to train and evaluate computer-use AI agents operating inside project management systems.

The simulation models a B2B SaaS company (**Vertexloop AI**) with approximately **8,000 employees** across Engineering, Marketing, Sales, Operations, Support, HR, and Product teams.

---

## Project Structure

```
.
├── README.md
├── requirements.txt
├── schema.sql
├── .env.example
├── src/
│   ├── main.py
│   ├── generators/
│   │   ├── users.py
│   │   ├── teams.py
│   │   ├── projects.py
│   │   ├── sections.py
│   │   ├── tasks.py
│   │   └── comments.py
│   └── utils/
│       ├── init_db.py
│       ├── db.py
│       ├── build_pools.py
│       └── hf_pool.py
└── output/
    └── asana_simulation.sqlite
```

---

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API key (only needed once)

Create `.env` from `.env.example` and add:

```
HUGGINGFACE_TOKEN=your_api_key_here
```

---

## Build LLM Content Pools (one-time)

Human-language content (task names, descriptions, comments) is generated once and cached.

```bash
python -m src.utils.build_pools
```

This creates cached pools used by the generators to avoid repeated API calls.

---

## Generate the Asana Workspace

```bash
python -m src.main
```

This builds the full enterprise workspace and outputs:

```
output/asana_simulation.sqlite
```



