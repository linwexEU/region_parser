import csv
import random

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-UA,en;q=0.9,ru-UA;q=0.8,ru;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=qm79mqju7gr8ivf31iikddh8d6; _ga=GA1.1.684644062.1713983960; G_ENABLED_IDPS=google; __gads=ID=426c9c285c39033d:T=1713983960:RT=1713983960:S=ALNI_MbYfR5gPbXeKWrqbZ0JEKSq7FJJkw; __gpi=UID=00000dfde2f30ad2:T=1713983960:RT=1713983960:S=ALNI_MZ7YVmRduEdJHjMl40iAXu08383ig; __eoi=ID=b99cab20fed0ed0d:T=1713983960:RT=1713983960:S=AA-AfjYBj9C2T3VaOsLsa8PFzu-H; FCNEC=%5B%5B%22AKsRol9e4zZvuZ-Q2dWu1Z3snzcNGgK4gJ-gEqIpazsBnXziVH1N7cgsj_HNLD_mIchear4-I-B8cikzkkIgZhdzfnmNtfzeqzxMuHaZe8abWZqCJ_JfUZno7FF6RlIB-cHW7ywt8IYuDL4l38Ih8yXFzYNxAiW72A%3D%3D%22%5D%5D; _ga_TDFGJDHCY1=GS1.1.1713983959.1.1.1713983982.37.0.0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


class UserAgentAndProxy:
    @classmethod
    def get_random_ua(cls):
        with open("user_agent.txt") as file:
            ua = file.readlines()
            return random.choice(ua).strip()

    @classmethod
    def get_random_proxy(cls):
        with open("proxy.txt") as file:
            proxy = random.choice(file.readlines()).strip()
            return proxy.split(":")


class FileWork:
    @classmethod
    def create_file(cls):
        with open("region.csv", "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                (
                    "ЄДРПОУ",
                    "Назва компанії",
                    "E-mail",
                    "Номери телефонів",
                    "Сайт"
                )
            )

    @classmethod
    def add_to_file(
        cls,
        code,
        company_name,
        emails,
        phones,
        sites
    ):
        with open("region.csv", "a", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                (
                    code,
                    company_name,
                    emails,
                    phones,
                    sites
                )
            )
