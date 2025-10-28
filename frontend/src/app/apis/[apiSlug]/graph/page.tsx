import Link from "next/link";
import { notFound } from "next/navigation";
import { getComponentGraph } from "@/lib/api";
import DependencyGraph from "./DependencyGraph";

type PageProps = {
  params: Promise<{ apiSlug: string }>;
};

export default async function ComponentGraphPage({ params }: PageProps) {
  const { apiSlug } = await params;
  let graph;
  try {
    graph = await getComponentGraph(apiSlug);
  } catch (err) {
    if (err instanceof Error && err.message.includes("404")) {
      notFound();
    }
    throw err;
  }

  return (
    <main className="mx-auto max-w-6xl p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Component Graph</h1>
          <p className="text-sm text-gray-600">Showing schema references for {apiSlug}</p>
        </div>
        <div className="flex gap-4 text-sm">
          <Link className="text-blue-600 hover:underline" href={`/apis/${encodeURIComponent(apiSlug)}`}>
            Back to components
          </Link>
          <Link className="text-blue-600 hover:underline" href="/">
            Dashboard
          </Link>
        </div>
      </div>

      <DependencyGraph apiSlug={apiSlug} graph={graph} />
    </main>
  );
}
