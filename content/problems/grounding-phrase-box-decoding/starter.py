import numpy as np

def decode_grounded_boxes(boxes: np.ndarray, token_logits: np.ndarray, phrase_map: np.ndarray, image_size: tuple[int,int], threshold: float) -> dict:
    """Decode Phrase-Labeled Boxes. See the problem contract for shapes and units."""
    raise NotImplementedError
