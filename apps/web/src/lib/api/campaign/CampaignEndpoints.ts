import axios from 'axios';
import { Campaign, type CampaignResponse } from './Campaign';
import type { CampaignListRequest } from './CampaignListRequest';

const BASE_URL = '/api/brands/';

const getUrl = (brandId: string, campaignId?: string) =>
	`${BASE_URL}${brandId}/campaigns${campaignId ? `/${campaignId}` : ''}`;

const listForBrand = async (brandId: string, props?: CampaignListRequest): Promise<Campaign[]> => {
	const response = await axios.get<CampaignResponse[]>(getUrl(brandId), {
		params: props
	});
	return response.data.map((r) => Campaign.fromResponse(r));
};

const remove = async (brandId: string, campaignId: string): Promise<void> => {
	await axios.delete(getUrl(brandId, campaignId));
};

export const CampaignEndpoints = {
	listForBrand,
	remove
};
