# External Python dependency for the Phase 8 offline FAQ chatbot.
# Install once into the Odoo Python environment with:
#   pip install scikit-learn --break-system-packages
# See requirements.txt at the module root. NOT auto-installed by Odoo.
{
    'name': 'Bus Booking System',
    'summary': 'Intercity bus route, trip, and seat booking management',
    'description': """
        Bus Booking System
        ===================
        Manage intercity bus operations with ease.

        * Routes — define origin, destination, distance, and base fare
        * Vehicles — register buses with type (AC/Non-AC) and seat layout
        * Seats — auto-generate seat maps per vehicle
        * Drivers — maintain driver profiles and licenses

        This module provides the master data foundation for trip scheduling,
        seat-level booking, and invoicing (coming in future phases).
    """,
    'author': 'Faraz Bashir',
    'category': 'Operations/Fleet',
    'sequence': -100,
    'version': '19.0.1.0.0',
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'account', 'website', 'portal', 'auth_signup'],
    'data': [
        'security/bus_booking_security.xml',
        'security/ir.model.access.csv',
        'data/bus_booking_sequence.xml',
        'data/website_menu_data.xml',
        'data/website_pages.xml',
        'views/bus_route_views.xml',
        'views/bus_vehicle_views.xml',
        'views/bus_seat_views.xml',
        'views/bus_driver_views.xml',
        'views/bus_trip_views.xml',
        'views/bus_trip_seat_views.xml',
        'reports/bus_ticket_report.xml',
        'views/bus_booking_views.xml',
        'views/bus_booking_report_views.xml',
        'views/bus_trip_report_views.xml',
        'views/bus_booking_menus.xml',
        'views/portal_booking_templates.xml',
        'views/chatbot_widget_template.xml',
    ],
    'demo': [],
    'assets': {
        'web.assets_frontend': [
            'bus_booking/static/src/css/chatbot_widget.css',
            'bus_booking/static/src/js/chatbot.js',
        ],
    },
    'images': ['static/description/icon.png'],
    'website': False,
}
