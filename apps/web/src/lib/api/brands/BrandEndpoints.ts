import axios from 'axios';
import { Brand } from './model/Brand';
import type { BrandCreateRequest } from './schema/BrandCreateRequest';
import type { BrandListRequest } from './schema/BrandListRequest';
import type { BrandResponse } from './schema/BrandResponse';
import type { BrandUpdateRequest } from './schema/BrandUpdateRequest';

const BASE_URL = '/api/brands';

const getUrl = (brandId?: string) => `${BASE_URL}${brandId ? '/' + brandId : ''}`;

const get = async (brandId: string): Promise<Brand | null> => {
	try {
		const response = await axios.get<BrandResponse>(getUrl(brandId));
		return Brand.fromResponse(response.data);
	} catch (error) {
		if (axios.isAxiosError(error) && error.response?.status === 404) {
			return null;
		}
		throw error;
	}
};

const list = async (props?: BrandListRequest): Promise<Brand[]> => {
	const response = await axios.get<BrandResponse[]>(getUrl(), { params: props });
	return response.data.map(Brand.fromResponse);
};

const create = async (data: BrandCreateRequest): Promise<Brand> => {
	const response = await axios.post<BrandResponse>(getUrl(), data);
	return Brand.fromResponse(response.data);
};

const update = async (brandId: string, data: BrandUpdateRequest): Promise<Brand> => {
	const formData = new FormData();
	formData.append('request_data', JSON.stringify(data));
	const response = await axios.put<BrandResponse>(getUrl(brandId), formData);
	return Brand.fromResponse(response.data);
};

const uploadLogo = async (
	brandId: string,
	logoFile: File,
	data: BrandUpdateRequest
): Promise<Brand> => {
	const formData = new FormData();
	formData.append('request_data', JSON.stringify(data));
	formData.append('logo_file', logoFile);
	const response = await axios.put<BrandResponse>(getUrl(brandId), formData);
	return Brand.fromResponse(response.data);
};

const remove = async (brandId: string): Promise<Brand> => {
	const response = await axios.delete<BrandResponse>(getUrl(brandId));
	return Brand.fromResponse(response.data);
};

export const BrandEndpoints = {
	get,
	list,
	create,
	update,
	uploadLogo,
	remove
};
