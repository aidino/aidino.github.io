---
layout: libdoc/page
title: Basic Skills
permalink: /pytorch-lightning/lv1-intermediate-skills/
category: Pytorch lightning
description: "Intermadiate Skills"
order: 3
---
{:toc}
- *source: https://lightning.ai/* 
<br>


## Level 7: Interactive cloud developments

### Prepare your code

To train on CPU/GPU/TPU without changing your code, we need to build a few good habits :)

#### Delete .cuda() or .to() calls

Delete any calls to .cuda() or .to(device).

```python
# before lightning
def forward(self, x):
    x = x.cuda(0)
    layer_1.cuda(0)
    x_hat = layer_1(x)

# after lightning
def forward(self, x):
    x_hat = layer_1(x)
```

#### Init tensors using Tensor.to and register_buffer

When you need to create a new tensor, use `Tensor.to`.

Điều này sẽ làm cho mã của bạn mở rộng theo bất kỳ số lượng GPU hoặc TPU tùy ý nào với Lightning.

```python
# before lightning
def forward(self, x):
    z = torch.Tensor(2, 3)
    z = z.cuda(0)

# with lightning
def forward(self, x):
    z = torch.Tensor(2, 3)
    z = z.to(x)
```

`LightningModule` biết được thiết bị nào nó đang chạy trên. Bạn có thể truy cập tham chiếu thông qua `self.device`. Đôi khi cần phải lưu trữ các tensors như thuộc tính của module. Tuy nhiên, nếu chúng không phải là các tham số, chúng sẽ vẫn được lưu trữ trên CPU ngay cả khi module được chuyển đến một thiết bị mới. Để ngăn chặn điều đó và giữ cho module không phụ thuộc vào thiết bị, hãy đăng ký tensor như một buffer trong phương thức `__init__` của các module của bạn bằng cách sử dụng `register_buffer()`.

```python
class LitModel(LightningModule):
    def __init__(self):
        ...
        self.register_buffer("sigma", torch.eye(3))
        # you can now access self.sigma anywhere in your module
```

#### Remove samplers

