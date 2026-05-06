import { ContentFormat } from '$lib/api/content/ContentFormat';
import type { ContentPillarType, ContentType } from './schema/ContentPillar';

function enumValueToLabel(value?: string | null): string {
	if (!value) return '';

	return value
		.split('_')
		.map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
		.join(' ');
}

export function contentFormatToLabel(format?: ContentFormat | null): string {
	return enumValueToLabel(format ?? undefined);
}

export function contentPillarTypeToLabel(type?: ContentPillarType | null): string {
	return enumValueToLabel(type ?? undefined);
}

export function contentTypeToLabel(type?: ContentType | null): string {
	return enumValueToLabel(type ?? undefined);
}
