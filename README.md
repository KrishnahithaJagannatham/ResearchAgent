# 🧠 Strategic Research Analyst Agent

🔗 **Live Demo:**  
https://researchagent-gmteqfvbtcjkka8wyjyhrj.streamlit.app/

---

## 📌 Overview

The **Strategic Research Analyst Agent** is a stateful, multi-step AI system designed to perform structured research rather than act as a simple chatbot.

It:

- Decomposes complex queries into strategic dimensions  
- Uses external search tools (Tavily API)  
- Scores evidence credibility  
- Iteratively refines research if confidence is low  
- Detects conflicting viewpoints  
- Generates a structured strategic intelligence report  
- Quantifies confidence in its findings  

Built using **LangGraph** for orchestration and **Streamlit** for UI.

---

## 🏗 Architecture

The agent follows a bounded refinement workflow:

User Input
  ↓
Strategic Planning
  ↓
Tool-Based Evidence Gathering
  ↓
Evidence Scoring
  ↓
Confidence Evaluation
  ↓
Refinement Loop (if low confidence)
  ↓
Conflict Detection
  ↓
Final Strategic Intelligence Report

## 🔁 Core Capabilities

- ✅ Multi-step reasoning  
- ✅ Autonomous tool usage  
- ✅ Self-evaluation & refinement loop  
- ✅ Evidence scoring  
- ✅ Conflict detection  
- ✅ Confidence tracking  
- ✅ Transparent thinking log  

---

## ⚠ Hallucination Mitigation

The system reduces hallucination risk through:

- External tool grounding (Tavily search)
- Evidence scoring heuristics
- Confidence threshold control
- Iteration cap to prevent infinite loops
- Structured prompt engineering

---

## 🧪 Stress Testing

Tested against:

- Ambiguous queries  
- Controversial topics  
- Sparse evidence domains  
- Biased/adversarial prompts  

The refinement mechanism improves reliability before final synthesis.

---

## 🛠 Tech Stack

- Python  
- LangGraph  
- Groq (LLM Provider)  
- Tavily API  
- Streamlit  
   

---

## 🎯 Why This Project Is Different

This is not a single-pass chatbot.

It is a **stateful autonomous research workflow** that:

- Plans  
- Acts  
- Evaluates  
- Improves  
- Synthesizes  

Designed for strategic decision support rather than conversational output.

---

## 👩‍💻 Author

Krishnahitha Jagannatham


