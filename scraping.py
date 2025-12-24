from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

URL ="https://www.starlux-airlines.com/zh-TW/booking/book-flight/search-a-flight?trip=round-trip"
# From = "TPE"
# To = "NRT"
# Date = "2025/11/25 - 2025/12/03"
# Class_name = "經濟艙"
# class_level = "eco"

class FlightScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)

    def run_selenium_price_scraper(self,From,To,Date,Class_name,class_level):
        self.driver.get(URL)

        cookie_accept = self.driver.find_element(By.XPATH,
                                            value="//*[@id='__layout']/div/div[5]/div/div/div[3]/div[1]/button[1]")
        cookie_accept.click()

        # 輸入出發地
        flight_from = self.driver.find_element(By.XPATH,
                                          value="//*[@id='layout-content']/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/button")
        flight_from.click()
        # time.sleep(1)
        from_airport = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="qa-txt-search"]')))
        from_airport.click()
        from_airport.send_keys(From, Keys.ENTER)

        # 輸入目的地
        flight_to = self.driver.find_element(By.XPATH,
                                        value="//*[@id='layout-content']/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[2]/button")
        flight_to.click()
        # time.sleep(1)
        to_airport = self.driver.find_element(By.CSS_SELECTOR, value='[data-qa="qa-txt-search"]')
        to_airport.click()
        to_airport.send_keys(To, Keys.ENTER)

        # 輸入日期
        date = self.driver.find_element(By.CSS_SELECTOR, value='[data-qa="qa-datetime-date"]')
        date.click()
        date.click()
        date.send_keys(Date)

        close_button = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '[class="flex justify-between items-center m-1 ml-auto"]')))
        close_button.click()

        # 選擇人數和艙等
        passenger = self.driver.find_element(By.CSS_SELECTOR, value='[data-qa="qa-ddl-paxAndCabin"]')
        passenger.click()
        passenger_number = self.driver.find_element(By.XPATH,
                                               value="//*[@id='__layout']/div/div[5]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/button[2]")

        Class_level = self.driver.find_element(By.CSS_SELECTOR, value=f'[value="{class_level}"]')
        Class_level.click()
        Class_button = self.driver.find_element(By.XPATH,
                                           value="//*[@id='__layout']/div/div[5]/div/div/div[2]/div[2]/div[2]/div/button")
        Class_button.click()

        # search
        search_button = self.driver.find_element(By.XPATH, value="//*[@id='layout-content']/div[2]/div/div/div[2]/button")
        search_button.click()

        # 找最便宜的機票
        def get_cheapest_economy():
            flight_elements = self.wait.until(
                ec.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-qa="qa-item-flight"]')))

            best_price = None
            best_flight_info = None
            best_button = None
            lowest_price = None
            all_flights = []
            for f in flight_elements:
                try:
                    # 取得艙等名稱
                    cabin_name = f.find_element(By.CSS_SELECTOR, '[data-qa="qa-lbl-cabin"]').text.strip()
                    # 抓出發/到達時間（可選）
                    depart_time = f.find_element(By.CSS_SELECTOR, '[data-qa="qa-lbl-departureTime"]').text.strip()
                    arrive_time = f.find_element(By.CSS_SELECTOR, '[data-qa="qa-lbl-arrivalTime"]').text.strip()
                    # 所需時間
                    duration = f.find_element(By.CSS_SELECTOR, '[data-qa="qa-lbl-duration"]').text.strip()
                    # 抓航班號
                    flight_no = f.find_element(By.CSS_SELECTOR, '[data-qa="qa-lbl-flightNo"]').text.strip()
                    # 抓價錢字串
                    price_text = f.find_element(By.CSS_SELECTOR, '[data-qa="qa-lbl-price"] strong').text.strip()
                    # 轉成整數
                    price_int = int(price_text.replace(',', ''))
                    if cabin_name == Class_name:
                        best_flight_info = {
                            'flight_no': flight_no,
                            'price': price_int,
                            'depart_time': depart_time,
                            'arrive_time': arrive_time,
                            'duration': duration
                        }
                        all_flights.append(best_flight_info)
                        # 更新最便宜
                        if best_price is None or price_int < best_price:
                            best_price = price_int

                            best_button = f.find_element(By.CSS_SELECTOR, '[data-qa="qa-btn-cabin"]')
                            lowest_price = price_text
                except Exception as e:
                    # 若某些航班資料缺少欄位，就跳過
                    print(f"跳過航班因錯誤: {e}")
                    continue
            # 選出所有最便宜的機票
            cheapest_flights = [f for f in all_flights if f['price'] == best_price]

            if cheapest_flights:
                print(f"最便宜航班：{best_flight_info['flight_no']}，價格：{best_flight_info['price']}\n"
                      f"出發時間:{best_flight_info['depart_time']}\n"
                      f"抵達時間:{best_flight_info['arrive_time']}\n"
                      f"所需時間:{best_flight_info['duration']}")

                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", best_button)
                best_button.click()
                time.sleep(1)
                level_text = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="qa-lbl-fareProductName"]').text.strip()
                currency_text = self.driver.find_element(By.CSS_SELECTOR, '[data-i18n-text="CW_booking32"]').text.strip().split(" ")[0]
                final_button = self.driver.find_element(By.CSS_SELECTOR,
                                                   f'[aria-label="{level_text} {currency_text} {lowest_price}"]')
                final_button.click()
            else:
                print("未找到任何航班或價格資訊。")

            return cheapest_flights

        from_best_info = get_cheapest_economy()
        time.sleep(3)
        to_best_info = get_cheapest_economy()

        self.driver.quit()
        return from_best_info, to_best_info

