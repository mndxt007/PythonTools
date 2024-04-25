#pyinstaller --onefile -i .\resources\logo.ico .\httpload.py

# %%
import xlsxwriter
import asyncio
import requests
from datetime import datetime
import urllib3
urllib3.disable_warnings()
import os



# %%
def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    return wrapped

@background
def httpattack(reqnum,url,reqtotal,worksheet,workbook):
    try:
        worksheet.write(reqnum,0,reqnum-1)
        curtime = datetime.now()
        worksheet.write(reqnum,2,curtime.strftime("%m/%d/%Y, %H:%M:%S"))
        try:
            r = requests.get(url+str(str("?")+str(reqnum-1)), verify=False)
            worksheet.write(reqnum,1,r.status_code)
            if (r.status_code > 499):
                #worksheet.write(reqnum,5,str(r.text))
                pass
            status = r.status_code
            if r.history:
                worksheet.write(reqnum,6,str(r.history))
                worksheet.write(reqnum,7,r.url)
        except Exception as e:
             worksheet.write(reqnum,5,str(e))
             print("Request",reqnum-1,"failed :",e)
             status = -1
        finally:
            delta = datetime.now()- curtime
            worksheet.write(reqnum,3,datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            timetaken = str(delta.seconds)+"."+str(delta.microseconds)[:3]
            worksheet.write(reqnum,4,timetaken)
            print("Completed HTTP request for ",reqnum-1,"in",timetaken,"with response",status)
    except Exception as e:
             print(e)

# %%
async def httpreq(url,reqtotal,worksheet,workbook):
    for reqnum in range(reqtotal):
        httpattack(reqnum+2,url,reqtotal,worksheet,workbook)

# %%
while True:
    try:
        workbook = xlsxwriter.Workbook('httpattack.xlsx')
        worksheet = workbook.add_worksheet()
        print(" HTTP Load Tester ".center((os.get_terminal_size().columns),"*"))
        url = input("Enter URL: ")
        reqtotal = int(input("Enter number of tests: "))
        worksheet.write(0,0,url)
        headers = ["Request Number", "Request Status", "Request Start", "Request End", "Time Taken","Exception","History","URL"]
        worksheet.set_column(0,8,20)
        worksheet.write_row(1,0,headers)
        asyncio.run(httpreq(url,reqtotal,worksheet,workbook))
        workbook.close()
        if(input("Open report file? (y/n) : ").capitalize()=='Y'):
            os.system("httpattack.xlsx")
        if (input("Rerun load test? (y/n) :  ").capitalize() == 'Y'):
            pass
        else: 
            break
        os.system("cls")
    except Exception as e:
                print(e)
# %%
