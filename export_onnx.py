import numpy as np
import logging
import time
import clip
import torch
from tqdm import tqdm


""" 导出时需要 修改 clip.model 中 358 行 forward 替换成以下代码：
    def forward(self, text):
        text_features = self.encode_text(text)
        text_features = text_features / text_features.norm(dim=1, keepdim=True)
        # shape = [global_batch_size, global_batch_size]
        return text_features
"""
with torch.no_grad():
    model, preprocess = clip.load("ViT-L/14@336px", "cpu")
    # 根据这里的shape，来设置 x 的shape
    print(preprocess)
    x = torch.randn(1, 3, 336, 336, dtype=torch.float32)
    torch.onnx.export(
        model.visual,
        (x),
        "clip_vit_l14_336px_image_encoder_batchfirst.onnx",
    )

    text = clip.tokenize(["a diagram"]).to("cpu")
    torch.onnx.export(
        model, (text,), "clip_vit_l14_336px_text_encoder.onnx", input_names=['texts'],
                            output_names=['text_features'],opset_version=14
    )
