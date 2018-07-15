# coding=utf-8
import os
import subprocess
from PIL import Image,ImageDraw


def image_to_string(img, cleanup=True, plus=''):#为Tesseract实现一个Python接口
    # 因为Pytesser从2007年起就没有再更新过，不宜使用。因此这里使用C++版Tesseract并手动实现接口
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    subprocess.check_output('tesseract ' + img + ' ' +
                            img + ' ' + plus, shell=True)  # 生成同名txt文件
    text = ''
    with open(img + '.txt', 'r') as f:
        text = f.read().strip()
    if cleanup:
        os.remove(img + '.txt')
    return text


def getPixel(image, x, y, G, N):
    L = image.getpixel((x, y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x, y - 1))
    else:
        return None

    # 降噪


# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image, G, N, Z):
    draw = ImageDraw.Draw(image)

    for i in range(0, Z):
        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                color = getPixel(image, x, y, G, N)
                if color != None:
                    draw.point((x, y), color)


print(image_to_string('./a.png', False, '-l eng'))
print(image_to_string('./b.png', False, '-l eng'))
print(image_to_string('./c.png', False, '-l eng'))
#print(image_to_string('./Image.png', False, '-l eng'))
def parse_captcha(filename):
    image = Image.open(filename)
    imgry = image.convert('L')  # 转化为灰度图
    imgry.save('ry.png')
    threshold=160#二值化阈值，低于这个值的填白色，高于的填黑色
    table=[]
    for j in range(256):#二值化填充操作
        if j<threshold:
            table.append(0)
        else:
            table.append(1)
    bim=imgry.point(table,'1')
    bim.save('erzhi.png')#保存二值化之后的图片
    image=Image.open('erzhi.png')
    clearNoise(image,160,1,1)#图片引用，二值化阈值，降噪率，降噪次数
    #这里使用的是8邻域降噪算法
    image.save('jiangzao.png')

    str=(image_to_string('./jiangzao.png', False, '-l eng'))
    i=0
    result=""
    #print ("****"+str)
    while i<len(str):

        if str[i].isalpha() or str[i].isdigit() or str[i]=='/':
           # print("******"+str[i])
            if str[i] == 'n':#因为M字的尖部有噪点时会被误认为M，而这个网站的验证码里并没有n这个字符
                result= result+'M'
            elif str[i] == '/':#因为“7”的横线部分会被去噪算法误杀，而这个网站的验证码里没有/这个字符
                result=result+'7'
            elif str[i]=='l':#这个网站的验证码里没有小写字母。实测发现l多数情况下是M
                if str[i+2]=='l':
                    result=result+'M'
                    i=i+2
                else:
                    result=result+'M'
            elif str[i]=='y':#这个网站的验证码里没有小写字母。实测发现y多数情况下是多余字符。
                result=result+''
            elif str[i]=='b':#这个网站的验证码里没有小写字母，实测发现b多数情况下是E
                result=result+'E'
            elif str[i]=='e':#这个网站的验证码里没有小写字母，实测发现e多数情况下是6
                result=result+'6'

            else:
                result=result+str[i]

        i=i+1

    print(result)

#parse_captcha('./image.php.png')
p=1
while p<=7:
    try:
        parse_captcha('./imag'+str(p)+'.png')
    except:
        print ("第"+str(p)+"张图片识别失败")
    p=p+1
'''
pic=1
while pic<15:
    parse_captcha('./image'+str(pic)+'.jpg')  

'''