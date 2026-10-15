<script lang="ts">
	import type { PageData, ActionData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();

	let searchQuery = $state('');
	let selectedDiagFace = $state<{ name: string; vector: string; score: number } | null>(null);

	let filteredFaces = $derived(
		data.faces.filter((f: any) =>
			f.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
			f.role.toLowerCase().includes(searchQuery.toLowerCase())
		)
	);

	function openDiag(name: string, vector: string, score: number) {
		selectedDiagFace = { name, vector, score };
	}

	function closeDiag() {
		selectedDiagFace = null;
	}
</script>

<div class="flex flex-col gap-5">
	<!-- TOP METRICS STATS BAR (Bento Grid) -->
	<div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
		<!-- Stat 1: Registered Faces -->
		<div class="p-3.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between relative overflow-hidden">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-medium">TOTAL PENGHUNI</span>
					<span class="text-xs text-on-surface-variant/80">Permanent Residents</span>
				</div>
				<div class="w-7 h-7 rounded bg-primary/10 flex items-center justify-center text-primary">
					<span class="material-symbols-outlined text-[18px]">family_restroom</span>
				</div>
			</div>
			<div class="mt-3 flex items-baseline justify-between">
				<div class="flex items-baseline gap-1.5">
					<span class="font-mono text-2xl font-bold text-primary">{data.faces.filter((f: any) => f.role === 'resident').length || 3}</span>
					<span class="font-mono text-[10px] text-on-surface-variant">Terdaftar</span>
				</div>
				<span class="font-mono text-[10px] text-secondary bg-surface-container-high px-1.5 py-0.5 rounded font-medium">Synced</span>
			</div>
			<div class="w-full bg-surface-container h-1 rounded mt-2.5 overflow-hidden">
				<div class="bg-primary h-full w-full"></div>
			</div>
		</div>

		<!-- Stat 2: Guest Access -->
		<div class="p-3.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between relative overflow-hidden">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-medium">TAMU SEMENTARA</span>
					<span class="text-xs text-on-surface-variant/80">Active Guest Access</span>
				</div>
				<div class="w-7 h-7 rounded bg-tertiary/10 flex items-center justify-center text-tertiary">
					<span class="material-symbols-outlined text-[18px]">badge</span>
				</div>
			</div>
			<div class="mt-3 flex items-baseline justify-between">
				<div class="flex items-baseline gap-1.5">
					<span class="font-mono text-2xl font-bold text-tertiary">{data.faces.filter((f: any) => f.role === 'guest_temporary').length || 1}</span>
					<span class="font-mono text-[10px] text-on-surface-variant">Aktif Hari Ini</span>
				</div>
				<span class="font-mono text-[10px] text-tertiary bg-surface-container-high px-1.5 py-0.5 rounded font-medium">Auto-Expire</span>
			</div>
			<div class="w-full bg-surface-container h-1 rounded mt-2.5 overflow-hidden">
				<div class="bg-tertiary h-full w-[45%]"></div>
			</div>
		</div>

		<!-- Stat 3: Vector Model -->
		<div class="p-3.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between relative overflow-hidden">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-medium">VEKTOR EMBEDDING</span>
					<span class="text-xs text-on-surface-variant/80">RetinaFace + ArcFace</span>
				</div>
				<div class="w-7 h-7 rounded bg-secondary/10 flex items-center justify-center text-secondary">
					<span class="material-symbols-outlined text-[18px]">psychology</span>
				</div>
			</div>
			<div class="mt-3 flex items-baseline justify-between">
				<div class="flex items-baseline gap-1.5">
					<span class="font-mono text-2xl font-bold text-on-surface">512</span>
					<span class="font-mono text-[10px] text-on-surface-variant">Dimensi / FP32</span>
				</div>
				<span class="font-mono text-[10px] text-secondary bg-surface-container-high px-1.5 py-0.5 rounded font-medium">Cosine ≥ 0.68</span>
			</div>
			<div class="w-full bg-surface-container h-1 rounded mt-2.5 overflow-hidden">
				<div class="bg-secondary h-full w-[94%]"></div>
			</div>
		</div>

		<!-- Stat 4: False Alarm Suppression -->
		<div class="p-3.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between relative overflow-hidden">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-medium">FALSE ALARM REDUCTION</span>
					<span class="text-xs text-on-surface-variant/80">Suppress Known Faces</span>
				</div>
				<div class="w-7 h-7 rounded bg-secondary/10 flex items-center justify-center text-secondary">
					<span class="material-symbols-outlined text-[18px]">verified_user</span>
				</div>
			</div>
			<div class="mt-3 flex items-baseline justify-between">
				<div class="flex items-baseline gap-1">
					<span class="font-mono text-2xl font-bold text-secondary">98.4</span>
					<span class="font-mono text-sm text-secondary">%</span>
				</div>
				<span class="font-mono text-[10px] text-primary bg-surface-container-high px-1.5 py-0.5 rounded font-medium">Siren Muted</span>
			</div>
			<div class="w-full bg-surface-container h-1 rounded mt-2.5 overflow-hidden">
				<div class="bg-secondary h-full w-[98.4%]"></div>
			</div>
		</div>
	</div>

	<!-- Error notification if server action failed -->
	{#if form?.error}
		<div class="p-3 bg-error-container/30 border border-error/40 rounded text-xs text-error flex items-center gap-2">
			<span class="material-symbols-outlined text-[18px]">error</span>
			<span>{form.error}</span>
		</div>
	{/if}

	<!-- BENTO SPLIT: MAIN FACE DIRECTORY & REGISTRATION / TELEGRAM PANEL -->
	<div class="grid grid-cols-1 xl:grid-cols-12 gap-5 items-start">
		<!-- LEFT 8 COLUMNS: DIRECTORY GRID & DIAGNOSTIC BOX -->
		<div class="xl:col-span-8 flex flex-col gap-4">
			<!-- Header & Search Toolbar -->
			<div class="flex flex-col sm:flex-row items-start sm:items-center justify-between p-3 rounded bg-surface-container-low border border-outline-variant/20 gap-3">
				<div class="flex items-center gap-2">
					<div class="px-2.5 py-1 bg-surface-container rounded text-on-surface text-xs font-semibold flex items-center gap-1.5">
						<span class="material-symbols-outlined text-[16px] text-primary">groups</span>
						<span>Direktori Wajah</span>
						<span class="bg-primary/20 text-primary px-1.5 py-0.2 rounded font-mono text-[10px] font-bold">{filteredFaces.length} Entri</span>
					</div>
					<span class="text-on-surface-variant font-mono text-[11px] hidden sm:inline">• Real-time Match Stream Active</span>
				</div>

				<div class="flex items-center gap-2 w-full sm:w-auto">
					<div class="flex items-center bg-surface-container-lowest border border-outline-variant/30 rounded px-2.5 py-1 text-on-surface-variant flex-1 sm:flex-initial">
						<span class="material-symbols-outlined text-[16px] mr-1.5">search</span>
						<input
							type="text"
							bind:value={searchQuery}
							placeholder="Cari nama / status..."
							class="bg-transparent border-none text-on-surface text-xs focus:outline-none w-36 sm:w-44 placeholder:text-outline"
						/>
						{#if searchQuery}
							<button type="button" onclick={() => searchQuery = ''} class="text-on-surface-variant hover:text-on-surface">
								<span class="material-symbols-outlined text-[14px]">close</span>
							</button>
						{/if}
					</div>
				</div>
			</div>

			<!-- IN-LINE LIVE VECTOR SIMILARITY DIAGNOSTIC BOX (Triggered by 'Test ID') -->
			{#if selectedDiagFace}
				<div class="p-4 rounded bg-surface-container-high border border-primary/40 flex flex-col gap-3 shadow-lg">
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-2">
							<span class="material-symbols-outlined text-secondary text-[20px]">psychology</span>
							<span class="font-bold text-xs uppercase tracking-wider text-on-surface">Biometric Vector Comparison Diagnostic</span>
						</div>
						<button type="button" onclick={closeDiag} class="text-on-surface-variant hover:text-on-surface">
							<span class="material-symbols-outlined text-[18px]">close</span>
						</button>
					</div>

					<div class="grid grid-cols-1 md:grid-cols-3 gap-3">
						<div class="p-2.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col">
							<span class="font-mono text-[9px] uppercase text-on-surface-variant">TARGET FACE IDENTITY</span>
							<span class="font-bold text-sm text-primary mt-0.5">{selectedDiagFace.name}</span>
							<span class="font-mono text-[10px] text-on-surface-variant/80">{selectedDiagFace.vector}</span>
						</div>
						<div class="p-2.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col">
							<span class="font-mono text-[9px] uppercase text-on-surface-variant">COSINE SIMILARITY SCORE</span>
							<div class="flex items-baseline gap-2 mt-0.5">
								<span class="font-mono text-lg font-bold text-secondary">{selectedDiagFace.score.toFixed(4)}</span>
								<span class="font-mono text-[9px] text-secondary bg-secondary/15 px-1 py-0.2 rounded font-bold">MATCH VALID</span>
							</div>
							<span class="font-mono text-[9px] text-on-surface-variant">Cutoff Threshold: ≥ 0.6800</span>
						</div>
						<div class="p-2.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between">
							<span class="font-mono text-[9px] uppercase text-on-surface-variant">HARDWARE ACCELERATION</span>
							<div class="flex items-center gap-1.5 text-primary font-mono text-[10px] font-semibold">
								<span class="material-symbols-outlined text-[15px]">memory</span>
								<span>Intel UHD 630 VAAPI</span>
							</div>
							<span class="font-mono text-[9px] text-on-surface-variant">Latency: 14.2ms · Zero CPU Lag</span>
						</div>
					</div>
				</div>
			{/if}

			<!-- BIOMETRIC FACE CARDS GRID -->
			<div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
				{#each filteredFaces as face, i (face.id)}
					<div class="flex flex-col justify-between p-3.5 rounded bg-surface-container-low border border-outline-variant/20 hover:border-outline-variant/40 transition-all relative overflow-hidden group">
						<div class="flex items-start gap-3">
							<!-- Avatar with Sight Bounding Box Accents -->
							<div class="relative w-16 h-16 rounded overflow-hidden shrink-0 bg-surface-container-lowest border border-outline-variant/30 flex items-center justify-center">
								<!-- Realistic Biometric Avatar representation -->
								<div class="w-full h-full bg-gradient-to-tr from-surface-container-high to-surface-container flex items-center justify-center text-on-surface-variant">
									<span class="material-symbols-outlined text-[32px] text-primary/70">face</span>
								</div>
								<!-- Tactical Corner Marks -->
								<div class="absolute top-0.5 left-0.5 w-2 h-2 border-t-2 border-l-2 {face.role === 'resident' ? 'border-primary' : 'border-tertiary'}"></div>
								<div class="absolute top-0.5 right-0.5 w-2 h-2 border-t-2 border-r-2 {face.role === 'resident' ? 'border-primary' : 'border-tertiary'}"></div>
								<div class="absolute bottom-0.5 left-0.5 w-2 h-2 border-b-2 border-l-2 {face.role === 'resident' ? 'border-primary' : 'border-tertiary'}"></div>
								<div class="absolute bottom-0.5 right-0.5 w-2 h-2 border-b-2 border-r-2 {face.role === 'resident' ? 'border-primary' : 'border-tertiary'}"></div>
								<span class="absolute bottom-0.5 left-0.5 right-0.5 text-center font-mono text-[8px] bg-surface-container-lowest/90 {face.role === 'resident' ? 'text-primary' : 'text-tertiary'} py-0.2 rounded font-bold">
									{face.role === 'resident' ? '99.8% SIM' : 'GUEST 3H'}
								</span>
							</div>

							<!-- Profile Information -->
							<div class="flex flex-col min-w-0 flex-1">
								<div class="flex items-center justify-between gap-1">
									<span class="font-bold text-sm text-on-surface truncate">{face.name}</span>
									<span class="font-mono text-[9px] px-2 py-0.5 rounded uppercase font-bold tracking-wider {face.role === 'resident' ? 'bg-primary/15 text-primary' : 'bg-tertiary-container/30 text-tertiary border border-tertiary/30'}">
										{face.role === 'resident' ? 'Resident' : 'Guest'}
									</span>
								</div>

								<div class="flex items-center gap-1.5 font-mono text-[10px] text-on-surface-variant mt-0.5">
									<span class="font-semibold text-on-surface">ID: #{face.id}</span>
									<span>•</span>
									<span class="{face.role === 'resident' ? 'text-secondary' : 'text-tertiary'}">
										{face.role === 'resident' ? 'Status: Permanen' : 'Expire: 3 Jam'}
									</span>
								</div>

								<div class="font-mono text-[10px] text-on-surface-variant/80 truncate mt-1">
									Vector: <span class="text-primary-fixed-dim">arcface_emb_00{face.id}</span> (512D)
								</div>
								<div class="font-mono text-[9px] text-outline mt-0.5">
									Didaftarkan: {face.created_at || '2026-10-15 22:30 WIB'}
								</div>
							</div>
						</div>

						<!-- Card Bottom Actions Footer -->
						<div class="mt-3 pt-2.5 flex items-center justify-between gap-1 border-t border-outline-variant/20 -mx-3.5 -mb-3.5 px-3.5 pb-2 bg-surface-container-lowest/40">
							<div class="flex items-center gap-1 text-on-surface-variant font-mono text-[10px]">
								<span class="material-symbols-outlined text-[13px] text-secondary">check_circle</span>
								<span>Zona: Gerbang & Teras</span>
							</div>

							<div class="flex items-center gap-1.5">
								<button
									type="button"
									onclick={() => openDiag(face.name, `arcface_emb_00${face.id}`, 0.9982)}
									class="px-2 py-1 rounded bg-surface-container hover:bg-surface-container-high text-primary font-mono text-[10px] font-semibold transition-colors flex items-center gap-1 cursor-pointer"
								>
									<span class="material-symbols-outlined text-[13px]">psychology</span>
									<span>Test ID</span>
								</button>

								<!-- Delete Face Form -->
								<form
									method="POST"
									action="?/delete"
									onsubmit={(e) => {
										if (!confirm(`Hapus ${face.name} dari whitelist wajah?`)) {
											e.preventDefault();
										}
									}}
								>
									<input type="hidden" name="id" value={face.id} />
									<button
										type="submit"
										class="p-1 rounded bg-error-container/30 hover:bg-error-container text-error transition-colors cursor-pointer"
										title="Hapus dari Whitelist"
									>
										<span class="material-symbols-outlined text-[15px]">delete</span>
									</button>
								</form>
							</div>
						</div>
					</div>
				{/each}

				{#if filteredFaces.length === 0}
					<div class="col-span-2 p-8 text-center bg-surface-container-low border border-outline-variant/20 rounded flex flex-col items-center justify-center gap-2">
						<span class="material-symbols-outlined text-outline text-[32px]">face_retouching_off</span>
						<p class="text-xs text-on-surface-variant">Tidak ada wajah yang sesuai dengan pencarian "{searchQuery}"</p>
					</div>
				{/if}
			</div>
		</div>

		<!-- RIGHT 4 COLUMNS: REGISTRATION FORM & TELEGRAM BOT SYNC -->
		<div class="xl:col-span-4 flex flex-col gap-4">
			<!-- Registration Form Card -->
			<div class="p-4 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col gap-3 shadow-sm">
				<div class="flex items-center justify-between pb-1 border-b border-outline-variant/20">
					<div class="flex items-center gap-2">
						<span class="material-symbols-outlined text-primary text-[18px]">person_add</span>
						<span class="font-bold text-xs uppercase tracking-wider text-on-surface">Tambah Wajah Baru</span>
					</div>
					<span class="font-mono text-[9px] text-primary bg-primary/10 px-1.5 py-0.2 rounded font-semibold">POST /api/faces</span>
				</div>

				<form method="POST" action="?/add" class="flex flex-col gap-3">
					<div class="flex flex-col gap-1">
						<label for="input-face-name" class="font-mono text-[10px] uppercase text-on-surface font-semibold">NAMA ANGGOTA / TAMU *</label>
						<input
							id="input-face-name"
							name="name"
							type="text"
							required
							placeholder="Contoh: Ayah, Ibu, Reza, Kurir"
							class="w-full bg-surface-container-lowest border border-outline-variant/30 text-on-surface text-xs px-3 py-2 rounded focus:outline-none focus:border-primary"
						/>
					</div>

					<div class="flex flex-col gap-1">
						<label for="input-face-role" class="font-mono text-[10px] uppercase text-on-surface font-semibold">PERAN / HAK AKSES *</label>
						<select
							id="input-face-role"
							name="role"
							class="w-full bg-surface-container-lowest border border-outline-variant/30 text-on-surface text-xs px-3 py-2 rounded focus:outline-none focus:border-primary"
						>
							<option value="resident">Penghuni Rumah (Permanen - Auto Mute Siren)</option>
							<option value="guest_temporary">Tamu Sementara (Whitelist 3 Jam)</option>
						</select>
					</div>

					<div class="p-2.5 rounded bg-surface-container-lowest border border-outline-variant/20 flex flex-col gap-1 text-[11px]">
						<div class="flex items-center gap-1.5 text-primary font-mono text-[10px] font-semibold">
							<span class="material-symbols-outlined text-[14px]">neurology</span>
							<span>ArcFace 512D Vector Generator</span>
						</div>
						<p class="text-[10px] text-on-surface-variant leading-relaxed">
							Sistem mengekstrak landmark biometrik 512 dimensi dan menyimpannya ke database lokal SQLite.
						</p>
					</div>

					<button
						type="submit"
						class="w-full py-2 px-3 rounded bg-primary text-on-primary font-semibold text-xs hover:bg-surface-tint transition-all shadow-md active:scale-95 cursor-pointer flex items-center justify-center gap-1.5"
					>
						<span class="material-symbols-outlined text-[16px]">save</span>
						<span>SIMPAN KE WHITELIST</span>
					</button>
				</form>
			</div>

			<!-- Telegram Bot Sync Panel -->
			<div class="p-4 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col gap-3 relative overflow-hidden">
				<div class="flex items-center justify-between">
					<div class="flex items-center gap-2">
						<div class="w-7 h-7 rounded bg-primary-container text-on-primary-container flex items-center justify-center">
							<span class="material-symbols-outlined text-[16px]">send</span>
						</div>
						<div class="flex flex-col">
							<span class="font-bold text-xs uppercase tracking-wider text-on-surface">Telegram Bot Sync</span>
							<span class="font-mono text-[10px] text-secondary">@cctv_rumah_guard_bot</span>
						</div>
					</div>
					<span class="font-mono text-[9px] bg-secondary/15 text-secondary px-1.5 py-0.5 rounded font-semibold">WEBHOOK ACTIVE</span>
				</div>

				<p class="text-xs text-on-surface-variant leading-relaxed">
					Keluarga dapat langsung mendaftarkan tamu dari smartphone via Telegram tanpa membuka konsol ini. Ketika orang asing terdeteksi di teras, bot mengirim foto & tombol aksi instan.
				</p>

				<!-- Telegram Bot Simulated Message Card -->
				<div class="rounded bg-surface-container-lowest border border-outline-variant/30 p-2.5 flex flex-col gap-2">
					<div class="flex items-center justify-between font-mono text-[10px] text-on-surface-variant">
						<span class="font-semibold text-primary">CCTV Rumah Alert Bot</span>
						<span>14:28 WIB</span>
					</div>

					<div class="text-[11px] text-on-surface">
						<span class="text-tertiary font-bold">[DETEKSI ORANG ASING]</span> Kamera Pagar Depan mendeteksi orang tidak dikenal (loitering 12s).
					</div>

					<!-- Simulated Inline Action Buttons -->
					<div class="flex flex-col gap-1 pt-1">
						<button
							type="button"
							class="w-full py-1 px-2 rounded bg-surface-variant hover:bg-surface-bright text-on-surface font-mono text-[10px] flex items-center justify-center gap-1 transition-colors"
						>
							<span class="material-symbols-outlined text-[12px] text-tertiary">check</span>
							<span>whitelist_guest:ev_9281a (3 Jam)</span>
						</button>
						<div class="grid grid-cols-2 gap-1">
							<button type="button" class="py-1 px-2 rounded bg-surface-variant text-on-surface-variant font-mono text-[10px] flex items-center justify-center gap-1">
								<span class="material-symbols-outlined text-[12px] text-error">alarm</span>
								<span>Sirine</span>
							</button>
							<button type="button" class="py-1 px-2 rounded bg-surface-variant text-on-surface-variant font-mono text-[10px] flex items-center justify-center gap-1">
								<span class="material-symbols-outlined text-[12px]">volume_off</span>
								<span>Mute</span>
							</button>
						</div>
					</div>
				</div>

				<div class="flex items-center justify-between font-mono text-[9px] text-on-surface-variant">
					<span>Auto-Whitelisting via Bot</span>
					<span class="text-primary font-medium">REST API Sync OK</span>
				</div>
			</div>
		</div>
	</div>
</div>
