import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


class ElementNotFound(Exception):
    def __init__(self, xpath):
        self.xpath = xpath

    def __str__(self):
        return "Element no found, xpath: " + self.xpath


class UnknownCommand(Exception):
    def __init__(self, commandName):
        self.commandName = commandName

    def __str__(self):
        return "This command does not exist: " + self.commandName


class SeleniumChrome:
    def __init__(self, backgroundMode=False):
        s = webdriver.ChromeOptions()
        s.headless = backgroundMode
        s.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        # for ChromeDriver version 79.0.3945.16 or over
        s.add_argument("--disable-blink-features=AutomationControlled")
        s.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            options=s
        )

    def goTo(self, link):
        self.driver.get(link)

    def setSize(self, h, w):
        self.driver.set_window_size(h, w)

    def findElementInf(self, xpath):
        """this version can search for an element indefinitely"""
        result = None
        while True:
            try:
                result = self.driver.find_element('xpath', xpath)
            except:
                continue
            break
        return result

    def findElement(self, xpath):
        return self.driver.find_element('xpath', xpath)

    def elementExits(self, xpath):
        try:
            self.driver.find_element("xpath", xpath)
            return True
        except:
            pass
        return False

    def clickInf(self, xpath):
        element = None
        while True:
            try:
                element = self.findElement(xpath)
            except:
                continue
            break
        try:
            element.click()
            return
        except AttributeError:
            raise ElementNotFound(xpath)

    def write(self, xpath, text):
        self.findElementInf(xpath).send_keys(text)

    def read(self, xpath):
        return self.findElementInf(xpath).text

    def quit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()

    def authorization(self, loginXpath, passwordXpath, enter, login, password):
        self.write(loginXpath, login)
        self.write(passwordXpath, password)
        self.clickInf(enter)

    def moveToElement(self, xpath):
        ActionChains(self.driver).move_to_element(self.findElement(xpath)).perform()

    def refresh(self):
        self.driver.refresh()


def main():
    driver = SeleniumChrome()
    try:
        driver.goTo("https://www.google.com/?client=chrome")
        time.sleep(5)
        print(driver.elementExits("/html/body/div[1]/div[5]/div[2]/div[1]/a[1]"))
        print(driver.elementExits("text"))
    finally:
        driver.close()


if __name__ == "__main__":
    main()

