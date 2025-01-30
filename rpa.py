from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from bs4 import BeautifulSoup
import time
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
import os
import shutil
import urllib.parse

# สร้าง WebDriver
driver = webdriver.Chrome()  # หรือ WebDriver ที่ใช้งาน
output_dir = "download_images"
os.makedirs(output_dir, exist_ok=True)

# driver = webdriver.Edge()


# ใช้งาน WebDriver
driver.get("https://pm-rsm.cpretailink.co.th/login")


class RPA:
    def __init__(self, url):
        self.url = url

    def getURL(self, window):
        chrome_options = webdriver.ChromeOptions()
        if window:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        else:
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(self.url)  
        return driver
    
    def getpageScript(self, driver):
        return driver.page_source

    def getList(self, script_contents, split, filter):
        hope = []
        script_contents = str(script_contents)

        #split = str(script_contents).split('"')
        # 'app-images'
        split = str(script_contents).split(split)
        for i in split:
            if filter in i:
                i = i.replace("<div _ngcontent", "")
                i = i.replace(">", "")
                i = i.replace(" ", "", 1)
                hope.append(i)
        return hope
    
    def initialize(self, driver, date, month, year):
        ## element ของ fill text username และ password
        username =  driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="username"]')
        password =  driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
        
        ## กรอก username และ password
        username.send_keys('benjaponsuns')
        password.send_keys('Benjapon@0125')
        
        ## กดปุ่ม enter เพื่อ login
        password.send_keys(Keys.RETURN)

        time.sleep(2)

        ## element ของปุ่ม "เดือนที่เปิดงาน"
        date_select =  driver.find_element(By.XPATH, "/html/body/app-root/app-plan-search/div/div/div[2]/app-search-pm-box/div/form/div[1]/div[2]/mat-form-field/div[1]/div[2]/div[1]/input")
        ## กดปุ่ม "เดือนที่เปิดงาน"
        date_select.click()

        time.sleep(2)
       
        if year == 2024:
            ## element ของปุ่ม "2024"
            year2024_select =  driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-multi-year-view/table/tbody/tr[6]/td[4]/button')
            ## กดปุ่ม "2024"
            year2024_select.click()
        else:
            ## element ของปุ่ม "2023"
            year2024_select =  driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-multi-year-view/table/tbody/tr[6]/td[3]/button')
            ## กดปุ่ม "2023"
            year2024_select.click()
        
        time.sleep(2)

        month_table = {'January': [2,1], 'February': [2,2], 'March': [2,3], 'April': [2,4], 'May': [3,1], 'June': [3,2], 'July': [3,3], 'August': [3,4], 'September': [4,1], 'October': [4,2], 'November': [4,3], 'December': [4,4]}
        month_table = {1: [2,1], 2: [2,2], 3: [2,3], 4: [2,4], 5: [3,1], 6: [3,2], 7: [3,3], 8: [3,4], 9: [4,1], 10: [4,2], 11: [4,3], 12: [4,4]}
        ## element ของปุ่ม "month"
        JUN_select =  driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-year-view/table/tbody/tr[{month_table[month][0]}]/td[{month_table[month][1]}]/button')
        ## กดปุ่ม "month"
        JUN_select.click()

        time.sleep(2)

        ## เช็ค element ของปุ่ม "ทั้งหมด"
        all_Button = driver.find_element(By.ID, 'mat-button-toggle-7-button') 
        ## กดปุ่ม "ทั้งหมด"
        all_Button.click()
        
        time.sleep(2)

        ## element ของปุ่ม "โปรดเลือกบริษัท"
        cop_Button = driver.find_element(By.CSS_SELECTOR, 'input.form-control[placeholder="โปรดเลือก"]')
        ## กดปุ่ม "โปรดเลือกบริษัท"
        cop_Button.click()

        time.sleep(2)

        ## element ของ multi selected "เลือกบริษัท"
        cop_Button = driver.find_element(By.CSS_SELECTOR, 'angular2-multiselect.ng-untouched.ng-pristine.ng-valid')
        ## กด multi selected "เลือกบริษัท"
        cop_Button.click()
        
        time.sleep(2)

        ## หา element ของ "Seven Eleven"
        seven11_element = driver.find_element(By.XPATH, '//li[label[text()="Seven Eleven"]]/label')
        ## กดปุ่ม "Seven Eleven"
        seven11_element.click()

        time.sleep(2)

        ## element ของปุ่ม "เสร็จสิ้น"
        finish_Button = driver.find_element(By.XPATH, '//button[contains(text(), "เสร็จสิ้น")]')
        ## กดปุ่ม "เสร็จสิ้น"
        finish_Button.click()

        time.sleep(3)

        ## element ของปุ่ม "ประเภทสัญญา"
        contract_Button = driver.find_element(By.XPATH, '/html/body/app-root/app-plan-search/div/div/div[2]/app-search-pm-box/div/form/div[4]/div[2]/app-multi-search-box/div/input')
        ## กดปุ่ม "ประเภทสัญญา"
        contract_Button.click()

        time.sleep(2)

        ## element ของ multi selected "เลือกสัญญา"
        selectcont_Button = driver.find_element(By.CSS_SELECTOR, 'angular2-multiselect.ng-untouched.ng-pristine.ng-valid')
        ## กด multi selected "เลือกสัญญา"
        selectcont_Button.click()

        time.sleep(2)
        
        ## หา element ของ "สัญญาล้างถัง PP 3 เดือน"
        PPtank_element = driver.find_element(By.XPATH, '//li[label[text()="สัญญาล้างถัง PP 3 เดือน"]]/label')
        ## กดปุ่ม "สัญญาล้างถัง PP 3 เดือน"
        PPtank_element.click()

        time.sleep(2)

        ## element ของปุ่ม "เสร็จสิ้น"
        finish_Button = driver.find_element(By.XPATH, '//button[contains(text(), "เสร็จสิ้น")]')
        ## กดปุ่ม "เสร็จสิ้น"
        finish_Button.click()

        time.sleep(2)

        ## element ของปุ่ม "ค้นหา"
        search_Button = driver.find_element(By.XPATH, '//button[contains(text(), "ค้นหา")]')
        ## กดปุ่ม "ค้นหา"
        search_Button.click()
        time.sleep(5)
        pan_table = driver.find_element(By.XPATH, '/html/body/app-root/app-e-service-plan/div/full-calendar/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[1]/td[4]/div/div[2]/div[1]/a')


        pan_table.click()
        time.sleep(2)

        # สร้างเซ็ตสำหรับเก็บ URL ของไฟล์ที่ดาวน์โหลดแล้ว
        downloaded_urls = set() 

        # กำหนดตัวนับเริ่มต้น
        # current_page = 1  # เริ่มต้นที่หน้าแรก
        max_pages = 10  # ตั้งค่าสูงสุดของหน้า (ปรับได้ตามจำนวนหน้าจริง)

        while True:
            try:
                current_page = 1
                print(f"กำลังประมวลผลหน้า {current_page}...")

                # ตรวจสอบจำนวนหัวข้อในหน้านั้น
                total_rows = len(driver.find_elements(By.XPATH, '//app-table-contract/div/table/tbody/tr'))
                print(f"พบหัวข้อทั้งหมด {total_rows} รายการในหน้า {current_page}")

                if current_page == 1:
                    # ลูปผ่านแต่ละหัวข้อ (สูงสุด 10 หัวข้อ)
                    for row_index in range(1, min(total_rows, 10) + 1):
                        try:
                            topic_xpath = f'//app-table-contract/div/table/tbody/tr[{row_index}]/td[5]'
                            topic_link = driver.find_element(By.XPATH, topic_xpath)

                            # เลื่อนองค์ประกอบให้เห็นก่อนคลิก
                            driver.execute_script("arguments[0].scrollIntoView(true);", topic_link)
                            topic_link.click()
                            print(f"กำลังคลิกหัวข้อที่ {row_index} ในหน้า {current_page}")

                            time.sleep(2)  # รอหน้าโหลด

                            # ดึงรูปภาพในหัวข้อ
                            div_elements = driver.find_elements(By.XPATH, '/html/body/app-root/app-images/div/div')
                            image_idx = 1

                            for div_element in div_elements:
                                image_elements = div_element.find_elements(By.TAG_NAME, 'img')

                                for img in image_elements:
                                    image_url = img.get_attribute("src")
                                    if image_url.endswith(".svg"):
                                        print(f"ข้ามไฟล์ SVG: {image_url}")
                                        continue
                                    if image_url in downloaded_urls:
                                        print(f"ข้ามรูปที่เคยดาวน์โหลด: {image_url}")
                                        continue

                                    response = requests.get(image_url, stream=True)
                                    if response.status_code == 200:
                                        filename = os.path.join(output_dir, f"downloaded_image_page{current_page}_{row_index}_{image_idx}.jpg")
                                        with open(filename, 'wb') as file:
                                            for chunk in response.iter_content(1024):
                                                file.write(chunk)
                                        print(f"ดาวน์โหลดรูปภาพสำเร็จ: {filename}")
                                        downloaded_urls.add(image_url)
                                        image_idx += 1
                                    else:
                                        print(f"ไม่สามารถดาวน์โหลดรูปภาพจาก {image_url} ได้ (HTTP {response.status_code})")

                            # ย้อนกลับไปที่หน้าก่อนหน้านี้
                            driver.back()
                            time.sleep(2)

                        except Exception as e:
                            print(f"เกิดข้อผิดพลาดในหัวข้อที่ {row_index}: {e}")
                            continue
                elif current_page > 1:
                    next_button = driver.find_element(By.XPATH, '/html/body/app-root/app-e-service-table/div/mat-paginator/div/div/div[2]/button[3]')
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    if next_button.is_enabled():
                        next_button.click()
                        print(f"กดปุ่ม Next ครั้งที่ {_ + 1} สำหรับหน้า {current_page}")
                        time.sleep(3)  # รอให้หน้าถัดไปโหลด
                    else:
                        print("ไม่มีหน้าถัดไปแล้ว")
                        break

                    for row_index in range(1, min(total_rows, 10) + 1):
                        try:
                            topic_xpath = f'//app-table-contract/div/table/tbody/tr[{row_index}]/td[5]'
                            topic_link = driver.find_element(By.XPATH, topic_xpath)

                            # เลื่อนองค์ประกอบให้เห็นก่อนคลิก
                            driver.execute_script("arguments[0].scrollIntoView(true);", topic_link)
                            topic_link.click()
                            print(f"กำลังคลิกหัวข้อที่ {row_index} ในหน้า {current_page}")

                            time.sleep(2)  # รอหน้าโหลด

                            # ดึงรูปภาพในหัวข้อ
                            div_elements = driver.find_elements(By.XPATH, '/html/body/app-root/app-images/div/div')
                            image_idx = 1

                            for div_element in div_elements:
                                image_elements = div_element.find_elements(By.TAG_NAME, 'img')

                                for img in image_elements:
                                    image_url = img.get_attribute("src")
                                    if image_url.endswith(".svg"):
                                        print(f"ข้ามไฟล์ SVG: {image_url}")
                                        continue
                                    if image_url in downloaded_urls:
                                        print(f"ข้ามรูปที่เคยดาวน์โหลด: {image_url}")
                                        continue

                                    response = requests.get(image_url, stream=True)
                                    if response.status_code == 200:
                                        filename = os.path.join(output_dir, f"downloaded_image_page{current_page}_{row_index}_{image_idx}.jpg")
                                        with open(filename, 'wb') as file:
                                            for chunk in response.iter_content(1024):
                                                file.write(chunk)
                                        print(f"ดาวน์โหลดรูปภาพสำเร็จ: {filename}")
                                        downloaded_urls.add(image_url)
                                        image_idx += 1
                                    else:
                                        print(f"ไม่สามารถดาวน์โหลดรูปภาพจาก {image_url} ได้ (HTTP {response.status_code})")

                            # ย้อนกลับไปที่หน้าก่อนหน้านี้
                            driver.back()
                            time.sleep(2)

                        except Exception as e:
                            print(f"เกิดข้อผิดพลาดในหัวข้อที่ {row_index}: {e}")
                            continue

                # กดปุ่ม Next ตามจำนวนที่กำหนด
                for _ in range(current_page):
                    try:
                        next_button = driver.find_element(By.XPATH, '/html/body/app-root/app-e-service-table/div/mat-paginator/div/div/div[2]/button[3]')
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        if next_button.is_enabled():
                            next_button.click()
                            print(f"กดปุ่ม Next ครั้งที่ {_ + 1} สำหรับหน้า {current_page}")
                            time.sleep(3)  # รอให้หน้าถัดไปโหลด
                        else:
                            print("ไม่มีหน้าถัดไปแล้ว")
                            break
                    except Exception as e:
                        print(f"เกิดข้อผิดพลาดในการกดปุ่ม Next: {e}")
                        break

                # เพิ่มตัวนับเพื่อเปลี่ยนเป็นหน้าถัดไป
                current_page += 1

            except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")
                break

