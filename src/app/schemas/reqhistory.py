from pydantic import BaseModel


class ReqItemBase(BaseModel):
    """
    所有soh请求：
     - status字段，从pending到settled。
     - result字段，从pending到执行的结果。
     - requestts字段，发起调用的时间戳。
     - settledts字段，回调结果的时间戳。
     - memo字段，保存一些额外信息。
    """
    status: str
    result: str
    requestts: int = 0
    settledts: int = 0
    memo: str = ''


class ReqItemCreate(ReqItemBase):
    """
    创建的时候必须提供模型类型。
    """
    model: str


class ReqItem(ReqItemBase):
    """
    获取记录必须提供关键字id。
    """
    id: int

    class Config:
        orm_mode = True
