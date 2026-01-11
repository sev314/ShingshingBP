from __future__ import annotations

import os
import subprocess
import time
from os import getenv
from typing import Self

import selenium
from selenium import webdriver

from shingshingBP.crawling import crawl_posts

from .types import SeleniumWebDriver


# 『Man』은 『매니저』라는 뜻이다.
class BackupMan:
    """네이버카페 게시글을 백업합니다."""

    driver: SeleniumWebDriver

    def __init__(self, driver: SeleniumWebDriver):
        self.driver = driver

    @property
    def username(self) -> str | None:
        return getenv("USERNAME")

    @classmethod
    def setup(cls) -> Self:
        """풀그림 실행에 필요한 초기 설정을 수행합니다."""

        ##-------프로그램 초기화--------
        print("프로그램 초기화중....")

        backup_man = cls(webdriver.Edge())
        backup_man.init_webdriver()
        backup_man.driver.get("https://naver.com")

        if os.path.exists("C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"):
            print("wkHTMLtoPDF가 설치되어 있습니다. 프로그램이 준비되었습니다")
        else:
            print("wkHTMLtoPDF가 없습니다. 준비되지 않았습니다. wkHTMLtoPDF를 재설치 하세요")
            print("계속할수는 있지만 정상적으로 진행되지 않습니다.")

        ##--------초기화 끝----------------

        return backup_man

    def init_webdriver(self) -> None:
        self.driver.implicitly_wait(1)

    def run_backup(self) -> None:
        ##-------크롤링 사이트 로그인요청/사이트 지정----------------

        print("현재 접속된 네이버 홈페이지에서 로그인해 주세요!")

        time.sleep(5)

        print("\n\n아래에 https://cafe.naver.com/skyplanet와 같이 카페 주소를 입력하세요.")
        print("주소 뒤쪽에 슬래시 있으면 안됩니다. 없애주세요!")

        cafedir = input(" 여기 오른쪽에 카페주소를 Ctrl+C V 해 주세요 >>")
        start = input("저장을 시작할 게시글 번호를 입력하고 엔터키 누르세요: ")
        end = input("저장을 끝낼 게시글 번호를 입력하고 엔터키 누르세요: ")
        start = int(start)
        end = int(end)

        print("카페 설정이 완료되었습니다.")

        sleeptime = input("딜레이를 몇 초나 줄지 입력하세요: ")

        print("알림:사용자이름은 %s 입니다" % self.username)
        print("컴퓨터 설정이 완료되었습니다.")

        crawl_posts(self.username, cafedir, self.driver, start, end, float(sleeptime))
        os.system("start C:/Users/%s/NCBP/CAFE" % (self.username))

        print("크롤링 결과를 확인하세요. %d번 게시글 부터 %d번 게시글까지 크롤링되었습니다." % (start, end))
        print("존재하지 않는 게시글은 저장되지 않았습니다.")


def main() -> None:
    print("크롤링 프로그램 시작중...")
    print("사용중 문제나 어려움이 있을시, 스크린샷 첨부해서 admin@nonaver.com으로 메일 주시면 도와드리겠습니다.")
    print("NCBP 0.39버젼입니다. 2022년 02월 08일 배포.")

    # -----------------------아래부터 프로그램 시작-----------------------------

    try:
        backup_man = BackupMan.setup()

    except:
        print("프로그램 초기화에 실패했습니다")
        print("Selenium 설치여부와 위치를 확인해주세요")

        return

    backup_man.run_backup()
