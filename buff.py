# 网易buff CS2皮肤交易信息爬取
# Created by nolan
# 代理IP购买 ：https://www.xiaoxiangdaili.com/
# 短信接收平台 : https://lubansms.com/

#----------------------------------------------------------------------------
# 每页20个皮肤展示的API ：
# Domain : https://buff.163.com/api/market/goods
# Parameters : ?game=csgo&page_num=1&category={这里是皮肤type}&sort_by=sell_num.desc&tab=selling&use_suggestion=0

# 单个皮肤的API (第一页也就是前十底的在售无需登录，其他需要)：
# Domain : https://buff.163.com/api/market/goods/sell_order
# Paramters : ?game=csgo&goods_id={这里是皮肤id}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1

import requests
from datetime import datetime
from time import sleep

# parameters
types = {
    # 步枪
    'AK47': 'weapon_ak47',
    'M4A1': 'weapon_m4a1_silencer',
    'M4A4': 'weapon_m4a1',
    'Galilar': 'weapon_galilar',
    'AUG': 'weapon_aug',
    'SG553': 'weapon_sg556',
    'Famas': 'weapon_famas',
    'SSG08': 'weapon_ssg08',
    'Scar20': 'weapon_scar20',
    'G3sg1': 'weapon_g3sg1',
    'AWP': 'weapon_awp',
    # 手枪
    'Deagle': 'weapon_deagle',
    'USP': 'weapon_usp_silencer',
    'Glock': 'weapon_glock',
    'P2000': 'weapon_hkp2000',
    'P250': 'weapon_p250',
    'FN57': 'weapon_fiveseven',
    'R8': 'weapon_revolver',
    'Tec-9': 'weapon_tec9',
    'Elite': 'weapon_elite',  #双枪
    'CZ75': 'weapon_cz75a',
    'Zeus': 'weapon_zeus',
    # 冲锋枪
    'MP9': 'weapon_mp9',
    'Mac-10': 'weapon_mac10',
    'Ump-45': 'weapon_ump45',
    'P90': 'weapon_p90',
    'MP7': 'weapon_mp7',
    'Bizon': 'weapon_bizon',  #野牛
    'MP5-SD': 'weapon_mp5sd',
    # 短枪
    'XM1014': 'weapon_xm1014',
    'MAG-7': 'weapon_mag7',
    'Sawedoff': 'weapon_sawedoff', #截短霰弹枪
    'Nova': 'weapon_nova',
    # 刀
    'Butterfly': 'weapon_knife_butterfly',
    'M9': 'weapon_knife_m9_bayonet',
    'Karambit': 'weapon_knife_karambit',  #爪子刀
    'KKE': 'weapon_knife_kke',   #廓尔喀刀
    'Skeleton': 'weapon_knife_skeleton',  #骷髅匕首
    'Bayonet': 'weapon_bayonet',  #刺刀
    'Widowmaker': 'weapon_knife_widowmaker',  #锯齿爪刀
    'Outdoor': 'weapon_knife_outdoor',  #流浪者匕首
    'Flip': 'weapon_knife_flip',  #折叠刀
    'Stiletto': 'weapon_knife_stiletto',  #短剑
    'CSS': 'weapon_knife_css',  #海豹短刀
    'Ursus': 'weapon_knife_ursus',  #熊刀
    'Tactical': 'weapon_knife_tactical',  #猎杀者匕首
    'Cord': 'weapon_knife_cord',  #系绳匕首
    'Canis': 'weapon_knife_canis',  #求生匕首
    'Falchion': 'weapon_knife_falchion',  #弯刀
    'Push': 'weapon_knife_push',  #暗影双刃
    'Bowie': 'weapon_knife_survival_bowie',  #鲍伊猎刀
    'Gut': 'weapon_knife_gut',  #穿肠刀
    'Jackknife': 'weapon_knife_gypsy_jackknife' #折刀
}

