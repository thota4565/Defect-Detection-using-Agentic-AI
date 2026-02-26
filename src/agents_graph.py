# src/agents_graph.py

from typing import TypedDict, Optional
from pathlib import Path
from datetime import datetime

from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
from langgraph.graph import StateGraph, END

# ==========================================
# CONFIG
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "best_model.pth"

# Your original training classes:
# 0 -> def_front (defect), 1 -> ok_front (good)
CLASS_NAMES = ["def_front", "ok_front"]

# ==========================================
# SHARED STATE (memory between agents)
# ==========================================
class ConveyorState(TypedDict, total=False):
    frame: Image.Image          # current frame
    image_name: str             # "Image 0", "Image 1", ...
    frame_id: int               # index in sequence
    prediction: str             # "OK" / "Defective" / "ERROR"
    confidence: float           # 0.0–1.0
    action: str                 # "ACCEPT" / "REJECT" / "ERROR"
    timestamp: str              # when processed
    error: Optional[str]        # error text if any


# ==========================================
# MODEL + TRANSFORMS
# ==========================================
_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

_model: Optional[nn.Module] = None


def load_model() -> nn.Module:
    """Load ResNet18 once and reuse."""
    global _model
    if _model is None:
        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, len(CLASS_NAMES))

        state_dict = torch.load(MODEL_PATH, map_location="cpu")
        model.load_state_dict(state_dict)
        model.eval()
        _model = model
    return _model


def classify_frame(frame: Image.Image) -> tuple[str, float]:
    """
    Run ResNet18 on a belt frame.
    Returns label: "OK" or "Defective", and confidence 0–1.
    """
    model = load_model()
    img = frame.convert("RGB")
    tensor = _transform(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(tensor)
        prob = torch.softmax(outputs, dim=1)
        conf, idx = torch.max(prob, 1)

    class_name = CLASS_NAMES[idx.item()]
    if class_name == "def_front":
        label = "Defective"
    else:
        label = "OK"

    return label, float(conf.item())


# ==========================================
# AGENT NODES
# ==========================================

def vision_agent(state: ConveyorState) -> ConveyorState:
    """Vision Agent: just checks that a frame is present."""
    if "frame" not in state or state["frame"] is None:
        return {"error": "VisionAgent: No frame provided"}
    return {}  # no change


def analysis_agent(state: ConveyorState) -> ConveyorState:
    """Analysis Agent: classify frame with ResNet18."""
    try:
        frame = state["frame"]
        label, conf = classify_frame(frame)
        return {
            "prediction": label,
            "confidence": conf,
            "error": None,
        }
    except Exception as e:
        return {
            "prediction": "ERROR",
            "confidence": 0.0,
            "error": f"AnalysisAgent error: {e}",
        }


def decision_agent(state: ConveyorState) -> ConveyorState:
    """Decision Agent: map prediction → action."""
    if state.get("error"):
        return {"action": "ERROR"}

    label = state.get("prediction", "ERROR")
    if label == "OK":
        action = "ACCEPT"
    elif label == "Defective":
        action = "REJECT"
    else:
        action = "ERROR"

    return {"action": action}


def report_agent(state: ConveyorState) -> ConveyorState:
    """Report Agent: add timestamp."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"timestamp": ts}


# ==========================================
# BUILD LANGGRAPH PIPELINE
# ==========================================
def build_app():
    graph = StateGraph(ConveyorState)

    graph.add_node("vision_agent", vision_agent)
    graph.add_node("analysis_agent", analysis_agent)
    graph.add_node("decision_agent", decision_agent)
    graph.add_node("report_agent", report_agent)

    graph.set_entry_point("vision_agent")
    graph.add_edge("vision_agent", "analysis_agent")
    graph.add_edge("analysis_agent", "decision_agent")
    graph.add_edge("decision_agent", "report_agent")
    graph.add_edge("report_agent", END)

    return graph.compile()


_app = None


def run_agents_on_frame(image_name: str, frame_id: int, frame: Image.Image) -> ConveyorState:
    """
    Called from Streamlit:
    - Takes one belt frame
    - Runs through Vision → Analysis → Decision → Report
    - Returns final ConveyorState with prediction / action / timestamp
    """
    global _app
    if _app is None:
        _app = build_app()

    init_state: ConveyorState = {
        "frame": frame,
        "image_name": image_name,
        "frame_id": frame_id,
    }

    final_state: ConveyorState = _app.invoke(init_state)
    return final_state


if __name__ == "__main__":
    # quick sanity check
    dummy = Image.new("RGB", (224, 224), color=(128, 128, 128))
    s = run_agents_on_frame("Image 0", 0, dummy)
    print("Test state:", s)
