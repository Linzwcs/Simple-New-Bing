from torch import nn
from .BertEncoder import BertEncoder


class BertBilstm(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.encoder = BertEncoder()
        self.bilstm = nn.LSTM(
            input_size=768, hidden_size=384, batch_first=True, bidirectional=True
        )
        self.classifier = nn.Linear(768, 9)

    def forward(self, **inputs):
        x = self.encoder(**inputs)
        output, (hn, cn) = self.bilstm(x)
        # print(output.size())
        return self.classifier(output)
