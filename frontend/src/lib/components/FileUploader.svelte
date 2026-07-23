<script lang="ts">
	import { type FileUploaderProps } from './types';

	let { 
		onUpload, 
		acceptedTypes = ['video/*', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
		label = 'Upload Video or Document'
	} = $props<FileUploaderProps>();

	let files = $state<File[]>([]);
	let isDragging = $state(false);
	let uploadProgress = $state<Record<string, number>>({});
	let isUploading = $state(false);

	async function handleFiles(newFiles: FileList | null) {
		if (!newFiles) return;
		const fileArray = Array.from(newFiles);
		files = [...files, ...fileArray];
	}

	function handleDragOver(e: DragEvent) {
		e.preventDefault();
		isDragging = true;
	}

	function handleDragLeave() {
		isDragging = false;
	}

	async function handleDrop(e: DragEvent) {
		e.preventDefault();
		isDragging = false;
		handleFiles(e.dataTransfer?.files);
	}

	async function startUpload() {
		if (files.length === 0) return;
		isUploading = true;
		
		try {
			await onUpload(files);
		} catch (error) {
			console.error('Upload failed:', error);
		} finally {
			isUploading = false;
		}
	}

	function removeFile(index: number) {
		files = files.filter((_, i) => i !== index);
		delete uploadProgress[files[index]?.name || ''];
	}
</script>

<div class="flex flex-col gap-4 w-full max-w-2xl mx-auto p-6">
	<div 
		class="relative border-2 border-dashed rounded-xl p-12 text-center transition-all cursor-pointer
		{isDragging ? 'border-blue-500 bg-blue-50 scale-105' : 'border-gray-300 bg-gray-50 hover:border-gray-400'}"
		onkeydown={(e) => (e.key === 'Enter' || e.key === ' ') && document.getElementById('file-input')?.click()}
		role="button"
		tabindex="0"
		ondragover={handleDragOver}
		ondragleave={handleDragLeave}
		ondrop={handleDrop}
		onclick={() => document.getElementById('file-input')?.click()}
	>
		<input 
			id="file-input"
			type="file" 
			multiple 
			accept={acceptedTypes.join(',')} 
			onchange={(e) => handleFiles(e.currentTarget.files)} 
			class="hidden" 
		/>
		
		<div class="flex flex-col items-center gap-3">
			<div class="p-3 bg-white rounded-full shadow-sm text-blue-600">
				<svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<path d="M21 15v4a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
				</svg>
			</div>
			<div class="text-gray-700">
				<p class="font-medium">{label}</p>
				<p class="text-sm text-gray-500">Drag and drop your files here or click to browse</p>
			</div>
		</div>
	</div>

	{#if files.length > 0}
		<div class="grid grid-cols-1 gap-3">
			{#each files as file, index}
				<div class="flex items-center justify-between p-3 bg-white border rounded-lg shadow-sm group">
					<div class="flex items-center gap-3 overflow-hidden">
						<div class="p-2 bg-gray-100 rounded text-gray-600">
							{#if file.type.startsWith('video')}
								<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
									<polygon points="23 7 16 12 23 17 23 7"/><rect x="2" y="2" width="20" height="20" rx="2.181818" ry="2.181818"/>
								</svg>
							{:else}
								<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
									<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/>
								</svg>
							{/if}
						</div>
						<div class="overflow-hidden">
							<p class="text-sm font-medium truncate">{file.name}</p>
							<p class="text-xs text-gray-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
						</div>
					</div>
					
					<div class="flex items-center gap-2">
						{#if uploadProgress[file.name] !== undefined}
							<div class="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
								<div 
									class="h-full bg-blue-500 transition-all duration-300" 
									style="width: {uploadProgress[file.name]}%"
								></div>
							</div>
						{/if}
						<button 
							onclick={() => removeFile(index)} 
							class="p-1 text-gray-400 hover:text-red-500 transition-colors"
							aria-label="Remove file"
						>
							<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
								<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
								<line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>
							</svg>
						</button>
					</div>
				</div>
			{/each}
		</div>

		<div class="flex justify-end gap-3 mt-6">
			<button 
				onclick={() => files = []} 
				disabled={isUploading}
				class="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-800 disabled:opacity-50 transition-colors"
			>
				Clear All
			</button>
			<button 
				onclick={startUpload} 
				disabled={isUploading}
				class="px-6 py-2 text-sm font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-400 transition-all shadow-sm flex items-center gap-2"
			>
				{#if isUploading}
					<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
						<circle cx="12" cy="12" r="10"/><path d="M12 3a9 9 0 0 1 0 18"/>
					</svg>
					Uploading...
				{:else}
					Upload Files
				{/if}
			</button>
		</div>
	{/if}
</div>
