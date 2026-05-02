import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
import time

# In-memory store for debouncing
debounce_store = {}
work_items = {}
signal_log = []
throughput_counter = 0
last_throughput_time = time.time()

DEBOUNCE_WINDOW = 10  # seconds

async def process_signal(signal_data: dict):
    global throughput_counter
    
    component_id = signal_data["component_id"]
    now = datetime.utcnow()
    
    # Add to raw signal log (Data Lake)
    signal_data["timestamp"] = now.isoformat()
    signal_log.append(signal_data)
    throughput_counter += 1
    
    # Debouncing logic - within 10 seconds same component = one work item
    if component_id in debounce_store:
        last_time = debounce_store[component_id]["last_seen"]
        if (now - last_time).seconds <= DEBOUNCE_WINDOW:
            # Update existing work item signal count
            work_items[component_id]["signal_count"] += 1
            debounce_store[component_id]["last_seen"] = now
            return work_items[component_id]
    
    # New work item
    work_item = {
        "id": f"WI-{component_id}-{int(now.timestamp())}",
        "component_id": component_id,
        "status": "OPEN",
        "signal_count": 1,
        "created_at": now.isoformat(),
        "severity": signal_data.get("severity", "P2"),
        "rca": None
    }
    
    work_items[component_id] = work_item
    debounce_store[component_id] = {"last_seen": now}
    
    return work_item

async def get_all_work_items():
    return list(work_items.values())

async def get_signal_log():
    return signal_log[-100:]  # Return last 100 signals

async def get_throughput():
    global throughput_counter, last_throughput_time
    now = time.time()
    elapsed = now - last_throughput_time
    rate = throughput_counter / elapsed if elapsed > 0 else 0
    return round(rate, 2)

async def update_work_item_status(component_id: str, new_status: str, rca: dict = None):
    valid_transitions = {
        "OPEN": ["INVESTIGATING"],
        "INVESTIGATING": ["RESOLVED"],
        "RESOLVED": ["CLOSED"]
    }
    
    if component_id not in work_items:
        return None
    
    current_status = work_items[component_id]["status"]
    
    if new_status not in valid_transitions.get(current_status, []):
        raise ValueError(f"Invalid transition from {current_status} to {new_status}")
    
    # Mandatory RCA check before closing
    if new_status == "CLOSED" and not rca:
        raise ValueError("RCA is mandatory before closing a work item")
    
    work_items[component_id]["status"] = new_status
    if rca:
        work_items[component_id]["rca"] = rca
    
    return work_items[component_id]
