from selenium import webdriver
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
#创建一个空的图片文件
def get_snap(driver):
    driver.save_screenshot('snap.png')
    snap_obj = Image.open('snap.png')
    return snap_obj
    pass

#通过xpath找到元素
def get_image(driver):
    img_element = driver.find_element_by_xpath('//div[@class="geetest_panel_next"]//canvas[@class="geetest_canvas_slice geetest_absolute"]')
    #获得图片的大小和位置
    size = img_element.size
    location = img_element.location
    left = location['x']
    top = location['y']
    right = left +size['width']
    bottom = top + size['height']
    snap_obj = get_snap(driver)
    #注意该参数是元祖
    img_obj = snap_obj.crop((left,top,right,bottom))
    return img_obj

def get_distance(img1,img2):
    start_x = 60
    threhold = 60#阈值
    for x in range(start_x,img1.size[0]):
        for y in range(img1.size[1]):
            rgb1 = img1.load()[x,y]
            rgb2 = img2.load()[x,y]
            res1 = abs(rgb1[0]-rgb2[0])
            res2 = abs(rgb1[1]-rgb2[1])
            res3 = abs(rgb1[2]-rgb2[2])
            if not (res1<threhold and res2<threhold and res3<threhold):
                return x-7   #测试后-7可以提高成功率
    pass

def get_tracks(distance):
    #distance为上一步得出的总距离。20是等会要回退的像素
    distance += 20
    #初速度为0，s是已经走的鹿城，t是时间
    v0 = 2
    s = 0
    t = 0.4
    #mid是进行减速的鹿城
    mid = distance*3/5
    #存放走的距离
    forward_tracks = []
    while s<distance:
        if s<mid:
            a=2
        else:
            a=-3
        v = v0
        tance = v*t+0.5*a*(t**2)
        tance = round(tance)
        s+=tance
        v0=v+a*t
        forward_tracks.append(tance)
    #因为回退20像素，所以可以手动打出，只要和为20即可
    back_tancks = [-1,-1,-1,-2,-2,-2,-3,-3,-2,-2,-1]
    return {"forward_tracks":forward_tracks,'back_tracks':back_tancks}

driver = webdriver.Chrome()
driver.get('https://account.cnblogs.com/signin')
#隐式等待3秒
driver.implicitly_wait(3)
#找到用户名标签和密码标签，用ID查找
input_username = driver.find_element_by_id('LoginName')
input_password = driver.find_element_by_id('Password')
#输入用户名和密码
input_username.send_keys('cww9458')
time.sleep(1)
input_password.send_keys('cww945800..')
time.sleep(5)
#找到提交按钮
submitBtn = driver.find_element_by_id('submitBtn').click()
#点击提交
# submitBtn.click()
time.sleep(5)#等待验证码加载
none_img = get_image(driver)
driver.execute_script("var x=document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0];"
                          "x.style.display='block';"
                          "x.style.opacity=1")
block_img = get_image(driver)
geetest_slider_button = driver.find_element_by_class_name('geetest_slider_button')
distance = get_distance(block_img,none_img) #
tracks_dic = get_tracks(distance)
ActionChains(driver).click_and_hold(geetest_slider_button).perform()
forword_tracks = tracks_dic['forward_tracks']
back_tracks = tracks_dic['back_tracks']
for forword_tracks in forword_tracks:
    ActionChains(driver).move_by_offset(xoffset=forword_tracks,yoffset=0).perform()
time.sleep(0.2)
for back_tracks in back_tracks:
    ActionChains(driver).move_by_offset(xoffset=back_tracks,yoffset=0).perform()
print(forword_tracks)
ActionChains(driver).move_by_offset(xoffset=-3,yoffset=0).perform()
ActionChains(driver).move_by_offset(xoffset=3,yoffset=0).perform()
time.sleep(0.3)
ActionChains(driver).release().perform()
time.sleep(10)
driver.close()