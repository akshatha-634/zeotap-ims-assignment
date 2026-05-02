import requests
import time

API = "http://127.0.0.1:8000/api"

signals = [
    {"component_id": "RDBMS_PRIMARY", "error_type": "connection_timeout", "severity": "P0", "message": "Database connection pool exhausted"},
    {"component_id": "RDBMS_PRIMARY", "error_type": "connection_timeout", "severity": "P0", "message": "Database connection pool exhausted"},
    {"component_id": "RDBMS_PRIMARY", "error_type": "connection_timeout", "severity": "P0", "message": "Database connection pool exhausted"},
    {"component_id": "CACHE_CLUSTER_01", "error_type": "memory_full", "severity": "P1", "message": "Cache memory utilization at 98%"},
    {"component_id": "CACHE_CLUSTER_01", "error_type": "memory_full", "severity": "P1", "message": "Cache memory utilization at 98%"},
    {"component_id": "API_GATEWAY", "error_type": "error_rate", "severity": "P2", "message": "5xx error rate above 10%"},
    {"component_id": "MCP_HOST_01", "error_type": "host_unreachable", "severity": "P0", "message": "MCP Host not responding to health checks"},
]

print("Sending sample signals...")
for i, signal in enumerate(signals):
    response = requests.post(f"{API}/ingest", json=signal)
    print(f"Signal {i+1}: {signal['component_id']} [{signal['severity']}] -> {response.json()['work_item']['status']}")
    time.sleep(0.5)

print("\nSample data loaded! Check http://localhost:3000")