###### 
if __name__ == '__main__':
    login_url = 'https://pm-rsm.cpretailink.co.th/login'

    try:
        loginPage = RPA(login_url)
        driver = loginPage.getURL(window=True)
        # driver.set_window_size(500, 850)

        # zoom_level = "0.75"  # Zoom in to 150%
        # driver.execute_script(f"document.body.style.zoom='{zoom_level}'")
        
        # เลือกวัน
        day = 31
        # เลือกเดือน
        month = 1
        # เลือกปี
        year = 2025
        ## หน้า login --> หน้าตารางรวมแผนงาน
        date = loginPage.initialize(driver=driver,date=day, month=month, year=year)
        print(date)
        time.sleep(3)

        # สร้าง element ที่กำหนดจำนวน column
        choose_column = driver.find_element(By.XPATH, '/html/body/app-root/app-e-service-table/div/mat-paginator/div/div/div[1]/mat-form-field/div[1]/div/div[2]/mat-select')
        ## กดปุ่มที่กำหนดจำนวน column
        choose_column.click()
        time.sleep(3)
        
        # สร้าง element ที่กำหนดตารางเป็น 100 column 
        hundred_column = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/mat-option[4]')
        ## กดปุ่มที่กำหนดจำนวน column
        hundred_column.click()
        time.sleep(3)

        # หาจำนวนรูปภาพทั้งหมด
        ## print html script ของหน้านี้
        num_pic_link_contents = loginPage.getpageScript(driver=driver)
        print(f"get page script : {num_pic_link_contents}")
        # Specify the path to the file
        file_path = 'D:\\download\\webtext.txt'
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(str(num_pic_link_contents))
        num_pic_list = loginPage.getList(num_pic_link_contents,'"', ' of ')
        num_pic = num_pic_list[0].split(' ')[2]
        print(f"number of img : {num_pic}")
        
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(3)

        # row  column(pic button)
        # tr[1]/td[4]
        # path หน้าตารางแผนงาน ณ เดือนที่เลือก
        n = 32
        while n <= int(num_pic):
            print(f"n = {n}")

            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

            # สร้าง element ที่กำหนดจำนวน column
            choose_column = driver.find_element(By.XPATH, '/html/body/app-root/app-e-service-table/div/mat-paginator/div/div/div[1]/mat-form-field/div[1]/div/div[2]/mat-select')
            ## กดปุ่มที่กำหนดจำนวน column
            choose_column.click()
            time.sleep(3)
        
            # สร้าง element ที่กำหนดตารางเป็น 100 column 
            hundred_column = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/mat-option[4]')
            ## กดปุ่มที่กำหนดจำนวน column
            hundred_column.click()
            time.sleep(5)

            driver.execute_script(f"window.scrollTo(0, 0)")
            time.sleep(2)

            # scroll หา element ของปุ่ม รูปภาพ ในตารางแผนงาน ณ เดือนที่เลือก
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            scroll_to_height = round((scroll_height * n) // int(num_pic))
            print(f"scroll_height : {scroll_height}")
            print(f"scroll_to_height : {scroll_to_height}")
            driver.execute_script(f"window.scrollTo(0, {scroll_to_height})")
            time.sleep(2)
            ## /html/body/app-root/app-e-service-table/div/app-table-contract/div/table/tbody/tr[33]/td[4]
            sub_table_path = '/html/body/app-root/app-e-service-table/div/app-table-contract/div/table/tbody/'
            print(sub_table_path + f'tr[{n}]/td[4]')

            try:
                ## element ของปุ่ม รูปภาพ ในตารางแผนงาน ณ เดือนที่เลือก
                pic_button = driver.find_element(By.XPATH, sub_table_path + f'tr[{n}]/td[4]')
                ## กดปุ่ม รูปภาพ ในตารางแผนงาน ณ เดือนที่เลือก
                pic_button.click()
            except Exception as e:
                print(f"Cannot find element no. {n}")
                #print(e)
                n += 1
                continue

            time.sleep(17)

            ## print html script ของหน้านี้
            pic_link_contents = loginPage.getpageScript(driver=driver)
            pic_list = loginPage.getList(pic_link_contents,'"', 'amazon')
            # print(pic_list[1])

            ## หา work sap (ID)
            work_sap = loginPage.getList(pic_link_contents, '"', 'Work SAP')
            work_sap[0] = work_sap[0].replace(" ", "")
            for i in range(len(work_sap[0])-12):
                if '52000' in work_sap[0][i:i+12]:
                    try:
                        work_sap = str(int(work_sap[0][i:i+12]))
                        break
                    except:
                        continue
            print(work_sap)

            ## หาชื่อของถัง
            tank_name_trash = loginPage.getList(pic_link_contents, '"', 'NO.')
            tank_name = []
            for tank in tank_name_trash:
                tank.replace("<div _ngcontent-hls-c96=", "")
                tank.replace(">", "")
                ch = 0
                for i in tank:
                    if i == '-':
                        break
                    else:
                        ch += 1
                print(f'tank : {tank}')
                print(f'tank_new : {tank[:ch]}')
                #tank.replace(tank, tank[:ch])
                tank_name.append(tank[:ch])
            print(tank_name)

            ## หา label ของรูปภาพ
            label  = loginPage.getlabel(pic_link_contents)
            print("label : ", label)

            pic_ch = 0
            for i in range(len(tank_name)):        
                ## save images
                current_directory = os.getcwd()
                pic_root_path = '.\\images\\'
                date = date
                work_sap = work_sap
                t = tank_name[i]
                sum_path = f"{pic_root_path}{date}\\{work_sap}\\{t}\\"
                #sum_path = sum_path.replace("\\\\", "\\")
                print(sum_path + "before\\")
                try:
                    os.mkdir(f"{pic_root_path}{date}")
                except Exception as e:
                    print(f"you suck : {e}")
                    pass
                try:
                    os.mkdir(f"{pic_root_path}{date}\\{work_sap}\\")
                except Exception as e:
                    print(f"you suck : {e}")
                    pass
                try:
                    os.mkdir(f"{pic_root_path}{date}\\{work_sap}\\{t}\\")
                except Exception as e:
                    print(f"you suck : {e}")
                    pass
                try:
                    os.mkdir(sum_path + "before\\")
                except Exception as e:
                    print(f"you suck : {e}")
                    pass
                try:
                    os.mkdir(sum_path + "after\\")
                except Exception as e:
                    print(f"you suck : {e}")
                    pass
                # for url in pic_list:
                #     # print(url)
                #     loginPage.savePic(url, pic_root_path)
                print(len(label[i][1][0]))
                for j in range(len(label[i][1])):
                    if j == 0:
                        for k in label[i][1][j][1:]:
                            loginPage.savePic(pic_list[pic_ch], sum_path + "before\\")
                            pic_ch += 1 
                    elif j == 1:
                        for k in label[i][1][j][1:]:
                            loginPage.savePic(pic_list[pic_ch], sum_path + "after\\")
                            pic_ch += 1

            # time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

            bank_len = len(tank_name)
            # print(f"bank_len : {bank_len}")

            # สร้าง element ปุ่มย้อนกลับ
            #/html/body/app-root/app-images/div/div/div[3]
            back_button = driver.find_element(By.XPATH, f"/html/body/app-root/app-images/div/div/div[{bank_len + 1}]")
            ## กดปุ่มย้อนกลับ
            driver.execute_script("arguments[0].click();", back_button)
            #back_button.click()
            time.sleep(2)
            print(f"n = {n} is done.")
            n += 1


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the browser is closed even if an error occurs
        time.sleep(3)
        driver.quit()