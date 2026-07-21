from PIL import Image
from utils.resources import resource_path

caminho = resource_path("assets/bot_eorder.png")

print(caminho)
print(caminho.exists())

img = Image.open(caminho)

print(img.size)

img.show()