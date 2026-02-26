"""
train_cnn.py

This script trains a ResNet-18 model to classify casting images as Good or Defective.
It loads the dataset using our data_loader, fine-tunes the last layer for 2 classes,
saves the best weights, and also plots/saves accuracy & loss graphs.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from pathlib import Path
import matplotlib.pyplot as plt

from data_loader import make_dataloaders


def train_model():

    # -----------------------------
    # 1. Paths
    # -----------------------------
    project_root = Path.cwd().parent  # since running from /src
    data_dir = project_root / "data" / "casting_data"
    save_dir = project_root / "models"
    results_dir = project_root / "results"

    save_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    # -----------------------------
    # 2. Create dataloaders
    # -----------------------------
    dataloaders, class_names = make_dataloaders(
        str(data_dir),
        batch_size=16,
        img_size=224,
        num_workers=0,      # Windows safe
        pin_memory=False
    )

    print("Classes:", class_names)

    # -----------------------------
    # 3. Select device
    # -----------------------------
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # -----------------------------
    # 4. Load pretrained ResNet18
    # -----------------------------
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

    # Replace last FC layer → 2 output classes
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(class_names))

    model = model.to(device)

    # -----------------------------
    # 5. Loss + Optimizer
    # -----------------------------
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    # -----------------------------
    # 6. History Lists
    # -----------------------------
    train_losses = []
    test_losses = []
    train_accuracies = []
    test_accuracies = []

    # -----------------------------
    # 7. Training Loop
    # -----------------------------
    epochs = 5
    best_accuracy = 0.0
    best_model_path = save_dir / "best_model.pth"

    for epoch in range(epochs):
        print(f"\nEpoch {epoch+1}/{epochs}")
        print("-" * 30)

        for phase in ["train", "test"]:
            model.train() if phase == "train" else model.eval()

            running_loss = 0.0
            running_corrects = 0

            for images, labels in dataloaders[phase]:
                images = images.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                    _, preds = torch.max(outputs, 1)

                    if phase == "train":
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * images.size(0)
                running_corrects += torch.sum(preds == labels)

            # Epoch results
            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            print(f"{phase.capitalize()} Loss: {epoch_loss:.4f}  Acc: {epoch_acc:.4f}")

            # Save values for graphs
            if phase == "train":
                train_losses.append(epoch_loss)
                train_accuracies.append(epoch_acc.item())
            else:
                test_losses.append(epoch_loss)
                test_accuracies.append(epoch_acc.item())

                # Save best model
                if epoch_acc > best_accuracy:
                    best_accuracy = epoch_acc
                    torch.save(model.state_dict(), best_model_path)
                    print(f"→ Saved Best Model with Acc: {best_accuracy:.4f}")

    print("\nTraining Completed!")
    print("Best model saved at:", best_model_path)

    # -----------------------------
    # 8. Plot & Save Accuracy Curve
    # -----------------------------
    plt.figure(figsize=(8, 6))
    plt.plot(train_accuracies, label="Train Accuracy", marker='o')
    plt.plot(test_accuracies, label="Test Accuracy", marker='o')
    plt.title("Accuracy Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)
    plt.savefig(results_dir / "accuracy_curve.png")
    plt.show()

    # -----------------------------
    # 9. Plot & Save Loss Curve
    # -----------------------------
    plt.figure(figsize=(8, 6))
    plt.plot(train_losses, label="Train Loss", marker='o')
    plt.plot(test_losses, label="Test Loss", marker='o')
    plt.title("Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)
    plt.savefig(results_dir / "loss_curve.png")
    plt.show()


if __name__ == "__main__":
    train_model()

