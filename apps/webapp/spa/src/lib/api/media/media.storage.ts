import { StorageClient } from '@supabase/storage-js';
import { env } from '$env/dynamic/private';
import { env as publicEnv } from '$env/dynamic/public';
import type { StorageUploadParams, StorageUploadResult } from './media.types';

const SUPABASE_URL = publicEnv.PUBLIC_SUPABASE_URL;
const SUPABASE_SERVICE_ROLE_KEY = env.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL) {
	throw new Error('PUBLIC_SUPABASE_URL is not set');
}

if (!SUPABASE_SERVICE_ROLE_KEY) {
	throw new Error('SUPABASE_SERVICE_ROLE_KEY is not set');
}

const STORAGE_URL = `${SUPABASE_URL}/storage/v1`;

const storageClient = new StorageClient(STORAGE_URL, {
	apikey: SUPABASE_SERVICE_ROLE_KEY,
	authorization: `Bearer ${SUPABASE_SERVICE_ROLE_KEY}`
});

const uploadToStorage = async (params: StorageUploadParams): Promise<StorageUploadResult> => {
	const { fileName, blob, contentType, bucket } = params;

	const { data, error } = await storageClient.from(bucket).upload(fileName, blob, {
		contentType,
		upsert: false
	});

	if (error) {
		throw new Error(`Failed to upload to storage: ${error.message} (bucket: ${bucket}, file: ${fileName})`);
	}

	if (!data) {
		throw new Error('Storage upload returned empty response');
	}

	const { data: publicUrlData } = storageClient.from(bucket).getPublicUrl(data.path);

	return {
		path: data.path,
		publicUrl: publicUrlData.publicUrl
	};
};

const getPublicUrl = (bucket: string, path: string): string => {
	const { data } = storageClient.from(bucket).getPublicUrl(path);
	return data.publicUrl;
};

export const MediaStorage = {
	uploadToStorage,
	getPublicUrl
};

