from ._base_path import storage_path
from ._base_storage import TextStorage, BinaryStorage
from ._orjson_storage import OrjsonStorage
from ._yaml_storage import YamlStorage

text_storage = TextStorage(storage_path.storage_base_path)
binary_storage = BinaryStorage(storage_path.storage_base_path)
json_storage = OrjsonStorage(storage_path.storage_base_path)
yaml_storage = YamlStorage(storage_path.storage_base_path)