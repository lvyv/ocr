# 快速开始

1. 在python3.10环境下，项目的根目录执行如下命令安装依赖包。
   
   ```shell
   pip install -r requirements.txt
   ```

2. 确保test目录下的配置文件配置正确。
   
   进入test目录运行如下命令启动服务。
   
   【windows环境】
   
   ```shell
   cd test
   set PYTHONPATH=..\src
   python test_scheduler.py
   ```
   
   【linux环境】
   
   ```shell
   cd test
   export PYTHONPATH=../src
   python test_scheduler.py
   ```

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
- [并发](https://fastapi.tiangolo.com/async/)