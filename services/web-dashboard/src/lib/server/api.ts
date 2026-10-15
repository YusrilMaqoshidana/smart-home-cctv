/**
 * Server-only API client for SvelteKit SSR.
 * All requests are executed on the server inside Docker network.
 * Zero tokens or internal URLs are exposed to the client browser.
 */

const BACKEND_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

export async function fetchSystemStatus() {
	try {
		const res = await fetch(`${BACKEND_URL}/api/status`, { signal: AbortSignal.timeout(3000) });
		if (res.ok) return await res.json();
	} catch (e) {
		console.warn('[API Client] Backend API unreachable for status:', e);
	}
	return {
		status: 'connecting',
		server: 'Production CCTV Host',
		cpu: 'Intel QuickSync / VAAPI Host',
		ram_total: '32 GB',
		storage_quota_cctv: '300 GB NVMe Storage',
		cameras: ['halaman_depan', 'carport'],
		hwaccel: 'Intel QuickSync (VAAPI)'
	};
}

export async function fetchFaces() {
	try {
		const res = await fetch(`${BACKEND_URL}/api/faces`, { signal: AbortSignal.timeout(3000) });
		if (res.ok) {
			const data = await res.json();
			return data.faces || [];
		}
	} catch (e) {
		console.warn('[API Client] Backend API unreachable for faces:', e);
	}
	return [];
}

export async function addFace(name: string, role: string) {
	// Auto-generate 512-d normalized mock embedding for SSR web form
	const dim = 512;
	const val = 1.0 / Math.sqrt(dim);
	const embedding = new Array(dim).fill(val);

	const res = await fetch(`${BACKEND_URL}/api/faces`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ name, role, embedding })
	});
	return await res.json();
}

export async function deleteFace(id: number) {
	const res = await fetch(`${BACKEND_URL}/api/faces/${id}`, { method: 'DELETE' });
	return await res.json();
}

export async function fetchPlates() {
	try {
		const res = await fetch(`${BACKEND_URL}/api/plates`, { signal: AbortSignal.timeout(3000) });
		if (res.ok) {
			const data = await res.json();
			return data.plates || [];
		}
	} catch (e) {
		console.warn('[API Client] Backend API unreachable for plates:', e);
	}
	return [];
}

export async function addPlate(plate_number: string, owner_label: string, vehicle_type: string) {
	const res = await fetch(`${BACKEND_URL}/api/plates`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ plate_number, owner_label, vehicle_type, is_family: true })
	});
	return await res.json();
}

export async function deletePlate(id: number) {
	const res = await fetch(`${BACKEND_URL}/api/plates/${id}`, { method: 'DELETE' });
	return await res.json();
}

export async function fetchEvents() {
	try {
		const res = await fetch(`${BACKEND_URL}/api/events`, { signal: AbortSignal.timeout(3000) });
		if (res.ok) {
			const data = await res.json();
			return data.events || [];
		}
	} catch (e) {
		console.warn('[API Client] Backend API unreachable for events:', e);
	}
	return [];
}
