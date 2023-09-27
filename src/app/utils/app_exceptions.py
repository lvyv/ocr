from fastapi import Request
from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class AppException(object):
    class HttpRequestParamsIllegal(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            HTTP请求的参数错误
            """
            status_code = 422
            AppExceptionCase.__init__(self, status_code, context)

    class HttpRequestTimeout(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            HTTP请求超时
            """
            status_code = 504
            AppExceptionCase.__init__(self, status_code, context)
