# 任务要求

**1. 熟悉FastAPI的用法**


**2. 完成对图片的文字识别服务，并通过FastAPI以REST服务的方式对外提供**
具体要求：
- 通过POST方式上传图片到FastAPI
- FastAPI程序根据上传图片，调用PaddlePaddleOCR库识别文字
- 调用Shapely库对识别文字的矩形区域进行归并，把距离近的矩形合并到一起，拟采用HDBSCAN算法
- 把相邻文字整合到一段通过langchain，调用访问openai，提取要点（提词有参考）
- 因为识别、访问openai的时间比较长，为不影响服务，采用create_task，get_result的方法


**3. 测试pic目录下所有图片的识别结果**

【参考与致谢】
 - [Trickle的分析](https://github.com/PromptExpert/Trickle-On-WeChat/)