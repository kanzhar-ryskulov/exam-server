import os
from app import BouquetController, CartController
from http_fw import Router, run


config = {
    "host": "0.0.0.0",
    "port": int(os.environ.get("PORT", 8001)),
    "static_dir": "static"
}

router = Router()
router.get("/", BouquetController, "home")
router.get("/bouquet/new", BouquetController, "new")
router.post("/bouquet", BouquetController, "create")
router.get("/cart", CartController, "cart")
router.get("/cart/add", CartController, "save_to_json")
router.get("/cart/remove", CartController, "remove_from_json")

run(router, config)