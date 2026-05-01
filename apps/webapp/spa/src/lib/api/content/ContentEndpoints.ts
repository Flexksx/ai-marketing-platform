import axios from 'axios';
import { Content, type ContentResponse } from './Content';
import type { ContentListRequest } from './ContentListRequest';

const BASE_URL = '/api/brands';

const getUrl = (brandId: string) => `${BASE_URL}/${brandId}/content`;

const list = async (brandId: string, params: ContentListRequest): Promise<Content[]> => {
	const response = await axios.get<ContentResponse[]>(getUrl(brandId), {
		params
	});
	return response.data.map(Content.fromResponse);
};

export const ContentEndpoints = {
	list
};
