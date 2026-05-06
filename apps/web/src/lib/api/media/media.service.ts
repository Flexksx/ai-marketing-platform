import { env } from '$env/dynamic/private';
import { MediaStorage } from './media.storage';
import type {
	UploadImageParams,
	DownloadAndUploadParams,
	UploadMultipleImagesParams,
	UploadMultipleImagesResult
} from './media.types';

const STORAGE_BUCKET = env.STORAGE_BUCKET ?? 'posts';
const DEFAULT_TIMEOUT = 10000;
const DEFAULT_MAX_CONCURRENT = 5;

const inferExtensionFromContentType = (contentType: string): string => {
	if (contentType.includes('png')) return 'png';
	if (contentType.includes('jpeg') || contentType.includes('jpg')) return 'jpg';
	if (contentType.includes('webp')) return 'webp';
	if (contentType.includes('gif')) return 'gif';
	if (contentType.includes('svg')) return 'svg';
	return 'png';
};

const uploadImage = async (params: UploadImageParams): Promise<string> => {
	const { imageData, brandId, options } = params;

	const sanitizedBrandId = brandId.replace(/[^a-zA-Z0-9-_]/g, '_');
	const timestamp = Date.now();
	const contentType = options?.contentType ?? 'image/png';
	const extension = options?.fileExtension ?? inferExtensionFromContentType(contentType);
	const fileName = `${sanitizedBrandId}_${timestamp}.${extension}`;

	const blob = new Blob([imageData.buffer as ArrayBuffer], { type: contentType });

	const result = await MediaStorage.uploadToStorage({
		fileName,
		blob,
		contentType,
		bucket: STORAGE_BUCKET
	});

	return result.publicUrl;
};

const downloadImageWithTimeout = async (url: string, timeout: number): Promise<Uint8Array> => {
	const controller = new AbortController();
	const timeoutId = setTimeout(() => controller.abort(), timeout);

	try {
		const response = await fetch(url, {
			signal: controller.signal,
			headers: {
				'User-Agent': 'Mozilla/5.0 (compatible; BrandScraper/1.0)'
			}
		});

		if (!response.ok) {
			throw new Error(`HTTP ${response.status}: ${response.statusText}`);
		}

		const arrayBuffer = await response.arrayBuffer();
		return new Uint8Array(arrayBuffer);
	} finally {
		clearTimeout(timeoutId);
	}
};

const downloadAndUploadImage = async (params: DownloadAndUploadParams): Promise<string> => {
	const { imageUrl, brandId, timeout = DEFAULT_TIMEOUT } = params;

	const imageData = await downloadImageWithTimeout(imageUrl, timeout);

	let contentType = 'image/png';
	const urlLower = imageUrl.toLowerCase();
	if (urlLower.endsWith('.jpg') || urlLower.endsWith('.jpeg')) contentType = 'image/jpeg';
	else if (urlLower.endsWith('.png')) contentType = 'image/png';
	else if (urlLower.endsWith('.webp')) contentType = 'image/webp';
	else if (urlLower.endsWith('.gif')) contentType = 'image/gif';
	else if (urlLower.endsWith('.svg')) contentType = 'image/svg+xml';

	return await uploadImage({
		imageData,
		brandId,
		options: { contentType }
	});
};

const uploadMultipleImages = async (
	params: UploadMultipleImagesParams
): Promise<UploadMultipleImagesResult> => {
	const {
		imageUrls,
		brandId,
		maxConcurrent = DEFAULT_MAX_CONCURRENT,
		timeout = DEFAULT_TIMEOUT
	} = params;

	const successfulUploads: string[] = [];
	const failedUploads: Array<{ url: string; error: string }> = [];

	const processImage = async (url: string): Promise<void> => {
		try {
			const storageUrl = await downloadAndUploadImage({
				imageUrl: url,
				brandId,
				timeout
			});
			successfulUploads.push(storageUrl);
		} catch (error) {
			const errorMessage = error instanceof Error ? error.message : 'Unknown error';
			console.warn(`Failed to download/upload image ${url}:`, errorMessage);
			failedUploads.push({ url, error: errorMessage });
		}
	};

	for (let i = 0; i < imageUrls.length; i += maxConcurrent) {
		const batch = imageUrls.slice(i, i + maxConcurrent);
		await Promise.all(batch.map(processImage));
	}

	return {
		successfulUploads,
		failedUploads
	};
};

export const MediaService = {
	uploadImage,
	downloadAndUploadImage,
	uploadMultipleImages
};

