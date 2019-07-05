from PIL import Image
str1 = "F:/proj/data/5-11/img/"
str2 = ".jpg"
for i in range(1, 103):
    str3 = str1 + str(i) + str2
    image = Image.open(str3)
    print(image.mode)                       # RGB
    new_image = image.convert('L')          # 黑白8位
    # new_image = image.convert('P')        # 彩色8位
    print(new_image.mode)
    print(image.size, new_image.size)
    print(image.getpixel((0, 0)))
    print(image.getpixel((10, 120)))
    print(new_image.getpixel((0, 0)))
    print(new_image.getpixel((10, 120)))
    new_image.save(str3)