# buff bot
class Buff_bot():

    def __init__(self, types, headers, sleep_time=2.5):
        '''
        types : list of string, the skins types you want to collect
        headers : list of dic, the buff headers you need, 5 types per day(for account safety)
        data : list of dic, the collected data
        failed : dic, the failed pages
        '''
        self.types = types
        self.headers = headers
        self.data = []
        self.failed = {}
        self.sleep_time = sleep_time

    def run(self):
        # testing all headers
        print('Testing headers...')
        for i, header in enumerate(self.headers):
            if not self.test(header):
                print(f'{i+1}th header failed the test. pls check again')
                return None
        print('All headers passed.')
        sleep(2)

        # split the task
        for type in self.types:
            if type not in types:
                print(f'{type} is not in the types list, pls check again.')
                return None
        self.types = split_series(self.types, len(self.headers))
        print('Types are splitted into following parts:')
        for type in self.types:
            print(type)

        # start running
        for i, header in enumerate(self.headers):
            for type in self.types[i]:
                print(f'Collecting {type} skins...')
                url = get_api_url(types[type])
                data, fail = self.collect_type(url, header, sleep_time=self.sleep_time)
                self.data += data
                self.failed[type] = fail
                
        return self.data

    def test(self, header):
        '''
        Testing connection.
        '''
        test_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&category_group=knife&tab=selling&use_suggestion=0'
        test_res = requests.get(test_url, headers=header)
        if test_res.json()['code'] == 'OK':
            return True
        return False

    def collect_type(self, url, headers, sleep_time):
        '''
        Collecting the sell(buy) min price and num based on skin type.
        Need user account, very easy to be banned, 4 types per day for one account is recommended.
        '''
        current_page = 0
        data, failed = [], []
        test = urlGet(url, headers)
        if test == None:
            print('Failed to connect, pls check again')
            return None, None
        total_page = test.json()['data']['total_page']
        data += parse(test)
        current_page += 1
        print(f'Now in page {current_page} / {total_page}', end='\r')
        while current_page < total_page:
            url = url.replace(f'page_num={current_page}', f'page_num={current_page+1}')
            current_page += 1
            response = urlGet(url, headers)
            print(f'Now in page {current_page} / {total_page}', end='\r')
            if response == None:
                sleep(sleep_time)
                failed.append(current_page)
                continue
            data += parse(response)
            sleep(sleep_time)
    
        print(f'Task Finished, {len(failed)} pages failed')
    
        return data, failed

# get api url
def get_api_url(skin_type):
    api_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&category=TYPE&sort_by=sell_num.desc&tab=selling&use_suggestion=0'
    return api_url.replace('category=TYPE', f'category={skin_type}')

# self imporved url get function
def urlGet(url, headers, max_try=3, sleep_time=5):
    '''
    self designed url get request using requests
    '''
    not_connected = True
    tried = 0
    while not_connected and tried < max_try:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                sleep(sleep_time)
            else:
                not_connected = False
            tried += 1
        except:
            sleep(sleep_time)
            tried += 1
    if tried == max_try:
        return None
    
    return response

# split sereis into n parts
def split_series(series, n):

    total_elements = len(series)
    elements_per_partition, remainder = divmod(total_elements, n)

    start = 0
    partitions = []

    for i in range(n):
        end = start + elements_per_partition + (1 if i < remainder else 0)
        partition = series[start:end]
        partitions.append(partition)
        start = end

    return partitions

# parse the response json file from buff
def parse(response):
    output = []
    date = str(datetime.now().date())
    data = response.json()['data']['items']
    for i in data:
        tem = {}
        tem['id'] = i['id']
        tem['data_date'] = date
        tem['skin_name'] = i['name']
        tem['short_name'] = i['short_name']
        tem['sell_min_price'] = i['sell_min_price']
        tem['sell_num'] = i['sell_num']
        tem['buy_max_price'] = i['buy_max_price']
        tem['buy_num'] = i['buy_num']
        
        for tag in i['goods_info']['info']['tags']:
            tem[tag] = i['goods_info']['info']['tags'][tag]['localized_name']
            
        tem['steam_price'] = i['goods_info']['steam_price']
        tem['steam_price_cny'] = i['goods_info']['steam_price_cny']
        
        output.append(tem)
    return output

# new collecting function
