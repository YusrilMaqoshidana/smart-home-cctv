<script lang="ts">
	import type { PageData, ActionData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();
</script>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
		<div>
			<h1 class="text-lg font-bold text-slate-100 flex items-center gap-2">
				<i class="fa-solid fa-user-check text-emerald-400"></i> Whitelist Wajah Keluarga (InsightFace)
			</h1>
			<p class="text-xs text-slate-400">
				Daftarkan foto wajah anggota keluarga untuk menekan notifikasi darurat palsu saat beraktivitas normal.
			</p>
		</div>
	</div>

	{#if form?.error}
		<div class="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl text-xs text-rose-400 flex items-center gap-2">
			<i class="fa-solid fa-circle-exclamation"></i>
			<span>{form.error}</span>
		</div>
	{/if}

	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
		<!-- Form Tambah Wajah Baru -->
		<div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4 h-fit">
			<h2 class="text-sm font-semibold text-slate-200 flex items-center gap-2">
				<i class="fa-solid fa-user-plus text-indigo-400"></i> Tambah Wajah Baru
			</h2>

			<form method="POST" action="?/add" class="space-y-3.5">
				<div>
					<label for="face-name" class="block text-xs font-medium text-slate-300 mb-1">Nama Anggota Keluarga</label>
					<input
						id="face-name"
						type="text"
						name="name"
						required
						placeholder="Contoh: Ayah, Ibu, Kakak"
						class="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
					/>
				</div>

				<div>
					<label for="face-role" class="block text-xs font-medium text-slate-300 mb-1">Peran / Status</label>
					<select
						id="face-role"
						name="role"
						class="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
					>
						<option value="resident">Penghuni Rumah (Permanen)</option>
						<option value="guest_temporary">Tamu Sementara (Whitelist 3 Jam)</option>
					</select>
				</div>

				<div class="p-3 bg-slate-950/60 border border-slate-800 rounded-xl space-y-1">
					<p class="text-[11px] font-medium text-indigo-400 flex items-center gap-1.5">
						<i class="fa-solid fa-shield text-[10px]"></i> ArcFace Vector Engine
					</p>
					<p class="text-[10px] text-slate-400">Vektor embedding 512-dimensi dihasilkan dan disimpan ke database lokal SQLite-VSS.</p>
				</div>

				<button
					type="submit"
					class="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-500 rounded-xl text-xs font-semibold text-white shadow-lg shadow-indigo-600/30 transition-all flex items-center justify-center gap-2"
				>
					<i class="fa-solid fa-plus"></i> Simpan ke Whitelist
				</button>
			</form>
		</div>

		<!-- Tabel Daftar Wajah Terdaftar -->
		<div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
			<h2 class="text-sm font-semibold text-slate-200 flex items-center justify-between">
				<span>Daftar Wajah Aktif ({data.faces.length})</span>
				<span class="text-[11px] font-mono text-emerald-400">InsightFace Vector Store</span>
			</h2>

			<div class="overflow-x-auto">
				<table class="w-full text-left text-xs">
					<thead class="text-slate-400 border-b border-slate-800 bg-slate-950/40">
						<tr>
							<th class="py-2.5 px-3">Nama</th>
							<th class="py-2.5 px-3">Status</th>
							<th class="py-2.5 px-3">Terdaftar</th>
							<th class="py-2.5 px-3 text-right">Aksi</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-slate-800/60">
						{#each data.faces as face}
							<tr class="hover:bg-slate-800/30">
								<td class="py-3 px-3 flex items-center gap-2.5 font-medium text-slate-200">
									<span class="h-6 w-6 rounded-full bg-indigo-950 border border-indigo-500/30 flex items-center justify-center text-[10px]">
										👤
									</span>
									{face.name}
								</td>
								<td class="py-3 px-3">
									<span class="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/10 text-emerald-400 font-medium capitalize">
										{face.role}
									</span>
								</td>
								<td class="py-3 px-3 text-slate-400 text-[11px] font-mono">
									{face.created_at || 'Baru saja'}
								</td>
								<td class="py-3 px-3 text-right">
									<form
										method="POST"
										action="?/delete"
										class="inline"
										onsubmit={(e) => {
											if (!confirm(`Hapus wajah ${face.name} dari whitelist?`)) e.preventDefault();
										}}
									>
										<input type="hidden" name="id" value={face.id} />
										<button
											type="submit"
											aria-label="Hapus wajah"
											class="px-2.5 py-1 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
										>
											<i class="fa-solid fa-trash"></i>
										</button>
									</form>
								</td>
							</tr>
						{:else}
							<tr>
								<td colspan="4" class="py-8 text-center text-slate-500">
									Belum ada anggota keluarga yang didaftarkan.
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
