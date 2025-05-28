import numpy as np
import cn_clip.clip as clip
import torch
import numpy as np
import logging
import time
# import clip
import torch
import os
from tqdm import tqdm
from imagenet_dataset import ImagenetDataset, imagenet_classes, imagenet_templates
import onnx
import onnxruntime as ort
import numpy as np

import random

# model, preprocess = clip.load("ViT-L/14@336px", "cpu")


for i, classname in enumerate(imagenet_classes):
    if i>=64:
        break

    idx = random.randint(0, 79)

    texts = [imagenet_templates[idx].format(classname)]
    # format with class
    texts = clip.tokenize(texts,context_length=77)  # tokenize
    texts = texts.to(torch.int32)
    s_path = f"dataset/text_quant_data/{idx}.npy"
    print("save: ", s_path, texts.shape)
    np.save(s_path, texts.numpy())
