from django.http import JsonResponse
from minio import Minio
from minio.error import S3Error
from ultralytics import YOLO
from io import BytesIO
from PIL import Image
import os
import shutil
import cv2
import config
from road_detection import settings
from model.models import DetectionResult
from model.serializers import DetectionResultSerializer

minio_cli = Minio(
    config.MINIO_ADDRESS_PORT,
    access_key=config.MINIO_ACCESS_KEY,
    secret_key=config.MINIO_SECRET_KEY,
    secure=False

)


def detect_and_save_images(request):
    try:
        DetectionResult.objects.all().delete()
        # 模型路径
        model_path = "newModel.pt"
        # 临时目录
        temp_dir = os.path.join(settings.BASE_DIR, 'temp')

        model_absolute_path = os.path.join(settings.BASE_DIR, model_path)

        # 模型使用
        model = YOLO(model_absolute_path)

        # 列出存储桶中的所有对象
        objects = minio_cli.list_objects(config.MINIO_BUCKET_NAME, recursive=True)

        # 确保临时目录存在
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        # detection_json = []
        for obj in objects:
            file_data = minio_cli.get_object(config.MINIO_BUCKET_NAME, obj.object_name)
            image_data = BytesIO(file_data.read())
            image = Image.open(image_data)

            # 保存到临时目录
            temp_image_path = os.path.join(temp_dir, obj.object_name)
            image.save(temp_image_path)

            # 进行预测
            results = model(temp_image_path)
            for r in results:
                im_array = r.plot()  # 绘制包含预测结果的BGR numpy数组
                im = Image.fromarray(im_array[..., ::-1])  # RGB PIL图像
                im.save(os.path.join(temp_dir, obj.object_name))  # 保存图像
                detection_res = r.tojson()

            # 将检测结果上传到存储桶
            minio_cli.fput_object(config.MINIO_BUCKET_NAME, obj.object_name,
                                  os.path.join(temp_dir, obj.object_name))

            # 获取预签名URL
            presigned_url = minio_cli.presigned_get_object(config.MINIO_BUCKET_NAME, obj.object_name,
                                                           )

            # 创建检测结果数据放入表中
            DetectionResult.objects.create(
                img_url=presigned_url,
                result=detection_res
            )

        return JsonResponse({"status": 200, "message": "预测结果保存成功"})
        # except S3Error as e:
        return JsonResponse({"status": 500, "message": str(e)})
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)


"""
对视频进行检测
"""


def detect_and_save_video(request):
    try:
        """
        清空数据库
        """
        DetectionResult.objects.all().delete()

        # 模型路径
        model_path = "newModel.pt"
        model_absolute_path = os.path.join(settings.BASE_DIR, model_path)

        # 模型使用
        model = YOLO(model_absolute_path)

        # 临时目录
        temp_dir = os.path.join(settings.BASE_DIR, 'temp')

        # 确保临时目录存在
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # 列出存储桶中的所有对象
        objects = minio_cli.list_objects(config.MINIO_BUCKET_NAME, recursive=True)

        for obj in objects:
            file_data = minio_cli.get_object(config.MINIO_BUCKET_NAME, obj.object_name)
            video_data = BytesIO(file_data.read())

            # 保存视频数据到临时目录
            temp_video_path = os.path.join(temp_dir, obj.object_name + ".mp4")
            with open(temp_video_path, "wb") as temp_file:
                temp_file.write(video_data.getvalue())

            # 从临时目录读取数据
            cap = cv2.VideoCapture(temp_video_path)

            # 获取原始视频的帧速率、宽度和高度
            fps = cap.get(cv2.CAP_PROP_FPS)

            # 为处理后的视频创建VideoWriter对象
            out_path = os.path.join(temp_dir, f"processed_{obj.object_name}.mp4")
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'H264'), fps,
                                  (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # 使用模型执行目标检测
                results = model(frame, stream=True)

                # 确保结果列表不为空
                if not results:
                    raise ValueError("视频未捕获到任何帧.")

                for r in results:
                    im_array = r.plot()  # 带有检测结果的BGR numpy数组
                    out.write(im_array)

            cap.release()
            out.release()

            # 将处理后的视频上传到存储桶
            processed_video_name = f"processed_{obj.object_name}.mp4"
            minio_cli.fput_object(config.MINIO_BUCKET_NAME, processed_video_name, out_path, content_type='video/mp4')

            # 移除源视频
            minio_cli.remove_object(config.MINIO_BUCKET_NAME, obj.object_name)

        return JsonResponse({"status": 200, "message": "视频处理结果保存成功"})
    except S3Error as e:
        return JsonResponse({"status": 500, "message": str(e)})
    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)})
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)


"""
获取检测结果信息
"""


def get_detection_info(request):
    try:
        detection_res = DetectionResult.objects.all()
        serializer = DetectionResultSerializer(detection_res, many=True)
        return JsonResponse({"status": 200, "message": "获取数据成功", "data": serializer.data})

    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)})


def realtime_detect(request):
    try:
        # 模型路径
        model_path = "newModel.pt"
        model_absolute_path = os.path.join(settings.BASE_DIR, model_path)

        # 模型使用
        model = YOLO(model_absolute_path)

        # Create a video capture object for the computer's webcam (camera index 0)
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLOv8 inference on the frame
                results = model(frame)

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Display the annotated frame
                cv2.imshow("RRD  click q to exit", annotated_frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Break the loop if the end of the video is reached
                break

        # Release the video capture object and close the display window
        cap.release()
        cv2.destroyAllWindows()

        return JsonResponse({"status": 200, "message": "检测完成"})

    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)})
