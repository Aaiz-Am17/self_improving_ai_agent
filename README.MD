# Self-Improving Autonomous Data Pipeline Agent

### Agentic AI System using LoRA + LangGraph

![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Framework-orange)
![LoRA](https://img.shields.io/badge/Fine--Tuning-LoRA-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

An **Agentic AI system** that analyzes datasets, recommends machine learning pipelines, and **improves itself using user feedback via LoRA fine-tuning**.

This project demonstrates how modern **AI agents can assist ML engineers by automating early-stage data science workflows**.

---

# Overview

Machine learning practitioners spend a large portion of their time on repetitive tasks such as:

* data inspection
* missing value handling
* feature encoding
* selecting baseline models
* designing preprocessing pipelines

These tasks require experience and are often done manually.

Current AI tools can suggest solutions but **do not improve based on user feedback**.

This project introduces a **self-improving ML assistant** capable of:

1. Inspecting datasets
2. Recommending preprocessing pipelines
3. Generating baseline machine learning models
4. Learning from user corrections

The system improves its recommendations through a **continuous learning loop using LoRA fine-tuning**.

---

# Key Features

## Dataset Understanding

Automatically analyzes uploaded datasets to detect:

* column types
* missing values
* outliers
* categorical features
* class imbalance

---

## Pipeline Generation

Generates recommended preprocessing steps and baseline ML models.

Example output:

Cleaning Plan

Age → Median Imputation
TransactionAmount → Log Transformation
Category → One Hot Encoding

Model Recommendation

XGBoost Classifier

---

## Agentic Reasoning

The system follows the **Perceive → Reason → Act** paradigm.

Perceive

* Read datasets
* Retrieve knowledge from vector database

Reason

* Decide which analysis tools to use
* Plan preprocessing strategies

Act

* Execute Python tools to generate pipelines

---

## Self-Improving Feedback Loop

Users can provide corrections such as:

> “Median imputation is not ideal here. Use KNN imputation instead.”

The system will:

1. Store the feedback
2. Convert it into training examples
3. Fine-tune the model using **LoRA**

This creates a **continually improving ML assistant**.

---

# System Architecture

The system is composed of several interacting components.

```
User
  │
  │ Upload Dataset
  ▼
Dataset Inspection Tools
  │
  ▼
LangGraph Agent
  │
  ├── Tool Selection
  ├── Pipeline Reasoning
  └── Model Recommendation
  │
  ▼
Generated ML Pipeline
  │
  ▼
User Feedback
  │
  ▼
Feedback Dataset
  │
  ▼
LoRA Fine-Tuning
  │
  ▼
Improved Model
```

---

# Technology Stack

### Programming Language

Python 3.12

---

### Agent Framework

LangGraph
LangChain

---

### Machine Learning

Scikit-learn
XGBoost
Pandas
NumPy

---

### Vector Database

ChromaDB

---

### Fine-Tuning

PEFT (LoRA)

---

### Deployment

FastAPI
Docker

---

# Project Structure

```
self_improving_ai_agent/

data/
│
├── datasets/
│   ├── titanic.csv
│   ├── housing.csv
│   └── credit_risk.csv
│
├── feedback/
│   └── corrections.json
│

src/

├── agent/
│   ├── langgraph_agent.py
│   └── reasoning_loop.py
│
├── tools/
│   ├── inspect_dataset.py
│   ├── detect_missing_values.py
│   ├── detect_outliers.py
│   └── recommend_pipeline.py
│
├── training/
│   ├── create_training_data.py
│   └── lora_finetune.py
│
├── vector_db/
│   └── chroma_setup.py
│
├── api/
│   └── fastapi_server.py
│
└── main.py

README.md
requirements.txt
```

---

# Installation

Clone the repository

```
git clone https://github.com/yourusername/self-improving-ai-agent
cd self-improving-ai-agent
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

---

# Running the Project

Run the main agent

```
python src/main.py
```

Start API server

```
uvicorn src.api.fastapi_server:app --reload
```

---

# Example Workflow

1. Upload dataset
2. Agent analyzes dataset
3. Agent generates preprocessing pipeline
4. User reviews suggestion
5. User provides correction
6. Correction stored as training example
7. LoRA fine-tuning improves the model

---

# Evaluation Metrics

## Functional Metrics

* successful dataset inspection
* correct tool selection
* valid ML pipeline generation

---

## Model Metrics

* accuracy of preprocessing recommendations
* improvement after LoRA fine-tuning

---

## System Metrics

* reasoning trace clarity
* latency of responses
* reliability of LangGraph nodes

---

# Project Roadmap

### Phase 1 — Project Setup

* repository structure
* dataset collection
* basic dataset inspection tools

### Phase 2 — Agent Development

* LangGraph reasoning loop
* tool integration

### Phase 3 — Pipeline Generation

* preprocessing recommendations
* baseline model generation

### Phase 4 — Feedback System

* correction storage
* feedback dataset creation

### Phase 5 — LoRA Fine-Tuning

* training dataset preparation
* model adaptation

### Phase 6 — Deployment

* FastAPI API
* Docker containerization

---

# Future Improvements

* automatic hyperparameter tuning
* AutoML integration
* dataset recommendation systems
* multi-agent architecture

---

# Contributions

Contributions are welcome.

If you would like to improve the project:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

# License

This project is released under the MIT License.

---

# Author

Aaiz Mohsin
BS Artificial Intelligence
Ghulam Ishaq Khan Institute of Engineering Sciences and Technology
