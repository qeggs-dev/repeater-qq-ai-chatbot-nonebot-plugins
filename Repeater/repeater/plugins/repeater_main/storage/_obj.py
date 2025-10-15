from ._base_path import storage_path
from ._sync_base_storage import (
    TextStorage,
    BinaryStorage
)
from ._async_base_storage import (
    TextStorage as AsyncTextStorage,
    BinaryStorage as AsyncBinaryStorage
)
from ._orjson_storage import OrjsonStorage
from ._async_orjson_storage import OrjsonStorage as AsyncOrjsonStorage
from ._yaml_storage import YamlStorage
from ._async_yaml_storage import YamlStorage as AsyncYamlStorage

text_storage = TextStorage(storage_path.storage_base_path)
binary_storage = BinaryStorage(storage_path.storage_base_path)
async_text_storage = AsyncTextStorage(storage_path.storage_base_path)
async_binary_storage = AsyncBinaryStorage(storage_path.storage_base_path)
json_storage = OrjsonStorage(storage_path.storage_base_path)
yaml_storage = YamlStorage(storage_path.storage_base_path)
async_json_storage = AsyncOrjsonStorage(storage_path.storage_base_path)
async_yaml_storage = AsyncYamlStorage(storage_path.storage_base_path)