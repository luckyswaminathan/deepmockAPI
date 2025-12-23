# Reverse Engineering Plan for `sample_api`

**Total Routes:** 2
**Generated At:** 2025-12-23T01:05:51.684162+00:00

## Agent Directives
1. Review the component summary below to understand the CRUD surface.
2. Use component-specific plans in `plan/components/` for detailed route information.
3. Implement server handlers that satisfy the described operations and filters.
4. Raise any ambiguities called out in validation warnings before coding.

## Component Summary

Each component below has a dedicated plan file in `plan/components/` with detailed route information.

| Component | Operations | Route Count | Plan File |
|-----------|------------|-------------|-----------|
| `Order` | `read_one` | 1 | `plan/components/order.md` |
| `OrderList` | `read_many` | 1 | `plan/components/orderlist.md` |

## Quick Stats

**Operations by Type:**
- `read_one`: 1 routes
- `read_many`: 1 routes

**Routes by Status:**
- `planned`: 2 routes

---

**Note:** For detailed route-by-route information, see individual component plan files in `plan/components/`.
