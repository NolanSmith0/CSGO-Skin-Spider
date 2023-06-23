import requests
import re
from datetime import datetime
import pandas as pd
from threading import Thread
import os
from bs4 import BeautifulSoup
from time import sleep

# Main function
def GetData(urls):
    global Data
    global time
    global failed_urls
    global FinishedLength
    global NumOfFailed
    global now
    
    def CollectOneURL(url):
        
        all_data = []

        data = {}

        buff = requests.get(url)

        while buff.status_code != 200:
            sleep(1)
            buff = requests.get(url)

        soup = BeautifulSoup(buff.text, 'html.parser')
        
        # time
        data['Time'] = time

        # full name
        data['Full_name'] = soup.select('div.market-list h1')[0].get_text()
        
        # skin name
        skin_name = data['Full_name'][:data['Full_name'].index('(')]

        # quality type and kind
        a = soup.select('div[class="detail-header black"]')[0].find('p').get_text().strip().split('|')

        data['Quality'] = a[1].split(' ')[0]
        data['Type'] = a[2][:-4]
        data['Kind'] = a[-1]

        # exterior
        data['Exterior'] = soup.select_one('div.scope-btns a[class="i_Btn i_Btn_trans_bule active"]').next_sibling.strip()

        # price
        data['Price'] = soup.select_one('div.scope-btns a[class="i_Btn i_Btn_trans_bule active"]').next_sibling.next_sibling['data-price']

        # num of on sale
        data['OnSale'] = soup.select('ul.new-tab li[class="selling on"] a[href="javascript:;"]')[0].get_text()
        
        all_data.append(data)
        
        # other exterior
        for i in [(i.get_text().strip(), i.find('span')) for i in soup.select('div.scope-btns a[class="i_Btn i_Btn_trans_bule j_Goods-jump"]')]:
            if i[0] not in ['崭新出厂', '略有磨损', '久经沙场', '战痕累累', '破损不堪']:
                continue
            else:
                data = {}
                data['Time'] = time
                data['Full_name'] = skin_name + '(' + i[0] + ')'
                data['Quality'] = a[1].split(' ')[0]
                data['Type'] = a[2].split(' ')[0]
                data['Kind'] = a[-1]
                data['Exterior'] = i[0]
                data['Price'] = i[1]['data-price']
                data['OnSale'] = soup.select('ul.new-tab li[class="selling on"] a[href="javascript:;"]')[0].get_text()
                all_data.append(data)
        
        return all_data
    
    for url in urls:
        try:
            Data += CollectOneURL(url)
            #print(f'URL \033[1;32m{url}\033[0m Collected !'.center(70, ' '), end='\r')
        except:
            failed_urls.add(url)
            NumOfFailed += 1
            #print(f'URL \033[1;31m{url}\033[0m Failed......'.center(70, ' '), end='\r')
        FinishedLength += 1
        percent = round((FinishedLength / TaskLength)*100, 2)

        # Print out information about the collecting process
        if FinishedLength > 10:
            ExpectedTime = int(float(((datetime.now() - now).total_seconds() / FinishedLength)*(TaskLength - FinishedLength)))
            ExpectedTime = '{}h {}min {}sec'.format(ExpectedTime // 3600, (ExpectedTime % 3600) // 60, ExpectedTime % 60)
        else:
            ExpectedTime = '......'
        
        sleep(1)
        
        print(f'Finished: \033[1;32m{percent}\033[0m%. Time to finish: \033[1;32m{ExpectedTime}\033[0m . Num of Failed: \033[1;31m{NumOfFailed}\033[0m / {FinishedLength}'.center(75, ' '), end='\r')
        
            
    return None
    

# IGXE collection
def GetDataIGXE(urls):
    global Data_IGXE
    global time
    global failed_urls
    global FinishedLength
    global NumOfFailed
    global now
    
    def CollectOneURL(url):
        
        all_data = []

        igxe = requests.get(url)

        while igxe.status_code != 200:
            sleep(3)
            igxe = requests.get(url)

        soup = BeautifulSoup(igxe.text, 'html.parser')

        # full name
        Full_name = soup.select_one('#id-box4-vue > div.com-wrapper > div.productDetailsCn > div > div.productInfo.csgoInfo.csgoInfo2 > div.infobok > div.txt > div.name').get_text()

        # skin name
        if '(' in Full_name:
            skin_name = Full_name[:Full_name.index('(')].strip()
        else:
            skin_name = Full_name

        # quality
        Quality = soup.select_one('#id-box4-vue > div.com-wrapper > div.productDetailsCn > div > div.productInfo.csgoInfo.csgoInfo2 > div.infobok > div.txt > div.rarity.mt-30 > span:nth-child(4)').get_text()

        all_exterior = soup.select('div.parts-bok a[class="a-but"]') + soup.select('div.parts-bok a[class="a-but select"]')
        
        for i in all_exterior:

            try:
                
                # Exterior
                pattern1 = r'(.+?)\n'
                exterior = re.findall(pattern1, i.get_text())[0].strip()

                # Price
                if '暂无在售' in i.get_text():
                    price = None
                else:
                    pattern2 = r'(\d+\.\d+)'
                    price = re.findall(pattern2, i.get_text())[0]
                
                if exterior not in ['崭新出厂', '略有磨损', '久经沙场', '战痕累累', '破损不堪']:
                    continue
                else:
                    data = {}
                    if exterior in Full_name:
                        data['Full_name'] = Full_name
                    else:
                        data['Full_name'] = skin_name + ' (' + exterior + ')'
                    data['skin_name'] = skin_name
                    data['Quality'] = Quality
                    data['Exterior'] = exterior
                    data['Price'] = price
                    all_data.append(data)
                    
            except:
                continue
        
        return all_data
    
    for url in urls:
        try:
            Data_IGXE += CollectOneURL(url)
            #print(f'URL \033[1;32m{url}\033[0m Collected !'.center(70, ' '), end='\r')
        except:
            failed_urls.add(url)
            NumOfFailed += 1
            #print(f'URL \033[1;31m{url}\033[0m Failed......'.center(70, ' '), end='\r')
        FinishedLength += 1
        percent = round((FinishedLength / TaskLength)*100, 2)
        if FinishedLength > 10:
            ExpectedTime = int(float(((datetime.now() - now).total_seconds() / FinishedLength)*(TaskLength - FinishedLength)))
            ExpectedTime = '{}h {}min {}sec'.format(ExpectedTime // 3600, (ExpectedTime % 3600) // 60, ExpectedTime % 60)
        else:
            ExpectedTime = '......'
        
        sleep(1)
        
        print(f'Finished: \033[1;32m{percent}\033[0m%. Time to finish: \033[1;32m{ExpectedTime}\033[0m . Num of Failed: \033[1;31m{NumOfFailed}\033[0m / {FinishedLength}'.center(75, ' '), end='\r')
        
            
    return None
    

if __name__ == '__main__':
    
    # preparing log
    failed_urls = set()
    NumOfThreading = 5
    now = datetime.now()
    time = f'{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}'
    FinishedLength = 0
    NumOfFailed = 0

    print(f'Collection Started ! Time: {time}'.center(70, '='))

    # Get URLs
    urls = pd.read_csv('./Buff_URLs.csv').values
    urls = [urls[i][0] for i in range(len(urls))]
    
    # preparing
    Data_IGXE = []
    Data = []

    # Get URLs
    urls_IGXE = pd.read_csv('./IGXE_URLs.csv').values
    urls_IGXE = [urls_IGXE[i][0] for i in range(len(urls_IGXE))]
    
    TaskLength = len(urls) + len(urls_IGXE)
    
    step1 = len(urls_IGXE) // NumOfThreading

    DividedUrls1 = [urls_IGXE[i*step1 : (i+1)*step1] for i in range(NumOfThreading - 1)] + [urls_IGXE[(NumOfThreading-1)*step1:]]
    
    step = len(urls) // NumOfThreading

    DividedUrls = [urls[i*step : (i+1)*step] for i in range(NumOfThreading - 1)] + [urls[(NumOfThreading - 1)*step:]]

    # Speed up using Thread
    threading_list = {}
    for num in range(NumOfThreading):
        threading_list[f'{num}'] = Thread(target=GetData, args=[DividedUrls[num]])

    for num in range(NumOfThreading):
        threading_list[f'{num}'].start()
        
    threading_list1 = {}
    for num in range(NumOfThreading):
        threading_list1[f'{num}'] = Thread(target=GetDataIGXE, args=[DividedUrls1[num]])

    for num in range(NumOfThreading):
        threading_list1[f'{num}'].start()
        sleep(0.2)
        
        
    for num in range(NumOfThreading):
        threading_list[f'{num}'].join()

    for num in range(NumOfThreading):
        threading_list1[f'{num}'].join()

    end = datetime.now()
    print(f'All Finished ! Time : {time} \033[1;32m>>>\033[0m {end.year}-{end.month}-{end.day} {end.hour}:{end.minute}')
    
    # Saving Data
    pd.DataFrame(Data).to_csv(f'./price_data/{time}.csv', index=False)
    pd.DataFrame(Data_IGXE).to_csv(f'./IGXE_price/{time}.csv', index=False)
    
    print('Data Saved Successfully !'.center(70, '='))
    
    if len(failed_urls) > 0:
        pd.Series(list(failed_urls)).to_csv(f'./wrong_url/{time}.csv', index=False)
