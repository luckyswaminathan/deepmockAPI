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
        <Link href="/" className="text-blue-600 hover:underline">Back</Link>
      </div>
      {components.length === 0 ? (
        <p className="text-gray-600">No components found.</p>
      ) : (
        <ComponentsFilterList components={components} apiSlug={apiSlug} />
      )}
    </main>
  );
}


