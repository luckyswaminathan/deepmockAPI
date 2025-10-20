import Link from "next/link";
import { listApis } from "@/lib/api";

export default async function Home() {
  let apis = [] as Awaited<ReturnType<typeof listApis>>;
  try {
    apis = await listApis();
  } catch {
    // ignore and show empty state
  }
  return (
    <main className="mx-auto max-w-5xl p-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold">DeepMock Dashboard</h1>
        <Link href="/upload" className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          Upload API Spec
        </Link>
      </div>
      <div className="space-y-4">
        <h2 className="text-xl font-medium">APIs</h2>
        {apis.length === 0 ? (
          <p className="text-gray-600">No APIs found. Upload an OpenAPI spec to get started.</p>
        ) : (
          <ul className="divide-y divide-gray-200 rounded border">
            {apis.map((api) => (
              <li key={api.api_slug} className="p-4 flex items-center justify-between">
                <div>
                  <div className="font-medium">{api.api_name || api.title}</div>
                  <div className="text-sm text-gray-600">{api.api_slug}{api.version ? ` • v${api.version}` : ""}</div>
                </div>
                <Link
                  className="text-blue-600 hover:underline"
                  href={`/apis/${encodeURIComponent(api.api_slug)}`}
                >
                  View components
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
    </main>
  );
}
