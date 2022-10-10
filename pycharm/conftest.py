#执行之前先清空extract文件内容
import pytest

from common.yaml_util import clear_extract_yaml

@pytest.fixture(scope="session",autouse=True)
def clear_extract():
    clear_extract_yaml()