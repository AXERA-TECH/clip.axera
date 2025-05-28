import cv2
import numpy as np
import glob
import pandas as pd
import axengine as ort
import Tokenizer
import copy

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def get_tokenizer():
    tokenizer = Tokenizer.TokenizerClip()
    tokenizer.load_tokenize("vocab.txt")
    return tokenizer

def get_image_encoder() -> ort.InferenceSession:
    image_encoder = ort.InferenceSession("clip_vit_l14_336px_image_encoder_all_u16_fc_u8.axmodel")

    for input in image_encoder.get_inputs():
        print(input.name, input.shape, input.dtype)

    for output in image_encoder.get_outputs():
        print(output.name, output.shape, output.dtype)
    
    return image_encoder

def get_text_encoder() -> ort.InferenceSession:
    text_encoder = ort.InferenceSession("clip_vit_l14_336px_text_encoder_u16.axmodel")

    for input in text_encoder.get_inputs():
        print(input.name, input.shape, input.dtype)

    for output in text_encoder.get_outputs():
        print(output.name, output.shape, output.dtype)
    
    return text_encoder
    
def preprocess_image(image, width=336, height=336):
    data = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    data = cv2.resize(data, (width, height)).astype(np.float32)
    mean = np.array([123.680, 116.779, 103.939], dtype=np.float32)
    std = np.array([68.5, 66.6, 70.32], dtype=np.float32)
    data = (data - mean) / std
    data = data.transpose(2, 0, 1).reshape(1, 3, height, width)
    return data


def features_matmul(
            image_features: np.ndarray,
            text_features: np.ndarray
            ) -> tuple[np.ndarray, np.ndarray]:
    """
    Args:
        image_features: shape (N_img, D)
        text_features : shape (N_txt, D)
    
    Returns:
        logits_per_image_softmax: shape (N_img, N_txt)
        logits_per_text_softmax : shape (N_txt, N_img)
    """
    logit_scale = 100
    # 1. Normalize each image feature vector to unit length
    norms = np.linalg.norm(image_features, axis=1, keepdims=True)  # :contentReference[oaicite:2]{index=2}
    image_normed = image_features / norms

    # 2. Compute raw logits: (N_img, D) @ (D, N_txt) → (N_img, N_txt)
    logits_per_image = logit_scale * image_normed.dot(text_features.T)

    # 3. Softmax over each image’s logits (rows)
    #    softmax(x)_ij = exp(x_ij) / sum_j exp(x_ij)
    exp_img = np.exp(logits_per_image)                                  # :contentReference[oaicite:3]{index=3}
    sum_exp_img = exp_img.sum(axis=1, keepdims=True)                    # :contentReference[oaicite:4]{index=4}
    logits_per_image_softmax = exp_img / sum_exp_img

    # 4. Transpose logits to get (N_txt, N_img), then softmax over texts
    logits_per_text = logits_per_image.T
    exp_txt = np.exp(logits_per_text)
    sum_exp_txt = exp_txt.sum(axis=1, keepdims=True)
    logits_per_text_softmax = exp_txt / sum_exp_txt

    return logits_per_image_softmax, logits_per_text_softmax

if __name__ == "__main__":
    image_encoder = get_image_encoder()
    text_encoder = get_text_encoder()
    tokenizer = get_tokenizer()
    
    img_features = []
    image_list = glob.glob("images/*.*")
    for image_path in image_list:
        img = cv2.imread(image_path)
        data = preprocess_image(img)
        img_feat = image_encoder.run(None, {"input.1": data})[0]
        img_features.append(copy.deepcopy(img_feat))
    img_features = np.concatenate(img_features, axis=0)
    print(img_features.shape)
    
    texts = ["cat","dog","husky","airplane","car","cityscape","fire","person","eagle","bike","pineapple"]
    text_features = []
    for text in texts:
        t = tokenizer.encode_text(text)
        text_feat = text_encoder.run(None, {"texts": np.array(t).reshape(1, -1).astype(np.int32)})[0]
        text_features.append(copy.deepcopy(text_feat))
    text_features = np.concatenate(text_features, axis=0)
    print(text_features.shape)

    logits_per_image, logits_per_text = features_matmul(img_features, text_features)
    
    image_names = [path.split('/')[-1] for path in image_list]
    
    df_img = pd.DataFrame(
        np.around(logits_per_image,2),
        index=image_names,
        columns=texts
    )
    print("=== logits_per_image ===")
    print(df_img.to_string()) 
    
    df_txt = pd.DataFrame(
        np.around(logits_per_text,2),
        index=texts,
        columns=image_names
    )
    print("\n=== logits_per_text ===")
    print(df_txt.to_string())