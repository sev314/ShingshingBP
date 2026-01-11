import os
import subprocess
import time
from os import getenv

import selenium
from selenium import webdriver

SeleniumWebDriver = webdriver.Firefox | webdriver.Edge | webdriver.Chrome


# 『Man』은 『매니저』라는 뜻이다.
class BackupMan:
    """네이버카페 게시글을 백업합니다."""

    driver: SeleniumWebDriver

    @property
    def username(self) -> str | None:
        return getenv("USERNAME")

    def init(self) -> None:
        """풀그림 실행에 필요한 초기 설정을 수행합니다."""

        ##-------프로그램 초기화--------
        print("프로그램 초기화중....")

        try:
            self.init_webdriver()
            self.driver.get("https://naver.com")

            if os.path.exists("C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"):
                print("wkHTMLtoPDF가 설치되어 있습니다. 프로그램이 준비되었습니다")
            else:
                print("wkHTMLtoPDF가 없습니다. 준비되지 않았습니다. wkHTMLtoPDF를 재설치 하세요")
                print("계속할수는 있지만 정상적으로 진행되지 않습니다.")

        except:
            print("프로그램 초기화에 실패했습니다")
            print("Selenium 설치여부와 위치를 확인해주세요")

        ##--------초기화 끝----------------

    def init_webdriver(self) -> None:
        self.driver = webdriver.Edge()
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

        # 본격 크롤링 시작.

        tno = start

        while tno <= end:
            no = cafedir + "/" + str(tno)

            self.driver.get(no)
            time.sleep(int(sleeptime))

            try:
                alert = self.driver.switch_to.alert

                alert.accept()
                print("%d번 게시글은 존재하지 않음" % tno)

                tno = tno + 1

            except:
                self.driver.switch_to.frame("cafe_main")

                html = self.driver.page_source.encode("utf-8")
                html = html.decode("utf-8")

                f = open(
                    "C:/Users/%s/NCBP/CAFE/%d.html" % (self.username, int(tno)),
                    "w",
                    encoding="UTF-8",
                )

                # NOTE:
                # <iframe title="답변쓰기에디터" ...>는 게시글 본문이 아닌, 댓글(답글) 작성용 에디터 영역입니다.
                # 이는 백업 대상이 아닌 불필요한 내용이므로, 저장된 HTML 파일을 열 때 해당 에디터 UI가 보이지 않도록 미리 제거합니다.
                html = html.replace('<iframe title="답변쓰기에디터"', "w")

                # NOTE: 한글을 비롯한 UTF-8 문자들이 올바르게 렌더링되도록 하기 위한 조치입니다.
                html = html.replace(
                    '<meta name="robots" content="noindex, nofollow">',
                    '<meta charset="UTF-8">',
                    1,
                )

                f.write(html)
                f.close()
                print("%d번 게시글 저장완료." % int(tno))
                os.system(
                    'start cmd /c start /d "C:/Program Files/wkhtmltopdf/bin/" /b wkhtmltopdf.exe --encoding UTF-8 C:/Users/%s/NCBP/CAFE/%d.html C:/Users/%s/NCBP/CAFE/%d.pdf'
                    % (self.username, tno, self.username, tno)
                )
                print("%d번 게시글 변환요청 완료." % int(tno))

                tno = tno + 1

        print("크롤링이 완료되었습니다")
        os.system("start C:/Users/%s/NCBP/CAFE" % (self.username))

        print("크롤링 결과를 확인하세요. %d번 게시글 부터 %d번 게시글까지 크롤링되었습니다." % (start, end))
        print("존재하지 않는 게시글은 저장되지 않았습니다.")


def main() -> None:
    print("크롤링 프로그램 시작중...")
    print("사용중 문제나 어려움이 있을시, 스크린샷 첨부해서 admin@nonaver.com으로 메일 주시면 도와드리겠습니다.")
    print("NCBP 0.39버젼입니다. 2022년 02월 08일 배포.")

    # -----------------------아래부터 프로그램 시작-----------------------------

    backup_man = BackupMan()

    backup_man.init()
    backup_man.run_backup()
