const axios = require('axios');
const fs = require('fs');

const QuantixProxies = [];
const QuantixOutputFile = 'proxy.txt';

if (fs.existsSync(QuantixOutputFile)) {
  fs.unlinkSync(QuantixOutputFile);
  console.log('\x1b[33m%s\x1b[0m', `'${QuantixOutputFile}' telah dihapus.`); // Warna kuning
}

const QuantixProxySites = [
  'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
  'http://hack-hack.chat.ru/proxy/p4.txt',
  'https://github.com/themiralay/Proxy-List-World/raw/master/data.txt',
  'https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/all.txt',
  'https://github.com/im-razvan/proxy_list/raw/main/http.txt',
  'https://github.com/im-razvan/proxy_list/raw/main/socks5',
  'https://github.com/TuanMinPay/live-proxy/raw/master/all.txt',
  'https://github.com/andigwandi/free-proxy/raw/main/proxy_list.txt',
  'https://github.com/ALIILAPRO/Proxy/raw/main/http.txt',
  'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
  'https://github.com/MrMarble/proxy-list/raw/main/all.txt',
  'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
  'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
  'https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt',
  'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
  'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
  'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt',
  'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
  'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt',
  'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt',
  'https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt',
  'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt',
  'https://spys.me/socks.txt',
  'https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt',
  'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
  'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt',
  'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
  'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
  'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
  'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
  'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
  'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt',
  'https://raw.githubusercontent.com/mallisc5/master/proxy-list-raw.txt',
  'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
  'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
  'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
  'https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt',
  'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/https.txt',
  'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt',
  'https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt',
  'https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt',
  'https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt',
  'https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt',
  'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt',
  'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt',
  'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt',
  'https://raw.githubusercontent.com/tuanminpay/live-proxy/master/http.txt',
  'https://raw.githubusercontent.com/casals-ar/proxy-list/main/https',
  'https://raw.githubusercontent.com/casals-ar/proxy-list/main/http',
  'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
  'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt',
  'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
  'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
  'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt',
  'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt',
  'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
  'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
  'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt',
  'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
  'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
  'http://atomintersoft.com/proxy_list_port_80',
  'http://atomintersoft.com/proxy_list_domain_org',
  'http://atomintersoft.com/proxy_list_port_3128',
  'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt',
  'https://raw.githubusercontent.com/mallisc5/master/proxy-list-raw.txt',
  'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
  'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
  'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
  'https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt',
  'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/https.txt',
  'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt',
  'https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt',
  'https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt',
  'https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt',
  'https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt',
  'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt',
  'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt',
  'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt',
  'https://raw.githubusercontent.com/tuanminpay/live-proxy/master/http.txt',
  'https://raw.githubusercontent.com/casals-ar/proxy-list/main/https',
  'https://raw.githubusercontent.com/casals-ar/proxy-list/main/http',
  'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
  'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt',
  'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
  'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
  'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt',
  'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt',
  'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
  'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
  'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt',
  'http://freeproxylist-daily.blogspot.com/2013/05/usa-proxy-list-2013-05-15-0111-am-gmt8.html',
  'http://freeproxylist-daily.blogspot.com/2013/05/usa-proxy-list-2013-05-13-812-gmt7.html',
  'http://www.cybersyndrome.net/pla5.html',
  'http://vipprox.blogspot.com/2013_06_01_archive.html',
  'http://vipprox.blogspot.com/2013/05/us-proxy-servers-74_24.html',
  'http://vipprox.blogspot.com/p/blog-page_7.html',
  'http://vipprox.blogspot.com/2013/05/us-proxy-servers-199_20.html',
  'http://vipprox.blogspot.com/2013_02_01_archive.html',
  'http://alexa.lr2b.com/proxylist.txt',
  'http://proxylist.psihialt.com/index.html',
  'http://proxylistbylocation.web.fc2.com/proxylistbycountry.html',
  'http://web.harvard.edu/~hcohen/proxylist.html',
  'http://proxyworldnetwork.blogspot.com/p/proxylist.html',
  'http://www.proxywebdata.com/HTTP.txt',
  'http://proxylist.webs.com/proxylist.txt',
  'http://updatedproxylist.blogspot.com/2012/07/free-proxy-list.html',
  'http://www.proxyarchive.com/proxylist.txt',
  'http://www.rebeldotnet.com/ProxyList/ProxyList.html',
  'http://www.freedownloadweb.com/proxies/http.txt',
  'http://updatedproxylist.blogspot.com/2012/07/free-proxy-list.html'
];

async function QuantixFetchProxiesFromSite(site) {
  try {
    const response = await axios.get(site);
    const lines = response.data.split('\n');
    lines.forEach(line => {
      if (line.includes(':')) {
        const [ip, port] = line.split(':', 2);
        QuantixProxies.push(`${ip}:${port}`);
      }
    });
  } catch (error) {
    console.log('\x1b[31m%s\x1b[0m', `Gagal mengambil proxy dari ${site}: ${error.message}`); // Warna merah
  }
}

function drawProgressBar(progress) {
  const barLength = 50;
  const filledLength = Math.round(barLength * progress);
  const filledBar = '█'.repeat(filledLength);
  const emptyBar = '░'.repeat(barLength - filledLength);
  return `[${filledBar}${emptyBar}] ${(progress * 100).toFixed(2)}%`;
}

async function QuantixFetchAllProxies() {
  console.log('\x1b[36m%s\x1b[0m', 'Memulai proses pengambilan proxy...'); // Warna cyan

  const QuantixStartTime = Date.now();

  for (let i = 0; i < QuantixProxySites.length; i++) {
    await QuantixFetchProxiesFromSite(QuantixProxySites[i]);
    const progress = (i + 1) / QuantixProxySites.length;
    process.stdout.write(`\r${drawProgressBar(progress)}`);
  }

  console.log('\n\x1b[32m%s\x1b[0m', 'Proses pengambilan proxy selesai.'); // Warna hijau

  fs.writeFileSync(QuantixOutputFile, QuantixProxies.join('\n'));
  console.log('\x1b[32m%s\x1b[0m', `Proxies berhasil diambil dan disimpan dalam ${QuantixOutputFile}`); // Warna hijau
  console.log('\x1b[34m%s\x1b[0m', `Total proxy valid: ${QuantixProxies.length}`); // Warna biru

  const QuantixEndTime = Date.now();
  const QuantixExecutionTime = (QuantixEndTime - QuantixStartTime) / 1000;
  console.log('\x1b[33m%s\x1b[0m', `Waktu eksekusi: ${QuantixExecutionTime.toFixed(2)} detik`); // Warna kuning

  console.log('\x1b[35m%s\x1b[0m', 'Kredit oleh: t.me/Quantix Service'); // Warna magenta
}

QuantixFetchAllProxies();