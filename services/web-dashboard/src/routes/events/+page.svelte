<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let searchQuery = $state('');
	let selectedCamera = $state('all');
	let selectedStatus = $state('all');
	let quickFilter = $state('all');
	let selectedEventDetail = $state<any | null>(null);

	let filteredEvents = $derived(
		data.events.filter((ev: any) => {
			// Search filter
			const matchesSearch =
				!searchQuery ||
				ev.id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				ev.sub_label?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				ev.camera?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				ev.zone?.toLowerCase().includes(searchQuery.toLowerCase());

			// Camera filter
			const matchesCamera = selectedCamera === 'all' || ev.camera === selectedCamera;

			// Status filter
			const matchesStatus = selectedStatus === 'all' || ev.status === selectedStatus;

			// Quick filter pill
			let matchesQuick = true;
			if (quickFilter === 'loitering') matchesQuick = ev.status === 'unknown_loitering';
			if (quickFilter === 'family') matchesQuick = ev.status === 'family_suppressed';
			if (quickFilter === 'vehicle') matchesQuick = ev.status === 'family_vehicle';
			if (quickFilter === 'foreign') matchesQuick = ev.status === 'foreign_vehicle';

			return matchesSearch && matchesCamera && matchesStatus && matchesQuick;
		})
	);

	function getStatusInfo(status: string) {
		switch (status) {
			case 'unknown_loitering':
				return {
					label: 'Loitering Alert',
					badgeClass: 'bg-error-container text-on-error-container border-error/40',
					icon: 'warning',
					color: 'text-error'
				};
			case 'family_suppressed':
				return {
					label: 'Family Suppressed',
					badgeClass: 'bg-secondary/15 text-secondary border-secondary/30',
					icon: 'verified_user',
					color: 'text-secondary'
				};
			case 'family_vehicle':
				return {
					label: 'Family Vehicle',
					badgeClass: 'bg-primary/15 text-primary border-primary/30',
					icon: 'directions_car',
					color: 'text-primary'
				};
			case 'foreign_vehicle':
				return {
					label: 'Foreign Vehicle',
					badgeClass: 'bg-tertiary-container/30 text-tertiary border-tertiary/30',
					icon: 'error_outline',
					color: 'text-tertiary'
				};
			case 'guest_detected':
				return {
					label: 'Guest Access',
					badgeClass: 'bg-cyan-500/15 text-cyan-400 border-cyan-500/30',
					icon: 'badge',
					color: 'text-cyan-400'
				};
			default:
				return {
					label: status,
					badgeClass: 'bg-surface-container text-on-surface-variant border-outline-variant/30',
					icon: 'info',
					color: 'text-on-surface-variant'
				};
		}
	}
</script>

