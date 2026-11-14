import numpy as np


def patchify(images: np.ndarray, patch_size: int) -> np.ndarray:
    """Return ordered patch vectors with shape (B,N,C*P*P)."""
    pass


def unpatchify(patches: np.ndarray, image_shape: tuple[int, int, int, int],
               patch_size: int) -> np.ndarray:
    """Recover an independently owned (B,C,H,W) image tensor."""
    pass
