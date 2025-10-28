import Link from "next/link";
import { listRoutes } from "@/lib/api";
import RoutePlayground from "./RoutePlayground";

type PageProps = {
  params: Promise<{
    apiSlug: string;
  }>;
};

export default async function ApiRoutesPage({ params }: PageProps) {
  const { apiSlug } = await params;
  const routes = await listRoutes(apiSlug);

  return (
    <main className="mx-auto max-w-6xl p-8 space-y-6">
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Route Explorer</h1>
          <p className="text-sm text-gray-600">Send requests to generated mock routes for {apiSlug}.</p>
        </div>
        <div className="flex gap-4 text-sm">
          <Link href={`/apis/${encodeURIComponent(apiSlug)}`} className="text-blue-600 hover:underline">
            Components
          </Link>
          <Link href="/" className="text-blue-600 hover:underline">
            Back
          </Link>
        </div>
      </div>
      {routes.length === 0 ? (
        <p className="rounded border border-dashed p-6 text-center text-gray-600">
          No routes found. Upload an OpenAPI spec and generate routes first.
        </p>
      ) : (
        <RoutePlayground apiSlug={apiSlug} routes={routes} />
      )}
    </main>
  );
}