[`DistributedSampler`](https://pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler) is automatically handled by Lightning.

See [use_distributed_sampler](https://lightning.ai/docs/pytorch/stable/common/trainer.html#replace-sampler-ddp) for more information.

#### Synchronize validation and test logging

Đồng bộ hóa logging cho bước validation và test Khi chạy ở chế độ phân tán, 

Chúng ta phải đảm bảo rằng các loggings call cho bước validation and test được đồng bộ hóa trên tất cả các quá trình. Điều này được thực hiện bằng cách thêm `sync_dist=True` vào tất cả các `self.log` calls trong bước validation and test. Điều này đảm bảo rằng mỗi worker GPU có cùng hành vi khi theo dõi các điểm kiểm tra mô hình, điều này rất quan trọng cho các tác vụ hậu xử lý sau này, chẳng hạn như testing the best checkpoint across all workersr. Tùy chọn `sync_dist` cũng có thể được sử dụng trong các logging call trong các step methods, nhưng hãy lưu ý rằng điều này có thể dẫn đến chi phí giao tiếp đáng kể và làm chậm quá trình huấn luyện của bạn.

Lưu ý nếu bạn sử dụng bất kỳ chỉ số tích hợp nào hoặc chỉ số tùy chỉnh sử dụng `TorchMetrics`, chúng không cần được cập nhật và được tự động xử lý cho bạn.

```python
def validation_step(self, batch, batch_idx):
    x, y = batch
    logits = self(x)
    loss = self.loss(logits, y)
    # Add sync_dist=True to sync logging across all GPU workers (may have performance impact)
    self.log("validation_loss", loss, on_step=True, on_epoch=True, sync_dist=True)


def test_step(self, batch, batch_idx):
    x, y = batch
    logits = self(x)
    loss = self.loss(logits, y)
    # Add sync_dist=True to sync logging across all GPU workers (may have performance impact)
    self.log("test_loss", loss, on_step=True, on_epoch=True, sync_dist=True)
```

Có thể thực hiện một số tính toán theo cách thủ công và ghi lại kết quả giảm trên hạng 0 như sau:

```python
def __init__(self):
    super().__init__()
    self.outputs = []


def test_step(self, batch, batch_idx):
    x, y = batch
    tensors = self(x)
    self.outputs.append(tensors)
    return tensors


def on_test_epoch_end(self):
    mean = torch.mean(self.all_gather(self.outputs))
    self.outputs.clear()  # free memory

    # When logging only on rank 0, don't forget to add
    # `rank_zero_only=True` to avoid deadlocks on synchronization.
    # caveat: monitoring this is unimplemented. see https://github.com/Lightning-AI/lightning/issues/15852
    if self.trainer.is_global_zero:
        self.log("my_reduced_metric", mean, rank_zero_only=True)
```

#### Make models pickleable

It’s very likely your code is already [pickleable](https://docs.python.org/3/library/pickle.html), in that case no change in necessary. However, if you run a distributed model and get the following error:

```bash
self._launch(process_obj)
File "/net/software/local/python/3.6.5/lib/python3.6/multiprocessing/popen_spawn_posix.py", line 47,
in _launch reduction.dump(process_obj, fp)
File "/net/software/local/python/3.6.5/lib/python3.6/multiprocessing/reduction.py", line 60, in dump
ForkingPickler(file, protocol).dump(obj)
_pickle.PicklingError: Can't pickle <function <lambda> at 0x2b599e088ae8>:
attribute lookup <lambda> on __main__ failed
```

This means something in your model definition, transforms, optimizer, dataloader or callbacks cannot be pickled, and the following code will fail:

```python
import pickle

pickle.dump(some_object)
```

This is a limitation of using multiple processes for distributed training within PyTorch. To fix this issue, find your piece of code that cannot be pickled. The end of the stacktrace is usually helpful. ie: in the stacktrace example here, there seems to be a lambda function somewhere in the code which cannot be pickled.

```bash
self._launch(process_obj)
File "/net/software/local/python/3.6.5/lib/python3.6/multiprocessing/popen_spawn_posix.py", line 47,
in _launch reduction.dump(process_obj, fp)
File "/net/software/local/python/3.6.5/lib/python3.6/multiprocessing/reduction.py", line 60, in dump
ForkingPickler(file, protocol).dump(obj)
_pickle.PicklingError: Can't pickle [THIS IS THE THING TO FIND AND DELETE]:
attribute lookup <lambda> on __main__ failed
```

### GPU Training

#### What is a GPU?

A Graphics Processing Unit (GPU), is a specialized hardware accelerator designed to speed up mathematical computations used in gaming and deep learning.

#### Train on GPUs

The Trainer will run on all available GPUs by default. Make sure you’re running on a machine with at least one GPU. There’s no need to specify any NVIDIA flags as Lightning will do it for you.

```python
# run on as many GPUs as available by default
trainer = Trainer(accelerator="auto", devices="auto", strategy="auto")
# equivalent to
trainer = Trainer()

# run on one GPU
trainer = Trainer(accelerator="gpu", devices=1)
# run on multiple GPUs
trainer = Trainer(accelerator="gpu", devices=8)
# choose the number of devices automatically
trainer = Trainer(accelerator="gpu", devices="auto")
```



> Note: Setting `accelerator="gpu"` will also automatically choose the “mps” device on Apple sillicon GPUs. If you want to avoid this, you can set `accelerator="cuda"` instead.

##### Choosing GPU devices

You can select the GPU devices using ranges, a list of indices or a string containing a comma separated list of GPU ids:

```python
# DEFAULT (int) specifies how many GPUs to use per node
Trainer(accelerator="gpu", devices=k)

# Above is equivalent to
Trainer(accelerator="gpu", devices=list(range(k)))

# Specify which GPUs to use (don't use when running on cluster)
Trainer(accelerator="gpu", devices=[0, 1])

# Equivalent using a string
Trainer(accelerator="gpu", devices="0, 1")

# To use all available GPUs put -1 or '-1'
# equivalent to `list(range(torch.cuda.device_count())) and `"auto"`
Trainer(accelerator="gpu", devices=-1)
```

The table below lists examples of possible input formats and how they are interpreted by Lightning.

| devices | Type | Parsed       | Meaning                     |
| ------- | ---- | ------------ | --------------------------- |
| 3       | int  | [0, 1, 2]    | first 3 GPUs                |
| -1      | int  | [0, 1, 2, …] | all available GPUs          |
| [0]     | list | [0]          | GPU 0                       |
| [1, 3]  | list | [1, 3]       | GPU index 1 and 3 (0-based) |
| “3”     | str  | [0, 1, 2]    | first 3 GPUs                |
| “1, 3”  | str  | [1, 3]       | GPU index 1 and 3 (0-based) |
| “-1”    | str  | [0, 1, 2, …] | all available GPUs          |

##### Find usable CUDA devices

If you want to run several experiments at the same time on your machine, for example for a hyperparameter sweep, then you can use the following utility function to pick GPU indices that are “accessible”, without having to change your code every time.

```python
from lightning.pytorch.accelerators import find_usable_cuda_devices

# Find two GPUs on the system that are not already occupied
trainer = Trainer(accelerator="cuda", devices=find_usable_cuda_devices(2))

from lightning.fabric.accelerators import find_usable_cuda_devices

# Works with Fabric too
fabric = Fabric(accelerator="cuda", devices=find_usable_cuda_devices(2))
```



This is especially useful when GPUs are configured to be in “exclusive compute mode”, such that only one process at a time is allowed access to the device. This special mode is often enabled on server GPUs or systems shared among multiple users.



### TPU Training

Lightning supports running on TPUs. At this moment, TPUs are available on Google Cloud (GCP), Google Colab and Kaggle Environments. For more information on TPUs [watch this video](https://www.youtube.com/watch?v=kPMpmcl_Pyw).

#### What is a TPU?

Tensor Processing Unit (TPU) is an AI accelerator application-specific integrated circuit (ASIC) developed by Google specifically for neural networks.

A TPU has 8 cores where each core is optimized for 128x128 matrix multiplies. In general, a single TPU is about as fast as 5 V100 GPUs!

A TPU pod hosts many TPUs on it. Currently, TPU v3 Pod has up to 2048 TPU cores and 32 TiB of memory! You can request a full pod from Google cloud or a “slice” which gives you some subset of those 2048 cores.

#### Run on TPU cores

To run on different cores, modify the `devices` argument.

```python
# run on as many TPUs as available by default
trainer = Trainer(accelerator="auto", devices="auto", strategy="auto")
# equivalent to
trainer = Trainer()

# run on one TPU core
trainer = Trainer(accelerator="tpu", devices=1)
# run on multiple TPU cores
trainer = Trainer(accelerator="tpu", devices=8)
# run on the 5th core
trainer = Trainer(accelerator="tpu", devices=[5])
# choose the number of cores automatically
trainer = Trainer(accelerator="tpu", devices="auto")
```

#### How to access TPUs

To access TPUs, there are three main ways.

##### Google Colab

Colab is like a jupyter notebook with a free GPU or TPU hosted on GCP.

To get a TPU on colab, follow these steps:

1. Go to [Google Colab](https://colab.research.google.com/).

2. Click “new notebook” (bottom right of pop-up).

3. Click runtime > change runtime settings. Select Python 3, and hardware accelerator “TPU”. This will give you a TPU with 8 cores.

4. Next, insert this code into the first cell and execute. This will install the xla library that interfaces between PyTorch and the TPU.

    ```bash
    !pip install cloud-tpu-client https://storage.googleapis.com/tpu-pytorch/wheels/torch_xla-1.13-cp38-cp38m-linux_x86_64.whl
    ```

5. Once the above is done, install PyTorch Lightning.

    ```
    !pip install lightning
    ```

6. Then set up your LightningModule as normal.

##### Google Cloud (GCP)

You could refer to this [page](https://cloud.google.com/tpu/docs/setup-gcp-account) for getting started with Cloud TPU resources on GCP.

##### Kaggle

For starting Kaggle projects with TPUs, refer to this [kernel](https://www.kaggle.com/pytorchlightning/pytorch-on-tpu-with-pytorch-lightning).

#### Optimize Performance

The TPU was designed for specific workloads and operations to carry out large volumes of matrix multiplication, convolution operations and other commonly used ops in applied deep learning. The specialization makes it a strong choice for NLP tasks, sequential convolutional networks, and under low precision operation. There are cases in which training on TPUs is slower when compared with GPUs, for possible reasons listed:

- Too small batch size.
- Explicit evaluation of tensors during training, e.g. `tensor.item()`
- Tensor shapes (e.g. model inputs) change often during training.
- Limited resources when using TPU’s with PyTorch [Link](https://github.com/pytorch/xla/issues/2054#issuecomment-627367729)
- XLA Graph compilation during the initial steps [Reference](https://github.com/pytorch/xla/issues/2383#issuecomment-666519998)
- Some tensor ops are not fully supported on TPU, or not supported at all. These operations will be performed on CPU (context switch).

The official PyTorch XLA [performance guide](https://github.com/pytorch/xla/blob/master/TROUBLESHOOTING.md#known-performance-caveats) has more detailed information on how PyTorch code can be optimized for TPU. In particular, the [metrics report](https://github.com/pytorch/xla/blob/master/TROUBLESHOOTING.md#get-a-metrics-report) allows one to identify operations that lead to context switching.

## Level 9: Modularize your projects

### Modularize your datasets

A datamodule is a shareable, reusable class that encapsulates all the steps needed to process data

A datamodule encapsulates the five steps involved in data processing in PyTorch:

1. Download / tokenize / process.
2. Clean and (maybe) save to disk.
3. Load inside [`Dataset`](https://pytorch.org/docs/stable/data.html#torch.utils.data.Dataset).
4. Apply transforms (rotate, tokenize, etc…).
5. Wrap inside a [`DataLoader`](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader).

#### Why do I need a DataModule?

In normal PyTorch code, the data cleaning/preparation is usually scattered across many files. This makes sharing and reusing the exact splits and transforms across projects impossible.

Datamodules are for you if you ever asked the questions:

- what splits did you use?
- what transforms did you use?
- what normalization did you use?
- how did you prepare/tokenize the data?

#### What is a DataModule?

The [`LightningDataModule`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningDataModule.html#lightning.pytorch.core.LightningDataModule) is a convenient way to manage data in PyTorch Lightning. It encapsulates training, validation, testing, and prediction dataloaders, as well as any necessary steps for data processing, downloads, and transformations. By using a [`LightningDataModule`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningDataModule.html#lightning.pytorch.core.LightningDataModule), you can easily develop dataset-agnostic models, hot-swap different datasets, and share data splits and transformations across projects.

Here’s a simple PyTorch example:

```python
# regular PyTorch
test_data = MNIST(my_path, train=False, download=True)
predict_data = MNIST(my_path, train=False, download=True)
train_data = MNIST(my_path, train=True, download=True)
train_data, val_data = random_split(train_data, [55000, 5000])

train_loader = DataLoader(train_data, batch_size=32)
val_loader = DataLoader(val_data, batch_size=32)
test_loader = DataLoader(test_data, batch_size=32)
predict_loader = DataLoader(predict_data, batch_size=32)
```

The equivalent (tương đương) `DataModule` just organizes the same exact code, but makes it reusable across projects.

```python
class MNISTDataModule(pl.LightningDataModule):
    def __init__(self, data_dir: str = "path/to/dir", batch_size: int = 32):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size

    def setup(self, stage: str):
        self.mnist_test = MNIST(self.data_dir, train=False)
        self.mnist_predict = MNIST(self.data_dir, train=False)
        mnist_full = MNIST(self.data_dir, train=True)
        self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=self.batch_size)

    def predict_dataloader(self):
        return DataLoader(self.mnist_predict, batch_size=self.batch_size)

    def teardown(self, stage: str):
        # Used to clean-up when the run is finished
        ...
```

But now, as the complexity of your processing grows (transforms, multiple-GPU training), you can let Lightning handle those details for you while making this dataset reusable so you can share with colleagues or use in different projects.

```python
mnist = MNISTDataModule(my_path)
model = LitClassifier()

trainer = Trainer()
trainer.fit(model, mnist)
```



Đây là một thực tế hơn, complex DataModule that shows how much more reusable the datamodule is.

```python
import lightning.pytorch as pl
from torch.utils.data import random_split, DataLoader

# Note - you must have torchvision installed for this example
from torchvision.datasets import MNIST
from torchvision import transforms


class MNISTDataModule(pl.LightningDataModule):
    def __init__(self, data_dir: str = "./"):
        super().__init__()
        self.data_dir = data_dir
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    def prepare_data(self):
        # download
        MNIST(self.data_dir, train=True, download=True)
        MNIST(self.data_dir, train=False, download=True)

    def setup(self, stage: str):
        # Assign train/val datasets for use in dataloaders
        if stage == "fit":
            mnist_full = MNIST(self.data_dir, train=True, transform=self.transform)
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

        # Assign test dataset for use in dataloader(s)
        if stage == "test":
            self.mnist_test = MNIST(self.data_dir, train=False, transform=self.transform)

        if stage == "predict":
            self.mnist_predict = MNIST(self.data_dir, train=False, transform=self.transform)

    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=32)

    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=32)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=32)

    def predict_dataloader(self):
        return DataLoader(self.mnist_predict, batch_size=32)
