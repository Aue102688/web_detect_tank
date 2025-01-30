from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import math

# ตั้งค่าโฟลเดอร์ดาวน์โหลด
DOWNLOAD_FOLDER = "C:\\Users\\Ratti\\TestAI_WaterTank\\download_csv"

# ตั้งค่า Edge WebDriver
edge_options = webdriver.EdgeOptions()
edge_options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_FOLDER,
    "download.prompt_for_download": False,
    "directory_upgrade": True
})

# ใช้ WebDriver Manager เพื่อติดตั้ง EdgeDriver
service = EdgeService(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

# ฟังก์ชันคำนวณจำนวนหน้าสูงสุด
def get_max_pages():
    rows_ALL = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-e-service-table/div/mat-paginator/div/div/div[2]/div'))
    )
    rows_text = rows_ALL.text.strip()
    rows_count = float(rows_text.split('of')[-1].strip())  # ดึงค่าจำนวนแถวทั้งหมด
    pages_pp = math.ceil(rows_count / 10)
    print(pages_pp)
    return pages_pp

# เริ่มกระบวนการ
try:
    driver.get("https://pm-rsm.cpretailink.co.th/login")
    time.sleep(2)

    # ใส่ Username & Password
    username_user = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-login/div/div/div/div/div/div[2]/form/div[1]/input'))
    )
    password_user = driver.find_element(By.XPATH, '/html/body/app-root/app-login/div/div/div/div/div/div[2]/form/div[2]/div/input')

    username_put = 'benjaponsuns'
    password_put = 'Benjapon@0125'
    
    username_user.send_keys(username_put)
    password_user.send_keys(password_put)
    password_user.send_keys(Keys.RETURN)
    time.sleep(2)

    # Select Part of year you want to check
    selecting_part = driver.find_element(By.XPATH, '/html/body/app-root/app-plan-search/div/div/div[2]/app-search-pm-box/div/form/div[1]/div[2]/mat-form-field/div[1]/div[2]/div[1]/input')
    selecting_part.click()
    time.sleep(2)

    # เลือกปีที่ต้องการค้นหา
    year_put = 2025
    if year_put == 2023:
        year_select = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-multi-year-view/table/tbody/tr[6]/td[2]/button/div[1]')
        year_select.click()
        time.sleep(2)
    elif year_put == 2024:
        year_select = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-multi-year-view/table/tbody/tr[6]/td[3]/button/div[1]')
        year_select.click()
        time.sleep(2)
    elif year_put == 2025:
        year_select = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-multi-year-view/table/tbody/tr[6]/td[4]/button/div[1]')
        year_select.click()
        time.sleep(2)

    # เลือกเดือน
    month_put = 1
    month_table = {1: [2,1], 2: [2,2], 3: [2,3], 4: [2,4], 5: [3,1], 6: [3,2], 7: [3,3], 8: [3,4], 9: [4,1], 10: [4,2], 11: [4,3], 12: [4,4]}
    month_xpath = f'/html/body/div/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-year-view/table/tbody/tr[{month_table[month_put][0]}]/td[{month_table[month_put][1]}]/button'
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, month_xpath))
    ).click()
    time.sleep(2)

    # Select ALL from search from
    search_select = driver.find_element(By.XPATH, '/html/body/app-root/app-plan-search/div/div/div[2]/app-search-pm-box/div/form/div[2]/div[2]/mat-button-toggle-group/mat-button-toggle[4]/button/span')
    search_select.click()
    time.sleep(2)

    # Select Company part
    cpn_select = driver.find_element(By.XPATH, '/html/body/app-root/app-plan-search/div/div/div[2]/app-search-pm-box/div/form/div[3]/div[2]/app-multi-search-box/div/input')
    cpn_select.click()
    time.sleep(2)

    cpn_select = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-dialog-container/div/div/app-dialog-multiselect/div/div[2]/angular2-multiselect/div/div[1]/div')
    cpn_select.click()
    time.sleep(2)

    seven_select = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-dialog-container/div/div/app-dialog-multiselect/div/div[2]/angular2-multiselect/div/div[2]/div[3]/div[2]/ul/li[1]/label')
    seven_select.click()
    time.sleep(2)

    finish_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-dialog-container/div/div/app-dialog-multiselect/div/div[1]/button')
    finish_button.click()
    time.sleep(2)

    # Select Contract type
    contract_select = driver.find_element(By.XPATH, '/html/body/app-root/app-plan-search/div/div/div[2]/app-search-pm-box/div/form/div[4]/div[2]/app-multi-search-box/div/input')
    contract_select.click()
    time.sleep(2)

    contract_select = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-dialog-container/div/div/app-dialog-multiselect/div/div[2]/angular2-multiselect/div/div[1]/div')
    contract_select.click()
    time.sleep(2)

    PP_contract = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-dialog-container/div/div/app-dialog-multiselect/div/div[2]/angular2-multiselect/div/div[2]/div[3]/div[2]/ul/li[7]/label')
    PP_contract.click()
    time.sleep(2)

    finish_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/mat-dialog-container/div/div/app-dialog-multiselect/div/div[1]/button')
    finish_button.click()
    time.sleep(2)

    # Select search
    search_button = driver.find_element(By.XPATH, '/html/body/app-root/app-plan-search/div/div/div[2]/app-search-pm-box/div/form/div[7]/button')
    search_button.click()
    time.sleep(3)


    # คลิกวันที่ที่ต้องการ
    day_search = driver.find_elements(By.XPATH, '/html/body/app-root/app-e-service-plan/div/full-calendar/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[5]/td[5]/div/div[2]/div[1]/a/div/div/div/div')
    print(f"Found {len(day_search)} elements")
    time.sleep(4)

    # downloaded_urls = set() 

    # คำนวณจำนวนหน้า
    max_pages = get_max_pages()

except Exception as e:
    print("เกิดข้อผิดพลาด:", e)
finally:
    driver.quit()
