---
layout: libdoc/page
title: Basic Skills
permalink: /pytorch-lightning/lv0-basic-skills/
category: Pytorch lightning
description: "Basic Skills"
order: 2
---
{:toc}
- *Code:* 
<br>

source: https://lightning.ai/


## Level 1: Training a model

### Add import

```python
import os
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
import lightning.pytorch as pl
```

### Define the PyTorch nn.Modules

```python
class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Sequential(nn.Linear(28 * 28, 64), nn.ReLU(), nn.Linear(64, 3))

    def forward(self, x):
        return self.l1(x)


class Decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Sequential(nn.Linear(3, 64), nn.ReLU(), nn.Linear(64, 28 * 28))

    def forward(self, x):
        return self.l1(x)
```

### Define a LightningModule

The LightningModule is the full **recipe** that defines how your nn.Modules interact.

- The **training_step** defines how the *nn.Modules* interact together.
- In the **configure_optimizers** define the optimizer(s) for your models.

```python
class LitAutoEncoder(pl.LightningModule):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder

    def training_step(self, batch, batch_idx):
        # training_step defines the train loop.
        x, y = batch
        x = x.view(x.size(0), -1)
        z = self.encoder(x)
        x_hat = self.decoder(z)
        loss = F.mse_loss(x_hat, x)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer
```

### Define the training dataset

```python
dataset = MNIST(os.getcwd(), download=True, transform=transforms.ToTensor())
train_loader = DataLoader(dataset)
```

### Train the model

