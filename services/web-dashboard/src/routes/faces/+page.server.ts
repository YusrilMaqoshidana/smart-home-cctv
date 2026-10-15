import { fetchFaces, addFace, deleteFace } from '$lib/server/api';
import type { PageServerLoad, Actions } from './$types';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
	const faces = await fetchFaces();
	return { faces };
};

export const actions: Actions = {
	add: async ({ request }) => {
		const formData = await request.formData();
		const name = formData.get('name')?.toString();
		const role = formData.get('role')?.toString() || 'resident';

		if (!name) {
			return fail(400, { error: 'Nama anggota keluarga wajib diisi' });
		}

		await addFace(name, role);
		return { success: true };
	},
	delete: async ({ request }) => {
		const formData = await request.formData();
		const idStr = formData.get('id')?.toString();
		if (!idStr) return fail(400, { error: 'ID tidak valid' });

		await deleteFace(parseInt(idStr, 10));
		return { success: true };
	}
};
