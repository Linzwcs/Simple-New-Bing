import torch


def evaluate_recall(preds, labels, num_classes=19):
    preds = torch.argmax(preds, dim=-1)
    recall = 0
    for i in range(1, num_classes):
        i_labels = labels == i
        i_preds = preds == i
        recall_num = (i_labels * i_preds).sum()
        total_num = i_labels.sum()
        recall += recall_num / (total_num + 1e-5)
    return recall / (num_classes - 1)


def evaluate_precision(preds, labels, num_classes=19):
    preds = torch.argmax(preds, dim=-1)
    precision = 0
    for i in range(num_classes):
        i_labels = labels == i
        i_preds = preds == i
        recall_num = (i_labels * i_preds).sum()
        total_num = i_preds.sum()
        precision += recall_num / (total_num + 1e-5)
    return precision / (num_classes - 1)


def evaluate_f1(preds, labels, num_classes=19):
    recall = evaluate_recall(preds, labels, num_classes)
    precision = evaluate_precision(preds, labels, num_classes)
    f1 = 2 * (recall * precision) / (recall + precision)
    return f1 / (num_classes - 1)
