# Bus Booking & Ticketing System — Odoo 19

A custom Odoo 19 module for intercity bus ticket booking, modeled on real-world
operators like Faisal Movers. Covers route/vehicle master data, trip scheduling ,
seat-level booking with double-booking prevention, invoicing, and reporting.

Built as a professional, deployable project — not a demo module.

---

## 1. Project Overview

| | |
|---|---|
| **Platform** | Odoo 19 (Community) |
| **Language** | Python 3, XML (views), QWeb (reports) |
| **Database** | PostgreSQL |
| **Module name** | `bus_booking` |
| **Location in repo** | `custom_addons/bus_booking/` |
| **Status** | In development — MVP phase |
| **Full spec** | See [`docs/Bus_Booking_System_Proposal.docx`](docs/Bus_Booking_System_Proposal.docx) |

---

## 2. Core Business Flow

```
Route  →  Vehicle  →  Trip (Route + Vehicle + Date/Time)  →  Booking (Seat + Customer)
```

1. **Route** — origin, destination, distance, base fare.
2. **Vehicle** — a bus with a fixed seat layout/capacity.
3. **Trip** — a scheduled journey: specific vehicle + route + departure date/time.
4. **Booking** — a customer reserving a specific seat on a specific trip.

A confirmed booking automatically generates an invoice and a printable PDF ticket.

---

## 3. Data Models

| Model | Purpose | Key Fields |
|---|---|---|
| `bus.route` | Master data for city-to-city routes | `origin`, `destination`, `distance`, `base_fare` |
| `bus.vehicle` | A physical bus | `name`, `registration_no`, `total_seats`, `type` |
| `bus.seat` | Individual seat linked to a vehicle | `seat_number`, `seat_type`, `vehicle_id` |
| `bus.trip` | A scheduled journey instance | `route_id`, `vehicle_id`, `departure_datetime`, `driver_id`, `state` |
| `bus.booking` | Core transactional record | `customer_id`, `trip_id`, `seat_ids`, `fare`, `payment_status`, `state` |

**Critical rule:** a seat can only belong to one active (non-cancelled) booking per
trip. Enforced via `@api.constrains` at the model layer — not just UI validation —
so it holds under concurrent booking attempts.

---

## 4. Scope

### MVP (current focus)
- Routes, Vehicles, Seats, Drivers (master data)
- Trip scheduling with auto-generated seat availability
- Seat booking with double-booking prevention
- Auto-invoicing on confirmed booking
- Role-based security (Booking Agent / Manager / Administrator)
- Printable PDF ticket + basic revenue report
- Live deployment (not localhost-only)

### Extended / Phase 2
- Online payment gateway (JazzCash / EasyPaisa / Stripe test mode)
- Customer self-service portal (search, seat map, book & pay)
- SMS/Email booking confirmations and reminders
- Multi-branch / multi-company support
- Occupancy & route profitability dashboards
- Automated test suite

---

## 5. Security Groups

| Role | Access |
|---|---|
| Booking Agent | Create/view bookings only |
| Terminal Manager | Manage routes, vehicles, trips; view bookings & reports |
| Administrator | Full access — config, security, financial reports |
| Portal Customer (Phase 2) | View own bookings; create bookings via portal |

---

## 6. Repository Structure

```
bus-booking-odoo19/
├── README.md
├── docs/
│   └── Bus_Booking_System_Proposal.docx
└── custom_addons/
    └── bus_booking/
        ├── __init__.py
        ├── __manifest__.py
        ├── models/
        │   ├── bus_route.py
        │   ├── bus_vehicle.py
        │   ├── bus_seat.py
        │   ├── bus_trip.py
        │   └── bus_booking.py
        ├── views/
        │   ├── bus_route_views.xml
        │   ├── bus_vehicle_views.xml
        │   ├── bus_trip_views.xml
        │   └── bus_booking_views.xml
        ├── security/
        │   ├── security_groups.xml
        │   └── ir.model.access.csv
        ├── reports/
        │   └── bus_ticket_report.xml
        └── static/
            └── description/
                └── icon.png
```

---

## 7. Local Setup

```bash
# 1. Clone the repo
git clone <repo-url> bus-booking-odoo19
cd bus-booking-odoo19

# 2. Point your Odoo instance's addons_path to custom_addons/
#    In odoo.conf:
#    addons_path = /path/to/odoo/addons,/path/to/bus-booking-odoo19/custom_addons

# 3. Restart Odoo and update the apps list, then install "Bus Booking"
```

---

## 8. Development Notes (for AI coding agents)

- Follow Odoo 19 ORM conventions — no deprecated API patterns from older versions.
- Every business rule that affects data integrity (e.g. seat availability) must be
  enforced with `@api.constrains` or SQL constraints, not only in views.
- Keep models in `models/`, one file per model, registered in `models/__init__.py`.
- Security: every new model needs a matching row in `ir.model.access.csv` and, where
  relevant, a record rule scoped to the correct security group.
- Reports go through QWeb (`reports/`), not external PDF libraries.
- Reference `docs/Bus_Booking_System_Proposal.docx` for full scope, phase breakdown,
  and success criteria before implementing a new phase.

---

## 9. Delivery Phases

| Phase | Deliverable |
|---|---|
| 1 | Master Data models (Route, Vehicle, Seat) |
| 2 | Trip Scheduling + seat availability generation |
| 3 | Booking logic + double-booking prevention + invoicing |
| 4 | Security groups + printable ticket report |
| 5 | Dashboard + operational reports |
| 6 | Live deployment (MVP goes live) |
| 7 | Extended features — payments, portal, notifications |

---

## License

Private / commercial project — not for public redistribution.