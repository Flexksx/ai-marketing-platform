export interface ScrapeResultResponse {
	text: string;
	image_urls: string[];
	video_urls: string[];
	logo: string | null;
	screenshot: string | null;
	page_urls: string[];
}
