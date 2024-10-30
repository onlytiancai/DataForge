import json
from dataclasses import dataclass
from typing import List, Generic, Optional, TypeVar, Union

from pydantic import Field

from fastapi import Query

from .exceptions import HTTP_400_BAD_REQUEST
from pydantic import BaseModel
_T = TypeVar("_T", bound=BaseModel)

class BaseApiOut(BaseModel, Generic[_T]):
    message: str = Field(default="ok", description="状态描述")
    data: Union[Optional[_T], List[_T]] = Field(default=None, description="返回数据")
    code: Optional[int] = Field(default=0, description="状态码")


@dataclass
class PagingRequest:
    """分页请求

    Attributes:
        page: 当前的页数
        page_size: 每一页的行数
        query: 过滤条件
        order_by: 排序条件
        nopaging: 是否分页
    """

    page: int = Query(default=1, description="当前的页数")
    page_size: int = Query(default=10, description="每一页的行数")
    query: Optional[List[str]] = Query(
        default=None, description="过滤条件", examples=['{"account": "admin"}']
    )
    order_by: Optional[List[str]] = Query(
        default=None,
        description="排序条件",
        examples=[
            '{"id": "asc"}',
            '{"id": "ascending"}',
            '{"id": "ascend"}',
            '{"id": "desc"}',
            '{"id": "descending"}',
            '{"id": "descend"}',
        ],
    )
    nopaging: Optional[bool] = Query(default=None, description="是否分页")

    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    def limit(self) -> int:
        return self.page_size

    def need_paging(self) -> bool:
        return self.nopaging is None or self.nopaging

    def query_dict(self):
        if self.query is None:
            return None
        try:
            return list(map(json.loads, self.query))
        except Exception as e:
            print(e)
            raise HTTP_400_BAD_REQUEST

    def orderby_dict(self):
        if self.order_by is None:
            return None
        try:
            return list(map(json.loads, self.order_by))
        except Exception as e:
            print(e)
            raise HTTP_400_BAD_REQUEST


class PagingResponse(BaseModel, Generic[_T]):
    """分页回应

    Attributes:
        total: 总行数
        items: 分页数据
    """

    total: Optional[int] = Field(description="总行数")
    items: List[_T] = Field(default=[], description="分页数据")