To train the model use the Lightning [Trainer](https://lightning.ai/docs/pytorch/stable/common/trainer.html) which handles all the engineering and abstracts away all the complexity needed for scale.

```python
# model
autoencoder = LitAutoEncoder(Encoder(), Decoder())

# train model
trainer = pl.Trainer()
trainer.fit(model=autoencoder, train_dataloaders=train_loader)
```

### Eliminate the training loop (Loại bỏ vòng lặp training)

Under the hood, the Lightning Trainer runs the following training loop on your behalf

```python
autoencoder = LitAutoEncoder(Encoder(), Decoder())
optimizer = autoencoder.configure_optimizers()

for batch_idx, batch in enumerate(train_loader):
    loss = autoencoder.training_step(batch, batch_idx)

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

The power of Lightning comes when the training loop gets complicated as you add validation/test splits, schedulers, distributed training and all the latest SOTA techniques.

With Lightning, you can add mix all these techniques together without needing to rewrite a new loop every time.

## Level 2: Add a validation and test set

### Validate and test a model

#### Add a test loop

To make sure a model can generalize to an unseen dataset (ie: to publish a paper or in a production environment) a dataset is normally split into two parts, the *train* split and the *test* split.

The test set is **NOT** used during training, it is **ONLY** used once the model has been trained to see how the model will do in the real-world.

##### Find the train and test splits

Datasets come with two splits. Refer to the dataset documentation to find the *train* and *test* splits.

```python
import torch.utils.data as data
from torchvision import datasets
import torchvision.transforms as transforms

# Load data sets
transform = transforms.ToTensor()
train_set = datasets.MNIST(root="MNIST", download=True, train=True, transform=transform)
test_set = datasets.MNIST(root="MNIST", download=True, train=False, transform=transform)
```

##### Define the test loop

To add a test loop, implement the **test_step** method of the LightningModule

```python
class LitAutoEncoder(pl.LightningModule):
    def training_step(self, batch, batch_idx):
        ...

    def test_step(self, batch, batch_idx):
        # this is the test loop
        x, y = batch
        x = x.view(x.size(0), -1)
        z = self.encoder(x)
        x_hat = self.decoder(z)
        test_loss = F.mse_loss(x_hat, x)
        self.log("test_loss", test_loss)
```

##### Train with the test loop

Once the model has finished training, call **.test**

```python
from torch.utils.data import DataLoader

# initialize the Trainer
trainer = Trainer()

# test the model
trainer.test(model, dataloaders=DataLoader(test_set))
```

#### Add a validation loop

During training, it’s common practice to use a small portion of the train split to determine when the model has finished training.

##### Split the training data

As a rule of thumb, we use 20% of the training set as the **validation set**. This number varies from dataset to dataset.

```python
# use 20% of training data for validation
train_set_size = int(len(train_set) * 0.8)
valid_set_size = len(train_set) - train_set_size

# split the train set into two
seed = torch.Generator().manual_seed(42)
train_set, valid_set = data.random_split(train_set, [train_set_size, valid_set_size], generator=seed)
```

##### Define the validation loop

To add a validation loop, implement the **validation_step** method of the LightningModule

```python
class LitAutoEncoder(pl.LightningModule):
    def training_step(self, batch, batch_idx):
        ...

    def validation_step(self, batch, batch_idx):
        # this is the validation loop
        x, y = batch
        x = x.view(x.size(0), -1)
        z = self.encoder(x)
        x_hat = self.decoder(z)
        val_loss = F.mse_loss(x_hat, x)
        self.log("val_loss", val_loss)
```

##### Train with the validation loop

To run the validation loop, pass in the validation set to **.fit**

```python
from torch.utils.data import DataLoader

train_loader = DataLoader(train_set)
valid_loader = DataLoader(valid_set)

# train with both splits
trainer = Trainer()
trainer.fit(model, train_loader, valid_loader)
```

### Saving and loading checkpoints

#### What is a checkpoint?

When a model is training, the performance changes as it continues to see more data. It is a best practice to save the state of a model throughout the training process. This gives you a version of the model, *a checkpoint*, at each key point during the development of the model. Once training has completed, use the checkpoint that corresponds to the best performance you found during the training process.

Checkpoints also enable your training to resume from where it was in case the training process is interrupted.

PyTorch Lightning checkpoints are fully usable in plain PyTorch.

#### Contents of a checkpoint

A Lightning checkpoint contains a dump of the model’s entire internal state. Unlike plain PyTorch, Lightning saves *everything* you need to restore a model even in the most complex distributed training environments.

Inside a Lightning checkpoint you’ll find:

- 16-bit scaling factor (if using 16-bit precision training)
- Current epoch
- Global step
- LightningModule’s state_dict
- State of all optimizers
- State of all learning rate schedulers
- State of all callbacks (for stateful callbacks)
- State of datamodule (for stateful datamodules)
- The hyperparameters (init arguments) with which the model was created
- The hyperparameters (init arguments) with which the datamodule was created
- State of Loops

#### Save a checkpoint

Lightning automatically saves a checkpoint for you in your current working directory, with the state of your last training epoch. This makes sure you can resume training in case it was interrupted.

```python
# simply by using the Trainer you get automatic checkpointing
trainer = Trainer()
```

To change the checkpoint path use the `default_root_dir` argument:

```python
# saves checkpoints to 'some/path/' at every epoch end
trainer = Trainer(default_root_dir="some/path/")
```

#### LightningModule from checkpoint

To load a LightningModule along with its weights and hyperparameters use the following method:

```python
model = MyLightningModule.load_from_checkpoint("/path/to/checkpoint.ckpt")

# disable randomness, dropout, etc...
model.eval()

# predict with the model
y_hat = model(x)
```

##### Save hyperparameters

The LightningModule allows you to automatically save all the hyperparameters passed to *init* simply by calling *self.save_hyperparameters()*.

```python
class MyLightningModule(LightningModule):
    def __init__(self, learning_rate, another_parameter, *args, **kwargs):
        super().__init__()
        self.save_hyperparameters()
```

The hyperparameters are saved to the “hyper_parameters” key in the checkpoint

```python
checkpoint = torch.load(checkpoint, map_location=lambda storage, loc: storage)
print(checkpoint["hyper_parameters"])
# {"learning_rate": the_value, "another_parameter": the_other_value}
```

The LightningModule also has access to the Hyperparameters

```python
model = MyLightningModule.load_from_checkpoint("/path/to/checkpoint.ckpt")
print(model.learning_rate)
```

##### Initialize with other parameters

If you used the *self.save_hyperparameters()* method in the init of the LightningModule, you can initialize the model with different hyperparameters.

```python
# if you train and save the model like this it will use these values when loading
# the weights. But you can overwrite this
LitModel(in_dim=32, out_dim=10)

# uses in_dim=32, out_dim=10
model = LitModel.load_from_checkpoint(PATH)

# uses in_dim=128, out_dim=10
model = LitModel.load_from_checkpoint(PATH, in_dim=128, out_dim=10)
```

#### nn.Module from checkpoint

Lightning checkpoints are fully compatible with plain torch nn.Modules.

```python
checkpoint = torch.load(CKPT_PATH)
print(checkpoint.keys())
```

For example, let’s pretend we created a LightningModule like so:

```python
class Encoder(nn.Module):
    ...


class Decoder(nn.Module):
    ...


class Autoencoder(pl.LightningModule):
    def __init__(self, encoder, decoder, *args, **kwargs):
        ...


autoencoder = Autoencoder(Encoder(), Decoder())
```

Once the autoencoder has trained, pull out the relevant weights for your torch nn.Module:

```python
checkpoint = torch.load(CKPT_PATH)
encoder_weights = checkpoint["encoder"]
decoder_weights = checkpoint["decoder"]
```

#### Disable checkpointing

You can disable checkpointing by passing:

```python
trainer = Trainer(enable_checkpointing=False)
```

#### Resume training state

If you don’t just want to load weights, but instead restore the full training, do the following:

```python
model = LitModel()
trainer = Trainer()

# automatically restores model, epoch, step, LR schedulers, etc...
trainer.fit(model, ckpt_path="some/path/to/my_checkpoint.ckpt")
```

### Enable early stopping

#### Stopping an Epoch Early

You can stop and skip the rest of the current epoch early by overriding [`on_train_batch_start()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.ModelHooks.html#lightning.pytorch.core.hooks.ModelHooks.on_train_batch_start) to return `-1` when some condition is met.

If you do this repeatedly, for every epoch you had originally requested, then this will stop your entire training.

#### EarlyStopping Callback

The [`EarlyStopping`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.EarlyStopping.html#lightning.pytorch.callbacks.EarlyStopping) callback can be used to monitor a metric and stop the training when no improvement is observed.

To enable it:

- Import [`EarlyStopping`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.EarlyStopping.html#lightning.pytorch.callbacks.EarlyStopping) callback.
- Log the metric you want to monitor using `log()` method.
- Init the callback, and set `monitor` to the logged metric of your choice.
- Set the `mode` based on the metric needs to be monitored.
- Pass the [`EarlyStopping`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.EarlyStopping.html#lightning.pytorch.callbacks.EarlyStopping) callback to the [`Trainer`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer) callbacks flag.

```python
from lightning.pytorch.callbacks.early_stopping import EarlyStopping

class LitModel(LightningModule):
    def validation_step(self, batch, batch_idx):
        loss = ...
        self.log("val_loss", loss)


model = LitModel()
trainer = Trainer(callbacks=[EarlyStopping(monitor="val_loss", mode="min")])
trainer.fit(model)
```

You can customize the callbacks behaviour by changing its parameters.

```python
early_stop_callback = EarlyStopping(monitor="val_accuracy", min_delta=0.00, patience=3, verbose=False, mode="max")
trainer = Trainer(callbacks=[early_stop_callback])
```

Additional parameters that stop training at extreme points:

- `stopping_threshold`: Dừng ngay lập tức quá trình huấn luyện khi đạt đến ngưỡng này. Nó hữu ích khi chúng ta biết rằng vượt qua một giá trị tối ưu nhất định không mang lại lợi ích cho chúng ta nữa.
- `divergence_threshold`: Dừng quá trình huấn luyện ngay lập tức khi đạt đến giá trị xấu hơn ngưỡng này. Khi đạt đến một giá trị tệ hại như vậy, chúng ta tin rằng mô hình không thể phục hồi được nữa và tốt hơn là dừng sớm và chạy với điều kiện ban đầu khác.
- `check_finite`: Khi bật, dừng quá trình huấn luyện nếu chỉ số được giám sát trở thành NaN hoặc vô hạn.
- `check_on_train_epoch_end`: Khi bật, nó kiểm tra chỉ số vào cuối một epoch huấn luyện. Sử dụng tính năng này chỉ khi bạn đang giám sát bất kỳ chỉ số nào được lưu trữ trong các kết nối huấn luyện cụ thể trên mức epoch.

In case you need early stopping in a different part of training, subclass [`EarlyStopping`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.EarlyStopping.html#lightning.pytorch.callbacks.EarlyStopping) and change where it is called:

```python
class MyEarlyStopping(EarlyStopping):
    def on_validation_end(self, trainer, pl_module):
        # override this to disable early stopping at the end of val loop
        pass

    def on_train_end(self, trainer, pl_module):
        # instead, do it at the end of training loop
        self._run_early_stopping_check(trainer)
```

> Note: The [`EarlyStopping`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.EarlyStopping.html#lightning.pytorch.callbacks.EarlyStopping) callback runs at the end of every validation epoch by default. However, the frequency of validation can be modified by setting various parameters in the [`Trainer`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer), for example [`check_val_every_n_epoch`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.params.check_val_every_n_epoch) and [`val_check_interval`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.params.val_check_interval). It must be noted that the `patience` parameter counts the number of validation checks with no improvement, and not the number of training epochs. Therefore, with parameters `check_val_every_n_epoch=10` and `patience=3`, the trainer will perform at least 40 training epochs before being stopped

> Dịch Note: Theo mặc định, callback `EarlyStopping` được chạy vào cuối mỗi epoch validation. Tuy nhiên, tần suất của validation có thể được thay đổi bằng cách thiết lập các tham số khác nhau trong `Trainer`, ví dụ như `check_val_every_n_epoch` và `val_check_interval`. Chú ý rằng tham số `patience` đếm số lần kiểm tra validation mà không có cải thiện, và không phải là số epoch huấn luyện. Do đó, với các tham số `check_val_every_n_epoch=10` và `patience=3`, Trainer sẽ thực hiện ít nhất 40 epoch huấn luyện trước khi bị dừng.



## Level 3: Use pretrained models

### Use any PyTorch nn.Module

Any model that is a PyTorch nn.Module can be used with Lightning (because LightningModules are nn.Modules also).

### Use a pretrained LightningModule

Let’s use the AutoEncoder as a feature extractor in a separate model.

```python
class Encoder(torch.nn.Module):
    ...


class AutoEncoder(LightningModule):
    def __init__(self):
        self.encoder = Encoder()
        self.decoder = Decoder()


class CIFAR10Classifier(LightningModule):
    def __init__(self):
        # init the pretrained LightningModule
        self.feature_extractor = AutoEncoder.load_from_checkpoint(PATH)
        self.feature_extractor.freeze()

        # the autoencoder outputs a 100-dim representation and CIFAR-10 has 10 classes
        self.classifier = nn.Linear(100, 10)

    def forward(self, x):
        representations = self.feature_extractor(x)
        x = self.classifier(representations)
        ...
```

We used our pretrained Autoencoder (a LightningModule) for transfer learning!

### Example: Imagenet (Computer Vision)

```python
import torchvision.models as models


class ImagenetTransferLearning(LightningModule):
    def __init__(self):
        super().__init__()

        # init a pretrained resnet
        backbone = models.resnet50(weights="DEFAULT")
        num_filters = backbone.fc.in_features
        layers = list(backbone.children())[:-1]
        self.feature_extractor = nn.Sequential(*layers)

        # use the pretrained model to classify cifar-10 (10 image classes)
        num_target_classes = 10
        self.classifier = nn.Linear(num_filters, num_target_classes)

    def forward(self, x):
        self.feature_extractor.eval()
        with torch.no_grad():
            representations = self.feature_extractor(x).flatten(1)
        x = self.classifier(representations)
        ...
```

Fine turning

```python
model = ImagenetTransferLearning()
trainer = Trainer()
trainer.fit(model)
```

And use it to predict your data of interest

```python
model = ImagenetTransferLearning.load_from_checkpoint(PATH)
model.freeze()

x = some_images_from_cifar10()
predictions = model(x)
```

We used a pretrained model on imagenet, finetuned on CIFAR-10 to predict on CIFAR-10. In the non-academic world we would finetune on a tiny dataset you have and predict on your dataset.

### Example: BERT (NLP)

Lightning is completely agnostic to what’s used for transfer learning so long as it is a torch.nn.Module subclass.

Here’s a model that uses [Huggingface transformers](https://github.com/huggingface/transformers).

```python
class BertMNLIFinetuner(LightningModule):
    def __init__(self):
        super().__init__()

        self.bert = BertModel.from_pretrained("bert-base-cased", output_attentions=True)
        self.W = nn.Linear(bert.config.hidden_size, 3)
        self.num_classes = 3

    def forward(self, input_ids, attention_mask, token_type_ids):
        h, _, attn = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)

        h_cls = h[:, 0]
        logits = self.W(h_cls)
        return logits, attn
```



## Level 4: Enable script parameters

You can use any CLI tool you want with Lightning. For beginners, we recommand using Python’s built-in argument parser.

### ArgumentParser

The [`ArgumentParser`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser) is a built-in feature in Python that let’s you build CLI programs. You can use it to make hyperparameters and other training settings available from the command line:

```python
from argparse import ArgumentParser

parser = ArgumentParser()

# Trainer arguments
parser.add_argument("--devices", type=int, default=2)

# Hyperparameters for the model
parser.add_argument("--layer_1_dim", type=int, default=128)

# Parse the user inputs and defaults (returns a argparse.Namespace)
args = parser.parse_args()

# Use the parsed arguments in your program
trainer = Trainer(devices=args.devices)
model = MyModel(layer_1_dim=args.layer_1_dim)
```

This allows you to call your program like so:

```python
python trainer.py --layer_1_dim 64 --devices 1
```

### LightningCLI

Python’s argument parser works well for simple use cases, but it can become cumbersome to maintain for larger projects. For example, every time you add, change, or delete an argument from your model, you will have to add, edit, or remove the corresponding `parser.add_argument` code. The [Lightning CLI](https://lightning.ai/docs/pytorch/stable/cli/lightning_cli.html) provides a seamless integration with the Trainer and LightningModule for which the CLI arguments get generated automatically for you!

## Level 5: Understand and visualize your model

### Debug your model

##### How does Lightning help me debug ?

The Lightning Trainer has *a lot* of arguments devoted to maximizing your debugging productivity.

##### Set a breakpoint

A breakpoint stops your code execution so you can inspect variables, etc… and allow your code to execute one line at a time.

```python
def function_to_debug():
    x = 2

    # set breakpoint
    import pdb

    pdb.set_trace()
    y = x**2
```

In this example, the code will stop before executing the `y = x**2` line.

##### Run all your model code once quickly

If you’ve ever trained a model for days only to crash during validation or testing then this trainer argument is about to become your best friend.

The [`fast_dev_run`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.params.fast_dev_run) argument in the trainer runs 5 batch of training, validation, test and prediction data through your trainer to see if there are any bugs:

```python
Trainer(fast_dev_run=True)
```

To change how many batches to use, change the argument to an integer. Here we run 7 batches of each:

```python
Trainer(fast_dev_run=7)
```

> Note: This argument will disable tuner, checkpoint callbacks, early stopping callbacks, loggers and logger callbacks like [`LearningRateMonitor`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.LearningRateMonitor.html#lightning.pytorch.callbacks.LearningRateMonitor) and [`DeviceStatsMonitor`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.DeviceStatsMonitor.html#lightning.pytorch.callbacks.DeviceStatsMonitor).

##### Shorten the epoch length

Sometimes it’s helpful to only use a fraction of your training, val, test, or predict data (or a set number of batches). For example, you can use 20% of the training set and 1% of the validation set.

On larger datasets like Imagenet, this can help you debug or test a few things faster than waiting for a full epoch.

```python
# use only 10% of training data and 1% of val data
trainer = Trainer(limit_train_batches=0.1, limit_val_batches=0.01)

# use 10 batches of train and 5 batches of val
trainer = Trainer(limit_train_batches=10, limit_val_batches=5)

```

##### Run a Sanity Check

Lightning runs **2** steps of validation in the beginning of training. This avoids crashing in the validation loop sometime deep into a lengthy training loop.

(See: [`num_sanity_val_steps`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.params.num_sanity_val_steps) argument of [`Trainer`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer))

```python
trainer = Trainer(num_sanity_val_steps=2)
```

##### Print LightningModule weights summary

Whenever the `.fit()` function gets called, the Trainer will print the weights summary for the LightningModule.

```python
trainer.fit(...)
```

this generate a table like:

```bash
  | Name  | Type        | Params
----------------------------------
0 | net   | Sequential  | 132 K
1 | net.0 | Linear      | 131 K
2 | net.1 | BatchNorm1d | 1.0 K
```

To add the child modules to the summary add a [`ModelSummary`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelSummary.html#lightning.pytorch.callbacks.ModelSummary):

```python
from lightning.pytorch.callbacks import ModelSummary

trainer = Trainer(callbacks=[ModelSummary(max_depth=-1)])
```

To print the model summary if `.fit()` is not called:

```python
from lightning.pytorch.utilities.model_summary import ModelSummary

model = LitModel()
summary = ModelSummary(model, max_depth=-1)
print(summary)
```

To turn off the autosummary use:

```python
Trainer(enable_model_summary=False)
```

##### Print input output layer dimensions

Another debugging tool is to display the intermediate input- and output sizes of all your layers by setting the `example_input_array` attribute in your LightningModule.

```python
class LitModel(LightningModule):
    def __init__(self, *args, **kwargs):
        self.example_input_array = torch.Tensor(32, 1, 28, 28)
```

With the input array, the summary table will include the input and output layer dimensions:

```bash
  | Name  | Type        | Params | In sizes  | Out sizes
--------------------------------------------------------------
0 | net   | Sequential  | 132 K  | [10, 256] | [10, 512]
1 | net.0 | Linear      | 131 K  | [10, 256] | [10, 512]
2 | net.1 | BatchNorm1d | 1.0 K  | [10, 512] | [10, 512]
```

when you call `.fit()` on the Trainer. This can help you find bugs in the composition of your layers.

### Find bottlenecks in training

#### Why do I need profiling?

Profiling (Lập hồ sơ) helps you find bottlenecks in your code by capturing analytics such as how long a function takes or how much memory is used.

#### Find training loop bottlenecks

The most basic profile measures all the key methods across **Callbacks**, **DataModules** and the **LightningModule** in the training loop.

```python
trainer = Trainer(profiler="simple")
```

Once the **.fit()** function has completed, you’ll see an output like this:

```bash
FIT Profiler Report

-----------------------------------------------------------------------------------------------
|  Action                                          |  Mean duration (s)     |  Total time (s) |
-----------------------------------------------------------------------------------------------
|  [LightningModule]BoringModel.prepare_data       |  10.0001               |  20.00          |
|  run_training_epoch                              |  6.1558                |  6.1558         |
|  run_training_batch                              |  0.0022506             |  0.015754       |
|  [LightningModule]BoringModel.optimizer_step     |  0.0017477             |  0.012234       |
|  [LightningModule]BoringModel.val_dataloader     |  0.00024388            |  0.00024388     |
|  on_train_batch_start                            |  0.00014637            |  0.0010246      |
|  [LightningModule]BoringModel.teardown           |  2.15e-06              |  2.15e-06       |
|  [LightningModule]BoringModel.on_train_start     |  1.644e-06             |  1.644e-06      |
|  [LightningModule]BoringModel.on_train_end       |  1.516e-06             |  1.516e-06      |
|  [LightningModule]BoringModel.on_fit_end         |  1.426e-06             |  1.426e-06      |
|  [LightningModule]BoringModel.setup              |  1.403e-06             |  1.403e-06      |
|  [LightningModule]BoringModel.on_fit_start       |  1.226e-06             |  1.226e-06      |
-----------------------------------------------------------------------------------------------
```

In this report we can see that the slowest function is **prepare_data**. Now you can figure out why data preparation is slowing down your training.

The simple profiler measures all the standard methods used in the training loop automatically, including:

- on_train_epoch_start
- on_train_epoch_end
- on_train_batch_start
- model_backward
- on_after_backward
- optimizer_step
- on_train_batch_end
- on_training_end
- etc…

#### Profile the time within every function

To profile the time within every function, use the [`AdvancedProfiler`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.profilers.AdvancedProfiler.html#lightning.pytorch.profilers.AdvancedProfiler) built on top of Python’s [cProfiler](https://docs.python.org/3/library/profile.html#module-cProfile).

```python
trainer = Trainer(profiler="advanced")
```

Once the **.fit()** function has completed, you’ll see an output like this:

```bash
Profiler Report

Profile stats for: get_train_batch
        4869394 function calls (4863767 primitive calls) in 18.893 seconds
Ordered by: cumulative time
List reduced from 76 to 10 due to restriction <10>
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
3752/1876    0.011    0.000   18.887    0.010 {built-in method builtins.next}
    1876     0.008    0.000   18.877    0.010 dataloader.py:344(__next__)
    1876     0.074    0.000   18.869    0.010 dataloader.py:383(_next_data)
    1875     0.012    0.000   18.721    0.010 fetch.py:42(fetch)
    1875     0.084    0.000   18.290    0.010 fetch.py:44(<listcomp>)
    60000    1.759    0.000   18.206    0.000 mnist.py:80(__getitem__)
    60000    0.267    0.000   13.022    0.000 transforms.py:68(__call__)
    60000    0.182    0.000    7.020    0.000 transforms.py:93(__call__)
    60000    1.651    0.000    6.839    0.000 functional.py:42(to_tensor)
    60000    0.260    0.000    5.734    0.000 transforms.py:167(__call__)
```

If the profiler report becomes too long, you can stream the report to a file:

```python
from lightning.pytorch.profilers import AdvancedProfiler

profiler = AdvancedProfiler(dirpath=".", filename="perf_logs")
trainer = Trainer(profiler=profiler)
```

#### Measure accelerator usage

Another helpful technique to detect bottlenecks is to ensure that you’re using the full capacity of your accelerator (GPU/TPU/IPU/HPU). This can be measured with the [`DeviceStatsMonitor`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.DeviceStatsMonitor.html#lightning.pytorch.callbacks.DeviceStatsMonitor):

```python
from lightning.pytorch.callbacks import DeviceStatsMonitor

trainer = Trainer(callbacks=[DeviceStatsMonitor()])
```

CPU metrics will be tracked by default on the CPU accelerator. To enable it for other accelerators set `DeviceStatsMonitor(cpu_stats=True)`. To disable logging CPU metrics, you can specify `DeviceStatsMonitor(cpu_stats=False)`.

### Visualize metrics, image and text

Learn how to track and visualize metrics, images and text.

#### Why do I need to track metrics?

In model development, we track values of interest such as the *validation_loss* to visualize the learning process for our models. Model development is like driving a car without windows, charts and logs provide the *windows* to know where to drive the car.

With Lightning, you can visualize virtually anything you can think of: numbers, text, images, audio. Your creativity and imagination are the only limiting factor.

#### Track metrics

Metric visualization is the most basic but powerful way of understanding how your model is doing throughout the model development process.

To track a metric, simply use the *self.log* method available inside the *LightningModule*

```python
class LitModel(pl.LightningModule):
    def training_step(self, batch, batch_idx):
        value = ...
        self.log("some_value", value)
```

To log multiple metrics at once, use *self.log_dict*

```python
values = {"loss": loss, "acc": acc, "metric_n": metric_n}  # add more items if needed
self.log_dict(values)
```

TODO: show plot of metric changing over time'

##### View in the commandline

To view metrics in the commandline progress bar, set the *prog_bar* argument to True.

```python
self.log(..., prog_bar=True)
```

##### View in the browser

To view metrics in the browser you need to use an *experiment manager* with these capabilities.

By Default, Lightning uses Tensorboard (if available) and a simple CSV logger otherwise.

```python
# every trainer already has tensorboard enabled by default (if the dependency is available)
trainer = Trainer()
```

To launch the tensorboard dashboard run the following command on the commandline.

```python
tensorboard --logdir=lightning_logs/
```

If you’re using a notebook environment such as *colab* or *kaggle* or *jupyter*, launch Tensorboard with this command

```python
%reload_ext tensorboard
%tensorboard --logdir=lightning_logs/
```

##### Accumulate a metric

When *self.log* is called inside the *training_step*, it generates a timeseries showing how the metric behaves over time.

However, For the validation and test sets we are not generally interested in plotting the metric values per batch of data. Instead, we want to compute a summary statistic (such as average, min or max) across the full split of data.

When you call self.log inside the *validation_step* and *test_step*, Lightning automatically accumulates the metric and averages it once it’s gone through the whole split (*epoch*).

```python
def validation_step(self, batch, batch_idx):
    value = batch_idx + 1
    self.log("average_value", value)
```

If you don’t want to average you can also choose from `{min,max,sum}` by passing the *reduce_fx* argument.

```python
# default function
self.log(..., reduce_fx="mean")
```

For other reductions, we recommend logging a [`torchmetrics.Metric`](https://torchmetrics.readthedocs.io/en/stable/pages/implement.html#torchmetrics.Metric) instance instead.

#### Configure the saving directory

By default, anything that is logged is saved to the current working directory. To use a different directory, set the *default_root_dir* argument in the Trainer.

```python
Trainer(default_root_dir="/your/custom/path")
```

## Level 6: Predict your model

### Predict with LightningModule

#### Load a checkpoint and predict

The easiest way to use a model for predictions is to load the weights using **load_from_checkpoint** found in the LightningModule.

```python
model = LitModel.load_from_checkpoint("best_model.ckpt")
model.eval()
x = torch.randn(1, 64)
with torch.no_grad():
    y_hat = model(x)
```

#### Predict step with your LightningModule

Loading a checkpoint and predicting still leaves you with a lot of boilerplate (= template) around the predict epoch. The **predict step** in the LightningModule removes this boilerplate.

```python
class MyModel(LightningModule):
    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        return self(batch)
```

And pass in any dataloader to the Lightning Trainer:

```python
data_loader = DataLoader(...)
model = MyModel()
trainer = Trainer()
predictions = trainer.predict(model, data_loader)
```

#### Enable complicated predict logic

When you need to add complicated pre-processing or post-processing logic to your data use the predict step. For example here we do [Monte Carlo Dropout](https://arxiv.org/pdf/1506.02142.pdf) for predictions:

```python
class LitMCdropoutModel(pl.LightningModule):
    def __init__(self, model, mc_iteration):
        super().__init__()
        self.model = model
        self.dropout = nn.Dropout()
        self.mc_iteration = mc_iteration

    def predict_step(self, batch, batch_idx):
        # enable Monte Carlo Dropout
        self.dropout.train()

        # take average of `self.mc_iteration` iterations
        pred = [self.dropout(self.model(x)).unsqueeze(0) for _ in range(self.mc_iteration)]
        pred = torch.vstack(pred).mean(dim=0)
        return pred
```

#### Enable distributed inference

By using the predict step in Lightning you get free distributed inference using [`BasePredictionWriter`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.BasePredictionWriter.html#lightning.pytorch.callbacks.BasePredictionWriter).

```python
import torch
from lightning.pytorch.callbacks import BasePredictionWriter


class CustomWriter(BasePredictionWriter):
    def __init__(self, output_dir, write_interval):
        super().__init__(write_interval)
        self.output_dir = output_dir

    def write_on_epoch_end(self, trainer, pl_module, predictions, batch_indices):
        # this will create N (num processes) files in `output_dir` each containing
        # the predictions of it's respective rank
        torch.save(predictions, os.path.join(self.output_dir, f"predictions_{trainer.global_rank}.pt"))

        # optionally, you can also save `batch_indices` to get the information about the data index
        # from your prediction data
        torch.save(batch_indices, os.path.join(self.output_dir, f"batch_indices_{trainer.global_rank}.pt"))


# or you can set `writer_interval="batch"` and override `write_on_batch_end` to save
# predictions at batch level
pred_writer = CustomWriter(output_dir="pred_path", write_interval="epoch")
trainer = Trainer(accelerator="gpu", strategy="ddp", devices=8, callbacks=[pred_writer])
model = BoringModel()
trainer.predict(model, return_predictions=False)
```



### Predict with pure Pytorch

#### Use PyTorch as normal

If you prefer to use PyTorch directly, feel free to use any Lightning checkpoint without Lightning.

```python
import torch


class MyModel(nn.Module):
    ...


model = MyModel()
checkpoint = torch.load("path/to/lightning/checkpoint.ckpt")
model.load_state_dict(checkpoint["state_dict"])
model.eval()
```

#### Extract nn.Module from Lightning checkpoints

You can also load the saved checkpoint and use it as a regular [`torch.nn.Module`](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module). You can extract all your [`torch.nn.Module`](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module) and load the weights using the checkpoint saved using LightningModule after training. For this, we recommend copying the exact implementation from your LightningModule `init` and `forward` method.

```python
class Encoder(nn.Module):
    ...


class Decoder(nn.Module):
    ...


class AutoEncoderProd(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = Encoder()
        self.decoder = Decoder()

    def forward(self, x):
        return self.encoder(x)


class AutoEncoderSystem(LightningModule):
    def __init__(self):
        super().__init__()
        self.auto_encoder = AutoEncoderProd()

    def forward(self, x):
        return self.auto_encoder.encoder(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.auto_encoder.encoder(x)
        y_hat = self.auto_encoder.decoder(y_hat)
        loss = ...
        return loss


# train it
trainer = Trainer(devices=2, accelerator="gpu", strategy="ddp")
model = AutoEncoderSystem()
trainer.fit(model, train_dataloader, val_dataloader)
trainer.save_checkpoint("best_model.ckpt")


# create the PyTorch model and load the checkpoint weights
model = AutoEncoderProd()
checkpoint = torch.load("best_model.ckpt")
hyper_parameters = checkpoint["hyper_parameters"]

# if you want to restore any hyperparameters, you can pass them too
model = AutoEncoderProd(**hyper_parameters)

model_weights = checkpoint["state_dict"]

# update keys by dropping `auto_encoder.`
for key in list(model_weights):
    model_weights[key.replace("auto_encoder.", "")] = model_weights.pop(key)

model.load_state_dict(model_weights)
model.eval()
x = torch.randn(1, 64)

with torch.no_grad():
    y_hat = model(x)
```