import logging
from datetime import datetime, timedelta

from werkzeug.exceptions import Forbidden
from werkzeug.urls import url_quote

from odoo import http, fields
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class BusPortalController(http.Controller):

    # ------------------------------------------------------------------
    # Route A: GET /bus/trips — Public trip search & listing
    # ------------------------------------------------------------------
    @http.route('/bus/trips', type='http', auth='public', website=True)
    def trip_search(self, origin=None, destination=None, date=None, **kw):
        domain = [('state', '=', 'scheduled')]

        if origin:
            domain.append(('route_id.origin', 'ilike', origin))
        if destination:
            domain.append(('route_id.destination', 'ilike', destination))

        if date:
            try:
                day = fields.Date.to_date(date)
            except ValueError:
                day = fields.Date.context_today(request.env)
            day_start = datetime.combine(day, datetime.min.time())
            day_end = datetime.combine(day + timedelta(days=1), datetime.min.time())
            domain.append(('departure_datetime', '>=', fields.Datetime.to_string(day_start)))
            domain.append(('departure_datetime', '<', fields.Datetime.to_string(day_end)))
        else:
            domain.append(('departure_datetime', '>=', fields.Datetime.now()))

        trips = request.env['bus.trip'].sudo().search(domain, order='departure_datetime')

        origins = request.env['bus.route'].sudo().search([]).mapped('origin')
        destinations = request.env['bus.route'].sudo().search([]).mapped('destination')

        values = {
            'trips': trips,
            'origins': sorted(set(origins)),
            'destinations': sorted(set(destinations)),
            'search_origin': origin or '',
            'search_destination': destination or '',
            'search_date': date or '',
        }
        return request.render('bus_booking.portal_trip_search', values)

    # ------------------------------------------------------------------
    # Route B: GET /bus/trip/<trip_id> — Trip detail + seat map
    # ------------------------------------------------------------------
    @http.route('/bus/trip/<int:trip_id>', type='http', auth='public', website=True)
    def trip_detail(self, trip_id, error=None, **kw):
        trip = request.env['bus.trip'].sudo().browse(trip_id)
        if not trip.exists():
            return request.render('website.404')

        seats = trip.trip_seat_ids

        user = request.env.user
        is_logged_in = not user._is_public()

        values = {
            'trip': trip,
            'seats': seats,
            'is_logged_in': is_logged_in,
            'error': error,
        }
        return request.render('bus_booking.portal_trip_detail', values)

    # ------------------------------------------------------------------
    # Route C: POST /bus/trip/<trip_id>/book — Create booking (auth user)
    # ------------------------------------------------------------------
    @http.route('/bus/trip/<int:trip_id>/book', type='http',
                auth='user', website=True, methods=['POST'], csrf=True)
    def trip_book(self, trip_id, **post):
        trip = request.env['bus.trip'].sudo().browse(trip_id)
        if not trip.exists():
            return request.render('website.404')

        selected_seat_ids = request.httprequest.form.getlist('selected_seats')
        if not selected_seat_ids:
            error = 'Please select at least one seat to book.'
            return request.redirect(
                '/bus/trip/%d?error=%s' % (trip_id, url_quote(error))
            )

        try:
            seat_ids = [int(s) for s in selected_seat_ids]
        except (ValueError, TypeError):
            error = 'Invalid seat selection. Please try again.'
            return request.redirect(
                '/bus/trip/%d?error=%s' % (trip_id, url_quote(error))
            )

        seats = request.env['bus.trip.seat'].sudo().browse(seat_ids)
        invalid = seats.filtered(lambda s: s.trip_id.id != trip_id)
        if invalid:
            error = 'Some selected seats are invalid for this trip.'
            return request.redirect(
                '/bus/trip/%d?error=%s' % (trip_id, url_quote(error))
            )

        try:
            booking = request.env['bus.booking'].sudo().create({
                'customer_id': request.env.user.partner_id.id,
                'trip_id': trip_id,
                'booking_seat_ids': [(6, 0, seat_ids)],
            })
            booking.sudo().action_confirm()
        except ValidationError as e:
            _logger.info(
                'Portal booking failed for user %s on trip %d: %s',
                request.env.user.login, trip_id, str(e),
            )
            error_msg = str(e) if str(e) else (
                'The selected seats are no longer available. '
                'Please go back and choose different seats.'
            )
            return request.redirect(
                '/bus/trip/%d?error=%s' % (trip_id, url_quote(error_msg))
            )
        except Exception:
            _logger.exception('Unexpected error during portal booking')
            return request.redirect(
                '/bus/trip/%d?error=%s' % (
                    trip_id,
                    url_quote('An unexpected error occurred. Please try again.'),
                )
            )

        return request.redirect('/my/bus-bookings/%d' % booking.id)

    # ------------------------------------------------------------------
    # Route D: GET /my/bus-bookings — Portal "My Bookings" listing
    #         GET /my/bus-bookings/<booking_id> — Booking detail
    # ------------------------------------------------------------------
    @http.route(['/my/bus-bookings', '/my/bus-bookings/<int:booking_id>'],
                type='http', auth='user', website=True)
    def my_bookings(self, booking_id=None, error=None, success=None, **kw):
        user = request.env.user

        if booking_id:
            booking = request.env['bus.booking'].sudo().browse(booking_id)
            if (not booking.exists()
                    or booking.customer_id != user.partner_id):
                return request.render('website.404')

            invoice_url = False
            if booking.invoice_id:
                invoice_url = '/my/invoices/%d' % booking.invoice_id.id

            ticket_url = (
                '/report/pdf/bus_booking.report_bus_ticket/%d'
                % booking.id
            )

            values = {
                'booking': booking,
                'invoice_url': invoice_url,
                'ticket_url': ticket_url,
                'error': error,
                'success': success,
            }
            return request.render('bus_booking.portal_booking_detail', values)

        bookings = request.env['bus.booking'].search([
            ('customer_id', '=', user.partner_id.id),
        ], order='create_date desc')

        values = {
            'bookings': bookings,
        }
        return request.render('bus_booking.portal_my_bus_bookings', values)

    # ------------------------------------------------------------------
    # Route E: POST /my/bus-bookings/<booking_id>/cancel — Self-service
    #          cancellation (auth user). Ownership is verified server-side
    #          BEFORE any action_cancel() call.
    # ------------------------------------------------------------------
    @http.route('/my/bus-bookings/<int:booking_id>/cancel', type='http',
                auth='user', website=True, methods=['POST'], csrf=True)
    def booking_cancel(self, booking_id, **post):
        user = request.env.user
        booking = request.env['bus.booking'].sudo().browse(booking_id)

        # Real server-side ownership check: a booking can only be cancelled
        # by the partner who owns it, never by browsing/hand-crafting a POST.
        if (not booking.exists()
                or booking.customer_id.id != user.partner_id.id):
            raise Forbidden()

        if booking.state != 'confirmed':
            error_msg = (
                'This booking can no longer be cancelled. Only confirmed '
                'bookings can be cancelled.'
            )
            return request.redirect(
                '/my/bus-bookings/%d?error=%s' % (booking_id, url_quote(error_msg))
            )

        try:
            booking.sudo().action_cancel()
        except ValidationError as e:
            _logger.info(
                'Portal cancellation failed for user %s on booking %s: %s',
                user.login, booking.name, str(e),
            )
            error_msg = str(e) or (
                'The booking could not be cancelled. Please try again.'
            )
            return request.redirect(
                '/my/bus-bookings/%d?error=%s' % (booking_id, url_quote(error_msg))
            )
        except Exception:
            _logger.exception('Unexpected error during portal cancellation')
            return request.redirect(
                '/my/bus-bookings/%d?error=%s' % (
                    booking_id,
                    url_quote('An unexpected error occurred. Please try again.'),
                )
            )

        return request.redirect('/my/bus-bookings/%d?success=1' % booking_id)
