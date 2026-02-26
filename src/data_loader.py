"""
src/data_loader.py

Creates PyTorch ImageFolder datasets and DataLoaders for train/test.
Assumes dataset layout:
    data/
      casting_data/
         train/
            def_front/
            ok_front/
         test/
            def_front/
            ok_front/

Functions:
- get_transforms(img_size, train=True): torchvision transforms for augmentation/normalization
- make_dataloaders(data_dir, batch_size=32, img_size=224, num_workers=4): returns dict of dataloaders and class_names
- show_sample_batch(loader): helper to quickly visualize one batch (uses matplotlib)
"""

from pathlib import Path
from typing import Tuple, Dict, List
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np


def get_transforms(img_size: int = 224, train: bool = True):
    """
    Return torchvision transforms.
    - img_size: final size (square) for model input
    - train: whether to include basic augmentations
    """
    # Normalization values (ImageNet) - good default for ResNet-style models
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])

    if train:
        transform = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=12),
            transforms.ColorJitter(brightness=0.1, contrast=0.1),
            transforms.ToTensor(),
            normalize,
        ])
    else:
        transform = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            normalize,
        ])

    return transform


def make_dataloaders(data_dir: str,
                     batch_size: int = 32,
                     img_size: int = 224,
                     num_workers: int = 4,
                     pin_memory: bool = True) -> Tuple[Dict[str, DataLoader], List[str]]:
    """
    Build PyTorch DataLoaders for train and test folders.

    Args:
        data_dir: path to 'casting_data' directory (the parent of 'train' and 'test')
        batch_size: batch size for loaders
        img_size: image resize side length
        num_workers: DataLoader workers for parallel loading (set 0 on Windows if issues)
        pin_memory: boolean for CUDA performance (True if using GPU)

    Returns:
        dataloaders: {'train': DataLoader, 'test': DataLoader}
        class_names: list e.g. ['def_front', 'ok_front']
    """
    data_dir = Path(data_dir)
    train_dir = data_dir / "train"
    test_dir = data_dir / "test"

    if not train_dir.exists() or not test_dir.exists():
        raise FileNotFoundError(f"Expected `train/` and `test/` inside {data_dir}. "
                                "Check extraction or pass the correct data_dir.")

    train_dataset = datasets.ImageFolder(
        root=str(train_dir),
        transform=get_transforms(img_size=img_size, train=True)
    )

    test_dataset = datasets.ImageFolder(
        root=str(test_dir),
        transform=get_transforms(img_size=img_size, train=False)
    )

    class_names = train_dataset.classes  # order matters for predictions/labels

    # DataLoaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory
    )

    dataloaders = {"train": train_loader, "test": test_loader}
    return dataloaders, class_names


def imshow_batch(images: torch.Tensor, labels: torch.Tensor, class_names: List[str], n: int = 8):
    """
    Show a grid of images from a batch (after normalization reversal).
    images: tensor shape (B, C, H, W)
    labels: tensor of ints
    """
    # unnormalize with ImageNet stats
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    images = images.cpu().numpy()
    images = images[:n]
    labels = labels[:n].cpu().numpy()

    fig, axes = plt.subplots(1, n, figsize=(n * 2.2, 2.5))
    for idx in range(n):
        img = images[idx].transpose((1, 2, 0))  # CHW -> HWC
        img = std * img + mean
        img = np.clip(img, 0, 1)
        ax = axes[idx]
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(class_names[labels[idx]])
    plt.show()


def show_sample_batch(loader: DataLoader, class_names: List[str], device: torch.device = torch.device("cpu")):
    """
    Pull one batch from loader and visualize examples.
    Use this to confirm dataset mapping and transforms.
    """
    batch = next(iter(loader))
    images, labels = batch
    imshow_batch(images, labels, class_names)


# Quick test function usable from command-line:
if __name__ == "__main__":
    # Minimal smoke test when running: python src/data_loader.py
    import os
    from pathlib import Path

    # Try to auto-locate dataset in project 'data/casting_data'
    project_root = Path.cwd().parent # when executed from /src this points to project root
    default_data = project_root / "data" / "casting_data"

    print("Project root detected as:", project_root)
    print("Looking for dataset at:", default_data)

    dataloaders, class_names = make_dataloaders(str(default_data), batch_size=8, img_size=224, num_workers=0, pin_memory=False)
    print("Classes found:", class_names)
    print("Train batches available:", len(dataloaders["train"]))
    print("Test  batches available:", len(dataloaders["test"]))

    # Optionally visualize one batch (comment/uncomment as needed)
    try:
        show_sample_batch(dataloaders["train"], class_names)
    except Exception as e:
        print("Could not display images (maybe running in headless environment). Error:", e)
