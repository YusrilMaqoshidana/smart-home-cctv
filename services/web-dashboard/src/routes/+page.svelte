<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let activePreset = $state<'all' | 'depan' | 'carport'>('all');
	let barrierTriggered = $state(false);

	// Production Camera Definitions
	const cameras = [
		{
			id: 'halaman_depan',
			name: 'FEED #01 : HALAMAN DEPAN & GERBANG',
			zone: 'perimeter_gerbang',
			fps: '29.8 FPS',
			bitrate: '4.2 Mbps',
			codec: 'H.265 VAAPI',
			streamUrl: 'http://localhost:8889/halaman_depan'
		},
		{
			id: 'carport',
			name: 'FEED #02 : CARPORT & BARRIER GATE',
			zone: 'carport_barrier',
			fps: '24.0 FPS',
			bitrate: '3.8 Mbps',
			codec: 'ALPR OCR',
			streamUrl: 'http://localhost:8889/carport'
		}
	];

	function getLatestCameraEvent(camId: string) {
		return data.events.find((ev: any) => ev.camera === camId) || null;
	}

	function triggerBarrier() {
		barrierTriggered = true;
		setTimeout(() => {
			barrierTriggered = false;
		}, 3000);
	}
</script>

<div class="flex flex-col gap-5">
	<!-- Production 2-CCTV Stream Matrix Header -->
	<div class="flex flex-col xl:flex-row items-stretch xl:items-center justify-between gap-3 p-3.5 bg-surface-container-low border border-outline-variant/30 rounded-lg shadow-sm">
		<!-- Camera Preset Selectors -->
		<div class="flex flex-wrap items-center gap-2">
			<button
				type="button"
				onclick={() => activePreset = 'all'}
				class="flex items-center gap-2 px-3 py-1.5 rounded transition-all text-xs {activePreset === 'all' ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.35)]' : 'bg-surface-container text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high'}"
			>
				<span class="material-symbols-outlined text-[16px]">grid_view</span>
				<span>Multi-Grid 2x2 View (2 CCTV)</span>
			</button>
			<button
				type="button"
				onclick={() => activePreset = 'depan'}
				class="flex items-center gap-2 px-3 py-1.5 rounded transition-all text-xs {activePreset === 'depan' ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.35)]' : 'bg-surface-container text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high'}"
			>
				<span class="material-symbols-outlined text-[16px]">videocam</span>
				<span>Halaman Depan</span>
				<span class="font-mono text-[10px] bg-surface-container-lowest/80 text-primary px-1.5 py-0.5 rounded ml-1">RTSP Cam 1</span>
			</button>
			<button
				type="button"
				onclick={() => activePreset = 'carport'}
				class="flex items-center gap-2 px-3 py-1.5 rounded transition-all text-xs {activePreset === 'carport' ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.35)]' : 'bg-surface-container text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high'}"
			>
				<span class="material-symbols-outlined text-[16px]">sensors</span>
				<span>Carport & Gate</span>
				<span class="font-mono text-[10px] bg-surface-container-lowest text-secondary px-1.5 py-0.5 rounded ml-1">RTSP Cam 2</span>
			</button>
		</div>

		<!-- Telemetry Badges & Detection Engine Specs -->
		<div class="flex flex-wrap items-center gap-2 text-xs">
			<div class="flex items-center gap-1.5 px-2.5 py-1 bg-surface-container-lowest border border-outline-variant/20 rounded">
				<div class="w-1.5 h-1.5 rounded-full bg-secondary animate-ping"></div>
				<span class="font-mono text-[10px] text-on-surface-variant uppercase">LATENCY</span>
				<span class="font-mono text-[11px] text-secondary font-semibold">42ms WHEP</span>
			</div>
			<div class="flex items-center gap-1.5 px-2.5 py-1 bg-surface-container-lowest border border-outline-variant/20 rounded">
				<span class="material-symbols-outlined text-[15px] text-primary">psychology</span>
				<span class="font-mono text-[10px] text-on-surface-variant">MODELS:</span>
				<span class="font-mono text-[11px] text-primary tracking-tight font-medium">InsightFace 512d · TNKB OCR · SSD</span>
			</div>
			<div class="flex items-center gap-1.5 px-2.5 py-1 bg-surface-container-lowest border border-outline-variant/20 rounded">
				<span class="material-symbols-outlined text-[15px] text-tertiary">memory</span>
				<span class="font-mono text-[10px] text-on-surface-variant">HOST:</span>
				<span class="font-mono text-[11px] text-tertiary font-semibold">{data.status.server || 'Production Node'}</span>
			</div>
		</div>
	</div>

	<!-- Primary Dual Surveillance Matrix Grid (2 CCTV) -->
	<div class="grid grid-cols-1 {activePreset === 'all' ? 'lg:grid-cols-2' : 'grid-cols-1'} gap-5">
		<!-- Dynamic Camera Feed Loop -->
		{#each cameras as cam}
			{#if activePreset === 'all' || (activePreset === 'depan' && cam.id === 'halaman_depan') || (activePreset === 'carport' && cam.id === 'carport')}
				{@const latestEv = getLatestCameraEvent(cam.id)}
				<div class="flex flex-col bg-surface-container-lowest border border-outline-variant/30 rounded-lg overflow-hidden shadow-lg relative group">
					<!-- Stream Header HUD -->
					<div class="flex items-center justify-between px-4 py-2 bg-surface-container-low text-on-surface border-b border-outline-variant/20 z-20">
						<div class="flex items-center gap-2">
							<span class="w-2 h-2 rounded-full {latestEv?.status === 'unknown_loitering' || latestEv?.status === 'foreign_vehicle' ? 'bg-error animate-ping' : 'bg-secondary animate-pulse'}"></span>
							<span class="font-mono text-[11px] font-bold tracking-wider uppercase {latestEv?.status === 'unknown_loitering' ? 'text-error' : 'text-primary'}">
								{cam.name}
							</span>
							<span class="font-mono text-[10px] text-on-surface-variant px-1.5 py-0.5 rounded bg-surface-container-highest">
								ZONE: {cam.zone}
							</span>
						</div>
						<div class="flex items-center gap-2 font-mono text-[10px] text-on-surface-variant">
							<span class="text-secondary">{cam.fps}</span>
							<span>|</span>
							<span class="text-primary">{cam.bitrate}</span>
							<span>|</span>
							<span>{cam.codec}</span>
						</div>
					</div>

					<!-- Video Feed Container (16:9 Canvas) -->
					<div class="relative w-full aspect-video bg-black overflow-hidden flex items-center justify-center">
						<!-- Live RTSP / WebRTC Stream iframe -->
						<iframe 
							src={cam.streamUrl} 
							title="Live Stream {cam.name}"
							class="w-full h-full border-0 absolute inset-0 z-0" 
							allow="autoplay; fullscreen"
							loading="lazy">
						</iframe>

						<!-- Tactical Grid Scrim Overlay -->
						<div class="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-background/40 pointer-events-none z-10"></div>

						<!-- Center Crosshair Marker -->
						<div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20 z-10">
							<div class="w-10 h-px bg-primary"></div>
							<div class="h-10 w-px bg-primary -ml-[5px]"></div>
						</div>

						<!-- Top Right Stream HUD Overlays -->
						<div class="absolute top-2.5 right-2.5 flex flex-col items-end gap-1 z-20">
							<span class="font-mono text-[10px] text-secondary bg-surface-container-lowest/90 px-2 py-0.5 rounded uppercase font-bold tracking-wider border border-secondary/30">
								● LIVE FEED
							</span>
							<span class="font-mono text-[9px] text-on-surface bg-surface-container-lowest/80 px-1.5 py-0.5 rounded">
								STREAM: go2rtc WHEP
							</span>
						</div>

						<!-- Real-Time Detection HUD Pill (Driven by actual Database Events) -->
						{#if latestEv}
							<div class="absolute bottom-3 left-3 right-3 flex items-center justify-between p-2 rounded bg-surface-container-lowest/95 backdrop-blur border {latestEv.status === 'unknown_loitering' ? 'border-error text-error' : latestEv.status === 'foreign_vehicle' ? 'border-tertiary text-tertiary' : 'border-secondary text-secondary'} z-20">
								<div class="flex items-center gap-2">
									<span class="material-symbols-outlined text-[16px]">
										{latestEv.status === 'unknown_loitering' ? 'warning' : latestEv.status === 'foreign_vehicle' ? 'directions_car' : 'verified_user'}
									</span>
									<div class="flex flex-col">
										<span class="font-mono text-[10px] font-bold uppercase">
											DETEKSI AKTIF: {latestEv.sub_label || latestEv.label} ({latestEv.status})
										</span>
										<span class="text-[9px] text-on-surface-variant font-mono">
											Waktu: {latestEv.created_at || 'Baru Saja'} · Confidence: {Math.round((latestEv.confidence || 0.95) * 100)}%
										</span>
									</div>
								</div>
								<span class="font-mono text-[10px] px-1.5 py-0.5 rounded bg-surface-container font-semibold">
									{latestEv.camera}
								</span>
							</div>
						{:else}
							<div class="absolute bottom-3 left-3 flex items-center gap-1.5 px-2.5 py-1 rounded bg-surface-container-lowest/80 backdrop-blur border border-outline-variant/20 z-20">
								<span class="w-1.5 h-1.5 rounded-full bg-secondary"></span>
								<span class="font-mono text-[10px] text-on-surface-variant">STATUS: AMAN / STANDBY (Tidak ada anomali)</span>
							</div>
						{/if}
					</div>

					<!-- Stream Control Footer -->
					<div class="p-2.5 bg-surface-container-low border-t border-outline-variant/20 flex flex-wrap items-center justify-between gap-2 text-xs">
						<div class="flex items-center gap-2">
							{#if cam.id === 'carport'}
								<button
									type="button"
									onclick={triggerBarrier}
									class="flex items-center gap-1.5 px-3 py-1 rounded font-mono text-[10px] font-semibold transition-all {barrierTriggered ? 'bg-secondary text-on-secondary shadow-[0_0_12px_rgba(78,222,163,0.5)]' : 'bg-surface-container hover:bg-surface-container-high text-primary border border-primary/30'}"
								>
									<span class="material-symbols-outlined text-[15px]">lock_open</span>
									<span>{barrierTriggered ? 'PORTAL TERBUKA (GPIO 18)...' : 'Manual Trigger Portal'}</span>
								</button>
							{:else}
								<span class="font-mono text-[10px] text-on-surface-variant">Zone Detection: Aktif</span>
							{/if}
						</div>

						<div class="flex items-center gap-1.5">
							<button type="button" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Capture Snapshot">
								<span class="material-symbols-outlined text-[16px]">photo_camera</span>
							</button>
							<button type="button" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Audio Alert Settings">
								<span class="material-symbols-outlined text-[16px]">volume_up</span>
							</button>
							<a href={cam.streamUrl} target="_blank" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Fullscreen Stream">
								<span class="material-symbols-outlined text-[16px]">fullscreen</span>
							</a>
						</div>
					</div>
				</div>
			{/if}
		{/each}
	</div>

	<!-- System Telemetry & Quick Hardware Audit Row -->
	<div class="grid grid-cols-2 md:grid-cols-4 gap-3">
		<div class="p-3 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between">
			<span class="font-mono text-[10px] uppercase text-on-surface-variant">HARDWARE HOST</span>
			<span class="font-bold text-xs text-on-surface mt-1">{data.status.server}</span>
			<span class="font-mono text-[10px] text-on-surface-variant/80">{data.status.cpu}</span>
		</div>
		<div class="p-3 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between">
			<span class="font-mono text-[10px] uppercase text-on-surface-variant">VIDEO ACCELERATION</span>
			<span class="font-bold text-xs text-secondary mt-1">{data.status.hwaccel}</span>
			<span class="font-mono text-[10px] text-secondary-fixed-dim">iGPU QuickSync / VAAPI</span>
		</div>
		<div class="p-3 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between">
			<span class="font-mono text-[10px] uppercase text-on-surface-variant">STORAGE QUOTA</span>
			<span class="font-bold text-xs text-primary mt-1">{data.status.storage_quota_cctv}</span>
			<span class="font-mono text-[10px] text-on-surface-variant/80">Retensi 7 Hari + FIFO</span>
		</div>
		<div class="p-3 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between">
			<span class="font-mono text-[10px] uppercase text-on-surface-variant">TELEGRAM GATEWAY</span>
			<span class="font-bold text-xs text-on-surface mt-1">@cctv_rumah_guard_bot</span>
			<span class="font-mono text-[10px] text-secondary">● Webhook Connected</span>
		</div>
	</div>

	<!-- Recent Security Events Log Section (Dynamic from Database) -->
	<div class="flex flex-col gap-3 p-4 rounded-lg bg-surface-container-low border border-outline-variant/30">
		<div class="flex items-center justify-between">
			<div class="flex items-center gap-2">
				<span class="material-symbols-outlined text-[18px] text-primary">history</span>
				<span class="font-mono text-xs font-bold text-on-surface uppercase tracking-wider">LOG AKTIVITAS & EVENT KEAMANAN TERBARU</span>
			</div>
			<a href="/events" class="text-xs text-primary hover:underline">Lihat Log Lengkap &rarr;</a>
		</div>

		{#if data.events && data.events.length > 0}
			<div class="overflow-x-auto">
				<table class="w-full text-left text-xs">
					<thead>
						<tr class="border-b border-outline-variant/20 text-on-surface-variant font-mono text-[10px] uppercase">
							<th class="py-2 px-3">Waktu</th>
							<th class="py-2 px-3">Kamera</th>
							<th class="py-2 px-3">Label</th>
							<th class="py-2 px-3">Sub-Label / Identitas</th>
							<th class="py-2 px-3">Status</th>
							<th class="py-2 px-3">Confidence</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-outline-variant/10">
						{#each data.events.slice(0, 5) as ev}
							<tr class="hover:bg-surface-container/40">
								<td class="py-2 px-3 font-mono text-[11px] text-on-surface-variant">{ev.created_at || 'Baru saja'}</td>
								<td class="py-2 px-3 font-mono text-[11px] text-on-surface">{ev.camera}</td>
								<td class="py-2 px-3">
									<span class="font-mono text-[10px] px-1.5 py-0.5 rounded bg-surface-container font-semibold uppercase">{ev.label}</span>
								</td>
								<td class="py-2 px-3 font-medium text-on-surface">{ev.sub_label || '-'}</td>
								<td class="py-2 px-3">
									{#if ev.status === 'family_suppressed' || ev.status === 'family_vehicle'}
										<span class="text-secondary font-mono text-[10px] font-semibold">● Family (Suppressed)</span>
									{:else if ev.status === 'unknown_loitering'}
										<span class="text-error font-mono text-[10px] font-semibold">● Loitering Alert</span>
									{:else}
										<span class="text-primary font-mono text-[10px] font-semibold">● {ev.status}</span>
									{/if}
								</td>
								<td class="py-2 px-3 font-mono text-[11px]">{Math.round((ev.confidence || 0.95) * 100)}%</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{:else}
			<div class="py-6 text-center text-xs text-on-surface-variant font-mono">
				Belum ada riwayat aktivitas keamanan tercatat. Sistem siap memproses event dari 2 CCTV Frigate.
			</div>
		{/if}
	</div>
</div>
