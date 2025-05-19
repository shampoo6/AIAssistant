import os
from typing import Annotated

from langchain_core.tools import tool
from pathlib import Path
from zhipuai import ZhipuAI

_client = ZhipuAI(
    api_key=os.getenv('ZHIPU_API_KEY'),
    base_url="https://open.bigmodel.cn/api/paas/v4"
)


@tool
def extract_text_from_docx(docx_path: Annotated[str, '.docx 或 .doc 文件的绝对路径']):
    """调用 zhipu api 接口，提取文档中的文本"""
    # 用于上传文件
    # 格式限制：.PDF .DOCX .DOC .XLS .XLSX .PPT .PPTX .PNG .JPG .JPEG .CSV .PY .TXT .MD .BMP .GIF
    # 文件大小不超过50M，图片大小不超过5M、总数限制为100个文件
    file_object = _client.files.create(file=Path(docx_path), purpose="file-extract")
    file_content = _client.files.content(file_id=file_object.id).content.decode()
    result = _client.files.delete(
        file_id=file_object.id  # 支持retrieval、batch、fine-tune、file-extract文件
    )
    return file_content
