import json
import pprint 
import pytz
import pandas as pd
import numpy as np
import requests
import os
import time
import oauth2 as oauth 
import time
import datetime
import multiprocessing
import warnings
warnings.filterwarnings('ignore')

# ------- 본인 토큰으로 수정 필요 -------
APP_KEY = "PSNeOvV92SiRB7a1bbXLYBJt8nuQNicHhLNQ"
APP_SECRET = "Qxud73tJ6NDVGoSXNQckFzJbv7oPI08Q"
# -------------------------------------
count = 0

def access_token(APP_KEY,APP_SECRET):
    header = {"content-type":"application/x-www-form-urlencoded"}
    param = {"grant_type":"client_credentials",
            "appkey":APP_KEY,
            "appsecretkey":APP_SECRET,
            "scope":"oob"
            }
    PATH = "oauth2/token"
    BASE_URL = "https://openapi.ebestsec.co.kr:8080"
    URL = f"{BASE_URL}/{PATH}"

    request = requests.post(URL, verify=False, headers=header, params=param ,timeout=3)

    if __name__ == "__main__":
        print("URL          : ", URL, "\n")               
        print("OAuth        : ")
        pprint.pprint(request.json()) 
    
    ACCESS_TOKEN = request.json()["access_token"] 

    return ACCESS_TOKEN


class t1101:
    def t1101(shcode = None, todt = "", period = 365, acc_tk="") :
        """
        eBest Open API에서 t1716 TR을 호출하기 위한 URL, 헤더 및 바디 정보를 반환하는 함수입니다.

        Parameters:
            shcode (str, optional)  : 종목코드를 지정하는 매개변수입니다.
            todt (str, optional)    : 조회를 종료할 날짜를 지정하는 매개변수입니다. 기본값은 오늘 날짜로 설정됩니다.
            period (int, optional)  : 조회 기간을 지정하는 매개변수입니다. 기본값은 365일(1년)입니다.

        Returns:
            tuple                   : url, 헤더, 바디 정보, 함수 이름, 반환 데이터 태그, 종목코드를 포함하는 튜플을 반환합니다.
        """

        _url_base   = "https://openapi.ebestsec.co.kr:8080"
        _path       = "stock/market-data"
        _url        = f"{_url_base}/{_path}"

        _header     = {
            "content-type"  : "application/json; charset=UTF-8",
            "authorization" : acc_tk,
            "tr_cd"         : "t1101",
            "tr_cont"       : "N",
            "tr_cont_key"   : "",
        }

        _body           ={
            "t1101InBlock" : {
                "shcode" : shcode,
            }
        }

        _out_block_tag = "OutBlock"

        return _url, _header, _body, t1101.t1101.__name__, _out_block_tag, shcode
    
    
def request_tr(url, header, body, tr_name, out_block_tag, shcode,ACCESS_TOKEN):
    """
    eBest Open API에서 TR을 호출하여 데이터를 조회하는 함수입니다.

    Parameters:
        url (str)           : API 호출을 위한 URL입니다.
        header (dict)       : API 호출에 필요한 헤더 정보가 담긴 딕셔너리입니다.
        body (dict)         : API 호출에 필요한 바디 정보가 담긴 딕셔너리입니다.
        tr_name (str)       : 함수 이름입니다.
        out_block_tag (str) : 반환 데이터의 태그입니다.
        shcode (str)        : 종목코드를 지정하는 매개변수입니다.
        ACCESS_TOKEN (str)  : access_token(APP_KEY,APP_SECRET)메소드로 반한된 접근 토큰입니다.
    Returns:
        pandas.DataFrame    : 조회된 데이터가 담긴 DataFrame 객체를 반환합니다.
        str                 : 함수 이름을 반환합니다.
        str                 : 종목코드를 반환합니다.
    """

    header["authorization"] = f"Bearer {ACCESS_TOKEN}"
    _res = requests.post(url, headers=header, data=json.dumps(body), timeout=3.2)   #지정된 시간내에 응답이 오지 않으면 예외가 발생하므로 try/except 구문설정하기
    _json_data = _res.json()
    _data_frame = pd.json_normalize(_json_data[f"{tr_name}{out_block_tag}"])    #json양식을 데이터 프레임으로 바꾸기

    return _data_frame, tr_name, shcode


def save_csv(data_frame, tr_name, shcode=""):
    """
    조회된 데이터를 CSV 파일로 저장하는 함수입니다.

    Parameters:
        data_frame (pandas.DataFrame) : 조회된 데이터가 담긴 DataFrame 객체입니다.
        tr_name (str)                 : 저장할 파일의 이름을 지정하는 매개변수입니다.
        shcode (str, optional)        : 종목코드를 지정하는 매개변수입니다. 기본값은 ""(빈 문자열)입니다.

    Returns:
        None
    """

    _seoul_timezone = pytz.timezone('Asia/Seoul')
    _time_stamp = datetime.datetime.now(_seoul_timezone).strftime("%Y%m%d")
    
    # 경로 수정 필요
    if len(shcode) > 0:
        _path = f'D:\csv\{_time_stamp}_{shcode}.csv'
    else:
        _path = f'D:\csv\{_time_stamp}_{shcode}.csv'
            
    global count 
    count += 1       
    if os.path.exists(_path):
        # If the file already exists, append the data
        data_frame.to_csv(_path, mode='a', header=False, index=False)
        print(f'{shcode} : {count}')
    else:
        # If the file does not exist, create a new file
        data_frame.to_csv(_path, index=False)
        print(f"새로운 파일을 생성 {shcode} : {count}")
        


def mainFunc(code):
    acc_tk_main=access_token(APP_KEY,APP_SECRET)
    while True:   
        results, tr_name, shcode = request_tr(*t1101.t1101(shcode=code, period=365, acc_tk=acc_tk_main), ACCESS_TOKEN=acc_tk_main)
        save_csv(results, tr_name, shcode)
        current_time = datetime.datetime.now().time()
        if current_time.hour == 15 and current_time.minute == 31:
            print("현재 시간이 15:31이므로 프로그램을 종료합니다.")
            break
        time.sleep(0.34)

def run_at_specific_time(dd):
    current_time = datetime.datetime.now().strftime("%H%M")
    target_time = dd
    while current_time != target_time:
        time.sleep(0.05)
        current_time = datetime.datetime.now().strftime("%H%M")



if __name__ == '__main__':
    run_at_specific_time('0859')
    procs = []
    # 종목 코드 3개 수정 필요
    for i in ['069500',"005380",'006400']:
        p = multiprocessing.Process(target=mainFunc, args=(i, ))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()



