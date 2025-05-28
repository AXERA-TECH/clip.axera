# CLIP.axera
clip-vit-l-14 demo on axera

## 支持平台
- [x] AX650N
- [ ] AX630C

### requirements.txt

需要安装 clip , `pip install clip`

### 导出模型(PyTorch -> ONNX)
运行前请注意export_onnx.py的注释，为了方便导出对clip源码进行了修改
```
python export_onnx.py
```
导出成功后会生成两个onnx模型:
- image encoder: clip_vit_l14_336px_image_encoder_batchfirst.onnx
- text encoder: clip_vit_l14_336px_text_encoder.onnx


#### 转换模型(ONNX -> Axera)
使用模型转换工具 Pulsar2 将 ONNX 模型转换成适用于 Axera 的 NPU 运行的模型文件格式 .axmodel，通常情况下需要经过以下两个步骤：

- 生成适用于该模型的 PTQ 量化校准数据集
- 使用 Pulsar2 build 命令集进行模型转换（PTQ 量化、编译），更详细的使用说明请参考[AXera Pulsar2 工具链指导手册](https://pulsar2-docs.readthedocs.io/zh-cn/latest/index.html)


#### 量化数据集准备
- image数据
下载[dataset_v04.zip](https://github.com/user-attachments/files/20480889/dataset_v04.zip)或自行准备
- text数据
    ```
    python gen_text_calibration_data.py
    cd dataset
    zip -r dataset/text_quant_data.zip dataset/text_quant_data
    ```
最终得到两个数据集：

\- dataset_v04.zip

\- dataset/text_quant_data.zip

#### 模型编译
修改配置文件
检查config.json 中 calibration_dataset 字段，将该字段配置的路径改为上一步准备的量化数据集存放路径

在编译环境中，执行pulsar2 build参考命令：
```
# image encoder
pulsar2 build --config build_config/clip_vit_l14_336px_image_encoder_all_u16_fc_u8.json --input clip_vit_l14_336px_image_encoder_batchfirst.onnx --output_dir build_output/image_encoder --output_name clip_vit_l14_336px_image_encoder_all_u16_fc_u8.axmodel

# text encoder
pulsar2 build --config build_config/clip_vit_l14_336px_text_encoder_u16.json --input clip_vit_l14_336px_text_encoder.onnx --output_dir build_output/text_encoder --output_name clip_vit_l14_336px_text_encoder_u16.axmodel
```
编译完成后得到两个axmodel模型：

\- clip_vit_l14_336px_image_encoder_all_u16_fc_u8.axmodel

\- clip_vit_l14_336px_text_encoder_u16.axmodel


### Python API 运行
需基于[PyAXEngine](https://github.com/AXERA-TECH/pyaxengine)在AX650N上进行部署,安装完成后运行main.py文件，得到以下输出demo
```shell
$ python main.py 
python main.py
[INFO] Available providers:  ['AxEngineExecutionProvider']
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Chip type: ChipType.MC50
[INFO] VNPU type: VNPUType.DISABLED
[INFO] Engine version: 2.10.1s
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.0 685bfee4
input.1 [1, 3, 336, 336] float32
4002 [1, 768] float32
[INFO] Using provider: AxEngineExecutionProvider
[INFO] Model type: 2 (triple core)
[INFO] Compiler version: 4.0 685bfee4
texts [1, 77] int32
text_features [1, 768] float32
(14, 768)
(11, 768)
=== logits_per_image ===
                   cat   dog  husky  airplane   car  cityscape  fire  person  eagle  bike  pineapple
cityscape.png     0.00  0.00   0.00      0.00  0.19       0.24  0.50    0.00    0.0  0.00       0.05
fire.png          0.00  0.00   0.00      0.00  0.00       0.00  1.00    0.00    0.0  0.00       0.00
air.jpg           0.00  0.00   0.00      0.94  0.04       0.00  0.01    0.00    0.0  0.01       0.00
bike2.jpg         0.00  0.02   0.01      0.00  0.46       0.00  0.01    0.29    0.0  0.21       0.00
pineapple.jpg     0.00  0.00   0.00      0.00  0.00       0.00  0.00    0.00    0.0  0.00       1.00
husky.jpeg        0.00  0.00   1.00      0.00  0.00       0.00  0.00    0.00    0.0  0.00       0.00
big-dog.jpg       0.00  0.15   0.07      0.00  0.56       0.00  0.03    0.09    0.0  0.01       0.08
eagle.jpg         0.00  0.00   0.00      0.00  0.00       0.00  0.00    0.00    1.0  0.00       0.00
cat.jpg           0.91  0.03   0.01      0.00  0.01       0.00  0.01    0.00    0.0  0.01       0.03
bike.jpg          0.00  0.00   0.01      0.00  0.01       0.00  0.00    0.05    0.0  0.92       0.00
grace_hopper.jpg  0.02  0.07   0.00      0.00  0.55       0.00  0.28    0.07    0.0  0.00       0.00
dog.jpg           0.00  0.12   0.04      0.00  0.04       0.00  0.00    0.00    0.0  0.80       0.00
dog-chai.jpeg     0.00  0.23   0.04      0.00  0.57       0.00  0.06    0.07    0.0  0.01       0.02
mv2seg.png        0.00  0.00   0.00      0.00  0.98       0.00  0.00    0.01    0.0  0.00       0.00

=== logits_per_text ===
           cityscape.png  fire.png  air.jpg  bike2.jpg  pineapple.jpg  husky.jpeg  big-dog.jpg  eagle.jpg  cat.jpg  bike.jpg  grace_hopper.jpg  dog.jpg  dog-chai.jpeg  mv2seg.png
cat                 0.00      0.00     0.00       0.00            0.0        0.00         0.01       0.01     0.92      0.00              0.02     0.00           0.04        0.00
dog                 0.00      0.00     0.00       0.00            0.0        0.01         0.14       0.02     0.01      0.00              0.01     0.40           0.41        0.00
husky               0.00      0.00     0.00       0.00            0.0        1.00         0.00       0.00     0.00      0.00              0.00     0.00           0.00        0.00
airplane            0.00      0.00     0.91       0.00            0.0        0.00         0.01       0.07     0.00      0.00              0.00     0.00           0.01        0.00
car                 0.01      0.00     0.01       0.03            0.0        0.00         0.19       0.01     0.00      0.00              0.03     0.05           0.38        0.29
cityscape           0.64      0.00     0.00       0.00            0.0        0.00         0.05       0.01     0.00      0.09              0.00     0.00           0.16        0.05
fire                0.01      0.94     0.00       0.00            0.0        0.00         0.01       0.01     0.00      0.00              0.01     0.00           0.02        0.00
person              0.00      0.00     0.00       0.15            0.0        0.00         0.22       0.04     0.00      0.17              0.03     0.03           0.33        0.01
eagle               0.00      0.00     0.00       0.00            0.0        0.00         0.00       1.00     0.00      0.00              0.00     0.00           0.00        0.00
bike                0.00      0.00     0.00       0.01            0.0        0.00         0.00       0.00     0.00      0.29              0.00     0.69           0.00        0.00
pineapple           0.00      0.00     0.00       0.00            1.0        0.00         0.00       0.00     0.00      0.00              0.00     0.00           0.00        0.00
```


## 技术讨论

- Github issues
- QQ 群: 139953715