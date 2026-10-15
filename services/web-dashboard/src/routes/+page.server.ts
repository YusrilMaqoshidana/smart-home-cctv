import { fetchSystemStatus, fetchFaces, fetchPlates, fetchEvents } from '$lib/server/api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const [status, faces, plates, events] = await Promise.all([
		fetchSystemStatus(),
		fetchFaces(),
		fetchPlates(),
		fetchEvents()
	]);

	return {
		status,
		faces,
		plates,
		events
	};
};
