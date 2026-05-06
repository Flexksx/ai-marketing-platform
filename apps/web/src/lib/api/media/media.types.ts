export type UploadImageParams = {
	imageData: Uint8Array;
	brandId: string;
	options?: {
		contentType?: string;
		fileExtension?: string;
	};
};

export type UploadImageResult = {
	success: boolean;
	url?: string;
	error?: string;
};

export type DownloadAndUploadParams = {
	imageUrl: string;
	brandId: string;
	timeout?: number;
};

export type UploadMultipleImagesParams = {
	imageUrls: string[];
	brandId: string;
	maxConcurrent?: number;
	timeout?: number;
};

export type UploadMultipleImagesResult = {
	successfulUploads: string[];
	failedUploads: Array<{ url: string; error: string }>;
};

export type StorageUploadParams = {
	fileName: string;
	blob: Blob;
	contentType: string;
	bucket: string;
};

export type StorageUploadResult = {
	path: string;
	publicUrl: string;
};

