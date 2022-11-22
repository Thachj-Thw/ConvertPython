import asyncio


async def func(idx: int):
    for _ in range(5):
        await asyncio.sleep(3)
        print(idx, "refresh")

async def main():
    await asyncio.gather(
        func(1),
        func(2),
        func(3),
        func(4)
    )

if __name__ == "__main__":
    asyncio.run(main())
    input()
