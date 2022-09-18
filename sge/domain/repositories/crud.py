async def get_list_data(collection, helper, **kwargs) -> dict:
    """Retorna uma lista de dados do banco de dados."""
    data = []
    async for obj in collection.find(kwargs):
        data.append(helper(obj))
    return data


async def add_data(collection, helper, payload: dict) -> dict:
    """Adiciona um novo registro no banco de dados."""
    data = await collection.insert_one(payload)
    return helper(await collection.find_one({'_id': data.inserted_id}))


async def get_data(collection, helper, id: str) -> dict:
    """Retorna um registro do banco de dados."""
    data = await collection.find_one({'_id': id})
    if data:
        return helper(data)


async def update_data(collection, id: str, payload: dict) -> bool:
    """Atualiza um registro no banco de dados."""
    if len(payload) < 1:
        return False
    data = await collection.find_one({'_id': id})
    if data:
        updated = await collection.update_one(
            {'_id': id}, {'$set': payload}
        )
        if updated:
            return True
        return False


async def delete_data(collection, id: str) -> bool:
    """Remove um registro do banco de dados."""
    data = await collection.find_one({'_id': id})
    if data:
        await collection.delete_one({'_id': id})
        return True
