"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { ComponentMeta } from "@/lib/api";

type ComponentUsage = {
  total: number;
  request: number;
  response: number;
};

type Props = {
  components: ComponentMeta[];
  apiSlug: string;
  usageByComponent?: Record<string, ComponentUsage>;
  optionalComponents?: string[];
};

export default function ComponentsFilterList({
  components,
  apiSlug,
  usageByComponent,
  optionalComponents,
}: Props) {
  const optionalSet = useMemo(
    () => new Set(optionalComponents ?? []),
    [optionalComponents]
  );
  const [query, setQuery] = useState("");

  const normalizedQuery = query.trim().toLowerCase();
  const filtered = useMemo(() => {
    const base = !normalizedQuery
      ? components
      : components.filter((c) => {
          const name = c.component_name.toLowerCase();
          const key = (c.storage_key || "").toLowerCase();
          return name.includes(normalizedQuery) || key.includes(normalizedQuery);
        });

    return [...base].sort((a, b) => {
      if (b.property_count !== a.property_count) return b.property_count - a.property_count;
      return a.component_name.localeCompare(b.component_name);
    });
  }, [components, normalizedQuery]);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search components by name or storage key"
          className="w-full max-w-xl rounded border px-3 py-2 shadow-sm focus:outline-none focus:ring focus:border-blue-500"
        />
        <div className="text-sm text-gray-600 whitespace-nowrap">
          Showing {filtered.length} of {components.length} component{components.length === 1 ? "" : "s"}
        </div>
      </div>

      {filtered.length === 0 ? (
        <p className="text-gray-600">No matching components.</p>
      ) : (
        <ul className="divide-y divide-gray-200 rounded border">
          {filtered.map((c) => {
            const usage = usageByComponent?.[c.component_name];
            const total = usage?.total ?? 0;
            const detailParts: string[] = [];
            if ((usage?.request ?? 0) > 0) {
              detailParts.push(`request: ${usage.request}`);
            }
            if ((usage?.response ?? 0) > 0) {
              detailParts.push(`response: ${usage.response}`);
            }
            const usageDetail = detailParts.length > 0 ? ` (${detailParts.join(", ")})` : "";
            const usageText =
              total > 0
                ? ` • Used by ${total} route${total === 1 ? "" : "s"}${usageDetail}`
                : " • Not referenced by any route";
            return (
              <li key={c.component_name} className="p-4 flex items-center justify-between">
                <div>
                  <div className="font-medium">
                    {c.component_name}
                    {optionalSet.has(c.component_name) ? "*" : ""}
                  </div>
                  <div className="text-sm text-gray-600">
                    {c.storage_key ?? "n/a"} • {c.property_count} properties{usageText}
                  </div>
                </div>
                <Link
                  className="text-blue-600 hover:underline"
                  href={`/apis/${encodeURIComponent(apiSlug)}/components/${encodeURIComponent(c.component_name)}`}
                >
                  View details
                </Link>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
