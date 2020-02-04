from urllib.request import urlopen
import os 
import json
import re
import datetime

def get_html(url):
    rs = urlopen(url)
    text = rs.readline().decode('ascii')
    json_text = re.findall(r"\((.*?)\)", text)[0]
    result = json.loads(json_text)
  
    latest_bios = result["Result"]["Obj"][0]["Files"][0]
    print(latest_bios)
    
    newBIOSreleaseDate = datetime.datetime.strptime(latest_bios["ReleaseDate"], '%Y/%m/%d')
    newBIOSversion = int(latest_bios["Version"])

    currentBIOSreleaseDate = datetime.datetime.strptime(os.popen('dmidecode -s bios-release-date').read()[:-1],'%m/%d/%Y')
    currentModel,currentBIOSversion = (os.popen('dmidecode -s bios-version').read()[:-1]).split('.')
    currentBIOSversion = int(currentBIOSversion)

    if newBIOSreleaseDate <= currentBIOSreleaseDate or newBIOSversion <= currentBIOSversion:
        return
    print("Update!\n")
    print("Current BIOS")
    print("Release date: " + currentBIOSreleaseDate.strftime('%x'))
    print("Version: " + str(currentBIOSversion))
    print("\nNew BIOS")
    print("Release date: " + newBIOSreleaseDate.strftime('%x'))
    print("Version: " + str(newBIOSversion))

    os.system('cd /boot/EFI/')
    os.system('wget ' + latest_bios["DownloadUrl"]["Global"])
    os.system("unzip "+currentModel+'*'+str(newBIOSversion)+".zip -d " + EFI_path)
    os.system("rm " +currentModel+'*'+str(newBIOSversion)+".zip")


model_name = "UX333FA"
cpu = ""
EFI_path = "/boot/EFI/"

url = "https://www.asus.com/support/api/product.asmx/GetPDBIOS?website=global&pdhashedid=YXAdDPC8x8xmgSYE&model=" + model_name + "&cpu="+cpu+"&callback=supportpdpage"
print(url)
get_html(url)
