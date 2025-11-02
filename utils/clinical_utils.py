try:
    import torch
    from transformers import AutoTokenizer, AutoModel
    _TRANSFORMERS_AVAILABLE = True
except ImportError:
    _TRANSFORMERS_AVAILABLE = False
    torch = None
    AutoTokenizer = None
    AutoModel = None


class ClinicalEmbedder:
    """Lightweight clinical text embedder stub.
    
    For Render free tier (512MB RAM), we use a lightweight approach:
    - Uses hash-based deterministic embedding to avoid loading transformer models
    - Produces 384-dim embedding (same as sentence-transformers/all-MiniLM-L6-v2)
    """
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", embedding_dim=384):
        if not _TRANSFORMERS_AVAILABLE:
            # For now, use a deterministic hash-based approach instead of loading transformer
            # This allows the app to work on low-memory systems
            import hashlib
            import numpy as np
            self.use_hash = True
            self.embedding_dim = embedding_dim
            return
        
        # If torch/transformers are available, use them (but only on high-memory systems)
        self.use_hash = False
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to("cpu")
        self.model.eval()
        self.embedding_dim = embedding_dim

    def get_embedding(self, text):
        """Get embedding for text. Returns tensor of shape (1, 384)."""
        if self.use_hash:
            # Lightweight hash-based embedding
            import hashlib
            import numpy as np
            h = hashlib.sha256(text.encode()).digest()
            seed = int.from_bytes(h[:8], 'big')
            np.random.seed(seed % (2**32))
            embedding = np.random.randn(1, self.embedding_dim).astype(np.float32)
            embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
            return torch.from_numpy(embedding)
        else:
            # Transformer-based embedding
            import torch
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=256
            )
            with torch.no_grad():
                outputs = self.model(**inputs)
            # Mean pooling
            token_embeddings = outputs[0]
            input_mask_expanded = inputs['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
            sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)
            sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)
            return sum_embeddings / sum_mask




