# import re
#
# from common.requests_util import RequestUtil
# from common.yaml_util import write_extract_yaml, read_extract_yaml
#
#
# class TestRequests_03:
#     def test_php(self):
#         url = "/phpwind/"
#         res = RequestUtil("base", "base_php_url").send_requests(url=url, method="get")
#         return_data = res.text
#         #通过正则表达式取值
#         obj= re.search('name="csrf_token" value="(.*?)"',return_data)
#         #写入extract_token
#         extract_data={"csrf_token":obj.group(1)}
#         write_extract_yaml(extract_data)



