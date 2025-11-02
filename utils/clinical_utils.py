try:try:

    import torch    import torch

    from transformers import AutoTokenizer, AutoModel    from transformers import AutoTokenizer, AutoModel

    _TRANSFORMERS_AVAILABLE = True    _TRANSFORMERS_AVAILABLE = True

except ImportError:except ImportError:

    _TRANSFORMERS_AVAILABLE = False    _TRANSFORMERS_AVAILABLE = False

    torch = None    torch = None

    AutoTokenizer = None    AutoTokenizer = None

    AutoModel = None    AutoModel = None





def _mean_pooling(model_output, attention_mask):def _mean_pooling(model_output, attention_mask):

    """Mean pooling from token embeddings, respecting attention mask."""    """Mean pooling from token embeddings, respecting attention mask."""

    token_embeddings = model_output[0]  # first element of model_output contains token embeddings    token_embeddings = model_output[0]  # first element of model_output contains token embeddings

    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()

    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)

    sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)    sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)

    return sum_embeddings / sum_mask    return sum_embeddings / sum_mask





class ClinicalEmbedder:class ClinicalEmbedder:

    """Lightweight clinical text embedder.    """Lightweight clinical text embedder.



    Uses a compact sentence-transformer model by default to reduce memory usage    Uses a compact sentence-transformer model by default to reduce memory usage

    and speed up startup on low-memory hosts (Render free tier ~512MiB RAM).    and speed up startup on low-memory hosts (Render free tier ~512MiB RAM).

    """    """

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):

        if not _TRANSFORMERS_AVAILABLE:        if not _TRANSFORMERS_AVAILABLE:

            raise RuntimeError("Transformers and PyTorch are required for ClinicalEmbedder")            raise RuntimeError("Transformers and PyTorch are required for ClinicalEmbedder")



        # Use low_cpu_mem_usage when available to reduce peak memory during loading        # Use low_cpu_mem_usage when available to reduce peak memory during loading

        kwargs = {}        kwargs = {}

        try:        try:

            kwargs = {"low_cpu_mem_usage": True}            kwargs = {"low_cpu_mem_usage": True}

        except Exception:        except Exception:

            kwargs = {}            kwargs = {}



        self.tokenizer = AutoTokenizer.from_pretrained(model_name)        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Load a small model to save RAM; move to CPU explicitly        # Load a small model to save RAM; move to CPU explicitly

        self.model = AutoModel.from_pretrained(model_name, **kwargs)        self.model = AutoModel.from_pretrained(model_name, **kwargs)

        self.model.to("cpu")        self.model.to("cpu")

        self.model.eval()        self.model.eval()



    def get_embedding(self, text):    def get_embedding(self, text):

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)

        with torch.no_grad():        with torch.no_grad():

            outputs = self.model(**inputs)            outputs = self.model(**inputs)

        pooled = _mean_pooling(outputs, inputs.get("attention_mask"))        pooled = _mean_pooling(outputs, inputs.get("attention_mask"))

        return pooled        return pooled

