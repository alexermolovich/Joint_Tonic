import numpy as np

def encode_boxes(boxes: np.ndarray, image_size: tuple[int,int], frequencies: np.ndarray, corner_embeddings: np.ndarray) -> np.ndarray:
    """Encode a Box Prompt with Positional Features. See the problem contract for shapes and units."""
    raise NotImplementedError
