<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="space-y-8">
	<!-- System Resource Status Bar (Server-Side Computed) -->
	<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
		<div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 shadow-sm">
			<div class="flex items-center justify-between text-xs text-slate-400 mb-1">
				<span>Hardware Host</span>
				<i class="fa-solid fa-server text-indigo-400"></i>
			</div>
			<p class="text-sm font-semibold text-slate-100">{data.status.server}</p>
			<p class="text-[11px] text-slate-400 mt-0.5">{data.status.cpu}</p>
		</div>

		<div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 shadow-sm">
			<div class="flex items-center justify-between text-xs text-slate-400 mb-1">
				<span>Akselerasi Video</span>
				<i class="fa-solid fa-microchip text-emerald-400"></i>
			</div>
			<p class="text-sm font-semibold text-emerald-400">{data.status.hwaccel}</p>
			<p class="text-[11px] text-slate-400 mt-0.5">Hardware H.264/H.265 Decode</p>
		</div>

		<div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 shadow-sm">
			<div class="flex items-center justify-between text-xs text-slate-400 mb-1">
				<span>Penyimpanan NVMe</span>
				<i class="fa-solid fa-hard-drive text-cyan-400"></i>
			</div>
			<p class="text-sm font-semibold text-slate-100">{data.status.storage_quota_cctv}</p>
			<p class="text-[11px] text-slate-400 mt-0.5">Retensi 7 Hari + FIFO Auto-prune</p>
		</div>

		<div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 shadow-sm">
			<div class="flex items-center justify-between text-xs text-slate-400 mb-1">
				<span>Grup Telegram</span>
				<i class="fa-brands fa-telegram text-sky-400"></i>
			</div>
			<p class="text-sm font-semibold text-slate-100">CCTV Rumah Alert</p>
			<p class="text-[11px] text-emerald-400 font-mono mt-0.5">● Bot Terhubung</p>
		</div>
	</div>

	<!-- Live Video Feeds Grid -->
	<section class="space-y-4">
		<div class="flex items-center justify-between">
			<div>
				<h2 class="text-base font-semibold text-slate-100 flex items-center gap-2">
					<i class="fa-solid fa-video text-indigo-400"></i> Pantauan Kamera Perimeter (Live View)
				</h2>
				<p class="text-xs text-slate-400">Stream WebRTC langsung via go2rtc tanpa delay (ultra-low latency).</p>
			</div>
			<span class="text-xs px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700 text-slate-300 font-mono">
				2 Kamera Terdaftar
			</span>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
			<!-- Camera 1: Halaman Depan (Active from Laptop Webcam / CCTV) -->
			<div class="bg-slate-900 border border-slate-800/90 rounded-2xl overflow-hidden shadow-xl flex flex-col">
				<div class="px-4 py-3 bg-slate-800/40 border-b border-slate-800 flex items-center justify-between text-xs">
					<div class="flex items-center gap-2">
						<span class="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
						<span class="font-semibold text-slate-200">Kamera 1: Halaman Depan & Pagar</span>
					</div>
					<span class="text-emerald-400 font-mono">1080p @ 7 FPS (Sub)</span>
				</div>
				<div class="aspect-video bg-black relative flex items-center justify-center">
					<iframe 
						src="http://localhost:8889/halaman_depan" 
						title="Live Stream Halaman Depan"
						class="w-full h-full border-0" 
						allow="autoplay; fullscreen"
						loading="lazy">
					</iframe>
				</div>
				<div class="p-3 bg-slate-900/90 border-t border-slate-800/60 flex items-center justify-between text-xs text-slate-400">
					<span>Zona: <code class="text-slate-300">perimeter_gerbang</code>, <code class="text-slate-300">teras_depan</code></span>
					<span class="text-indigo-400 font-medium">InsightFace Active</span>
				</div>
			</div>

			<!-- Camera 2: Carport & Garasi -->
			<div class="bg-slate-900 border border-slate-800/90 rounded-2xl overflow-hidden shadow-xl flex flex-col">
				<div class="px-4 py-3 bg-slate-800/40 border-b border-slate-800 flex items-center justify-between text-xs">
					<div class="flex items-center gap-2">
						<span class="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
						<span class="font-semibold text-slate-200">Kamera 2: Carport & Pintu Garasi</span>
					</div>
					<span class="text-slate-400 font-mono">1080p @ 7 FPS (Sub)</span>
				</div>
				<div class="aspect-video bg-black relative flex items-center justify-center">
					<div class="text-center p-6 space-y-2">
						<i class="fa-solid fa-car text-slate-700 text-4xl"></i>
						<p class="text-xs text-slate-400">Menunggu stream kamera fisik tiba besok</p>
						<span class="inline-block text-[10px] text-slate-500 font-mono px-2 py-0.5 rounded bg-slate-800">RTSP: carport</span>
					</div>
				</div>
				<div class="p-3 bg-slate-900/90 border-t border-slate-800/60 flex items-center justify-between text-xs text-slate-400">
					<span>Zona: <code class="text-slate-300">area_parkir</code>, <code class="text-slate-300">pintu_garasi</code></span>
					<span class="text-cyan-400 font-medium">TNKB ANPR Active</span>
				</div>
			</div>
		</div>
	</section>

	<!-- Quick Whitelist Summary -->
	<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
		<div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
			<div class="flex items-center justify-between">
				<h3 class="text-sm font-semibold text-slate-200 flex items-center gap-2">
					<i class="fa-solid fa-user-check text-emerald-400"></i> Wajah Keluarga ({data.faces.length})
				</h3>
				<a href="/faces" class="text-xs text-indigo-400 hover:text-indigo-300">Kelola Semua &rarr;</a>
			</div>
			<div class="divide-y divide-slate-800/60">
				{#each data.faces.slice(0, 4) as face}
					<div class="py-2.5 flex items-center justify-between text-xs">
						<div class="flex items-center gap-3">
							<div class="h-7 w-7 rounded-full bg-indigo-950 border border-indigo-500/30 flex items-center justify-center text-xs">
								👤
							</div>
							<div>
								<p class="font-medium text-slate-200">{face.name}</p>
								<p class="text-[10px] text-slate-400 capitalize">{face.role}</p>
							</div>
						</div>
						<span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-medium">
							Penghuni Tetap
						</span>
					</div>
				{/each}
			</div>
		</div>

		<div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
			<div class="flex items-center justify-between">
				<h3 class="text-sm font-semibold text-slate-200 flex items-center gap-2">
					<i class="fa-solid fa-car text-cyan-400"></i> Plat Kendaraan ({data.plates.length})
				</h3>
				<a href="/plates" class="text-xs text-indigo-400 hover:text-indigo-300">Kelola Semua &rarr;</a>
			</div>
			<div class="divide-y divide-slate-800/60">
				{#each data.plates.slice(0, 4) as plate}
					<div class="py-2.5 flex items-center justify-between text-xs">
						<div class="flex items-center gap-3">
							<span class="px-2 py-1 bg-black border border-slate-700 rounded text-xs font-mono font-bold text-white tracking-widest">
								{plate.display_plate}
							</span>
							<span class="text-slate-300 text-xs">{plate.owner_label}</span>
						</div>
						<span class="text-[10px] text-slate-400 uppercase font-mono">{plate.vehicle_type}</span>
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>
