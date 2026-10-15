import { fetchEvents } from '$lib/server/api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const events = await fetchEvents();
	return { events };
};
