from pydantic import BaseModel


class ModuleInfo(BaseModel):
    name: str
    purpose: str


class ArchitectureAnalysis(BaseModel):
    architecture_summary: str

    main_modules: list[ModuleInfo]

    reading_order: list[str]

    entry_points: list[str]