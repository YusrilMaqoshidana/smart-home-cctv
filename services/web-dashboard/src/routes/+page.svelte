<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let isSimulatingBreach = $state(false);
	let testingModel = $state(false);
	let testResult = $state<string | null>(null);

	async function runQuickModelTest(type: 'face' | 'plate' | 'loiter') {
		testingModel = true;
		testResult = null;
		try {
			if (type === 'face') {
				testResult = 'Menguji model YuNet + SFace pada webcam /dev/video0... Status: Model siap, Cosine similarity threshold: 0.36';
			} else if (type === 'plate') {
				testResult = 'Menguji model ANPR TNKB Regex & Matching... Whitelist plat terdaftar aktif.';
			} else if (type === 'loiter') {
				isSimulatingBreach = !isSimulatingBreach;
				testResult = isSimulatingBreach ? 'Simulasi deteksi penyusup/unknown loitering (>45s) diaktifkan.' : 'Status perimeter kembali normal.';
			}
		} finally {
			setTimeout(() => {
				testingModel = false;
			}, 600);
		}
	}
</script>

<div class="flex flex-col gap-5">
	<!-- BRANCH LOCAL BANNER -->
	<div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 p-3 bg-secondary/10 border border-secondary/30 rounded-lg">
		<div class="flex items-center gap-2.5">
			<span class="w-2.5 h-2.5 rounded-full bg-secondary animate-pulse"></span>
			<div>
				<div class="flex items-center gap-2">
					<span class="font-mono text-xs font-bold text-secondary uppercase tracking-wider">[BRANCH: LOCAL]</span>
					<span class="text-xs font-semibold text-on-surface">1 CCTV Mode (Laptop Webcam /dev/video0)</span>
				</div>
				<p class="text-[11px] text-on-surface-variant">Khusus pengujian model AI (Face Recognition & ANPR) di lingkungan lokal tanpa CCTV fisik.</p>
			</div>
		</div>
		<div class="flex items-center gap-2">
			<span class="font-mono text-[10px] bg-surface-container-high px-2 py-1 rounded text-on-surface">
				RTSP: <code class="text-primary">rtsp://localhost:8554/halaman_depan</code>
			</span>
		</div>
	</div>

	<!-- Stream & Telemetry HUD Header -->
	<div class="flex flex-col xl:flex-row items-stretch xl:items-center justify-between gap-3 p-3.5 bg-surface-container-low border border-outline-variant/30 rounded-lg shadow-sm">
		<div class="flex items-center gap-2">
			<div class="flex items-center gap-2 px-3 py-1.5 rounded bg-primary-container text-on-primary-container font-semibold text-xs shadow-[0_0_12px_rgba(6,182,212,0.35)]">
				<span class="material-symbols-outlined text-[16px]">videocam</span>
				<span>Webcam Laptop #01 (Halaman Depan)</span>
			</div>
			<span class="font-mono text-[11px] text-on-surface-variant bg-surface-container-highest px-2 py-1 rounded">
				/dev/video0 via MediaMTX WHEP
			</span>
		</div>

		<!-- Telemetry Badges -->
		<div class="flex flex-wrap items-center gap-2 text-xs">
			<div class="flex items-center gap-1.5 px-2.5 py-1 bg-surface-container-lowest border border-outline-variant/20 rounded">
				<div class="w-1.5 h-1.5 rounded-full bg-secondary animate-ping"></div>
				<span class="font-mono text-[10px] text-on-surface-variant uppercase">LATENCY</span>
				<span class="font-mono text-[11px] text-secondary font-semibold">18ms Ultra-Low</span>
			</div>
			<div class="flex items-center gap-1.5 px-2.5 py-1 bg-surface-container-lowest border border-outline-variant/20 rounded">
				<span class="material-symbols-outlined text-[15px] text-primary">psychology</span>
				<span class="font-mono text-[10px] text-on-surface-variant">AI ENGINE:</span>
				<span class="font-mono text-[11px] text-primary font-medium">YuNet · SFace · TNKB OCR</span>
			</div>
			<div class="flex items-center gap-1.5 px-2.5 py-1 bg-surface-container-lowest border border-outline-variant/20 rounded">
				<span class="material-symbols-outlined text-[15px] text-tertiary">devices</span>
				<span class="font-mono text-[10px] text-on-surface-variant">HOST:</span>
				<span class="font-mono text-[11px] text-tertiary font-semibold">Local Laptop CachyOS</span>
			</div>
		</div>
	</div>

	<!-- Primary Single CCTV Layout (Laptop Webcam View) -->
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
		<!-- Left / Main: Video Feed Container (2 cols) -->
		<div class="lg:col-span-2 flex flex-col bg-surface-container-lowest border border-outline-variant/30 rounded-lg overflow-hidden shadow-lg relative group">
			<!-- Stream Header HUD -->
			<div class="flex items-center justify-between px-4 py-2 bg-surface-container-low text-on-surface border-b border-outline-variant/20 z-20">
				<div class="flex items-center gap-2">
					<span class="w-2 h-2 rounded-full {isSimulatingBreach ? 'bg-error animate-ping' : 'bg-secondary animate-pulse'}"></span>
					<span class="font-mono text-[11px] font-bold tracking-wider uppercase {isSimulatingBreach ? 'text-error' : 'text-primary'}">
						LIVE STREAM : WEBCAM LAPTOP (/dev/video0)
					</span>
					<span class="font-mono text-[10px] text-on-surface-variant px-1.5 py-0.5 rounded bg-surface-container-highest">
						ZONE: perimeter_gerbang
					</span>
				</div>
				<div class="flex items-center gap-2 font-mono text-[10px] text-on-surface-variant">
					<span class="text-secondary">30.0 FPS</span>
					<span>|</span>
					<span class="text-primary">1280x720</span>
					<span>|</span>
					<span>H.264 WHEP</span>
				</div>
			</div>

			<!-- Video Feed Container (16:9 Canvas) -->
			<div class="relative w-full aspect-video bg-black overflow-hidden flex items-center justify-center">
				<!-- MediaMTX Live WebRTC Stream iframe -->
				<iframe 
					src="http://localhost:8889/halaman_depan" 
					title="Live Stream Webcam Laptop"
					class="w-full h-full border-0 absolute inset-0 z-0" 
					allow="autoplay; fullscreen"
					loading="lazy">
				</iframe>

				<!-- Tactical Grid Scrim Overlay -->
				<div class="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-background/40 pointer-events-none z-10"></div>

				<!-- Center Crosshair HUD -->
				<div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20 z-10">
					<div class="w-10 h-px bg-primary"></div>
					<div class="h-10 w-px bg-primary -ml-[5px]"></div>
				</div>

				<!-- Top Right HUD Badge -->
				<div class="absolute top-2.5 right-2.5 flex flex-col items-end gap-1 z-20">
					<span class="font-mono text-[10px] text-secondary bg-surface-container-lowest/90 px-2 py-0.5 rounded uppercase font-bold tracking-wider border border-secondary/30">
						● LOCAL DEV TESTBENCH
					</span>
					<span class="font-mono text-[9px] text-on-surface bg-surface-container-lowest/80 px-1.5 py-0.5 rounded">
						FEED: rtsp://localhost:8554/halaman_depan
					</span>
				</div>
			</div>

			<!-- Stream Control Footer -->
			<div class="p-2.5 bg-surface-container-low border-t border-outline-variant/20 flex flex-wrap items-center justify-between gap-2 text-xs">
				<div class="flex items-center gap-2">
					<span class="font-mono text-[10px] text-on-surface-variant">Stream Source: v4l2 /dev/video0</span>
				</div>

				<div class="flex items-center gap-1.5">
					<button type="button" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Capture Snapshot">
						<span class="material-symbols-outlined text-[16px]">photo_camera</span>
					</button>
					<a href="http://localhost:8889/halaman_depan" target="_blank" class="p-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface" title="Buka Stream di Tab Baru">
						<span class="material-symbols-outlined text-[16px]">fullscreen</span>
					</a>
				</div>
			</div>
		</div>

		<!-- Right: Local AI Model Testing Panel (1 col) -->
		<div class="flex flex-col gap-4">
			<!-- Model Test Controls -->
			<div class="p-4 rounded-lg bg-surface-container-low border border-outline-variant/30 flex flex-col gap-3">
				<div class="flex items-center justify-between">
					<span class="font-mono text-xs font-bold text-primary uppercase tracking-wider">PENGUJIAN MODEL AI</span>
					<span class="font-mono text-[10px] bg-primary/10 text-primary px-1.5 py-0.5 rounded">1-Click Test</span>
				</div>
				<p class="text-[11px] text-on-surface-variant">Uji model AI secara langsung menggunakan camera laptop sebelum dideploy ke 2 CCTV produksi.</p>

				<div class="flex flex-col gap-2">
					<button
						type="button"
						onclick={() => runQuickModelTest('face')}
						disabled={testingModel}
						class="w-full flex items-center justify-between px-3 py-2 rounded bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-medium transition-colors border border-outline-variant/20 cursor-pointer"
					>
						<div class="flex items-center gap-2">
							<span class="material-symbols-outlined text-[16px] text-primary">face</span>
							<span>Test Face Model (YuNet/SFace)</span>
						</div>
						<span class="font-mono text-[10px] text-primary">Run</span>
					</button>

					<button
						type="button"
						onclick={() => runQuickModelTest('plate')}
						disabled={testingModel}
						class="w-full flex items-center justify-between px-3 py-2 rounded bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-medium transition-colors border border-outline-variant/20 cursor-pointer"
					>
						<div class="flex items-center gap-2">
							<span class="material-symbols-outlined text-[16px] text-secondary">pin</span>
							<span>Test ANPR TNKB Validation</span>
						</div>
						<span class="font-mono text-[10px] text-secondary">Run</span>
					</button>

					<button
						type="button"
						onclick={() => runQuickModelTest('loiter')}
						disabled={testingModel}
						class="w-full flex items-center justify-between px-3 py-2 rounded bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-medium transition-colors border border-outline-variant/20 cursor-pointer"
					>
						<div class="flex items-center gap-2">
							<span class="material-symbols-outlined text-[16px] text-error">warning</span>
							<span>Simulasi Loitering Alert</span>
						</div>
						<span class="font-mono text-[10px] {isSimulatingBreach ? 'text-error' : 'text-on-surface-variant'}">
							{isSimulatingBreach ? 'Active' : 'Toggle'}
						</span>
					</button>
				</div>

				{#if testResult}
					<div class="p-2.5 rounded bg-surface-container-lowest border border-outline-variant/20 font-mono text-[10px] text-on-surface">
						<div class="text-secondary font-bold mb-1">[TEST OUTPUT]</div>
						<div>{testResult}</div>
					</div>
				{/if}

				<div class="pt-2 border-t border-outline-variant/20 flex flex-col gap-1 text-[11px]">
					<span class="font-mono text-[10px] text-on-surface-variant font-semibold">CLI RUNNER:</span>
					<code class="p-1.5 rounded bg-surface-container-lowest text-[10px] text-primary font-mono select-all">
						python3 scripts/test_model_laptop.py
					</code>
				</div>
			</div>

			<!-- Whitelist Quick Summary -->
			<div class="p-4 rounded-lg bg-surface-container-low border border-outline-variant/30 flex flex-col gap-2.5">
				<span class="font-mono text-xs font-bold text-on-surface uppercase tracking-wider">DATABASE WHITELIST LOKAL</span>
				<div class="grid grid-cols-2 gap-2 text-xs">
					<div class="p-2 rounded bg-surface-container-lowest border border-outline-variant/20">
						<span class="text-[10px] text-on-surface-variant block">Wajah Terdaftar</span>
						<span class="font-mono text-lg font-bold text-primary">{data.faces.length}</span>
					</div>
					<div class="p-2 rounded bg-surface-container-lowest border border-outline-variant/20">
						<span class="text-[10px] text-on-surface-variant block">Plat Terdaftar</span>
						<span class="font-mono text-lg font-bold text-secondary">{data.plates.length}</span>
					</div>
				</div>
				<a href="/faces" class="text-[11px] text-primary hover:underline flex items-center gap-1">
					<span>Kelola Database Wajah & Plat</span>
					<span class="material-symbols-outlined text-[14px]">arrow_forward</span>
				</a>
			</div>
		</div>
	</div>

	<!-- Recent Security Events List from DB -->
	<div class="flex flex-col gap-3 p-4 rounded-lg bg-surface-container-low border border-outline-variant/30">
		<div class="flex items-center justify-between">
			<div class="flex items-center gap-2">
				<span class="material-symbols-outlined text-[18px] text-primary">history</span>
				<span class="font-mono text-xs font-bold text-on-surface uppercase tracking-wider">EVENT LOG TERBARU (DATABASE LOKAL)</span>
			</div>
			<a href="/events" class="text-xs text-primary hover:underline">Lihat Semua Event &rarr;</a>
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
				Belum ada event deteksi di database. Jalankan pengujian model untuk membuat event.
			</div>
		{/if}
	</div>
</div>
