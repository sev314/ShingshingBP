class NCBPError(Exception):
    """싱싱비피 프로그램 기본 예외 클래스"""

    pass


class DriverNotFoundError(NCBPError):
    """웹 드라이버를 찾을 수 없을 때 발생"""

    pass


class CrawlingError(NCBPError):
    """크롤링 중 문제가 발생할 때 발생"""

    pass


# EOF
