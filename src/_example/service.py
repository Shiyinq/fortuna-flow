from src._example import repository


async def get_examples():
    return await repository.find_examples({})

async def create_example(data: dict):
    return await repository.insert_example(data)

async def update_example(example_id: str, data: dict):
    return await repository.update_example({"_id": example_id}, data)

async def delete_example(example_id: str):
    return await repository.delete_example({"_id": example_id})
