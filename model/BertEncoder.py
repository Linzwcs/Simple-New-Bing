from transformers import AutoModel
from torch import nn


class BertEncoder(nn.Module):
    def __init__(self, model_path="bert-base-chinese", freeze=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encoder = AutoModel.from_pretrained(model_path)
        if freeze:
            for name, param in self.encoder.parameters():
                param.requires_grad = False

    def forward(self, **inputs):
        return self.encoder(**inputs).last_hidden_state
