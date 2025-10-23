import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        "postgresql://postgres:123456@localhost:5433/realtime_collab"
    )
    print("✅ Connected successfully!")
    await conn.close()

asyncio.run(test())
