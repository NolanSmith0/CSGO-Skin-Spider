import buff
from datetime import datetime
import pandas as pd

target_types = [
    'AK47', 
    'M4A1', 
    'M4A4',
    'Galilar',
    'Deagle', 
    'USP', 
    'Glock', 
    'Tec-9',
    'Butterfly',
    'M9',
    'Karambit',
    'Skeleton',
    'Widowmaker'
]

headers = [
    # lzh
    {'Cookie' : 'Device-Id=YLXa2smvtbqQze3FhdOU; csrf_token=Ijg0ODJhZTYzMTc0NjY4NWQ1ODIzNmM2Y2QzZjAzOWRjMTcyOGIyZjci.GSxsbw.IjhblwUnta3x--SBKPxAcTzyhrw; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=8FeFArgiwMRe_AN4oWMGyNi1ZwhfD7mI1oJWULu_SSCKQkujQqfOaEPB4dcKyQPSpCIQ2s_sX8yA9hio4D10fMwaSgK.ZPlJTFS3nsoRwZQjfNtzJAqbSe.Sl4V24UJDJPsejj6IDYMaXkbtqQ4YIMlqbEriVSdC3cK5Lxl6Its.8Z0wj1BrAw7.gvsfSPEXzkgXNYt42b7TQqfFUe.Fih5jd_3uRqEB33pwnJoO0AiKm; S_INFO=1716181669|0|0&60##|15053740127; P_INFO=15053740127|1716181669|1|netease_buff|00&99|null&null&null#shd&370100#10#0|&0||15053740127; remember_me=U1098288149|kD0uXHKctzysoDeEsL1sz5dqm7wmuV6z; session=1-unvEhHLlXO560zGCJplh6_1by8_ZaE_ke-sn_4naMIwk2042106701'},
    # wjh
    {'Cookie' : 'Device-Id=cT8OdygrK14bDvGbWpIT; game=csgo; qr_code_verify_ticket=2aeL9LM44e8de92a3d86460bc3e568d628b1; remember_me=U1096419965|KTAaMPlgCtmpBlMbdiPuf70iJ3Lemh0d; session=1-c2vffS8JRHGYbfndrQWmqTSCAnzuiyihcVmZw-qmEnaa2039780645; Locale-Supported=zh-Hans; csrf_token=ImJiMDZiMzJiYTE0ZTY1NGY2MTQxYjBhNmUwMDY3NTk1YjkzMTgxODci.GSueHA._rMpwX9nHdw9q45plqd8lp5LXI0'},
    # wym
    {'Cookie' : 'Device-Id=832kNOor4Txs44LQJrp3; P_INFO=18518022855|1716951103|1|netease_buff|00&99|null&null&null#US&null#10#0|&0||18518022855; remember_me=U1103533064|Rg0n7ywBlmOqo49KRaHpHm6cfC7AmDU7; session=1-jL9N1Hk3jeq3iQffFRBr15cJSBqYyStY5v0YuR_JMYsO2030570320; csrf_token=ImE5MDEzMTRiOTJiOTZhODg0NjFhMzA0NTZkZmVhNWI2MjY5MjA4ZWUi.GTgrYQ.wjF7nhcow1w7tonXPoM_AsYz41o; Locale-Supported=zh-Hans; game=csgo'}
]

save_path = 'E:/Notebook/CSGO Spider/data/'

if __name__ == "__main__":
    buff_scraper = buff.Buff_bot(target_types, headers)
    data = buff_scraper.run()
    pd.DataFrame(buff_scraper.data).to_csv(f'{save_path}{datetime.now().date()}.csv', index=False)