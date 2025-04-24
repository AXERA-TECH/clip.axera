# CLIP.axera
clip-vit-l-14 demo on axera

## 支持平台
- [x] AX650N
- [ ] AX630C

### Python API 运行
```shell
$ python main.py 
[INFO] Available providers:  ['AXCLRTExecutionProvider']
[INFO] Using provider: AXCLRTExecutionProvider
[INFO] SOC Name: AX650N
[INFO] VNPU type: VNPUType.DISABLED
[INFO] Compiler version: 3.4-dirty d92a794b-dirty
input.1 [1, 3, 336, 336] float32
4502 [1, 768] float32
[INFO] Using provider: AXCLRTExecutionProvider
[INFO] SOC Name: AX650N
[INFO] VNPU type: VNPUType.DISABLED
[INFO] Compiler version: 3.4-dirty d92a794b-dirty
texts [1, 77] int32
text_features [1, 768] float32
(14, 768)
(11, 768)
=== logits_per_image ===
                   cat   dog  husky  airplane   car  cityscape  fire  person  eagle  bike  pineapple
dog.jpg           0.00  0.09   0.02      0.00  0.06       0.00  0.00    0.00   0.00  0.82       0.00
big-dog.jpg       0.00  0.09   0.31      0.01  0.36       0.00  0.01    0.17   0.00  0.00       0.05
fire.png          0.00  0.00   0.00      0.00  0.00       0.00  1.00    0.00   0.00  0.00       0.00
bike2.jpg         0.00  0.02   0.00      0.00  0.18       0.00  0.04    0.21   0.00  0.54       0.00
bike.jpg          0.00  0.00   0.00      0.00  0.00       0.01  0.00    0.02   0.00  0.97       0.00
air.jpg           0.00  0.00   0.00      0.95  0.04       0.00  0.00    0.01   0.00  0.00       0.00
dog-chai.jpeg     0.01  0.22   0.16      0.01  0.44       0.01  0.02    0.11   0.00  0.00       0.02
cityscape.png     0.01  0.00   0.00      0.00  0.28       0.29  0.40    0.00   0.00  0.00       0.01
husky.jpeg        0.00  0.00   1.00      0.00  0.00       0.00  0.00    0.00   0.00  0.00       0.00
grace_hopper.jpg  0.05  0.05   0.00      0.00  0.51       0.00  0.23    0.16   0.01  0.00       0.00
cat.jpg           0.93  0.02   0.01      0.00  0.01       0.00  0.00    0.00   0.00  0.01       0.01
pineapple.jpg     0.00  0.00   0.00      0.00  0.00       0.00  0.00    0.00   0.00  0.00       1.00
mv2seg.png        0.00  0.00   0.00      0.00  0.96       0.00  0.00    0.01   0.01  0.00       0.01
eagle.jpg         0.00  0.00   0.00      0.00  0.00       0.00  0.00    0.00   1.00  0.00       0.00

=== logits_per_text ===
           dog.jpg  big-dog.jpg  fire.png  bike2.jpg  bike.jpg  air.jpg  dog-chai.jpeg  cityscape.png  husky.jpeg  grace_hopper.jpg  cat.jpg  pineapple.jpg  mv2seg.png  eagle.jpg
cat           0.00         0.01      0.00       0.00      0.00     0.00           0.01           0.00        0.00              0.01     0.97            0.0        0.00       0.00
dog           0.39         0.15      0.00       0.00      0.00     0.00           0.29           0.00        0.05              0.00     0.02            0.0        0.00       0.08
husky         0.00         0.00      0.00       0.00      0.00     0.00           0.00           0.00        1.00              0.00     0.00            0.0        0.00       0.00
airplane      0.00         0.01      0.00       0.00      0.00     0.92           0.01           0.00        0.00              0.00     0.00            0.0        0.00       0.07
car           0.11         0.25      0.00       0.02      0.01     0.02           0.26           0.02        0.00              0.02     0.00            0.0        0.22       0.06
cityscape     0.00         0.09      0.00       0.00      0.27     0.00           0.12           0.47        0.01              0.00     0.00            0.0        0.00       0.02
fire          0.00         0.00      0.98       0.00      0.00     0.00           0.00           0.00        0.00              0.00     0.00            0.0        0.00       0.01
person        0.01         0.38      0.00       0.07      0.08     0.02           0.20           0.00        0.01              0.02     0.00            0.0        0.01       0.19
eagle         0.00         0.00      0.00       0.00      0.00     0.00           0.00           0.00        0.00              0.00     0.00            0.0        0.00       1.00
bike          0.48         0.00      0.00       0.02      0.50     0.00           0.00           0.00        0.00              0.00     0.00            0.0        0.00       0.00
pineapple     0.00         0.00      0.00       0.00      0.00     0.00           0.00           0.00        0.00              0.00     0.00            1.0        0.00       0.00
```




## 技术讨论

- Github issues
- QQ 群: 139953715