"use client";

import { useRef, useState } from "react";
import { uploadOpenApiSpec } from "@/lib/api";
import Link from "next/link";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [apiName, setApiName] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus(null);
    setError(null);
    if (!file) {
      setError("Select a file.");
      return;
    }
    const form = new FormData();
    form.append("spec_file", file);
    if (apiName.trim()) form.append("api_name", apiName.trim());
    try {
      setIsSubmitting(true);
      const result = await uploadOpenApiSpec(form);
      setStatus(`Uploaded ${result.api_name} (${result.api_slug}) with ${result.components.length} components.`);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Upload failed";
      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="mx-auto max-w-3xl p-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Upload OpenAPI Spec</h1>
          <p className="text-sm text-gray-600 mt-1">JSON or YAML. We will parse components and generate browsable tables.</p>
        </div>
        <Link href="/" className="text-purple-700 hover:underline">Back</Link>
      </div>

      <div className="rounded-lg border shadow-sm p-6 bg-white">
        <form className="space-y-6" onSubmit={onSubmit}>
          <div className="space-y-2">
            <label className="block text-sm font-medium">API Name (optional)</label>
            <input
              className="w-full rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-300"
              value={apiName}
              onChange={(e) => setApiName(e.target.value)}
              placeholder="Friendly API name"
            />
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-medium">OpenAPI JSON/YAML</label>
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              accept=".json,.yaml,.yml,application/json,application/yaml,text/yaml"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="rounded-md bg-purple-600 px-4 py-2 text-white hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-300"
              >
                Choose file
              </button>
              {file ? (
                <span className="text-sm text-gray-700 truncate max-w-[60%]">{file.name}</span>
              ) : (
                <span className="text-sm text-gray-500">No file selected</span>
              )}
              {file && (
                <button
                  type="button"
                  onClick={() => setFile(null)}
                  className="text-sm text-purple-700 hover:underline"
                >
                  Clear
                </button>
              )}
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={!file || isSubmitting}
              className="rounded-md bg-purple-600 px-4 py-2 text-white hover:bg-purple-700 disabled:opacity-60 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-purple-300"
            >
              {isSubmitting ? "Uploading..." : "Upload"}
            </button>
          </div>
        </form>
      </div>

      <div className="mt-4 min-h-[24px]">
        {status && <p className="text-green-700">{status}</p>}
        {error && <p className="text-red-700">{error}</p>}
      </div>
    </main>
  );
}


