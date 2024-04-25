from bs4 import BeautifulSoup
import dateutil.parser
import os

import xml.etree.ElementTree as ET

import xlsxwriter
import dateutil.parser



#To do - Add async
#path2 = """D:\\Case\\2303040030000252_Pramod\\2023-03-04\\2\\2\\Freb"""



try:
    path2 = input("Enter fully qualified path where the freb file is present: ")
    files = os.listdir(path2)
    workbook = xlsxwriter.Workbook(str(path2+'\\Summary.xlsx'))
    try:
        for file in files:
            try:
                if file[-3:] != "xml":
                    continue
                row = 0
                first = False
                worksheet = workbook.add_worksheet()
                worksheet.set_column(row,0,20)
                worksheet.set_column(row,1,20)
                worksheet.set_column(row,2,80)
                worksheet.set_column(row,3,20)
                tree = ET.parse(str(path2+"\\"+file))
                root = tree.getroot()
                title = "filename="+file+"url="+root.attrib.get("url")+"  "+"verb="+root.attrib.get("verb")+"  "+"statusCode="+root.attrib.get("statusCode")+"  "+"timeTaken="+root.attrib.get("timeTaken")+"  "
                worksheet.write(row,0,title);row+=1;
                headers = ["EventName", "UTCTime","Details","timedelta"]
                worksheet.write_row(row,0,headers);row+=1;
                with open(str(path2+"\\"+file), 'r') as f:
                    data = f.read()
                Bs_data = BeautifulSoup(data, "xml")

                for items in Bs_data.findAll('Event'):
                    worksheet.write(row,0,items.find('RenderingInfo').find('Opcode').text)
                    times = items.find('TimeCreated').get('SystemTime')
                    worksheet.write(row,1,times)
                    time = dateutil.parser.isoparse(times)
                    if first:
                        timedelta=time-timeprev
                        worksheet.write(row,3,str(timedelta.seconds)+'.'+str(timedelta.microseconds//1000))
                        timeprev=time
                        if timedelta.seconds > 0:
                            pass
                    else:
                        timeprev = time
                        first=True
                    details= """"""
                    for data in items.findAll('Data'):
                        if data.get('Name')!="ContextId":
                            details+=str(data.get('Name')+'='+data.text+"    ")
                    worksheet.write(row,2,details)
                    row+=1
                print("Processing completed for",file)
            except Exception as e:
                print("Processing failed for",file)
                print(e)
                continue

    except Exception as e:
        print("Processing failed for",file)
        print(e)      
    finally:
        workbook.close()
except Exception as e:
        print(e)
finally:
    print("Processing complete")
    if(input("Open report file? (y/n) : ").capitalize()=='Y'):
            os.system(str(path2+'\\Summary.xlsx'))


