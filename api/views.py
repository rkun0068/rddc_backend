from datetime import timedelta

from django.http import JsonResponse, HttpResponse
from minio import Minio
from minio.error import S3Error
import config
from django.http import FileResponse
import google.generativeai as genai
import requests

minio_cli = Minio(
    config.MINIO_ADDRESS_PORT,
    access_key=config.MINIO_ACCESS_KEY,
    secret_key=config.MINIO_SECRET_KEY,
    secure=False

)

genai.configure(api_key=config.GEMINI_API_KEY)


def upload_file(request):
    try:
        bucket_name = config.MINIO_BUCKET_NAME
        remove_all_objects(minio_cli, bucket_name=bucket_name)

        for file in request.FILES.getlist('file'):
            filename = file.name

            # 将每个文件上传到 MinIO 存储桶中
            minio_cli.put_object(bucket_name, filename, file, file.size)

        # 返回成功的响应
        return JsonResponse({"status": 200, "msg": "文件被成功上传"})
    except S3Error as e:
        return JsonResponse({"status": 500, "msg": str(e)})


def remove_all_objects(minio_client, bucket_name):
    try:
        # 列出存储桶中的所有对象
        objects = minio_client.list_objects(bucket_name, recursive=True)

        # 删除每个对象
        for obj in objects:
            minio_client.remove_object(bucket_name, obj.object_name)

        print(f"All objects in bucket {bucket_name} removed successfully.")
    except S3Error as e:
        print(f"Error: {e}")


"""
删除存储桶里所有数据
"""


def delete_files(request):
    try:
        remove_all_objects(minio_cli, config.MINIO_BUCKET_NAME)
        return JsonResponse({"status": 200, "msg": "存储桶内容已被删除"})
    except Exception as e:
        return JsonResponse({"status": 500, "msg": str(e)})


def get_image(request):
    try:
        objects = minio_cli.list_objects(config.MINIO_BUCKET_NAME, recursive=True)
        image_items = []
        for obj in objects:
            # Generate a direct link to the image file
            img_url = f"http://localhost:9000/{config.MINIO_BUCKET_NAME}/{obj.object_name}"
            image_items.append({
                "img": img_url,
                "title": obj.object_name
            })

        return JsonResponse({"code": 200, "msg": image_items})
    except S3Error as e:
        return JsonResponse({"code": 500, "msg": str(e)})


"""
获取视频URL
"""


def get_video_url(request):
    try:
        objects = minio_cli.list_objects(config.MINIO_BUCKET_NAME, recursive=True)

        # Get the first object
        first_object = next(objects, None)

        if first_object:
            # Construct the file URL
            file_url = f"http://localhost:9000/{config.MINIO_BUCKET_NAME}/{first_object.object_name}"

            # Generate a presigned URL for the first object (expires in 3600 seconds)
            expires = timedelta(seconds=3600)
            presigned_url = minio_cli.presigned_get_object(
                config.MINIO_BUCKET_NAME,
                first_object.object_name,
                expires=expires,
            )

            # Construct the response data with file name, URL, and presigned URL
            response_data = {
                "code": 200,
                "msg": "Success",
                "file_name": first_object.object_name,
                "file_url": file_url,
                "presigned_url": presigned_url,
            }

            # Set CORS headers to allow cross-origin requests (adjust origins accordingly)
            response = JsonResponse(response_data)
            response['Access-Control-Allow-Origin'] = '*'  # Adjust origin based on your needs
            response['Access-Control-Allow-Methods'] = 'GET'

            return response

        else:
            response_data = {"code": 404, "msg": "No files found in the bucket"}
            return JsonResponse(response_data)

    except S3Error as e:
        return JsonResponse({"code": 500, "msg": str(e)})
