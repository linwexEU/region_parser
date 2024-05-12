import subprocess

import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from optional import FileWork, UserAgentAndProxy


class Region:
    def get_browser_with_proxy(self, proxy):
        user_agent = UserAgentAndProxy.get_random_ua()

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (
            proxy[0],
            proxy[1],
            proxy[2],
            proxy[3],
        )

        chrome_options = undetected_chromedriver.ChromeOptions()

        with open("manifest.json", "w") as file:
            file.write(manifest_json)

        with open("background.js", "w") as file:
            file.write(background_js)

        chrome_options.add_argument("--load-extension=D:\\Python\\TEST")
        chrome_options.add_argument("--user-agent=%s" % user_agent)
        chrome_options.add_argument("--headless=chrome")

        driver = undetected_chromedriver.Chrome(options=chrome_options)
        return driver

    def parse_page(self, url, proxy):
        try:
            browser = self.get_browser_with_proxy(proxy)
            browser.get(url)

            WebDriverWait(browser, 60).until(
                EC.visibility_of_all_elements_located(
                    (
                        By.XPATH,
                        "//div[@class='d-none d-xl-block col-xl-3 company-item-sidebar']",
                    )
                )
            )

            src = browser.page_source
            soup = BeautifulSoup(src, "lxml")

            code = (
                soup.find(
                    "div", class_="company-sidebar border rounded p-3 p-md-4 mb-3"
                )
                .find_all("div", class_="company-sidebar__item")[0]
                .text.strip()
                .split("ЄДРПОУ")[-1]
            )
            company_name = (
                soup.find("h1", class_="ui-title col-md-10")
                .text.strip()
                .replace(",", " ")
            )

            emails = []
            phones = []
            sites = []
            for item in (
                soup.find(
                    "div", class_="d-none d-xl-block col-xl-3 company-item-sidebar"
                )
                .find(
                    "div",
                    class_="d-none d-lg-block company-sidebar p-3 p-md-4 mb-3 border",
                )
                .find_all("div", class_="company-sidebar__item")
            ):
                try:
                    query = item.find("div", class_="company-sidebar__data")
                    if query.find_all("a") != None:
                        for subq in item.find(
                            "div", class_="company-sidebar__data"
                        ).find_all("a"):
                            element = subq.text
                            if "@" in element:
                                emails.append(element)
                            elif "https://" in element or "http://" in element:
                                sites.append(element)
                            else:
                                phones.append(element.replace("\xa0", " "))
                except:
                    pass

            FileWork.add_to_file(
                code,
                company_name,
                " ".join(map(lambda x: f"({x})", emails)),
                " ".join(map(lambda x: f"[{x}]", phones)),
                " ".join(map(lambda x: f"({x})", sites)),
            )
            print(f"[INFO] {code} - success parsed!")
        except Exception as ex:
            print(f"[ERROR] {ex}")
        finally:
            browser.quit()
            subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def parser_initialization(self):
        count_for_proxy = 1
        proxy = UserAgentAndProxy.get_random_proxy()
        for code in [
            "2919103017",
            "38853509",
            "39165816",
            "41675320",
            "40672752",
            "40396139",
            "32181742",
            "39714715",
            "43383337",
            "42830482",
            "41215180",
            "41266590",
            "35466539",
            "40401693",
            "41585268",
            "02904160"
        ]:
            url = "https://www.ua-region.com.ua/" + code

            if count_for_proxy % 5 == 0:
                proxy = UserAgentAndProxy.get_random_proxy()
                print(f"[INFO change proxy to {proxy[0]}]")

            self.parse_page(url, proxy)
            count_for_proxy += 1


if __name__ == "__main__":
    FileWork.create_file()
    region = Region()
    region.parser_initialization()
