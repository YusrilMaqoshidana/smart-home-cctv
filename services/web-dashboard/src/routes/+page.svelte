<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let activePreset = $state<'all' | 'depan' | 'carport'>('all');
	let isSimulatingBreach = $state(false);
	let barrierTriggered = $state(false);

	function triggerBarrier() {
		barrierTriggered = true;
		setTimeout(() => {
			barrierTriggered = false;
		}, 3000);
	}
</script>

<div class="flex flex-col gap-5">
	<!-- Stream Routing & Engine Matrix Header -->
	<div class="flex flex-col xl:flex-row items-stretch xl:items-center justify-between gap-3 p-3.5 bg-surface-container-low border border-outline-variant/30 rounded-lg shadow-sm">
		<!-- Camera Preset Selectors -->
		<div class="flex flex-wrap items-center gap-2">
			<button
				type="button"
				onclick={() => activePreset = 'all'}
				class="flex items-center gap-2 px-3 py-1.5 rounded transition-all text-xs {activePreset === 'all' ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.35)]' : 'bg-surface-container text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high'}"
			>
				<span class="material-symbols-outlined text-[16px]">grid_view</span>
				<span>Multi-Grid 2x2 View</span>
			</button>
			<button
				type="button"
				onclick={() => activePreset = 'depan'}
				class="flex items-center gap-2 px-3 py-1.5 rounded transition-all text-xs {activePreset === 'depan' ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.35)]' : 'bg-surface-container text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high'}"
			>
				<span class="material-symbols-outlined text-[16px]">videocam</span>
				<span>Halaman Depan</span>
				<span class="font-mono text-[10px] bg-surface-container-lowest/80 text-primary px-1.5 py-0.5 rounded ml-1">rtsp://8554/depan</span>
			</button>
			<button
				type="button"
				onclick={() => activePreset = 'carport'}
				class="flex items-center gap-2 px-3 py-1.5 rounded transition-all text-xs {activePreset === 'carport' ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.35)]' : 'bg-surface-container text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high'}"
			>
				<span class="material-symbols-outlined text-[16px]">sensors</span>
				<span>Carport & Gate</span>
				<span class="font-mono text-[10px] bg-surface-container-lowest text-secondary px-1.5 py-0.5 rounded ml-1">WHEP 1080p</span>
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
				<span class="font-mono text-[11px] text-tertiary font-semibold">M70q UHD 630 VAAPI</span>
			</div>
		</div>
	</div>

	<!-- Primary Dual Surveillance Matrix Grid -->
	<div class="grid grid-cols-1 {activePreset === 'all' ? 'lg:grid-cols-2' : 'grid-cols-1'} gap-5">
		<!-- FEED 01: Halaman Depan -->
		{#if activePreset === 'all' || activePreset === 'depan'}
			<div class="flex flex-col bg-surface-container-lowest border border-outline-variant/30 rounded-lg overflow-hidden shadow-lg relative group">
				<!-- Stream Header HUD -->
				<div class="flex items-center justify-between px-4 py-2 bg-surface-container-low text-on-surface border-b border-outline-variant/20 z-20">
					<div class="flex items-center gap-2">
						<span class="w-2 h-2 rounded-full {isSimulatingBreach ? 'bg-error animate-ping' : 'bg-secondary animate-pulse'}"></span>
						<span class="font-mono text-[11px] font-bold tracking-wider uppercase {isSimulatingBreach ? 'text-error' : 'text-primary'}">
							FEED #01 : HALAMAN DEPAN & GERBANG
						</span>
						<span class="font-mono text-[10px] text-on-surface-variant px-1.5 py-0.5 rounded bg-surface-container-highest">
							ZONE: perimeter_gerbang
						</span>
					</div>
					<div class="flex items-center gap-2 font-mono text-[10px] text-on-surface-variant">
						<span class="text-secondary">29.8 FPS</span>
						<span>|</span>
						<span class="text-primary">4.2 Mbps</span>
						<span>|</span>
						<span>H.265 VAAPI</span>
					</div>
				</div>

				<!-- Video Feed Container (16:9 Canvas) -->
				<div class="relative w-full aspect-video bg-black overflow-hidden flex items-center justify-center">
					<!-- go2rtc Live WebRTC / MP4 Stream iframe -->
					<iframe 
						src="http://localhost:8889/halaman_depan" 
						title="Live Stream Halaman Depan"
						class="w-full h-full border-0 absolute inset-0 z-0" 
						allow="autoplay; fullscreen"
						loading="lazy">
					</iframe>

					<!-- Tactical Grid Scrim Overlay -->
					<div class="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-background/40 pointer-events-none z-10"></div>

					<!-- Crosshair HUD Center Marker -->
					<div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20 z-10">
						<div class="w-10 h-px bg-primary"></div>
						<div class="h-10 w-px bg-primary -ml-[5px]"></div>
					</div>

					<!-- Top Right Stream HUD Overlays -->
					<div class="absolute top-2.5 right-2.5 flex flex-col items-end gap-1 z-20">
						<span class="font-mono text-[10px] text-error bg-error-container/90 px-2 py-0.5 rounded uppercase font-bold tracking-wider border border-error/30">
							● REC [BURST BUFFER]
						</span>
						<span class="font-mono text-[9px] text-on-surface bg-surface-container-lowest/80 px-1.5 py-0.5 rounded">
							BUFFER: 14.8 MB / RING
						</span>
					</div>

					<!-- Perimeter Zone Boundary SVG Trace -->
					<svg class="absolute inset-0 w-full h-full pointer-events-none z-10" preserveAspectRatio="none" viewBox="0 0 100 100">
						<polygon class="{isSimulatingBreach ? 'fill-error/15 stroke-error stroke-[0.5] stroke-dasharray-[2,1] animate-pulse' : 'fill-primary/5 stroke-primary/40 stroke-[0.3]'}" points="12,35 68,32 78,88 8,92"></polygon>
						<text class="{isSimulatingBreach ? 'fill-error font-bold' : 'fill-primary/80'} font-mono text-[3px] tracking-wider uppercase" x="14" y="38">
							ZONE: PERIMETER_GERBANG {isSimulatingBreach ? '(ALERT: LOITERING DETECTED)' : '(SECURE)'}
						</text>
					</svg>

					<!-- Dynamic AI ML Detection Bounding Box -->
					{#if isSimulatingBreach}
						<!-- Alert: Unknown Person Loitering -->
						<div class="absolute top-[28%] left-[34%] w-[22%] h-[48%] pointer-events-auto flex flex-col justify-between p-1 border border-error bg-error/10 shadow-[0_0_15px_rgba(239,68,68,0.45)] z-20 transition-all">
							<div class="flex justify-between items-start">
								<span class="w-2 h-2 border-t-2 border-l-2 border-error"></span>
								<span class="w-2 h-2 border-t-2 border-r-2 border-error"></span>
							</div>
							<div class="bg-surface-container-lowest/95 p-1 rounded backdrop-blur flex flex-col gap-0.5 border border-error/40">
								<div class="flex items-center justify-between gap-1">
									<span class="font-mono text-[9px] font-bold text-error uppercase">person: UNKNOWN [94.4%]</span>
									<span class="w-1.5 h-1.5 rounded-full bg-error animate-ping"></span>
								</div>
								<span class="font-mono text-[8px] text-tertiary">Vector: No Match (ArcFace &lt;0.31)</span>
								<span class="font-mono text-[8px] text-error font-semibold">Loitering: 14s &gt; 10s Alert Threshold</span>
							</div>
							<div class="flex justify-between items-end">
								<span class="w-2 h-2 border-b-2 border-l-2 border-error"></span>
								<span class="w-2 h-2 border-b-2 border-r-2 border-error"></span>
							</div>
						</div>
					{:else}
						<!-- Normal: Family Member Detected -->
						<div class="absolute top-[28%] left-[34%] w-[22%] h-[48%] pointer-events-auto flex flex-col justify-between p-1 border border-secondary/60 bg-secondary/5 shadow-[0_0_15px_rgba(78,222,163,0.3)] z-20 transition-all">
							<div class="flex justify-between items-start">
								<span class="w-2 h-2 border-t-2 border-l-2 border-secondary"></span>
								<span class="w-2 h-2 border-t-2 border-r-2 border-secondary"></span>
							</div>
							<div class="bg-surface-container-lowest/95 p-1 rounded backdrop-blur flex flex-col gap-0.5 border border-secondary/40">
								<div class="flex items-center justify-between gap-1">
									<span class="font-mono text-[9px] font-bold text-secondary uppercase">person: AYAH [99.8%]</span>
									<span class="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
								</div>
								<span class="font-mono text-[8px] text-secondary-fixed-dim">ArcFace Cosine: 0.9982 (Whitelisted)</span>
								<span class="font-mono text-[8px] text-on-surface-variant">Siren: Auto-Suppressed (Family)</span>
							</div>
							<div class="flex justify-between items-end">
								<span class="w-2 h-2 border-b-2 border-l-2 border-secondary"></span>
								<span class="w-2 h-2 border-b-2 border-r-2 border-secondary"></span>
							</div>
						</div>
					{/if}
				</div>

				<!-- Stream Control Footer -->
				<div class="p-2.5 bg-surface-container-low border-t border-outline-variant/20 flex flex-wrap items-center justify-between gap-2 text-xs">
					<div class="flex items-center gap-2">
						<button
							type="button"
							onclick={() => isSimulatingBreach = !isSimulatingBreach}
							class="flex items-center gap-1.5 px-2.5 py-1 rounded font-mono text-[10px] font-semibold transition-colors {isSimulatingBreach ? 'bg-secondary/20 text-secondary border border-secondary/40' : 'bg-error-container/40 text-error border border-error/30'}"
						>
							<span class="material-symbols-outlined text-[14px]">warning</span>
							<span>{isSimulatingBreach ? 'Reset ke Status Normal' : 'Simulasi Loitering Alert'}</span>
						</button>
						<span class="font-mono text-[10px] text-on-surface-variant">PTZ: Depan Pagar</span>
					</div>

					<div class="flex items-center gap-1.5">
						<button type="button" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Capture Snapshot">
							<span class="material-symbols-outlined text-[16px]">photo_camera</span>
						</button>
						<button type="button" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Mute Audio Alert">
							<span class="material-symbols-outlined text-[16px]">volume_up</span>
						</button>
						<a href="http://localhost:8889/halaman_depan" target="_blank" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Fullscreen Stream">
							<span class="material-symbols-outlined text-[16px]">fullscreen</span>
						</a>
					</div>
				</div>
			</div>
		{/if}

		<!-- FEED 02: Carport & Pintu Garasi (ALPR Cam) -->
		{#if activePreset === 'all' || activePreset === 'carport'}
			<div class="flex flex-col bg-surface-container-lowest border border-outline-variant/30 rounded-lg overflow-hidden shadow-lg relative group">
				<!-- Stream Header HUD -->
				<div class="flex items-center justify-between px-4 py-2 bg-surface-container-low text-on-surface border-b border-outline-variant/20 z-20">
					<div class="flex items-center gap-2">
						<span class="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
						<span class="font-mono text-[11px] font-bold tracking-wider uppercase text-secondary">
							FEED #02 : CARPORT & BARRIER GATE
						</span>
						<span class="font-mono text-[10px] text-on-surface-variant px-1.5 py-0.5 rounded bg-surface-container-highest">
							ZONE: carport_barrier
						</span>
					</div>
					<div class="flex items-center gap-2 font-mono text-[10px] text-on-surface-variant">
						<span class="text-secondary">24.0 FPS</span>
						<span>|</span>
						<span class="text-primary">3.8 Mbps</span>
						<span>|</span>
						<span>ALPR OCR</span>
					</div>
				</div>

				<!-- Video Feed Container -->
				<div class="relative w-full aspect-video bg-black overflow-hidden flex items-center justify-center">
					<iframe 
						src="http://localhost:8889/carport" 
						title="Live Stream Carport"
						class="w-full h-full border-0 absolute inset-0 z-0" 
						allow="autoplay; fullscreen"
						loading="lazy">
					</iframe>

					<!-- Tactical Grid Scrim Overlay -->
					<div class="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-background/40 pointer-events-none z-10"></div>

					<!-- Top Right Stream HUD Overlays -->
					<div class="absolute top-2.5 right-2.5 flex flex-col items-end gap-1 z-20">
						<span class="font-mono text-[10px] text-secondary bg-surface-container-lowest/90 px-2 py-0.5 rounded uppercase font-bold tracking-wider border border-secondary/30">
							● ALPR SENSING
						</span>
						<span class="font-mono text-[9px] text-on-surface bg-surface-container-lowest/80 px-1.5 py-0.5 rounded">
							TRIGGER: BARRIER AUTO-OPEN
						</span>
					</div>

					<!-- Vehicle Plate Bounding Box HUD Overlay -->
					<div class="absolute bottom-[20%] left-[25%] w-[42%] h-[32%] pointer-events-auto flex flex-col justify-between p-1 border border-secondary/70 bg-secondary/5 shadow-[0_0_15px_rgba(78,222,163,0.3)] z-20">
						<div class="flex justify-between items-start">
							<span class="w-2 h-2 border-t-2 border-l-2 border-secondary"></span>
							<span class="w-2 h-2 border-t-2 border-r-2 border-secondary"></span>
						</div>
						<div class="bg-surface-container-lowest/95 p-1.5 rounded backdrop-blur flex flex-col gap-0.5 border border-secondary/40">
							<div class="flex items-center justify-between gap-1">
								<span class="font-mono text-[11px] font-bold text-secondary uppercase tracking-wider">PLAT: B 1234 XYZ</span>
								<span class="font-mono text-[9px] bg-secondary/20 text-secondary px-1 py-0.2 rounded font-bold">MATCH 98.1%</span>
							</div>
							<span class="font-mono text-[9px] text-on-surface">Avanza Hitam Ayah (Mobil Keluarga)</span>
							<span class="font-mono text-[8px] text-secondary">Aksi: Buka Portal Barrier Otomatis (GPIO Pin 18)</span>
						</div>
						<div class="flex justify-between items-end">
							<span class="w-2 h-2 border-b-2 border-l-2 border-secondary"></span>
							<span class="w-2 h-2 border-b-2 border-r-2 border-secondary"></span>
						</div>
					</div>
				</div>

				<!-- Stream Control Footer -->
				<div class="p-2.5 bg-surface-container-low border-t border-outline-variant/20 flex flex-wrap items-center justify-between gap-2 text-xs">
					<div class="flex items-center gap-2">
						<button
							type="button"
							onclick={triggerBarrier}
							class="flex items-center gap-1.5 px-3 py-1 rounded font-mono text-[10px] font-semibold transition-all {barrierTriggered ? 'bg-secondary text-on-secondary shadow-[0_0_12px_rgba(78,222,163,0.5)]' : 'bg-surface-container hover:bg-surface-container-high text-primary border border-primary/30'}"
						>
							<span class="material-symbols-outlined text-[15px]">lock_open</span>
							<span>{barrierTriggered ? 'BARRIER OPENING (GPIO 18)...' : 'Manual Trigger Portal (Buka)'}</span>
						</button>
						<span class="font-mono text-[10px] text-on-surface-variant">Gate Status: Normal</span>
					</div>

					<div class="flex items-center gap-1.5">
						<button type="button" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Capture Snapshot">
							<span class="material-symbols-outlined text-[16px]">photo_camera</span>
						</button>
						<a href="http://localhost:8889/carport" target="_blank" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Fullscreen Stream">
							<span class="material-symbols-outlined text-[16px]">fullscreen</span>
						</a>
					</div>
				</div>
			</div>
		{/if}
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
</div>
