import allure
import pytest
from common.parameters_util import  read_testcase_file
from common.requests_util import RequestUtil


@allure.epic("微信公众号平台")
@allure.feature("标签管理")
class TestRequest_03:
    @allure.story("获取统一接口token")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("caseinfo",read_testcase_file('/testcases/api/gzh/get_token.yml'))
    def test_get01(self,caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story("查询标签")
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/api/gzh/select_flag.yml'))
    def test_get02(self,caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story("编辑标签")
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/api/gzh/edit_flag.yml'))
    def test_post02(self,caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story("文件上传")
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/api/gzh/updata_file.yml'))
    def test_file_upload(self,caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

