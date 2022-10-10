#
# from common.requests_util import RequestUtil
# from common.yaml_util import write_extract_yaml, read_extract_yaml
#
#
# class TestRequest_01:
#
#     def test_01(self):
#
#         url = "/login"
#         data = {"username": "admin", "password": "123456"}
#         res=RequestUtil('base','base_bd_url').send_requests(url=url,method='post',data=data)
#         return_data = res.json()
#         extract_token={'Authorization':return_data['data']['token']}
#         write_extract_yaml(extract_token)
#         print(res.json())
#
#     def test_02(self):
#         url = "/menus"
#         headers = {
#             "Authorization": "{{Authorization}}"
#         }
#         res = RequestUtil('base', 'base_bd_url').send_requests(url=url, method='get', headers=headers)
#
#         print(res.json())