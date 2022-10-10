
import allure
import pytest
import config
from base.base_util import Library
from common.execl_open import Execl_open


@allure.epic("商城")
@allure.feature("登录管理")
class TestCase01():
    excel = Execl_open()
    datas = excel.get_data()



    @pytest.mark.parametrize('casedata',datas)
    @allure.story("登录")
    @pytest.mark.run(order=1)
    def test_login(self, casedata):
        #print(caseinfo)
        casename = casedata['casename']
        stepdatas = casedata['stepdata']
        lib = Library()
        for index, stepdata in enumerate(stepdatas):
            # index 索引 当index为0，row则是2 stepdata测试步骤的数据
            try:
                lib.run(*stepdata)
                self.excel.write_steptime(sheetname=casename, row=index + 2)
                # 写入测试结果
                self.excel.write_stepresult(sheetname=casename, row=index + 2, col=config.stepresult_col, result='PASS')
                # self.excel.write_casetime()
            except Exception as error:
                self.excel.write_stepresult(sheetname=casename, row=index + 2, col=config.stepresult_col, result='FLASE')
        self.excel.write_caseresult()
        self.excel.write_casetime()
