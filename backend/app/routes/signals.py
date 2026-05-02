from fastapi import APIRouter, HTTPException
from app.services.signal_service import (
    process_signal,
    get_all_work_items,
    get_signal_log,
    get_throughput,
    update_work_item_status
)

router = APIRouter()

@router.post("/ingest")
async def ingest_signal(signal: dict):
    try:
        work_item = await process_signal(signal)
        return {"success": True, "work_item": work_item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/work-items")
async def get_work_items():
    items = await get_all_work_items()
    return {"work_items": items}

@router.get("/signals/raw")
async def get_raw_signals():
    logs = await get_signal_log()
    return {"signals": logs}

@router.patch("/work-items/{component_id}/status")
async def update_status(component_id: str, payload: dict):
    try:
        updated = await update_work_item_status(
            component_id,
            payload.get("status"),
            payload.get("rca")
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Work item not found")
        return {"success": True, "work_item": updated}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/throughput")
async def throughput():
    rate = await get_throughput()
    return {"signals_per_second": rate}
