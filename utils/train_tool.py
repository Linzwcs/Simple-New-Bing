import os, sys, time
import numpy as np
import pandas as pd
import datetime
from tqdm import tqdm
import torch
from torch import nn
from copy import deepcopy


def printlog(info):
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "==========" * 8 + "%s" % nowtime)
    print(str(info) + "\n")


class StepRunner:
    def __init__(self, net, loss_fn, stage="train", metrics_dict=None, optimizer=None):
        self.net, self.loss_fn, self.metrics_dict, self.stage = (
            net,
            loss_fn,
            metrics_dict,
            stage,
        )
        self.optimizer = optimizer

    def step(self, features, labels):
        # ////////////////////////////////////////////////////////////////
        preds = self.net(**features)  # .logits
        loss = self.loss_fn(preds.view(-1, preds.size(-1)), labels.view(-1))

        # ////////////////////////////////////////////////////////////////

        if self.optimizer is not None and self.stage == "train":
            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()

        step_metrics = {
            self.stage
            + "_"
            + name: metric_fn(preds.view(-1, preds.size(-1)), labels.view(-1)).item()
            for name, metric_fn in self.metrics_dict.items()
        }

        return loss.item(), step_metrics

    def train_step(self, features, labels):
        self.net.train()
        return self.step(features, labels)

    @torch.no_grad()
    def eval_step(self, features, labels):
        self.net.eval()
        return self.step(features, labels)

    def __call__(self, features, labels):
        if self.stage == "train":
            return self.train_step(features, labels)
        else:
            return self.eval_step(features, labels)


class EpochRunner:
    def __init__(self, steprunner):
        self.steprunner = steprunner
        self.stage = steprunner.stage

    def __call__(self, dataloader):
        total_loss, step = 0, 0
        loop = tqdm(enumerate(dataloader), total=len(dataloader), file=sys.stdout)

        for i, batch in loop:
            loss, step_metrics = self.steprunner(*batch)

            step_log = dict({self.stage + "_loss": loss}, **step_metrics)
            total_loss += loss
            step += 1
            if i != len(dataloader) - 1:
                loop.set_postfix(**step_log)
            else:
                epoch_loss = total_loss / step

                epoch_metrics = {
                    self.stage + "_" + name: metric_fn.compute().item()
                    for name, metric_fn in self.steprunner.metrics_dict.items()
                }
                epoch_log = dict({self.stage + "_loss": epoch_loss}, **epoch_metrics)
                loop.set_postfix(**epoch_log)

                for name, metric_fn in self.steprunner.metrics_dict.items():
                    metric_fn.reset()

        return epoch_log


def train_model(
    net,
    optimizer,
    loss_fn,
    metrics_dict,
    train_data,
    val_data=None,
    epochs=10,
    ckpt_path="./checkpoints/checkpoint.pt",
    patience=5,
    monitor="val_loss",
    mode="min",
):
    history = {}

    for epoch in range(1, epochs + 1):
        printlog("Epoch {0} / {1}".format(epoch, epochs))

        train_step_runner = StepRunner(
            net=net,
            stage="train",
            loss_fn=loss_fn,
            metrics_dict=deepcopy(metrics_dict),
            optimizer=optimizer,
        )
        train_epoch_runner = EpochRunner(train_step_runner)
        train_metrics = train_epoch_runner(train_data)

        for name, metric in train_metrics.items():
            history[name] = history.get(name, []) + [metric]

        if val_data:
            val_step_runner = StepRunner(
                net=net,
                stage="val",
                loss_fn=loss_fn,
                metrics_dict=deepcopy(metrics_dict),
            )
            val_epoch_runner = EpochRunner(val_step_runner)
            with torch.no_grad():
                val_metrics = val_epoch_runner(val_data)
            val_metrics["epoch"] = epoch
            for name, metric in val_metrics.items():
                history[name] = history.get(name, []) + [metric]

        arr_scores = history[monitor]
        best_score_idx = (
            np.argmax(arr_scores) if mode == "max" else np.argmin(arr_scores)
        )
        if best_score_idx == len(arr_scores) - 1:
            torch.save(net.state_dict(), ckpt_path)
            print(
                "<<<<<< reach best {0} : {1} >>>>>>".format(
                    monitor, arr_scores[best_score_idx]
                )
            )
        if len(arr_scores) - best_score_idx > patience:
            print(
                "<<<<<< {} without improvement in {} epoch, early stopping >>>>>>".format(
                    monitor, patience
                )
            )
            break
    net.load_state_dict(torch.load(ckpt_path))

    return pd.DataFrame(history)
