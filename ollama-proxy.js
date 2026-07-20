const http = require('http');

let requestCount = 0;

const server = http.createServer((req, res) => {
    requestCount++;
    console.log(=== Request # ===);
    console.log(Method: );
    console.log(URL: );
    console.log(Headers:, req.headers);
    
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
        console.log(Body: );
        console.log('========================');
        
        // Forward to Ollama
        const options = {
            hostname: 'localhost',
            port: 11434,
            path: req.url,
            method: req.method,
            headers: req.headers
        };
        
        const proxyReq = http.request(options, (proxyRes) => {
            res.writeHead(proxyRes.statusCode, proxyRes.headers);
            proxyRes.pipe(res);
        });
        
        proxyReq.on('error', (e) => {
            console.log('Proxy error:', e);
            res.writeHead(500);
            res.end(JSON.stringify({error: 'Proxy error', details: e.message}));
        });
        
        if (body) {
            proxyReq.write(body);
        }
        proxyReq.end();
    });
});

server.listen(11435, 'localhost', () => {
    console.log('Debug proxy running on localhost:11435');
    console.log('Configure OpenCode to use: http://localhost:11435');
    console.log('This will log all requests and forward to Ollama on port 11434');
});
