import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from utils.parser import parse_attendance_text


def scrape_attendance(roll_no: str, password: str) -> dict:
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver_path = ChromeDriverManager().install()
    driver_dir = os.path.dirname(driver_path)
    exe_path = os.path.join(driver_dir, 'chromedriver.exe')
    if os.path.exists(exe_path):
        driver_path = exe_path

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 20)

    try:
        driver.get('http://mitsims.in/studentLogin.jsp?personType=student')

        wait.until(EC.presence_of_element_located((By.ID, 'userId'))).send_keys(roll_no)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.ID, 'loginBtn').click()

        try:
            attendance_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[contains(text(),'Attendance') or contains(text(),'ATTENDANCE') or contains(text(),'attendance')]")
                    )
            )
        except TimeoutException:
            body_text = driver.find_element(By.TAG_NAME, 'body').text
            if any(term in body_text.lower() for term in ['invalid', 'incorrect', 'failed', 'wrong']):
                raise RuntimeError('Login failed: invalid roll number or password')
            raise RuntimeError('Login completed but attendance button was not found')

        attendance_button.click()
        time.sleep(5)

        body_text = driver.find_element(By.TAG_NAME, 'body').text
        attendance = parse_attendance_text(body_text)

        if attendance is None:
            raise RuntimeError('Failed to parse attendance data')

        return attendance
    finally:
        driver.quit()
