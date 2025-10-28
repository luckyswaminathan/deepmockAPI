import Link from "next/link";
import { listComponents } from "@/lib/api";
import ComponentsFilterList from "./ComponentsFilterList";

export default async function ApiComponents({ params }: { params: { apiSlug: string } }) {
  const { apiSlug } = params;
  const components = await listComponents(apiSlug);
  return (
    <main className="mx-auto max-w-5xl p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Components for {apiSlug}</h1>
        <div className="flex items-center gap-4 text-sm">
          <Link href={`/apis/${encodeURIComponent(apiSlug)}/routes`} className="text-blue-600 hover:underline">
            Route explorer
          </Link>
          <Link href={`/apis/${encodeURIComponent(apiSlug)}/graph`} className="text-blue-600 hover:underline">
            View graph
          </Link>
          <Link href="/" className="text-blue-600 hover:underline">Back</Link>
        </div>
      </div>
      {components.length === 0 ? (
        <p className="text-gray-600">No components found.</p>
      ) : (
        <ComponentsFilterList components={components} apiSlug={apiSlug} />
      )}
    </main>
  );
}
