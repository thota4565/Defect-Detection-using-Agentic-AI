"""
predict_all.py
Runs the trained model on ALL test images and reports:
- Correct predictions
- Wrong predictions
- Final test accuracy
- Saves results with timestamp
- Saves CSV in /results
- Saves wrong predictions for inspection
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from pathlib import Path
from PIL import Image
import csv
from datetime import datetime
import shutil


# -----------------------------
# Image Preprocessing
# -----------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# -----------------------------
# Load Model
# -----------------------------
def load_model(model_path, num_classes=2):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    return model


# -----------------------------
# Predict Single Image
# -----------------------------
def predict(model, img_path, class_names):
    img = Image.open(img_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        prob = torch.softmax(outputs, dim=1)
        conf, pred = torch.max(prob, 1)

    return class_names[pred.item()], float(conf.item())


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def run_full_test():

    print("\n🔍 Running full Test Dataset Evaluation...\n")

    project_root = Path.cwd().parent
    test_dir = project_root / "data" / "casting_data" / "test"
    model_path = project_root / "models" / "best_model.pth"
    results_dir = project_root / "results"
    wrong_dir = results_dir / "wrong_predictions"

    results_dir.mkdir(exist_ok=True)
    wrong_dir.mkdir(exist_ok=True)

    class_names = ["def_front", "ok_front"]

    # Load model
    model = load_model(model_path, num_classes=len(class_names))

    # For CSV output filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = results_dir / f"test_results_{timestamp}.csv"

    total = 0
    correct = 0

    with open(csv_path, "w", newline="") as file:
        writer = csv.writer(file)

        # Updated CSV header with timestamp
        writer.writerow(["Image", "True Label", "Predicted Label", "Confidence", "Timestamp"])

        # Loop through both folders
        for label_name in ["def_front", "ok_front"]:
            folder_path = test_dir / label_name

            for img_path in folder_path.glob("*.*"):
                total += 1
                pred_label, confidence = predict(model, img_path, class_names)

                # Per-image timestamp
                img_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Count accuracy
                if pred_label == label_name:
                    correct += 1
                else:
                    # Copy wrong predictions
                    shutil.copy(img_path, wrong_dir / f"WRONG_{img_path.name}")

                # Write row including timestamp
                writer.writerow([
                    img_path.name,
                    label_name,
                    pred_label,
                    round(confidence, 4),
                    img_timestamp
                ])

    accuracy = correct / total

    print(f"Total images      : {total}")
    print(f"Correct predictions: {correct}")
    print(f"Wrong predictions  : {total - correct}")
    print(f"Final Test Accuracy: {accuracy * 100:.2f}%")
    print(f"\n📁 CSV saved at: {csv_path}")
    print(f"📁 Wrong images saved in: {wrong_dir}")


if __name__ == "__main__":
    run_full_test()
