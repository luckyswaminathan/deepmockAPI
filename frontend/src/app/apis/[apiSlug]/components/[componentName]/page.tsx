import Link from "next/link";
import { getComponentDetail } from "@/lib/api";

export default async function ComponentDetailPage({
  params,
}: {
  params: { apiSlug: string; componentName: string };
}) {
  const { apiSlug, componentName } = params;
  const detail = await getComponentDetail(apiSlug, componentName);

  return (
    <main className="mx-auto max-w-5xl p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{detail.component_name}</h1>
        <Link href={`/apis/${encodeURIComponent(apiSlug)}`} className="text-blue-600 hover:underline">
          Back
        </Link>
      </div>
      <p className="text-sm text-gray-600">Table: {detail.table_name}</p>
      <div className="overflow-x-auto">
        <table className="min-w-full border rounded">
          <thead>
            <tr className="bg-gray-100 text-left">
              <th className="border p-2">Property</th>
              <th className="border p-2">Type</th>
              <th className="border p-2">Format</th>
              <th className="border p-2">Required</th>
              <th className="border p-2">Description</th>
              <th className="border p-2">Example</th>
              <th className="border p-2">Reference</th>
            </tr>
          </thead>
          <tbody>
            {detail.properties.map((row) => (
              <tr key={row.id}>
                <td className="border p-2 whitespace-nowrap">{row.property_name}</td>
                <td className="border p-2">{row.property_type ?? "n/a"}</td>
                <td className="border p-2">{row.property_format ?? "n/a"}</td>
                <td className="border p-2">{row.is_required ? "Yes" : "No"}</td>
                <td className="border p-2">{row.description ?? "—"}</td>
                <td className="border p-2">
                  {row.example !== undefined && row.example !== null ? (
                    <code className="text-xs">{String(row.example)}</code>
                  ) : (
                    "—"
                  )}
                </td>
                <td className="border p-2">{row.reference ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}


