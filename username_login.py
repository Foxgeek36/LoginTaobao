import re

import requests

s = requests.Session()


class UsernameLogin:

    def __init__(self, username, ua, TPL_password2):
        """
        账号登录对象
        :param username: 用户名
        :param ua: 淘宝的ua参数
        :param TPL_password2: 加密后的密码
        """
        # 检测是否需要验证码的URL
        self.user_check_url = 'https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'
        # 验证淘宝用户名密码URL
        self.verify_password_url = "https://login.taobao.com/member/login.jhtml"
        # 访问st码URL
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'

        # 淘宝用户名
        self.username = username
        # 淘宝关键参数，包含用户浏览器等一些信息，很多地方会使用，从浏览器或抓包工具中复制，可重复使用
        self.ua = ua
        # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
        self.TPL_password2 = TPL_password2

        # 请求超时时间
        self.timeout = 3

    def _user_check(self):
        """
        检测账号是否需要验证码
        :return:
        """
        data = {
            'username': self.username,
            'ua': self.ua
        }
        try:
            response = s.post(self.user_check_url, data=data, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print('检测是否需要验证码请求失败，原因：')
            raise e
        needcode = response.json()['needcode']
        print('是否需要滑块验证：{}'.format(needcode))
        return needcode

    def _verify_password(self):
        """
        验证用户名密码，并获取st码申请URL
        :return: 验证成功返回st码申请地址
        """
        verify_password_headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://login.taobao.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://login.taobao.com/member/login.jhtml?from=taobaoindex&f=top&style=&sub=true&redirect_url=https%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm',
        }
        # 登录toabao.com提交的数据，如果登录失败，可以从浏览器复制你的form data
        verify_password_data = {
            'TPL_username': self.username,
            'ncoToken': 'cdf05a89ad5104403ebb12ebc9b7626af277b066',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'https://s.taobao.com/search?q=%E9%80%9F%E5%BA%A6%E9%80%9F%E5%BA%A6&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            'gvfdcre': '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61323330722E312E3735343839343433372E372E33353836363032633279704A767526663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246732E74616F62616F2E636F6D25324673656172636825334671253344253235453925323538302532353946253235453525323542412532354136253235453925323538302532353946253235453525323542412532354136253236696D6766696C65253344253236636F6D6D656E64253344616C6C2532367373696425334473352D652532367365617263685F747970652533446974656D253236736F75726365496425334474622E696E64657825323673706D253344613231626F2E323031372E3230313835362D74616F62616F2D6974656D2E31253236696525334475746638253236696E69746961746976655F69642533447462696E6465787A5F3230313730333036',
            'TPL_password_2': self.TPL_password2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'oslanguage': 'zh-CN',
            'sr': '1440*900',
            'osVer': 'macos|10.145',
            'naviVer': 'chrome|76.038091',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'osPF': 'MacIntel',
            'appkey': '00000000',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?redirectURL=https://s.taobao.com/search?q=%E9%80%9F%E5%BA%A6%E9%80%9F%E5%BA%A6&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&useMobile=true',
            'showAssistantLink': '',
            'um_token': 'T898C0FDF1A3CEE5389D682340C5F299FFE590F51543C8E3DDA8341C869',
            'ua': self.ua
        }
        try:
            response = s.post(self.verify_password_url, headers=verify_password_headers, data=verify_password_data,
                              timeout=self.timeout)
            response.raise_for_status()
            # 从返回的页面中提取申请st码地址
        except Exception as e:
            print('验证用户名和密码请求失败，原因：')
            raise e
        # 提取申请st码url
        apply_st_url_match = re.search(r'<script src="(.*?)"></script>', response.text)
        # 存在则返回
        if apply_st_url_match:
            print('验证用户名密码成功，st码申请地址：{}'.format(apply_st_url_match.group(1)))
            return apply_st_url_match.group(1)
        else:
            raise RuntimeError('用户名密码验证失败！response：{}'.format(response.text))

    def _apply_st(self):
        """
        申请st码
        :return: st码
        """
        apply_st_url = self._verify_password()
        try:
            response = s.get(apply_st_url)
            response.raise_for_status()
        except Exception as e:
            print('申请st码请求失败，原因：')
            raise e
        st_match = re.search(r'"data":{"st":"(.*?)"}', response.text)
        if st_match:
            print('获取st码成功，st码：{}'.format(st_match.group(1)))
            return st_match.group(1)
        else:
            raise RuntimeError('获取st码失败！response：{}'.format(response.text))

    def login(self):
        """
        使用st码登录
        :return:
        """
        # 目前requests库还没有很好的办法破解淘宝滑块验证
        self._user_check()
        st = self._apply_st()
        headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = s.get(self.vst_url.format(st), headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('st码登录请求，原因：')
            raise e
        # 登录成功，提取跳转淘宝用户主页url
        my_taobao_match = re.search(r'top.location.href = "(.*?)"', response.text)
        if my_taobao_match:
            print('登录淘宝成功，跳转链接：{}'.format(my_taobao_match.group(1)))
            return my_taobao_match.group(1)
        else:
            raise RuntimeError('登录失败！response：{}'.format(response.text))

    def get_taobao_nick_name(self):
        """
        获取淘宝昵称
        :return: 淘宝昵称
        """
        # 淘宝用户主页url
        my_taobao_url = self.login()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = s.get(my_taobao_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('获取淘宝主页请求失败！原因：')
            raise e
        # 提取淘宝昵称
        nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if nick_name_match:
            print('骚呢，兄弟：{}'.format(nick_name_match.group(1)))
            return nick_name_match.group(1)
        else:
            raise RuntimeError('获取淘宝昵称失败！response：{}'.format(response.text))


if __name__ == '__main__':
    # 淘宝用户名
    username = '你的淘宝账号'
    # 淘宝重要参数，从浏览器或抓包工具中复制，可重复使用
    ua = ua = '119#MlKma56msEckrMMzpwSCmgNzxbdQaRlcBPmaXIoz1usOCPPTlaAYXAvkIAl6Tg2dmQPTrKdo29CxyU/mLlGMarUsz9bGztA8RJBONt7J9CiLfBMKME3fx2Nqk/xMdGLWRU6O8t7M5x2omSgOwtNLfU+S4lkGdoHsRIVXNEFL9eAzMSTozSo8uJOqBtmOyaHCRSVJcF8L8xqzRBsUdA3q9U+SLgR+deF7yJShN8lL9dXzRPqLo+Y8q2vp499wde3lR2KVt9kLEhEzR/sU3AFh9UNltxhLSHr8y2SVNEH093ASRPSM2IRe9/sdLUq7+MMOqC9gSCqOfoerT6smYcVg5JqMfCr70SmjkQVwgE7l+3grCrjB6Sc4xGvCtyLxy197yTuyzTUCQL3ItdRejyQq8hPbRuvwxi68oUWwdilfcUAQc0yTRhWEcwDbcFvDFG+nYdPvylWaIOAGUlsrTKWdppT7iLVsNH/Fnh088EtTbL+pBSbjWj5Pa8/fnARp/MZ6BEmHE+mDR7RDvhJfdhNaxHrGadtaGmbVvHYo0oR6wWqiOkSfH2vD9TqEpp4amiEByxXMG+JMFNin+TFzA/FxLpIqGUzIO/vKtVv6jhy0GWosbEz1YHSkXkPM8m455opHcnWeKNtKQSUGtljeUW4da8T7SeEE1DZjeQBqZagX2CVkZqSMeTE5slss8IYeC0FL14tBih8cLP+zuAEikLq35Fv9e75A/p+Yp2Qb8PZoacMTxyhxOMvJZ64+RxSTQskuJx4GIbifdptOpIUdiwe+BSh3k9nq6WEEaP0eX6u9ZXoSLs7BoZtHJ74Mu2Au+q+zAHG4fUBGKdOvLb/7iwy3yXofRIUsKNFnADN/sezd4l0/aZfcFL9LicBF3SMKBJkgagHgzLkjZfOiWs68UtO0MAIHMSyI3zrG+QdZRehgbbjGYLlwzbfEzToF1aKi+2t8wdUORclDXthMsTTzb5bhCcJjwY/Ms8+0STdOUsC6paC9svXcF7pPxuTtGY/7IWM260DuzGDYe8Q9GU2zFrFVyiYXBjY3ZGmfgsuMP/iDswoO23eucC9dYHRoK0IMHHHDOFDMAA016r400YX6eg47FIVexIF1pNCzhZvXTnBCbDgTT6nvcokIWAyd0kVwH33Sgap4Z3rj5rQyaAVwsUpH2hjve0lBNasoMfOr/hUuyIS5DHodjsZCO+nKqRKEPUryHf7Ma9v5g5J46kF5lL0aJMf6kxJhcSvaNMa4dWVhsk3UyDPG5xdRZBO6e2OlimMoN7f8AbVfZF9LJrBiVSgDWgq1zBC/tNhg7Wm+aLf+VxbtAxr1CjtSt89mGdDCUr9LWftfHyncXh1ub6A2HRBcfah9M/Rru13An1WGWqOf8Xh7QSRdDn3fOEVl/SesmxJyDKkE61/Ri3h7h+W2n87nmgIaAIVg8ovsFIN0OZm6J2CyxgCjis2GuCLurnSCAFgiRsm9IP6PQLk5/3llWSrFmVoDDtfJD9P5apjuae5IqWfJWiMfvyEfTevqmufTTTS+w74lFv6OSHMK3yI5P0Z1/CYipvytIx+l8X6SHj19NizLJPWkMimJXAp4Fy3hebN85g5N7oYrjdDYonYrIo0eN1Ps6iCIz5dOCRPd0GIWpMSsFDx9IzVcwUzdU0Wfa+zmMpBsPHquxm/pJTkSV/KVEQf4cw7Q'
    # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
    TPL_password2 = '8a65e84dbd099e3eb728bfbbbf6ecb2b759b50745120e186ad94b171e369dac0d877d0c816d49898ea166d2842469dcec0435e88d4f534ee502967eafd30976ca0424f9c4a65bfb8b27c1cd8cf68a3c94be4fb7bd4102095f34cfbfca2649eee9ac3ee3d2785789fc4de15279cfab6d6984c90ab557bb1ee83c187a4fd25698d'
    ul = UsernameLogin(username, ua, TPL_password2)
    ul.get_taobao_nick_name()
