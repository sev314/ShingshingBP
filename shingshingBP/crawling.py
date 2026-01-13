import os
import time

from bs4 import BeautifulSoup

from .types import SeleniumWebDriver


def crawl_posts(username: str | None, cafedir: str, driver: SeleniumWebDriver, start: int, end: int, sleeptime: float) -> None:
    # 본격 크롤링 시작.

    tno = start

    while tno <= end:
        no = cafedir + "/" + str(tno)

        driver.get(no)
        time.sleep(sleeptime)

        try:
            alert = driver.switch_to.alert

            alert.accept()
            print("%d번 게시글은 존재하지 않음" % tno)

            tno = tno + 1

        except:
            driver.switch_to.frame("cafe_main")

            html = driver.page_source.encode("utf-8")
            html = html.decode("utf-8")

            f = open(
                "C:/Users/%s/NCBP/CAFE/%d.html" % (username, int(tno)),
                "w",
                encoding="UTF-8",
            )

            f.write(clean_html(html))
            f.close()
            print("%d번 게시글 저장완료." % int(tno))
            os.system(
                'start cmd /c start /d "C:/Program Files/wkhtmltopdf/bin/" /b wkhtmltopdf.exe --encoding UTF-8 C:/Users/%s/NCBP/CAFE/%d.html C:/Users/%s/NCBP/CAFE/%d.pdf'
                % (username, tno, username, tno)
            )
            print("%d번 게시글 변환요청 완료." % int(tno))

            tno = tno + 1

    print("크롤링이 완료되었습니다")


def clean_html(raw_html: str) -> str:
    """불필요한 iframe을 제거하고 인코딩을 설정합니다."""

    soup = BeautifulSoup(raw_html, "html.parser")

    # NOTE:
    # <iframe title="답변쓰기에디터" ...>는 게시글 본문이 아닌, 댓글(답글) 작성용 에디터 영역입니다.
    # 이는 백업 대상이 아닌 불필요한 내용이므로, 저장된 HTML 파일을 열 때 해당 에디터 UI가 보이지 않도록 미리 제거합니다.

    for iframe in soup.find_all("iframe", title="답변쓰기에디터"):
        iframe.decompose()

    # 메타 태그 교체 (Charset 설정)

    if soup.head:
        new_meta = soup.new_tag("meta", charset="UTF-8")
        soup.head.insert(0, new_meta)

    return soup.prettify()
