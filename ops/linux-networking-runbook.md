# Linux & Networking Operations Runbook

## Project Context

This runbook documents Linux and networking commands used to
operate and troubleshoot the Finance Tracker FastAPI service.

Application:
- Framework: FastAPI
- Server: Uvicorn
- Local address: 127.0.0.1
- Port: 8001
- Health endpoint: /health
- Log file: logs/api.log

## 1. Start the Application

From the project root:

```bash
source .venv/bin/activate
mkdir -p logs
python -m uvicorn main:app --host 127.0.0.1 --port 8001 > logs/api.log 2>&1
```

This runs Uvicorn in the foreground and redirects standard output
and standard error to logs/api.log.

Press Ctrl+C in the server terminal to stop it gracefully.

## 2. Process Troubleshooting

Find the Uvicorn process:

```bash
pgrep -af uvicorn
```

Inspect running processes:

```bash
ps aux | grep '[u]vicorn'
```

Use these commands to check whether the application process is running.

## 3. Port and Socket Troubleshooting

Check TCP listening sockets:

```bash
ss -ltnp
ss -ltnp | grep 8001
```

Confirm that the application is listening on the expected address
and port. Process details may depend on permissions.

## 4. HTTP Health Check

Send an HTTP request:

```bash
curl -i http://127.0.0.1:8001/health
```

Check only the HTTP status:

```bash
curl -sS -o /dev/null -w "HTTP status: %{http_code}\n" \
  http://127.0.0.1:8001/health
```

A 200 response indicates that the health endpoint responded successfully.

## 5. Application Logs

Display the latest log entries:

```bash
tail -n 20 logs/api.log
```

Follow new log entries:

```bash
tail -f logs/api.log
```

Search for errors:

```bash
grep -i "error" logs/api.log
```

No search results can simply mean no matching errors were recorded.

## 6. Network Interfaces and IP Addresses

Display network interfaces and addresses:

```bash
ip addr
```

The loopback interface is commonly named lo and uses 127.0.0.1
for IPv4 loopback communication.

In WSL, other interfaces and addresses depend on the network setup.

## 7. Routing Table

Inspect the routing table:

```bash
ip route
```

Look for the default route, gateway, network interface, and source address.

Do not assume that WSL network addresses or gateways are fixed.

## 8. DNS Resolution

Resolve a hostname:

```bash
getent hosts github.com
```

This checks hostname resolution through the system's configured
name-service mechanisms.

## 9. HTTPS Connectivity

Check connectivity to GitHub over HTTPS:

```bash
curl -I --connect-timeout 5 https://github.com/
```

A failed request may involve DNS, routing, TCP connectivity, TLS,
proxy configuration, or the remote service.

## 10. Service Outage Troubleshooting

If the health endpoint fails:

1. Check the process using pgrep -af uvicorn.
2. Check the listening port using ss -ltnp.
3. Inspect logs using tail -n 20 logs/api.log.
4. Verify the URL, bind address, and port.
5. Restart the service if necessary.
6. Retry the health endpoint using curl.
7. Record the symptom, evidence, cause, fix, and verification.

## Troubleshooting Principles

- A running process does not guarantee a healthy endpoint.
- A listening port does not guarantee the application works correctly.
- A connection-refused error often means no service is listening
  at the requested address and port.
- DNS resolution, routing, TCP connectivity, TLS, and HTTP are
  separate troubleshooting layers.
- 127.0.0.1 is loopback; it is not another machine's IP address.
- Do not commit passwords, access tokens, secrets, or generated logs.

## Learning Status

Documented commands are a learning reference, not proof that every
exercise has been completed. Record observed results and completed
labs as the exercises are performed.
