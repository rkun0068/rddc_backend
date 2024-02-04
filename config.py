"""
MINIO配置信息
"""
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_ADDRESS_PORT = "localhost:9000"
MINIO_BUCKET_NAME = "storage"

"""
Gemini API_KEY
"""

GEMINI_API_KEY = "AIzaSyC_6hUHEX6KhhaBnOY7tR3zLa8l_qmYfLc"

"""
MYSQL 配置信息
"""
MYSQL_USER = "root"
MYSQL_PASSWD = "mysql12345"
MYSQL_DB = "road_detection"
MYSQL_PORT = 3306
MYSQL_IP_ADDRESS = "127.0.0.1"

MYSQL_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWD,
        'HOST': MYSQL_IP_ADDRESS,
        'PORT': MYSQL_PORT,
        'OPTIONS': {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# 纵向裂缝、横向裂缝、鳄鱼裂缝和坑洼