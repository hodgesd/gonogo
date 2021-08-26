import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Back, Style
import pyautogui
import PIL


#Logic for conditional highlighting

class Field:
    """docstring for Field."""

    def __init__(self,icao,opr,arff,valid,notes):
        self.icao=icao
        self.opr=opr
        self.arff=arff
        self.valid=valid
        self.notes=notes

    def i(self):
        print ("ICAO:", icao)

    def o(self):
        print ("HOURS:", end=" ")
        if atct == "":
            print(Back.YELLOW+"NO ATCT"+Style.RESET_ALL, self.valid)
        else:
            if atct == "Airport traffic control tower":
                print ("ATCT", self.valid)
            else:
                print (atct,self.valid)

    def a_e(self):
        if elev != "":
            print ("ELEV: "+str(FE)+"'")
        if arff != "":
            print ("ARFF: "+self.arff)



class Strip:
    def __init__(self,length,width,pcn,wbc,grvd):
        self.length=length
        self.width=width
        self.pcn=pcn
        self.wbc=wbc
        self.grvd=grvd

    def w(self):
        if self.width < 75:
            print(Back.RED + str(self.width)+"'"+Style.RESET_ALL, end=" ")
            pass
        elif self.width <= 100:
            print(Back.YELLOW + str(self.width)+"'"+Style.RESET_ALL, end=" ")
        elif self.width > 100:
            print(str(self.width)+"'"+Style.RESET_ALL, end=" ")
    def l(self):
        if self.length < 5000:
            print(Back.RED + str(self.length)+"'"+Style.RESET_ALL, end="x")
            pass
        elif self.length <= 6000:
            print(Back.YELLOW + str(self.length)+"'"+Style.RESET_ALL, end="x")
        elif self.length >6000:
            print(str(self.length)+"'", end="x")

    def d(self):
        self.wbc = " ".join(self.wbc.split())
        result2 = re.search(r"(\d+),", self.wbc)
        # print("wbc"+self.wbc+"contents")
        if self.wbc is None:
            self.wbc = ""

        if self.wbc == "":
            print("")
            pass
        elif self.wbc is None:
            print("")
            pass
        else:
            self.wbc = int(result2.group(1))
            # print(self.wbc)
            if self.wbc < 80:
                print(Back.RED+"D" + str(self.wbc)+Style.RESET_ALL)
                pass
            elif self.wbc < 96:
                print(Back.YELLOW+"D" + str(self.wbc)+Style.RESET_ALL)
            elif self.wbc >= 96:
                print("D" + str(self.wbc)+Style.RESET_ALL)

    def g(self):
        if self.grvd == "":
            print(Back.YELLOW+"NOT GRVD"+Style.RESET_ALL, end=" ")

        elif self.grvd == "GRVD":
            print(self.grvd, end=" ")
        else:
            print(Back.YELLOW+self.grvd+Style.RESET_ALL, end=" ")
    def p(self):
        #print ("PCN = ",self.pcn, end=" ")
        if self.pcn == "":
            # print("PCN is None")
            print("", end="")
            pass
        else:
            result = re.search(r"(.+)/(.+)/(.+)/(.+)/(.+)", self.pcn)
            acn = int(result.group(1))
            u = result.group(2)
            x = result.group(3)
            y = result.group(4)
            z = result.group(5)
            if acn < 24:
                print(Back.RED+str(acn)+Style.RESET_ALL, end="/")
            elif acn >= 24:
                print(acn, end="/")
            print(u, end="/")
            print(x, end="/")
            if y=="Y":
                print(Back.YELLOW+y+Style.RESET_ALL, end="/")
            elif y=="Z":
                print(Back.RED+y+Style.RESET_ALL, end="/")
            print(z, end=" ")

# Prompt for airport input and build FAA url
airport = input("Airfield: ")
base = "https://nfdc.faa.gov/nfdcApps/services/ajv5/airportDisplay.jsp?airportId="
url=base+airport

# Get and parse current FAA data with soup
r = requests.get(url)
soup = BeautifulSoup(r.text,"html.parser")

icao = soup.find("span", {"style":"font-size: 24px; font-weight: 900;"}).text
name = soup.find('title').text
icao = icao+": "+name

atct = soup.find("td", text="Control Tower").find_next_sibling("td").text
atct = " ".join(atct.split())
opr = soup.find("td", text="Tower Hours").find_next_sibling("td").text
opr = " ".join(opr.split())
elev = soup.find("td", text="Elevation").find_next_sibling("td").text
elev = " ".join(elev.split())
result3 = re.search(r"(\d+)\.", elev)
FE = int(result3.group(1))


arff = soup.find("td", text="Fire and Rescue").find_next_sibling("td").text
arff = " ".join(arff.split())
r4 = re.search(r"(ARFF Index \w)", arff)
arff=r4.group(1)
notes = "Test"
# print ("OPR:", atct, opr)

a = Field(icao,atct,arff,opr,notes)

a.i()
a.a_e()
a.o()


# runways = soup.find_all("div", {"class":"tab-pane active"})
runways = soup.find_all('div', {'id': re.compile(r'runway')})
print("RUNWAYS:")

for runway in runways:
    rwy = runway.find("span").text
    rw = re.sub(r"RUNWAY", "", rwy)
    print("-"+rw, end=": ")

    dimension = runway.find_all("td")[1].text
    #remove whitespace
    dim = " ".join(dimension.split())
    result = re.search(r"(\d+) ft\. x (\d+) ", dim)
    length = int(result.group(1))
    width = int(result.group(2))
    pcn = runway.find("td", text="PCN").find_next_sibling("td").text
    pcn = " ".join(pcn.split())
    treatment = runway.find("td", text="Treatment").find_next_sibling("td").text
    grvd = " ".join(treatment.split())
    # print(grvd)

    doublewheel = runway.find("td", text="Double Wheel").find_next_sibling("td").text
    r = Strip(length, width, pcn, doublewheel, grvd)
    r.l()
    r.w()
    r.g()
    r.p()
    r.d()

print("")
myScreenshot = pyautogui.screenshot()
myScreenshot.save(r'/Users/derrickhodges/Documents/Scripts/screenshot_1.png')
