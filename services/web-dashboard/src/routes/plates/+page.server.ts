import { fetchPlates, addPlate, deletePlate } from '$lib/server/api';
import type { PageServerLoad, Actions } from './$types';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
	const plates = await fetchPlates();
	return { plates };
};

export const actions: Actions = {
	add: async ({ request }) => {
		const formData = await request.formData();
		const plate_number = formData.get('plate_number')?.toString()?.trim();
		const owner_label = formData.get('owner_label')?.toString()?.trim();
		const vehicle_type = formData.get('vehicle_type')?.toString() || 'car';

		if (!plate_number || !owner_label) {
			return fail(400, { error: 'Nomor plat dan keterangan wajib diisi' });
		}

		// Indonesian TNKB validation
		const tnkbRegex = /^([A-Z]{1,2})\s*([0-9]{1,4})\s*([A-Z]{1,3})$/i;
		if (!tnkbRegex.test(plate_number)) {
			return fail(400, {
				error: `Format plat nomor '${plate_number}' tidak valid. Gunakan pola TNKB Indonesia (contoh: B 1234 XYZ atau D 8888 ZZ)`
			});
		}

		const result = await addPlate(plate_number, owner_label, vehicle_type);
		if (result && result.error) {
			return fail(400, { error: result.error });
		}

		return { success: true };
	},
	delete: async ({ request }) => {
		const formData = await request.formData();
		const idStr = formData.get('id')?.toString();
		if (!idStr) return fail(400, { error: 'ID tidak valid' });

		await deletePlate(parseInt(idStr, 10));
		return { success: true };
	}
};
