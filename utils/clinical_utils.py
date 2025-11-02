try:
    import torch
    from transformers import AutoTokenizer, AutoModel
    _TRANSFORMERS_AVAILABLE = True
except ImportError:
    _TRANSFORMERS_AVAILABLE = False
    torch = None
    AutoTokenizer = None
    AutoModel = None


def _mean_pooling(model_output, attention_mask):
    """Mean pooling from token embeddings, respecting attention mask."""
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)
    sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)
    return sum_embeddings / sum_mask


class ClinicalEmbedder:
    """Lightweight clinical text embedder.
    
    Uses a compact sentence-transformer model (all-MiniLM-L6-v2) by default.
    Embedding dimension is 384.
    """
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", embedding_dim=384):
        if not _TRANSFORMERS_AVAILABLE:
            raise RuntimeError("Transformers and PyTorch are required for ClinicalEmbedder")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to("cpu")
        self.model.eval()
        self.embedding_dim = embedding_dim

    def get_embedding(self, text):
        """Get embedding for text. Returns tensor of shape (1, embedding_dim)."""
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
        pooled = _mean_pooling(outputs, inputs.get("attention_mask"))
        return pooled



