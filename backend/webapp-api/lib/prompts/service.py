import os
import tomllib
from pathlib import Path
from typing import Any, cast

import public
from jinja2 import Environment, FileSystemLoader, select_autoescape

from lib.prompts.model import (
    PromptConfigError,
    PromptLibraries,
    PromptTemplateName,
)
from src.brand.archetype.model import (
    BrandArchetype,
    BrandArchetypeData,
    BrandArchetypeName,
)
from src.brand.model import ContentType, ContentTypeName


@public.add
class PromptService:
    def __init__(self, prompts_dir: Path | None = None):
        self._prompts_dir = prompts_dir or self._get_default_prompts_dir()
        self._libraries = self._load_libraries()
        self._environment = self._create_environment()

    def render(self, template_name: PromptTemplateName | str, context: dict) -> str:
        template_path = (
            template_name.value
            if isinstance(template_name, PromptTemplateName)
            else template_name
        )
        template = self._environment.get_template(template_path)
        return template.render(**context)

    def get_libraries(self) -> PromptLibraries:
        return self._libraries

    def _get_default_prompts_dir(self) -> Path:
        path = os.environ.get("PROMPTS_DIR")
        if path:
            return Path(path)

        current_file = Path(__file__).resolve()
        repo_root = current_file.parent.parent.parent.parent.parent.parent
        prompts_path = repo_root / "prompts"

        if not prompts_path.exists():
            prompts_path = Path("/app/prompts")

        return prompts_path

    def _load_libraries(self) -> PromptLibraries:
        return PromptLibraries(
            archetype_library=self._load_archetype_library(),
            content_type_library=self._load_content_type_library(),
        )

    def _create_environment(self) -> Environment:
        env = Environment(
            loader=FileSystemLoader(str(self._prompts_dir)),
            autoescape=select_autoescape(default=False),
        )
        tmpl_globals = cast(dict[str, Any], env.globals)
        tmpl_globals["archetype_library"] = (
            self._transform_archetype_library_for_template()
        )
        tmpl_globals["content_type_library"] = (
            self._transform_content_type_library_for_template()
        )

        return env

    def _load_archetype_library(self) -> dict[BrandArchetypeName, BrandArchetype]:
        path = self._prompts_dir / "brand" / "archetypes.toml"
        if not path.exists():
            raise PromptConfigError(f"Missing archetypes config at {path}")

        with path.open("rb") as f:
            data = tomllib.load(f)

        if not isinstance(data, dict):
            raise PromptConfigError(f"Invalid archetypes config structure in {path}")

        result: dict[BrandArchetypeName, BrandArchetype] = {}

        for section_name, values in data.items():
            if not isinstance(values, dict):
                raise PromptConfigError(
                    f"Invalid data for archetype {section_name} in {path}"
                )

            try:
                archetype_name = BrandArchetypeName[section_name]
            except KeyError as e:
                raise PromptConfigError(
                    f"Unknown archetype {section_name} in {path}"
                ) from e

            required_keys = [
                "base_human_need",
                "description",
                "core_values",
                "target_audience",
                "writing_style",
                "examples",
            ]

            for key in required_keys:
                if key not in values or not isinstance(values[key], str):
                    raise PromptConfigError(
                        f"Missing or invalid {key} for archetype {section_name} in {path}"
                    )

            data_model = BrandArchetypeData(
                base_human_need=values["base_human_need"],
                archetype_description=values["description"],
                identification_clues="",
                core_shared_values=values["core_values"],
                typical_target_audience=values["target_audience"],
                colors_graphics_description="",
                writing_style_description=values["writing_style"],
                examples=values["examples"],
            )

            result[archetype_name] = BrandArchetype(
                name=archetype_name,
                data=data_model,
            )

        return result

    def _load_content_type_library(self) -> dict[ContentTypeName, ContentType]:
        path = self._prompts_dir / "content" / "content_types.toml"
        if not path.exists():
            raise PromptConfigError(f"Missing content types config at {path}")

        with path.open("rb") as f:
            data = tomllib.load(f)

        if not isinstance(data, dict):
            raise PromptConfigError(f"Invalid content types config structure in {path}")

        result: dict[ContentTypeName, ContentType] = {}

        for section_name, values in data.items():
            if not isinstance(values, dict):
                raise PromptConfigError(
                    f"Invalid data for content type {section_name} in {path}"
                )

            try:
                content_type_name = ContentTypeName[section_name]
            except KeyError as e:
                raise PromptConfigError(
                    f"Unknown content type {section_name} in {path}"
                ) from e

            description = values.get("description")
            if not isinstance(description, str):
                raise PromptConfigError(
                    f"Missing or invalid description for content type {section_name} in {path}"
                )

            result[content_type_name] = ContentType(
                name=content_type_name,
                description=description,
            )

        return result

    def _transform_archetype_library_for_template(self) -> dict[str, dict[str, str]]:
        return {
            archetype_name.value: {
                "description": archetype.data.archetype_description,
                "base_human_need": archetype.data.base_human_need,
                "core_values": archetype.data.core_shared_values,
                "writing_style": archetype.data.writing_style_description,
            }
            for archetype_name, archetype in self._libraries.archetype_library.items()
        }

    def _transform_content_type_library_for_template(self) -> dict[str, str]:
        return {
            content_type.value: data.description
            for content_type, data in self._libraries.content_type_library.items()
        }
