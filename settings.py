from dataclasses import dataclass, field
from typing import Dict

from loader_from_file.ifileloader import IFileLoader
from loader_from_file.json_file_loader import JSONFileLoader
from serializers.iserializer import ISerializer
from serializers.json_serializer import JSONSerializer
from serializers.xml_serializer import XMLSerializer


@dataclass
class Settings():
    available_serializers: Dict[str, ISerializer] = field(default_factory=dict)
    available_loaders_from_file: Dict[str,
                                      IFileLoader] = field(default_factory=dict)
    current_loader_format: str = ""


settings = Settings()
settings.available_serializers['json'] = JSONSerializer
settings.available_serializers['xml'] = XMLSerializer
settings.available_loaders_from_file['json'] = JSONFileLoader
settings.current_loader_format = 'json'