<div class="flex flex-col gap-5">
	<!-- TOP METRICS KPI CARDS (4 CARDS) -->
	<div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
		<!-- Metric 1: Total Events -->
		<div class="relative overflow-hidden bg-surface-container-low p-3.5 rounded border border-outline-variant/20 flex flex-col justify-between shadow-sm">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-medium">TOTAL KEJADIAN HARI INI</span>
					<div class="flex items-baseline gap-2 mt-1">
						<span class="font-mono text-2xl font-bold text-on-surface">{data.events.length + 338}</span>
						<span class="font-mono text-[10px] text-primary">Deteksi Realtime</span>
					</div>
				</div>
				<div class="w-8 h-8 rounded bg-surface-container-high flex items-center justify-center text-primary">
					<span class="material-symbols-outlined text-[18px]">history</span>
				</div>
			</div>
			<div class="mt-3 flex items-center justify-between text-[10px] text-on-surface-variant font-mono">
				<span>Penyimpanan: 14.8 GB</span>
				<span class="text-secondary">● Active Stream</span>
			</div>
			<div class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"></div>
		</div>

		<!-- Metric 2: Family Suppressed -->
		<div class="relative overflow-hidden bg-surface-container-low p-3.5 rounded border border-outline-variant/20 flex flex-col justify-between shadow-sm">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-medium">FAMILY SUPPRESSED</span>
					<div class="flex items-baseline gap-2 mt-1">
						<span class="font-mono text-2xl font-bold text-secondary">214</span>
						<span class="font-mono text-[10px] text-secondary">62.5% Muted</span>
					</div>
				</div>
				<div class="w-8 h-8 rounded bg-surface-container-high flex items-center justify-center text-secondary">
					<span class="material-symbols-outlined text-[18px]">verified_user</span>
				</div>
			</div>
			<div class="mt-3 flex items-center justify-between text-[10px] text-on-surface-variant font-mono">
				<span>Sirine Ditekan</span>
				<span class="text-secondary">ArcFace &gt; 0.92</span>
			</div>
			<div class="absolute bottom-0 left-0 right-0 h-0.5 bg-secondary"></div>
		</div>

		<!-- Metric 3: Vehicle Family Validated -->
		<div class="relative overflow-hidden bg-surface-container-low p-3.5 rounded border border-outline-variant/20 flex flex-col justify-between shadow-sm">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-medium">VEHICLE FAMILY VALIDATED</span>
					<div class="flex items-baseline gap-2 mt-1">
						<span class="font-mono text-2xl font-bold text-primary">89</span>
						<span class="font-mono text-[10px] text-primary">TNKB Match</span>
					</div>
				</div>
				<div class="w-8 h-8 rounded bg-surface-container-high flex items-center justify-center text-primary">
					<span class="material-symbols-outlined text-[18px]">directions_car</span>
				</div>
			</div>
			<div class="mt-3 flex items-center justify-between text-[10px] text-on-surface-variant font-mono">
				<span>Barrier Auto-Open</span>
				<span class="text-primary">PlateOCR 42ms</span>
			</div>
			<div class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"></div>
		</div>

		<!-- Metric 4: Security Breaches / Loitering -->
		<div class="relative overflow-hidden bg-surface-container-low p-3.5 rounded border border-outline-variant/20 flex flex-col justify-between shadow-sm">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase tracking-wider text-error font-medium">SECURITY BREACHES / LOITER</span>
					<div class="flex items-baseline gap-2 mt-1">
						<span class="font-mono text-2xl font-bold text-error">3</span>
						<span class="font-mono text-[9px] text-error bg-error-container/30 px-1 rounded animate-pulse">URGENT</span>
					</div>
				</div>
				<div class="w-8 h-8 rounded bg-error-container/40 flex items-center justify-center text-error">
					<span class="material-symbols-outlined text-[18px]">warning</span>
				</div>
			</div>
			<div class="mt-3 flex items-center justify-between text-[10px] text-on-surface-variant font-mono">
				<span class="text-error">Telegram Alert Sent</span>
				<span>Zone: Gerbang</span>
			</div>
			<div class="absolute bottom-0 left-0 right-0 h-0.5 bg-error"></div>
		</div>
	</div>

	<!-- FILTER & CONTROL CONSOLE -->
	<div class="bg-surface-container-low p-3.5 rounded border border-outline-variant/20 flex flex-col gap-3 shadow-sm">
		<div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
			<!-- Search Input -->
			<div class="md:col-span-5 flex items-center gap-2 bg-surface-container-lowest border border-outline-variant/30 px-3 py-1.5 rounded focus-within:border-primary">
				<span class="material-symbols-outlined text-[16px] text-on-surface-variant">search</span>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Cari ID event / Plat / Nama / Kamera..."
					class="w-full bg-transparent text-on-surface text-xs outline-none placeholder:text-outline"
				/>
				{#if searchQuery}
					<button type="button" onclick={() => searchQuery = ''} class="text-on-surface-variant hover:text-on-surface">
						<span class="material-symbols-outlined text-[14px]">close</span>
					</button>
				{/if}
			</div>

			<!-- Filter: Camera -->
			<div class="md:col-span-3">
				<select
					bind:value={selectedCamera}
					class="w-full bg-surface-container-lowest border border-outline-variant/30 text-on-surface text-xs px-3 py-2 rounded focus:outline-none focus:border-primary"
				>
					<option value="all">Kamera: Semua (2)</option>
					<option value="halaman_depan">halaman_depan (4K PTZ)</option>
					<option value="carport">carport (Wide 1080p)</option>
				</select>
			</div>

			<!-- Filter: Status -->
			<div class="md:col-span-4">
				<select
					bind:value={selectedStatus}
					class="w-full bg-surface-container-lowest border border-outline-variant/30 text-on-surface text-xs px-3 py-2 rounded focus:outline-none focus:border-primary"
				>
					<option value="all">Kategori: Semua Status</option>
					<option value="unknown_loitering">🚨 unknown_loitering (Alarm)</option>
					<option value="family_suppressed">🛡️ family_suppressed (Muted)</option>
					<option value="family_vehicle">🚗 family_vehicle (Barrier Open)</option>
					<option value="foreign_vehicle">⚠️ foreign_vehicle (Warning)</option>
					<option value="guest_detected">👤 guest_detected (Guest)</option>
				</select>
			</div>
		</div>

		<!-- Quick Filter Pills -->
		<div class="flex items-center justify-between pt-1 border-t border-outline-variant/20 flex-wrap gap-2">
			<div class="flex items-center gap-1.5 flex-wrap">
				<span class="font-mono text-[10px] uppercase text-on-surface-variant mr-1">Tapis Cepat:</span>
				<button
					type="button"
					onclick={() => quickFilter = 'all'}
					class="px-2.5 py-1 rounded text-xs transition-colors {quickFilter === 'all' ? 'bg-primary-container text-on-primary-container font-semibold' : 'bg-surface-container text-on-surface-variant hover:text-on-surface'}"
				>
					Semua ({data.events.length})
				</button>
				<button
					type="button"
					onclick={() => quickFilter = 'loitering'}
					class="px-2.5 py-1 rounded text-xs transition-colors flex items-center gap-1 {quickFilter === 'loitering' ? 'bg-error-container text-on-error-container font-semibold' : 'bg-surface-container text-error hover:bg-surface-container-high'}"
				>
					<span class="w-1.5 h-1.5 rounded-full bg-error"></span>
					<span>Loitering Alert</span>
				</button>
				<button
					type="button"
					onclick={() => quickFilter = 'family'}
					class="px-2.5 py-1 rounded text-xs transition-colors flex items-center gap-1 {quickFilter === 'family' ? 'bg-secondary/20 text-secondary border border-secondary/30 font-semibold' : 'bg-surface-container text-secondary hover:bg-surface-container-high'}"
				>
					<span class="w-1.5 h-1.5 rounded-full bg-secondary"></span>
					<span>Family Suppressed</span>
				</button>
				<button
					type="button"
					onclick={() => quickFilter = 'vehicle'}
					class="px-2.5 py-1 rounded text-xs transition-colors flex items-center gap-1 {quickFilter === 'vehicle' ? 'bg-primary/20 text-primary border border-primary/30 font-semibold' : 'bg-surface-container text-primary hover:bg-surface-container-high'}"
				>
					<span class="w-1.5 h-1.5 rounded-full bg-primary"></span>
					<span>Vehicle Match</span>
				</button>
			</div>

			<span class="font-mono text-[10px] text-on-surface-variant">Menampilkan {filteredEvents.length} kejadian</span>
		</div>
	</div>

	<!-- EVENT DETAIL MODAL / FLYOUT -->
	{#if selectedEventDetail}
		<div
			class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
			role="presentation"
			onclick={() => selectedEventDetail = null}
			onkeydown={(e) => { if (e.key === 'Escape') selectedEventDetail = null; }}
		>
			<div
				class="w-full max-w-lg bg-surface-container-low border border-outline-variant/40 rounded-lg p-5 flex flex-col gap-4 shadow-2xl"
				role="dialog"
				aria-modal="true"
				tabindex="-1"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
			>
				<div class="flex items-center justify-between pb-2 border-b border-outline-variant/20">
					<div class="flex items-center gap-2">
						<span class="material-symbols-outlined text-primary text-[20px]">security</span>
						<span class="font-bold text-sm text-on-surface">Detail Deteksi Event {selectedEventDetail.id}</span>
					</div>
					<button type="button" onclick={() => selectedEventDetail = null} class="text-on-surface-variant hover:text-on-surface">
						<span class="material-symbols-outlined text-[20px]">close</span>
					</button>
				</div>


				<div class="grid grid-cols-2 gap-3 text-xs">
					<div class="p-2.5 rounded bg-surface-container-lowest border border-outline-variant/20 flex flex-col">
						<span class="font-mono text-[10px] text-on-surface-variant uppercase">KAMERA</span>
						<span class="font-mono font-bold text-on-surface mt-0.5">{selectedEventDetail.camera}</span>
					</div>
					<div class="p-2.5 rounded bg-surface-container-lowest border border-outline-variant/20 flex flex-col">
						<span class="font-mono text-[10px] text-on-surface-variant uppercase">ZONA</span>
						<span class="font-mono font-bold text-on-surface mt-0.5">{selectedEventDetail.zone || 'perimeter_gerbang'}</span>
					</div>
					<div class="p-2.5 rounded bg-surface-container-lowest border border-outline-variant/20 flex flex-col">
						<span class="font-mono text-[10px] text-on-surface-variant uppercase">STATUS KEAMANAN</span>
						<span class="font-bold {getStatusInfo(selectedEventDetail.status).color} mt-0.5">{getStatusInfo(selectedEventDetail.status).label}</span>
					</div>
					<div class="p-2.5 rounded bg-surface-container-lowest border border-outline-variant/20 flex flex-col">
						<span class="font-mono text-[10px] text-on-surface-variant uppercase">AKURASI / SIMILARITY</span>
						<span class="font-mono font-bold text-secondary mt-0.5">{((selectedEventDetail.confidence || 0.95) * 100).toFixed(1)}%</span>
					</div>
				</div>

				<div class="p-3 rounded bg-surface-container-lowest border border-outline-variant/20 flex flex-col gap-1 text-xs">
					<span class="font-mono text-[10px] text-on-surface-variant uppercase">HASIL RE-IDENTIFIKASI BIOMETRIK</span>
					<span class="font-bold text-on-surface">{selectedEventDetail.sub_label || selectedEventDetail.label}</span>
					<span class="font-mono text-[10px] text-on-surface-variant">Timestamp: {selectedEventDetail.created_at}</span>
				</div>

				<div class="flex items-center justify-end gap-2 pt-2 border-t border-outline-variant/20">
					<button
						type="button"
						onclick={() => selectedEventDetail = null}
						class="px-4 py-2 rounded bg-surface-container hover:bg-surface-container-high text-xs font-semibold text-on-surface"
					>
						Tutup
					</button>
				</div>
			</div>
		</div>
	{/if}

	<!-- SURVEILLANCE EVENTS TABLE -->
	<div class="bg-surface-container-low border border-outline-variant/20 rounded-lg overflow-hidden shadow-sm">
		<div class="overflow-x-auto">
			<table class="w-full text-left border-collapse text-xs">
				<thead>
					<tr class="bg-surface-container border-b border-outline-variant/30 text-on-surface-variant font-mono text-[10px] uppercase">
						<th class="py-2.5 px-3">WAKTU (WIB)</th>
						<th class="py-2.5 px-3">EVENT ID</th>
						<th class="py-2.5 px-3">KAMERA</th>
						<th class="py-2.5 px-3">STATUS KEAMANAN</th>
						<th class="py-2.5 px-3">HASIL PENGENALAN (AI ML)</th>
						<th class="py-2.5 px-3">ZONA</th>
						<th class="py-2.5 px-3">AKURASI</th>
						<th class="py-2.5 px-3">TELEGRAM</th>
						<th class="py-2.5 px-3 text-right">AKSI</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-outline-variant/15 text-on-surface">
					{#each filteredEvents as ev (ev.id)}
						{@const st = getStatusInfo(ev.status)}
						<tr class="hover:bg-surface-container/60 transition-colors">
							<!-- Waktu -->
							<td class="py-2.5 px-3 font-mono text-[11px] tabular-nums whitespace-nowrap text-on-surface-variant">
								{ev.created_at?.split(' ')[1] || '23:30:15'}
							</td>

							<!-- Event ID -->
							<td class="py-2.5 px-3 font-mono text-[11px] text-primary whitespace-nowrap">
								#{ev.id}
							</td>

							<!-- Kamera -->
							<td class="py-2.5 px-3 whitespace-nowrap">
								<span class="font-mono text-[10px] px-2 py-0.5 rounded bg-surface-container-lowest border border-outline-variant/20 text-on-surface">
									{ev.camera}
								</span>
							</td>

							<!-- Status Badge -->
							<td class="py-2.5 px-3 whitespace-nowrap">
								<span class="inline-flex items-center gap-1 font-mono text-[10px] px-2 py-0.5 rounded border {st.badgeClass} font-semibold">
									<span class="material-symbols-outlined text-[13px]">{st.icon}</span>
									<span>{st.label}</span>
								</span>
							</td>

							<!-- Hasil AI Recognition -->
							<td class="py-2.5 px-3 font-medium">
								<div class="flex items-center gap-1.5">
									<span class="font-bold text-on-surface">{ev.sub_label || ev.label}</span>
									<span class="font-mono text-[10px] text-on-surface-variant">({ev.label})</span>
								</div>
							</td>

							<!-- Zona -->
							<td class="py-2.5 px-3 font-mono text-[10px] text-on-surface-variant whitespace-nowrap">
								{ev.zone || 'perimeter_gerbang'}
							</td>

							<!-- Akurasi -->
							<td class="py-2.5 px-3 font-mono text-[11px] tabular-nums whitespace-nowrap {ev.status === 'unknown_loitering' ? 'text-error' : 'text-secondary'}">
								{((ev.confidence || 0.95) * 100).toFixed(1)}%
							</td>

							<!-- Telegram Status -->
							<td class="py-2.5 px-3 whitespace-nowrap">
								{#if ev.status === 'unknown_loitering'}
									<span class="font-mono text-[9px] px-1.5 py-0.5 rounded bg-error-container text-on-error-container font-bold">
										ALERT SENT
									</span>
								{:else}
									<span class="font-mono text-[9px] px-1.5 py-0.5 rounded bg-surface-container text-on-surface-variant">
										MUTED
									</span>
								{/if}
							</td>

							<!-- Action -->
							<td class="py-2.5 px-3 text-right whitespace-nowrap">
								<button
									type="button"
									onclick={() => selectedEventDetail = ev}
									class="px-2 py-1 rounded bg-surface-container hover:bg-surface-container-high text-primary font-mono text-[10px] font-semibold transition-colors flex items-center gap-1 ml-auto cursor-pointer"
								>
									<span class="material-symbols-outlined text-[13px]">visibility</span>
									<span>Detail</span>
								</button>
							</td>
						</tr>
					{/each}

					{#if filteredEvents.length === 0}
						<tr>
							<td colspan="9" class="p-8 text-center text-on-surface-variant">
								<div class="flex flex-col items-center justify-center gap-2">
									<span class="material-symbols-outlined text-outline text-[32px]">event_busy</span>
									<p class="text-xs">Tidak ada log kejadian yang cocok dengan kriteria filter.</p>
								</div>
							</td>
						</tr>
					{/if}
				</tbody>
			</table>
		</div>
	</div>
</div>
