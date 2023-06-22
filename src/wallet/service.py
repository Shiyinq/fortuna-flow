from src.db import database
from src.wallet.constants import Info
from src.wallet.schemas import WalletCreate

async def create_wallet(wallet: WalletCreate):
    wallet_data = wallet.dict()
    await database["wallets"].insert_one(wallet_data)
    return {"detail": Info.WALLET_CREATED}
