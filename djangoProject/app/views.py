from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import PictureStore as ps1
import os
import pytesseract
import datetime
import logging


# Create your views here.

#
# 日志记录
logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    filename='runtime.log',
                    filemode='a')
logger = logging.getLogger(__name__)


class UploadPicture(APIView):
    authentication_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.path.exists('/photos/'):
            pass
        else:
            os.mkdir('/photos/')

    def post(self, request, *args, **kwargs):
        res = {'content': [], 'msg': 'success', 'code': 200}
        file = request.FILES.getlist('img')
        for img in file:
            # 给图片名称添加时间戳防重名
            time = datetime.datetime.now()
            dt = str(time.date())+str(time.time().hour)+str(time.time().minute)+str(time.time().second)
            new_name = img.name.split('.')[0] + dt + '.' + img.name.split('.')[1]
            img.name = new_name
            # 将图片和识别码存入数据库
            try:
                ps1.objects.create(picture_path=img)
            except Exception as e:
                logger.error(e)
                res['code'] = 500
                res['msg'] = 'there was an error when creating the record!'
                return Response(res)
            # 识别图中识别码
            pwd = os.getcwd()
            img_path = pwd + '/photos/' + new_name
            im = Image.open(img_path)
            character = pytesseract.image_to_string(im, lang='chi_sim')
            s = ''
            for i in character:
                s += i
            res['content'].append(s)
            # 修改数据库识别码
            try:
                code_change = ps1.objects.get(picture_path='photos/' + img.name)
                code_change.translate_code = s
                code_change.save()
            except Exception as e:
                logger.error(e)
                res['code'] = 500
                res['msg'] = 'there was an error when rewrite the record!'
                return Response(res)
        logger.info('operation success!')
        return Response(res)
