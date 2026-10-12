import os
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Xinggou Mock Order API")

ORDERS = {
    "ORD1001": {
        "order_id": "ORD1001",
        "owner_user_id": "USER_A",
        "product_name": "AirSound Pro 蓝牙耳机",
        "status": "SHIPPED",
        "logistics_status": "运输中",
        "estimated_delivery": "2026-10-15"
    },
    "ORD1002": {
        "order_id": "ORD1002",
        "owner_user_id": "USER_A",
        "product_name": "智能手环",
        "status": "PENDING_SHIPMENT",
        "logistics_status": None,
        "estimated_delivery": None
    },
    "ORD2001": {
        "order_id": "ORD2001",
        "owner_user_id": "USER_B",
        "product_name": "蓝牙音箱",
        "status": "COMPLETED",
        "logistics_status": "已签收",
        "estimated_delivery": None
    }
}

TOKENS = {
    "USER_A": os.getenv("USER_A_TEST_TOKEN", ""),
    "USER_B": os.getenv("USER_B_TEST_TOKEN", "")
}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/orders/{order_id}")
def get_order(order_id: str, authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")

    token = authorization.removeprefix("Bearer ").strip()
    user_id = next(
        (uid for uid, expected in TOKENS.items() if expected and token == expected),
        None
    )
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    order = ORDERS.get(order_id)
    if not order or order["owner_user_id"] != user_id:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "ORDER_NOT_FOUND",
                "message": "无法查询该订单"
            }
        }

    return {
        "success": True,
        "data": {
            k: v for k, v in order.items()
            if k != "owner_user_id"
        },
        "error": None
    }
