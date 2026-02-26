# 🏭 Agentic AI – Conveyor Belt Defect Detection

An interactive **Agentic AI-powered defect detection system** simulating real-time quality inspection on a conveyor belt.

This project demonstrates:
- Multi-agent workflow orchestration
- Deep learning-based image classification (ResNet-18)
- Streamlit-based live production simulation
- Real-time inspection dashboard
- Automated batch reporting

---

## 🚀 Project Overview

This system simulates an industrial production line where:

1. Products move on a conveyor belt
2. AI agents inspect each item
3. A classification model predicts:
   - ✅ OK
   - ❌ Defective
4. The system automatically decides:
   - ACCEPT
   - REJECT
5. A final inspection report is generated

---

## 🧠 Agent Workflow

Each frame passes through an agent graph:

```
Image → Detection Agent → Classification Agent → Decision Agent → Report Agent
```

The agents return:
- Prediction
- Confidence
- Action
- Timestamp

---

## 🎥 Features

- 🎬 Conveyor belt animation
- 🤖 Agent-based inference workflow
- 📊 Real-time system health dashboard
- 📦 Batch processing (30–80 images)
- 📑 Inspection report table
- ⬇ Downloadable CSV report
- 🩺 Production health monitoring logic

---

## 🛠 Tech Stack

- Python
- Streamlit
- PyTorch (ResNet-18)
- Pandas
- Pillow (PIL)
- Multi-agent workflow architecture

---

## 📂 Project Structure

```
defect-detection-agentic-ai/
│
├── streamlit_app.py
├── src/
│   ├── conveyor_belt.py
│   ├── agents_graph.py
│
├── data/
│   └── casting_data/
│
├── models/
├── results/
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/defect-detection-agentic-ai.git
cd defect-detection-agentic-ai
```

### 2️⃣ Create virtual environment

```
python -m venv defect_env
defect_env\Scripts\activate
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```
streamlit run streamlit_app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 📊 System Metrics

The dashboard displays:

- 🩺 System Health (Healthy / Warning / Critical)
- 🤖 Model version
- ⏱ Processing time
- 📦 Total items processed
- ❌ Defective count
- 🚀 Throughput (items/sec)

---

## 📂 Dataset

This project uses the **Casting Defect Detection Dataset**:

- Defective (def_front)
- OK (ok_front)

Dataset is not included in this repository due to size.
https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product

---

## ⚠️ Disclaimer

This is a simulated industrial system built for demonstration and research purposes.

---

## 👨‍💻 Author

Agentic AI Industrial Automation Simulation Project
