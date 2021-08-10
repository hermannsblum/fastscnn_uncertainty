from sacred import Experiment
import torch
import tensorflow_datasets as tfds
import tensorflow as tf
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

tf.config.set_visible_devices([], 'GPU')

from semseg_density.gdrive import load_gdrive_file
from semseg_density.settings import TMPDIR, EXP_OUT
from semseg_density.data.nyu_depth_v2 import TRAINING_LABEL_NAMES

ex = Experiment()


@ex.main
def scatter(
    path,
    out_classes=['pilow', 'refridgerator',
                                                 'television'],
):
  # make sure the directory exists, but is empty
  directory = os.path.join(EXP_OUT, path)

  in_nll = []
  out_nll = []
  in_entropy = []
  out_entropy = []

  # map labels to in-domain (0) or out-domain (1)
  ood_map = np.zeros(40, dtype='uint8')
  for c in range(40):
    if TRAINING_LABEL_NAMES[c] in out_classes:
      ood_map[c] = 1

  frames = [x[:-10] for x in os.listdir(directory) if x.endswith('label.npy')]
  for frame in tqdm(frames):
    label = np.load(os.path.join(directory, f'{frame}_label.npy'))
    ood = ood_map[label]
    nll = np.load(os.path.join(directory, f'{frame}_nll.npy'))
    entropy = np.load(os.path.join(directory, f'{frame}_entropy.npy'))
    in_nll.append(nll[ood == 0].reshape((-1)))
    in_entropy.append(entropy[ood == 0].reshape((-1)))
    out_nll.append(nll[ood == 1].reshape((-1)))
    out_entropy.append(entropy[ood == 1].reshape((-1)))
  in_nll = np.concatenate(in_nll)
  out_nll = np.concatenate(out_nll)
  in_entropy = np.concatenate(in_entropy)
  out_entropy = np.concatenate(out_entropy)

  plt.figure(figsize=(10, 10))
  plt.scatter(in_nll,
              in_entropy,
              c="black",
              alpha=0.05,
              linewidths=0.0,
              rasterized=True)
  plt.scatter(out_nll,
              out_entropy,
              c="red",
              alpha=0.05,
              linewidths=0.0,
              rasterized=True)
  plt.xlabel('Latent Density')
  plt.ylabel('Softmax Entropy')
  plt.savefig(os.path.join(directory, 'ood_scatter.pdf'), dpi=400)


if __name__ == '__main__':
  ex.run_commandline()
