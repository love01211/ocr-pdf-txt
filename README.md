# 
目前有很多开源多模态模型和视觉模型，可以做ocr识别，真实体验下来，模型需要消耗一定的gpu资源，而且效果不稳定，就和同事一起基于PaddleOCR搞了一个简单的小脚本。
## 安装虚拟环境
```bash
conda create -n PaddleOCR python==3.10
```
## 安装包
```bash
pip install -r requirements.txt
```
## 使用命令查看效果
```bash
conda activate PaddleOCR
python ocr_conv_txt.py <pdfname.pdf>
```
## 启动前端页面
```bash
conda activate PaddleOCR
python app_fastapi.py
```
## 效果图
![image](https://github.com/user-attachments/assets/098b2b6e-30b2-43c7-b3f4-72cdd397dddf)
