=================
django-sendcloud2
=================

提供django下sendcloud接口,支持python2/3，支持replyto

Quick start
-----------
1. Install::

    pip install django_sendcloud2


2. 配置，在settings.py中

```
EMAIL_BACKEND = 'sendcloud.SendCloudBackend'
SENDCLOUD_API_USER = '***'
SENDCLOUD_API_KEY = '***'
```

3. 按照正常django方式发送邮件即可
