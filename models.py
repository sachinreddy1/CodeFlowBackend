from dataclasses import dataclass
from typing import List, Optional
from dataclasses_json import dataclass_json

@dataclass
class RepositoryInfo:
    owner: str
    repository: str
    branch: str

@dataclass_json
@dataclass
class GitHubTreeFile:
    path: str
    url: str

@dataclass_json
@dataclass
class GitHubTreeResponse:
    tree: List[GitHubTreeFile]

@dataclass_json
@dataclass
class GitHubBlobResponse:
    content: Optional[str] = None
