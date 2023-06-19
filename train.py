import json
from transformers import AutoTokenizer, AutoModel
from torchmetrics import Accuracy
from torch import nn
from torch.utils.data import DataLoader
from model import BertBilstm
import torch
from utils import (
    evaluate_recall,
    evaluate_f1,
    evaluate_precision,
    train_model,
    generate_collate_fn,
)
from torchmetrics import Precision, Recall, F1Score

with open("./data/train.json", "r") as f:
    train_data = json.load(f)
with open("./data/test.json", "r") as f:
    test_data = json.load(f)
with open("./data/label2index.json", "r") as f:
    label2index = json.load(f)

precision = Precision(task="multiclass", num_classes=9)
recall = Recall(task="multiclass", num_classes=9)
f1 = F1Score(task="multiclass", num_classes=9)
device = "cuda" if torch.cuda.is_available() else "cpu"
precision.to(device)
recall.to(device)
f1.to(device)
bertbilstm = BertBilstm().to(device)
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
# net = AutoModel.from_pretrained("bert-base-chinese")
# net.to(device)
optimizer = torch.optim.Adam(bertbilstm.parameters(), lr=1e-5)
loss_fn = nn.CrossEntropyLoss()
metrics_dict = {"precision": precision, "recall": precision, "f1": precision}

collate_fn = generate_collate_fn(tokenizer, label2index, device=device)
dl_train = DataLoader(train_data[:3000], batch_size=10, collate_fn=collate_fn)
dl_test = DataLoader(test_data[:1000], batch_size=10, collate_fn=collate_fn)
history = train_model(
    bertbilstm,
    optimizer,
    loss_fn,
    metrics_dict,
    train_data=dl_train,
    val_data=dl_train,
    epochs=1,
    patience=5,
    monitor="val_f1",
    mode="max",
)
history.to_csv("./log/log.csv")
