SimpleUpload
=============

A HTTP Server for upload file.

安装
----

.. code-block::

    pip install SimpleUpload


配置文件
--------

使用环境变量指定配置文件的位置::

    export SIMPLE_UPLOAD_SETTINGS="{path}/simple_upload.cfg"


配置项
-------

==============  =====================================================
RANDOM_KEY      配置随机字符串，对应着提交的r字段，用于防止非法访问
CLIENT_PREFIX   本地文件路径的前缀
SERVER_PREFIX   服务器文件路径的前缀
==============  =====================================================

运行
----

可以使用unicorn运行，安装unicorn::

    pip install unicorn

启动::

    gunicorn -b :8000 http_upload.server:app


上传文件
--------

以HTTPie为例::

    http -f POST yldev.lankaifa.com:8000 r={your random string} path={local path} f@{local_path}

Virtual Studio Code
--------------------

可以结合vscode的插件Run on Save 或者Save and Run达到自动上传的目的

vscode的Save And Run插件的一个配置示例::

    "saveAndRun": {
        "commands": [
            {
                "match": "^/home/ubuntu/",
                "cmd": "http -f POST ip:port r=r参数 path=${file} f@${file}"
            }
        ]
    }
