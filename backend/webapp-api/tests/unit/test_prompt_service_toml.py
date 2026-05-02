from pathlib import Path

import pytest

from webapp_api_contract.brands import BrandArchetypeName
from webapp_api_contract.brand_settings import (
    ContentTypeName,
    ToneOfVoiceDimensionName,
)
from lib.prompts.model import PromptConfigError
from lib.prompts.service import PromptService


def test_prompt_service_loads_libraries_from_repo_prompts() -> None:
    service = PromptService()
    libraries = service.get_libraries()

    assert ToneOfVoiceDimensionName.FORMALITY in libraries.tone_library
    assert BrandArchetypeName.INNOCENT in libraries.archetype_library
    assert ContentTypeName.TESTIMONIAL in libraries.content_type_library

    testimonial = libraries.content_type_library[ContentTypeName.TESTIMONIAL]
    assert testimonial["description"].startswith("Highlight the specific 'before'")


def test_prompt_service_raises_for_invalid_tone_config(tmp_path: Path) -> None:
    prompts_dir = tmp_path
    brand_dir = prompts_dir / "brand"
    brand_dir.mkdir(parents=True)

    tone_file = brand_dir / "tone_of_voice.toml"
    tone_file.write_text(
        '[UNKNOWN_DIMENSION]\n1 = "Test description"\n',
        encoding="utf-8",
    )

    archetypes_file = brand_dir / "archetypes.toml"
    archetypes_file.write_text(
        "[INNOCENT]\n"
        'base_human_need = "x"\n'
        'description = "x"\n'
        'core_values = "x"\n'
        'target_audience = "x"\n'
        'writing_style = "x"\n'
        'examples = "x"\n',
        encoding="utf-8",
    )

    content_dir = prompts_dir / "content"
    content_dir.mkdir(parents=True)
    content_types_file = content_dir / "content_types.toml"
    content_types_file.write_text(
        '[TESTIMONIAL]\ndescription = "x"\n',
        encoding="utf-8",
    )

    with pytest.raises(PromptConfigError):
        PromptService(prompts_dir=prompts_dir)
