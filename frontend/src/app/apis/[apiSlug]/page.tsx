import Link from "next/link";
import { listComponents } from "@/lib/api";

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
        <ul className="divide-y divide-gray-200 rounded border">
          {components.map((c) => (
            <li key={c.component_name} className="p-4 flex items-center justify-between">
              <div>
                <div className="font-medium">{c.component_name}</div>
                <div className="text-sm text-gray-600">{c.table_name}</div>
              </div>
              <Link
                className="text-blue-600 hover:underline"
                href={`/apis/${encodeURIComponent(apiSlug)}/components/${encodeURIComponent(c.component_name)}`}
              >
                View details
              </Link>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}


