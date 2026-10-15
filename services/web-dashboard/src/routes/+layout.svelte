<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';

	let { children } = $props();

	function isActive(pathname: string, current: string) {
		if (pathname === '/' && current === '/') return true;
		if (pathname !== '/' && current.startsWith(pathname)) return true;
		return false;
	}
</script>

<svelte:head>
	<title>Smart Home Guard - Lenovo M70q Homelab</title>
</svelte:head>

<div class="min-h-screen flex flex-col bg-slate-950 text-slate-100">
	<!-- Top Navigation Header -->
	<header class="border-b border-slate-800/80 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
			<div class="flex items-center gap-6">
				<a href="/" class="flex items-center gap-3 group">
					<div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 group-hover:scale-105 transition-transform">
						<i class="fa-solid fa-shield-halved text-lg"></i>
					</div>
					<div>
						<span class="font-bold text-base tracking-wide flex items-center gap-2 text-white">
							Smart Home Guard
							<span class="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">SvelteKit SSR</span>
						</span>
						<p class="text-xs text-slate-400">Lenovo ThinkCentre M70q &bull; Frigate 0.15 &bull; Dokploy</p>
					</div>
				</a>

				<!-- Navigation Links -->
				<nav class="hidden md:flex items-center gap-1.5 pl-4 border-l border-slate-800">
					<a
						href="/"
						class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors {isActive('/', $page.url.pathname) ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'}"
					>
						<i class="fa-solid fa-chart-line mr-1.5"></i> Dashboard
					</a>
					<a
						href="/faces"
						class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors {isActive('/faces', $page.url.pathname) ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'}"
					>
						<i class="fa-solid fa-user-check mr-1.5"></i> Wajah Keluarga
					</a>
					<a
						href="/plates"
						class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors {isActive('/plates', $page.url.pathname) ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'}"
					>
						<i class="fa-solid fa-car mr-1.5"></i> Plat Kendaraan
					</a>
					<a
						href="/events"
						class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors {isActive('/events', $page.url.pathname) ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'}"
					>
						<i class="fa-solid fa-list-ul mr-1.5"></i> Log Kejadian
					</a>
				</nav>
			</div>

			<!-- System Indicator -->
			<div class="flex items-center gap-3">
				<div class="hidden sm:flex flex-col text-right">
					<span class="text-xs font-medium text-slate-200">Server Homelab</span>
					<span class="text-[10px] text-emerald-400 font-mono">CPU &lt; 20% (VAAPI iGPU)</span>
				</div>
				<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm">
					<span class="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span> Online
				</span>
			</div>
		</div>
	</header>

	<!-- Mobile Bottom Nav -->
	<div class="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-slate-900/90 backdrop-blur border-t border-slate-800 flex justify-around py-2.5">
		<a href="/" class="flex flex-col items-center gap-1 text-[10px] {isActive('/', $page.url.pathname) ? 'text-indigo-400 font-semibold' : 'text-slate-400'}">
			<i class="fa-solid fa-chart-line text-sm"></i> Beranda
		</a>
		<a href="/faces" class="flex flex-col items-center gap-1 text-[10px] {isActive('/faces', $page.url.pathname) ? 'text-indigo-400 font-semibold' : 'text-slate-400'}">
			<i class="fa-solid fa-user-check text-sm"></i> Wajah
		</a>
		<a href="/plates" class="flex flex-col items-center gap-1 text-[10px] {isActive('/plates', $page.url.pathname) ? 'text-indigo-400 font-semibold' : 'text-slate-400'}">
			<i class="fa-solid fa-car text-sm"></i> Plat
		</a>
		<a href="/events" class="flex flex-col items-center gap-1 text-[10px] {isActive('/events', $page.url.pathname) ? 'text-indigo-400 font-semibold' : 'text-slate-400'}">
			<i class="fa-solid fa-list-ul text-sm"></i> Log
		</a>
	</div>

	<!-- Main Body Container -->
	<main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 pb-20 md:pb-8">
		{@render children()}
	</main>

	<!-- Footer -->
	<footer class="border-t border-slate-900 bg-slate-950 py-4 text-center text-xs text-slate-500 hidden md:block">
		Smart Home CCTV &bull; SvelteKit SSR Architecture &bull; Secure Internal Network
	</footer>
</div>
