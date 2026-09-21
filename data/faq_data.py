# -*- coding: utf-8 -*-
"""Offline FAQ knowledge base for the Bus Booking customer portal.

Plain Python module (NOT an Odoo model). It contains the fixed list of
FAQ (question, answer) tuples that the Phase 8 chatbot is allowed to
answer from. The chatbot NEVER generates free-form answers - it only
retrieves one of these answers when the user's question is similar
enough to the matching question, and otherwise replies with a fallback
message asking the user to contact the support desk.

This is a module-level singleton: the chatbot builds its TF-IDF model
once per worker process and caches it in memory.

Exactly 200 entries across the categories marked below.
"""

FAQ_DATA = [
    # ------------------------------------------------------------------
    # Booking process
    # ------------------------------------------------------------------
    ("How do I book a bus ticket or make a booking?", "You can search for available trips on the Find Trips page, choose your origin, destination and travel date, then open a trip and select your seats. Once you confirm, your booking is created and you can view it under My Bus Bookings."),
    ("How do I search for trips?", "Open the Find Trips page, enter your origin, destination and travel date, then press Search. A list of scheduled trips with fares and available seats will be shown - click View Details on any trip to open its seat map."),
    ("How do I select my seats?", "On the trip detail page you will see the bus seat map. Click on the seats you want - available seats are green - and then press the Book Selected Seats button. Your chosen seats will be highlighted in blue."),
    ("How do I confirm my booking?", "After selecting your seats, press Book Selected Seats. Your booking is created immediately and shown as Confirmed. You will find it under My Bus Bookings with the ticket download link."),
    ("Can I book a ticket for someone else?", "Yes. When booking, the seat is reserved under your portal account, and anyone travelling can board using the ticket reference. Seat names are not printed on the ticket, so you can book for family or friends."),
    ("What is the minimum number of seats I can book?", "You can book a single seat as a minimum. Select just one available seat on the trip detail page and confirm."),
    ("What is the maximum number of seats per booking?", "There is no fixed maximum, but all seats must be available on the same trip. If you need a large group, it is safer to book early because seats are limited and are reserved on a first-come, first-served basis."),
    ("Can I book without creating an account?", "Trip browsing is open to everyone, but to confirm a booking you must log in. Creating a free portal account lets you keep your booking history, invoices and tickets in one place."),
    ("Do I need to pay at the time of booking?", "No. There is no online payment yet - you pay in cash at the counter or when boarding. Your confirmed seat is held for you and you simply pay before or during the journey."),
    ("How long does a booking take?", "The whole process takes less than a minute. Search for your trip, pick your seats and confirm - your booking reference is shown immediately."),
    ("Can I change my trip after booking?", "Bookings cannot be edited directly online. Please cancel the existing booking and make a new one, and contact our support desk if you need help with a change."),
    ("Can I book for a child or infant?", "Children occupy regular seats and are booked exactly like adults. For very young children who will sit on a guardian's lap, contact the terminal to confirm the policy for your route."),
    ("How do I know my booking is confirmed?", "Your booking shows the Confirmed status immediately after you press the booking button, and the ticket becomes available to download from My Bus Bookings."),
    ("Can I book seats on different trips at once?", "No, each booking belongs to a single trip. If you need several connections, create a separate booking for each trip."),
    ("Is there a booking fee?", "There is no extra booking fee. You only pay the fare of the seats you reserve, either at the counter or on boarding."),
    ("How do I reserve or book a seat on a trip?", "A seat is only reserved after the booking is confirmed. Until you press the final button, the seats you clicked are not held for you and can be taken by someone else."),
    ("What information do I need to book?", "Only your portal account. The trip is booked under your name and your booking reference is used to collect your ticket at the terminal."),
    ("Can I book from my mobile phone?", "Yes. The trip search, seat selection and booking pages work fully on mobile browsers, so you can book from your phone anywhere."),
    ("How do I book a return trip?", "Book each direction separately - search once for your outbound journey and once for the return. You will get a booking reference and ticket for each leg."),
    ("Can agents book on my behalf?", "Yes. Licensed booking agents at the terminal can create bookings for you. In the portal you can also book a ticket and simply give the reference to whoever is travelling."),
    ("What happens if I book twice by mistake?", "If you create two bookings for the same trip you will get two booking references. You can cancel one of them - cancellation rules and refund terms will apply based on how close to departure you cancel."),
    ("How far in advance can I book?", "Trips open for booking as soon as they are scheduled. You can reserve your seat days or even weeks before the travel date, subject to seat availability on your chosen trip."),

    # ------------------------------------------------------------------
    # Payment
    # ------------------------------------------------------------------
    ("Is online payment available?", "No. Online payment is not available at the moment. You pay in cash at the counter or on boarding - there is no payment gateway on this platform yet."),
    ("How do I pay for my booking?", "Payment is by cash, either at the terminal counter before departure or directly to the conductor when you board. Keep your booking reference handy to identify your reservation."),
    ("Is payment mandatory to reserve a seat?", "Your seat is reserved when the booking is confirmed, and we hold it on good faith for you. Payment is expected at the counter or on boarding on the travel day."),
    ("What happens if I do not pay?", "Unpaid seats may be released for resale shortly before departure, especially when the trip is close to full. To be safe, pay at the counter as early as possible."),
    ("Can I pay before boarding, or at the counter when I get on the bus?", "Yes, our conductors accept cash on board. The fare is the same as at the counter - there is no extra charge for paying during the trip."),
    ("Can I get a payment receipt?", "Please ask the conductor or the terminal counter for a receipt when you pay. The booking confirmation in your portal account also shows the fare details."),
    ("Are there any extra charges on payment?", "No hidden charges. You pay exactly the fare shown on the trip page - the amount you see when confirming your booking."),
    ("Can I pay in cash?", "Yes, all payments are currently cash based - either at the counter or to the conductor on board. Digital payment methods are planned for a future phase."),
    ("Which payment methods do you accept?", "Cash at the counter or cash on board. We do not accept cards, mobile wallets or bank transfers yet - online payment is coming in a future phase."),
    ("Will my card be charged automatically?", "No. We never ask for card details and there is no automatic charge on this platform. All payments are in cash at the counter or on board."),
    ("Do I need to pay for luggage?", "Normal luggage within the allowance is included in your fare. Only excess or oversized baggage may attract an extra charge - confirm at the counter before travel."),
    ("Can someone else pay on my behalf?", "Yes. The person travelling does not have to be the one who pays - any cash payment at the counter will be matched to your booking reference."),
    ("How do I know my payment was received?", "The counter or conductor will confirm your payment and you will receive a receipt. Your booking remains confirmed for boarding once payment is recorded."),
    ("Can I pay later at the terminal?", "Yes, you can pay at the terminal before departure. Please arrive a little earlier if you plan to pay at the counter rather than on board."),
    ("Is there a discount for early payment?", "Currently the fare is the same whether you pay early or on board. Special promotional fares are shown directly on the trip page when available."),
    ("Do receipts include tax?", "The ticket fare includes all applicable taxes on the intercity route. For a detailed breakdown, request the official invoice from our accounts desk."),
    ("Can I get an advance booking on credit?", "Bookings are made in good faith with payment at boarding. Company or corporate accounts can arrange credit terms - please contact our accounts department."),
    ("What currency do you charge in?", "All fares are quoted and payable in Pakistani Rupees (PKR). The fare shown on the trip page is the total amount you will pay."),
    ("Can I pay through a mobile wallet?", "Not yet. Mobile wallet and card payments are planned but currently payments are cash only at the counter or on board."),

    # ------------------------------------------------------------------
    # Cancellation & refunds
    # ------------------------------------------------------------------
    ("Can I cancel my booking?", "Yes. Go to My Bus Bookings, open the booking and use the cancel option, or ask our support desk or the terminal counter to cancel it for you."),
    ("How do I cancel a booking?", "From My Bus Bookings, open the booking you want to cancel and press cancel. The seats are released immediately and your booking moves to Cancelled status."),
    ("Is there a cancellation deadline?", "Cancellations are generally accepted up to a few hours before departure. Check with our support desk for the exact cutoff time for your trip - last minute cancellations may not be possible."),
    ("Can I cancel just before departure?", "Cancellations very close to departure are difficult because the seats may already be issued to the trip manifest. Please contact the terminal as soon as you know you cannot travel."),
    ("Do I get a refund after cancelling?", "Refunds depend on when you cancel. Early cancellations qualify for a full return of your fare; closer to departure a cancellation fee may apply."),
    ("How long does a refund take?", "Approved refunds are processed quickly by our accounts desk. Since all payments are cash based, refunds are usually paid back in cash at the terminal."),
    ("Can I get a full refund?", "If you cancel well before the departure time, yes - your full fare is returned. Cancelling closer to departure may be subject to a cancellation charge."),
    ("What if the operator cancels the bus?", "If a trip is cancelled by the operator, you are entitled to a full refund of your fare, or you can transfer your booking to another departure at no extra charge."),
    ("Can I transfer my ticket to another passenger?", "Yes, tickets are transferable - the new passenger simply travels using the same booking reference. If names are required, update the details with our support desk."),
    ("Can I change my travel date instead of cancelling?", "We recommend cancelling and rebooking to your new date, so the seats are released correctly. For transfers to the same route, ask our support desk and we will try to help."),
    ("Are cancellation charges applied?", "Yes, a small cancellation fee may apply when you cancel close to departure. Cancellations made well in advance are generally free of charge."),
    ("Can I cancel at the terminal?", "Yes, the terminal counter can cancel your booking and, where applicable, settle your refund in cash on the spot."),
    ("What happens to cancelled seat availability?", "When a booking is cancelled, its seats are released immediately and become available for other customers to book on the trip page."),
    ("Can I cancel an agent booking myself?", "If the booking is linked to your portal account it shows in My Bus Bookings and you can cancel it yourself. Otherwise, contact the counter that issued it."),
    ("Do refunds go back to my original payment method?", "Since payments are cash based, refunds are returned in cash at the terminal. There is no card or wallet refund because there is no digital payment yet."),
    ("Can I rebook with the refund amount?", "Yes. If you cancel and receive a cash refund, you can immediately use that amount to book a different trip at the counter."),
    ("What if I miss my bus?", "A missed departure is treated as no-show and the fare is generally not refundable. Contact the terminal immediately - they may rebook you on a later trip if seats are free."),
    ("Can I cancel part of my seats only?", "Yes, a partial cancellation is possible - cancel the booking through support and keep the seats you still need by rebooking them on the same trip if available."),
    ("Who do I contact for refund issues?", "Visit the terminal counter or contact our support desk with your booking reference. Our team will verify the cancellation and arrange the refund."),
    ("How will I know my refund is processed?", "Once the refund is approved and paid, the booking is updated to reflect the cancellation and you receive confirmation from our team or the counter."),
    ("Is insurance available for cancellations?", "Travel insurance for bus trips is not currently offered. We recommend contacting our support desk early if you think you may need to cancel."),

    # ------------------------------------------------------------------
    # Seats
    # ------------------------------------------------------------------
    ("How are seats numbered?", "Seats are numbered from the front of the bus, usually starting at 1 on the window side of the first row and alternating between window and aisle positions as you go back."),
    ("What is the difference between window and aisle seats?", "Window seats sit next to the window and give you a view and a wall to lean on. Aisle seats are on the walkway side and make it easier to stand up and move around."),
    ("Can I choose a specific seat?", "Yes. On the trip detail page, use the seat map to select exactly which seat numbers you want before confirming your booking."),
    ("What if my chosen seat is already taken?", "Seats already booked appear grey and blocked on the seat map and cannot be selected. You simply choose another available seat."),
    ("How do I read the seat map?", "Green buttons on the seat map are available seats you can click, grey are already booked, and red are blocked or out of service. Each button shows the seat number and whether it is window or aisle."),
    ("What does a blocked seat mean?", "A blocked seat is one that cannot be sold for this trip - it may be reserved by the operator, out of service, or held for staff. It appears red on the seat map."),
    ("Can I ask for a front seat?", "Front seats are shown on the seat map like any other seat. If a front seat is available, you can select it directly - otherwise choose the next available one."),
    ("Are there reserved seats for women?", "Some trips reserve a ladies' section near the front. If the seat map shows such seats, they are labelled or limited - please contact our support desk for the current policy."),
    ("How many seats does a bus have?", "Our standard coaches typically have 44 to 50 seats depending on the model and whether the bus is AC or Non-AC. The exact number is shown on the trip detail page."),
    ("Can I book a pair of seats together?", "Yes. When available, select two adjacent seats on the seat map at the same time and book them together in one booking."),
    ("What if my seat is dirty or damaged?", "Please inform the conductor before departure so the seat can be changed if possible. If the bus leaves with an issue, report it on arrival and our team will follow up."),
    ("Can I sit on an empty seat after departure?", "No. Passengers must use the seat they booked. If you wish to move, ask the conductor first - they may reassign an empty seat when the manifest has free space."),
    ("How do I find my seat number?", "Your seat numbers are listed on your ticket and in My Bus Bookings. The conductor will also guide you to your seat when you board."),
    ("Can I change my seat at the terminal?", "If you want a different seat, ask the counter before departure. Available seats can be reassigned on the spot; already booked seats cannot be swapped."),
    ("Do seats recline?", "Our AC coaches have gently reclining seats for extra comfort. Non-AC coaches have semi-reclining seats. Recline gently so you do not disturb the passenger behind you."),
    ("Are there seats for children?", "Children occupy normal seats like adults on the manifest. For infants who travel on a guardian's lap, please check the child policy at the terminal."),
    ("Can two people share one seat?", "No, every passenger needs their own seat on the bus. Book one seat per traveller so the manifest and safety count are correct."),
    ("What is the seat spacing like?", "Our intercity coaches offer generous legroom, especially on AC services. Seat pitch varies slightly by bus model - generally enough for a comfortable long journey."),
    ("Can I request a specific row?", "Specific rows are not reserved by request. You can try selecting a front row on the seat map - if it is free, it is yours."),
    ("What if I have a problem with my seat?", "Tell the conductor on boarding - they will help swap you to a free seat if one exists. For serious issues, our support desk will follow up after the trip."),

    # ------------------------------------------------------------------
    # Tickets
    # ------------------------------------------------------------------
    ("How do I get my ticket?", "After confirming your booking, your ticket is available instantly under My Bus Bookings. Open the booking and press Download Ticket to get the PDF."),
    ("Can I print my ticket?", "Yes. Download the PDF ticket and print it, or simply show the digital version on your phone - both are accepted at boarding."),
    ("Do I need to show ID to board?", "Your booking reference is the main check. However, a valid government ID is required to match the passenger details and for safety verification on several routes."),
    ("What if I lose my ticket?", "Your booking is stored in your portal account, so you can re-download it any time from My Bus Bookings. The conductor can also verify your reference on board."),
    ("Can I show my ticket on my phone?", "Yes, the digital PDF ticket on your phone is fully accepted. Keep the screen bright and the QR code or reference visible for the conductor."),
    ("What information is on my ticket?", "The ticket shows your booking reference, route, departure date and time, seat numbers, fare, and the bus details. It is your proof of travel for this trip."),
    ("Can I get a physical ticket at the counter?", "Yes, present your booking reference at the terminal counter and they will issue a printed ticket if you prefer a physical copy."),
    ("Do I need to show my ticket while boarding?", "Yes, the conductor checks tickets or booking references before boarding. Have your ticket or reference ready to speed up the process."),
    ("Can I share my ticket with someone else?", "Yes - tickets are transferable. The person travelling presents the reference and a valid government ID. You do not need to transfer the ticket in any way."),
    ("Is a ticket needed for a child?", "Children travelling in their own seat need their own ticket. Lap-held infants follow the infant policy - confirm with the terminal before boarding."),
    ("What if my ticket is damaged?", "A damaged paper ticket can be verified using your booking reference. If you used a printed copy, simply show the digital version instead."),
    ("Can I e-mail my ticket to someone?", "You can download the PDF from My Bus Bookings and attach it to an e-mail yourself. The ticket is a normal PDF and travels as an attachment."),
    ("How do I download my ticket again?", "Log in, open My Bus Bookings, open the relevant booking and press Download Ticket. The latest version is always regenerated for you."),
    ("Do I need a printed copy for boarding?", "No. A mobile ticket or your booking reference at the gate is enough - printing is optional and only for your own convenience."),
    ("Can I request a duplicate ticket?", "Yes - the digital ticket can be downloaded any number of times from your account, so there is no separate duplicate process."),
    ("Is my booking reference the same as my ticket?", "Yes. The booking reference is the unique code that identifies your reservation, and it appears together with the seat numbers on your ticket."),
    ("Can I receive my ticket by e-mail?", "Tickets are available for download in My Bus Bookings immediately after booking. Automatic ticket e-mails are being considered for a future phase."),
    ("What should I do if my ticket is not loading?", "Refresh the page and try again from My Bus Bookings. If it still fails, contact our support desk with your booking reference and we will e-mail you a copy."),

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------
    ("How do I create a portal account?", "On the login page choose the sign up option and register with your e-mail and a password. After verification you can log in and start booking trips."),
    ("How do I reset my password?", "On the login page press the password reset link, enter your registered e-mail and follow the instructions in the reset message to choose a new password."),
    ("How do I view my booking history?", "Once logged in, open My Bus Bookings from the portal. It lists all your bookings with their trip, seats and status, past and upcoming."),
    ("Is my personal data safe?", "Yes. Your contact details are stored securely on our own servers and are only used to manage your bookings and tickets. We do not sell or share your data."),
    ("Can I update my profile details?", "Yes. On the portal home page open your account settings and update your name, e-mail and contact number. Changes apply to new bookings immediately."),
    ("Why do I need an account?", "An account keeps your bookings, tickets and invoices in one place and lets you manage them yourself - including on mobile. It also speeds up repeat booking."),
    ("Can I log in with my mobile number?", "Login is with your registered e-mail and password. If you prefer to log in with your phone number, contact support and we will enable it for your account."),
    ("How do I change my e-mail address?", "Update it in your account settings. Use a working address - it is what we use to send password resets and booking communications."),
    ("I forgot my password, what do I do?", "Use the reset link on the login page. Enter your registered e-mail and you will receive instructions to set a new password in a few minutes."),
    ("Can I have multiple bookings under one account?", "Yes, all bookings you create through the portal are saved under your account in My Bus Bookings, no matter how many you make."),
    ("Is my payment information stored?", "No. Because payments are cash at the counter or on board, we never collect or store card or wallet details on your account."),
    ("Can I delete my account?", "Yes - contact our support desk with a deletion request and we will remove your account and personal data (booking history may be kept for legal records)."),
    ("How do I log out?", "On the portal home page use the logout option in the top right menu. This ends the session on your device."),
    ("Can I share my account access?", "We recommend against sharing passwords. For family bookings, simply book under your account and share the ticket reference with other travellers instead."),
    ("How do I contact support about account issues?", "Use the contact form or helpline numbers on the support page, or ask the terminal counter. Keep your registered e-mail handy for verification."),
    ("Are my tickets linked to my account?", "Yes. Every booking you make is linked to your account, and the tickets are always available to download from My Bus Bookings."),
    ("Can I book as a guest without registering?", "Trip browsing works as a guest, but confirming a booking requires a login so the reservation is saved to an account. Registration takes under a minute."),
    ("Does the account show invoice copies?", "Yes. When a booking is confirmed, the generated invoice is linked to your account and can be accessed from the booking detail page."),
    ("How do I verify my e-mail address?", "After signing up you receive a verification e-mail - click the link inside to confirm your address. Once verified, your account is fully active."),
    ("Can I switch between accounts easily?", "Yes - log out of one account and log in with the other. Each account keeps its own booking history."),

    # ------------------------------------------------------------------
    # Trips & Routes
    # ------------------------------------------------------------------
    ("How do I find available routes?", "On the Find Trips page pick an origin and destination from the dropdowns - only active routes appear. Choose your date and search to see the available trips."),
    ("How early can I book before the trip departs?", "As soon as a trip is scheduled you can book it. Advance booking opens days to weeks before departure depending on how far ahead the schedule is published."),
    ("What if there is no trip on my date?", "If no trip is scheduled for your date, try a neighbouring date or contact our support desk - popular routes add trips based on demand."),
    ("How do I know my boarding point?", "The boarding terminal is shown on the trip detail page. Arrive with enough time and keep your booking reference ready for the gate."),
    ("What is the boarding point or arrival point?", "Your ticket shows both the origin terminal where boarding starts and the destination terminal where the trip arrives. Depart and alight only at these points."),
    ("How early should I arrive at the terminal?", "We recommend arriving at least 30 minutes before departure so the conductor can check you in and load your luggage without stress."),
    ("How much baggage or luggage can I carry on a trip?", "The standard allowance is around 2 medium bags per passenger. Large or excess baggage is subject to an extra charge - confirm at the counter."),
    ("Can I carry extra luggage?", "Extra luggage can be carried for a small charge if there is space in the cargo hold. Book or inform the counter in advance so it is loaded properly."),
    ("Are there trips between Lahore and Karachi?", "Yes, Lahore-Karachi is one of our busiest intercity corridors, with several departures daily on both AC and non-AC coaches."),
    ("How long is the journey?", "Travel time depends on the distance and stops - our typical intercity journeys range from a few hours to around a day for the longest cross-country routes."),
    ("Do trips run every day?", "Most scheduled routes run daily. A few low-demand routes run on alternate days - search by date to see the departures available for your day."),
    ("Are there overnight trips?", "Yes, on longer corridors we operate night coaches so you can travel while you sleep and arrive the next morning."),
    ("Can I board from a pick-up stop?", "Most services board only at the designated terminal. Temporary pick-up points are decided by the operator - contact support for your specific stop."),
    ("How do I find departure times?", "Search your route on the Find Trips page and all upcoming departures with their times, fares and seat availability will be listed."),
    ("How do I check if my trip is on time?", "Contact the terminal or our support desk with your booking reference before leaving and they will confirm the live departure status."),
    ("What if my trip is delayed?", "Minor delays happen on roads. The terminal keeps you informed of the estimated departure. If a trip is cancelled by the operator, you get a full refund or a rebooking."),
    ("Can I book on the day of travel?", "Yes, subject to seat availability. Check the Find Trips page or come to the terminal - remaining seats are bookable up until the departure cutoff."),
    ("How many stops does the bus make?", "Intercity coaches make a small number of scheduled refreshment and restroom stops depending on the route length - usually 1 to 3 for long journeys."),
    ("Are meals provided on long trips?", "Meals are generally not included, but long trips include scheduled refreshment stops at reliable cafes along the highway."),
    ("Can I check trip details like duration and fare?", "Yes - the trip detail page shows the departure time, journey duration, fare per seat and remaining seats for every scheduled departure."),
    ("Are there stops for restrooms?", "Yes, along the intercity highways we stop at secure service areas with clean restrooms and refreshment options."),
    ("Do I need to book to board?", "Yes, seats must be booked - we do not carry standing passengers. Even same-day boarding requires an available booked seat."),
    ("Can I join the trip from the middle?", "Boardings are normally managed at the designated terminals. Special arrangements for en-route boarding are decided at the counter and may not be available."),
    ("What should I do if I miss my boarding point?", "Contact the terminal immediately. If the bus has not left the stop, they may hold or coordinate a pickup; if it has left, they will help with rebooking."),

    # ------------------------------------------------------------------
    # Vehicles
    # ------------------------------------------------------------------
    ("What is the difference between AC and Non-AC coaches?", "AC coaches have fully air-conditioned cabins and more comfortable reclining seats, usually with a slightly higher fare. Non-AC coaches run with open windows and a standard fare."),
    ("Are all buses air conditioned?", "No. The platform runs both AC and Non-AC services. The vehicle type is clearly shown on the trip listing, so you can choose your preference."),
    ("How comfortable are the seats?", "Our AC coaches feature cushioned reclining seats with generous legroom. Non-AC coaches have comfortable semi-reclining seats for the standard fare."),
    ("Do buses have WiFi?", "WiFi is available on select AC coaches. Power outlets and WiFi are indicated on the trip page where the coach supports them."),
    ("Is there a restroom on the bus?", "Most standard coaches do not have onboard restrooms, but long routes include scheduled stops at service areas with clean facilities."),
    ("Do buses have charging points?", "Many AC coaches have USB or power outlets for charging your phone. Check the trip detail page - coaches with charging are clearly marked."),
    ("What is the condition of the buses?", "All coaches are serviced regularly and inspected before every departure. We run a young, well-maintained fleet with comfortable interiors."),
    ("Are the buses new?", "The fleet is continuously updated and all buses are professionally serviced. While models vary by route, every coach meets our comfort and safety standards."),
    ("Are blankets provided on AC buses?", "Yes, blankets and a light pillow are provided on most AC overnight services to keep you comfortable in the cool cabin."),
    ("Can I choose between AC and Non-AC?", "Yes - the vehicle type appears on the trip listing and detail page. Search and pick whichever coach suits your budget and preference."),
    ("Are there luxury or executive coaches?", "On premium corridors we operate executive AC coaches with extra legroom and enhanced amenities. They are labelled on the trip page when available."),
    ("How many seats do the buses have?", "Standard coaches seat between 44 and 50 passengers depending on the model and AC configuration. The exact capacity is shown on the trip page."),
    ("Is there TV or entertainment on board?", "Some AC coaches have an entertainment system with music and videos. Availability depends on the coach, so check the trip description."),
    ("Do buses have safety belts?", "Seat belts are fitted on our newer coaches. For your own safety, please buckle up as soon as you take your seat."),
    ("Are there double-decker buses?", "On selected high-demand corridors we operate comfortable double-decker coaches with more capacity - check the vehicle type on the trip you choose."),
    ("What does the inside of the bus look like?", "The cabin has orderly rows of numbered seats, an aisle, overhead luggage racks and large windows. AC coaches add tinted glass and climate control."),

    # ------------------------------------------------------------------
    # Drivers & Safety
    # ------------------------------------------------------------------
    ("Are the drivers verified?", "Yes. Every driver holds a valid professional licence with a clean record check, and is verified and documented before being assigned to any trip."),
    ("What if the driver is late?", "Drivers are rostered well before departure so terminals almost always leave on time. If your trip starts late, the terminal keeps passengers informed of the delay."),
    ("What safety measures are in place?", "All coaches are inspected before departure, drivers follow rest-break schedules, and every vehicle carries a first-aid kit and emergency tools."),
    ("Do buses have GPS tracking?", "Yes, our fleet is GPS tracked so operations can monitor each trip in real time and respond quickly if anything goes wrong."),
    ("How is the driver's driving record checked?", "Drivers undergo background and record checks before joining, and their trips are monitored - speed and route are reviewed by the operations team."),
    ("What happens in case of an accident?", "Trained staff respond first on the scene and our 24-7 operations centre is alerted automatically via GPS. Passengers are helped and the terminal coordinates onward travel where possible."),
    ("Are drivers trained for emergencies?", "Yes - our drivers are trained in safe driving, breakdown response and emergency handling so they can act calmly if something goes wrong."),
    ("Can I report a driver?", "Yes. Any feedback about driving or conduct can be reported to our support desk with the trip details and driver name, and we will investigate."),
    ("What if the driver changes mid-journey?", "Trips on very long routes may change drivers at scheduled points to keep within rest limits. The relief driver is also fully verified and briefed."),
    ("Is there a speed limit enforced?", "Yes, coaches are electronically limited and drivers must follow the highway speed limits. The operations team monitors real-time speed data."),
    ("Do drivers take rest breaks?", "Yes. Rest schedules are built into every long trip and drivers rotate at planned stops to stay alert throughout the journey."),
    ("How are parcels and baggage kept safe?", "Luggage is stored in the secured cargo hold and handed back with your claim tag. Keep valuables with you in the cabin."),
    ("Are there staff members on board?", "Every trip has at least a trained conductor on board to help with tickets, luggage and passenger safety."),
    ("Can I see my driver's details?", "The driver's name is available at the terminal on departure day. Share your booking reference with the counter if you need it."),
    ("What if I feel unsafe during a trip?", "Alert the conductor immediately. For more serious concerns, call our support helpline - our operations centre monitors every trip."),
    ("Are buses checked before every trip?", "Yes - each coach passes a pre-departure safety inspection covering brakes, tyres, lights and cabin equipment before it is cleared for departure."),

    # ------------------------------------------------------------------
    # General / support
    # ------------------------------------------------------------------
    ("How do I contact or phone your support desk?", "You can reach our support desk through the contact form on the website, our helpline numbers, or in person at any terminal. Keep your booking reference ready."),
    ("What are the terminal timings or business hours?", "The support desk is available daily from early morning to late evening, and terminals operate on the full departure schedule, including public holidays."),
    ("Where are the terminals located?", "Our terminals are located in the main city centres along the intercity corridors we serve, with clearly signposted boarding gates and waiting areas."),
    ("How do I give feedback?", "We love feedback! Use the feedback form on the contact page or talk to our team at the terminal - comments are reviewed by operations weekly."),
    ("Can I visit the office in person?", "Yes, our main office welcomes visitors during business hours, and every terminal counter can resolve booking, payment or refund issues on the spot."),
    ("How do I make a complaint?", "Submit your complaint through the contact page or at the terminal counter. Every complaint receives a reference number and is answered by our team."),
    ("How long does support take to reply?", "Most enquiries are answered within a few hours during business hours. Complaints about service are reviewed and closed within a few working days."),
    ("Is there a helpline?", "Yes, toll-free helpline numbers are listed on the contact page and printed on your ticket, in case you need assistance at any point during your journey."),
    ("Can I connect on social media?", "Yes, we are active on the major platforms and share travel updates, offers and route news there. Links are on the website footer."),
    ("How do I track my booking?", "Your booking status is always visible in My Bus Bookings. For live departure updates, contact the terminal or check with support."),
    ("Do you serve all cities?", "We focus on the country's main intercity corridors and major cities. New routes are added based on demand - suggest your city and we will consider it."),
    ("Can you hold my seat while I decide?", "A seat is only held once a booking is confirmed. To avoid losing seats, confirm your selection - the booking process takes under a minute anyway."),
    ("Can I change my booking details?", "Changes are easiest by cancelling and rebooking. For simple changes like adding a seat or adjusting a name, contact our support desk for assistance."),
    ("What documents do I need to travel?", "Your ticket or booking reference, and a valid government ID for the check-in and safety verification at boarding."),
    ("Are pets allowed on the bus?", "Only small pets in carriers are considered, subject to route policy and prior approval from the counter. Support animals are welcomed with documentation."),
    ("Can I carry a bicycle or large items?", "Bicycles and very large items need special arrangement for the cargo hold. Please contact the terminal with the item details before your trip."),
    ("Do you offer a loyalty program?", "Frequent travellers can earn benefits through our loyalty programme - ask the counter to enrol you and accumulate points on every ticket."),
    ("Can I book tickets for corporate needs?", "Yes, corporate and group bookings are available with account billing and shared manifests. Contact our accounts department for the terms."),
    ("Are special discounts available?", "Promotional fares and festival offers appear directly on the trip page when active. Student and senior discounts are offered at selected counters."),
    ("How do I get a copy of my invoice?", "Open your booking in My Bus Bookings and use the invoice link - the official invoice is linked to every confirmed booking."),
    ("Can I use the chatbot for account help?", "The chatbot answers general questions about booking, payments, seats, tickets and support contacts. For account-specific actions, log in or contact the support desk."),
    ("What should I do if the website is slow?", "Refresh the page and try a different browser. If problems continue, contact support with a screenshot so our team can investigate."),
    ("How do I suggest a new route?", "Use the feedback form and mention the route you need - requests are reviewed by our planning team and popular corridors are added over time."),
    ("Where can I find the latest travel updates?", "Follow our social media pages and watch the notices posted at terminals for the latest announcements on routes, schedules and offers."),
]

if __name__ == "__main__":
    # Quick sanity check when run directly (e.g. during development).
    total = len(FAQ_DATA)
    assert total == 200, "FAQ_DATA must contain exactly 200 entries, got %d" % total
    assert all(isinstance(q, str) and isinstance(a, str) for q, a in FAQ_DATA)
    print("FAQ_DATA OK: %d entries" % total)