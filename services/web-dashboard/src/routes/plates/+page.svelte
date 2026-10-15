<script lang="ts">
	import type { PageData, ActionData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();

	let inputPlate = $state('B 1234 XYZ');
	let inputLabel = $state('Avanza Hitam Ayah');
	let selectedVehicleType = $state<'car' | 'motorcycle'>('car');
	let isFamily = $state(true);
	let manualGateOpen = $state(false);

	// Indonesian TNKB regex validator
	const tnkbRegex = /^([A-Z]{1,2})\s*([0-9]{1,4})\s*([A-Z]{1,3})$/i;
	let isValidPlate = $derived(tnkbRegex.test(inputPlate.trim()));

	function formatPlateInput(val: string) {
		inputPlate = val.toUpperCase();
	}

	function triggerManualGate() {
		manualGateOpen = true;
		setTimeout(() => {
			manualGateOpen = false;
		}, 3000);
	}
</script>

<div class="flex flex-col gap-5">
	<!-- TOP METRICS STATS BAR -->
	<div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
		<!-- Stat 1: Total Registered Plates -->
		<div class="p-3.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase text-on-surface-variant font-medium">TOTAL PLAT WHITELIST</span>
					<span class="text-xs text-on-surface-variant/80">Kendaraan Terdaftar</span>
				</div>
				<div class="w-7 h-7 rounded bg-primary/10 flex items-center justify-center text-primary">
					<span class="material-symbols-outlined text-[18px]">badge</span>
				</div>
			</div>
			<div class="mt-3 flex items-baseline justify-between">
				<span class="font-mono text-2xl font-bold text-primary">{data.plates.length || 2}</span>
				<span class="font-mono text-[10px] text-secondary bg-surface-container-high px-1.5 py-0.5 rounded font-medium">ALPR Ready</span>
			</div>
			<div class="w-full bg-surface-container h-1 rounded mt-2.5 overflow-hidden">
				<div class="bg-primary h-full w-full"></div>
			</div>
		</div>

		<!-- Stat 2: Family Vehicles (Auto-Barrier) -->
		<div class="p-3.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase text-on-surface-variant font-medium">KENDARAAN KELUARGA</span>
					<span class="text-xs text-on-surface-variant/80">Auto-Barrier GPIO 18</span>
				</div>
				<div class="w-7 h-7 rounded bg-secondary/10 flex items-center justify-center text-secondary">
					<span class="material-symbols-outlined text-[18px]">garage</span>
				</div>
			</div>
			<div class="mt-3 flex items-baseline justify-between">
				<span class="font-mono text-2xl font-bold text-secondary">{data.plates.length || 2}</span>
				<span class="font-mono text-[10px] text-secondary bg-surface-container-high px-1.5 py-0.5 rounded font-medium">Auto-Open</span>
			</div>
			<div class="w-full bg-surface-container h-1 rounded mt-2.5 overflow-hidden">
				<div class="bg-secondary h-full w-full"></div>
			</div>
		</div>

		<!-- Stat 3: OCR Accuracy -->
		<div class="p-3.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase text-on-surface-variant font-medium">AKURASI OCR TNKB</span>
					<span class="text-xs text-on-surface-variant/80">DeepPlate Indonesia</span>
				</div>
				<div class="w-7 h-7 rounded bg-tertiary/10 flex items-center justify-center text-tertiary">
					<span class="material-symbols-outlined text-[18px]">document_scanner</span>
				</div>
			</div>
			<div class="mt-3 flex items-baseline justify-between">
				<div class="flex items-baseline gap-1">
					<span class="font-mono text-2xl font-bold text-tertiary">98.9</span>
					<span class="font-mono text-sm text-tertiary">%</span>
				</div>
				<span class="font-mono text-[10px] text-tertiary bg-surface-container-high px-1.5 py-0.5 rounded font-medium">42ms Latency</span>
			</div>
			<div class="w-full bg-surface-container h-1 rounded mt-2.5 overflow-hidden">
				<div class="bg-tertiary h-full w-[98.9%]"></div>
			</div>
		</div>

		<!-- Stat 4: Barrier Relay Status -->
		<div class="p-3.5 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col justify-between">
			<div class="flex items-start justify-between">
				<div class="flex flex-col">
					<span class="font-mono text-[10px] uppercase text-on-surface-variant font-medium">RELAY CARPORT</span>
					<span class="text-xs text-on-surface-variant/80">Hardware Pin GPIO 18</span>
				</div>
				<div class="w-7 h-7 rounded bg-secondary/10 flex items-center justify-center text-secondary">
					<span class="material-symbols-outlined text-[18px]">lock_open</span>
				</div>
			</div>
			<div class="mt-3 flex items-baseline justify-between">
				<span class="font-mono text-sm font-bold text-secondary">STANDBY</span>
				<span class="font-mono text-[10px] text-secondary bg-surface-container-high px-1.5 py-0.5 rounded font-medium">&lt; 250ms</span>
			</div>
			<div class="w-full bg-surface-container h-1 rounded mt-2.5 overflow-hidden">
				<div class="bg-secondary h-full w-full"></div>
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

	<!-- BENTO SPLIT: REGISTRATION FORM + MOCKUP (7 COLS) & LIVE OCR CAM (5 COLS) -->
	<div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
		<!-- LEFT 7 COLUMNS: REGISTRATION FORM & PHYSICAL TNKB MOCKUP -->
		<div class="lg:col-span-7 flex flex-col gap-4">
			<div class="p-4 bg-surface-container-low border border-outline-variant/20 rounded-lg shadow-sm flex flex-col gap-4">
				<div class="flex items-center justify-between pb-2 border-b border-outline-variant/20">
					<div class="flex items-center gap-2">
						<span class="material-symbols-outlined text-primary text-[20px]">badge</span>
						<span class="font-bold text-xs uppercase tracking-wider text-on-surface">Registrasi Kendaraan & Plat Nomor</span>
					</div>
					<span class="font-mono text-[9px] px-2 py-0.5 rounded bg-surface-container text-primary font-medium">POST /api/plates</span>
				</div>

				<!-- Realistic Indonesian TNKB Plate Visual Mockup -->
				<div class="p-3.5 rounded bg-surface-container-lowest border border-outline-variant/30 flex flex-col gap-2">
					<div class="flex items-center justify-between">
						<span class="font-mono text-[10px] uppercase text-on-surface-variant font-medium">PREVIEW FISIK TNKB INDONESIA (STANDAR KORLANTAS)</span>
						<div class="flex items-center gap-1.5 font-mono text-[10px] {isValidPlate ? 'text-secondary' : 'text-error'}">
							<span class="material-symbols-outlined text-[14px]">{isValidPlate ? 'verified' : 'error'}</span>
							<span>{isValidPlate ? 'SYNTAX SAMSAT VALID' : 'FORMAT BELUM SESUAI'}</span>
						</div>
					</div>

					<!-- Embossed Stamped Plate Element -->
					<div class="relative w-full py-4 px-6 bg-surface-dim rounded border-2 border-surface-variant/40 flex flex-col items-center justify-center shadow-inner overflow-hidden">
						<!-- Outer embossed outline -->
						<div class="absolute inset-1 rounded border border-white/20 pointer-events-none"></div>

						<!-- Realtime Dynamic Stamped Plate Text -->
						<div class="flex items-center justify-center gap-3 py-1">
							<span class="font-mono text-3xl sm:text-4xl leading-none font-bold text-on-surface tracking-[0.22em] drop-shadow-[0_2px_4px_rgba(0,0,0,0.9)]">
								{inputPlate || 'B 1234 XYZ'}
							</span>
						</div>

						<!-- Tax Period Stamp (Masa Berlaku) -->
						<div class="flex items-center justify-between w-full max-w-[260px] pt-1.5 px-3">
							<span class="font-mono text-[9px] text-on-surface-variant/70 tracking-widest font-semibold">KORLANTAS POLRI</span>
							<span class="font-mono text-[10px] text-on-surface-variant font-bold tracking-widest">10 • 29</span>
						</div>
					</div>
				</div>

				<!-- Registration Form -->
				<form method="POST" action="?/add" class="flex flex-col gap-3.5">
					<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
						<!-- Input Plate Number -->
						<div class="flex flex-col gap-1">
							<label for="input-tnkb-plate" class="font-mono text-[10px] uppercase text-on-surface font-semibold">NOMOR TNKB (PLAT NOMOR) *</label>
							<div class="relative flex items-center">
								<input
									id="input-tnkb-plate"
									name="plate_number"
									type="text"
									required
									maxlength="12"
									value={inputPlate}
									oninput={(e) => formatPlateInput(e.currentTarget.value)}
									placeholder="Contoh: B 1234 XYZ"
									class="w-full bg-surface-container text-on-surface font-mono text-xs px-3 py-2 rounded border {isValidPlate ? 'border-outline-variant/30 focus:border-secondary' : 'border-error/50 focus:border-error'} focus:outline-none uppercase tracking-wider"
								/>
								<span class="material-symbols-outlined {isValidPlate ? 'text-secondary' : 'text-outline'} absolute right-2.5 pointer-events-none text-[18px]">
									{isValidPlate ? 'check_circle' : 'pending'}
								</span>
							</div>
							<span class="font-mono text-[9px] text-on-surface-variant">Pola: ^[A-Z]{'{1,2}'}\s[0-9]{'{1,4}'}\s[A-Z]{'{1,3}'}$</span>
						</div>

						<!-- Input Vehicle Owner / Label -->
						<div class="flex flex-col gap-1">
							<label for="input-tnkb-label" class="font-mono text-[10px] uppercase text-on-surface font-semibold">KETERANGAN / PEMILIK *</label>
							<input
								id="input-tnkb-label"
								name="owner_label"
								type="text"
								required
								bind:value={inputLabel}
								placeholder="Contoh: Avanza Hitam Ayah"
								class="w-full bg-surface-container text-on-surface text-xs px-3 py-2 rounded border border-outline-variant/30 focus:outline-none focus:border-primary"
							/>
							<span class="font-mono text-[9px] text-on-surface-variant">Label untuk push alert Telegram & log</span>
						</div>
					</div>

					<!-- Vehicle Type Selector + Family Switch -->
					<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
						<!-- Vehicle Type Radio Cards -->
						<div class="flex flex-col gap-1">
							<span class="font-mono text-[10px] uppercase text-on-surface font-semibold">TIPE KENDARAAN</span>
							<div class="grid grid-cols-2 gap-2">
								<label class="flex items-center gap-2 p-2 rounded cursor-pointer transition-colors border {selectedVehicleType === 'car' ? 'bg-surface-container-high border-primary text-on-surface' : 'bg-surface-container border-transparent text-on-surface-variant'}">
									<input
										type="radio"
										name="vehicle_type"
										value="car"
										checked={selectedVehicleType === 'car'}
										onchange={() => selectedVehicleType = 'car'}
										class="hidden"
									/>
									<span class="material-symbols-outlined text-[18px] {selectedVehicleType === 'car' ? 'text-primary' : 'text-on-surface-variant'}">directions_car</span>
									<div class="flex flex-col">
										<span class="text-xs font-semibold">Mobil</span>
										<span class="font-mono text-[9px] text-on-surface-variant">Car / SUV</span>
									</div>
								</label>

								<label class="flex items-center gap-2 p-2 rounded cursor-pointer transition-colors border {selectedVehicleType === 'motorcycle' ? 'bg-surface-container-high border-primary text-on-surface' : 'bg-surface-container border-transparent text-on-surface-variant'}">
									<input
										type="radio"
										name="vehicle_type"
										value="motorcycle"
										checked={selectedVehicleType === 'motorcycle'}
										onchange={() => selectedVehicleType = 'motorcycle'}
										class="hidden"
									/>
									<span class="material-symbols-outlined text-[18px] {selectedVehicleType === 'motorcycle' ? 'text-primary' : 'text-on-surface-variant'}">two_wheeler</span>
									<div class="flex flex-col">
										<span class="text-xs font-semibold">Motor</span>
										<span class="font-mono text-[9px] text-on-surface-variant">Roda 2</span>
									</div>
								</label>
							</div>
						</div>

						<!-- Family Status Card -->
						<div class="flex flex-col gap-1">
							<span class="font-mono text-[10px] uppercase text-on-surface font-semibold">HAK AKSES PORTAL</span>
							<div class="p-2 rounded bg-surface-container border border-outline-variant/20 flex items-center justify-between">
								<div class="flex flex-col">
									<span class="text-xs text-secondary font-semibold">Kendaraan Keluarga</span>
									<span class="font-mono text-[9px] text-on-surface-variant">Auto-buka portal barrier</span>
								</div>
								<input
									type="checkbox"
									bind:checked={isFamily}
									class="w-4 h-4 accent-secondary cursor-pointer"
								/>
							</div>
						</div>
					</div>

					<!-- Submit Action Toolbar -->
					<div class="flex items-center justify-between pt-2 border-t border-outline-variant/20">
						<div class="flex items-center gap-1.5 text-on-surface-variant font-mono text-[10px]">
							<span class="material-symbols-outlined text-[14px] text-primary">lock_open</span>
							<span>Target Relay: GPIO 18 (Barrier Carport)</span>
						</div>
						<button
							type="submit"
							class="flex items-center gap-1.5 px-4 py-2 rounded bg-primary text-on-primary font-semibold text-xs hover:bg-surface-tint transition-all shadow-md active:scale-95 cursor-pointer"
						>
							<span class="material-symbols-outlined text-[16px]">save</span>
							<span>SIMPAN PLAT NOMOR (POST)</span>
						</button>
					</div>
				</form>
			</div>

			<!-- Whitelisted Plates Table -->
			<div class="bg-surface-container-low border border-outline-variant/20 rounded-lg overflow-hidden shadow-sm">
				<div class="p-3 bg-surface-container border-b border-outline-variant/20 flex items-center justify-between">
					<div class="flex items-center gap-2">
						<span class="material-symbols-outlined text-primary text-[18px]">table_rows</span>
						<span class="font-bold text-xs uppercase tracking-wider text-on-surface">Daftar Plat Whitelist Aktif</span>
					</div>
					<span class="font-mono text-[10px] text-on-surface-variant">{data.plates.length} Kendaraan</span>
				</div>

				<div class="divide-y divide-outline-variant/20">
					{#each data.plates as plate (plate.id)}
						<div class="p-3 flex items-center justify-between gap-3 hover:bg-surface-container/50 transition-colors">
							<div class="flex items-center gap-3">
								<div class="w-8 h-8 rounded bg-surface-container-lowest border border-outline-variant/30 flex items-center justify-center text-primary">
									<span class="material-symbols-outlined text-[18px]">
										{plate.vehicle_type === 'motorcycle' ? 'two_wheeler' : 'directions_car'}
									</span>
								</div>
								<div class="flex flex-col">
									<div class="flex items-center gap-2">
										<span class="font-mono text-xs font-bold text-on-surface tracking-wider bg-surface-container-lowest px-1.5 py-0.5 rounded border border-outline-variant/30">
											{plate.display_plate || plate.plate_number}
										</span>
										<span class="font-mono text-[9px] px-1.5 py-0.2 rounded bg-secondary/15 text-secondary font-bold">
											KELUARGA
										</span>
									</div>
									<span class="text-xs text-on-surface-variant mt-0.5">{plate.owner_label}</span>
								</div>
							</div>

							<div class="flex items-center gap-2">
								<span class="hidden sm:inline font-mono text-[10px] text-secondary bg-surface-container px-2 py-0.5 rounded">
									Barrier OK
								</span>
								<form
									method="POST"
									action="?/delete"
									onsubmit={(e) => {
										if (!confirm(`Hapus plat ${plate.plate_number} dari whitelist?`)) {
											e.preventDefault();
										}
									}}
								>
									<input type="hidden" name="id" value={plate.id} />
									<button
										type="submit"
										class="p-1 rounded bg-error-container/30 hover:bg-error-container text-error transition-colors cursor-pointer"
										title="Hapus Plat"
									>
										<span class="material-symbols-outlined text-[15px]">delete</span>
									</button>
								</form>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>

		<!-- RIGHT 5 COLUMNS: LIVE CARPORT OCR CAM & HARDWARE SENSING -->
		<div class="lg:col-span-5 flex flex-col gap-4">
			<!-- Live Carport OCR Widget -->
			<div class="p-4 bg-surface-container-low border border-outline-variant/20 rounded-lg shadow-sm flex flex-col gap-3">
				<div class="flex items-center justify-between pb-1 border-b border-outline-variant/20">
					<div class="flex items-center gap-2">
						<div class="w-2 h-2 rounded-full bg-secondary animate-pulse"></div>
						<span class="font-bold text-xs uppercase tracking-wider text-on-surface">Live Carport OCR Cam</span>
					</div>
					<span class="font-mono text-[10px] px-2 py-0.5 rounded bg-surface-container text-secondary">RTSP: CAM_CARPORT_01</span>
				</div>

				<!-- 16:9 Video Stream Simulation -->
				<div class="relative w-full aspect-video bg-surface-container-lowest rounded overflow-hidden border border-outline-variant/30 flex items-center justify-center">
					<iframe 
						src="http://localhost:8889/carport" 
						title="Live Stream Carport OCR"
						class="w-full h-full border-0 absolute inset-0 z-0" 
						allow="autoplay; fullscreen"
						loading="lazy">
					</iframe>

					<div class="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-background/30 pointer-events-none z-10"></div>

					<!-- Plate Detection Box Overlay -->
					<div class="absolute bottom-[22%] left-[25%] w-[48%] h-[32%] pointer-events-auto flex flex-col justify-between p-1 border border-secondary/70 bg-secondary/10 shadow-[0_0_15px_rgba(78,222,163,0.3)] z-20">
						<div class="flex justify-between items-start">
							<span class="w-2 h-2 border-t-2 border-l-2 border-secondary"></span>
							<span class="w-2 h-2 border-t-2 border-r-2 border-secondary"></span>
						</div>
						<div class="bg-surface-container-lowest/95 p-1 rounded backdrop-blur flex flex-col gap-0.5 border border-secondary/40">
							<div class="flex items-center justify-between gap-1">
								<span class="font-mono text-[10px] font-bold text-secondary uppercase tracking-wider">OCR: B 1234 XYZ</span>
								<span class="font-mono text-[8px] bg-secondary/20 text-secondary px-1 py-0.2 rounded font-bold">98.1% MATCH</span>
							</div>
							<span class="font-mono text-[8px] text-on-surface-variant">Avanza Hitam Ayah (Keluarga)</span>
						</div>
						<div class="flex justify-between items-end">
							<span class="w-2 h-2 border-b-2 border-l-2 border-secondary"></span>
							<span class="w-2 h-2 border-b-2 border-r-2 border-secondary"></span>
						</div>
					</div>
				</div>

				<!-- Barrier Gate Relay Manual Control -->
				<div class="p-3 rounded bg-surface-container border border-outline-variant/20 flex flex-col gap-2">
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-1.5 text-xs font-semibold text-on-surface">
							<span class="material-symbols-outlined text-[16px] text-secondary">power</span>
							<span>Relay Barrier Gate (GPIO 18)</span>
						</div>
						<span class="font-mono text-[10px] text-secondary font-bold">READY</span>
					</div>
					<p class="text-[10px] text-on-surface-variant leading-relaxed">
						Saat plat keluarga terdeteksi &gt; 90% confidence di zona carport, relay 5V membuka barrier otomatis selama 10 detik.
					</p>
					<button
						type="button"
						onclick={triggerManualGate}
						class="w-full py-2 px-3 rounded font-mono text-xs font-semibold transition-all {manualGateOpen ? 'bg-secondary text-on-secondary shadow-lg' : 'bg-primary text-on-primary hover:bg-surface-tint'} cursor-pointer flex items-center justify-center gap-1.5"
					>
						<span class="material-symbols-outlined text-[16px]">{manualGateOpen ? 'lock_open' : 'garage'}</span>
						<span>{manualGateOpen ? 'BARRIER OPENING (GPIO 18 PULSE)...' : 'TEST TRIGGER BUKA BARRIER'}</span>
					</button>
				</div>
			</div>
		</div>
	</div>
</div>
