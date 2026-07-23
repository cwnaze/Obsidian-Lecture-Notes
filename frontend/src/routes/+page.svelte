<script lang="ts">
	import FileUploader from '$lib/components/FileUploader.svelte';
	import '../app.css';

	async function handleUpload(files: File[]) {
		console.log('Uploading files:', files);
		// Simulate upload delay
		await new Promise(resolve => setTimeout(resolve, 2000));
		alert(`Successfully uploaded ${files.length} files!`);
	}
</script>

<div class="min-h-screen bg-gray-100 py-12 px-4">
	<div class="max-w-4xl mx-auto">
		<header class="mb-12 text-center">
			<h1 class="text-4xl font-bold text-gray-900 mb-4">Lecture Notes Upload</h1>
			<p class="text-lg text-gray-600">Upload your lecture videos and documents to your Obsidian vault</p>
		</header>

		<main class="bg-white rounded-2xl shadow-xl p-8">
			<FileUploader 
				onUpload={handleUpload} 
				label="Upload Lecture Materials"
			/>
		</main>
	</div>
</div>