```

#### LightningDataModule API

To define a DataModule the following methods are used to create train/val/test/predict dataloaders:

- [prepare_data](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#prepare-data) (how to download, tokenize, etc…)
- [setup](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#setup) (how to split, define dataset, etc…)
- [train_dataloader](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#train-dataloader)
- [val_dataloader](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#val-dataloader)
- [test_dataloader](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#test-dataloader)
- [predict_dataloader](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#predict-dataloader)

##### prepare_data

Downloading and saving data with multiple processes (distributed settings) will result in corrupted data. Lightning ensures the [`prepare_data()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.prepare_data) is called only within a single process on CPU, so you can safely add your downloading logic within. In case of multi-node training, the execution of this hook depends upon [prepare_data_per_node](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#prepare-data-per-node). [`setup()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.setup) is called after `prepare_data` and there is a barrier in between which ensures that all the processes proceed to `setup` once the data is prepared and available for use.

- download, i.e. download data only once on the disk from a single process
- tokenize. Since it’s a one time process, it is not recommended to do it on all processes
- etc…

```python
class MNISTDataModule(pl.LightningDataModule):
    def prepare_data(self):
        # download
        MNIST(os.getcwd(), train=True, download=True, transform=transforms.ToTensor())
        MNIST(os.getcwd(), train=False, download=True, transform=transforms.ToTensor())
```

> Warning: `prepare_data` is called from the main process. It is not recommended to assign state here (e.g. `self.x = y`) since it is called on a single process and if you assign states here then they won’t be available for other processes.

##### setup

There are also data operations you might want to perform on every GPU. Use [`setup()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.setup) to do things like:

- count number of classes
- build vocabulary
- perform train/val/test splits
- create datasets
- apply transforms (defined explicitly in your datamodule)
- etc…

```python
import lightning.pytorch as pl

class MNISTDataModule(pl.LightningDataModule):
    def setup(self, stage: str):
        # Assign Train/val split(s) for use in Dataloaders
        if stage == "fit":
            mnist_full = MNIST(self.data_dir, train=True, download=True, transform=self.transform)
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

        # Assign Test split(s) for use in Dataloaders
        if stage == "test":
            self.mnist_test = MNIST(self.data_dir, train=False, download=True, transform=self.transform)
```

For eg., if you are working with NLP task where you need to tokenize the text and use it, then you can do something like as follows:

```python
class LitDataModule(LightningDataModule):
    def prepare_data(self):
        dataset = load_Dataset(...)
        train_dataset = ...
        val_dataset = ...
        # tokenize
        # save it to disk

    def setup(self, stage):
        # load it back here
        dataset = load_dataset_from_disk(...)
```



This method expects a `stage` argument. It is used to separate setup logic for `trainer.{fit,validate,test,predict}`.

> Note: [setup](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#setup) is called from every process across all the nodes. Setting state here is recommended.

> Note: [teardown](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#teardown) can be used to clean up the state. It is also called from every process across all the nodes.

##### train_dataloader

Use the [`train_dataloader()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.train_dataloader) method to generate the training dataloader(s). Usually you just wrap the dataset you defined in [setup](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#setup). This is the dataloader that the Trainer [`fit()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.fit) method uses.

```python
import lightning.pytorch as pl

class MNISTDataModule(pl.LightningDataModule):
    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=64)
```

##### val_dataloader

Use the [`val_dataloader()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.val_dataloader) method to generate the validation dataloader(s). Usually you just wrap the dataset you defined in [setup](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#setup). This is the dataloader that the Trainer [`fit()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.fit) and [`validate()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.validate) methods uses.

```python
import lightning.pytorch as pl

class MNISTDataModule(pl.LightningDataModule):
    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=64)
```

##### test_dataloader

Use the [`test_dataloader()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.test_dataloader) method to generate the test dataloader(s). Usually you just wrap the dataset you defined in [setup](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#setup). This is the dataloader that the Trainer [`test()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.test) method uses.

```python
import lightning.pytorch as pl

class MNISTDataModule(pl.LightningDataModule):
    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=64)
```

##### predict_dataloader

Use the [`predict_dataloader()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.hooks.DataHooks.html#lightning.pytorch.core.hooks.DataHooks.predict_dataloader) method to generate the prediction dataloader(s). Usually you just wrap the dataset you defined in [setup](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#setup). This is the dataloader that the Trainer [`predict()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.predict) method uses.

```python
import lightning.pytorch as pl

class MNISTDataModule(pl.LightningDataModule):
    def predict_dataloader(self):
        return DataLoader(self.mnist_predict, batch_size=64)
```

##### transasfer_batch_to_device

`LightningDataModule.transfer_batch_to_device(batch, device, dataloader_idx)`

Override this hook if your [`DataLoader`](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader) returns tensors wrapped in a custom data structure.

The data types listed below (and any arbitrary nesting of them) are supported out of the box:

- [`torch.Tensor`](https://pytorch.org/docs/stable/tensors.html#torch.Tensor) or anything that implements .to(…)

- [`list`](https://docs.python.org/3/library/stdtypes.html#list)

- [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)

- [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple)


For anything else, you need to define how the data is moved to the target device (CPU, GPU, TPU, …).

>  Note: This hook should only transfer the data and not modify it, nor should it move the data to any other device than the one passed in as argument (unless you know what you are doing). To check the current state of execution of this hook you can use `self.trainer.training/testing/validating/predicting` so that you can add different logic as per your requirement.

> Note: This hook only runs on single GPU training and DDP (no data-parallel). Data-Parallel support will come in near future.

- Parameters
    - **batch** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – A batch of data that needs to be transferred to a new device.
    - **device** ([`device`](https://pytorch.org/docs/stable/tensor_attributes.html#torch.device)) – The target device as defined in PyTorch.
    - **dataloader_idx** ([`int`](https://docs.python.org/3/library/functions.html#int)) – The index of the dataloader to which the batch belongs.
- Return type
    - [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)
- Returns
    - A reference to the data on the new device.

Example:

```python
def transfer_batch_to_device(self, batch, device, dataloader_idx):
    if isinstance(batch, CustomBatch):
        # move all tensors in your custom data structure to the device
        batch.samples = batch.samples.to(device)
        batch.targets = batch.targets.to(device)
    elif dataloader_idx == 0:
        # skip device transfer for the first dataloader or anything you wish
        pass
    else:
        batch = super().transfer_batch_to_device(batch, device, dataloader_idx)
    return batch
```



- Raises
    - **MisconfigurationException** – If using data-parallel, `Trainer(strategy='dp')`.
    - **MisconfigurationException** – If using IPUs, `Trainer(accelerator='ipu')`.

SEE ALSO

- `move_data_to_device()`
- `apply_to_collection()`



##### on_before_batch_transfer

`LightningDataModule.on_before_batch_transfer(batch, dataloader_idx)`

Override to alter or apply batch augmentations to your batch before it is transferred to the device

>  NOTE: To check the current state of execution of this hook you can use `self.trainer.training/testing/validating/predicting` so that you can add different logic as per your requirement.

> NOTE: This hook only runs on single GPU training and DDP (no data-parallel). Data-Parallel support will come in near future.

- Parameters
    - **batch** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – A batch of data that needs to be altered or augmented.
    - **dataloader_idx** ([`int`](https://docs.python.org/3/library/functions.html#int)) – The index of the dataloader to which the batch belongs.
    - 
- Return type
  - [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)
  
- Returns
  - A batch of data
  
- Example:

```python
def on_before_batch_transfer(self, batch, dataloader_idx):
    batch['x'] = transforms(batch['x'])
    return batch
```



##### on_after_batch_transfer

`LightningDataModule.on_after_batch_transfer(batch, dataloader_idx)`

Override to alter or apply batch augmentations to your batch after it is transferred to the device.

>  NOTE: To check the current state of execution of this hook you can use `self.trainer.training/testing/validating/predicting` so that you can add different logic as per your requirement.

> NOTE: This hook only runs on single GPU training and DDP (no data-parallel). Data-Parallel support will come in near future.

- Parameters
    - **batch** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – A batch of data that needs to be altered or augmented.
    - **dataloader_idx** ([`int`](https://docs.python.org/3/library/functions.html#int)) – The index of the dataloader to which the batch belongs.

- Return type
    - [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)

- Returns
    - A batch of data

- Example:

```python
def on_after_batch_transfer(self, batch, dataloader_idx):
    batch['x'] = gpu_transforms(batch['x'])
    return batch
```

- Raises

    - **MisconfigurationException** – If using data-parallel, `Trainer(strategy='dp')`.	

    - **MisconfigurationException** – If using IPUs, `Trainer(accelerator='ipu')`.



- SEE ALSO

    - `on_before_batch_transfer()`

    - `transfer_batch_to_device()`

##### load_state_dict

`LightningDataModule.load_state_dict(state_dict)`[[SOURCE\]](https://lightning.ai/docs/pytorch/stable/_modules/lightning/pytorch/core/datamodule.html#LightningDataModule.load_state_dict)

Called when loading a checkpoint, implement to reload datamodule state given datamodule state_dict.

- Parameters
    - **state_dict** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/library/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – the datamodule state returned by `state_dict`.

- Return type
    - [`None`](https://docs.python.org/3/library/constants.html#None)

##### state_dict

`LightningDataModule.state_dict()`[[SOURCE\]](https://lightning.ai/docs/pytorch/stable/_modules/lightning/pytorch/core/datamodule.html#LightningDataModule.state_dict)

Called when saving a checkpoint, implement to generate and save datamodule state.

- Return type
    - [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/library/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
- Returns
    - A dictionary containing datamodule state.

##### teardown

`LightningDataModule.teardown(*stage*)`

Called at the end of fit (train + validate), validate, test, or predict.

- Parameters
    - **stage** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – either `'fit'`, `'validate'`, `'test'`, or `'predict'`

- Return type
    - [`None`](https://docs.python.org/3/library/constants.html#None)

##### prepare_data_per_node

If set to `True` will call `prepare_data()` on LOCAL_RANK=0 for every node. If set to `False` will only call from NODE_RANK=0, LOCAL_RANK=0.

```python
class LitDataModule(LightningDataModule):
    def __init__(self):
        super().__init__()
        self.prepare_data_per_node = True
```



#### Using a DataModule

The recommended way to use a DataModule is simply:

```python
dm = MNISTDataModule()
model = Model()
trainer.fit(model, datamodule=dm)
trainer.test(datamodule=dm)
trainer.validate(datamodule=dm)
trainer.predict(datamodule=dm)
```



If you need information from the dataset to build your model, then run [prepare_data](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#prepare-data) and [setup](https://lightning.ai/docs/pytorch/stable/data/datamodule.html#setup) manually (Lightning ensures the method runs on the correct devices).

```python
dm = MNISTDataModule()
dm.prepare_data()
dm.setup(stage="fit")

model = Model(num_classes=dm.num_classes, width=dm.width, vocab=dm.vocab)
trainer.fit(model, dm)

dm.setup(stage="test")
trainer.test(datamodule=dm)
```

You can access the current used datamodule of a trainer via `trainer.datamodule` and the current used dataloaders via the trainer properties [`train_dataloader()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.train_dataloader), [`val_dataloaders()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.val_dataloaders), [`test_dataloaders()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.test_dataloaders), and [`predict_dataloaders()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.predict_dataloaders).

#### DataModules without Lightning

You can of course use DataModules in plain PyTorch code as well.

```python
# download, etc...
dm = MNISTDataModule()
dm.prepare_data()

# splits/transforms
dm.setup(stage="fit")

# use data
for batch in dm.train_dataloader():
    ...

for batch in dm.val_dataloader():
    ...

dm.teardown(stage="fit")

# lazy load test data
dm.setup(stage="test")
for batch in dm.test_dataloader():
    ...

dm.teardown(stage="test")
```

But overall, DataModules encourage reproducibility by allowing all details of a dataset to be specified in a unified structure.

#### Hyperparameters in DataModules

Like LightningModules, DataModules support hyperparameters with the same API.

```python
import lightning.pytorch as pl

class CustomDataModule(pl.LightningDataModule):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.save_hyperparameters()

    def configure_optimizers(self):
        # access the saved hyperparameters
        opt = optim.Adam(self.parameters(), lr=self.hparams.lr)
```



Refer to `save_hyperparameters` in [lightning module](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html) for more details.

------

##### Save DataModule state

When a checkpoint is created, it asks every DataModule for their state. If your DataModule defines the *state_dict* and *load_state_dict* methods, the checkpoint will automatically track and restore your DataModules.

```python
class LitDataModule(pl.DataModuler):
    def state_dict(self):
        # track whatever you want here
        state = {"current_train_batch_index": self.current_train_batch_index}
        return state

    def load_state_dict(self, state_dict):
        # restore the state based on what you tracked in (def state_dict)
        self.current_train_batch_index = state_dict["current_train_batch_index"]
```



### Control it all from the CLI

Configure hyperparameters from the CLI

#### LightningCLI requirements

The [`LightningCLI`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.cli.LightningCLI.html#lightning.pytorch.cli.LightningCLI) class is designed to significantly ease the implementation of CLIs. 

To use this class, an additional Python requirement is necessary than the minimal installation of Lightning provides. To enable, either install all extras:

```bash
pip install "pytorch-lightning[extra]"
```

or if only interested in `LightningCLI`, just install jsonargparse:

```bash
pip install "jsonargparse[signatures]"
```

#### Implementing a CLI

Implementing a CLI is as simple as instantiating a [`LightningCLI`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.cli.LightningCLI.html#lightning.pytorch.cli.LightningCLI) object giving as arguments classes for a `LightningModule` and optionally a `LightningDataModule`:

```python
# main.py
from lightning.pytorch.cli import LightningCLI

# simple demo classes for your convenience
from lightning.pytorch.demos.boring_classes import DemoModel, BoringDataModule


def cli_main():
    cli = LightningCLI(DemoModel, BoringDataModule)
    # note: don't call fit!!


if __name__ == "__main__":
    cli_main()
    # note: it is good practice to implement the CLI in a function and call it in the main if block
```



Now your model can be managed via the CLI. To see the available commands type:

```bash
$ python main.py --help
```



which prints out:

```bash
usage: main.py [-h] [-c CONFIG] [--print_config [={comments,skip_null,skip_default}+]]
        {fit,validate,test,predict,tune} ...

pytorch-lightning trainer command line tool

optional arguments:
-h, --help            Show this help message and exit.
-c CONFIG, --config CONFIG
                        Path to a configuration file in json or yaml format.
--print_config [={comments,skip_null,skip_default}+]
                        Print configuration and exit.

subcommands:
For more details of each subcommand add it as argument followed by --help.

{fit,validate,test,predict,tune}
    fit                 Runs the full optimization routine.
    validate            Perform one evaluation epoch over the validation set.
    test                Perform one evaluation epoch over the test set.
    predict             Run inference on your data.
    tune                Runs routines to tune hyperparameters before training.
```



The message tells us that we have a few available subcommands:

```bash
python main.py [subcommand]
```



which you can use depending on your use case:

```bash
$ python main.py fit
$ python main.py validate
$ python main.py test
$ python main.py predict
$ python main.py tune
```

#### Train a model with the CLI

To train a model, use the `fit` subcommand:

```bash
python main.py fit
```

View all available options with the `--help` argument given after the subcommand:

```bash
$ python main.py fit --help

usage: main.py [options] fit [-h] [-c CONFIG]
                            [--seed_everything SEED_EVERYTHING] [--trainer CONFIG]
                            ...
                            [--ckpt_path CKPT_PATH]
    --trainer.logger LOGGER

optional arguments:
<class '__main__.DemoModel'>:
    --model.out_dim OUT_DIM
                            (type: int, default: 10)
    --model.learning_rate LEARNING_RATE
                            (type: float, default: 0.02)
<class 'lightning.pytorch.demos.boring_classes.BoringDataModule'>:
--data CONFIG         Path to a configuration file.
--data.data_dir DATA_DIR
                        (type: str, default: ./)
```



With the Lightning CLI enabled, you can now change the parameters without touching your code:

```bash
# change the learning_rate
python main.py fit --model.learning_rate 0.1

# change the output dimensions also
python main.py fit --model.out_dim 10 --model.learning_rate 0.1

# change trainer and data arguments too
python main.py fit --model.out_dim 2 --model.learning_rate 0.1 --data.data_dir '~/' --trainer.logger False
```

> Tip: 
>
> The options that become available in the CLI are the `__init__` parameters of the `LightningModule` and `LightningDataModule` classes. Thus, to make hyperparameters configurable, just add them to your class’s `__init__`. It is highly recommended that these parameters are described in the docstring so that the CLI shows them in the help. Also, the parameters should have accurate type hints so that the CLI can fail early and give understandable error messages when incorrect values are given.



### Mix models and datasets

#### Why mix models and datasets

Lightning projects usually begin with one model and one dataset. As the project grows in complexity and you introduce more models and more datasets, it becomes desirable to mix any model with any dataset directly from the command line without changing your code.

```bash
# Mix and match anything
$ python main.py fit --model=GAN --data=MNIST
$ python main.py fit --model=Transformer --data=MNIST
```



`LightningCLI` makes this very simple. Otherwise, this kind of configuration requires a significant amount of boilerplate that often looks like this:

```python
# choose model
if args.model == "gan":
    model = GAN(args.feat_dim)
elif args.model == "transformer":
    model = Transformer(args.feat_dim)
...

# choose datamodule
if args.data == "MNIST":
    datamodule = MNIST()
elif args.data == "imagenet":
    datamodule = Imagenet()
...

# mix them!
trainer.fit(model, datamodule)
```



It is highly recommended that you avoid writing this kind of boilerplate and use `LightningCLI` instead.

#### Multiple LightningModules

To support multiple models, when instantiating `LightningCLI` omit the `model_class` parameter:

```python
# main.py
from lightning.pytorch.cli import LightningCLI
from lightning.pytorch.demos.boring_classes import DemoModel, BoringDataModule

class Model1(DemoModel):
    def configure_optimizers(self):
        print("⚡", "using Model1", "⚡")
        return super().configure_optimizers()


class Model2(DemoModel):
    def configure_optimizers(self):
        print("⚡", "using Model2", "⚡")
        return super().configure_optimizers()


cli = LightningCLI(datamodule_class=BoringDataModule)
```



Now you can choose between any model from the CLI:

```bash
# use Model1
python main.py fit --model Model1

# use Model2
python main.py fit --model Model2
```

> TIP:
>
> Instead of omitting the `model_class` parameter, you can give a base class and `subclass_mode_model=True`. This will make the CLI only accept models which are a subclass of the given base class.

#### Multiple LightningDataModules

To support multiple data modules, when instantiating `LightningCLI` omit the `datamodule_class` parameter:

```python
# main.py
import torch
from lightning.pytorch.cli import LightningCLI
from lightning.pytorch.demos.boring_classes import DemoModel, BoringDataModule


class FakeDataset1(BoringDataModule):
    def train_dataloader(self):
        print("⚡", "using FakeDataset1", "⚡")
        return torch.utils.data.DataLoader(self.random_train)


class FakeDataset2(BoringDataModule):
    def train_dataloader(self):
        print("⚡", "using FakeDataset2", "⚡")
        return torch.utils.data.DataLoader(self.random_train)


cli = LightningCLI(DemoModel)
```



Now you can choose between any dataset at runtime:

```bash
# use Model1
python main.py fit --data FakeDataset1

# use Model2
python main.py fit --data FakeDataset2
```

> TIP: 
>
> Instead of omitting the `datamodule_class` parameter, you can give a base class and `subclass_mode_data=True`. This will make the CLI only accept data modules that are a subclass of the given base class.

#### Multiple optimizers

Standard optimizers from `torch.optim` work out of the box:

```bash
python main.py fit --optimizer AdamW
```



If the optimizer you want needs other arguments, add them via the CLI (no need to change your code)!

```bash
python main.py fit --optimizer SGD --optimizer.lr=0.01
```



Furthermore, any custom subclass of [`torch.optim.Optimizer`](https://pytorch.org/docs/stable/optim.html#torch.optim.Optimizer) can be used as an optimizer:

```python
# main.py
import torch
from lightning.pytorch.cli import LightningCLI
from lightning.pytorch.demos.boring_classes import DemoModel, BoringDataModule


class LitAdam(torch.optim.Adam):
    def step(self, closure):
        print("⚡", "using LitAdam", "⚡")
        super().step(closure)


class FancyAdam(torch.optim.Adam):
    def step(self, closure):
        print("⚡", "using FancyAdam", "⚡")
        super().step(closure)


cli = LightningCLI(DemoModel, BoringDataModule)
```



Now you can choose between any optimizer at runtime:

```bash
# use LitAdam
python main.py fit --optimizer LitAdam

# use FancyAdam
python main.py fit --optimizer FancyAdam
```

#### Multiple schedulers

Standard learning rate schedulers from `torch.optim.lr_scheduler` work out of the box:

```bash
python main.py fit --lr_scheduler CosineAnnealingLR
```

If the scheduler you want needs other arguments, add them via the CLI (no need to change your code)!

```bash
python main.py fit --lr_scheduler=ReduceLROnPlateau --lr_scheduler.monitor=epoch
```

Furthermore, any custom subclass of `torch.optim.lr_scheduler.LRScheduler` can be used as learning rate scheduler:

```python
# main.py
import torch
from lightning.pytorch.cli import LightningCLI
from lightning.pytorch.demos.boring_classes import DemoModel, BoringDataModule


class LitLRScheduler(torch.optim.lr_scheduler.CosineAnnealingLR):
    def step(self):
        print("⚡", "using LitLRScheduler", "⚡")
        super().step()


cli = LightningCLI(DemoModel, BoringDataModule)
```

Now you can choose between any learning rate scheduler at runtime:

```bash
# LitLRScheduler
python main.py fit --lr_scheduler LitLRScheduler
```

#### Classes from any package

In the previous sections, custom classes to select were defined in the same python file where the `LightningCLI` class is run. To select classes from any package by using only the class name, import the respective package:

```python
from lightning.pytorch.cli import LightningCLI
import my_code.models  # noqa: F401
import my_code.data_modules  # noqa: F401
import my_code.optimizers  # noqa: F401

cli = LightningCLI()
```



Now use any of the classes:

```bash
python main.py fit --model Model1 --data FakeDataset1 --optimizer LitAdam --lr_scheduler LitLRScheduler
```



The `# noqa: F401` comment avoids a linter warning that the import is unused.

It is also possible to select subclasses that have not been imported by giving the full import path:

```bash
python main.py fit --model my_code.models.Model1
```

#### Help for specific classes

When multiple models or datasets are accepted, the main help of the CLI does not include their specific parameters. To show this specific help, additional help arguments expect the class name or its import path. For example:

```bash
python main.py fit --model.help Model1
python main.py fit --data.help FakeDataset2
python main.py fit --optimizer.help Adagrad
python main.py fit --lr_scheduler.help StepLR
```



## Level 10: Understand your model

1. [Alter checkpoint behavior](https://lightning.ai/docs/pytorch/stable/common/checkpointing_intermediate.html)

   Users looking to customize the checkpointing behavior

2. [Visualize more than metrics](https://lightning.ai/docs/pytorch/stable/visualize/logging_intermediate.html)

   Users who want to track more complex outputs and use third-party experiment managers.

3. [Granular control (Kiểm soát chi tiết) of logging](https://lightning.ai/docs/pytorch/stable/visualize/logging_advanced.html)

   Users who want to do advanced speed optimizations by customizing the logging behavior.

## Level 11: Explore SOTA scaling techniques

1. [Half precision training](https://lightning.ai/docs/pytorch/stable/common/precision_basic.html)

   Users looking to train models faster and consume less memory.

2. [SOTA scaling techniques](https://lightning.ai/docs/pytorch/stable/advanced/training_tricks.html)

   Lightning implements various techniques to help during training that can help make the training smoother.

## Level 12: Deploy your model

1. [Deploy with ONNX](https://lightning.ai/docs/pytorch/stable/deploy/production_advanced.html)

   Machine learning engineers optimizing models for enterprise-scale production environments.

2. [Deploy with torchscript](https://lightning.ai/docs/pytorch/stable/deploy/production_advanced_2.html)

   Machine learning engineers optimizing models for enterprise-scale production environments.

3. [Compress models for fast inference](https://lightning.ai/docs/pytorch/stable/advanced/pruning_quantization.html)

   Pruning and Quantization are techniques to compress model size for deployment, allowing inference speed up and energy saving without significant accuracy losses.

## Level 13: Optimize training speed

1. [Explore advanced mixed precision settings](https://lightning.ai/docs/pytorch/stable/common/precision_intermediate.html)

   Users looking to scale larger models or take advantage of optimized accelerators.

2. [Enable advanced profilers](https://lightning.ai/docs/pytorch/stable/tuning/profiler_basic.html)

   Users who want to learn the basics of removing bottlenecks from their code

3. [Profile Pytorch operation](https://lightning.ai/docs/pytorch/stable/tuning/profiler_intermediate.html)

   Users who want to see more granular profiling information

## Level 14: Run on on-prem clusters

1. [Run on an on-prem cluster](https://lightning.ai/docs/pytorch/stable/clouds/cluster_intermediate_1.html)

   Users who need to run on an academic or enterprise private cluster.

2. [Run on a SLURM cluster](https://lightning.ai/docs/pytorch/stable/clouds/cluster_advanced.html)

   Lightning automates the details behind training on a SLURM-powered cluster. In contrast to the general purpose cluster above, the user does not start the jobs manually on each node and instead submits it to SLURM which schedules the resources and time for which the job is allowed to run.

3. [Run with Torch Distributed](https://lightning.ai/docs/pytorch/stable/clouds/cluster_intermediate_2.html)

   [Torch Distributed Run](https://pytorch.org/docs/stable/elastic/run.html) provides helper functions to setup distributed environment variables from the [PyTorch distributed communication package](https://pytorch.org/docs/stable/distributed.html#environment-variable-initialization) that need to be defined on each node.
