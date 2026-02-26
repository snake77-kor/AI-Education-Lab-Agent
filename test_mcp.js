const { spawn } = require('child_process');

const server = spawn('/usr/local/bin/npx', ['-y', 'notebooklm-mcp@latest'], {
    stdio: ['pipe', 'pipe', 'pipe']
});

server.stderr.on('data', (data) => {
    console.error(`STDERR: ${data}`);
});

server.stdout.on('data', (data) => {
    console.log(`STDOUT: ${data}`);
    process.exit(0); // If we get data, it works!
});

const initRequest = {
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
        protocolVersion: "2024-11-05",
        capabilities: {},
        clientInfo: {
            name: "test-client",
            version: "1.0.0"
        }
    }
};

server.stdin.write(JSON.stringify(initRequest) + '\n');
console.log("Sent initialize request...");

setTimeout(() => {
    console.log("Timeout waiting for response");
    server.kill();
}, 10000);
