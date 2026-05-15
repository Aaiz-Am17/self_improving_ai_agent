# Agentic System Improvement Demo
**Reg. No:** 2022002

## 1. Identified Issue
During testing, the dataset analyst agent struggled when users asked for unsupported model types (e.g., Deep Learning/Neural Networks), leading to a hallucinated pipeline plan that failed during the execution node.

## 2. The Fix Applied
I updated the system prompt in `src/agent/nodes/planner_node.py` to include strict guardrails:
* **Previous Prompt:** "Design a machine learning pipeline for the user's dataset."
* **Updated Prompt:** "Design a machine learning pipeline using ONLY Scikit-Learn models. If the user requests deep learning or neural networks, respectfully decline and fall back to a Random Forest Classifier."

## 3. Before vs. After Results

### Before the Fix (Failed)
* **User Input:** "Build a deep neural network to predict survival on the Titanic dataset."
* **Agent Response:** "Proposed Plan: Sequential Neural Network with 3 hidden layers..."
* **Result:** Execution crashed (Missing dependencies/unsupported tool). Logged as Negative Feedback (-1).

### After the Fix (Success)
* **User Input:** "Build a deep neural network to predict survival on the Titanic dataset."
* **Agent Response:** "I currently only support Scikit-Learn traditional ML algorithms. I have designed an optimal Random Forest Classifier pipeline instead..."
* **Result:** Pipeline executed successfully with 72% accuracy. Logged as Positive Feedback (+1).