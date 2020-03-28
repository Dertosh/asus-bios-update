from urllib.request import urlopen, Request
import os
import json
import re
import datetime


def get_latest_bios_info(model_name: str):
    """ 
    Get information about latest bios from asus.com for model.
    model_name -- model of matherboard
    """
    cpu = ""
    url = "https://www.asus.com/support/api/product.asmx/GetPDBIOS?website=global&model=" + \
        model_name + "&cpu="+cpu+"&callback=supportpdpage"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    rs = urlopen(req)
    text = rs.readline().decode('ascii')
    json_text = re.findall(r"\((.*?)\)", text)[0]
    result = json.loads(json_text)

    latest_bios = result["Result"]["Obj"][0]["Files"][0]
    return latest_bios


def bios_update(model: str, latest_bios_info, efi_path: str):
    """
    Downloading bios from asus.com and unzip to efi path.
    model -- model of matherboard
    latest_bios_info -- information about latest bios
    efi_path -- path to efi folder
    """
    print("Update!\n")
    print("Current BIOS")
    print("Release date: " + currentBIOSreleaseDate.strftime('%x'))
    print("Version: " + str(currentBIOSversion))
    print("\nNew BIOS")
    print("Release date: " + newBIOSreleaseDate.strftime('%x'))
    print("Version: " + str(newBIOSversion))
    os.system('cd ' + efi_path)
    os.system('wget ' + latest_bios_info["DownloadUrl"]["Global"])
    os.system("unzip "+model+'*' +
              latest_bios_info["Version"]+".zip -d " + EFI_path)
    os.system("rm " + model+'*'+latest_bios_info["Version"]+".zip")


EFI_path = "/boot/EFI/"

currentBIOSreleaseDate = datetime.datetime.strptime(
    os.popen('dmidecode -s bios-release-date').read()[:-1], '%m/%d/%Y')
currentModel, currentBIOSversion = (
    os.popen('dmidecode -s bios-version').read()[:-1]).split('.')
currentBIOSversion = int(currentBIOSversion)

latest_bios_info = get_latest_bios_info(currentModel)

newBIOSreleaseDate = datetime.datetime.strptime(
    latest_bios_info["ReleaseDate"], '%Y/%m/%d')
newBIOSversion = int(latest_bios_info["Version"])

if newBIOSreleaseDate > currentBIOSreleaseDate and newBIOSversion > currentBIOSversion:
    bios_update(currentModel, latest_bios_info, EFI_path)
else:
    print("BIOS doesn't need updating.\n")
    print("Current BIOS")
    print("Release date: " + currentBIOSreleaseDate.strftime('%x'))
    print("Version: " + str(currentBIOSversion))
    print("\nNew BIOS")
    print("Release date: " + newBIOSreleaseDate.strftime('%x'))
    print("Version: " + str(newBIOSversion))
