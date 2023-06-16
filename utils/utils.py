import torch
import numpy as np


def generate_collate_fn(tokenizer, label2index, max_lenth=512, device="cpu"):
    def collate_fn(batch):
        texts, labels = [], []
        for item in batch:
            label = []
            for annotation in item["annotations"]:
                span = (annotation["start"], annotation["end"])
                label_index = label2index[annotation["type"]]
                label.append({"span": span, "label_index": label_index})
            texts.append(item["text"])
            labels.append(label)
        tokens_inputs = tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
            return_offsets_mapping=True,
        )
        token_labels = np.zeros(tokens_inputs["input_ids"].shape)

        offset_mapping = tokens_inputs.pop("offset_mapping")

        for i, mapping in enumerate(offset_mapping):
            for label in labels[i]:
                is_start = 0
                label_span = label["span"]
                label_index = label["label_index"]
                for j, span in enumerate(mapping):
                    if span[0] >= label_span[0] and span[1] <= label_span[1]:
                        if is_start == 0:
                            token_labels[i, j] = 2 * label_index - 1
                            is_start = 1
                        else:
                            token_labels[i, j] = 2 * label_index
        token_labels = torch.tensor(token_labels, dtype=torch.long).to(device)
        tokens_inputs = {
            key: tensor.to(device) for key, tensor in tokens_inputs.items()
        }
        return (tokens_inputs, token_labels)

    return collate_fn


def generate_parse_fn(tokenizer, index2label):
    def parse_fn(preds, sample_id, offset_mapping, text):
        preds = torch.argmax(preds, dim=-1)
        start, end, flag = 0, 0, 0
        Entitys = []

        for i, index in enumerate(preds.tolist()):
            if index % 2 == 1 and flag == 0:
                start, end, flag = i, i, index
            elif flag != 0 and index == flag + 1:
                end = i
            elif flag != 0:
                span = (offset_mapping[start][0], offset_mapping[end][1])
                print(start, index)
                Entitys.append(
                    {
                        "sample_id": sample_id,
                        "span": text[span[0] : span[1]],
                        "type": index2label[(flag + 1) // 2],
                    }
                )
                flag = 0
                if index % 2 == 1:
                    start, end, flag = i, i, index
            else:
                flag = 0

        return Entitys

    return parse_fn
