export interface FileUploaderProps {
	onUpload: (files: File[]) => Promise<void>;
	acceptedTypes?: string[];
	label?: string;
}
