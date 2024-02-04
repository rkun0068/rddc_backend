`前端：`  [https://github.com/rkun0068/rddc_frontend](https://github.com/rkun0068/rddc_frontend)
`后端：`  [https://github.com/rkun0068/rddc_backend](https://github.com/rkun0068/rddc_backend)
## 系统架构
![](https://cdn.nlark.com/yuque/0/2024/jpeg/29558585/1706890929722-94bcc9ca-99e8-443c-a9e8-c1a4aed43a98.jpeg)

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29558585/1706945978439-dc016228-8ff9-4cad-a1db-fab81c02d78e.jpeg)

## Docker部署minio对象存储
```bash
$ mkdir -p ~/minio/data

$ docker pull minio/minio

$ docker run \
   -p 9000:9000 \
   -p 9001:9001 \
   --name minio1 \
   -v ~/minio/data:/data \
   -e "MINIO_ROOT_USER=minioadmin" \
   -e "MINIO_ROOT_PASSWORD=minioadmin" \
   minio/minio server /data --console-address ":9001"
```
访问服务[http://127.0.0.1:9001/](http://127.0.0.1:9001/) 创建存储桶 `stroage`

## Docker部署Mysql数据库服务
```bash
$ docker pull mysql
$ docker run -d --name mysql-container -e MYSQL_ROOT_PASSWORD=your_password -p 3306:3306 mysql

```
然后使用Mysql创建数据库`road_detection`
创建数据表
```sql
-- road_detection.detection_result definition

CREATE TABLE `detection_result` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img_url` text,
  `result` text,
  `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```


## 实现功能
### 图片上传/检测

- 点击上传单个或多个图像

![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890105829-a26c7d50-0072-45d4-b2cf-ddb8557d1ead.png#averageHue=%23f6f6f5&clientId=u2109a791-c26b-4&from=paste&height=912&id=ucea8449a&originHeight=1140&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=287091&status=done&style=none&taskId=u58be5a45-c004-458f-b436-746deb6cceb&title=&width=1536)
![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890131384-5b115c67-977d-4cba-b408-bd4916b4134d.png#averageHue=%23fdfdfd&clientId=u2109a791-c26b-4&from=paste&height=838&id=u66591f10&originHeight=1048&originWidth=1860&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=56690&status=done&style=none&taskId=u031dd087-c30e-4af6-bfec-48e493a5358&title=&width=1488)
![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890147531-d279135a-450e-4c7a-8524-2a6663856508.png#averageHue=%23fdfdfd&clientId=u2109a791-c26b-4&from=paste&height=838&id=u550b42aa&originHeight=1048&originWidth=1860&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=40889&status=done&style=none&taskId=uc485e598-0c14-4425-970e-d9ab1d9e894&title=&width=1488)

- 上传的图片会被存储在MinIO提供的对象存储桶里

![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890256141-b3d0d9d6-0c99-4a06-b0f9-b89153f6f8dc.png#averageHue=%23fcfcfc&clientId=u2109a791-c26b-4&from=paste&height=838&id=u7671aa4e&originHeight=1048&originWidth=1860&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=363130&status=done&style=none&taskId=ubf39662b-0e69-4628-ab88-22d4a02a862&title=&width=1488)

- 点击检测，后端利用模型进行检测并生成新图片替换掉源图片

![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890363854-bc41473a-0ed2-4377-9cd6-d6e785a381fb.png#averageHue=%23fdfdfd&clientId=u2109a791-c26b-4&from=paste&height=838&id=ub2b89751&originHeight=1048&originWidth=1860&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=37609&status=done&style=none&taskId=uee4b56ff-75d5-495b-b9db-a4549c2dab2&title=&width=1488)

- 处理完成后会跳转到数据展示页面

![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890413780-287ec286-7e7e-49e0-851c-eee3ecd384c7.png#averageHue=%23f3f2f1&clientId=u2109a791-c26b-4&from=paste&height=838&id=ua0aff2bc&originHeight=1048&originWidth=1860&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=981567&status=done&style=none&taskId=u972adbbd-a615-4447-bc91-46e657c7b1d&title=&width=1488)

### 历史数据查看

- 可以查看每次检测的图片数据，使用JSON格式化展示

![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890512779-34324635-1e64-4795-a853-8ab7c32599e6.png#averageHue=%23fbfafa&clientId=u2109a791-c26b-4&from=paste&height=838&id=u128c3688&originHeight=1048&originWidth=1860&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=273467&status=done&style=none&taskId=u2aee239a-77cd-4c36-940b-3c3bdb78009&title=&width=1488)

### 视频上传/检测

- 点击直接上传视频

![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890659561-6ff43fd4-68df-4ea4-ac0a-5effb0b28d03.png#averageHue=%23f9f8f8&clientId=uc2c568f7-669b-4&from=paste&height=866&id=u555ff2c0&originHeight=1082&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=138178&status=done&style=none&taskId=u42f6fabd-8fba-4ee2-8667-907a69634e5&title=&width=1536)
![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890684568-66c7b12b-c6e8-4479-8992-3d60c5a0b163.png#averageHue=%23fcfcfc&clientId=uc2c568f7-669b-4&from=paste&height=838&id=u33df5066&originHeight=1048&originWidth=1860&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=44440&status=done&style=none&taskId=ubdb30ae4-e27e-45d7-97c9-756096d5d16&title=&width=1488)

- 点击检测进行检测，检测完成后会自动跳转到检测视频播放页面

![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890731358-a3c4c24e-4450-4be3-9793-b4a7d8e61ca2.png#averageHue=%23fdfdfd&clientId=uc2c568f7-669b-4&from=paste&height=838&id=ucb338330&originHeight=1048&originWidth=1860&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=39175&status=done&style=none&taskId=u5949fa06-dcd6-44b3-b594-16a31912f82&title=&width=1488)
![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1706890817420-6f63b401-165c-4862-8692-f4ebffba9343.png#averageHue=%23a3a8a1&clientId=uc2c568f7-669b-4&from=paste&height=838&id=u304e4457&originHeight=1048&originWidth=1860&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=2419178&status=done&style=none&taskId=u3a960754-0694-4757-b65b-20232b0c663&title=&width=1488)
### 实时检测

- 使用电脑摄像头，按Q进行退出

![image.png](https://cdn.nlark.com/yuque/0/2024/png/29558585/1707049078023-cf86c40f-8330-4ef8-8852-54c1ace2ba59.png#averageHue=%23754f3a&clientId=uccde196e-07d3-4&from=paste&height=838&id=ubc9bb81b&originHeight=1048&originWidth=1865&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=610848&status=done&style=none&taskId=u5c405604-c796-4ddf-871c-c512cc2c0bf&title=&width=1492)
## 

## 相关代码信息
`后端`
```basic
|-- __pycache__   # Python 编译缓存文件目录，包含已编译的 Python 文件
|-- api           # Django APP
|-- config.py     # 外部资源配置信息 （mysql,minio)等
|-- manage.py     # Django 项目管理脚本，用于执行不同的 Django 命令
|-- model         # Django APP
|-- newModel.pt   # 训练好的道路病害检测模型 （可替换为其他）
|-- requirements.txt  # 项目的依赖文件，包含项目所需的 Python 包及其版本信息
|-- road_detection    # Django 项目的主目录，包含项目的设置和配置等文件
```

### 启动后端
```bash
python -m venv venv        
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py runserver
```


### 启动前端
```bash
npm install
npm run dev
```



