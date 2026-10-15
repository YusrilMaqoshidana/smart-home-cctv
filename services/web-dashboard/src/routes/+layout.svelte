<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';

	let { children } = $props();

	let audioArmed = $state(true);
	let currentTime = $state('');
	let mobileMenuOpen = $state(false);

	$effect(() => {
		const updateClock = () => {
			const now = new Date();
			const hours = String(now.getHours()).padStart(2, '0');
			const minutes = String(now.getMinutes()).padStart(2, '0');
			const seconds = String(now.getSeconds()).padStart(2, '0');
			currentTime = `${hours}:${minutes}:${seconds} WIB`;
		};
		updateClock();
		const interval = setInterval(updateClock, 1000);
		return () => clearInterval(interval);
	});

	function isActive(pathname: string, current: string) {
		if (pathname === '/' && current === '/') return true;
		if (pathname !== '/' && current.startsWith(pathname)) return true;
		return false;
	}
</script>

<svelte:head>
	<title>ARGUS SENTINEL · NVR Tactical Core v4.2</title>
</svelte:head>

<div class="min-h-screen bg-background text-on-surface flex flex-col font-sans selection:bg-primary-container selection:text-on-primary-container">
	<!-- DESKTOP LEFT SIDEBAR (w-64) -->
	<aside class="hidden lg:flex fixed left-0 top-0 h-full w-64 bg-surface-container-lowest border-r border-outline-variant/30 z-50 flex-col justify-between py-4">
		<div class="flex flex-col gap-6">
			<!-- SOC Matrix Indicator -->
			<div class="px-5 flex items-center justify-between">
				<div class="flex items-center gap-2">
					<div class="w-2 h-2 rounded-full bg-secondary animate-pulse"></div>
					<span class="font-mono text-[11px] font-semibold tracking-wider text-secondary uppercase">SOC MATRIX ACTIVE</span>
				</div>
				<span class="font-mono text-[10px] text-on-surface-variant bg-surface-container px-1.5 py-0.5 rounded">NODE:01</span>
			</div>

			<!-- Nav links -->
			<nav class="flex flex-col gap-1 px-3">
				<!-- Live Monitor -->
				<a
					href="/"
					class="flex items-center justify-between px-3.5 py-2.5 rounded transition-all {isActive('/', page.url.pathname) ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.3)]' : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'}"
				>
					<div class="flex items-center gap-2.5">
						<span class="material-symbols-outlined text-[19px]">videocam</span>
						<span class="text-xs tracking-tight">Live Monitor & Feeds</span>
					</div>
					<span class="font-mono text-[10px] px-1.5 py-0.5 rounded {isActive('/', page.url.pathname) ? 'bg-on-primary-container/20 text-on-primary-container' : 'bg-surface-container-high text-primary'}">2 REC</span>
				</a>

				<!-- Surveillance Logs -->
				<a
					href="/events"
					class="flex items-center justify-between px-3.5 py-2.5 rounded transition-all {isActive('/events', page.url.pathname) ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.3)]' : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'}"
				>
					<div class="flex items-center gap-2.5">
						<span class="material-symbols-outlined text-[19px]">history</span>
						<span class="text-xs tracking-tight">Log Kejadian</span>
					</div>
					<span class="font-mono text-[10px] px-1.5 py-0.5 rounded {isActive('/events', page.url.pathname) ? 'bg-on-primary-container/20 text-on-primary-container' : 'bg-surface-container-high text-tertiary'}">LIVE</span>
				</a>

				<!-- Face Whitelist -->
				<a
					href="/faces"
					class="flex items-center justify-between px-3.5 py-2.5 rounded transition-all {isActive('/faces', page.url.pathname) ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.3)]' : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'}"
				>
					<div class="flex items-center gap-2.5">
						<span class="material-symbols-outlined text-[19px]">face</span>
						<span class="text-xs tracking-tight">Wajah Keluarga</span>
					</div>
					<span class="font-mono text-[10px] px-1.5 py-0.5 rounded {isActive('/faces', page.url.pathname) ? 'bg-on-primary-container/20 text-on-primary-container' : 'bg-surface-container-high text-on-surface-variant'}">ArcFace</span>
				</a>

				<!-- Plat Nomor TNKB -->
				<a
					href="/plates"
					class="flex items-center justify-between px-3.5 py-2.5 rounded transition-all {isActive('/plates', page.url.pathname) ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_0_12px_rgba(6,182,212,0.3)]' : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'}"
				>
					<div class="flex items-center gap-2.5">
						<span class="material-symbols-outlined text-[19px]">directions_car</span>
						<span class="text-xs tracking-tight">Plat Nomor TNKB</span>
					</div>
					<span class="font-mono text-[10px] px-1.5 py-0.5 rounded {isActive('/plates', page.url.pathname) ? 'bg-on-primary-container/20 text-on-primary-container' : 'bg-surface-container-high text-secondary-fixed-dim'}">ALPR</span>
				</a>
			</nav>
		</div>

		<!-- Sidebar Bottom Telemetry -->
		<div class="px-4 flex flex-col gap-2.5">
			<!-- Frigate Detect FPS bar -->
			<div class="p-3 rounded bg-surface-container-low border border-outline-variant/20 flex flex-col gap-1.5">
				<div class="flex items-center justify-between">
					<span class="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-medium">FRIGATE DETECT</span>
					<span class="font-mono text-[11px] text-secondary font-bold">68.4 FPS</span>
				</div>
				<div class="w-full bg-surface-container h-1.5 rounded overflow-hidden">
					<div class="bg-secondary h-full w-[82%] transition-all duration-500"></div>
				</div>
			</div>

			<!-- Audio Siren Toggle -->
			<div class="p-3 rounded bg-surface-container-low border border-outline-variant/20 flex items-center justify-between">
				<span class="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant font-medium">AUDIO SIREN</span>
				<button
					type="button"
					onclick={() => audioArmed = !audioArmed}
					class="flex items-center gap-1.5 px-2.5 py-1 rounded transition-colors {audioArmed ? 'bg-tertiary-container/30 text-tertiary border border-tertiary/40' : 'bg-surface-container text-on-surface-variant'}"
				>
					<span class="material-symbols-outlined text-[15px]">{audioArmed ? 'volume_up' : 'volume_off'}</span>
					<span class="font-mono text-[10px] font-bold">{audioArmed ? 'ARMED' : 'MUTED'}</span>
				</button>
			</div>
		</div>
	</aside>

	<!-- TOP TACTICAL HEADER -->
	<header class="fixed top-0 left-0 lg:left-64 right-0 h-16 bg-surface-container-lowest/90 backdrop-blur-xl border-b border-outline-variant/30 z-40 px-4 sm:px-6 flex items-center justify-between">
		<!-- Left: System Title & Host specs -->
		<div class="flex items-center gap-3 sm:gap-4">
			<!-- Mobile Hamburger Toggle -->
			<button
				type="button"
				class="lg:hidden p-1.5 rounded bg-surface-container text-on-surface-variant hover:text-on-surface"
				onclick={() => mobileMenuOpen = !mobileMenuOpen}
				aria-label="Toggle Navigation Menu"
			>
				<span class="material-symbols-outlined text-[20px]">menu</span>
			</button>

			<div class="flex flex-col">
				<div class="flex items-center gap-2">
					<span class="material-symbols-outlined text-primary text-[20px]">shield</span>
					<span class="font-bold text-sm tracking-tight text-on-surface leading-none">ARGUS SENTINEL</span>
					<span class="hidden sm:inline font-mono text-[10px] text-primary bg-primary/10 border border-primary/20 px-1.5 py-0.2 rounded font-semibold uppercase tracking-wider">v4.2 PRO</span>
				</div>
				<span class="font-mono text-[10px] text-on-surface-variant mt-0.5">Lenovo ThinkCentre M70q · UHD 630 VAAPI</span>
			</div>
		</div>

		<!-- Right: Status Badges, Clock & Controls -->
		<div class="flex items-center gap-3">
			<div class="hidden md:flex items-center gap-2">
				<div class="flex items-center gap-1.5 px-2.5 py-1 rounded bg-surface-container border border-outline-variant/20">
					<div class="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></div>
					<span class="font-mono text-[11px] text-secondary">MQTT: OK</span>
				</div>
				<div class="flex items-center gap-1.5 px-2.5 py-1 rounded bg-surface-container border border-outline-variant/20">
					<span class="material-symbols-outlined text-[15px] text-primary">schedule</span>
					<span class="font-mono text-[11px] text-primary font-semibold tabular-nums">{currentTime || '14:32:00 WIB'}</span>
				</div>
			</div>

			<!-- Emergency Mute Button -->
			<button
				type="button"
				class="flex items-center gap-1.5 px-3 py-1.5 rounded bg-error-container text-on-error-container hover:bg-error hover:text-on-error transition-all font-mono text-[10px] font-bold tracking-wider uppercase border border-error/30 active:scale-95 cursor-pointer"
				onclick={() => {
					audioArmed = false;
					alert('Emergency Mute diaktifkan: Seluruh alarm sirine dan audio chime disenyapkan.');
				}}
			>
				<span class="material-symbols-outlined text-[15px]">notifications_off</span>
				<span class="hidden sm:inline">EMERGENCY MUTE</span>
			</button>

			<!-- Admin Badge -->
			<div class="w-8 h-8 rounded-full bg-primary/20 border border-primary/40 flex items-center justify-center text-primary font-bold text-xs">
				<span class="material-symbols-outlined text-[18px]">admin_panel_settings</span>
			</div>
		</div>
	</header>

	<!-- MOBILE DRAWER MENU (if open) -->
	{#if mobileMenuOpen}
		<div
			class="lg:hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex"
			role="presentation"
			onclick={() => mobileMenuOpen = false}
			onkeydown={(e) => { if (e.key === 'Escape') mobileMenuOpen = false; }}
		>
			<div
				class="w-64 h-full bg-surface-container-lowest border-r border-outline-variant/40 p-4 flex flex-col justify-between"
				role="dialog"
				aria-modal="true"
				tabindex="-1"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
			>

				<div class="space-y-4">
					<div class="flex items-center justify-between pb-3 border-b border-outline-variant/30">
						<div class="flex items-center gap-2">
							<span class="material-symbols-outlined text-primary text-[20px]">shield</span>
							<span class="font-bold text-sm text-on-surface">ARGUS SENTINEL</span>
						</div>
						<button type="button" onclick={() => mobileMenuOpen = false} class="text-on-surface-variant hover:text-on-surface">
							<span class="material-symbols-outlined text-[20px]">close</span>
						</button>
					</div>

					<nav class="flex flex-col gap-1.5">
						<a href="/" onclick={() => mobileMenuOpen = false} class="flex items-center justify-between px-3 py-2 rounded text-xs {isActive('/', page.url.pathname) ? 'bg-primary-container text-on-primary-container font-semibold' : 'text-on-surface-variant hover:bg-surface-container'}">
							<span class="flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">videocam</span> Live Monitor</span>
							<span class="font-mono text-[10px] text-primary">2 REC</span>
						</a>
						<a href="/events" onclick={() => mobileMenuOpen = false} class="flex items-center justify-between px-3 py-2 rounded text-xs {isActive('/events', page.url.pathname) ? 'bg-primary-container text-on-primary-container font-semibold' : 'text-on-surface-variant hover:bg-surface-container'}">
							<span class="flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">history</span> Log Kejadian</span>
							<span class="font-mono text-[10px] text-tertiary">LIVE</span>
						</a>
						<a href="/faces" onclick={() => mobileMenuOpen = false} class="flex items-center justify-between px-3 py-2 rounded text-xs {isActive('/faces', page.url.pathname) ? 'bg-primary-container text-on-primary-container font-semibold' : 'text-on-surface-variant hover:bg-surface-container'}">
							<span class="flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">face</span> Wajah Keluarga</span>
							<span class="font-mono text-[10px]">ArcFace</span>
						</a>
						<a href="/plates" onclick={() => mobileMenuOpen = false} class="flex items-center justify-between px-3 py-2 rounded text-xs {isActive('/plates', page.url.pathname) ? 'bg-primary-container text-on-primary-container font-semibold' : 'text-on-surface-variant hover:bg-surface-container'}">
							<span class="flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">directions_car</span> Plat Kendaraan</span>
							<span class="font-mono text-[10px] text-secondary">ALPR</span>
						</a>
					</nav>
				</div>

				<div class="text-[11px] font-mono text-on-surface-variant border-t border-outline-variant/30 pt-3">
					<span>SERVER: THINKCENTRE M70q</span>
					<p class="text-[10px] text-secondary mt-0.5">VAAPI HWACCEL ACTIVE</p>
				</div>
			</div>
		</div>
	{/if}

	<!-- MAIN CONTENT WRAPPER -->
	<div class="lg:pl-64 flex flex-col flex-1 pt-16">
		<main class="flex-1 p-4 sm:p-6 pb-20 lg:pb-8 max-w-[1600px] w-full mx-auto">
			{@render children()}
		</main>

		<!-- Tactical Footer -->
		<footer class="border-t border-outline-variant/20 bg-surface-container-lowest/60 px-6 py-3 text-xs text-on-surface-variant flex flex-col sm:flex-row items-center justify-between gap-2">
			<div class="flex items-center gap-2 font-mono text-[11px]">
				<span class="text-secondary">● LOCAL NVR ONLINE</span>
				<span class="text-outline-variant">|</span>
				<span>DOKPLOY DOCKER NETWORK</span>
				<span class="text-outline-variant">|</span>
				<span>STORAGE FIFO: 7 HARI AUTO-PRUNE</span>
			</div>
			<div class="font-mono text-[10px] text-on-surface-variant/80">
				ARGUS SENTINEL NVR · INSIGHTFACE + INDONESIA TNKB ALPR
			</div>
		</footer>
	</div>

	<!-- MOBILE BOTTOM NAVIGATION BAR -->
	<div class="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-surface-container-lowest/95 backdrop-blur border-t border-outline-variant/30 flex justify-around py-2">
		<a href="/" class="flex flex-col items-center gap-0.5 text-[10px] {isActive('/', page.url.pathname) ? 'text-primary font-semibold' : 'text-on-surface-variant'}">
			<span class="material-symbols-outlined text-[20px]">videocam</span>
			<span>Live</span>
		</a>
		<a href="/events" class="flex flex-col items-center gap-0.5 text-[10px] {isActive('/events', page.url.pathname) ? 'text-primary font-semibold' : 'text-on-surface-variant'}">
			<span class="material-symbols-outlined text-[20px]">history</span>
			<span>Log</span>
		</a>
		<a href="/faces" class="flex flex-col items-center gap-0.5 text-[10px] {isActive('/faces', page.url.pathname) ? 'text-primary font-semibold' : 'text-on-surface-variant'}">
			<span class="material-symbols-outlined text-[20px]">face</span>
			<span>Wajah</span>
		</a>
		<a href="/plates" class="flex flex-col items-center gap-0.5 text-[10px] {isActive('/plates', page.url.pathname) ? 'text-primary font-semibold' : 'text-on-surface-variant'}">
			<span class="material-symbols-outlined text-[20px]">directions_car</span>
			<span>Plat</span>
		</a>
	</div>
</div>
