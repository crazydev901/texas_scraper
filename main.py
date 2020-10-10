import requests
import smtplib
import time

def emailSent(messageTexas):

    preMessage = 'Incident  RN	RE Name	Began	Ended	Event Type	Report Type	Report Date	Associated Customer'

    server = smtplib.SMTP('smtp.live.com', 587)

    SUBJECT = "Texas Air Emission Event Report!"
    TEXT = preMessage + '\n' + messageTexas

    # Prepare actual message
    try:
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('texas_scraper@outlook.com', 'asdf234%^AFE')
        server.sendmail("texas_scraper@outlook.com", "texas_scraper@outlook.com", message)
        server.quit()
        print('[#] Email is sent!')
    except:
        print('[#] Email cannot be sent!')


def main():
    print('[#] Texas scraper has been started!')
    while(True):
        dosya =  open('rawData.txt', 'a+')
        logCheck = open('rawData.txt', 'r').readlines()

        url = 'https://www2.tceq.texas.gov/oce/eer/index.cfm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                   #'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
                   'Host': 'www2.tceq.texas.gov',
                   'Origin': 'https://www2.tceq.texas.gov',
                    'Referer': 'https://www2.tceq.texas.gov/oce/eer/index.cfm'}

        postData = {
            "newsearch": "yes",
            "incid_track_num":"" ,
            "event_start_beg_dt": "",
            "event_start_end_dt": "",
            "event_end_beg_dt": "",
            "event_end_end_dt": "",
            "cn_txt": "",
            "cust_name": "",
            "rn_txt": "",
            "re_name": "Freeport LNG",
            "ls_cnty_name": "",
            "ls_region_cd": "",
            "ls_event_typ_cd": "",
            "_fuseaction=main.searchresults.x": "20",
            "_fuseaction=main.searchresults.y": "17",
        }
        try:
            req = requests.post(url, data=postData, headers=headers)
            rawdata = req.text
        except:
            continue
        j = 0
        resultFinalSent = ''

        try:
            for i in range(1,20):
                data = rawdata.split('index.cfm?fuseaction=main.getDetails&amp;target=')
                incident = rawdata.split('index.cfm?fuseaction=main.getDetails&amp;target=')[i].split('"')[0]
                dataFinal = data[i].split('<td>')
                resultFinal = incident
                for dataFinal2 in dataFinal:
                    result = dataFinal2.split("</td>")[0].strip()
                    if 'href=' not in result and '</a>' not in result:
                        resultFinal = resultFinal + ' ' + result
                logCheckID = [logCheck[i].split('\n')[0] for i in range(0, len(logCheck))]
                if str(incident) not in logCheckID:
                    j+=1
                    #print('[#] New update is found!')
                    dosya.write(incident + '\n')
                    resultFinalSent = resultFinalSent + '\n' + resultFinal
            if resultFinalSent != '':
                print('New updates are ...')
                print(resultFinalSent)
                emailSent(resultFinalSent)

            dosya.close()
        except Exception as e:
            print(f'[#] There is a problem in texas website, error is {e}')
        print('[#] Sleeping 5 min..')
        time.sleep(300)
if __name__ == '__main__':
    main()
