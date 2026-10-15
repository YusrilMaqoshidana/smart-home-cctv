<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
		<div>
			<h1 class="text-lg font-bold text-slate-100 flex items-center gap-2">
				<i class="fa-solid fa-list-ul text-indigo-400"></i> Log Riwayat Kejadian (Event Feed)
			</h1>
			<p class="text-xs text-slate-400">
				Catatan kronologis seluruh objek yang terdeteksi oleh Frigate NVR dan hasil inferensi AI.
			</p>
		</div>
		<span class="text-xs font-mono px-3 py-1 bg-slate-900 border border-slate-800 rounded-xl text-slate-300">
			Total Event: {data.events.length}
		</span>
	</div>

	<!-- Event Logs Table -->
	<div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
		<div class="overflow-x-auto">
			<table class="w-full text-left text-xs">
				<thead class="text-slate-400 border-b border-slate-800 bg-slate-950/40">
					<tr>
						<th class="py-2.5 px-3">Waktu</th>
						<th class="py-2.5 px-3">Kamera</th>
						<th class="py-2.5 px-3">Objek</th>
						<th class="py-2.5 px-3">Hasil AI</th>
						<th class="py-2.5 px-3">Status Sistem</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-slate-800/60 font-mono">
					{#each data.events as event}
						<tr class="hover:bg-slate-800/30">
							<td class="py-3 px-3 text-slate-400 text-[11px]">
								{event.created_at}
							</td>
							<td class="py-3 px-3 font-sans">
								<span class="font-medium text-slate-200">
									{event.camera.includes('halaman') ? 'Halaman Depan' : 'Carport & Garasi'}
								</span>
							</td>
							<td class="py-3 px-3 text-slate-300 uppercase text-[11px]">
								{event.label}
							</td>
							<td class="py-3 px-3 font-sans font-medium text-slate-200">
								{event.sub_label || '-'}
							</td>
							<td class="py-3 px-3 font-sans">
								{#if event.status === 'family_suppressed'}
									<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
										🟢 Penghuni (Alarm Disupresi)
									</span>
								{:else if event.status === 'family_vehicle'}
									<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-medium">
										🚗 Kendaraan Keluarga
									</span>
								{:else if event.status === 'foreign_vehicle'}
									<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 font-medium">
										⚠️ Kendaraan Asing
									</span>
								{:else if event.status === 'unknown_loitering'}
									<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] bg-rose-500/10 text-rose-400 border border-rose-500/20 font-medium">
										🔴 Peringatan Loitering
									</span>
								{:else}
									<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] bg-slate-800 text-slate-400 font-medium">
										{event.status}
									</span>
								{/if}
							</td>
						</tr>
					{:else}
						<tr>
							<td colspan="5" class="py-8 text-center text-slate-500 font-sans">
								Belum ada riwayat aktivitas yang tercatat dalam log.
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>
