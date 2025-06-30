from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
from PIL import Image


config = Cfg.load_config_from_name('vgg_transformer')
config['device'] = 'cpu'

config['weights'] = 'weights/vgg_transformer.pth' # Đường dẫn đến file trọng số local
#config['weights'] = 'https://vocr.vn/data/vietocr/vgg_transformer.pth'#

#
detector = Predictor(config)


img_path = 'image.jpg' 
img = Image.open(img_path)


s = detector.predict(img)
print(s)