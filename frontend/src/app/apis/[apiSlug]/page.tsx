import Link from "next/link";
import { listComponents, listRoutes } from "@/lib/api";
import ComponentsFilterList from "./ComponentsFilterList";

type ComponentUsage = {
  request: number;
  response: number;
  total: number;
};

function extractComponentName(ref?: string | null): string | null {
  if (!ref) return null;
  if (ref.startsWith("#/components/schemas/")) {
    const parts = ref.split("/");
    return parts[parts.length - 1] || null;
  }
  const schemasIndex = ref.indexOf("/schemas/");
  if (schemasIndex !== -1) {
    const remainder = ref.slice(schemasIndex + "/schemas/".length);
    const [name] = remainder.split("/");
    return name || null;
  }
  const fallback = ref.split("/").pop();
  return fallback && fallback !== "#" ? fallback : null;
}

export default async function ApiComponents({ params }: { params: Promise<{ apiSlug: string }> }) {
  const { apiSlug } = await params;
  const [components, routes] = await Promise.all([listComponents(apiSlug), listRoutes(apiSlug)]);

  const requiredNames = new Set<string>();
  const usageAccumulator: Record<string, { request: number; response: number }> = {};
  const routesPerComponent: Record<string, Set<string>> = {};

  const ensureUsage = (component: string) => {
    if (!usageAccumulator[component]) {
      usageAccumulator[component] = { request: 0, response: 0 };
    }
    if (!routesPerComponent[component]) {
      routesPerComponent[component] = new Set();
    }
    return usageAccumulator[component];
  };

  for (const route of routes) {
    const requestComponent = extractComponentName(route.request_body_ref);
    const responseComponent = extractComponentName(route.response_body_ref);
    const routeKey = `${route.method.toUpperCase()} ${route.path}`;

    if (requestComponent) {
      requiredNames.add(requestComponent);
      const usage = ensureUsage(requestComponent);
      usage.request += 1;
      routesPerComponent[requestComponent]?.add(routeKey);
    }

    if (responseComponent) {
      requiredNames.add(responseComponent);
      const usage = ensureUsage(responseComponent);
      usage.response += 1;
      routesPerComponent[responseComponent]?.add(routeKey);
    }
  }

  const usageByComponent: Record<string, ComponentUsage> = {};
  for (const [name, usage] of Object.entries(usageAccumulator)) {
    const total = routesPerComponent[name]?.size ?? 0;
    usageByComponent[name] = { request: usage.request, response: usage.response, total };
  }

  const optionalComponentNames = components
    .filter((component) => !requiredNames.has(component.component_name))
    .map((component) => component.component_name);
  const unusedCount = optionalComponentNames.length;

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
      <p className="text-sm text-gray-600">
        Components marked with * are not referenced by any route.
        {unusedCount > 0
          ? ` ${unusedCount} optional component${unusedCount === 1 ? " is" : "s are"} available.`
          : ""}
      </p>
      <ComponentsFilterList
        components={components}
        apiSlug={apiSlug}
        usageByComponent={usageByComponent}
        optionalComponents={optionalComponentNames}
      />
    </main>
  );
}
