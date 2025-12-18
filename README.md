# 🤖 PyFlow-Architect: Autonomous Python DevTeam

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![UI](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)

**PyFlow-Architect** is an advanced, multi-agent development system designed to automate the lifecycle of Python programming. Unlike standard AI chat bots, this system utilizes a "Scout-Mechanic-Inspector" loop to plan, write, and internally verify code before delivery.



## 🧠 The Agentic Workflow

The system operates using a state-machine architecture powered by **LangGraph**. Every request cycles through a rigorous development process:

1.  **🔍 The Scout**: Analyzes user requirements, identifies necessary libraries, and drafts a step-by-step logic plan.
2.  **🔧 The Mechanic**: Translates the Scout's plan into specialized, raw Python code. It is trained to handle complex algorithms and fallback to native libraries if necessary.
3.  **🕵️ The Inspector**: Executes the generated code in a secure internal environment using `exec()`. If the code fails (SyntaxError, LogicError, or AssertionError), the Inspector captures the traceback and sends it back to the Mechanic for automatic repair.

## ✨ Key Features

* **Self-Healing Code**: Automatically detects and fixes its own bugs via an internal feedback loop.
* **Zero-Dependency Fallbacks**: Capable of switching from high-level frameworks (like Flask) to standard library alternatives (like http.server) if environment constraints arise.
* **Mathematical Precision**: Optimized for complex computational geometry, numerical methods, and algorithmic design.
* **Transparent Reasoning**: A dedicated "Thinking Process" UI component allows users to audit the logic of every agent in real-time.



## 🛠️ Installation

1. **setup**
   ```bash
   git clone [https://github.com/DhashubhanKumar/PyFlow-Architect.git](https://github.com/DhashubhanKumar/PyFlow-Architect.git)
   cd PyFlow-Architect
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   GROQ_API_KEY=your_api_key_here
   streamlit run app.py
