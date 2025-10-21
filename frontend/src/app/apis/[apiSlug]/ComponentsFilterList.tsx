"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { ComponentMeta } from "@/lib/api";

type Props = {
  components: ComponentMeta[];
  apiSlug: string;
};

export default function ComponentsFilterList({ components, apiSlug }: Props) {
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
          Showing {filtered.length} of {components.length}
        </div>
      </div>

      {filtered.length === 0 ? (
        <p className="text-gray-600">No matching components.</p>
      ) : (
        <ul className="divide-y divide-gray-200 rounded border">
          {filtered.map((c) => (
            <li key={c.component_name} className="p-4 flex items-center justify-between">
              <div>
                <div className="font-medium">{c.component_name}</div>
                <div className="text-sm text-gray-600">{c.storage_key} • {c.property_count} properties</div>
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
    </div>
  );
}


