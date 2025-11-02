import hashlib
import numpy as np

try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    torch = None
    _TORCH_AVAILABLE = False


class ClinicalEmbedder:
    """Ultra-lightweight clinical embedder using deterministic hashing.
    
    Produces consistent 384-dim embeddings from clinical text without
    loading any transformer models. Perfect for memory-constrained systems.
    """
    
    def __init__(self, embedding_dim=384):
        if not _TORCH_AVAILABLE:
            raise RuntimeError("PyTorch is required")
        self.embedding_dim = embedding_dim

    def get_embedding(self, text):
        """Generate deterministic embedding from text via hashing."""
        # Hash the text to get a reproducible seed
        h = hashlib.sha256(text.encode()).digest()
        seed = int.from_bytes(h[:8], 'big') % (2**32)
        
        # Use seed to generate consistent random embedding
        rng = np.random.RandomState(seed)
        embedding = rng.randn(1, self.embedding_dim).astype(np.float32)
        
        # Normalize to unit vector
        embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
        
        return torch.from_numpy(embedding)





