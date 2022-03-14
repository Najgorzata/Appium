import unittest

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Cw1UnitTest(unittest.TestCase):

    def setUp(self):
        desired_caps = {
            "deviceName": "Pixel4XL",
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "appPackage": "com.saucelabs.mydemoapp.rn",
            "appActivity": "com.saucelabs.mydemoapp.rn.MainActivity"
        }

        # SETWEBDRIVERA
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    def test1(self):
        self.driver.implicitly_wait(30)
        # check if main page is displayed
        self.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Products']").is_displayed()
        products = self.driver.find_elements(AppiumBy.XPATH, "//*[@content-desc='store item']")

        price = products[1].find_element(AppiumBy.XPATH, "//*[@content-desc='store item price']").get_attribute("text")
        print(price)

        # click product nr 2
        products[1].click()

        # check if product page is displayed
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "product screen").is_displayed()
        self.driver.find_element(AppiumBy.XPATH,
                                 "//android.widget.TextView[@text='Sauce Labs Bike Light']").is_displayed()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Add To Cart button").is_displayed()

        headerElement = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'container header')
        productName = headerElement.find_element(AppiumBy.CLASS_NAME, 'android.widget.TextView').get_attribute("text")
        print(productName)

        # assert if product price is equal
        price2 = self.driver.find_element(AppiumBy.XPATH, "//*[@content-desc='product price']").get_attribute("text")
        print("Price on product page" + price2)
        self.assertEqual(price, price2)

        # click add to cart and assert if product is added
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Add To Cart button").click()
        productInCart = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cart badge").find_element(
            AppiumBy.CLASS_NAME, "android.widget.TextView").get_attribute("text")
        self.assertEqual("1", productInCart)

        # klikamyWKoszyk
        # sprawdzamyczyKoszykSieOtwrzoyl
        # a) Header b) nazwa produktu c)cena przy produkcie d) przycisk usuniecia e) product checkout d) footer
        # STRATEGIA - TO PODSTAWA

        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cart badge").click()

        # self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "cart screen").is_displayed()
        # JAK SPOWOLNIC TEGO POTWORKA -> WEBDRIVERWAIT
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='My Cart']")))
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "container header").find_element(AppiumBy.XPATH,
                                                                                             "//*[@text='My Cart']").is_displayed()
        # check if product name is equal to product from main page
        productNameCart = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "product label").get_attribute("text")
        self.assertEqual(productName, productNameCart)
        # check if price is equal
        priceInCart = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "product price").get_attribute("text")
        self.assertEqual(price, priceInCart)
        # check if remove is displayed
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "product row").find_element(AppiumBy.XPATH,
                                                                                        "//*[@text='Remove Item']").is_displayed()
        # check if Proceed To Checkout button is displayed
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Proceed To Checkout button").is_displayed()
        # checkout footer
        checkoutFooterElement = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "checkout footer")
        childrenFooterElements = checkoutFooterElement.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        self.assertEqual(childrenFooterElements[0].get_attribute("text"), "Total:")
        self.assertEqual(childrenFooterElements[1].get_attribute("text"), "1 item")
        self.assertEqual(childrenFooterElements[2].get_attribute("text"), priceInCart)

        # Proceed To Chekout Page
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Proceed To Checkout button").click()
        # check if checkout page is displayed
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='Login']")))
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "container header").find_element(AppiumBy.XPATH,
                                                                                             "//*[@text='Login']").is_displayed()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Username input field").send_keys("bob@example.com")
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Password input field").send_keys("10203040")
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Login button").click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='Checkout']")))
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "container header").find_element(AppiumBy.XPATH,
                                                                                             "//*[@text='Checkout']").is_displayed()