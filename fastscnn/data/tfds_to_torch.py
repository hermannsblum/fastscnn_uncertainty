import torch
import tensorflow_datasets as tfds

class TFDSIterableDataset(torch.utils.data.IterableDataset):
  def __init__(self, *args, **kwargs):
    super().__init__()
    self.tfds_data = tfds.load(*args, **kwargs)

  def __iter__(self):
    return iter(tfds.as_numpy(self.tfds_data))

  def __len__(self):
    return len(self.tfds_data)

class TFDataIterableDataset(torch.utils.data.IterableDataset):
  def __init__(self, ds):
    super().__init__()
    self.tf_dataset = ds

  def __iter__(self):
    return iter(tfds.as_numpy(self.tf_dataset))

  def __len__(self):
    return len(self.tf_dataset)
